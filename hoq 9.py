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
        color: #ffffff !important; /* Memaksa teks default tetap putih cerah */
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
    
    /* Memaksa isi sel default berwarna latar hitam/gelap */
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
    
    /* Responsive Container untuk Full HOQ */
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

# Mapping teks kualitatif ke bobot numerik HOQ standar
LABEL_TO_WEIGHT = {
    "Tidak Ada Hubungan": 0,
    "Hubungan Lemah (1)": 1,
    "Hubungan Sedang (3)": 3,
    "Hubungan Kuat (9)": 9
}
WEIGHT_OPTIONS = list(LABEL_TO_WEIGHT.keys())

# --- TABS STRUKTUR ---
t1, t2, t3, t4, t5, t6 = st.tabs([
    "1. WHATs", "2. HOWs", "3. Correlation", "4. Matrix", "5. 🏆 FINAL HOUSE", "🏛️ 6. FULL HOQ ARCHITECTURE"
])

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

# TAB 4 (Relationship Matrix - IMPLEMENTASI PILIHAN B / USER-FRIENDLY DIALECTS)
with t4:
    st.subheader("🎯 Matriks Hubungan Intuitif (WHATs vs HOWs)")
    st.caption("Gunakan pilihan bahasa sehari-hari di bawah ini. Sistem otomatis melakukan pembobotan matematis (0, 1, 3, 9) di balik layar.")
    
    # Inisialisasi ulang matriks menggunakan Label Teks jika list berubah
    if 'rel_matrix_text' not in st.session_state or list(st.session_state.rel_matrix_text.columns) != hows_list or list(st.session_state.rel_matrix_text.index) != whats_list:
        st.session_state.rel_matrix_text = pd.DataFrame("Tidak Ada Hubungan", index=whats_list, columns=hows_list)
    
    rel_column_config = {
        col: st.column_config.SelectboxColumn(col, options=WEIGHT_OPTIONS, required=True)
        for col in hows_list
    }
    
    # User menginputkan pilihan kata, bukan angka kaku
    st.session_state.rel_matrix_text = st.data_editor(
        st.session_state.rel_matrix_text, 
        use_container_width=True, 
        column_config=rel_column_config, 
        key="ed_rel"
    )

    # Proses translasi instan dari Teks kualitatif menjadi matriks angka numerik untuk kalkulasi
    st.session_state.rel_matrix = st.session_state.rel_matrix_text.map(lambda x: LABEL_TO_WEIGHT.get(x, 0))


# --- TAB 5: THE FINAL HOUSE ---
with t5:
    try:
        # Perhitungan Nilai Matematika Utama berdasarkan hasil konversi otomatis Tab 4
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
        # 1. VISUALISASI MATRIKS ATAP (HOWs vs HOWs) - VERSI LAMA
        # -------------------------------------------------------------
        st.write("### 🛖 Bagian Atap: Matriks Korelasi Antar Persyaratan Teknis")
        
        html_roof = '<table class="hoq-table">'
        html_roof += '<tr>'
        html_roof += '<th class="hoq-th-corner" style="width: 30%;">Spesifikasi Teknis</th>'
        for col in hows_list:
            html_roof += f'<th class="hoq-th-hows">{col}</th>'
        html_roof += '</tr>'
        
        for row_name in hows_list:
            html_roof += '<tr>'
            html_roof += f'<td class="hoq-td-whats">{row_name}</td>'
            for col_name in hows_list:
                val = st.session_state.roof_matrix.at[row_name, col_name]
                
                simbol = "0"
                bg_cell = 'style="background-color: #0f172a; color: #64748b;"'
                
                if "Strong Positive" in val: 
                    simbol = "++"
                    bg_cell = 'style="background-color: #1e3a8a; color: #ffffff; font-weight: 600;"' 
                elif "Positive" in val: 
                    simbol = "+"
                    bg_cell = 'style="background-color: #14532d; color: #ffffff; font-weight: 600;"' 
                elif "Strong Negative" in val: 
                    simbol = "--"
                    bg_cell = 'style="background-color: #7f1d1d; color: #ffffff; font-weight: 600;"' 
                elif "Negative" in val: 
                    simbol = "-"
                    bg_cell = 'style="background-color: #7c2d12; color: #ffffff; font-weight: 600;"' 
                
                html_roof += f'<td {bg_cell}>{simbol}</td>'
            html_roof += '</tr>'
        html_roof += '</table>'
        st.markdown(html_roof, unsafe_allow_html=True)

        st.write("")

        # -------------------------------------------------------------
        # 2. VISUALISASI BADAN & FONDASI RUMAH HOQ - VERSI LAMA (ANGKA)
        # -------------------------------------------------------------
        st.write("### 🏢 Bagian Utama & Fondasi: Matriks Hubungan Terintegrasi")
        
        html_body = '<table class="hoq-table">'
        html_body += '<tr>'
        html_body += '<th class="hoq-th-corner" style="width: 30%;">Customer Requirements (WHATs)</th>'
        html_body += '<th class="hoq-importance-header" style="width: 10%;">Importance</th>'
        for col in hows_list:
            html_body += f'<th class="hoq-th-hows">{col}</th>'
        html_body += '</tr>'
        
        for idx, row_name in enumerate(whats_list):
            imp_val = weights[idx]
            html_body += '<tr>'
            html_body += f'<td class="hoq-td-whats">{row_name}</td>'
            html_body += f'<td class="hoq-importance">{int(imp_val)}</td>'
            for col_name in hows_list:
                score_val = st.session_state.rel_matrix.at[row_name, col_name]
                
                bg_cell = 'style="background-color: #0f172a; color: #64748b;"'
                
                if score_val == 9: bg_cell = 'style="background-color: #881337; color: #ffffff; font-weight: 600;"' 
                elif score_val == 3: bg_cell = 'style="background-color: #7c2d12; color: #ffffff; font-weight: 600;"' 
                elif score_val == 1: bg_cell = 'style="background-color: #713f12; color: #ffffff; font-weight: 600;"' 
                
                html_body += f'<td {bg_cell}>{int(score_val)}</td>'
            html_body += '</tr>'
            
        # Fondasi: Absolute Importance
        html_body += '<tr class="hoq-score-row">'
        html_body += '<td style="text-align: right; color: #38bdf8;">Weighted Importance (Score)</td>'
        html_body += '<td style="color: #38bdf8;">-</td>'
        for score in abs_importance:
            html_body += f'<td style="background-color: #1e293b; color: #38bdf8 !important;">{int(score)}</td>'
        html_body += '</tr>'

        # Fondasi: Relative Weight %
        html_body += '<tr class="hoq-weight-row">'
        html_body += '<td style="text-align: right; color: #2dd4bf;">Relative Importance (%)</td>'
        html_body += '<td style="color: #2dd4bf;">-</td>'
        for weight in rel_importance:
            html_body += f'<td style="background-color: #1e293b; color: #2dd4bf !important;">{weight.round(1)}%</td>'
        html_body += '</tr>'
        html_body += '</table>'
        st.markdown(html_body, unsafe_allow_html=True)
        
        st.write("---")
        
        # 3. GRID GRAFIK BAR
        col_chart, col_rank = st.columns([1.5, 1])
        with col_chart:
            st.write("#### 📈 Grafik Kontribusi Prioritas Teknis")
            fig = px.bar(res_df, x="Requirement", y="Score", text="Weight %",
                         color="Score", color_continuous_scale="Blues")
            fig.update_layout(height=400, margin=dict(t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)
            
        with col_rank:
            st.write("#### 🏆 Urutan Rekomendasi Tindakan")
            for i, row in enumerate(res_df.itertuples()):
                medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🔹"
                st.info(f"{medal} **{row.Requirement}** — Skor: *{int(row.Score)}* ({row._3}%)")

    except Exception as e:
        st.error("Silakan lengkapi atau periksa kembali seluruh inputan di tab sebelumnya!")


# --- 🏛️ TAB 6: FULL HOQ ARCHITECTURE ---
with t6:
    try:
        st.write("### 🏛️ Arsitektur Matriks House of Quality (HoQ) Komplit")
        st.caption("Visualisasi profesional mengintegrasikan Atap Korelasi Segitiga Piramida, Kriteria WHATs, serta Simbol Hubungan.")
        
        # Ambil kembali data perhitungan terkini
        valid_whats = st.session_state.df_whats[st.session_state.df_whats["Customer Requirement (WHATs)"].isin(whats_list)]
        weights = valid_whats["Importance (1-5)"].values.astype(float)
        matrix_values = st.session_state.rel_matrix.loc[whats_list, hows_list].values.astype(float)
        
        abs_importance = weights @ matrix_values
        total = abs_importance.sum()
        rel_importance = (abs_importance / total * 100) if total > 0 else abs_importance * 0
        
        n_hows = len(hows_list)
        
        # Box Keterangan Simbol (Legend)
        st.markdown("""
        <div class="legend-box">
            <strong>ℹ️ Keterangan Simbol Hubungan Matriks (Badan Utama):</strong><br>
            <span style="color: #38bdf8;"><strong>◎</strong> Hubungan Kuat (Skor 9)</span> &nbsp;|&nbsp; 
            <span style="color: #4ade80;"><strong>○</strong> Hubungan Sedang (Skor 3)</span> &nbsp;|&nbsp; 
            <span style="color: #fef08a;"><strong>△</strong> Hubungan Lemah (Skor 1)</span> &nbsp;|&nbsp; 
            <span style="color: #64748b;">Tanpa Simbol = Tidak Berhubungan (Skor 0)</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Proteksi responsive overflow agar tabel tidak patah
        html_hoq = '<div class="hoq-scroll-container">'
        html_hoq += '<table class="hoq-table" style="width:auto; margin:auto;">'
        
        # -------------------------------------------------------------
        # 1. GENERATE ATAP SEGITIGA (Roof Matrix Upper Triangle)
        # -------------------------------------------------------------
        for i in range(n_hows - 1):
            html_hoq += '<tr>'
            html_hoq += '<td class="roof-blank" style="width:250px;"></td>'
            html_hoq += '<td class="roof-blank" style="width:80px;"></td>'
            
            for j in range(n_hows):
                if j < (n_hows - 1 - i):
                    html_hoq += '<td class="roof-blank"></td>'
                else:
                    row_target = hows_list[j]
                    col_target = hows_list[n_hows - 1 - i]
                    val = st.session_state.roof_matrix.at[row_target, col_target]
                    
                    simbol = ""
                    bg_color = "#1e293b"
                    text_color = "#64748b"
                    
                    if "Strong Positive" in val: simbol, bg_color, text_color = "++", "#1e3a8a", "#38bdf8"
                    elif "Positive" in val: simbol, bg_color, text_color = "+", "#14532d", "#4ade80"
                    elif "Strong Negative" in val: simbol, bg_color, text_color = "--", "#7f1d1d", "#f87171"
                    elif "Negative" in val: simbol, bg_color, text_color = "-", "#7c2d12", "#fb923c"
                    elif "No Correlation" in val: simbol, bg_color, text_color = "0", "#0f172a", "#475569"
                    
                    html_hoq += f'<td class="roof-cell" style="background-color: {bg_color}; color: {text_color} !important;">{simbol}</td>'
            html_hoq += '</tr>'

        # Garis pembatas antara atap dan kepala tabel utama
        html_hoq += '<tr><td colspan="{}" style="background-color:#334155; padding:2px; border:none;"></td></tr>'.format(n_hows + 2)

        # -------------------------------------------------------------
        # 2. GENERATE KEPALA TABEL BADAN UTAMA
        # -------------------------------------------------------------
        html_hoq += '<tr>'
        html_hoq += '<th class="hoq-th-corner">Customer Requirements (WHATs)</th>'
        html_hoq += '<th class="hoq-importance-header">Importance</th>'
        for col in hows_list:
            html_hoq += f'<th class="hoq-th-hows">{col}</th>'
        html_hoq += '</tr>'
        
        # -------------------------------------------------------------
        # 3. GENERATE BADAN MATRIKS UTAMA (MENGGUNAKAN SIMBOL ◎, ○, △)
        # -------------------------------------------------------------
        for idx, row_name in enumerate(whats_list):
            imp_val = weights[idx]
            html_hoq += '<tr>'
            html_hoq += f'<td class="hoq-td-whats">{row_name}</td>'
            html_hoq += f'<td class="hoq-importance">{int(imp_val)}</td>'
            for col_name in hows_list:
                score_val = st.session_state.rel_matrix.at[row_name, col_name]
                
                bg_cell = 'style="background-color: #0f172a; color: #64748b;"'
                simbol_hub = ""
                
                if score_val == 9: 
                    simbol_hub = "◎"
                    bg_cell = 'style="background-color: #1e3a8a; color: #38bdf8; font-size: 18px; font-weight: bold;"' 
                elif score_val == 3: 
                    simbol_hub = "○"
                    bg_cell = 'style="background-color: #1e293b; color: #4ade80; font-size: 18px; font-weight: bold;"' 
                elif score_val == 1: 
                    simbol_hub = "△"
                    bg_cell = 'style="background-color: #1e293b; color: #fef08a; font-size: 18px; font-weight: bold;"' 
                
                html_hoq += f'<td {bg_cell}>{simbol_hub}</td>'
            html_hoq += '</tr>'
            
        # -------------------------------------------------------------
        # 4. GENERATE FONDASI RUMAH HOQ (MUTED SCORE & WEIGHTS)
        # -------------------------------------------------------------
        html_hoq += '<tr class="hoq-score-row">'
        html_hoq += '<td style="text-align: right; color: #38bdf8;">Weighted Importance (Score)</td>'
        html_hoq += '<td style="color: #38bdf8;">-</td>'
        for score in abs_importance:
            html_hoq += f'<td style="background-color: #1e293b; color: #38bdf8 !important;">{int(score)}</td>'
        html_hoq += '</tr>'

        html_hoq += '<tr class="hoq-weight-row">'
        html_hoq += '<td style="text-align: right; color: #2dd4bf;">Relative Importance (%)</td>'
        html_hoq += '<td style="color: #2dd4bf;">-</td>'
        for weight in rel_importance:
            html_hoq += f'<td style="background-color: #1e293b; color: #2dd4bf !important;">{weight.round(1)}%</td>'
        html_hoq += '</tr>'
        
        html_hoq += '</table>'
        html_hoq += '</div>'
        
        st.markdown(html_hoq, unsafe_allow_html=True)
        
    except Exception as e:
        st.error("Silakan pastikan semua data pada input Tab 1 sampai 4 diisi dengan benar.")