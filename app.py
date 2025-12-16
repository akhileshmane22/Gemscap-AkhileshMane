import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Real-Time Pair Trading Analytics", layout="wide")

st.title("📈 Real-Time Pair Trading Analytics")

# -----------------------------
# UI Controls
# -----------------------------
symbol1 = st.selectbox("Symbol 1", ["btcusdt", "ethusdt", "bnbusdt"])
symbol2 = st.selectbox("Symbol 2", ["ethusdt", "bnbusdt", "btcusdt"])
lookback_minutes = st.slider("Lookback Window (minutes)", 1, 30, 5)

st.markdown("---")

# -----------------------------
# Load data from SQLite
# -----------------------------
@st.cache_data(ttl=1)  # refresh every second
def load_ticks(symbols, minutes):
    con = sqlite3.connect("ticks.db")
    since = datetime.utcnow() - timedelta(minutes=minutes)

    query = f"""
        SELECT *
        FROM ticks
        WHERE symbol IN ({','.join([f"'{s}'" for s in symbols])})
          AND timestamp >= '{since}'
        ORDER BY timestamp
    """

    df = pd.read_sql(query, con, parse_dates=["timestamp"])
    con.close()
    return df

df = load_ticks([symbol1, symbol2], lookback_minutes)

# -----------------------------
# Handle empty state
# -----------------------------
if df.empty:
    st.warning("Waiting for live data to accumulate...")
    st.stop()

# -----------------------------
# Plot live prices
# -----------------------------
st.subheader("Live Prices")

fig = px.line(
    df,
    x="timestamp",
    y="price",
    color="symbol",
    title="Price vs Time"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Data export
# -----------------------------
st.download_button(
    "⬇️ Download Raw Tick Data (CSV)",
    data=df.to_csv(index=False).encode(),
    file_name="ticks_data.csv",
    mime="text/csv"
)
