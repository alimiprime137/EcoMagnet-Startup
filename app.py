import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="EcoMagnet AI Global", page_icon="🌍", layout="wide")
st.title("🌍 EcoMagnet AI: Global Enterprise Edition")
st.markdown("Optimize Mineral Recovery, Minimize Carbon, Maximize Local Profit.")

# --- 2. LOAD AI MODEL ---
@st.cache_resource
def load_model():
    return joblib.load('ecomagnet_model.pkl')

model = load_model()

# --- 3. CURRENCY DICTIONARY ---
# We map the country/currency to its specific symbol
currency_dict = {
    "USD ($) - United States": "$",
    "INR (₹) - India": "₹",
    "SAR (﷼) - Saudi Arabia": "﷼",
    "AED (د.إ) - UAE": "د.إ",
    "QAR (﷼) - Qatar": "﷼",
    "KWD (د.ك) - Kuwait": "د.ك",
    "OMR (ر.ع.) - Oman": "ر.ع.",
    "BHD (.د.ب) - Bahrain": ".د.ب",
    "RUB (₽) - Russia": "₽",
    "KZT (₸) - Kazakhstan": "₸",
    "TRY (₺) - Turkey": "₺"
}

# --- 4. SIDEBAR: GLOBAL MARKET INPUTS ---
st.sidebar.header("🌍 Localization & Market Data")

# Currency Selector
selected_region = st.sidebar.selectbox("Select Region / Currency", list(currency_dict.keys()))
sym = currency_dict[selected_region] # This variable holds the chosen symbol!

# Financial inputs now dynamically show the selected currency symbol
iron_price = st.sidebar.number_input(f"Iron Ore Price ({sym}/ton)", value=110.0, step=5.0)
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

# --- 6. INTERACTIVE FINANCIAL GRAPH ---
st.write("---")
st.subheader("Financial & ESG Impact Visualization")

fig = go.Figure(data=[
    go.Bar(name=f'Gross Revenue ({sym})', x=['Baseline', 'AI Optimized'], y=[(base_recovery/100)*iron_price, (ai_recovery/100)*iron_price], marker_color='#2ecc71'),
    go.Bar(name=f'Energy Cost ({sym})', x=['Baseline', 'AI Optimized'], y=[base_kwh*energy_cost, ai_kwh*energy_cost], marker_color='#e74c3c'),
    go.Bar(name=f'Carbon Tax ({sym})', x=['Baseline', 'AI Optimized'], y=[(base_co2/1000)*carbon_tax, (ai_co2/1000)*carbon_tax], marker_color='#34495e')
])
fig.update_layout(barmode='group', title=f"Cost vs Revenue per Ton Processed ({sym})", template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# --- 7. THE "AHA" METRIC (Net Profit) ---
profit_diff = ai_profit - base_profit
st.metric("AI Generated Value (Extra Profit per Ton)", f"{sym}{profit_diff:.2f}", delta=f"{profit_diff/base_profit * 100:.1f}% Increase")

# --- 8. EXECUTIVE REPORT DOWNLOAD ---
st.write("---")
report_data = pd.DataFrame({
    "Metric": ["Recovery (%)", "Energy (kWh)", "CO2 Emissions (kg)", f"Net Profit ({sym})"],
    "Manual Settings": [round(base_recovery,2), round(base_kwh,2), round(base_co2,2), round(base_profit,2)],
    "AI Optimized": [round(ai_recovery,2), round(ai_kwh,2), round(ai_co2,2), round(ai_profit,2)]
})

csv = report_data.to_csv(index=False).encode('utf-8')

st.download_button(
    label=f"📥 Download Executive Summary (CSV format - {sym})",
    data=csv,
    file_name='EcoMagnet_Global_Report.csv',
    mime='text/csv',
)
