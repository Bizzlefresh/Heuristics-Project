from __future__ import annotations

import time

import matplotlib.pyplot as plt
import streamlit as st

from utils.scheduler_core import ALGO_EXPLANATIONS, CONFIGS
from utils.visuals import draw_schedule


st.set_page_config(page_title="Run Demo", page_icon="▶️", layout="wide")

st.title("Run Demo")

if not st.session_state.get("jobs_generated"):
    st.warning("Generate a job set first on the Configure Jobs page.")
    st.stop()

config = CONFIGS[st.session_state.selected_config]
results = st.session_state.results

left, right = st.columns([1.2, 0.9])

with left:
    st.subheader("Live visual area")
    st.write("Each horizontal lane is one machine. Each block is one job. The block starts at the job start time and ends at the job finish time.")
    chart_placeholder = st.empty()

with right:
    st.subheader("Demo controls")
    selected_algorithm = st.radio(
        "Choose one algorithm to demonstrate",
        list(results.keys()),
        index=list(results.keys()).index(st.session_state.get("selected_algorithm", "FCFS")),
    )
    st.session_state.selected_algorithm = selected_algorithm
    speed = st.slider("Animation speed", min_value=0.5, max_value=3.0, value=1.0, step=0.5)
    show_labels = st.checkbox("Show job labels", value=True)
    st.info(ALGO_EXPLANATIONS[selected_algorithm])

    if st.button("Run Live Demo", use_container_width=True):
        result = results[selected_algorithm]
        total = result["makespan"]
        step = max(1.0, total / 30)
        current = 0.0
        while current <= total:
            fig = draw_schedule(result, config["num_machines"], elapsed=current, annotate=show_labels)
            chart_placeholder.pyplot(fig, clear_figure=True)
            plt.close(fig)
            time.sleep(max(0.04, 0.18 / speed))
            current += step

        fig = draw_schedule(result, config["num_machines"], elapsed=total, annotate=show_labels)
        chart_placeholder.pyplot(fig, clear_figure=True)
        plt.close(fig)
        st.session_state.run_requested = True

    if st.button("Show Final Schedule Only", use_container_width=True):
        result = results[selected_algorithm]
        fig = draw_schedule(result, config["num_machines"], elapsed=result["makespan"], annotate=show_labels)
        chart_placeholder.pyplot(fig, clear_figure=True)
        plt.close(fig)

st.markdown("---")

st.subheader("How to read the visual")
exp1, exp2, exp3 = st.columns(3)
exp1.markdown("**Job block length** = processing time / duration")
exp2.markdown("**s=...** under a block = start time")
exp3.markdown("**e=...** above a block = finish time")

result = results[selected_algorithm]
detail_rows = []
for item in result["assignments"]:
    detail_rows.append(
        {
            "Job": f"J{item['job_id']}",
            "Duration": item["duration"],
            "Machine": f"Machine {item['machine'] + 1}",
            "Start": item["start"],
            "Finish": item["finish"],
        }
    )
st.subheader(f"Detailed assignment table for {selected_algorithm}")
st.dataframe(detail_rows, use_container_width=True, hide_index=True)