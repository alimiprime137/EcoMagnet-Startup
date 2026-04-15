import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import yfinance as yf
import time
import numpy as np

# --- 1. PAGE SETUP & SECURITY (LOGIN) ---
st.set_page_config(page_title="EcoMagnet AI Premium", page_icon="🌍", layout="wide")

# Login Logic
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🔒 EcoMagnet Enterprise Login")
    st.info("Please log in to access the AI Control Room.")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == "admin" and password == "mining2026":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Incorrect Username or Password")
    st.stop() # Stops the rest of the code from running if not logged in!

# --- IF LOGGED IN, SHOW THE DASHBOARD ---
st.title("🌍 EcoMagnet AI: Global Enterprise Edition")
st.markdown("Optimize Mineral Recovery, Minimize Carbon, Maximize Local Profit.")

# --- 2. LOAD AI MODEL ---
@st.cache_resource
def load_model():
    return joblib.load('ecomagnet_model.pkl')

model = load_model()

# --- 3. LIVE MARKET API (YFINANCE) ---
@st.cache_data(ttl=3600) # Remembers the price for 1 hour
def get_live_iron_price():
    try:
        ticker = yf.Ticker("TIO=F") # Iron Ore Futures
        live_price = ticker.history(period="1d")['Close'].iloc[-1]
        return round(live_price, 2)
    except:
        return 110.0 # Backup price if internet fails

live_price = get_live_iron_price()

# --- 4. SIDEBAR: GLOBAL MARKET INPUTS ---
st.sidebar.header("🌍 Localization & Market Data")
currency_dict = {"USD ($)": "$", "INR (₹)": "₹", "SAR (﷼)": "﷼", "RUB (₽)": "₽"}
selected_region = st.sidebar.selectbox("Select Currency", list(currency_dict.keys()))
sym = currency_dict[selected_region]

st.sidebar.success(f"📈 Live Global Iron Price: {sym}{live_price}/ton")

# Financial inputs
iron_price = st.sidebar.number_input(f"Iron Ore Price ({sym}/ton)", value=live_price, step=5.0)
carbon_tax = st.sidebar.number_input(f"Carbon Tax ({sym}/ton CO2)", value=50.0, step=5.0)
energy_cost = st.sidebar.number_input(f"Electricity Cost ({sym}/kWh)", value=0.12, step=0.01)

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Ore Feed Data")
grade = st.sidebar.slider("Feed Grade (%)", 20.0, 45.0, 32.0)

# --- 5. MAIN DASHBOARD: SCENARIO COMPARISON ---
st.subheader(f"Scenario Analysis: Profit calculated in {sym}")
col1, col2 = st.columns(2)

with col1:
    st.info("🛠️ Baseline (Current Manual Settings)")
    base_field = st.slider("Manual Field Strength (Gauss)", 1000, 3000, 2800, key="b_field")
    base_speed = st.slider("Manual Drum Speed (RPM)", 20, 50, 45, key="b_speed")
    
    base_recovery = model.predict([[base_field, base_speed, grade]])[0]
    base_kwh = (base_field / 1000) * 12.5
    base_co2 = base_kwh * 0.475
    base_profit = (base_recovery / 100) * iron_price - (base_kwh * energy_cost) - ((base_co2 / 1000) * carbon_tax)

with col2:
    st.success("🤖 AI Optimized Proposal")
    ai_field = st.slider("AI Field Strength (Gauss)", 1000, 3000, 2100, key="a_field")
    ai_speed = st.slider("AI Drum Speed (RPM)", 20, 50, 30, key="a_speed")
    
    ai_recovery = model.predict([[ai_field, ai_speed, grade]])[0]
    ai_kwh = (ai_field / 1000) * 12.5
    ai_co2 = ai_kwh * 0.475
    ai_profit = (ai_recovery / 100) * iron_price - (ai_kwh * energy_cost) - ((ai_co2 / 1000) * carbon_tax)

# --- 6. THE "AHA" METRIC (Net Profit) ---
profit_diff = ai_profit - base_profit
st.metric("AI Generated Value (Extra Profit per Ton)", f"{sym}{profit_diff:.2f}", delta=f"{profit_diff/base_profit * 100:.1f}% Increase")

# --- 7. LIVE SCADA SIMULATOR ---
st.write("---")
st.subheader("🔴 Live SCADA Sensor Feed (Simulator)")
st.write("Click below to simulate real-time sensor data streaming from the magnetic drum.")

if st.button("Start Live Feed Simulation"):
    placeholder = st.empty() # Creates an empty box to update
    for seconds in range(15): # Runs for 15 seconds
        live_field = base_field + np.random.randint(-50, 50)
        live_speed = base_speed + np.random.randint(-2, 2)
        live_recovery = model.predict([[live_field, live_speed, grade]])[0]
        
        with placeholder.container():
            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric("Live Sensor: Gauss", f"{live_field}")
            kpi2.metric("Live Sensor: RPM", f"{live_speed}")
            kpi3.metric("Live AI Prediction", f"{live_recovery:.2f}%")
        
        time.sleep(1) # Pauses for 1 second
    st.success("Simulation Complete.")
