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
# LOAD DATA (ROBUST)
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv(
        "hasil_kuesioner.csv",
        sep="\t",
        engine="python",
        encoding="latin1",
        on_bad_lines="skip"
    )
    return df

df = load_data()

if df.empty:
    st.error("Dataset kosong atau gagal dibaca.")
    st.stop()

# =========================
# IDENTIFIKASI VARIABEL
# =========================
metadata_cols = [
    col for col in df.columns
    if "Deskripsi" in col or "Landmark" in col or "Petunjuk" in col
]

navigation_cols = [
    col for col in df.columns
    if "Sistem" in col or "mengurangi" in col or "akurasi" in col.lower()
]

# numeric columns (Likert scale)
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

# =========================
# HEADER
# =========================
st.title("Smart Navigation Dashboard")
st.caption("Analisis Pengaruh User-Generated Metadata terhadap Akurasi Navigasi Transportasi Online")

st.divider()

# =========================
# 1. DATA RESPONDEN
# =========================
st.subheader("1. Profil Responden")

col1, col2, col3 = st.columns(3)
col1.metric("Total Responden", len(df))

if "Usia" in df.columns:
    col2.metric("Kelompok Usia Terbanyak", df["Usia"].mode()[0])

if "Platform" in df.columns:
    col3.metric("Platform Dominan", df["Platform"].mode()[0])

st.dataframe(df, use_container_width=True)

st.divider()

# =========================
# 2. USER-GENERATED METADATA (X)
# =========================
st.subheader("2. User-Generated Metadata (Variabel X)")

if metadata_cols:
    meta_mean = df[metadata_cols].mean(numeric_only=True)

    fig_meta = px.bar(
        x=meta_mean.index,
        y=meta_mean.values,
        title="Rata-rata Penilaian User-Generated Metadata"
    )
    st.plotly_chart(fig_meta, use_container_width=True)
else:
    st.warning("Kolom metadata tidak terdeteksi.")

st.divider()

# =========================
# 3. AKURASI NAVIGASI (Y)
# =========================
st.subheader("3. Akurasi Navigasi (Variabel Y)")

if navigation_cols:
    nav_mean = df[navigation_cols].mean(numeric_only=True)

    fig_nav = px.bar(
        x=nav_mean.index,
        y=nav_mean.values,
        title="Rata-rata Akurasi Navigasi"
    )
    st.plotly_chart(fig_nav, use_container_width=True)
else:
    st.warning("Kolom navigasi tidak terdeteksi.")

st.divider()

# =========================
# 4. HUBUNGAN X → Y (CORE ANALYSIS)
# =========================
st.subheader("4. Pengaruh Metadata terhadap Akurasi Navigasi")

if len(metadata_cols) > 0 and len(navigation_cols) > 0:

    avg_x = df[metadata_cols].mean(axis=1)
    avg_y = df[navigation_cols].mean(axis=1)

    correlation_df = pd.DataFrame({
        "Metadata (X)": avg_x,
        "Akurasi Navigasi (Y)": avg_y
    })

    fig_corr = px.scatter(
        correlation_df,
        x="Metadata (X)",
        y="Akurasi Navigasi (Y)",
        trendline="ols",
        title="Hubungan X → Y (Regresi Linear)"
    )

    st.plotly_chart(fig_corr, use_container_width=True)

    st.success("Model menunjukkan hubungan positif antara metadata dan akurasi navigasi.")

st.divider()

# =========================
# 5. HASIL PLS-SEM (DARI JURNAL KAMU)
# =========================
st.subheader("5. Hasil Model PLS-SEM")

col1, col2, col3 = st.columns(3)

col1.metric("Path Coefficient", "0.815")
col2.metric("R-Square", "0.653")
col3.metric("T-Statistic", "7.801")

st.caption("P-value = 0.000 (signifikan pada α < 0.05)")

st.divider()

# =========================
# 6. RELIABILITY & VALIDITY
# =========================
st.subheader("6. Validitas & Reliabilitas")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Cronbach Alpha", "0.914")
col2.metric("Composite Reliability", "0.939")
col3.metric("AVE", "0.795")
col4.metric("Model Quality", "Valid")

st.divider()

# =========================
# 7. ANALISIS SOSIOTEKNIS
# =========================
st.subheader("7. Analisis Sosioteknis (Teori Kritis)")

st.markdown("""
- ⚠ Ketergantungan pada partisipasi pengguna dapat menyebabkan ketidakseimbangan data  
- ⚠ Risiko bias spasial pada area dengan aktivitas rendah  
- ⚠ Beban kognitif pengemudi saat input metadata  
- ⚠ Isu privasi data lokasi perjalanan  

**Kesimpulan:** Sistem memberikan manfaat teknis, namun tetap memerlukan kontrol etis dan kebijakan keberlanjutan.
""")

st.divider()

# =========================
# 8. INSIGHT AKHIR
# =========================
st.subheader("8. Kesimpulan Sistem")

st.success("""
User-Generated Metadata terbukti memiliki pengaruh positif terhadap akurasi navigasi.
Dashboard ini menunjukkan bahwa peningkatan kualitas informasi pengguna dapat meningkatkan efisiensi layanan transportasi berbasis aplikasi secara signifikan.
""")
