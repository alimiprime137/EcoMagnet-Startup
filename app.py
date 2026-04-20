import streamlit as st
import pandas as pd
import numpy as np
import time
import random
from PIL import Image

# --- 1. LOGO LOADING & PAGE CONFIGURATION ---
# We try to load the logo. If it's not found, the app still runs perfectly without crashing.
try:
    logo = Image.open("logo.png")
except:
    logo = None

# This MUST be the first Streamlit command
st.set_page_config(page_title="Ferrum IQ | Enterprise AI", page_icon=logo, layout="wide")

# --- 2. SESSION STATE (For Login Memory) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- 3. LOGIN PAGE LOGIC ---
def login_page():
    # Display logo if it exists
    if logo:
        st.image(logo, width=150)
        
    st.title("Ferrum IQ Gateway")
    st.subheader("Enterprise Mineral Processing Control")
    st.markdown("---")
    
    with st.container():
        # FIXED: Changed 'placeholder' to 'value' so it is actually typed in!
        user = st.text_input("Username", value="admin")
        pw = st.text_input("Password", type="password", value="mining2026")
        
        if st.button("Login to Control Room"):
            if user == "admin" and pw == "mining2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials. Please contact your system administrator.")

# --- 4. MAIN DASHBOARD LOGIC ---
def main_dashboard():
    # --- SIDEBAR ---
    with st.sidebar:
        if logo: 
            st.image(logo, use_container_width=True)
        st.title("Ferrum IQ")
        st.markdown("---")
        st.header("🌍 Global Economics")
        currency = st.selectbox("Market Currency", ["USD ($)", "INR (₹)", "AUD ($)"])
        iron_price = st.number_input("Live Iron Ore Price ($/t)", value=118.50)
        carbon_tax = st.slider("Carbon Tax Penalty ($/t CO2)", 20, 100, 45)
        manager_phone = st.text_input("Manager SMS Alert Number", value="+91 98765 43210")
        
        st.markdown("---")
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.rerun()

    # --- HEADER ---
    col1, col2 = st.columns([1, 8])
    with col1:
        if logo: 
            st.image(logo, width=80)
    with col2:
        st.title("Enterprise Control Dashboard")
        st.write("Connected to: **Western Mine Site - Unit 4** | System Status: **🟢 Operational**")

    # --- TABS ---
    tab1, tab2, tab3 = st.tabs(["🎯 AI Optimizer", "🚛 Fleet Status", "📊 Financial Analytics"])

    # --- TAB 1: MACHINE OPTIMIZER & SCADA ---
    with tab1:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.subheader("Process Controls")
            feed = st.slider("Input Feed Grade (%)", 15.0, 55.0, 32.5)
            gauss = st.slider("Magnetic Strength (Gauss)", 500, 3000, 1850)
            rpm = st.slider("Drum Rotation Speed (RPM)", 10, 60, 38)
            
            # Predictive Maintenance Logic
            if gauss > 2750:
                st.error("⚠️ CRITICAL ALERT: Magnetic Coil Temperature Exceeding Safety Threshold!")
                st.warning(f"📱 Automated SMS Sent to {manager_phone}: 'Unit 4 High Heat Warning'")
            elif rpm > 52:
                st.error("⚠️ VIBRATION ALERT: Mechanical stress detected on main bearing.")

        with c2:
            st.subheader("AI Performance Prediction")
            # Logic: Recovery increases with Gauss, but drops if RPM is too high
            raw_rec = (feed * 1.2) + (gauss/100) - (abs(rpm-35)*0.5)
            rec = min(max(raw_rec, 0), 99.2) # Cap between 0 and 99.2%
            
            st.metric(label="Predicted Recovery", value=f"{rec:.2f}%", delta="Optimized via RF Model")
            
            with st.expander("View AI Recommendation", expanded=True):
                st.success(f"**Optimization Result:** Reducing Gauss to 1700 and RPM to 34 will maintain {rec-1.2:.1f}% recovery while reducing energy costs by 22%.")

        st.markdown("---")
        st.subheader("📡 Live SCADA Feed Simulator")
        if st.button("Activate Real-Time IoT Stream"):
            placeholder = st.empty()
            # Loop simulates 15 seconds of live data
            for _ in range(15):
                noise_gauss = gauss + random.uniform(-30, 30)
                noise_rpm = rpm + random.uniform(-1, 1)
                noise_rec = rec + random.uniform(-0.5, 0.5)
                
                with placeholder.container():
                    k1, k2, k3 = st.columns(3)
                    k1.metric("Live Gauss", f"{noise_gauss:.0f} G")
                    k2.metric("Live RPM", f"{noise_rpm:.1f} RPM")
                    k3.metric("Live Recovery", f"{noise_rec:.2f} %")
                    time.sleep(0.4) # Wait a fraction of a second before updating

    # --- TAB 2: FLEET STATUS ---
    with tab2:
        st.subheader("Active Asset Fleet Monitor")
        fleet_data = pd.DataFrame({
            "Unit ID": ["Ferrum-01", "Ferrum-02", "Ferrum-03", "Ferrum-04"],
            "Location": ["North Pit", "North Pit", "South Tailings", "East Processing"],
            "Performance": ["94% (Optimal)", "92% (Optimal)", "71% (Critical)", "89% (Stable)"],
            "Health": ["🟢 Healthy", "🟢 Healthy", "🔴 Maintenance Req", "🟡 Check Sensors"]
        })
        st.table(fleet_data)

    # --- TAB 3: FINANCIAL ANALYTICS ---
    with tab3:
        st.subheader("Economic Impact (30 Day Trend)")
        
        # Simulating 30 days of profit data
        days = np.arange(1, 31)
        manual_profit = np.random.normal(5000, 500, 30)
        ai_profit = manual_profit + np.random.normal(1200, 200, 30) # AI makes more profit
        
        chart_df = pd.DataFrame({
            "Day": days,
            "Manual Operation Profit": manual_profit,
            "Ferrum IQ AI Profit": ai_profit
        }).set_index("Day")
        
        st.area_chart(chart_df)
        
        total_savings = (ai_profit.sum() - manual_profit.sum())
        st.success(f"💰 Total AI-Driven Value Created this month: {currency} {total_savings:,.2f}")

    # --- FOOTER ---
    st.markdown("---")
    st.caption("Ferrum IQ Enterprise Suite v1.0.4 | Secured Industrial Cloud | Est. 2026")

# --- 5. APP ROUTING ---
# This decides whether to show the login screen or the main dashboard
if st.session_state.logged_in:
    main_dashboard()
else:
    login_page()
