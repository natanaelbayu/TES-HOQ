import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SETTING HALAMAN & STYLE HOQ RUMAH
st.set_page_config(page_title="Digital HoQ - UKM Tahu", layout="wide")

st.markdown("""
    <style>
    .main-header { font-size: 28px; font-weight: bold; color: #1E3A8A; margin-bottom: 10px; }
    .sub-header { font-size: 18px; color: #64748b; margin-bottom: 20px; }
    
    /* Style Tabel Rumah HoQ Modern & Muted Colors */
    .hoq-table {
        border-collapse: collapse;
        margin: 20px 0;
        font-family: sans-serif;
        width: 100%;
        border-radius: 8px;
        overflow: hidden;
    }
    .hoq-table th, .hoq-table td {
        border: 1px solid #e2e8f0;
        padding: 12px;
        text-align: center;
        font-size: 14px;
        color: #334155;
    }
    .hoq-th-corner {
        background-color: #f8fafc;
        font-weight: 600;
        color: #475569;
    }
    .hoq-th-hows {
        background-color: #f1f5f9;
        color: #1e3a8a;
        font-weight: 600;
    }
    .hoq-td-whats {
        background-color: #f8fafc;
        text-align: left !important;
        font-weight: 600;
        color: #334155;
    }
    .hoq-importance {
        background-color: #fafaf9;
        font-weight: 600;
        color: #475569;
    }
    .hoq-score-row {
        background-color: #f8fafc;
        font-weight: bold;
        color: #1e3a8a;
        border-top: 2px solid #cbd5e1;
    }
    .hoq-weight-row {
        background-color: #f8fafc;
        font-weight: bold;
        color: #0f766e;
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
    if 'rel_matrix' not in st.session_state or list(st.session_state.rel_matrix.columns) != hows_list or list(st.session_state.rel_matrix.index) != whats_list:
        st.session_state.rel_matrix = pd.DataFrame(0, index=whats_list, columns=hows_list)
    
    rel_column_config = {
        col: st.column_config.SelectboxColumn(col, options=[0, 1, 3, 9], required=True)
        for col in hows_list
    }
    st.session_state.rel_matrix = st.data_editor(st.session_state.rel_matrix, use_container_width=True, column_config=rel_column_config, key="ed_rel")

# --- TAB 5: THE FINAL HOUSE (BENTO COMPACT HOUSE WITH MUTED ROOF) ---
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

        st.write("### 📊 Kompleks Kisi-Kisi Matriks HoQ Terintegrasi")
        
        html_code = '<table class="hoq-table">'
        
# --- LAYOUT RUMAH ---
        
        # 1. ATAP (Correlation)
        st.info("🛖 **Bagian Atap:** Korelasi Antar Persyaratan Teknis (Trade-offs)")
        st.dataframe(roof_data, use_container_width=True)

        st.write("")
        
        # 2. HEADER BADAN RUMAH
        html_code += '<tr>'
        html_code += '<th class="hoq-th-corner" style="width: 30%;">Customer Requirements (WHATs)</th>'
        html_code += '<th class="hoq-importance" style="width: 10%;">Importance</th>'
        for col in hows_list:
            html_code += f'<th class="hoq-th-hows">{col}</th>'
        html_code += '</tr>'
        
        # 3. ISIAN BADAN RUMAH (Soft Heatmap Pastel)
        for idx, row_name in enumerate(whats_list):
            imp_val = weights[idx]
            html_code += '<tr>'
            html_code += f'<td class="hoq-td-whats">{row_name}</td>'
            html_code += f'<td class="hoq-importance">{int(imp_val)}</td>'
            for col_name in hows_list:
                score_val = st.session_state.rel_matrix.at[row_name, col_name]
                bg_cell = ""
                # Menggunakan warna pastel yang pudar (sangat tidak kontras)
                if score_val == 9: bg_cell = 'style="background-color: #ffe4e6; color: #9f1239; font-weight: 600;"' # Soft Rose (Kuat)
                elif score_val == 3: bg_cell = 'style="background-color: #ffedd5; color: #9a3412;"' # Soft Orange (Sedang)
                elif score_val == 1: bg_cell = 'style="background-color: #fef9c3; color: #854d0e;"' # Soft Yellow (Lemah)
                
                html_code += f'<td {bg_cell}>{int(score_val)}</td>'
            html_code += '</tr>'
            
        # 4. FONDASI RUMAH: Absolute Importance
        html_code += '<tr class="hoq-score-row">'
        html_code += '<td style="text-align: right;">Absolute Importance (Score)</td>'
        html_code += '<td>-</td>'
        for score in abs_importance:
            html_code += f'<td>{int(score)}</td>'
        html_code += '</tr>'

        # 5. FONDASI RUMAH: Relative Weight %
        html_code += '<tr class="hoq-weight-row">'
        html_code += '<td style="text-align: right;">Relative Weight (%)</td>'
        html_code += '<td>-</td>'
        for weight in rel_importance:
            html_code += f'<td>{weight.round(1)}%</td>'
        html_code += '</tr>'
        
        html_code += '</table>'
        st.markdown(html_code, unsafe_allow_html=True)
        
        st.write("---")
        
        # TAMPILAN 2: GRID GRAFIK PARETO & HIGHLIGHTS
        col_chart, col_rank = st.columns([1.5, 1])
        
        with col_chart:
            st.write("#### 📈 Grafik Kontribusi Prioritas Teknis")
            # Mengubah tema grafik ke 'Muted Blue/Teal' (Muted warna bar)
            fig = px.bar(res_df, x="Score", y="Requirement", orientation='h', text="Weight %",
                         color="Score", color_continuous_scale="Blues")
            fig.update_layout(height=350, margin=dict(t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)
            
        with col_rank:
            st.write("#### 🎯 Urutan Rekomendasi Tindakan")
            for i, row in enumerate(res_df.itertuples()):
                medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🔹"
                st.info(f"{medal} **{row.Requirement}** — Skor: *{int(row.Score)}* ({row._3}%)")

    except Exception as e:
        st.error("Silakan lengkapi atau periksa kembali seluruh inputan di tab sebelumnya!")