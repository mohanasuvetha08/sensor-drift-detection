
import streamlit as st

st.set_page_config(
    page_title="Sensor Drift Detection",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Privacy-Preserving Federated AI")
st.subheader("Sensor Drift Detection Dashboard")

st.write(
    "Monitor sensor readings, detect drift, "
    "and explore a privacy-preserving federated learning demo."
)

st.info("Welcome! Your prototype dashboard is running.")

st.header("Sensor Network")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Sensor Client 1", "Normal")

with col2:
    st.metric("Sensor Client 2", "Normal")

with col3:
    st.metric("Sensor Client 3", "Normal")

st.header("Drift Monitoring")

st.write("Sensor readings and drift alerts will appear here.")

st.caption("Prototype demonstration using simulated sensor data.")
