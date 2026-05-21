import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Smart Navigation Dashboard",
    layout="wide"
)

# =========================
# LOAD DATA (FIXED TOTAL)
# =========================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(
            "hasil_kuesioner.csv",
            sep="\t",                 # karena file kamu TAB-separated
            engine="python",
            encoding="latin1",       # aman untuk Excel Indonesia
            on_bad_lines="skip"      # skip baris yang rusak
        )
        return df

    except Exception as e:
        st.error("Gagal membaca file dataset. Periksa format file CSV/TSV kamu.")
        st.exception(e)
        return pd.DataFrame()

df = load_data()

# Stop kalau data kosong
if df.empty:
    st.stop()

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
st.dataframe(df, use_container_width=True)

# =========================
# DETEKSI VARIABEL OTOMATIS
# =========================
x_cols = [c for c in df.columns if str(c).strip().upper().startswith("X")]
y_cols = [c for c in df.columns if str(c).strip().upper().startswith("Y")]

# =========================
# RINGKASAN DATA
# =========================
st.subheader("Ringkasan Data")

col1, col2, col3 = st.columns(3)
col1.metric("Total Responden", len(df))
col2.metric("Variabel X", len(x_cols))
col3.metric("Variabel Y", len(y_cols))

st.divider()

# =========================
# VARIABEL X
# =========================
st.subheader("User-Generated Metadata (X)")

if len(x_cols) > 0:
    x_selected = st.selectbox("Pilih Variabel X", x_cols)

    fig_x = px.histogram(
        df,
        x=x_selected,
        title=f"Distribusi {x_selected}"
    )
    st.plotly_chart(fig_x, use_container_width=True)
else:
    st.warning("Kolom X tidak terdeteksi (cek penamaan kolom di dataset).")

# =========================
# VARIABEL Y
# =========================
st.subheader("Akurasi Navigasi (Y)")

if len(y_cols) > 0:
    y_selected = st.selectbox("Pilih Variabel Y", y_cols)

    fig_y = px.histogram(
        df,
        x=y_selected,
        title=f"Distribusi {y_selected}"
    )
    st.plotly_chart(fig_y, use_container_width=True)
else:
    st.warning("Kolom Y tidak terdeteksi (cek penamaan kolom di dataset).")

# =========================
# HUBUNGAN X vs Y
# =========================
st.subheader("Hubungan Variabel (Insight Awal)")

if len(x_cols) > 0 and len(y_cols) > 0:
    try:
        fig_scatter = px.scatter(
            df,
            x=x_cols[0],
            y=y_cols[0],
            trendline="ols",
            title=f"{x_cols[0]} vs {y_cols[0]}"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    except Exception:
        # fallback kalau statsmodels tidak ada
        fig_scatter = px.scatter(
            df,
            x=x_cols[0],
            y=y_cols[0],
            title=f"{x_cols[0]} vs {y_cols[0]}"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

# =========================
# FILTER SIDEBAR
# =========================
st.sidebar.header("Filter Data")

if "Platform" in df.columns:
    platform_filter = st.sidebar.multiselect(
        "Pilih Platform Transportasi",
        df["Platform"].dropna().unique()
    )

    if platform_filter:
        df = df[df["Platform"].isin(platform_filter)]
        st.rerun()
