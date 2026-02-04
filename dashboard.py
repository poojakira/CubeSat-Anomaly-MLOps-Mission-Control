import streamlit as st
import plotly.express as px
from ml_orchestrator import MLOrchestrator
import config

st.set_page_config(page_title="Mission Control 2026", layout="wide")
orch = MLOrchestrator()

st.title("🛰️ CubeSat Live 3D Command Center")

# Visualizing Live Data
df = orch.fetch_and_process()
if df is not None:
    preds, scores = orch.engine.predict(df[["distance_cm", "rolling_mean", "rolling_std"]])
    df["Status"] = ["Anomaly" if p == -1 else "Normal" for p in preds]

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("🌌 3D Feature Space Cluster")
        fig = px.scatter_3d(df, x='distance_cm', y='rolling_mean', z='rolling_std',
                             color='Status', symbol='face', template="plotly_dark", height=600)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📉 Sensor Drift")
        st.line_chart(df.set_index('timestamp')[['distance_cm', 'rolling_mean']])
        st.metric("System Health", "CRITICAL" if (df["Status"]=="Anomaly").any() else "NOMINAL")
else:
    st.error("Connecting to satellite telemetry...")