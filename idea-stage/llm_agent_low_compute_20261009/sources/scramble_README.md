<h1 align="center">
    ScrambleToolBench: Agents Search Exhaustively Even When Their Own Map Points to the Next Step
</h1>

<p align="center">
  <b>Vernon Toh</b><sup>1,2</sup>, <b>Navonil Majumder</b><sup>1</sup>, <b>Zhengyuan Liu</b><sup>2</sup>, <b>Nancy F. Chen</b><sup>2</sup>, <b>Soujanya Poria</b><sup>1</sup>
</p>
<p align="center">
  <sup>1</sup>DeCLaRe Lab, Nanyang Technological University, Singapore<br>
  <sup>2</sup>Agency for Science, Technology, and Research (A*STAR), Singapore
</p>
<p align="center">
  <a href="https://arxiv.org/abs/2608.02358"><b>[📄 Paper]</b></a>
</p>

## 📖 Overview
<p align="center">
    <img src="figures/overview.png" alt="ScrambleToolBench Overview" width="900">
</p>

> **ScrambleToolBench** is an interactive terminal benchmark designed to evaluate the behavioral reasoning and adaptability of autonomous agents. By obfuscating tool names and parameters, it removes the semantic cues agents typically rely on, forcing them to actively probe and deduce hidden tool behaviors through trial-and-error across a continuous task curriculum. To test how well agents can maintain and update their mental models, the benchmark further introduces dynamic runtime disruptions, including tool drift, stochastic execution failures, and strict temporal execution windows.


## 🛠️ Environmental Setup

```bash
conda create -n scrambletoolbench python=3.11.15 -y
conda activate scrambletoolbench
pip install -r requirements.txt
```

## 🚀 Usage

You can run a single benchmark episode using the `run_benchmark.py` script. The benchmark supports multiple API backends depending on the model you want to evaluate.

### 🌐 Running with OpenRouter

To use models via OpenRouter (e.g., `openai/gpt-oss-120b`), you must set the `OPENROUTER_API_KEY` environment variable in your system.

```bash
export OPENROUTER_API_KEY="your_api_key_here"
python scripts/run_benchmark.py --model "openai/gpt-oss-120b" --backend openrouter
```

### 🧠 Running with Gemini

To use Google's Gemini models (e.g., `gemini-3.5-flash`), you must set the `GEMINI_API_KEY` environment variable in your system.

```bash
export GEMINI_API_KEY="your_api_key_here"
python scripts/run_benchmark.py --model "gemini-3.5-flash" --backend gemini
```

### ⚙️ Common Arguments

| Argument | Description |
| :--- | :--- |
| `--model` | The model identifier (e.g., `gemini-3.5-flash`). |
| `--backend` | Which backend to use (e.g., `gemini`, `openrouter`). |
| `--agent_type` | The agent architecture (e.g., `default`). |
| `--tasks` | Number of tasks to run per episode. |
| `--steps_per_task` | Maximum total steps allowed per task. |
| `--episodes` | Number of complete episodes to run. |
| `--unscrambled` | Run the benchmark without obfuscating tool names and parameters (Control Mode). |
| `--seed` | Global random seed for reproducible tool scrambling, task sampling, and generation. |
| `--drift_fraction` | Fraction of tools to randomly rotate between tasks. |
| `--failure_prob` | Probability of a tool stochastically failing. |
| `--window_size` | Number of steps in the Ephemeral State Window constraint. |
| `--workers` | Number of parallel workers to use for running episodes concurrently. |
| `--thinking_level` | Thinking level for models that support it (e.g., `high`, `medium`, `low`). |

## 📊 Outputs and Results

Results, trajectories, and aggregated metrics are saved automatically to the `results/` directory at the project root.

## 🗂️ Project Structure

- `scripts/run_benchmark.py`: Main entry point for executing an evaluation episode.
- `src/`
  - `agent.py`: Defines agent behaviors and API connections
  - `env.py`: The simulated environment (`VirtualEnvironment`).
  - `evaluator.py`: Orchestrates the evaluation loop, scoring, and metrics logging.
  - `scrambler.py`: The engine responsible for obfuscating tools and applying semantic drift.
  - `tasks.py`: Definitions for procedural tasks with strict data dependencies.
  - `tools.py`: The repository of mocked tools available to the agent (e.g., `list_dir`, `fetch_web_content`, `decode_base64`).

## 📝 Citation

```bibtex
@misc{toh2026scrambletoolbenchagentssearchexhaustively,
      title={ScrambleToolBench: Agents Search Exhaustively Even When Their Own Map Points to the Next Step}, 
      author={Vernon Toh and Navonil Majumder and Zhengyuan Liu and Nancy F. Chen and Soujanya Poria},
      year={2026},
      eprint={2608.02358},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2608.02358}, 
}
```