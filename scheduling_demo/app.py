from __future__ import annotations

import streamlit as st

from utils.scheduler_core import ALGO_EXPLANATIONS, CONFIG_DESCRIPTIONS, METRIC_EXPLANATIONS


st.set_page_config(page_title="Scheduling Demo", page_icon="📊", layout="wide")


if "jobs_generated" not in st.session_state:
    st.session_state.jobs_generated = False
if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "results" not in st.session_state:
    st.session_state.results = None
if "selected_config" not in st.session_state:
    st.session_state.selected_config = "Configuration 1"
if "seed" not in st.session_state:
    st.session_state.seed = 42
if "selected_algorithm" not in st.session_state:
    st.session_state.selected_algorithm = "FCFS"
if "run_requested" not in st.session_state:
    st.session_state.run_requested = False


st.title("Scheduling Algorithms Demo")
st.caption("A cleaner presentation app for FCFS, SJF, LPT, and Greedy scheduling in a multi-machine system.")

left, right = st.columns([1.2, 1])

with left:
    st.subheader("What this project shows")
    st.write(
        "This demo compares four scheduling heuristics on the same generated job set so you can clearly show how algorithm choice affects the schedule."
    )
    st.write(
        "Use the pages in the sidebar from top to bottom: Configure Jobs → Run Demo → Results & Comparison."
    )

with right:
    st.subheader("Project structure")
    st.markdown(
        """
        - **Page 1:** Configure the experiment
        - **Page 2:** Run one algorithm live
        - **Page 3:** Compare all algorithms and inspect metrics
        """
    )

st.markdown("---")

c1, c2, c3 = st.columns(3)
with c1:
    st.subheader("Algorithms")
    for name, text in ALGO_EXPLANATIONS.items():
        st.markdown(f"**{name}:** {text}")

with c2:
    st.subheader("Configurations")
    for name, text in CONFIG_DESCRIPTIONS.items():
        st.markdown(f"**{name}:** {text}")

with c3:
    st.subheader("Metrics")
    for name, text in METRIC_EXPLANATIONS.items():
        st.markdown(f"**{name}:** {text}")

st.info("Nothing runs automatically. First generate jobs on the Configure Jobs page, then go to Run Demo.")
