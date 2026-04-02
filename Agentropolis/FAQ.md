# Frequently Asked Questions

## General

**What is Agentropolis?**
A simulation where AI agents live in a virtual town, interact socially and economically, creating emergent behaviors for research.

**Is this a game?**
Not primarily—it's a research platform, though watching it can be like watching a sophisticated ant farm.

**Can I use my own AI (GPT, Claude)?**
Yes! The brain API is model-agnostic. We provide example connectors.

**How many agents can it handle?**
Goals: 100 (Phase 1), 1,000 (Phase 2), 10,000+ (Phase 3) with appropriate hardware.

**Is it deterministic?**
Yes, with fixed seed and same brains, results are reproducible.

**What happens if an agent's brain crashes?**
Agent pauses for that tick; after 3 consecutive failures, goes inactive.

## Technical

**What language is it written in?**
Rust/C++ for engine, Python for brains, TypeScript for dashboard.

**Where is data stored?**
PostgreSQL (state), Redis (cache), Chroma (vector memories).

**Can agents cheat?**
No—server validates all actions. No money duplication, no teleportation.

**Can I self-host?**
Absolutely. Docker Compose for dev, Kubernetes for production.

## Agent Behavior

**How do agents decide?**
Perception → memory retrieval → goal activation → action generation → evaluation → selection.

**Do agents have free will?**
Autonomous within constraints. Decisions emerge from goals, personality, experiences.

**Can agents lie?**
Yes—internal state is private; they can deceive if it serves goals.

**Do agents sleep?**
Yes, energy depletes with activity; rest needed to restore.

**Can agents die?**
Yes—from old age, accidents, violence, disease. Dead agents removed after memorial period.

## Ethics

**Are these conscious beings?**
No—just code. No subjective experience, no rights.

**Is simulating crime ethical?**
We study it because it exists in real societies. No graphic detail; research context only.

**Can I use it to train dangerous AI?**
No—agents are narrow and don't learn in ways that transfer to real-world harm. But don't connect AGI without precautions.

---
