
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
        background-color: #0f172a; /* Background dasar tabel gelap modern */
    }
    .hoq-table th, .hoq-table td {
        border: 1px solid #334155;
        padding: 12px;
        text-align: center;
        font-size: 14px;
        color: #f1f5f9; /* Teks default putih/terang */
    }
    .hoq-th-corner {
        background-color: #1e293b;
        font-weight: 600;
        color: #94a3b8;
    }
    .hoq-th-hows {
        background-color: #1E3A8A; /* Warna Biru #1E3A8A tetap di header */
        color: #ffffff !important;  /* Memaksa teks tetap putih cerah */
        font-weight: 600;
    }
    .hoq-td-whats {
        background-color: #38bdf8;
        text-align: left !important;
        font-weight: 600;
        color: #1e293b;
    }
    .hoq-importance {
        background-color: #38bdf8;
        font-weight: 600;
        color: #1e293b;
    }
    .hoq-score-row {
        background-color: #38bdf8;
        font-weight: bold;
        color:  #1e293b;
        border-top: 2px solid #475569;
    }
    .hoq-weight-row {
        background-color: #38bdf8;
        font-weight: bold;
        color: #1e293b;
    }
    
    /* Memaksa isi sel default (nilai 0) berwarna latar hitam/gelap */
    .hoq-table td:not([style]) {
        background-color: #0f172a !important;
        color: #64748b !important;
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

# --- TABS STRUKTUR ---
t1, t2, t3, t4, t5 = st.tabs(["1. WHATs", "2. HOWs", "3. Correlation", "4. Matrix", "5. 🏆 FINAL HOUSE"])

# TAB 1: Input WHATs
with t1:
    st.subheader("Masukkan Voice of Customer (WHATs)")
    st.caption("Isi dengan bobot pentingnya dari 1 (tidak penting) hingga 5 (sangat penting).")
    st.session_state.df_whats = st.data_editor(
        st.session_state.df_whats, 
        num_rows="dynamic", 
        use_container_width=True, 
        column_config={
            "Importance (1-5)": st.column_config.NumberColumn("Importance (1-5)", min_value=1, max_value=5, step=1)
        },
        key="ed_whats"
    )

# TAB 2: Input HOWs
with t2:
    st.subheader("Masukkan Spesifikasi Teknis (HOWs)")
    st.caption("Pilih arah spesifikasi teknis: Max (maksimum), Min (minimum), atau Target (target).")
    st.session_state.df_hows = st.data_editor(
        st.session_state.df_hows, 
        num_rows="dynamic", 
        use_container_width=True, 
        column_config={
            "Direction": st.column_config.SelectboxColumn("Direction", options=["Max", "Min", "Target"], required=True)
        },
        key="ed_hows"
    )

# Filter list dinamis dari apa yang diinput user
whats_list = [x for x in st.session_state.df_whats["Customer Requirement (WHATs)"].tolist() if pd.notna(x) and x != ""]
hows_list = [x for x in st.session_state.df_hows["Technical Requirement (HOWs)"].tolist() if pd.notna(x) and x != ""]

# TAB 3 (Correlation - The Roof)
with t3:
    st.subheader("Matriks Korelasi Atap (HOWs vs HOWs)")
    st.caption("Pilih nilai korelasi antar spesifikasi teknis")
    if 'roof_matrix' not in st.session_state or list(st.session_state.roof_matrix.columns) != hows_list:
        st.session_state.roof_matrix = pd.DataFrame("No Correlation (0)", index=hows_list, columns=hows_list)
    
    roof_column_config = {
        col: st.column_config.SelectboxColumn(col, options=["Strong Positive (++)", "Positive (+)", "No Correlation (0)", "Negative (-)", "Strong Negative (--)"], required=True)
        for col in hows_list
    }
    st.session_state.roof_matrix = st.data_editor(st.session_state.roof_matrix, use_container_width=True, column_config=roof_column_config, key="ed_roof")

# TAB 4 (Relationship Matrix)
with t4:
    st.subheader("Matriks Hubungan (WHATs vs HOWs)")
    st.caption("Pilih nilai hubungan: 9 (Kuat), 3 (Sedang), 1 (Lemah), atau 0 jika tidak berhubungan.")
    if 'rel_matrix' not in st.session_state or list(st.session_state.rel_matrix.columns) != hows_list or list(st.session_state.rel_matrix.index) != whats_list:
        st.session_state.rel_matrix = pd.DataFrame(0, index=whats_list, columns=hows_list)
    
    rel_column_config = {
        col: st.column_config.SelectboxColumn(col, options=[0, 1, 3, 9], required=True)
        for col in hows_list
    }
    st.session_state.rel_matrix = st.data_editor(st.session_state.rel_matrix, use_container_width=True, column_config=rel_column_config, key="ed_rel")

# --- TAB 5: THE FINAL HOUSE (WITH FULL MUTED ROOF MATRIX) ---
with t5:
    try:
        # Perhitungan Nilai Matematika Utama
        valid_whats = st.session_state.df_whats[st.session_state.df_whats["Customer Requirement (WHATs)"].isin(whats_list)]
        weights = valid_whats["Importance (1-5)"].values.astype(float)
        matrix_values = st.session_state.rel_matrix.loc[whats_list, hows_list].values.astype(float)
        
        abs_importance = weights @ matrix_values
        total = abs_importance.sum()
        rel_importance = (abs_importance / total * 100) if total > 0 else abs_importance * 0

        # DataFrame Hasil Akhir untuk Chart
        res_df = pd.DataFrame({
            "Requirement": hows_list,
            "Score": abs_importance,
            "Weight %": rel_importance.round(1)
        }).sort_values(by="Score", ascending=False)

        # -------------------------------------------------------------
        # 1. VISUALISASI MATRIKS ATAP (HOWs vs HOWs)
        # -------------------------------------------------------------
        st.write("### 🛖 Bagian Atap: Matriks Korelasi Antar Persyaratan Teknis")
        
        html_roof = '<table class="hoq-table">'
        # Header Atap dengan warna #1E3A8A & teks putih
        html_roof += '<tr>'
        html_roof += '<th class="hoq-th-corner" style="width: 30%; background-color: #f1f5f9; color: #475569;">Spesifikasi Teknis</th>'
        for col in hows_list:
            html_roof += f'<th class="hoq-th-hows">{col}</th>'
        html_roof += '</tr>'
        
        # Isi Matriks Atap
        for row_name in hows_list:
            html_roof += '<tr>'
            # Kolom pertama atap diperbaiki agar teksnya kontras dan terbaca terang
            html_roof += f'<td class="hoq-td-whats" style="background-color: #f8fafc; color: #334155;">{row_name}</td>'
            for col_name in hows_list:
                val = st.session_state.roof_matrix.at[row_name, col_name]
                
                simbol = "0"
                bg_cell = 'style="background-color: #ffffff; color: #94a3b8;"' # Default putih jika nilai 0
                
                if "Strong Positive" in val: 
                    simbol = "++"
                    bg_cell = 'style="background-color: #e0f2fe; color: #0369a1; font-weight: 600;"' 
                elif "Positive" in val: 
                    simbol = "+"
                    bg_cell = 'style="background-color: #f0fdf4; color: #15803d; font-weight: 600;"' 
                elif "Strong Negative" in val: 
                    simbol = "--"
                    bg_cell = 'style="background-color: #fef2f2; color: #b91c1c; font-weight: 600;"' 
                elif "Negative" in val: 
                    simbol = "-"
                    bg_cell = 'style="background-color: #fff7ed; color: #c2410c; font-weight: 600;"' 
                
                html_roof += f'<td {bg_cell}>{simbol}</td>'
            html_roof += '</tr>'
        html_roof += '</table>'
        st.markdown(html_roof, unsafe_allow_html=True)

        st.write("")

        # -------------------------------------------------------------
        # 2. VISUALISASI BADAN & FONDASI RUMAH HOQ
        # -------------------------------------------------------------
        st.write("### 🏢 Bagian Utama & Fondasi: Matriks Hubungan Terintegrasi")
        
        html_body = '<table class="hoq-table">'
        # Header Badan dengan warna #1E3A8A & teks putih
        html_body += '<tr>'
        html_body += '<th class="hoq-th-corner" style="width: 30%; background-color: #f1f5f9; color: #475569;">Customer Requirements (WHATs)</th>'
        html_body += '<th class="hoq-importance" style="width: 10%;">Importance</th>'
        for col in hows_list:
            html_body += f'<th class="hoq-th-hows">{col}</th>'
        html_body += '</tr>'
        
        # Isi Hubungan WHATs vs HOWs
        for idx, row_name in enumerate(whats_list):
            imp_val = weights[idx]
            html_body += '<tr>'
            html_body += f'<td class="hoq-td-whats">{row_name}</td>'
            html_body += f'<td class="hoq-importance">{int(imp_val)}</td>'
            for col_name in hows_list:
                score_val = st.session_state.rel_matrix.at[row_name, col_name]
                
                # Default putih jika nilai hubungan adalah 0
                bg_cell = 'style="background-color: #ffffff; color: #94a3b8;"'
                
                if score_val == 9: bg_cell = 'style="background-color: #ffe4e6; color: #9f1239; font-weight: 600;"' 
                elif score_val == 3: bg_cell = 'style="background-color: #ffedd5; color: #9a3412;"' 
                elif score_val == 1: bg_cell = 'style="background-color: #fef9c3; color: #854d0e;"' 
                
                html_body += f'<td {bg_cell}>{int(score_val)}</td>'
            html_body += '</tr>'
            
        # Fondasi: Absolute Importance
        html_body += '<tr class="hoq-score-row" style="background-color: #f8fafc;">'
        html_body += '<td style="text-align: right; color: #1E3A8A;">Absolute Importance (Score)</td>'
        html_body += '<td style="color: #1E3A8A;">-</td>'
        for score in abs_importance:
            html_body += f'<td style="color: #1E3A8A;">{int(score)}</td>'
        html_body += '</tr>'

        # Fondasi: Relative Weight %
        html_body += '<tr class="hoq-weight-row" style="background-color: #f8fafc;">'
        html_body += '<td style="text-align: right; color: #0f766e;">Relative Weight (%)</td>'
        html_body += '<td style="color: #0f766e;">-</td>'
        for weight in rel_importance:
            html_body += f'<td style="color: #0f766e;">{weight.round(1)}%</td>'
        html_body += '</tr>'
        html_body += '</table>'
        st.markdown(html_body, unsafe_allow_html=True)
        
        st.write("---")
        
        # -------------------------------------------------------------
        # 3. GRID GRAFIK PARETO & HIGHLIGHTS RADAR
        # -------------------------------------------------------------
        col_chart, col_rank = st.columns([1.5, 1])
        
        with col_chart:
            st.write("#### 📈 Grafik Kontribusi Prioritas Teknis")
            fig = px.bar(res_df, x="Score", y="Requirement", orientation='h', text="Weight %",
                         color="Score", color_continuous_scale="Blues")
            fig.update_layout(height=350, margin=dict(t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)
            
        with col_rank:
            st.write("#### 🏆 Urutan Rekomendasi Tindakan")
            for i, row in enumerate(res_df.itertuples()):
                medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🔹"
                st.info(f"{medal} **{row.Requirement}** — Skor: *{int(row.Score)}* ({row._3}%)")

    except Exception as e:
        st.error("Silakan lengkapi atau periksa kembali seluruh inputan di tab sebelumnya!")
