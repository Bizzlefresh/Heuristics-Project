from __future__ import annotations

import random
from typing import Dict, List, Tuple


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


def fcfs(jobs: List[int], num_machines: int) -> dict:
    machines = [0] * num_machines
    completion_times: List[int] = []
    assignments: List[dict] = []

    for job_id, duration in enumerate(jobs, start=1):
        machine = min(range(num_machines), key=lambda i: machines[i])
        start = machines[machine]
        finish = start + duration
        machines[machine] = finish
        completion_times.append(finish)
        assignments.append(
            {
                "job_id": job_id,
                "duration": duration,
                "machine": machine,
                "start": start,
                "finish": finish,
                "order_reason": "Jobs stay in arrival order.",
            }
        )

    return build_result("FCFS", jobs, assignments, machines, completion_times)


def sjf(jobs: List[int], num_machines: int) -> dict:
    ordered = sorted(list(enumerate(jobs, start=1)), key=lambda x: x[1])
    return _assign_ordered("SJF", ordered, jobs, num_machines, "Shortest remaining duration scheduled first.")


def lpt(jobs: List[int], num_machines: int) -> dict:
    ordered = sorted(list(enumerate(jobs, start=1)), key=lambda x: x[1], reverse=True)
    return _assign_ordered("LPT", ordered, jobs, num_machines, "Longest jobs scheduled first to balance load.")


def greedy(jobs: List[int], num_machines: int) -> dict:
    machines = [0] * num_machines
    completion_times: List[int] = []
    assignments: List[dict] = []

    for job_id, duration in enumerate(jobs, start=1):
        best_machine = None
        best_makespan = float("inf")

        for i in range(num_machines):
            temp = machines.copy()
            temp[i] += duration
            projected_makespan = max(temp)
            if projected_makespan < best_makespan:
                best_makespan = projected_makespan
                best_machine = i

        start = machines[best_machine]
        finish = start + duration
        machines[best_machine] = finish
        completion_times.append(finish)
        assignments.append(
            {
                "job_id": job_id,
                "duration": duration,
                "machine": best_machine,
                "start": start,
                "finish": finish,
                "order_reason": "Current job placed on machine with best projected makespan.",
            }
        )

    return build_result("Greedy", jobs, assignments, machines, completion_times)


def _assign_ordered(name: str, ordered_jobs: List[Tuple[int, int]], original_jobs: List[int], num_machines: int, reason: str) -> dict:
    machines = [0] * num_machines
    completion_times: List[int] = []
    assignments: List[dict] = []

    for job_id, duration in ordered_jobs:
        machine = min(range(num_machines), key=lambda i: machines[i])
        start = machines[machine]
        finish = start + duration
        machines[machine] = finish
        completion_times.append(finish)
        assignments.append(
            {
                "job_id": job_id,
                "duration": duration,
                "machine": machine,
                "start": start,
                "finish": finish,
                "order_reason": reason,
            }
        )

    return build_result(name, original_jobs, assignments, machines, completion_times)


ALGORITHMS = {
    "FCFS": fcfs,
    "SJF": sjf,
    "LPT": lpt,
    "Greedy": greedy,
}

CONFIGS = {
    "Configuration 1": {"num_jobs": 20, "num_machines": 3},
    "Configuration 2": {"num_jobs": 50, "num_machines": 3},
    "Configuration 3": {"num_jobs": 50, "num_machines": 5},
}

CONFIG_DESCRIPTIONS = {
    "Configuration 1": "20 jobs across 3 machines. Good for explaining the idea clearly.",
    "Configuration 2": "50 jobs across 3 machines. Higher load with fewer machines.",
    "Configuration 3": "50 jobs across 5 machines. More machines, more parallelism.",
}

ALGO_EXPLANATIONS = {
    "FCFS": "First Come First Serve keeps the original arrival order of jobs and always sends the next job to the earliest available machine.",
    "SJF": "Shortest Job First sorts jobs from smallest to largest duration, then schedules them onto the earliest available machine.",
    "LPT": "Longest Processing Time sorts jobs from largest to smallest duration so long jobs are placed early and the machine loads are often more balanced.",
    "Greedy": "Greedy keeps the arrival order but, for each next job, checks every machine and chooses the one that gives the smallest projected makespan at that moment.",
}

METRIC_EXPLANATIONS = {
    "Makespan": "The total finishing time of the whole schedule. It is the maximum machine finish time, so lower is better.",
    "Average Completion": "The average of all job finish times. Lower means jobs tend to finish earlier on average.",
    "Utilisation": "Total busy time divided by (number of machines × makespan). Values closer to 1 mean the machines are kept busy for most of the schedule.",
}


def generate_jobs(n: int, seed: int, min_time: int = 1, max_time: int = 50) -> List[int]:
    rng = random.Random(seed)
    return [rng.randint(min_time, max_time) for _ in range(n)]


def compute_all_results(jobs: List[int], num_machines: int) -> Dict[str, dict]:
    return {name: func(jobs, num_machines) for name, func in ALGORITHMS.items()}


def build_results_table(results: Dict[str, dict]):
    import pandas as pd

    rows = []
    for name, result in results.items():
        rows.append(
            {
                "Algorithm": name,
                "Makespan": result["makespan"],
                "Average Completion": round(result["avg_completion"], 2),
                "Utilisation": round(result["utilisation"], 4),
            }
        )
    return pd.DataFrame(rows).sort_values("Makespan").reset_index(drop=True)
