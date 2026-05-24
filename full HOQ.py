import streamlit as st
import pandas as pd

# 1. SETTING HALAMAN & STYLE HOQ RUMAH
st.set_page_config(page_title="Digital HoQ - UKM Tahu", layout="wide")

st.markdown("""
    <style>
    .main-header { font-size: 28px; font-weight: bold; color: #38bdf8; margin-bottom: 10px; }
    .sub-header { font-size: 18px; color: #94a3b8; margin-bottom: 20px; }
    
    /* Style Tabel Rumah HoQ untuk Tema Gelap (Dark Mode) */
    .hoq-table {
        border-collapse: collapse;
        margin: 20px 0;
        font-family: sans-serif;
        width: 100%;
        border-radius: 8px;
        overflow: hidden;
        background-color: #0f172a; 
    }
    .hoq-table th, .hoq-table td {
        border: 1px solid #334155;
        padding: 12px;
        text-align: center;
        font-size: 14px;
        color: #ffffff !important; 
    }
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
    
    .hoq-table td:not([style]) {
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
    }
    
    /* Style Atap Atas (HOWs) */
    .roof-blank {
        background-color: transparent !important;
        border: none !important;
    }
    .roof-cell {
        background-color: #1e293b;
        border: 1px solid #475569 !important;
        font-weight: bold;
    }

    /* Style Atap Samping Kiri (WHATs) */
    .side-roof-cell {
        font-weight: bold;
        border: 1px solid #475569 !important;
    }
    .side-roof-header {
        background-color: #0f172a !important;
        font-size: 11px;
        color: #94a3b8 !important;
        border: none !important;
    }
    
    .legend-box {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #334155;
        margin-bottom: 15px;
    }
    
    .hoq-scroll-container {
        width: 100%;
        overflow-x: auto;
        padding-bottom: 15px;
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

whats_list = [x for x in st.session_state.df_whats["Customer Requirement (WHATs)"].tolist() if pd.notna(x) and x != ""]
hows_list = [x for x in st.session_state.df_hows["Technical Requirement (HOWs)"].tolist
