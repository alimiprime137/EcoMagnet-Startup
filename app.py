import streamlit as st
import pandas as pd
import numpy as np
import time
import random
from PIL import Image

# --- INITIALIZATION & SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- LOGO LOADING ---
try:
    logo = Image.open("logo.png")
except:
    logo = None

st.set_page_config(page_title="Ferrum IQ | Enterprise AI", page_icon=logo, layout="wide")

# --- LOGIN PAGE LOGIC ---
def login_page():
    st.image(logo, width=200) if logo else None
    st.title("Ferrum IQ Gateway")
    st.subheader("Enterprise Mineral Processing Control")
    
    with st.container():
        user = st.text_input("Username", placeholder="admin")
        pw = st.text_input("Password", type="password", placeholder="mining2026")
        
        if st.button("Login to Control Room"):
            if user == "admin" and pw == "mining2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials. Please contact your system administrator.")

# --- MAIN DASHBOARD LOGIC ---
def main_dashboard():
    # Sidebar Branding & Navigation
    with st.sidebar:
        if logo: st.image(logo, use_container_width=True)
        st.title("Ferrum IQ")
        st.markdown("---")
        st.header("🌍 Global Economics")
        currency = st.selectbox("Market Currency", ["USD ($)", "INR (₹)", "AUD ($)"])
        # Simulating live market price from "Yahoo Finance"
        iron_price = st.number_input("Live Iron Ore Price ($/t)", value=118.50)
        carbon_tax = st.slider("Carbon Tax Penalty ($/t CO2)", 20, 100, 45)
        manager_phone = st.text_input("Manager SMS Alert Number", "+91 98765 43210")
        
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.rerun()

    # Header
    col1, col2 = st.columns([1, 5])
    with col1:
        if logo: st.image(logo, width=100)
    with col2:
        st.title("Enterprise Control Dashboard")
        st.write(f"Connected to: **Western Mine Site - Unit 4** | System Status: **Operational**")

    tab1, tab2, tab3 = st.tabs(["🎯 AI Optimizer", "🚛 Fleet Fleet Status", "📊 Financial Analytics"])

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
                st.warning(f"SMS Sent to {manager_phone}: 'Unit 4 High Heat Warning'")
            elif rpm > 52:
                st.error("⚠️ VIBRATION ALERT: Mechanical stress detected on main bearing.")

        with c2:
            st.subheader("AI Performance Prediction")
            # Logic: Recovery increases with Gauss, but drops if RPM is too high (Centrifugal loss)
            raw_rec = (feed * 1.2) + (gauss/100) - (abs(rpm-35)*0.5)
            rec = min(max(raw_rec, 0), 99.2)
            
            st.metric(label="Predicted Recovery", value=f"{rec:.2f}%", delta="Optimized via RF Model")
            
            with st.expander("View AI Recommendation"):
                st.success(f"**Optimization Result:** Reducing Gauss to 1700 and RPM to 34 will maintain {rec-1:.1f}% recovery while reducing energy costs by 22%.")

        st.markdown("---")
        st.subheader("📡 Live SCADA Feed")
        if st.button("Activate Real-Time IoT Stream"):
            placeholder = st.empty()
            for _ in range(15):
                noise_gauss = gauss + random.uniform(-30, 30)
                noise_rpm = rpm + random.uniform(-1, 1)
                noise_rec = rec + random.uniform(-0.5, 0.5)
                
                with placeholder.container():
                    k1, k2, k3 = st.columns(3)
                    k1.metric("Live Gauss", f"{noise_gauss:.0f}")
                    k2.metric("Live RPM", f"{noise_rpm:.1f}")
                    k3.metric("Live Recovery", f"{noise_rec:.2f}%")
                    time.sleep(0.4)

    # --- TAB 2: FLEET STATUS ---
    with tab2:
        st.subheader("Active Asset Fleet Monitor")
        fleet_data = pd.DataFrame({
            "Unit ID": ["Ferrum-01", "Ferrum-02", "Ferrum-03", "Ferrum-04"],
            "Location": ["North Pit", "North Pit", "South Tailings", "East Processing"],
            "Performance": ["94% (Optimal)", "92% (Optimal)", "71% (Critical)", "89% (Stable)"],
            "Health": ["Healthy", "Healthy", "Maintenance Req", "Check Sensors"]
        })
        st.table(fleet_data)

    # --- TAB 3: FINANCIAL ANALYTICS ---
    with tab3:
        st.subheader("Economic Impact (30 Day Trend)")
        # Show comparison between Manual vs AI
        days = np.arange(1, 31)
        manual_profit = np.random.normal(5000, 500, 30)
        ai_profit = manual_profit + np.random.normal(1200, 200, 30)
        
        chart_df = pd.DataFrame({
            "Day": days,
            "Manual Operation Profit": manual_profit,
            "Ferrum IQ AI Profit": ai_profit
        }).set_index("Day")
        
        st.area_chart(chart_df)
        
        total_savings = (ai_profit.sum() - manual_profit.sum())
        st.success(f"Total AI-Driven Value Created this month: {currency} {total_savings:,.2f}")

    st.markdown("---")
    st.caption("Ferrum IQ Enterprise Suite v1.0.4 | Secured Industrial Cloud")

# --- APP ROUTING ---
if st.session_state.logged_in:
    main_dashboard()
else:
    login_page()
