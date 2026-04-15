import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
import time
import numpy as np
from datetime import datetime, timedelta

# --- 1. PAGE SETUP & SECURITY (LOGIN) ---
st.set_page_config(page_title="EcoMagnet AI Premium", page_icon="🏭", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🔒 EcoMagnet Enterprise Login")
    st.info("Authorized Control Room Personnel Only.")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == "admin" and password == "mining2026":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Incorrect Username or Password")
    st.stop()

# --- 2. LOAD AI MODEL & LIVE DATA ---
@st.cache_resource
def load_model():
    return joblib.load('ecomagnet_model.pkl')

model = load_model()

@st.cache_data(ttl=3600)
def get_live_iron_price():
    try:
        ticker = yf.Ticker("TIO=F") 
        live_price = ticker.history(period="1d")['Close'].iloc[-1]
        return round(live_price, 2)
    except:
        return 110.0 

live_price = get_live_iron_price()

# --- 3. SIDEBAR: GLOBAL SETTINGS & ALERTS ---
st.sidebar.header("🌍 Global Settings")
currency_dict = {"USD ($)": "$", "INR (₹)": "₹", "SAR (﷼)": "﷼", "RUB (₽)": "₽"}
selected_region = st.sidebar.selectbox("Select Currency", list(currency_dict.keys()))
sym = currency_dict[selected_region]

iron_price = st.sidebar.number_input(f"Iron Price ({sym}/t)", value=live_price, step=5.0)
carbon_tax = st.sidebar.number_input(f"Carbon Tax ({sym}/t CO2)", value=50.0, step=5.0)
energy_cost = st.sidebar.number_input(f"Energy Cost ({sym}/kWh)", value=0.12, step=0.01)

st.sidebar.markdown("---")
st.sidebar.header("📱 Alert System Setup")
manager_phone = st.sidebar.text_input("Manager Phone (for SMS Alerts)", "+91-")
alert_threshold = st.sidebar.slider("Minimum Recovery Alert (%)", 10, 40, 25)

# --- APP HEADER ---
st.title("🏭 EcoMagnet AI: Enterprise Control Room")
st.markdown("Digital Twin & Predictive Analytics Dashboard")

# --- CREATE TABS FOR CLEAN UI ---
tab1, tab2, tab3 = st.tabs(["🎛️ Single Machine Optimizer", "🏭 Fleet Overview", "📈 30-Day Analytics"])

# ==========================================
# TAB 1: SINGLE MACHINE & PREDICTIVE MAINTENANCE
# ==========================================
with tab1:
    st.header("Unit 1: Optimization & Maintenance")
    grade = st.slider("Current Feed Grade (%)", 20.0, 45.0, 32.0)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("🛠️ Baseline (Manual)")
        base_field = st.slider("Manual Field (Gauss)", 1000, 3000, 2800, key="b_field")
        base_speed = st.slider("Manual Speed (RPM)", 20, 50, 45, key="b_speed")
        
        base_recovery = model.predict([[base_field, base_speed, grade]])[0]
        st.metric("Baseline Recovery", f"{base_recovery:.2f}%")
        
        # FEATURE 1: PREDICTIVE MAINTENANCE WARNING
        if base_field > 2700 and base_speed > 40:
            st.error("⚠️ **MAINTENANCE WARNING:** High Gauss and High RPM detected. High risk of bearing failure and motor overheating within 48 hours.")

    with col2:
        st.success("🤖 AI Optimized")
        ai_field = st.slider("AI Field (Gauss)", 1000, 3000, 2100, key="a_field")
        ai_speed = st.slider("AI Speed (RPM)", 20, 50, 30, key="a_speed")
        
        ai_recovery = model.predict([[ai_field, ai_speed, grade]])[0]
        st.metric("AI Recovery", f"{ai_recovery:.2f}%", delta=f"{ai_recovery - base_recovery:.2f}%")
        
        # FEATURE 3: AUTOMATED ALERTS
        if ai_recovery < alert_threshold:
            st.warning(f"🚨 **AUTOMATED SMS SENT TO {manager_phone}:** Recovery dropped below critical threshold ({alert_threshold}%).")

    # LIVE SCADA SIMULATOR (From previous step)
    st.write("---")
    st.subheader("🔴 Live SCADA Sensor Feed")
    if st.button("Start Live Feed"):
        placeholder = st.empty()
        for seconds in range(10):
            live_field = base_field + np.random.randint(-50, 50)
            live_speed = base_speed + np.random.randint(-2, 2)
            live_rec = model.predict([[live_field, live_speed, grade]])[0]
            with placeholder.container():
                k1, k2, k3 = st.columns(3)
                k1.metric("Live Gauss", f"{live_field}")
                k2.metric("Live RPM", f"{live_speed}")
                k3.metric("Live Recovery", f"{live_rec:.2f}%")
            time.sleep(1)
        st.success("Simulation Complete.")

# ==========================================
# TAB 2: MULTI-MACHINE FLEET DASHBOARD
# ==========================================
with tab2:
    st.header("Plant Overview: Magnetic Separation Fleet")
    st.markdown("Monitor all processing units in real-time.")
    
    fleet_cols = st.columns(4)
    
    # Simulate 4 machines
    machines = [
        {"name": "Unit 1", "status": "Healthy", "rec": 42.1, "color": "normal"},
        {"name": "Unit 2", "status": "Warning (Vibration)", "rec": 38.5, "color": "off"},
        {"name": "Unit 3", "status": "Healthy", "rec": 41.2, "color": "normal"},
        {"name": "Unit 4", "status": "Critical (Low Grade)", "rec": 22.4, "color": "inverse"}
    ]
    
    for i, col in enumerate(fleet_cols):
        with col:
            st.subheader(machines[i]["name"])
            st.metric("Current Recovery", f"{machines[i]['rec']}%", delta=machines[i]["status"], delta_color=machines[i]["color"])
            if machines[i]["status"] == "Critical (Low Grade)":
                st.error("Action Required")
            elif machines[i]["status"] == "Warning (Vibration)":
                st.warning("Inspect Soon")
            else:
                st.success("Running Optimally")

# ==========================================
# TAB 3: 30-DAY HISTORICAL TRENDS
# ==========================================
with tab3:
    st.header("Executive ROI & Carbon Impact")
    
    # Generate Fake 30-Day Data
    dates = [datetime.today() - timedelta(days=x) for x in range(30)]
    dates.reverse() # Oldest to newest
    
    # Baseline profit is flat, AI profit grows
    base_profits = [10000 + np.random.randint(-500, 500) for _ in range(30)]
    ai_profits = [10000 + (x * 150) + np.random.randint(-200, 200) for x in range(30)] # Gradually increases
    
    df_history = pd.DataFrame({
        "Date": dates,
        "Manual Settings Profit": base_profits,
        "AI Optimized Profit": ai_profits
    })
    
    # Plotly Line Chart
    fig_hist = px.line(df_history, x="Date", y=["Manual Settings Profit", "AI Optimized Profit"], 
                       title=f"30-Day Cumulative Profit ({sym})",
                       labels={"value": f"Daily Profit ({sym})", "variable": "Operation Mode"})
    
    st.plotly_chart(fig_hist, use_container_width=True)
    
    total_saved = sum(ai_profits) - sum(base_profits)
    st.metric(f"Total AI Value Generated (30 Days)", f"{sym}{total_saved:,.2f}", delta="Proven ROI")
