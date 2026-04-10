from __future__ import annotations

from typing import List

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def draw_schedule(result: dict, num_machines: int, elapsed: float | None = None, annotate: bool = True):
    makespan = max(result["makespan"], 1)
    if elapsed is None:
        elapsed = makespan

    fig, ax = plt.subplots(figsize=(13, 7))
    ax.set_xlim(0, makespan * 1.08)
    ax.set_ylim(0.4, num_machines + 0.9)
    ax.set_xlabel("Time")
    ax.set_ylabel("Machine")
    ax.set_yticks(range(1, num_machines + 1))
    ax.set_yticklabels([f"Machine {i}" for i in range(1, num_machines + 1)])
    ax.set_title(f"{result['name']} Live Schedule   |   Progress {elapsed:.1f}/{result['makespan']}")

    for t in range(0, int(makespan) + 1, max(1, int(makespan // 12) or 1)):
        ax.axvline(t, linewidth=0.8, alpha=0.15)
        ax.text(t, num_machines + 0.72, str(t), ha="center", va="bottom", fontsize=8)

    for m in range(num_machines):
        y = m + 1
        ax.hlines(y, 0, makespan, linewidth=12, alpha=0.08)

    for item in result["assignments"]:
        y = item["machine"] + 1
        start = item["start"]
        finish = item["finish"]
        duration = item["duration"]
        if elapsed <= start:
            continue
        visible_width = min(elapsed, finish) - start
        if visible_width <= 0:
            continue

        rect = Rectangle((start, y - 0.34), visible_width, 0.68, alpha=0.85, ec="black", lw=1)
        ax.add_patch(rect)

        ax.text(start, y - 0.43, f"s={start}", ha="left", va="top", fontsize=8)
        if elapsed >= finish:
            ax.text(finish, y + 0.43, f"e={finish}", ha="right", va="bottom", fontsize=8)

        if annotate and visible_width > max(2.5, duration * 0.3):
            ax.text(
                start + visible_width / 2,
                y,
                f"J{item['job_id']}\n{duration}",
                ha="center",
                va="center",
                fontsize=8,
                fontweight="bold",
            )

    ax.axvline(elapsed, linestyle="--", linewidth=2)
    plt.tight_layout()
    return fig


def draw_jobs_chart(jobs: List[int]):
    fig, ax = plt.subplots(figsize=(13, 3.5))
    ax.bar(range(1, len(jobs) + 1), jobs)
    ax.set_title("Generated Job Durations")
    ax.set_xlabel("Job ID")
    ax.set_ylabel("Duration")
    plt.tight_layout()
    return fig


def draw_metric_chart(results_df, metric_name: str):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(results_df["Algorithm"], results_df[metric_name])
    ax.set_title(f"{metric_name} Comparison")
    ax.set_xlabel("Algorithm")
    ax.set_ylabel(metric_name)
    plt.tight_layout()
    return fig


def draw_boxplot(results_per_algo: dict):
    fig, ax = plt.subplots(figsize=(8, 5))
    labels = list(results_per_algo.keys())
    values = [results_per_algo[label] for label in labels]
    ax.boxplot(values, labels=labels)
    ax.set_title("Makespan Distribution Across Runs")
    ax.set_ylabel("Makespan")
    plt.tight_layout()
    return fig


def draw_line_chart(values: List[float], title: str, x_label: str, y_label: str):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(range(1, len(values) + 1), values)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.tight_layout()
    return fig

def draw_boxplot(results_per_algo: dict):
    fig, ax = plt.subplots(figsize=(8, 5))
    labels = list(results_per_algo.keys())
    values = [results_per_algo[label] for label in labels]
    ax.boxplot(values, labels=labels)
    ax.set_title("Makespan Distribution Across Runs")
    ax.set_ylabel("Makespan")
    plt.tight_layout()
    return fig


def draw_line_chart(values: List[float], title: str, x_label: str, y_label: str):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(range(1, len(values) + 1), values)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.tight_layout()
    return fig