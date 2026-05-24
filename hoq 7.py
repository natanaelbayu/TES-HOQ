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
    
    roof_column_config = {col: st.column_config.SelectboxColumn(col, options=["Strong Positive (++)", "Positive (+)", "No Correlation (0)", "Negative (-)", "Strong Negative (--)"], required=True) for col in hows_list}
    st.session_state.roof_matrix = st.data_editor(st.session_state.roof_matrix, use_container_width=True, column_config=roof_column_config, key="ed_roof")

# TAB 4 (Relationship Matrix)
with t4:
    st.subheader("Matriks Hubungan (WHATs vs HOWs)")
    if 'rel_matrix' not in st.session_state or list(st.session_state.rel_matrix.columns) != hows_list or list(st.session_state.rel_matrix.index) != whats_list:
        st.session_state.rel_matrix = pd.DataFrame(0, index=whats_list, columns=hows_list)
    
    rel_column_config = {col: st.column_config.SelectboxColumn(col, options=[0, 1, 3, 9], required=True) for col in hows_list}
    st.session_state.rel_matrix = st.data_editor(st.session_state.rel_matrix, use_container_width=True, column_config=rel_column_config, key="ed_rel")

# TAB 5: THE FINAL HOUSE (Sesuai kode kamu sebelumnya)
with t5:
    try:
        valid_whats = st.session_state.df_whats[st.session_state.df_whats["Customer Requirement (WHATs)"].isin(whats_list)]
        weights = valid_whats["Importance (1-5)"].values.astype(float)
        matrix_values = st.session_state.rel_matrix.loc[whats_list, hows_list].values.astype(float)
        abs_importance = weights @ matrix_values
        total = abs_importance.sum()
        rel_importance = (abs_importance / total * 100) if total > 0 else abs_importance * 0

        res_df = pd.DataFrame({"Requirement": hows_list, "Score": abs_importance, "Weight %": rel_importance.round(1)}).sort_values(by="Score", ascending=False)

        st.markdown('<div class="legend-box"><strong>ℹ️ Info Tab 5:</strong> Menampilkan tabel riwayat matriks dasar. Buka <strong>Tab 6</strong> untuk melihat arsitektur atap segitiga QFD utuh.</div>', unsafe_allow_html=True)
        
        # Grafik Bar Vertikal Berdiri
        col_chart, col_rank = st.columns([1.5, 1])
        with col_chart:
            st.write("#### 📈 Grafik Kontribusi Prioritas Teknis")
            fig = px.bar(res_df, x="Requirement", y="Score", text="Weight %", color="Score", color_continuous_scale="Blues")
            fig.update_layout(height=400, margin=dict(t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)
        with col_rank:
            st.write("#### 🏆 Urutan Rekomendasi Tindakan")
            for i, row in enumerate(res_df.itertuples()):
                medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🔹"
                st.info(f"{medal} **{row.Requirement}** — Skor: *{int(row.Score)}* ({row._3}%)")
    except Exception as e:
        st.error("Lengkapi data terlebih dahulu!")

# --- TAB baru: TAB 6 (ARSITEKTUR UTUH DENGAN ATAP SEGITIGA BERGAYA QFD) ---
with t6:
    try:
        st.write("### 🏛️ Matriks House of Quality (HoQ) Komplit")
        st.caption("Visualisasi komprehensif mengintegrasikan Atap Korelasi Segitiga, Kriteria WHATs, dan Fondasi Bobot.")
        
        # Ambil kembali kalkulasi data terkini
        valid_whats = st.session_state.df_whats[st.session_state.df_whats["Customer Requirement (WHATs)"].isin(whats_list)]
        weights = valid_whats["Importance (1-5)"].values.astype(float)
        matrix_values = st.session_state.rel_matrix.loc[whats_list, hows_list].values.astype(float)
        abs_importance = weights @ matrix_values
        total = abs_importance.sum()
        rel_importance = (abs_importance / total * 100) if total > 0 else abs_importance * 0
        
        n_hows = len(hows_list)
        
        # Mulai Generate Tabel HTML Gabungan Besar
        html_hoq = '<table class="hoq-table" style="width:auto; margin:auto;">'
        
        # ==========================================
        # BAGIAN A: RENDER ATAP SEGITIGA (Roof Matrix)
        # ==========================================
        for i in range(n_hows - 1):
            html_hoq += '<tr>'
            # Spacing kolom WHATs & Importance di kiri dibuat kosong (transparan)
            html_hoq += '<td class="roof-blank" style="width:250px;"></td>'
            html_hoq += '<td class="roof-blank" style="width:80px;"></td>'
            
            for j in range(n_hows):
                # Membuat bentuk atap piramida/segitiga naik-turun menggunakan relasi indeks
                if j < (n_hows - 1 - i):
                    html_hoq += '<td class="roof-blank"></td>'
                else:
                    row_target = hows_list[j]
                    col_target = hows_list[n_hows - 1 - i]
                    val = st.session_state.roof_matrix.at[row_target, col_target]
                    
                    # Mapping simbol korelasi atap
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

        # Separator Atap ke Kepala Tabel Utama
        html_hoq += '<tr><td colspan="{}" style="background-color:#334155; padding:2px; border:none;"></td></tr>'.format(n_hows + 2)

        # ==========================================
        # BAGIAN B: KEPALA TABEL BADAN UTAMA (Headers)
        # ==========================================
        html_hoq += '<tr>'
        html_hoq += '<th class="hoq-th-corner">Customer Requirements (WHATs)</th>'
        html_hoq += '<th class="hoq-importance-header">Importance</th>'
        for col in hows_list:
            html_hoq += f'<th class="hoq-th-hows">{col}</th>'
        html_hoq += '</tr>'
        
        # ==========================================
        # BAGIAN C: BADAN MATRIKS (Simbol ◎, ○, △)
        # ==========================================
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
            
        # ==========================================
        # BAGIAN D: FONDASI RUMAH (Scores & Weights)
        # ==========================================
        # Baris Skor Absolute
        html_hoq += '<tr class="hoq-score-row">'
        html_hoq += '<td style="text-align: right; color: #38bdf8;">Absolute Importance (Score)</td>'
        html_hoq += '<td style="color: #38bdf8;">-</td>'
        for score in abs_importance:
            html_hoq += f'<td style="background-color: #1e293b; color: #38bdf8 !important;">{int(score)}</td>'
        html_hoq += '</tr>'

        # Baris Bobot Relatif
        html_hoq += '<tr class="hoq-weight-row">'
        html_hoq += '<td style="text-align: right; color: #2dd4bf;">Relative Weight (%)</td>'
        html_hoq += '<td style="color: #2dd4bf;">-</td>'
        for weight in rel_importance:
            html_hoq += f'<td style="background-color: #1e293b; color: #2dd4bf !important;">{weight.round(1)}%</td>'
        html_hoq += '</tr>'
        
        html_hoq += '</table>'
        
        # Render Desain Rumah Akhir Ke Halaman Screen
        st.markdown(html_hoq, unsafe_allow_html=True)
        
    except Exception as e:
        st.error("Silakan pastikan semua data pada input Tab 1 sampai 4 diisi dengan benar.")
