from __future__ import annotations

import matplotlib.pyplot as plt
import streamlit as st

from utils.scheduler_core import METRIC_EXPLANATIONS, build_results_table
from utils.visuals import draw_metric_chart, draw_schedule


st.set_page_config(page_title="Results & Comparison", page_icon="📈", layout="wide")

st.title("Results & Comparison")

if not st.session_state.get("jobs_generated"):
    st.warning("Generate a job set first on the Configure Jobs page.")
    st.stop()

results = st.session_state.results
results_df = build_results_table(results)
best_algorithm = results_df.iloc[0]["Algorithm"]

st.success(f"Best algorithm by makespan on this generated job set: {best_algorithm}")

c1, c2 = st.columns([1.15, 1])
with c1:
    st.subheader("Comparison table")
    st.dataframe(results_df, use_container_width=True, hide_index=True)
with c2:
    st.subheader("Metric guide")
    for name, text in METRIC_EXPLANATIONS.items():
        st.markdown(f"**{name}:** {text}")

m1, m2, m3 = st.columns(3)
for col, metric in zip([m1, m2, m3], ["Makespan", "Average Completion", "Utilisation"]):
    with col:
        fig = draw_metric_chart(results_df, metric)
        st.pyplot(fig, clear_figure=True)
        plt.close(fig)

st.markdown("---")

selected_algorithm = st.selectbox("Inspect one final schedule", list(results.keys()), index=list(results.keys()).index(best_algorithm))
result = results[selected_algorithm]
fig = draw_schedule(result, num_machines=len(result["machines"]), elapsed=result["makespan"], annotate=True)
st.pyplot(fig, clear_figure=True)
plt.close(fig)

st.subheader("Explain these metrics in your own words")
mc1, mc2, mc3 = st.columns(3)
mc1.metric("Makespan", result["makespan"])
mc2.metric("Average Completion", f"{result['avg_completion']:.2f}")
mc3.metric("Utilisation", f"{result['utilisation']:.4f}")

st.markdown(
    f"""
**Why {selected_algorithm} got these values:**
- The schedule above shows exactly when every job starts and ends.
- **Makespan** is determined by the machine that finishes last.
- **Average completion** is determined by the finish times of all jobs.
- **Utilisation** depends on total job work divided by total machine capacity over the whole makespan.
"""
)
