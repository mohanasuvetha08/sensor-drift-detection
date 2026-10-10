
import random
import streamlit as st
import pandas as pd

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Privacy-Preserving Sensor Drift Detection",
    page_icon="📡",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("📡 Privacy-Preserving Federated AI")
st.subheader("Sensor Drift Detection Dashboard")

st.write(
    "A prototype demonstrating sensor monitoring, "
    "drift detection, and federated client aggregation."
)

st.info(
    "Demo mode: sensor temperatures and client updates "
    "are simulated for demonstration."
)

# ---------------- SETTINGS ----------------
BASELINE = 25.0

st.sidebar.header("Drift Detection Settings")
threshold = st.sidebar.slider(
    "Allowed difference from baseline (°C)",
    min_value=2.0,
    max_value=20.0,
    value=10.0,
    step=1.0
)

st.sidebar.write(f"Normal baseline: {BASELINE:.1f} °C")

# ---------------- SESSION STATE ----------------
if "sensor_values" not in st.session_state:
    st.session_state.sensor_values = [
        round(random.uniform(22, 28), 2),
        round(random.uniform(22, 28), 2),
        round(random.uniform(22, 28), 2)
    ]

if "test_results" not in st.session_state:
    st.session_state.test_results = []

# ---------------- SENSOR SIMULATION ----------------
st.header("1. Sensor Network")

st.write(
    "Use the buttons to generate normal readings "
    "or simulate drift in Sensor 2."
)

button1, button2, button3 = st.columns(3)

with button1:
    if st.button("🟢 Simulate Normal Sensors", use_container_width=True):
        st.session_state.sensor_values = [
            round(random.uniform(22, 28), 2)
            for _ in range(3)
        ]

with button2:
    if st.button("🔴 Simulate Sensor Drift", use_container_width=True):
        st.session_state.sensor_values = [
            round(random.uniform(22, 28), 2),
            round(random.uniform(65, 90), 2),
            round(random.uniform(22, 28), 2)
        ]

with button3:
    if st.button("🔄 Reset Demo", use_container_width=True):
        st.session_state.sensor_values = [25.0, 25.0, 25.0]
        st.session_state.test_results = []

sensor_values = st.session_state.sensor_values

# ---------------- DRIFT DETECTION ----------------
drift_flags = [
    abs(value - BASELINE) > threshold
    for value in sensor_values
]

st.subheader("Current Sensor Readings")

cols = st.columns(3)

for i, col in enumerate(cols):
    with col:
        st.metric(
            label=f"Sensor Client {i + 1}",
            value=f"{sensor_values[i]:.2f} °C",
            delta=f"{sensor_values[i] - BASELINE:+.2f} °C from baseline"
        )

        if drift_flags[i]:
            st.error("⚠️ Drift Detected")
        else:
            st.success("✅ Normal Reading")

# ---------------- GRAPH ----------------
st.subheader("2. Sensor Temperature Graph")

chart_data = pd.DataFrame({
    "Sensor": ["Sensor 1", "Sensor 2", "Sensor 3"],
    "Temperature (°C)": sensor_values
})

st.bar_chart(
    chart_data,
    x="Sensor",
    y="Temperature (°C)"
)

st.caption(
    f"Readings are compared with the {BASELINE:.1f} °C baseline. "
    f"A difference greater than {threshold:.1f} °C triggers an alert."
)

# ---------------- FEDERATED AGGREGATION ----------------
st.header("3. Federated Learning Demonstration")

st.write(
    "Each client calculates a normalized score from its current "
    "temperature. The server averages the scores. This is a "
    "demonstration of aggregation, not trained AI model weights."
)

if st.button("🔐 Run Federated Learning Round", use_container_width=True):

    client_updates = [
        round(value / 100.0, 3)
        for value in sensor_values
    ]

    st.subheader("Local Client Updates")

    update_cols = st.columns(3)

    for i, col in enumerate(update_cols):
        with col:
            st.metric(
                f"Client {i + 1} Update",
                f"{client_updates[i]:.3f}"
            )

    global_value = sum(client_updates) / len(client_updates)

    st.subheader("Central Server")

    st.metric(
        "Combined Model Value (Demo)",
        f"{global_value:.3f}"
    )

    st.success("Client scores aggregated successfully.")

    st.info(
        "Only derived scores are displayed as client updates in this "
        "demonstration. This interface alone does not prove that raw "
        "data is protected in a real federated learning system."
    )

# ---------------- EVALUATION ----------------
st.header("4. Drift Detection Evaluation")

st.write(
    "Record the current simulated readings as a test case. "
    "The expected status is determined using the configured "
    "baseline and threshold."
)

if st.button("📊 Record Current Test Result", use_container_width=True):

    result = {
        "Sensor 1 (°C)": sensor_values[0],
        "Sensor 2 (°C)": sensor_values[1],
        "Sensor 3 (°C)": sensor_values[2],
        "Sensors Flagged": sum(drift_flags),
        "Test Type": (
            "Drift Scenario" if any(drift_flags)
            else "No Drift Detected"
        )
    }

    st.session_state.test_results.append(result)

if st.session_state.test_results:
    results_df = pd.DataFrame(st.session_state.test_results)

    st.dataframe(
        results_df,
        use_container_width=True,
        hide_index=True
    )

    total_tests = len(st.session_state.test_results)
    tests_with_alerts = sum(
        1 for result in st.session_state.test_results
        if result["Sensors Flagged"] > 0
    )

    col1, col2 = st.columns(2)

    col1.metric("Test Cases Recorded", total_tests)
    col2.metric("Test Cases With Alerts", tests_with_alerts)

    st.caption(
        "These are observed prototype test outcomes, not a verified "
        "accuracy score or a measurement of real-world performance."
    )
else:
    st.write("No test results recorded yet. Run a simulation and record a test.")

# ---------------- PROJECT STATUS ----------------
st.header("5. Prototype Status")

st.write("""
- Sensor data: simulated.
- Drift detection: baseline and threshold rule.
- Federated learning: simulated score aggregation.
- Differential privacy: not implemented.
- Secure aggregation: not implemented.
- Real sensor deployment and trained AI evaluation: future work.
""")
