import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SETTING HALAMAN & STYLE HOQ RUMAH (LIGHT MODE & COLORFUL)
st.set_page_config(page_title="Digital HoQ - UKM Tahu", layout="wide")

st.markdown("""
    <style>
    /* Mengubah background aplikasi menjadi cerah */
    .stApp {
        background-color: #f8fafc;
    }
    
    .main-header { font-size: 28px; font-weight: bold; color: #1e3a8a; margin-bottom: 5px; }
    .sub-header { font-size: 16px; color: #475569; margin-bottom: 20px; }
    
    /* Style Tabel Rumah HoQ untuk Tema Terang & Colorful */
    .hoq-table {
        border-collapse: collapse;
        margin: 20px 0;
        font-family: sans-serif;
        width: 100%;
        border-radius: 8px;
        overflow: hidden;
        background-color: #ffffff;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .hoq-table th, .hoq-table td {
        border: 1px solid #cbd5e1;
        padding: 12px;
        text-align: center;
        font-size: 14px;
        color: #334155;
    }
    .hoq-th-corner {
        background-color: #f1f5f9 !important;
        font-weight: 600;
        color: #1e3a8a !important;
    }
    .hoq-th-hows {
        background-color: #eff6ff !important; 
        color: #1e40af !important;  
        font-weight: 600;
    }
    .hoq-importance-header {
        background-color: #fef3c7 !important;
        color: #92400e !important;
        font-weight: 600;
    }
    .hoq-td-whats {
        background-color: #ffffff !important;
        text-align: left !important;
        font-weight: 600;
        color: #334155 !important;
    }
    .hoq-importance {
        background-color: #fffbeb !important;
        font-weight: 600;
        color: #b45309 !important;
    }
    .hoq-score-row {
        background-color: #f0fdf4;
        font-weight: bold;
        color: #166534 !important;
        border-top: 2px solid #bbf7d0;
    }
    .hoq-weight-row {
        background-color: #faf5ff;
        font-weight: bold;
        color: #6b21a8 !important;
    }
    
    /* Style Khusus untuk Atap Segitiga Segitiga di Tab 6 */
    .roof-blank {
        background-color: transparent !important;
        border: none !important;
    }
    .roof-cell {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1 !important;
        font-weight: bold;
    }
    
    /* Legend Info Box */
    .legend-box {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-bottom: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
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

# 3. SIDEBAR CONFIGURATION (Pusat Input Data)
with st.sidebar:
    st.header("📋 Input Parameter HoQ")
    st.markdown("Silakan atur data kebutuhan konsumen dan spesifikasi teknis di bawah ini:")
    
    st.subheader("1. Kebutuhan Konsumen (WHATs)")
    st.session_state.df_whats = st.data_editor(
        st.session_state.df_whats, 
        num_rows="dynamic", 
        use_container_width=True, 
        column_config={
            "Importance (1-5)": st.column_config.NumberColumn("Importance (1-5)", min_value=1, max_value=5, step=1)
        },
        key="sb_whats"
    )
    
    st.write("---")
    
    st.subheader("2. Spesifikasi Teknis (HOWs)")
    st.session_state.df_hows = st.data_editor(
        st.session_state.df_hows, 
        num_rows="dynamic", 
        use_container_width=True, 
        column_config={
            "Direction": st.column_config.SelectboxColumn("Direction", options=["Max", "Min", "Target"], required=True)
        },
        key="sb_hows"
    )

# Filter list dinamis dari apa yang diinput user di sidebar
whats_list = [x for x in st.session_state.df_whats["Customer Requirement (WHATs)"].tolist() if pd.notna(x) and x != ""]
hows_list = [x for x in st.session_state.df_hows["Technical Requirement (HOWs)"].tolist() if pd.notna(x) and x != ""]

# 4. TABS STRUKTUR UTAMA (Area Kerja & Hasil)
t1, t2, t3, t4 = st.tabs([
    "🤝 Matriks Hubungan (WHATs vs HOWs)", "🛖 Matriks Korelasi Atap", "🏆 Final Kesimpulan & Analisis", "🏛️ Arsitektur Full HOQ"
])

# TAB 1: Relationship Matrix
with t1:
    st.subheader("♾️ Hubungan Kebutuhan Konsumen vs Spesifikasi Teknis")
    st.info("""
    💡 **Panduan Pengisian:**
    Tentukan seberapa besar pengaruh **'Spesifikasi Teknis'** dalam memenuhi **'Kebutuhan Konsumen'** Anda:
    - **9 (Kuat):** Spesifikasi ini adalah kunci utama agar kebutuhan konsumen tersebut terpenuhi.
    - **3 (Sedang):** Berpengaruh secara tidak langsung.
    - **1 (Lemah):** Memiliki pengaruh yang sangat kecil.
    - **0:** Tidak berkaitan sama sekali.
    """)
    
    if 'rel_matrix' not in st.session_state or list(st.session_state.rel_matrix.columns) != hows_list or list(st.session_state.rel_matrix.index) != whats_list:
        st.session_state.rel_matrix = pd.DataFrame(0, index=whats_list, columns=hows_list)
    
    rel_column_config = {
        col: st.column_config.SelectboxColumn(col, options=[0, 1, 3, 9], required=True)
        for col in hows_list
    }
    st.session_state.rel_matrix = st.data_editor(st.session_state.rel_matrix, use_container_width=True, column_config=rel_column_config, key="ed_rel")

# TAB 2: Correlation (The Roof)
with t2:
    st.subheader("📐 Matriks Korelasi Atap (HOWs vs HOWs)")
    st.caption("Pilih nilai korelasi atau hubungan timbal balik antar sesama spesifikasi teknis produksi.")
    
    if 'roof_matrix' not in st.session_state or list(st.session_state.roof_matrix.columns) != hows_list:
        st.session_state.roof_matrix = pd.DataFrame("No Correlation (0)", index=hows_list, columns=hows_list)
    
    roof_column_config = {
        col: st.column_config.SelectboxColumn(col, options=["Strong Positive (++)", "Positive (+)", "No Correlation (0)", "Negative (-)", "Strong Negative (--)"], required=True)
        for col in hows_list
    }
    st.session_state.roof_matrix = st.data_editor(st.session_state.roof_matrix, use_container_width=True, column_config=roof_column_config, key="ed_roof")

# Hitung Matematika Utama untuk dipakai di Tab Kesimpulan dan Full Architecture
try:
    valid_whats = st.session_state.df_whats[st.session_state.df_whats["Customer Requirement (WHATs)"].isin(whats_list)]
    weights = valid_whats["Importance (1-5)"].values.astype(float)
    matrix_values = st.session_state.rel_matrix.loc[whats_list, hows_list].values.astype(float)
    
    abs_importance = weights @ matrix_values
    total = abs_importance.sum()
    rel_importance = (abs_importance / total * 100) if total > 0 else abs_importance * 0

    res_df = pd.DataFrame({
        "Requirement": hows_list,
        "Score": abs_importance,
        "Weight %": rel_importance.round(1)
    }).sort_values(by="Score", ascending=False)
except:
    res_df = pd.DataFrame()

# TAB 3: THE FINAL HOUSE & ACTION PLAN
with t3:
    if not res_df.empty and len(res_df) > 0:
        st.write("### 💡 Kesimpulan Strategis & Arah Pengembangan")
        
        top_priorities = res_df.head(3)
        priority_names = top_priorities["Requirement"].tolist()
        priority_weights = top_priorities["Weight %"].tolist()
        
        col_rec, col_summary = st.columns([1.2, 1])
        
        with col_rec:
            st.success(f"✍️ **Rekomendasi Utama Bisnis:**")
            st.write(f"""
            Fokuskan biaya dan resource teknis tim Anda saat ini pada pengembangan parameter: **{priority_names[0]}**.
            Spesifikasi ini memegang kontribusi terbesar, yaitu sebesar **{priority_weights[0]}%** dari total seluruh ekspektasi pelanggan.
            """)
            
        with col_summary:
            st.warning("⚠️ **Urutan Rencana Aksi (Action Plan):**")
            st.write(f"1. **Prioritas Utama:** Optimalisasi penuh pada `{priority_names[0]}`.")
            if len(priority_names) > 1:
                st.write(f"2. **Prioritas Sekunder:** Jaga stabilitas kualitas `{priority_names[1]}`.")
            if len(priority_names) > 2:
                st.write(f"3. **Prioritas Tersier:** Pertahankan pengawasan pada `{priority_names[2]}`.")

        st.write("---")

        # Visualisasi Chart Berwarna Cerah
        col_chart, col_rank = st.columns([1.5, 1])
        with col_chart:
            st.write("#### 📈 Grafik Kontribusi Prioritas Teknis")
            fig = px.bar(res_df, x="Requirement", y="Score", text="Weight %",
                         color="Score", color_continuous_scale="Turbo") # Menggunakan skala Turbo agar penuh warna
            fig.update_layout(height=400, margin=dict(t=10, b=10), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            
        with col_rank:
            st.write("#### 🏆 Urutan Rekomendasi Tindakan")
            for i, row in enumerate(res_df.itertuples()):
                if i == 0:
                    st.toast(f"Prioritas Utama: {row.Requirement}")
                    st.error(f"🥇 **PRIORITAS UTAMA**\n\n**{row.Requirement}** — Skor: *{int(row.Score)}* ({row._3}%)")
                elif i == 1:
                    st.warning(f"🥈 **KEDUA**\n\n**{row.Requirement}** — Skor: *{int(row.Score)}* ({row._3}%)")
                elif i == 2:
                    st.success(f"🥉 **KETIGA**\n\n**{row.Requirement}** — Skor: *{int(row.Score)}* ({row._3}%)")
                else:
                    st.info(f"🔹 **PENDUKUNG**\n\n**{row.Requirement}** — Skor: *{int(row.Score)}* ({row._3}%)")
    else:
        st.error("Silakan lengkapi atau periksa kembali seluruh inputan di sidebar!")

# TAB 4: FULL HOQ ARCHITECTURE
with t4:
    try:
        st.write("### 🏛️ Arsitektur Matriks House of Quality (HoQ) Komplit")
        
        n_hows = len(hows_list)
        
        # Legend Box Berwarna-warni
        st.markdown("""
        <div class="legend-box">
            <strong>ℹ️ Keterangan Hubungan (Badan Utama):</strong><br>
            <span style="color: #ef4444; font-size:16px;"><strong>◎</strong> Kuat (9)</span> &nbsp;|&nbsp; 
            <span style="color: #f59e0b; font-size:16px;"><strong>○</strong> Sedang (3)</span> &nbsp;|&nbsp; 
            <span style="color: #10b981; font-size:16px;"><strong>△</strong> Lemah (1)</span>
            <br><br>
            <strong>ℹ️ Keterangan Korelasi Atap:</strong><br>
            <span style="background-color: #dbeafe; color: #1e40af; padding: 2px 6px; border-radius:4px;">++ Strong Positive</span>
            <span style="background-color: #dcfce7; color: #166534; padding: 2px 6px; border-radius:4px;">+ Positive</span>
            <span style="background-color: #fee2e2; color: #991b1b; padding: 2px 6px; border-radius:4px;">-- Strong Negative</span>
            <span style="background-color: #ffedd5; color: #9a3412; padding: 2px 6px; border-radius:4px;">- Negative</span>
        </div>
        """, unsafe_allow_html=True)
        
        html_hoq = '<div class="hoq-scroll-container">'
        html_hoq += '<table class="hoq-table" style="width:auto; margin:auto;">'
        
        # 1. GENERATE ATAP SEGITIGA COLORFUL
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
                    
                    simbol = "0"
                    bg_color = "#f8fafc"
                    text_color = "#94a3b8"
                    
                    if "Strong Positive" in val: simbol, bg_color, text_color = "++", "#dbeafe", "#1e40af"
                    elif "Positive" in val: simbol, bg_color, text_color = "+", "#dcfce7", "#166534"
                    elif "Strong Negative" in val: simbol, bg_color, text_color = "--", "#fee2e2", "#991b1b"
                    elif "Negative" in val: simbol, bg_color, text_color = "-", "#ffedd5", "#9a3412"
                    
                    html_hoq += f'<td class="roof-cell" style="background-color: {bg_color}; color: {text_color} !important;">{simbol}</td>'
            html_hoq += '</tr>'

        # Garis pembatas atap
        html_hoq += '<tr><td colspan="{}" style="background-color:#cbd5e1; padding:2px; border:none;"></td></tr>'.format(n_hows + 2)

        # 2. GENERATE KEPALA TABEL MAIN MATRIKS
        html_hoq += '<tr>'
        html_hoq += '<th class="hoq-th-corner">Customer Requirements (WHATs)</th>'
        html_hoq += '<th class="hoq-importance-header">Importance</th>'
        for col in hows_list:
            html_hoq += f'<th class="hoq-th-hows">{col}</th>'
        html_hoq += '</tr>'
        
        # 3. GENERATE BADAN MATRIKS UTAMA DENGAN SIMBOL WARNA CERAH
        for idx, row_name in enumerate(whats_list):
            imp_val = weights[idx]
            html_hoq += '<tr>'
            html_hoq += f'<td class="hoq-td-whats">{row_name}</td>'
            html_hoq += f'<td class="hoq-importance">{int(imp_val)}</td>'
            for col_name in hows_list:
                score_val = st.session_state.rel_matrix.at[row_name, col_name]
                
                bg_cell = 'style="background-color: #ffffff; color: #cbd5e1;"'
                simbol_hub = ""
                
                if score_val == 9: 
                    simbol_hub = "◎"
                    bg_cell = 'style="background-color: #fef2f2; color: #ef4444; font-size: 18px; font-weight: bold;"' 
                elif score_val == 3: 
                    simbol_hub = "○"
                    bg_cell = 'style="background-color: #fffbeb; color: #f59e0b; font-size: 18px; font-weight: bold;"' 
                elif score_val == 1: 
                    simbol_hub = "△"
                    bg_cell = 'style="background-color: #ecfdf5; color: #10b981; font-size: 18px; font-weight: bold;"' 
                
                html_hoq += f'<td {bg_cell}>{simbol_hub}</td>'
            html_hoq += '</tr>'
            
        # 4. GENERATE FONDASI RUMAH HOQ (HIJAU DAN UNGU CERAH)
        # Baris Absolute Importance (Score)
        html_hoq += '<tr class="hoq-score-row">'
        html_hoq += '<td style="text-align: right; font-weight: bold;">Weighted Importance (Score)</td>'
        html_hoq += '<td>-</td>'
        for score in abs_importance:
            html_hoq += f'<td style="background-color: #f0fdf4; color: #166534 !important; font-weight: bold;">{int(score)}</td>'
        html_hoq += '</tr>'

        # Baris Relative Weight (%)
        html_hoq += '<tr class="hoq-weight-row">'
        html_hoq += '<td style="text-align: right; font-weight: bold;">Relative Importance (%)</td>'
        html_hoq += '<td>-</td>'
        for weight in rel_importance:
            html_hoq += f'<td style="background-color: #faf5ff; color: #6b21a8 !important; font-weight: bold;">{weight.round(1)}%</td>'
        html_hoq += '</tr>'
        
        html_hoq += '</table>'
        html_hoq += '</div>'
        
        st.markdown(html_hoq, unsafe_allow_html=True)
        
    except Exception as e:
        st.error("Pastikan semua parameter pada data input di sidebar diisi dengan benar.")