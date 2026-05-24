import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SETTING HALAMAN & STYLE HOQ RUMAH
st.set_page_config(page_title="Digital HoQ - UKM Tahu", layout="wide")

st.markdown("""
    <style>
    .main-header { font-size: 28px; font-weight: bold; color: #38bdf8; margin-bottom: 10px; }
    .sub-header { font-size: 18px; color: #94a3b8; margin-bottom: 20px; }
    
    /* Style Tabel Rumah HoQ untuk Tema Gelap (Dark Mode) Uniform */
    .hoq-table {
        border-collapse: collapse;
        margin: 20px 0;
        font-family: sans-serif;
        width: 100%;
        border-radius: 8px;
        overflow: hidden;
        background-color: #0f172a; /* Background dasar tabel gelap */
    }
    .hoq-table th, .hoq-table td {
        border: 1px solid #334155;
        padding: 12px;
        text-align: center;
        font-size: 14px;
        color: #ffffff !important; 
    }
    
    /* Header Kepala Tabel (Satu Warna Gelap Uniform) */
    .hoq-th-corner {
        background-color: #1e293b !important;
        font-weight: 600;
        color: #ffffff !important;
    }
    .hoq-th-hows {
        background-color: #1e293b !important; 
        color: #ffffff !important;  
        font-weight: 600;
    }
    .hoq-importance-header {
        background-color: #1e293b !important;
        color: #ffffff !important;
        font-weight: 600;
    }
    
    /* Kolom Pertama Ke Bawah (Satu Warna Gelap Seragam) */
    .hoq-td-whats {
        background-color: #0f172a !important;
        text-align: left !important;
        font-weight: 600;
        color: #ffffff !important;
    }
    .hoq-importance {
        background-color: #1e293b !important;
        font-weight: 600;
        color: #ffffff !important;
    }
    
    /* Baris Fondasi Hasil Akhir */
    .hoq-score-row {
        background-color: #1e293b;
        font-weight: bold;
        color: #ffffff !important;
        border-top: 2px solid #475569;
    }
    .hoq-weight-row {
        background-color: #1e293b;
        font-weight: bold;
        color: #ffffff !important;
    }
    
    /* Memaksa isi sel default berwarna latar gelap */
    .hoq-table td:not([style]) {
        background-color: #0f172a !important;
        color: #e2e8f0 !important; 
    }
    
    /* Style Khusus untuk Atap Segitiga Segitiga di Tab 6 */
    .roof-blank {
        background-color: transparent !important;
        border: none !important;
    }
    .roof-cell {
        background-color: #1e293b;
        border: 1px solid #475569 !important;
        font-weight: bold;
    }
    
    /* Legend Info Box */
    .legend-box {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #334155;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-header">🏠 Digital House of Quality (HoQ)</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Optimalisasi Spesifikasi Teknis berdasarkan Voice of Customer (UKM Tahu Endang)</p>', unsafe_allow_html=True)

# 2. INISIALISASI DATA (Session State Utama)
if 'df_whats' not in st.session_state:
    st.session_state.df_whats = pd.DataFrame({
        "Customer Requirement (WHATs)": ["Tahu tidak mudah hancur", "Rasa kedelai terasa", "Warna kuning cerah", "Harga terjangkau"],
        "Importance (1-5)": [5, 4, 3, 5]
    })

if 'df_hows' not in st.session_state:
    st.session_state.df_hows = pd.DataFrame({
        "Technical Requirement (HOWs)": ["Tekanan Mesin Pres", "Kualitas Kedelai", "Lama Perebusan", "Takaran Kunyit"],
        "Direction": ["Max", "Max", "Target", "Max"]
    })

# --- TABS STRUKTUR (TAMBAH TAB 6) ---
t1, t2, t3, t4, t5, t6 = st.tabs([
    "1. WHATs", "2. HOWs", "3. Correlation", "4. Matrix", "5. 🏆 FINAL HOUSE", "🏛️ 6. FULL HOQ ARCHITECTURE"
])

# TAB 1: Input WHATs
with t1:
    st.subheader("Masukkan Voice of Customer (WHATs)")
    st.session_state.df_whats = st.data_editor(
        st.session_state.df_whats, num_rows="dynamic", use_container_width=True, 
        column_config={"Importance (1-5)": st.column_config.NumberColumn("Importance (1-5)", min_value=1, max_value=5, step=1)},
        key="ed_whats"
    )

# TAB 2: Input HOWs
with t2:
    st.subheader("Masukkan Spesifikasi Teknis (HOWs)")
    st.session_state.df_hows = st.data_editor(
        st.session_state.df_hows, num_rows="dynamic", use_container_width=True, 
        column_config={"Direction": st.column_config.SelectboxColumn("Direction", options=["Max", "Min", "Target"], required=True)},
        key="ed_hows"
    )

whats_list = [x for x in st.session_state.df_whats["Customer Requirement (WHATs)"].tolist() if pd.notna(x) and x != ""]
hows_list = [x for x in st.session_state.df_hows["Technical Requirement (HOWs)"].tolist() if pd.notna(x) and x != ""]

# TAB 3 (Correlation)
with t3:
    st.subheader("Matriks Korelasi Atap (HOWs vs HOWs)")
    if 'roof_matrix' not in st.session_state or list(st.session_state.roof_matrix.columns) != hows_list:
        st.session_state.roof_matrix = pd.DataFrame("No Correlation (0)", index=hows_list, columns=hows_list)
    
    roof_column_config = {col: st.column_config.SelectboxColumn(col, options=
