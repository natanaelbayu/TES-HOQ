import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SETTING HALAMAN & STYLE HOQ RUMAH (LIGHT & COLORFUL THEME)
st.set_page_config(page_title="Digital HoQ - UKM Tahu", layout="wide")

st.markdown("""
    <style>
    /* Mengubah background aplikasi menjadi putih cerah */
    .stApp {
        background-color: #ffffff;
    }

    /* Judul Utama dengan warna Biru Indigo Cerah */
    .main-header { 
        font-size: 32px; 
        font-weight: bold; 
        color: #4f46e5; 
        margin-bottom: 10px; 
    }
    
    /* Sub-judul dengan warna Abu-abu Medium */
    .sub-header { 
        font-size: 18px; 
        color: #6b7280; 
        margin-bottom: 25px; 
    }
    
    /* === Style Tabel Rumah HoQ untuk Tema Terang & Full Color === */
    .hoq-table {
        border-collapse: collapse;
        margin: 20px 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        width: 100%;
        border-radius: 12px;
        overflow: hidden;
        /* Menambahkan shadow agar tabel terlihat mengambang */
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        background-color: #ffffff;
        border: none;
    }
    
    /* Mengatur border dan padding dasar untuk semua sel */
    .hoq-table th, .hoq-table td {
        border: 1px solid #e5e7eb;
        padding: 14px;
        text-align: center;
        font-size: 14px;
        color: #1f2937 !important; /* Warna teks default gelap agar terbaca jelas */
    }

    /* === Warna Kepala Tabel (Headers) === */
    /* Pojok kiri atas (Ungu Pastel) */
    .hoq-th-corner {
        background-color: #ede9fe !important;
        font-weight: 700;
        color: #4c1d95 !important;
    }
    /* Header spesifikasi teknis / HOWs (Pink Pastel) */
    .hoq-th-hows {
        background-color: #fce7f3 !important; 
        color: #9d174d !important;  
        font-weight: 700;
    }
    /* Header Importance (Hijau Tosca Pastel) */
    .hoq-importance-header {
        background-color: #ccfbf1 !important;
        color: #115e59 !important;
        font-weight: 700;
    }

    /* === Warna Badan Tabel (Isi Utama) === */
    /* Kolom Kebutuhan Konsumen / WHATs (Biru Langit Pastel) */
    .hoq-td-whats {
        background-color: #e0f2fe !important;
        text-align: left !important;
        font-weight: 600;
        color: #075985 !important;
    }
    /* Kolom Angka Importance (Kuning Pastel) */
    .hoq-importance {
        background-color: #fef3c7 !important;
        font-weight: 700;
        color: #92400e !important;
    }
    
    /* === Warna Bagian Dalam (Sel Korelasi yang Sebelumnya Hitam) === */
    /* Kita beri warna Abu-abu Sangat Muda agar teks 0 terlihat bersih, tidak gelap */
    .hoq-table td:not([class]):not([style]) {
        background-color: #f9fafb !important;
        color: #4b5563 !important;
    }
    
    /* === Warna Fondasi Bawah (Hasil Akhir) === */
    /* Baris Weighted Importance Score (Oranye Pastel) */
    .hoq-score-row {
        background-color: #ffedd5;
        font-weight: bold;
        color: #9a3412 !important;
        border-top: 3px solid #fdba74;
    }
    /* Baris Relative Importance % (Merah Pastel) */
    .hoq-weight-row {
        background-color: #fee2e2;
        font-weight: bold;
        color: #991b1b !important;
    }
    
    /* === Style Khusus untuk Atap Segitiga di Tab 6 === */
    .roof-blank {
        background-color: transparent !important;
        border: none !important;
    }
    .roof-cell {
        background-color: #f3f4f6; /* Abu-abu muda untuk sel atap */
        border: 1px solid #d1d5db !important;
        font-weight: bold;
        color: #1f2937 !important;
    }
    
    /* Legend Info Box dengan gradient cerah */
    .legend-box {
        background: linear-gradient(135deg, #f3f4f6 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    /* Responsive Container */
    .hoq-scroll-container {
        width: 100%;
        overflow-x: auto;
        padding-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# Render Header
st.markdown('<p class="main-header">🏠 Digital House of Quality (HoQ) - UKM Tahu</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Analisis Spesifikasi Teknis vs Voice of Customer dengan Tampilan Fresh & Colorful</p>', unsafe_allow_html=True)

# 2. INISIALISASI DATA (Session State Utama - Tidak Berubah)
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
t1, t2, t3, t4, t5, t6 = st.tabs([
    "1. WHATs", "2. HOWs", "3. Correlation", "4. Matrix", "5. 🏆 FINAL HOUSE & ACTION PLAN", "🏛️ 6. FULL HOQ ARCHITECTURE"
])

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

# Filter list dinamis
whats_list = [x for x in st.session_state.df_whats["Customer Requirement (WHATs)"].tolist() if pd.notna(x) and x != ""]
hows_list = [x for x in st.session_state.df_hows["Technical Requirement (HOWs)"].tolist() if pd.notna(x) and x != ""]

# TAB 3 (Correlation)
with t3:
    st.subheader("Matriks Korelasi Atap (HOWs vs HOWs)")
    if 'roof_matrix' not in st.session_state or list(st.session_state.roof_matrix.columns) != hows_list:
        st.session_state.roof_matrix = pd.DataFrame("No Correlation (0)", index=hows_list, columns=hows_list)
    
    roof_column_config = {
        col: st.column_config.SelectboxColumn(col, options=["Strong Positive (++)", "Positive (+)", "No Correlation (0)", "Negative (-)", "Strong Negative (--)"], required=True)
        for col in hows_list
    }
    st.session_state.roof_matrix = st.data_editor(st.session_state.roof_matrix, use_container_width=True, column_config=roof_column_config, key="ed_roof")

# TAB 4 (Matrix)
with t4:
    st.subheader("♾️ Matriks Hubungan (WHATs vs HOWs)")
    if 'rel_matrix' not in st.session_state or list(st.session_state.rel_matrix.columns) != hows_list or list(st.session_state.rel_matrix.index) != whats_list:
        st.session_state.rel_matrix = pd.DataFrame(0, index=whats_list, columns=hows_list)
    
    rel_column_config = {
        col: st.column_config.SelectboxColumn(col, options=[0, 1, 3, 9], required=True)
        for col in hows_list
    }
    st.session_state.rel_matrix = st.data_editor(st.session_state.rel_matrix, use_container_width=True, column_config=rel_column_config, key="ed_rel")


# --- TAB 5: FINAL HOUSE & ACTION PLAN (PERBAIKAN GRAFIK HILANG) ---
with t5:
    try:
        # Perhitungan Nilai Matematika
        valid_whats = st.session_state.df_whats[st.session_state.df_whats["Customer Requirement (WHATs)"].isin(whats_list)]
        weights = valid_whats["Importance (1-5)"].values.astype(float)
        matrix_values = st.session_state.rel_matrix.loc[whats_list, hows_list].values.astype(float)
        
        abs_importance = weights @ matrix_values
        total = abs_importance.sum()
        rel_importance = (abs_importance / total * 100) if total > 0 else abs_importance * 0

        # Buat DataFrame Hasil Akhir
        res_df = pd.DataFrame({
            "Requirement": hows_list,
            "Score": abs_importance,
            "Weight %": rel_importance.round(1)
        }).sort_values(by="Score", ascending=False)

        st.markdown('### 💡 Kesimpulan Strategis & Arah Pengembangan')
        
        # Penanganan jika data masih serba nol (agar teks persentase dinamis)
        top_priority = res_df.iloc[0]
        display_weight = f"{top_priority['Weight %']}%" if total > 0 else "0.0%"

        # Membuat container atas (Rekomendasi Utama & Urutan Urgensi)
        col_rec, col_urg = st.columns([1.2, 1])
        
        with col_rec:
            st.success(f"✍️ **Rekomendasi Utama Untuk Bisnis Anda:**\n\nUntuk memaksimalkan kepuasan pelanggan tanpa membuang-buang anggaran, fokuskan seluruh biaya dan resource teknis tim Anda saat ini pada pengembangan: **{top_priority['Requirement']}**.\n\nSpesifikasi ini memegang kontribusi terbesar, yaitu sebesar **{display_weight}** dari total seluruh ekspektasi pelanggan yang Anda masukkan.")
        
        with col_urg:
            st.warning("⚠️ **Urutan Urgensi Rencana Aksi (Action Plan):**")
            for idx, row in enumerate(res_df.itertuples()):
                label = "Prioritas Utama (Segera Eksekusi)" if idx == 0 else "Prioritas Sekunder (Pantau Berkala)" if idx == 1 else "Prioritas Tersier (Pertahankan)" if idx == 2 else "Pendukung"
                st.markdown(f"{idx+1}. **{label}**: Optimalisasi/jaga parameter pada `{row.Requirement}`.")

        with st.expander("🔍 Bagaimana sistem menentukan arah rekomendasi ini?"):
            st.write("Sistem mendeteksi tingkat kepentingan pelanggan (Importance Score) lalu mengalikannya dengan bobot matriks hubungan (9/3/1/0) pada masing-masing spesifikasi teknis untuk mendapatkan nilai prioritas kumulatif.")

        st.write("---")

        # --------------------------------------------------------------------------------------
        # REVISI STRUKTUR: Meletakkan Cetak Grafik & Urutan Medali tepat di bawahnya secara absolut
        # --------------------------------------------------------------------------------------
        col_chart, col_rank = st.columns([1.4, 1])
        with col_chart:
            st.write("#### 📈 Grafik Prioritas Spesifikasi Teknis")
            # Skala warna cerah Viridis
            fig = px.bar(res_df, x="Requirement", y="Weight %", text="Weight %",
                         color="Score", color_continuous_scale="Viridis", labels={'Weight %':'Kontribusi (%)'})
            fig.update_layout(height=380, margin=dict(t=20, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
            
        with col_rank:
            st.write("#### 🏆 Urutan Rencana Aksi (Medal Berwarna)")
            for i, row in enumerate(res_df.itertuples()):
                medal = "🥇 PRIORITAS UTAMA" if i == 0 else "🥈 KEDUA" if i == 1 else "🥉 KETIGA" if i == 2 else "🔹 PENDUKUNG"
                st.info(f"**{medal}**\n\n**{row.Requirement}** — Skor: *{int(row.Score)}* ({row._3}%)")

        st.write("---")

        # -------------------------------------------------------------
        # VENDOR MATRIKS DI BAGIAN BAWAH TAB 5 (TETAP ADA & COLORFUL)
        # -------------------------------------------------------------
        st.write("### 🏢 Bagian Utama & Fondasi: Matriks Hubungan Terintegrasi")
        html_body = '<table class="hoq-table">'
        html_body += '<tr><th class="hoq-th-corner" style="width: 30%;">Customer Requirements (WHATs)</th><th class="hoq-importance-header" style="width: 10%;">Importance</th>'
        for col in hows_list:
            html_body += f'<th class="hoq-th-hows">{col}</th>'
        html_body += '</tr>'
        
        for idx, row_name in enumerate(whats_list):
            imp_val = weights[idx]
            html_body += f'<tr><td class="hoq-td-whats">{row_name}</td><td class="hoq-importance">{int(imp_val)}</td>'
            for col_name in hows_list:
                score_val = st.session_state.rel_matrix.at[row_name, col_name]
                bg_cell = 'style="background-color: #f9fafb; color: #6b7280;"'
                if score_val == 9: bg_cell = 'style="background-color: #fce7f3; color: #9d174d; font-weight: bold; font-size: 16px;"'
                elif score_val == 3: bg_cell = 'style="background-color: #ffedd5; color: #9a3412; font-weight: bold;"'
                elif score_val == 1: bg_cell = 'style="background-color: #ede9fe; color: #4c1d95; font-weight: bold;"'
                html_body += f'<td {bg_cell}>{int(score_val)}</td>'
            html_body += '</tr>'
            
        html_body += f'<tr class="hoq-score-row"><td style="text-align: right;">Weighted Importance (Score)</td><td>-</td>'
        for score in abs_importance: html_body += f'<td>{int(score)}</td>'
        html_body += '</tr><tr class="hoq-weight-row"><td style="text-align: right;">Relative Importance (%)</td><td>-</td>'
        for weight in rel_importance: html_body += f'<td>{weight.round(1)}%</td>'
        html_body += '</tr></table>'
        st.markdown(html_body, unsafe_allow_html=True)

    except Exception as e:
        st.error("Pastikan Anda mengisi data secukupnya pada Tab 1 sampai Tab 4.")


# --- 🏛️ TAB 6: ARSITEKTUR FULL HOQ ---
with t6:
    try:
        st.write("### 🏛️ Visualisasi Arsitektur House of Quality (HoQ) Komplit")
        
        valid_whats = st.session_state.df_whats[st.session_state.df_whats["Customer Requirement (WHATs)"].isin(whats_list)]
        weights = valid_whats["Importance (1-5)"].values.astype(float)
        matrix_values = st.session_state.rel_matrix.loc[whats_list, hows_list].values.astype(float)
        abs_importance = weights @ matrix_values
        total = abs_importance.sum()
        rel_importance = (abs_importance / total * 100) if total > 0 else abs_importance * 0
        n_hows = len(hows_list)
        
        st.markdown("""
        <div class="legend-box">
            <strong>ℹ️ Keterangan Simbol Matriks Hubungan:</strong><br>
            <span style="color: #9d174d; font-size: 16px;"><strong>◎</strong> Kuat (Skor 9)</span> &nbsp;|&nbsp; 
            <span style="color: #9a3412;"><strong>○</strong> Sedang (Skor 3)</span> &nbsp;|&nbsp; 
            <span style="color: #4c1d95;"><strong>△</strong> Lemah (Skor 1)</span> &nbsp;|&nbsp; 
            <span style="color: #6b7280;">Tanpa Simbol = Tidak Berhubungan (Skor 0)</span>
        </div>
        """, unsafe_allow_html=True)
        
        html_hoq = '<div class="hoq-scroll-container"><table class="hoq-table" style="width:auto; margin:auto; border: none; box-shadow: none;">'
        
        for i in range(n_hows - 1):
            html_hoq += '<tr><td class="roof-blank" style="width:250px; background-color: #ffffff;"></td><td class="roof-blank" style="width:80px; background-color: #ffffff;"></td>'
            for j in range(n_hows):
                if j < (n_hows - 1 - i):
                    html_hoq += '<td class="roof-blank" style="background-color: #ffffff;"></td>'
                else:
                    row_target = hows_list[j]
                    col_target = hows_list[n_hows - 1 - i]
                    val = st.session_state.roof_matrix.at[row_target, col_target]
                    simbol, bg_color, text_color = "", "#f3f4f6", "#6b7280"
                    if "Strong Positive" in val: simbol, bg_color, text_color = "++", "#dbeafe", "#1e40af"
                    elif "Positive" in val: simbol, bg_color, text_color = "+", "#d1fae5", "#065f46"
                    elif "Strong Negative" in val: simbol, bg_color, text_color = "--", "#fee2e2", "#991b1b"
                    elif "Negative" in val: simbol, bg_color, text_color = "-", "#ffedd5", "#9a3412"
                    elif "No Correlation" in val: simbol = "0"
                    html_hoq += f'<td class="roof-cell" style="background-color: {bg_color}; color: {text_color} !important;">{simbol}</td>'
            html_hoq += '</tr>'

        html_hoq += '<tr><td colspan="{}" style="background-color:#fdba74; padding:2px; border:none;"></td></tr>'.format(n_hows + 2)

        html_hoq += '<tr><th class="hoq-th-corner">Kebutuhan Konsumen (WHATs)</th><th class="hoq-importance-header">Importance</th>'
        for col in hows_list: html_hoq += f'<th class="hoq-th-hows">{col}</th>'
        html_hoq += '</tr>'
        
        for idx, row_name in enumerate(whats_list):
            imp_val = weights[idx]
            html_hoq += f'<tr><td class="hoq-td-whats">{row_name}</td><td class="hoq-importance">{int(imp_val)}</td>'
            for col_name in hows_list:
                score_val = st.session_state.rel_matrix.at[row_name, col_name]
                bg_cell = 'style="background-color: #f9fafb; color: #6b7280;"'
                simbol_hub = ""
                if score_val == 9: 
                    simbol_hub = "◎"
                    bg_cell = 'style="background-color: #fce7f3; color: #9d174d; font-size: 20px; font-weight: bold;"'
                elif score_val == 3: 
                    simbol_hub = "○"
                    bg_cell = 'style="background-color: #ffedd5; color: #9a3412; font-size: 18px; font-weight: bold;"'
                elif score_val == 1: 
                    simbol_hub = "△"
                    bg_cell = 'style="background-color: #ede9fe; color: #4c1d95; font-size: 18px; font-weight: bold;"'
                html_hoq += f'<td {bg_cell}>{simbol_hub}</td>'
            html_hoq += '</tr>'
            
        html_hoq += '<tr class="hoq-score-row" style="box-shadow: none;"><td style="text-align: right;">Weighted Importance Score</td><td>-</td>'
        for score in abs_importance: html_hoq += f'<td>{int(score)}</td>'
        html_hoq += '</tr><tr class="hoq-weight-row" style="box-shadow: none;"><td style="text-align: right;">Relative Importance (%)</td><td>-</td>'
        for weight in rel_importance: html_hoq += f'<td>{weight.round(1)}%</td>'
        html_hoq += '</tr></table></div>'
        
        st.markdown(html_hoq, unsafe_allow_html=True)
        
    except Exception as e:
        st.error("Lengkapi data terlebih dahulu untuk memuat arsitektur.")
