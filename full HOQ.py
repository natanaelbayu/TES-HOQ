import streamlit as st
import pandas as pd
import plotly.express as px

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
hows_list = [x for x in st.session_state.df_hows["Technical Requirement (HOWs)"].tolist() if pd.notna(x) and x != ""]

# Inisialisasi Matriks Korelasi Samping (WHATs vs WHATs)
if 'whats_roof_matrix' not in st.session_state or list(st.session_state.whats_roof_matrix.columns) != whats_list:
    st.session_state.whats_roof_matrix = pd.DataFrame("No Correlation (0)", index=whats_list, columns=whats_list)

# --- TABS STRUKTUR ---
t1, t2, t3, t4, t5, t6 = st.tabs([
    "1. WHATs", "2. HOWs", "3. Correlation (Top & Side)", "4. Matrix", "5. 🏆 FINAL HOUSE & ACTION PLAN", "🏛️ 6. FULL HOQ ARCHITECTURE"
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

# TAB 3: Correlation (Atap Atas & Samping Kiri)
with t3:
    col_roof_side, col_roof_top = st.columns(2)
    
    with col_roof_side:
        st.subheader("📐 Matriks Atap Samping Kiri (WHATs vs WHATs)")
        st.caption("Pilih nilai hubungan korelasi antar kebutuhan pelanggan (WHATs).")
        whats_roof_config = {col: st.column_config.SelectboxColumn(col, options=["Strong Positive (++)", "Positive (+)", "No Correlation (0)", "Negative (-)", "Strong Negative (--)"], required=True) for col in whats_list}
        st.session_state.whats_roof_matrix = st.data_editor(st.session_state.whats_roof_matrix, use_container_width=True, column_config=whats_roof_config, key="ed_whats_roof")

    with col_roof_top:
        st.subheader("🛖 Matriks Atap Atas (HOWs vs HOWs)")
        if 'roof_matrix' not in st.session_state or list(st.session_state.roof_matrix.columns) != hows_list:
            st.session_state.roof_matrix = pd.DataFrame("No Correlation (0)", index=hows_list, columns=hows_list)
        
        roof_column_config = {col: st.column_config.SelectboxColumn(col, options=["Strong Positive (++)", "Positive (+)", "No Correlation (0)", "Negative (-)", "Strong Negative (--)"], required=True) for col in hows_list}
        st.session_state.roof_matrix = st.data_editor(st.session_state.roof_matrix, use_container_width=True, column_config=roof_column_config, key="ed_roof")

# TAB 4: Relationship Matrix
with t4:
    st.subheader("♾️ Hubungan Kebutuhan Konsumen vs Spesifikasi Teknis")
    if 'rel_matrix' not in st.session_state or list(st.session_state.rel_matrix.columns) != hows_list or list(st.session_state.rel_matrix.index) != whats_list:
        st.session_state.rel_matrix = pd.DataFrame(0, index=whats_list, columns=hows_list)
    
    rel_column_config = {col: st.column_config.SelectboxColumn(col, options=[0, 1, 3, 9], required=True) for col in hows_list}
    st.session_state.rel_matrix = st.data_editor(st.session_state.rel_matrix, use_container_width=True, column_config=rel_column_config, key="ed_rel")

# TAB 5: FINAL HOUSE & ACTION PLAN
with t5:
    try:
        valid_whats = st.session_state.df_whats[st.session_state.df_whats["Customer Requirement (WHATs)"].isin(whats_list)]
        weights = valid_whats["Importance (1-5)"].values.astype(float)
        matrix_values = st.session_state.rel_matrix.loc[whats_list, hows_list].values.astype(float)
        
        abs_importance = weights @ matrix_values
        total = abs_importance.sum()
        rel_importance = (abs_importance / total * 100) if total > 0 else abs_importance * 0

        res_df = pd.DataFrame({"Requirement": hows_list, "Score": abs_importance, "Weight %": rel_importance.round(1)}).sort_values(by="Score", ascending=False)

        st.write("### 💡 Kesimpulan Strategis & Arah Pengembangan")
        top_priorities = res_df.head(3)
        priority_names = top_priorities["Requirement"].tolist()
        priority_weights = top_priorities["Weight %"].tolist()
        
        col_rec, col_summary = st.columns([1.2, 1])
        with col_rec:
            st.success(f"✍️ **Rekomendasi Utama For Business:** Fokus penuh pada **{priority_names[0]}** ({priority_weights[0]}%).")
        with col_summary:
            st.warning("⚠️ **Urutan Urgensi Rencana Aksi:**")
            st.write(f"1. **Segera Eksekusi:** `{priority_names[0]}`.")

    except Exception as e:
        st.error("Lengkapi data di tab sebelumnya!")

# --- 🏛️ TAB 6: FULL HOQ ARCHITECTURE (ROOF SAMPING DI SEBELAH KIRI) ---
with t6:
    try:
        st.write("### 🏛️ Arsitektur Matriks House of Quality (HoQ) Komplit + Roof Kiri")
        
        valid_whats = st.session_state.df_whats[st.session_state.df_whats["Customer Requirement (WHATs)"].isin(whats_list)]
        weights = valid_whats["Importance (1-5)"].values.astype(float)
        matrix_values = st.session_state.rel_matrix.loc[whats_list, hows_list].values.astype(float)
        abs_importance = weights @ matrix_values
        total = abs_importance.sum()
        rel_importance = (abs_importance / total * 100) if total > 0 else abs_importance * 0
        
        n_hows = len(hows_list)
        n_whats = len(whats_list)
        n_side_cols = n_whats - 1  # Jumlah kolom untuk atap samping kiri
        
        # Box Keterangan Simbol (Legend)
        st.markdown("""
        <div class="legend-box">
            <strong>ℹ️ Keterangan Simbol & Warna:</strong><br>
            <span><strong>◎</strong> Kuat (9) | <strong>○</strong> Sedang (3) | <strong>△</strong> Lemah (1)</span><br>
            <span style="border: 1px solid #475569; padding: 2px 5px; background-color: #1e3a8a;">++</span> Strong Positive &nbsp;|&nbsp;
            <span style="border: 1px solid #475569; padding: 2px 5px; background-color: #14532d;">+</span> Positive &nbsp;|&nbsp;
            <span style="border: 1px