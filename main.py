import streamlit as st
import pandas as pd
import pickle

# Load your trained model
model = pickle.load(open("Semi.pkl", "rb"))

# UI Config
st.set_page_config(page_title="Meets Timing Predictor", layout="centered")

st.title("⏱️ Meets Timing Prediction App")
st.markdown("This app predicts whether a chip design will meet timing based on your input parameters.")

# Input Fields
with st.form("prediction_form"):
    st.subheader("🔧 Enter Design Details")

    design_complexity = st.selectbox("Design Complexity", ["low", "medium", "high"])
    lines_of_code = st.number_input("Lines of Code", min_value=0, step=100)
    num_modules = st.number_input("Number of Modules", min_value=0)
    target_freq = st.number_input("Target Frequency (MHz)", min_value=0.0)
    design_tool = st.selectbox("Design Tool Used", ["Cadence", "OpenROAD", "Synopsys", "Mentor"])
    eda_runtime = st.number_input("EDA Runtime (min)", min_value=0.0)
    simulation_bugs = st.number_input("Simulation Bugs Found", min_value=0)
    estimated_power = st.number_input("Estimated Power Usage (mW)", min_value=0.0)

    submit = st.form_submit_button("Predict")

# Mapping inputs (manual encoding)
design_complexity_map = {"low": 0, "medium": 1, "high": 2}
design_tool_map = {"Cadence": 0, "OpenROAD": 1, "Synopsys": 2, "Mentor": 3}

if submit:
    input_df = pd.DataFrame([[
        design_complexity_map[design_complexity],
        lines_of_code,
        num_modules,
        target_freq,
        design_tool_map[design_tool],
        eda_runtime,
        simulation_bugs,
        estimated_power
    ]], columns=[
        "Design_Complexity",
        "Lines_of_Code",
        "Num_Modules",
        "Target_Frequency_MHz",
        "Design_Tool_Used",
        "EDA_Runtime_min",
        "Simulation_Bugs_Found",
        "Estimated_Power_Usage_mW"
    ])

    prediction = model.predict(input_df)[0]

    if prediction == 1:
        st.success("✅ The design **Meets Timing**.")
    else:
        st.error("❌ The design **Does Not Meet Timing**.")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit")
