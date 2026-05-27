import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SETTING HALAMAN & STYLE HOQ RUMAH
st.set_page_config(page_title="Digital HoQ - UKM Tahu", layout="wide")

# HEX Codes dari palet: #810530 (Maroon), #F1E2D0 (Cream), #D9C5B2 (Beige), #4E1D19 (Deep Coffee)
st.markdown("""
    <style>
    .stApp {
        background-color: #FDFBF9;
    }

    .main-header { 
        font-size: 32px; 
        font-weight: bold; 
        color: #810530; 
        margin-bottom: 10px; 
    }
    
    .sub-header { 
        font-size: 18px; 
        color: #4E1D19; 
        margin-bottom: 25px; 
    }
    
    .hoq-table {
        border-collapse: collapse;
        margin: 20px 0;
        font-family: 'Segoe UI', sans-serif;
        width: 100%;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 10px 15px -3px rgba(78, 29, 25, 0.1);
        background-color: #ffffff;
    }
    
    .hoq-table th, .hoq-table td {
        border: 1px solid #D9C5B2;
        padding: 14px;
        text-align: center;
        font-size: 14px;
        color: #4E1D19 !important;
    }

    /* Kepala Tabel (Maroon) */
    .hoq-th-corner, .hoq-th-hows {
        background-color: #810530 !important;
        color: #F1E2D0 !important;
        font-weight: 700;
    }

    /* Importance Header (Deep Coffee) */
    .hoq-importance-header {
        background-color: #4E1D19 !important;
        color: #F1E2D0 !important;
        font-weight: 700;
    }

    /* WHATs Column (Cream) */
    .hoq-td-whats {
        background-color: #F1E2D0 !important;
        text-align: left !important;
        font-weight: 600;
        color: #4E1D19 !important;
    }

    /* Importance Values (Beige) */
    .hoq-importance {
        background-color: #D9C5B2 !important;
        font-weight: 700;
    }
    
    /* Fondasi Bawah */
    .hoq-score-row {
        background-color: #F1E2D0 !important;
        font-weight: bold;
        border-top: 3px solid #810530;
    }
    .hoq-weight-row {
        background-color: #D9C5B2 !important;
        font-weight: bold;
    }

    .legend-box {
        background-color: #F1E2D0;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #D9C5B2;
        color: #4E1D19;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-header">🏠 Digital House of Quality (HoQ)</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Premium Analysis for UKM Tahu Endang</p>', unsafe_allow_html=True)

# --- Logic Data & Tabs (Tetap sama) ---
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

t1, t2, t3, t4, t5, t6 = st.tabs(["1. WHATs", "2. HOWs", "3. Correlation", "4. Matrix", "5. 🏆 FINAL", "🏛️ 6. FULL HOQ"])

# Filter list dinamis
whats_list = [x for x in st.session_state.df_whats["Customer Requirement (WHATs)"].tolist() if pd.notna(x) and x != ""]
hows_list = [x for x in st.session_state.df_hows["Technical Requirement (HOWs)"].tolist() if pd.notna(x) and x != ""]

# (Bagian Input Tab 1-4 diabaikan di sini agar ringkas, asumsikan tetap sama)
# ... [Lanjutkan dengan TAB 1 - 4 dari kode sebelumnya] ...

# --- TAB 6: FULL HOQ ARCHITECTURE DENGAN NEW PALETTE ---
with t6:
    try:
        # Perhitungan (Silently using weights & rel_matrix)
        valid_whats = st.session_state.df_whats[st.session_state.df_whats["Customer Requirement (WHATs)"].isin(whats_list)]
        weights = valid_whats["Importance (1-5)"].values.astype(float)
        matrix_values = st.session_state.rel_matrix.loc[whats_list, hows_list].values.astype(float)
        abs_importance = weights @ matrix_values
        total = abs_importance.sum()
        rel_importance = (abs_importance / total * 100) if total > 0 else abs_importance * 0
        
        n_hows = len(hows_list)
        
        html_hoq = '<div class="hoq-scroll-container">'
        html_hoq += '<table class="hoq-table" style="width:auto; margin:auto;">'
        
        # Atap Segitiga
        for i in range(n_hows - 1):
            html_hoq += '<tr><td style="border:none; background:transparent;" colspan="2"></td>'
            for j in range(n_hows):
                if j < (n_hows - 1 - i):
                    html_hoq += '<td style="border:none; background:transparent;"></td>'
                else:
                    # Logic Simbol Atap
                    html_hoq += f'<td style="background-color: #F1E2D0; color: #810530; font-weight:bold;">0</td>'
            html_hoq += '</tr>'

        # Header
        html_hoq += '<tr><th class="hoq-th-corner">WHATs</th><th class="hoq-importance-header">Imp</th>'
        for col in hows_list: html_hoq += f'<th class="hoq-th-hows">{col}</th>'
        html_hoq += '</tr>'
        
        # Body
        for idx, row_name in enumerate(whats_list):
            html_hoq += f'<tr><td class="hoq-td-whats">{row_name}</td><td class="hoq-importance">{int(weights[idx])}</td>'
            for col_name in hows_list:
                score = st.session_state.rel_matrix.at[row_name, col_name]
                bg = "#ffffff" if score == 0 else "#D9C5B2" if score == 1 else "#F1E2D0" if score == 3 else "#810530"
                txt = "#4E1D19" if score < 9 else "#F1E2D0"
                sym = "◎" if score == 9 else "○" if score == 3 else "△" if score == 1 else ""
                html_hoq += f'<td style="background-color:{bg}; color:{txt}; font-size:18px;">{sym}</td>'
            html_hoq += '</tr>'
            
        # Fondasi
        html_hoq += f'<tr class="hoq-score-row"><td>Score</td><td>-</td>'
        for s in abs_importance: html_hoq += f'<td>{int(s)}</td>'
        html_hoq += '</tr>'
        
        html_hoq += '</table></div>'
        st.markdown(html_hoq, unsafe_allow_html=True)
        
    except Exception as e:
        st.info("Isi data di Tab 1-4 dulu ya!")