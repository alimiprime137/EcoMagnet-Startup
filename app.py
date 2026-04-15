import streamlit as st
import pandas as pd
import joblib

# 1. Setup the Webpage
st.set_page_config(page_title="EcoMagnet AI", page_icon="🌱")
st.title("🌱 EcoMagnet: Mineral & ESG Optimizer")

# 2. Load the Saved Model (The Brain)
# We load the .pkl file we just created
@st.cache_resource
def load_model():
    return joblib.load('ecomagnet_model.pkl')

model = load_model()

# 3. Create the User Interface (Sidebar)
st.sidebar.header("Machine Settings")
field = st.sidebar.slider("Field Strength (Gauss)", 1000, 3000, 2200)
speed = st.sidebar.slider("Drum Speed (RPM)", 20, 50, 35)
grade = st.sidebar.number_input("Feed Grade (%)", 20.0, 45.0, 32.0)

# 4. Make the Prediction
prediction = model.predict([[field, speed, grade]])[0]

# 5. Calculate ESG (Carbon) Metrics
energy_kwh = (field / 1000) * 12.5 
co2_emissions = energy_kwh * 0.475 
carbon_cost = co2_emissions * 0.05 

# 6. Display the Results beautifully
col1, col2, col3 = st.columns(3)
col1.metric("Predicted Recovery", f"{prediction:.2f}%")
col2.metric("Carbon Footprint", f"{co2_emissions:.2f} kg/t")
col3.metric("Carbon Tax", f"${carbon_cost:.2f}/t")

st.write("---")
st.success(f"**Insight:** To maximize efficiency, keep Field Strength balanced. Pushing to 3000 Gauss spikes the Carbon Tax significantly.")
