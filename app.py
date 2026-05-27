import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================

st.set_page_config(
    page_title="Smart Navigation Dashboard",
    page_icon="🛰️",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.stMetric {
    background-color: white;
    padding: 15px;
    border-radius: 15px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}

h1, h2, h3 {
    color: #111827;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    # BACA FILE EXCEL
    df = pd.read_excel("Hasil Kuesioner.xlsx")

    # MEMBERSIHKAN NAMA KOLOM
    df.columns = df.columns.str.strip()

    return df

df = load_data()

# =========================================================
# DEBUG NAMA KOLOM
# =========================================================
# HAPUS ATAU COMMENT SETELAH DASHBOARD NORMAL

# st.write(df.columns.tolist())

# =========================================================
# VARIABEL PENELITIAN
# =========================================================

# Variabel X valid
x_columns = ["X1.1", "X1.2", "X1.3", "X1.4", "X1.6"]

# Variabel Y valid
y_columns = ["Y2", "Y3", "Y4", "Y6"]

# =========================================================
# KONVERSI DATA NUMERIK
# =========================================================

for col in x_columns + y_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# =========================================================
# HITUNG NILAI RATA-RATA
# =========================================================

df["Rata_X"] = df[x_columns].mean(axis=1)
df["Rata_Y"] = df[y_columns].mean(axis=1)

avg_x = round(df["Rata_X"].mean(), 2)
avg_y = round(df["Rata_Y"].mean(), 2)

# =========================================================
# NAMA KOLOM
# =========================================================

gender_col = "Jenis Kelamin"

platform_col = "Platform Transportasi Berbasis Aplikasi yang Digunakan"

misleading_col = "Pernah Mengalami Ketidaksesuaian Titik Lokasi (Misleading Points)"

metadata_col = "Pernah Ada Informasi Tambahan dari Pelanggan \n(seperti landmark, deskripsi lokasi, atau petunjuk arah tambahan)"

# =========================================================
# SIDEBAR FILTER
# =========================================================

st.sidebar.title("📌 Filter Dashboard")

gender_filter = st.sidebar.multiselect(
    "Jenis Kelamin",
    options=df[gender_col].dropna().unique(),
    default=df[gender_col].dropna().unique()
)

platform_filter = st.sidebar.multiselect(
    "Platform Transportasi",
    options=df[platform_col].dropna().unique(),
    default=df[platform_col].dropna().unique()
)

filtered_df = df[
    (df[gender_col].isin(gender_filter)) &
    (df[platform_col].isin(platform_filter))
]

# =========================================================
# HEADER
# =========================================================

st.title("🛰️ Smart Navigation Accuracy Monitoring Dashboard")

st.markdown("""
### Analisis Pengaruh *User-Generated Metadata* terhadap Akurasi Navigasi Transportasi Berbasis Aplikasi

Dashboard ini dikembangkan untuk membantu visualisasi
dan evaluasi hasil penelitian mengenai pengaruh
*User-Generated Metadata* terhadap akurasi navigasi
pada layanan transportasi berbasis aplikasi.
""")

st.markdown("---")

# =========================================================
# KPI CARDS
# =========================================================

total_responden = len(filtered_df)

misleading_total = filtered_df[misleading_col].value_counts().get("Pernah", 0)

metadata_total = filtered_df[metadata_col].value_counts().get("Pernah", 0)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Responden", total_responden)

with col2:
    st.metric("Rata-rata Metadata", avg_x)

with col3:
    st.metric("Rata-rata Akurasi", avg_y)

with col4:
    st.metric("Misleading Points", misleading_total)

st.markdown("---")

# =========================================================
# PROFIL RESPONDEN
# =========================================================

st.header("📊 Profil Responden")

col_a, col_b = st.columns(2)

# PIE CHART GENDER
with col_a:

    gender_data = filtered_df[gender_col].value_counts().reset_index()
    gender_data.columns = ["Jenis Kelamin", "Jumlah"]

    fig_gender = px.pie(
        gender_data,
        names="Jenis Kelamin",
        values="Jumlah",
        hole=0.5,
        title="Distribusi Jenis Kelamin"
    )

    st.plotly_chart(fig_gender, use_container_width=True)

# BAR CHART PLATFORM
with col_b:

    platform_data = filtered_df[platform_col].value_counts().reset_index()
    platform_data.columns = ["Platform", "Jumlah"]

    fig_platform = px.bar(
        platform_data,
        x="Platform",
        y="Jumlah",
        text_auto=True,
        title="Platform Transportasi yang Digunakan"
    )

    st.plotly_chart(fig_platform, use_container_width=True)

st.markdown("---")

# =========================================================
# ANALISIS USER GENERATED METADATA
# =========================================================

st.header("📍 Analisis User-Generated Metadata (Variabel X)")

x_mean = filtered_df[x_columns].mean().reset_index()
x_mean.columns = ["Indikator", "Rata-rata"]

fig_x = px.bar(
    x_mean,
    x="Indikator",
    y="Rata-rata",
    color="Rata-rata",
    text_auto=".2f",
    title="Efektivitas User-Generated Metadata"
)

fig_x.update_layout(
    yaxis_range=[0, 5],
    xaxis_title="Indikator",
    yaxis_title="Rata-rata Skor"
)

st.plotly_chart(fig_x, use_container_width=True)

st.info("""
Metadata pengguna seperti landmark,
deskripsi lokasi, dan petunjuk arah tambahan
membantu meningkatkan efektivitas navigasi digital.
""")

st.markdown("---")

# =========================================================
# ANALISIS AKURASI NAVIGASI
# =========================================================

st.header("🧭 Analisis Akurasi Navigasi (Variabel Y)")

y_mean = filtered_df[y_columns].mean().reset_index()
y_mean.columns = ["Indikator", "Rata-rata"]

fig_y = px.line(
    y_mean,
    x="Indikator",
    y="Rata-rata",
    markers=True,
    title="Tingkat Akurasi Navigasi"
)

fig_y.update_layout(
    yaxis_range=[0, 5],
    xaxis_title="Indikator",
    yaxis_title="Rata-rata Skor"
)

st.plotly_chart(fig_y, use_container_width=True)

st.success("""
Informasi tambahan dari pengguna membantu
meningkatkan akurasi navigasi dan mengurangi misleading points.
""")

st.markdown("---")

# =========================================================
# ANALISIS HUBUNGAN VARIABEL
# =========================================================

st.header("🔗 Analisis Pengaruh Variabel")

fig_relation = px.scatter(
    filtered_df,
    x="Rata_X",
    y="Rata_Y",
    trendline="ols",
    title="Hubungan User-Generated Metadata dan Akurasi Navigasi",
    labels={
        "Rata_X": "User-Generated Metadata",
        "Rata_Y": "Akurasi Navigasi"
    }
)

st.plotly_chart(fig_relation, use_container_width=True)

st.markdown("""
### Interpretasi Hasil

Semakin tinggi efektivitas *User-Generated Metadata*,
maka semakin tinggi tingkat akurasi navigasi
pada layanan transportasi berbasis aplikasi.
""")

st.markdown("---")

# =========================================================
# HASIL SMARTPLS
# =========================================================

st.header("📈 Hasil Analisis SmartPLS")

pls_result = pd.DataFrame({
    "Hubungan Variabel": [
        "User Generated Metadata → Akurasi Navigasi"
    ],
    "Path Coefficient": [0.815],
    "T Statistics": [7.801],
    "P-Value": [0.000]
})

st.dataframe(pls_result, use_container_width=True)

st.success("""
Variabel User-Generated Metadata
berpengaruh positif dan signifikan
terhadap Akurasi Navigasi.
""")

st.markdown("---")

# =========================================================
# VALIDITAS DAN RELIABILITAS
# =========================================================

st.header("✅ Uji Validitas dan Reliabilitas")

validity_df = pd.DataFrame({
    "Variabel": [
        "Akurasi Navigasi",
        "User Generated Metadata"
    ],
    "Cronbach Alpha": [0.914, 0.949],
    "Composite Reliability": [0.939, 0.962],
    "AVE": [0.795, 0.834]
})

st.dataframe(validity_df, use_container_width=True)

st.info("""
Seluruh variabel memenuhi syarat validitas
dan reliabilitas karena nilai
Cronbach Alpha > 0.70 dan AVE > 0.50.
""")

st.markdown("---")

# =========================================================
# OUTER LOADING
# =========================================================

st.header("📋 Outer Loading")

outer_loading = pd.DataFrame({
    "Indikator": [
        "X1.1",
        "X1.2",
        "X1.3",
        "X1.4",
        "X1.6",
        "Y2",
        "Y3",
        "Y4",
        "Y6"
    ],
    "Outer Loading": [
        0.958,
        0.869,
        0.950,
        0.956,
        0.826,
        0.820,
        0.943,
        0.908,
        0.893
    ]
})

fig_outer = px.bar(
    outer_loading,
    x="Indikator",
    y="Outer Loading",
    color="Outer Loading",
    text_auto=".3f",
    title="Nilai Outer Loading Variabel Penelitian"
)

fig_outer.update_layout(
    yaxis_range=[0, 1.1]
)

st.plotly_chart(fig_outer, use_container_width=True)

st.info("""
Seluruh indikator memiliki nilai outer loading > 0.70
sehingga dinyatakan valid.

Indikator X1.5, Y1, dan Y5 tidak digunakan
karena tidak memenuhi validitas konvergen.
""")

st.markdown("---")

# =========================================================
# INSIGHT PENELITIAN
# =========================================================

st.header("💡 Insight Penelitian")

highest_x = x_mean.loc[x_mean["Rata-rata"].idxmax()]
highest_y = y_mean.loc[y_mean["Rata-rata"].idxmax()]

st.write(f"""
- Indikator metadata tertinggi terdapat pada
**{highest_x['Indikator']}**
dengan rata-rata skor **{round(highest_x['Rata-rata'], 2)}**.

- Indikator akurasi navigasi tertinggi terdapat pada
**{highest_y['Indikator']}**
dengan rata-rata skor **{round(highest_y['Rata-rata'], 2)}**.

- Hasil penelitian menunjukkan bahwa metadata pengguna
memiliki kontribusi penting dalam meningkatkan
akurasi navigasi digital.
""")

st.markdown("---")

# =========================================================
# KESIMPULAN
# =========================================================

st.header("📌 Kesimpulan")

st.write("""
Dashboard ini membantu proses visualisasi
dan evaluasi hasil penelitian mengenai pengaruh
User-Generated Metadata terhadap Akurasi Navigasi
pada layanan transportasi berbasis aplikasi.

Berdasarkan hasil analisis SmartPLS,
User-Generated Metadata terbukti memiliki
pengaruh positif dan signifikan terhadap
akurasi navigasi dengan nilai path coefficient 0.815
dan P-value 0.000.

Pemanfaatan landmark, deskripsi lokasi,
dan petunjuk arah tambahan membantu meningkatkan
ketepatan identifikasi lokasi dan mengurangi misleading points.
""")

st.markdown("---")

st.caption("Smart Navigation Accuracy Monitoring Dashboard © 2026")
