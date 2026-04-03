"""LLM-powered brain for agents using OpenAI-compatible APIs."""
import os
import json
import logging
import random
import asyncio
import httpx
from typing import Dict, Any, Optional, List
from uuid import UUID
from datetime import datetime, timezone

from dotenv import load_dotenv

# Load .env at module import time
load_dotenv(os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    ".env",
))

from agentropolis.models import Agent, Location
from .base import Brain, BrainDecision
from .simple import SimpleBrain

logger = logging.getLogger(__name__)

# ---------- Configuration ----------
_LLM_BRAIN_CONFIG = {
    "api_base": os.getenv("LLM_API_BASE", "https://openrouter.ai/api/v1"),
    "api_key": os.getenv("LLM_API_KEY", ""),
    "model": os.getenv("LLM_MODEL", "meta-llama/llama-3.2-3b-instruct"),
    "decision_cooldown_ticks": int(os.getenv("LLM_DECISION_COOLDOWN_TICKS", "100")),
    "action_cooldown_ticks": int(os.getenv("LLM_ACTION_COOLDOWN_TICKS", "20")),
    "timeout": int(os.getenv("LLM_REQUEST_TIMEOUT", "15")),
}

VALID_ACTIONS = ["move", "work", "socialize", "idle", "wander"]

# Personality templates - random personas assigned per-agent to create variety
AGENT_PERSONALITIES = [
    "You are an ambitious workaholic. You prefer earning money and being productive.",
    "You are highly social and extroverted. You love meeting and chatting with others.",
    "You are a wanderer who loves exploration. You prefer moving around and discovering places.",
    "You are a laid-back, relaxed person. You enjoy idle time and going with the flow.",
    "You are cautious and need-driven. You prioritize your health, energy, and hunger above all else.",
    "You are socially awkward but trying. You sometimes socialize but often wander alone.",
    "You are always hungry for experience. You seek food and social events constantly.",
    "You are money-focused but also need to maintain relationships and stay healthy.",
    "You are a restless spirit. You can't stand staying still - always moving or working.",
    "You are a balanced person. You try to keep all needs in harmony - some work, some social, some rest.",
]

SYSTEM_PROMPT = """You are {name}, an AI agent living in the virtual town of Agentropolis.

{personality}

CURRENT STATUS:
- Energy: {energy}/100  (if < 30, you should rest)
- Hunger: {hunger}/100  (if > 70, you should eat)
- Happiness: {happiness}/100  (if low, socialize or find entertainment)
- Health: {health}/100
- Money: {money:.1f}  (if < 50, consider working)

TICK: {tick_counter} (this is how long you've been alive)
LAST actions taken: {recent_actions}

Based on your personality, current needs, and what you've done recently, choose EXACTLY ONE action.
DO NOT repeat the same action if you've done it in the last few decisions - BE DIVERSE.
Respond with ONLY valid JSON.

Available actions and when to use them:
- "move" - go to a specific location. Set target_name to one of the locations listed.
- "work" - earn money. Set target_name to a workplace (or "any work location").
- "socialize" - chat with another agent. Set target_name to their exact name.
- "wander" - roam around without destination (no target_name needed).
- "idle" - stay put and rest (use ONLY if energy < 30 or nothing else fits).

IMPORTANT: If your energy > 50 and hunger < 50, you MUST take an active action (move, work, socialize, or wander). Do NOT idle unless absolutely necessary.

Respond ONLY with this JSON format:
{{"action": "action_name", "target_name": "name or null", "reasoning": "brief creative explanation"}}"""


class LLMBrain(Brain):
    """An LLM-powered brain that makes decisions via an AI model call."""

    def __init__(self, agent_id: UUID):
        super().__init__(agent_id)
        self._last_llm_decision_tick = -999999
        self._cached_decision: Optional[BrainDecision] = None
        self._cached_action_remaining = 0
        self._tick_counter = 0
        self._http_client: Optional[httpx.AsyncClient] = None
        self._request_count = 0
        self._personality = random.choice(AGENT_PERSONALITIES)
        self._consecutive_idle_count = 0
        self._simple_brain = SimpleBrain(agent_id)  # fallback brain
        self._last_action_types: List[str] = []  # track recent actions for variety

    def _get_client(self) -> httpx.AsyncClient:
        if self._http_client is None or self._http_client.is_closed:
            self._http_client = httpx.AsyncClient(timeout=_LLM_BRAIN_CONFIG["timeout"])
        return self._http_client

    async def close(self):
        if self._http_client and not self._http_client.is_closed:
            await self._http_client.aclose()
            self._http_client = None

    def _build_prompt(self, agent: Agent, world_state: Dict[str, Any]) -> str:
        """Build the user context for the LLM."""
        locations = world_state.get("locations", [])
        location_list = []
        for loc in locations:
            services = []
            for attr in ["provides_food", "provides_work", "provides_entertainment",
                         "provides_healthcare", "provides_sleep", "provides_shopping"]:
                if getattr(loc, attr, False):
                    services.append(attr.replace("provides_", ""))
            loc_services = ", ".join(services) if services else "general"
            location_list.append(f"- {loc.name} ({loc_services})")

        all_agents = world_state.get("agents", [])
        other_agents = [a for a in all_agents if a.id != agent.id]
        agent_list = []
        for a in other_agents[:15]:
            agent_list.append(f"- {a.name} (occupation: {a.occupation or 'none'}, "
                              f"happiness: {a.happiness}, energy: {a.energy})")

        location_ctx = "\n".join(location_list) if location_list else "No locations."
        agent_ctx = "\n".join(agent_list) if agent_list else "No other agents nearby."

        recent_actions = ", ".join(self._last_action_types[-3:]) if self._last_action_types else "None yet"

        return f"""Location options:\n{location_ctx}\n\nOther agents nearby:\n{agent_ctx}\n\nYour last 3 actions: [{recent_actions}]""", recent_actions

    async def _call_llm(self, agent: Agent, world_state: Dict[str, Any]) -> tuple[BrainDecision, str]:
        """Make a real LLM call and return a decision + the chosen action type."""
        sys_prompt = SYSTEM_PROMPT.format(
            name=agent.name,
            personality=self._personality,
            energy=agent.energy,
            hunger=agent.hunger,
            happiness=agent.happiness,
            health=agent.health,
            money=agent.money,
            tick_counter=self._tick_counter,
            recent_actions=", ".join(self._last_action_types[-5:]) if self._last_action_types else "None yet",
        )
        user_prompt, _ = self._build_prompt(agent, world_state)

        api_base = _LLM_BRAIN_CONFIG["api_base"]
        api_key = _LLM_BRAIN_CONFIG["api_key"]
        model = _LLM_BRAIN_CONFIG["model"]

        if not api_key:
            logger.error(f"[LLMBrain] No API key for {agent.name}")
            return BrainDecision(
                action_type="idle", parameters={"duration": 1, "llm_reasoning": "No API key"},
                confidence=0.1, reasoning="LLM not configured",
            ), "idle"

        url = f"{api_base.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://agentropolis.local",
            "X-Title": "Agentropolis",
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.8,
            "max_tokens": 256,
        }

        try:
            client = self._get_client()
            response = await client.post(url, json=payload, headers=headers)
            self._request_count += 1

            if response.status_code != 200:
                logger.error(
                    f"[LLMBrain] API error for {agent.name}: HTTP {response.status_code}: "
                    f"{response.text[:200]}"
                )
                return self._fallback_decision(agent, "API error"), "idle"

            data = response.json()
            content = data["choices"][0]["message"]["content"].strip()
            content = content.strip().lstrip("```json").strip("```").strip()

            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                start = content.find("{")
                end = content.rfind("}") + 1
                if start >= 0 and end > start:
                    result = json.loads(content[start:end])
                else:
                    logger.warning(f"[LLMBrain] Bad JSON from LLM for {agent.name}: {content[:200]}")
                    return self._fallback_decision(agent, "Bad LLM response"), "idle"

            action = result.get("action", "idle").strip().lower()
            if action not in VALID_ACTIONS:
                action = "idle"

            target_name = result.get("target_name")
            reasoning = result.get("reasoning", "LLM decision")

            # Enforce variety - if action same as last 3, force a different one
            if len(self._last_action_types) >= 3 and all(a == action for a in self._last_action_types[-3:]):
                logger.debug(f"[LLMBrain] {agent.name}: forcing variety away from {action}")
                action = self._pick_variety_action(action)

            params = {
                "duration": 1,
                "llm_reasoning": reasoning,
                "llm_model": model,
                "llm_request": self._request_count,
            }

            if action in ("move", "work", "socialize"):
                target_id = self._resolve_target(target_name, agent, world_state)
                if target_id:
                    return BrainDecision(
                        action_type=action,
                        target_id=UUID(target_id) if isinstance(target_id, str) else target_id,
                        parameters=params,
                        confidence=0.8,
                        reasoning=f"[LLM] {reasoning} (model={model})",
                    ), action
                # Target not found, wander instead
                return BrainDecision(
                    action_type="wander", parameters={"wander": True, **params},
                    confidence=0.5, reasoning=f"[LLM] {reasoning} (target not found, wandering)",
                ), "wander"

            elif action == "wander":
                return BrainDecision(
                    action_type="wander", parameters={"wander": True, **params},
                    confidence=0.6, reasoning=f"[LLM] {reasoning}",
                ), "wander"
            else:
                return BrainDecision(
                    action_type="idle", parameters={"duration": 2, **params},
                    confidence=0.5, reasoning=f"[LLM] {reasoning}",
                ), "idle"

        except Exception as e:
            logger.error(f"[LLMBrain] Error calling LLM for {agent.name}: {e}")
            return self._fallback_decision(agent, str(e)), "idle"

    def _fallback_decision(self, agent: Agent, reason: str) -> BrainDecision:
        """Call SimpleBrain as fallback."""
        # Just return a simple random decision instead of calling the full SimpleBrain
        actions = ["move", "work", "socialize", "wander", "idle"]
        action = random.choice(actions)
        return BrainDecision(
            action_type="idle", parameters={"duration": 2, "llm_reasoning": f"Fallback: {reason}"},
            confidence=0.3, reasoning=f"LLM failed ({reason}), using idle fallback",
        )

    @staticmethod
    def _pick_variety_action(exclude: str) -> str:
        """Pick an action different from exclude."""
        options = [a for a in "move socialize wander work idle".split() if a != exclude]
        return random.choice(options)

    def _resolve_target(self, target_name: Optional[str], agent: Agent,
                        world_state: Dict[str, Any]) -> Optional[str]:
        """Resolve a target name to a UUID (agent or location)."""
        if not target_name or target_name in ("null", "any", "anyone", None):
            return None

        for loc in world_state.get("locations", []):
            if loc.name.lower() == target_name.lower():
                return str(loc.id)
        for a in world_state.get("agents", []):
            if a.name.lower() == target_name.lower() and a.id != agent.id:
                return str(a.id)

        # Fuzzy match
        name_part = target_name.split()[0].lower()
        for loc in world_state.get("locations", []):
            if name_part in loc.name.lower():
                return str(loc.id)
        for a in world_state.get("agents", []):
            if name_part in a.name.lower() and a.id != agent.id:
                return str(a.id)
        return None

    async def decide(self, agent: Agent, world_state: Dict[str, Any]) -> BrainDecision:
        """Decide: LLM call on cooldown, cached decision between calls."""
        self._tick_counter += 1

        # Return cached decision if still within cooldown
        if (self._cached_decision and
                0 < self._tick_counter - self._last_llm_decision_tick < _LLM_BRAIN_CONFIG["decision_cooldown_ticks"]):
            return self._cached_decision

        # Time for a fresh LLM call
        decision, action_type = await self._call_llm(agent, world_state)
        self._last_llm_decision_tick = self._tick_counter
        self._cached_decision = decision
        self._last_action_types.append(action_type)
        if len(self._last_action_types) > 10:
            self._last_action_types = self._last_action_types[-10:]

        self.remember({
            "action": action_type,
            "reasoning": decision.reasoning,
            "tick": self._tick_counter,
            "energy": agent.energy,
            "hunger": agent.hunger,
            "money": agent.money,
        })

        return decision
