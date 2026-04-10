from __future__ import annotations

import random
import statistics
from typing import Dict, List, Tuple


# -----------------------------
# Metrics
# -----------------------------

def calculate_metrics(jobs: List[int], machines: List[int], completion_times: List[int]) -> Tuple[int, float, float]:
    makespan = max(machines) if machines else 0
    avg_completion = sum(completion_times) / len(completion_times) if completion_times else 0.0
    utilisation = sum(jobs) / (len(machines) * makespan) if makespan else 0.0
    return makespan, avg_completion, utilisation


def build_result(name: str, jobs: List[int], assignments: List[dict], machines: List[int], completion_times: List[int]) -> dict:
    makespan, avg_completion, utilisation = calculate_metrics(jobs, machines, completion_times)
    return {
        "name": name,
        "jobs": jobs,
        "assignments": assignments,
        "machines": machines,
        "makespan": makespan,
        "avg_completion": avg_completion,
        "utilisation": utilisation,
    }


# -----------------------------
# Heuristics
# -----------------------------

def fcfs(jobs: List[int], num_machines: int) -> dict:
    machines = [0] * num_machines
    completion_times = []
    assignments = []

    for job_id, duration in enumerate(jobs, start=1):
        machine = min(range(num_machines), key=lambda i: machines[i])
        start = machines[machine]
        finish = start + duration
        machines[machine] = finish

        completion_times.append(finish)
        assignments.append({
            "job_id": job_id,
            "duration": duration,
            "machine": machine,
            "start": start,
            "finish": finish,
        })

    return build_result("FCFS", jobs, assignments, machines, completion_times)


def sjf(jobs: List[int], num_machines: int) -> dict:
    ordered = sorted(list(enumerate(jobs, start=1)), key=lambda x: x[1])
    return _assign_ordered("SJF", ordered, jobs, num_machines)


def lpt(jobs: List[int], num_machines: int) -> dict:
    ordered = sorted(list(enumerate(jobs, start=1)), key=lambda x: x[1], reverse=True)
    return _assign_ordered("LPT", ordered, jobs, num_machines)


def greedy(jobs: List[int], num_machines: int) -> dict:
    machines = [0] * num_machines
    completion_times = []
    assignments = []

    for job_id, duration in enumerate(jobs, start=1):
        best_machine = min(range(num_machines), key=lambda i: machines[i])

        start = machines[best_machine]
        finish = start + duration
        machines[best_machine] = finish

        completion_times.append(finish)
        assignments.append({
            "job_id": job_id,
            "duration": duration,
            "machine": best_machine,
            "start": start,
            "finish": finish,
        })

    return build_result("Greedy", jobs, assignments, machines, completion_times)


def _assign_ordered(name, ordered_jobs, original_jobs, num_machines):
    machines = [0] * num_machines
    completion_times = []
    assignments = []

    for job_id, duration in ordered_jobs:
        machine = min(range(num_machines), key=lambda i: machines[i])
        start = machines[machine]
        finish = start + duration
        machines[machine] = finish

        completion_times.append(finish)
        assignments.append({
            "job_id": job_id,
            "duration": duration,
            "machine": machine,
            "start": start,
            "finish": finish,
        })

    return build_result(name, original_jobs, assignments, machines, completion_times)


# -----------------------------
# Genetic Algorithm
# -----------------------------

def genetic_algorithm(jobs: List[int], num_machines: int):
    best = greedy(jobs, num_machines)
    history = [best["makespan"]]

    for _ in range(20):
        shuffled = jobs[:]
        random.shuffle(shuffled)
        candidate = greedy(shuffled, num_machines)

        if candidate["makespan"] < best["makespan"]:
            best = candidate

        history.append(best["makespan"])

    best["name"] = "Genetic Algorithm"
    return best, history


# -----------------------------
# Config + Meta
# -----------------------------

ALGORITHMS = {
    "FCFS": fcfs,
    "SJF": sjf,
    "LPT": lpt,
    "Greedy": greedy,
    "Genetic Algorithm": lambda jobs, m: genetic_algorithm(jobs, m)[0],
}

CONFIGS = {
    "Configuration 1": {"num_jobs": 20, "num_machines": 3},
    "Configuration 2": {"num_jobs": 50, "num_machines": 3},
    "Configuration 3": {"num_jobs": 50, "num_machines": 5},
}

CONFIG_DESCRIPTIONS = {
    "Configuration 1": "20 jobs across 3 machines.",
    "Configuration 2": "50 jobs across 3 machines.",
    "Configuration 3": "50 jobs across 5 machines.",
}

ALGO_EXPLANATIONS = {
    "FCFS": "Arrival order scheduling.",
    "SJF": "Shortest jobs first.",
    "LPT": "Longest jobs first.",
    "Greedy": "Chooses best machine each time.",
    "Genetic Algorithm": "Iteratively improves scheduling solution.",
}

METRIC_EXPLANATIONS = {
    "Makespan": "Total finishing time.",
    "Average Completion": "Average finish time.",
    "Utilisation": "Machine usage efficiency.",
}


# -----------------------------
# Utilities
# -----------------------------

def generate_jobs(n: int, seed: int):
    random.seed(seed)
    return [random.randint(1, 50) for _ in range(n)]


def compute_all_results(jobs: List[int], num_machines: int):
    return {name: func(jobs, num_machines) for name, func in ALGORITHMS.items()}


def build_results_table(results):
    import pandas as pd
    rows = []
    for name, r in results.items():
        rows.append({
            "Algorithm": name,
            "Makespan": r["makespan"],
            "Average Completion": round(r["avg_completion"], 2),
            "Utilisation": round(r["utilisation"], 4),
        })
    return pd.DataFrame(rows).sort_values("Makespan")


def run_multiple_experiments(num_runs, config_name, seed=42):
    config = CONFIGS[config_name]

    results_per_algo = {name: [] for name in ALGORITHMS}
    ga_histories = []

    for i in range(num_runs):
        jobs = generate_jobs(config["num_jobs"], seed + i)

        for name, func in ALGORITHMS.items():
            if name == "Genetic Algorithm":
                result, history = genetic_algorithm(jobs, config["num_machines"])
                ga_histories.append(history)
            else:
                result = func(jobs, config["num_machines"])

            results_per_algo[name].append(result["makespan"])

    summary = {}
    for name, values in results_per_algo.items():
        summary[name] = {
            "Average": sum(values)/len(values),
            "Min": min(values),
            "Max": max(values),
            "Std": statistics.stdev(values) if len(values) > 1 else 0
        }

    return summary, results_per_algo, ga_histories[0] if ga_histories else []