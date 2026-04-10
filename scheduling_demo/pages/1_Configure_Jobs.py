from __future__ import annotations

import streamlit as st

from utils.scheduler_core import CONFIGS, CONFIG_DESCRIPTIONS, compute_all_results, generate_jobs
from utils.visuals import draw_jobs_chart


st.set_page_config(page_title="Configure Jobs", page_icon="⚙️", layout="wide")

st.title("Configure Jobs")
st.write("Set the experiment first. The demo and results pages will stay empty until you generate the jobs.")

config_name = st.selectbox("Choose configuration", list(CONFIGS.keys()), index=list(CONFIGS.keys()).index(st.session_state.get("selected_config", "Configuration 1")))
st.session_state.selected_config = config_name
config = CONFIGS[config_name]

col1, col2 = st.columns(2)
with col1:
    st.metric("Number of jobs", config["num_jobs"])
    st.metric("Number of machines", config["num_machines"])
with col2:
    seed = st.number_input("Random seed", min_value=1, max_value=9999, value=int(st.session_state.get("seed", 42)), step=1)
    st.session_state.seed = int(seed)
    st.write(CONFIG_DESCRIPTIONS[config_name])

if st.button("Generate Job Set", use_container_width=True):
    jobs = generate_jobs(config["num_jobs"], st.session_state.seed)
    results = compute_all_results(jobs, config["num_machines"])
    st.session_state.jobs = jobs
    st.session_state.results = results
    st.session_state.jobs_generated = True
    st.session_state.run_requested = False
    st.success("Jobs generated. You can now move to Run Demo or Results & Comparison.")

st.markdown("---")

if st.session_state.get("jobs_generated"):
    st.subheader("Current generated jobs")
    jobs = st.session_state.jobs
    preview_cols = st.columns(4)
    preview_cols[0].metric("Min duration", min(jobs))
    preview_cols[1].metric("Max duration", max(jobs))
    preview_cols[2].metric("Average duration", f"{sum(jobs)/len(jobs):.2f}")
    preview_cols[3].metric("Seed used", st.session_state.seed)

    fig = draw_jobs_chart(jobs)
    st.pyplot(fig, clear_figure=True)

    st.subheader("Job list")
    st.code(", ".join(str(x) for x in jobs), language="text")
else:
    st.warning("No job set has been generated yet.")