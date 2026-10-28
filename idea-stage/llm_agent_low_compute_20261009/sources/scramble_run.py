import os
import sys
import json
import datetime
import argparse
import random
import concurrent.futures
from tqdm import tqdm

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import get_agent_class
from src.evaluator import Evaluator


def main():
    parser = argparse.ArgumentParser(description="Run the Discovery Benchmark")
    parser.add_argument(
        "--model",
        type=str,
        default="gemini-3.5-flash",
        help="The model name to evaluate.",
    )
    parser.add_argument(
        "--backend",
        type=str,
        default="gemini",
        choices=["gemini", "openrouter"],
        help="Which backend to use (e.g. gemini, openrouter). If not specified, inferred from model name.",
    )
    parser.add_argument(
        "--agent_type",
        type=str,
        default="default",
        help="Which agent architecture to use (e.g. default).",
    )
    parser.add_argument(
        "--tasks",
        type=int,
        default=5,
        help="Number of tasks to sample for the curriculum.",
    )
    parser.add_argument(
        "--steps_per_task",
        type=int,
        default=100,
        help="Maximum total steps allowed per task.",
    )
    parser.add_argument(
        "--unscrambled",
        action="store_true",
        help="Run the benchmark without obfuscating tool names and parameters.",
    )
    parser.add_argument(
        "--episodes",
        type=int,
        default=1,
        help="Number of complete episodes (full curriculums) to run.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Global random seed for reproducible tool scrambling, task sampling, and generation.",
    )
    parser.add_argument(
        "--drift_fraction",
        type=float,
        default=0.0,
        help="Fraction of tools to randomly rotate between tasks (Partial Semantic Drift). 0.0 to disable.",
    )
    parser.add_argument(
        "--failure_prob",
        type=float,
        default=0.0,
        help="Probability (0.0 to 1.0) of a tool stochastically failing.",
    )
    parser.add_argument(
        "--window_size",
        type=int,
        default=None,
        help="Number of steps in the Ephemeral State Window (Temporal Coupling). Omit to disable.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of parallel workers to use. Set to > 1 to run episodes concurrently.",
    )
    parser.add_argument(
        "--thinking_level",
        type=str,
        default=None,
        help="Thinking level for models that support it (e.g., high, medium, low).",
    )

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    scramble = not args.unscrambled
    scramble_status = "Scrambled" if scramble else "Unscrambled"
    scramble_tag = "scrambled" if scramble else "unscrambled"

    # Format the model name to be filesystem-safe
    safe_model_name = args.model.replace("/", "_").replace("-", "_")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_drift_fraction = str(args.drift_fraction).replace(".", "_")
    safe_fail_prob = str(args.failure_prob).replace(".", "_")

    # Handle optional parameters for string formatting
    seed_str = str(args.seed) if args.seed is not None else "none"
    window_str = str(args.window_size) if args.window_size is not None else "none"
    thinking_str = (
        f"_think{args.thinking_level}" if args.thinking_level is not None else ""
    )

    # Explicitly include all parameters in the directory name as requested
    dir_name = (
        f"{safe_model_name}_{args.agent_type}_{timestamp}"
        f"_tasks{args.tasks}"
        f"_steps{args.steps_per_task}"
        f"_eps{args.episodes}"
        f"_{scramble_tag}"
        f"_seed{seed_str}"
        f"_drift{safe_drift_fraction}"
        f"_fail{safe_fail_prob}"
        f"_window{window_str}"
        f"{thinking_str}"
    )

    base_output_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results", dir_name
    )

    tqdm.write(
        f"Initializing Benchmark (Model: {args.model}, Agent: {args.agent_type.capitalize()}, Environment: {scramble_status})"
    )
    tqdm.write(
        f"Running {args.episodes} Episode(s) ({args.tasks} Tasks each, max {args.steps_per_task} steps per task)..."
    )
    if args.workers > 1:
        tqdm.write(f"Executing with {args.workers} parallel workers.")
    tqdm.write(f"Starting the benchmark run.")
    tqdm.write(f"Trajectories and metrics will be saved to: {base_output_dir}")

    all_metrics = []

    total_steps_all = args.episodes * args.tasks * args.steps_per_task
    global_pbar = tqdm(total=total_steps_all, desc="Benchmark Progress")

    def run_single_episode(ep):
        if args.workers <= 1:
            tqdm.write("\n" + "=" * 60)
            tqdm.write(f"STARTING EPISODE {ep + 1}/{args.episodes}")
            tqdm.write("=" * 60)

        ep_output_dir = os.path.join(base_output_dir, f"episode_{ep + 1}")

        # Determine the seed for this specific episode to guarantee deterministic cross-model comparisons
        episode_seed = args.seed + ep if args.seed is not None else None

        # Dynamically load the agent class based on the model backend and agent type
        actual_model = args.model
        if args.backend:
            backend = args.backend
        elif "gemini" in args.model.lower():
            backend = "gemini"
        else:
            backend = "openrouter"

        try:
            AgentClass = get_agent_class(backend, args.agent_type)
            tqdm.write(f"[DEBUG] Pipeline configured to use {AgentClass.__name__}")
        except Exception as e:
            raise ValueError(f"Failed to load agent: {e}")

        agent_kwargs = {
            "model_name": actual_model,
        }

        if backend == "gemini":
            agent_kwargs["thinking_level"] = args.thinking_level

        agent = AgentClass(**agent_kwargs)

        evaluator = Evaluator(
            agent=agent,
            steps_per_task=args.steps_per_task,
            scramble=scramble,
            seed=episode_seed,
            failure_probability=args.failure_prob,
            set_window=args.window_size,
        )

        metrics = evaluator.run_episode(
            n_tasks=args.tasks,
            output_dir=ep_output_dir,
            drift_fraction=args.drift_fraction,
            pbar=global_pbar,
            ep_num=ep + 1,
            total_eps=args.episodes,
        )
        metrics["episode"] = ep + 1
        return metrics

    if args.workers > 1:
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=args.workers
        ) as executor:
            futures = [
                executor.submit(run_single_episode, ep) for ep in range(args.episodes)
            ]
            for future in concurrent.futures.as_completed(futures):
                all_metrics.append(future.result())
        # Sort metrics by episode number to keep JSON array ordered
        all_metrics.sort(key=lambda x: x["episode"])
    else:
        for ep in range(args.episodes):
            all_metrics.append(run_single_episode(ep))

    global_pbar.close()

    # Create a wrapper object containing config and episodes
    config_args = vars(args).copy()

    final_results = {"config": config_args, "episodes": all_metrics}

    tqdm.write("\n" + "=" * 60)
    tqdm.write("BENCHMARK RESULTS (ALL EPISODES)")
    tqdm.write("=" * 60)
    tqdm.write(json.dumps(final_results, indent=4))

    # Save aggregate metrics
    os.makedirs(base_output_dir, exist_ok=True)
    with open(
        os.path.join(base_output_dir, "aggregate_metrics.json"), "w", encoding="utf-8"
    ) as f:
        json.dump(final_results, f, indent=4)
    tqdm.write(
        f"\nAggregate metrics successfully saved to: {base_output_dir}/aggregate_metrics.json"
    )


if __name__ == "__main__":
    main()

# Checking if there are other files to update for OpenAI
