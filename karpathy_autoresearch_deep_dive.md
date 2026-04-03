# Deep Dive: Andrej Karpathy's AI Autoresearch Project

## Overview

Andrej Karpathy's `autoresearch` repository represents an experimental approach to autonomous AI research where an AI agent iteratively improves its own training code through small, controlled experiments. The core idea is to give an AI agent a manageable LLM training setup and let it autonomously experiment overnight—modifying code, training for short fixed intervals, evaluating results, and keeping or discarding changes based on performance.

## How It Works

### Core Components

1. **`prepare.py`** - Fixed constants, one-time data preparation (downloads training data, trains BPE tokenizer), and runtime utilities (dataloader, evaluation). **Not modified by the agent.**

2. **`train.py`** - The single file the agent edits. Contains:
   - Full GPT model implementation
   - Optimizer (Muon + AdamW)
   - Training loop
   - Everything is fair game: architecture, hyperparameters, optimizer, batch size, etc.
   - **This file is edited and iterated on by the agent**

3. **`program.md`** - Baseline instructions for one agent. Point your agent here and let it go.
   - **This file is edited and iterated on by the human** (serves as the agent's "skill" or instruction set)

4. **`pyproject.toml`** - Dependencies (primarily PyTorch and uv)

### Experimental Process

- Training runs for a **fixed 5-minute time budget** (wall clock, excluding startup/compilation)
- Metric: **val_bpb** (validation bits per byte) - lower is better, vocabulary-size independent
- After each 5-minute run:
  - Agent evaluates if validation performance improved
  - Keeps changes if better, discards if worse
  - Continues iterating with new modifications
- Expected throughput: ~12 experiments/hour, ~100 experiments overnight

### Key Design Choices

1. **Single File to Modify** - Agent only touches `train.py`, keeping scope manageable and diffs reviewable
2. **Fixed Time Budget** - Ensures experiments are comparable regardless of architectural changes
3. **Self-Contained** - No external dependencies beyond PyTorch and small packages
4. **No Distributed Training** - Single GPU, one file, one metric for simplicity

## Technical Details

### Model Architecture (in train.py)
- GPT-style transformer with configurable depth
- Muon optimizer combined with AdamW
- Custom attention mechanisms (including potential Flash Attention alternatives)
- Vocabulary size: 8192 (byte-level BPE tokenizer)
- Sequence length: 1024 tokens
- Evaluation on held-out validation set

### Data Pipeline
- Uses TinyStories dataset (or similar text corpora) for training
- BPE tokenizer trained on training data
- Fixed evaluation token count for consistent metrics

### Agent Interaction Pattern
1. Human points agent to `program.md` for initial instructions
2. Agent reads `program.md` to understand its task
3. Agent examines `train.py` and proposes modifications
4. Agent applies changes to `train.py`
5. Agent runs training for exactly 5 minutes
6. Agent evaluates results (val_bpb metric)
7. Agent decides to keep or revert changes
8. Cycle repeats with new hypotheses

## Running the System

### Requirements
- Single NVIDIA GPU (tested on H100)
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager

### Setup
```bash
# 1. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Install dependencies
uv sync

# 3. Download data and train tokenizer (one-time, ~2 min)
uv run prepare.py

# 4. Manual test run (~5 min)
uv run train.py
```

### Autonomous Mode
After verifying setup works:
```
Hi have a look at program.md and let's kick off a new experiment! let's do the setup first.
```
Then let the agent operate autonomously, editing `train.py` and `program.md` as needed.

## Notable Forks (Platform Adaptations)
- [miolini/autoresearch-macos](https://github.com/miolini/autoresearch-macos) - MacOS
- [trevin-creator/autoresearch-mlx](https://github.com/trevin-creator/autoresearch-mlx) - MacOS (MLX)
- [jsegov/autoresearch-win-rtx](https://github.com/jsegov/autoresearch-win-rtx) - Windows RTX
- [andyluo7/autoresearch](https://github.com/andyluo7/autoresearch) - AMD GPU

## Considerations for Hermes Agent Implementation

### Potential Adaptations for Hermes

1. **Domain Specialization** 
   - Instead of general LLM training, focus on Hermes-specific tasks:
     - Improving document processing pipelines
     - Enhancing OCR accuracy for receipts
     - Optimizing SQL queries for meal planner database
     - Refining cron job scheduling logic
     - Improving memory/skill retrieval relevance

2. **Modified Feedback Loop**
   - Replace val_bpb with domain-specific metrics:
     - Receipt processing accuracy (field extraction correctness)
     - Task completion rate for delegated subtasks
     - User satisfaction scores from clarifications
     - Reduction in redundant tool calls
     - Memory/skill hit rate improvement

3. **Safe Experimentation Boundaries**
   - Limit agent to modifying non-critical files:
     - Skill templates and references
     - Documentation and examples
     - Non-production configuration
     - Test scripts and prototypes
   - Use sandboxed environments for risky experiments
   - Implement rollback mechanisms for failed experiments

4. **Integration with Existing Hermes Systems**
   - Leverage `delegate_task` for spawning research subagents
   - Use `memory` and `skill_manage` to persist successful improvements
   - Employ `session_search` to avoid repeating failed experiments
   - Connect to existing cron system for scheduled research cycles

5. **Program.md Equivalent for Hermes**
   - Create evolving instruction files that guide research agents:
     - Current hypotheses to test
     - Constraints and boundaries
     - Success criteria definition
     - Resource limits (time, compute, API calls)
     - Safety guidelines

### Implementation Approach

#### Phase 1: Prototype
- Identify a small, well-defined Hermes component (e.g., receipt field extraction heuristics)
- Create a metrics system to measure improvement
- Set up agent with ability to modify specific rule files
- Run short experiments (5-15 minute cycles)

#### Phase 2: Expansion
- Extend to multiple components (memory organization, skill creation, etc.)
- Implement more sophisticated hypothesis generation
- Add collaboration between multiple research agents
- Create visualization of research progress over time

#### Phase 3: Production Integration
- Successful experiments automatically create/update skills
- Failed experiments logged for future reference
- Research agents can propose new skill categories
- Periodic research cycles during low-usage times

## Challenges and Mitigations

### 1. **Defining Appropriate Metrics**
   - Challenge: Research progress isn't always linearly measurable
   - Mitigation: Use composite metrics, combine quantitative with periodic qualitative review

### 2. **Avoiding Local Maxima**
   - Challenge: Agent might optimize for narrow metric without broader improvement
   - Mitigation: Periodically reset to baseline, encourage exploratory changes, novelty rewards

### 3. **Safety and Stability**
   - Challenge: Unconstrained self-modification risks breaking core functionality
   - Mitigation: Sandboxing, immutable core components, comprehensive test suites, gradual rollout

### 4. **Compute Efficiency**
   - Challenge: Research cycles consume resources
   - Mitigation: Schedule during off-hours, use inexpensive compute instances, early stopping criteria

### 5. **Knowledge Preservation**
   - Challenge: Successful experiments might be lost if not properly documented
   - Mitigation: Automatic skill creation from successful experiments, detailed experiment logs

## Connection to Broader AI Research Concepts

Karpathy's autoresearch touches on several advanced AI concepts:

1. **Recursive Self-Improvement** - AI systems that can improve their own architecture
2. **Meta-Learning** - Learning to learn more effectively
3. **Autonomous Scientific Discovery** - AI conducting hypothesis-driven experimentation
4. **Swarm Intelligence** - Multiple agents collaborating on research problems
5. **Neural Architecture Search** - Automated discovery of optimal model structures
6. **Hyperparameter Optimization** - Automated tuning of learning parameters

## References and Further Reading

1. [autoresearch GitHub Repository](https://github.com/karpathy/autoresearch)
2. [Karpathy's Twitter announcement](https://x.com/karpathy/status/2029701092347630069)
3. [Follow-up Twitter thread](https://x.com/karpathy/status/2031135152349524125)
4. [nanochat parent repository](https://github.com/karpathy/nanochat) (the full-featured version)
5. [Dummy's Guide to Neural Networks](https://x.com/hooeem/status/2030720614752039185) (referenced in README)
6. [TinyStories Dataset](https://huggingface.co/datasets/karpathy/tinystories-gpt4-clean) (recommended for smaller compute)

## Conclusion

Karpathy's autoresearch provides a compelling template for creating autonomous improvement cycles in AI systems. While focused on LLM training in the original implementation, the core principles—fixed-time experiments, single-file modification, clear metrics, and human-guided instruction files—can be adapted to improve various aspects of the Hermes Agent system.

The key insight is that meaningful self-improvement doesn't require massive compute or revolutionary algorithms; consistent, small, guided iterations can accumulate into significant improvements over time. By adapting this approach to Hermes' specific domains (document processing, memory management, skill creation, etc.), we could create an agent that not only assists users but continuously enhances its own capabilities.