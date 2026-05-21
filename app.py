import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Smart Navigation Dashboard", layout="wide")

# =========================
# LOAD DATA (sesuai file kamu)
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("hasil_kuesioner.csv")  # SESUAI NAMA FILE KAMU
    return df

df = load_data()

# =========================
# HEADER
# =========================
st.title("Smart Navigation Dashboard")
st.caption("Analisis Pengaruh User-Generated Metadata terhadap Akurasi Navigasi Transportasi Online")

st.divider()

# =========================
# DATA OVERVIEW
# =========================
st.subheader("Dataset Responden")
st.dataframe(df)

# =========================
# DETEKSI VARIABEL OTOMATIS
# =========================
x_cols = [c for c in df.columns if c.upper().startswith("X")]
y_cols = [c for c in df.columns if c.upper().startswith("Y")]

# =========================
# RINGKASAN
# =========================
st.subheader("Ringkasan Data")

col1, col2, col3 = st.columns(3)
col1.metric("Total Responden", len(df))
col2.metric("Jumlah Variabel X", len(x_cols))
col3.metric("Jumlah Variabel Y", len(y_cols))

st.divider()

# =========================
# VARIABEL X
# =========================
st.subheader("User-Generated Metadata (X)")

if x_cols:
    x_selected = st.selectbox("Pilih Variabel X", x_cols)
    fig = px.histogram(df, x=x_selected, title=f"Distribusi {x_selected}")
    st.plotly_chart(fig, use_container_width=True)

# =========================
# VARIABEL Y
# =========================
st.subheader("Akurasi Navigasi (Y)")

if y_cols:
    y_selected = st.selectbox("Pilih Variabel Y", y_cols)
    fig = px.histogram(df, x=y_selected, title=f"Distribusi {y_selected}")
    st.plotly_chart(fig, use_container_width=True)

# =========================
# HUBUNGAN X vs Y
# =========================
st.subheader("Hubungan Variabel (Insight Awal)")

if x_cols and y_cols:
    fig = px.scatter(
        df,
        x=x_cols[0],
        y=y_cols[0],
        trendline="ols",
        title=f"{x_cols[0]} vs {y_cols[0]}"
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================
# FILTER (opsional)
# =========================
st.sidebar.header("Filter")

if "Platform" in df.columns:
    platform = st.sidebar.multiselect(
        "Platform Transportasi",
        df["Platform"].dropna().unique()
    )

    if platform:
        df = df[df["Platform"].isin(platform)]
