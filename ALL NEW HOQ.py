import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SETTING HALAMAN & STYLE HOQ RUMAH
st.set_page_config(page_title="Digital HoQ - UKM Tahu", layout="wide")

# Mengambil variabel palet warna utama dari gambar image_31d5e2.png
color_maroon = "#810B31"
color_cream = "#F2E5D5"
color_beige = "#DEC9B1"
color_dark = "#511E1A"

st.markdown(f"""
    <style>
    /* Background aplikasi menggunakan warna cream yang sangat lembut */
    .stApp {{
        background-color: #FAF7F2;
    }}

    /* Judul Utama dengan warna Maroon */
    .main-header {{ 
        font-size: 32px; 
        font-weight: bold; 
        color: {color_maroon}; 
        margin-bottom: 10px; 
    }}
    
    /* Sub-judul dengan warna Cokelat Gelap */
    .sub-header {{ 
        font-size: 18px; 
        color: {color_dark}; 
        margin-bottom: 25px; 
    }}
    
    /* === Style Tabel Rumah HoQ untuk Tema Terang & Full Color === */
    .hoq-table {{
        border-collapse: collapse;
        margin: 20px 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        width: 100%;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        background-color: #ffffff;
        border: none;
    }}
    
    /* Mengatur border dan padding dasar untuk semua sel */
    .hoq-table th, .hoq-table td {{
        border: 1px solid {color_beige};
        padding: 14px;
        text-align: center;
        font-size: 14px;
        color: {color_dark} !important; /* Warna teks utama cokelat gelap agar terbaca jelas */
    }}

    /* === Warna Kepala Tabel (Headers) === */
    /* Pojok kiri atas (Beige) */
    .hoq-th-corner {{
        background-color: {color_beige} !important;
        font-weight: 700;
        color: {color_dark} !important;
    }}
    /* Header spesifikasi teknis / HOWs (Cream) */
    .hoq-th-hows {{
        background-color: {color_cream} !important; 
        color: {color_maroon} !important;  
        font-weight: 700;
    }}
    /* Header Importance (Maroon dengan teks Putih) */
    .hoq-importance-header {{
        background-color: {color_maroon} !important;
        color: #ffffff !important;
        font-weight: 700;
    }}

    /* === Warna Badan Tabel (Isi Utama) === */
    /* Kolom Kebutuhan Konsumen / WHATs (Putih Bersih dengan aksen border Maroon) */
    .hoq-td-whats {{
        background-color: #ffffff !important;
        text-align: left !important;
        font-weight: 600;
        color: {color_dark} !important;
        border-left: 5px solid {color_maroon} !important;
    }}
    /* Kolom Angka Importance (Cream) */
    .hoq-importance {{
        background-color: {color_cream} !important;
        font-weight: 700;
        color: {color_maroon} !important;
    }}
    
    /* === Warna Bagian Dalam (Sel Korelasi yang Belum Diatur Style-nya) === */
    .hoq-table td:not([class]):not([style]) {{
        background-color: #ffffff !important;
        color: #9ca3af !important;
    }}
    
    /* === Warna Fondasi Bawah (Hasil Akhir) === */
    /* Baris Weighted Importance Score (Beige) */
    .hoq-score-row {{
        background-color: {color_beige} !important;
        font-weight: bold;
        color: {color_dark} !important;
        border-top: 3px solid {color_maroon};
    }}
    /* Baris Relative Importance % (Cream) */
    .hoq-weight-row {{
        background-color: {color_cream} !important;
        font-weight: bold;
        color: {color_maroon} !important;
    }}
    
    /* === Style Khusus untuk Atap Segitiga di Tab 6 === */
    .roof-blank {{
        background-color: transparent !important;
        border: none !important;
    }}
    .roof-cell {{
        background-color: #ffffff; 
        border: 1px solid {color_beige} !important;
        font-weight: bold;
    }}
    
    /* Legend Info Box dengan warna Cream */
    .legend-box {{
        background-color: {color_cream};
        padding: 20px;
        border-radius: 12px;
        border: 1px solid {color_beige};
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }}
    
    /* Responsive Container */
    .hoq-scroll-container {{
        width: 100%;
        overflow-x: auto;
        padding-bottom: 15px;
    }}
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
t1, t2, t3, t4, t5, t6 = st.tabs([
    "1. WHATs", "2. HOWs", "3. Correlation", "4. Matrix", "5. 🏆 FINAL HOUSE & ACTION PLAN", "🏛️ 6. FULL HOQ ARCHITECTURE"
])

# TAB 1: Input WHATs
with t1:
    st.subheader("Masukkan Voice of Customer (WHATs)")
    st.caption("Isi dengan kebutuhan pelanggan dan bobot pentingnya dari 1 (tidak penting) hingga 5 (sangat penting).")
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
    st.subheader("♾️ Hubungan Kebutuhan Konsumen vs Spesifikasi Teknis")
    
    st.info("""
    💡 **Panduan :**
    Pikirkan seberapa besar pengaruh **'Spesifikasi Teknis'** dalam memenuhi **'Kebutuhan Konsumen'** Anda:
    - **9 (Kuat):** Spesifikasi ini adalah kunci utama agar kebutuhan konsumen tersebut terpenuhi.
    - **3 (Sedang):** Berpengaruh secara tidak langsung, namun bukan satu-satunya faktor penentu.
    - **1 (Lemah):** Memiliki pengaruh yang sangat kecil/tipis.
    - **0:** Tidak berkaitan atau tidak memiliki pengaruh sama sekali.
    """)
    
    if 'rel_matrix' not in st.session_state or list(st.session_state.rel_matrix.columns) != hows_list or list(st.session_state.rel_matrix.index) != whats_list:
        st.session_state.rel_matrix = pd.DataFrame(0, index=whats_list, columns=hows_list)
    
    rel_column_config = {
        col: st.column_config.SelectboxColumn(col, options=[0, 1, 3, 9], required=True)
        for col in hows_list
    }
    st.session_state.rel_matrix = st.data_editor(st.session_state.rel_matrix, use_container_width=True, column_config=rel_column_config, key="ed_rel")


# --- TAB 5: THE FINAL HOUSE & ACTION PLAN ---
with t5:
    try:
        # Perhitungan Nilai Matematika Utama
        valid_whats = st.session_state.df_whats[st.session_state.df_whats["Customer Requirement (WHATs)"].isin(whats_list)]
        weights = valid_whats["Importance (1-5)"].values.astype(float)
        matrix_values = st.session_state.rel_matrix.loc[whats_list, hows_list].values.astype(float)
        
        abs_importance = weights @ matrix_values
        total = abs_importance.sum()
        rel_importance = (abs_importance / total * 100) if total > 0 else abs_importance * 0

        # DataFrame Hasil Akhir untuk Chart dan Rekomendasi
        res_df = pd.DataFrame({
            "Requirement": hows_list,
            "Score": abs_importance,
            "Weight %": rel_importance.round(1)
        }).sort_values(by="Score", ascending=False)

        st.write("### 💡 Kesimpulan Strategis & Arah Pengembangan")
        
        top_priorities = res_df.head(3)
        priority_names = top_priorities["Requirement"].tolist()
        priority_weights = top_priorities["Weight %"].tolist()
        
        col_rec, col_summary = st.columns([1.2, 1])
        
        with col_rec:
            st.success(f"✍️ **Rekomendasi Utama Untuk Bisnis Anda:**")
            st.write(f"""
            Fokuskan seluruh biaya dan resource teknis tim Anda saat ini pada pengembangan: **{priority_names[0]}**.
            Spesifikasi ini memegang kontribusi terbesar, yaitu sebesar **{priority_weights[0]}%** dari total seluruh ekspektasi pelanggan.
            """)
            
        with col_summary:
            st.warning("⚠️ **Urutan Urgensi Rencana Aksi (Action Plan):**")
            st.write(f"1. **Prioritas Utama:** Optimalisasi penuh parameter pada `{priority_names[0]}`.")
            if len(priority_names) > 1:
                st.write(f"2. **Prioritas Sekunder:** Jaga stabilitas kualitas `{priority_names[1]}`.")
            if len(priority_names) > 2:
                st.write(f"3. **Prioritas Tersier:** Lakukan pengawasan standarisasi pada `{priority_names[2]}`.")
            
        st.write("---")

        # 1. VISUALISASI MATRIKS ATAP (HOWs vs HOWs) - VERSI PALET BARU
        st.write("### 🛖 Bagian Atap: Matriks Korelasi Antar Persyaratan Teknis")
        
        html_roof = '<table class="hoq-table">'
        html_roof += '<tr>'
        html_roof += f'<th class="hoq-th-corner" style="width: 30%;">Spesifikasi Teknis</th>'
        for col in hows_list:
            html_roof += f'<th class="hoq-th-hows">{col}</th>'
        html_roof += '</tr>'
        
        for row_name in hows_list:
            html_roof += '<tr>'
            html_roof += f'<td class="hoq-td-whats">{row_name}</td>'
            for col_name in hows_list:
                val = st.session_state.roof_matrix.at[row_name, col_name]
                
                simbol = "0"
                bg_cell = 'style="background-color: #ffffff; color: #9ca3af;"' 
                
                if "Strong Positive" in val: 
                    simbol = "++"
                    bg_cell = f'style="background-color: {color_maroon}; color: #ffffff; font-weight: 600;"' 
                elif "Positive" in val: 
                    simbol = "+"
                    bg_cell = f'style="background-color: {color_beige}; color: {color_dark}; font-weight: 600;"' 
                elif "Strong Negative" in val: 
                    simbol = "--"
                    bg_cell = f'style="background-color: {color_dark}; color: #ffffff; font-weight: 600;"' 
                elif "Negative" in val: 
                    simbol = "-"
                    bg_cell = f'style="background-color: {color_cream}; color: {color_maroon}; font-weight: 600;"' 
                
                html_roof += f'<td {bg_cell}>{simbol}</td>'
            html_roof += '</tr>'
        html_roof += '</table>'
        st.markdown(html_roof, unsafe_allow_html=True)

        st.write("")

        # 2. VISUALISASI BADAN & FONDASI RUMAH HOQ - VERSI PALET BARU
        st.write("### 🏢 Bagian Utama & Fondasi: Matriks Hubungan Terintegrasi")
        
        html_body = '<table class="hoq-table">'
        html_body += '<tr>'
        html_body += f'<th class="hoq-th-corner" style="width: 30%;">Customer Requirements (WHATs)</th>'
        html_body += f'<th class="hoq-importance-header" style="width: 10%;">Importance</th>'
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
                
                bg_cell = 'style="background-color: #ffffff; color: #9ca3af;"' 
                
                if score_val == 9: 
                    bg_cell = f'style="background-color: {color_maroon}; color: #ffffff; font-weight: 600;"' 
                elif score_val == 3: 
                    bg_cell = f'style="background-color: {color_beige}; color: {color_dark}; font-weight: 600;"' 
                elif score_val == 1: 
                    bg_cell = f'style="background-color: {color_cream}; color: {color_maroon}; font-weight: 600;"' 
                
                html_body += f'<td {bg_cell}>{int(score_val)}</td>'
            html_body += '</tr>'
            
        # Fondasi: Absolute Importance
        html_body += '<tr class="hoq-score-row">'
        html_body += '<td style="text-align: right; font-weight: bold;">Weighted Importance (Score)</td>'
        html_body += '<td>-</td>'
        for score in abs_importance:
            html_body += f'<td style="font-weight: 700;">{int(score)}</td>'
        html_body += '</tr>'

        # Fondasi: Relative Weight %
        html_body += '<tr class="hoq-weight-row">'
        html_body += '<td style="text-align: right; font-weight: bold;">Relative Importance (%)</td>'
        html_body += '<td>-</td>'
        for weight in rel_importance:
            html_body += f'<td style="font-weight: 700;">{weight.round(1)}%</td>'
        html_body += '</tr>'
        html_body += '</table>'
        st.markdown(html_body, unsafe_allow_html=True)
        
        st.write("---")
        
        # 3. GRID GRAFIK BAR (VERTIKAL)
        st.write("#### 📈 Grafik Kontribusi Prioritas Teknis")
        fig = px.bar(res_df, x="Requirement", y="Score", text="Weight %",
                     color_discrete_sequence=[color_maroon])
        fig.update_layout(height=400, margin=dict(t=10, b=10), plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error("Silakan lengkapi atau periksa kembali seluruh inputan di tab sebelumnya!")


# --- 🏛️ TAB 6: FULL HOQ ARCHITECTURE ---
with t6:
    try:
        st.write("### 🏛️ Arsitektur Matriks House of Quality (HoQ) Komplit")
        
        valid_whats = st.session_state.df_whats[st.session_state.df_whats["Customer Requirement (WHATs)"].isin(whats_list)]
        weights = valid_whats["Importance (1-5)"].values.astype(float)
        matrix_values = st.session_state.rel_matrix.loc[whats_list, hows_list].values.astype(float)
        
        abs_importance = weights @ matrix_values
        total = abs_importance.sum()
        rel_importance = (abs_importance / total * 100) if total > 0 else abs_importance * 0
        
        n_hows = len(hows_list)
        
        # Box Keterangan Simbol (Legend) dengan Palet Warna Baru
        st.markdown(f"""
        <div class="legend-box">
            <strong>ℹ️ Keterangan Simbol Hubungan Matriks (Badan Utama):</strong><br>
            <span style="color: {color_maroon}; font-weight: bold;">◎ Kontribusi Kuat (Skor 9)</span> &nbsp;|&nbsp; 
            <span style="color: {color_dark}; font-weight: bold;">○ Kontribusi Sedang (Skor 3)</span> &nbsp;|&nbsp; 
            <span style="color: {color_maroon}; font-weight: bold;">△ Kontribusi Lemah (Skor 1)</span> &nbsp;|&nbsp; 
            <span style="color: #9ca3af;">Tanpa Simbol = Tidak Berhubungan (Skor 0)</span>
        </div>
        """, unsafe_allow_html=True)
        
        html_hoq = '<div class="hoq-scroll-container">'
        html_hoq += '<table class="hoq-table" style="width:auto; margin:auto;">'
        
        # 1. GENERATE ATAP SEGITIGA (Roof Matrix Upper Triangle)
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
                    bg_color = "#ffffff"
                    text_color = "#9ca3af"
                    
                    if "Strong Positive" in val: simbol, bg_color, text_color = "++", color_maroon, "#ffffff"
                    elif "Positive" in val: simbol, bg_color, text_color = "+", color_beige, color_dark
                    elif "Strong Negative" in val: simbol, bg_color, text_color = "--", color_dark, "#ffffff"
                    elif "Negative" in val: simbol, bg_color, text_color = "-", color_cream, color_maroon
                    elif "No Correlation" in val: simbol, bg_color, text_color = "0", "#ffffff", "#6b7280"
                    
                    html_hoq += f'<td class="roof-cell" style="background-color: {bg_color}; color: {text_color} !important;">{simbol}</td>'
            html_hoq += '</tr>'

        html_hoq += f'<tr><td colspan="{{}}" style="background-color:{color_beige}; padding:2px; border:none;"></td></tr>'.format(n_hows + 2)

        # 2. GENERATE KEPALA TABEL BADAN UTAMA
        html_hoq += '<tr>'
        html_hoq += '<th class="hoq-th-corner">Customer Requirements (WHATs)</th>'
        html_hoq += '<th class="hoq-importance-header">Importance</th>'
        for col in hows_list:
            html_hoq += f'<th class="hoq-th-hows">{col}</th>'
        html_hoq += '</tr>'
        
        # 3. GENERATE BADAN MATRIKS UTAMA
        for idx, row_name in enumerate(whats_list):
            imp_val = weights[idx]
            html_hoq += '<tr>'
            html_hoq += f'<td class="hoq-td-whats">{row_name}</td>'
            html_hoq += f'<td class="hoq-importance">{int(imp_val)}</td>'
            for col_name in hows_list:
                score_val = st.session_state.rel_matrix.at[row_name, col_name]
                
                bg_cell = 'style="background-color: #ffffff; color: #9ca3af;"'
                simbol_hub = ""
                
                if score_val == 9: 
                    simbol_hub = "◎"
                    bg_cell = f'style="background-color: {color_maroon}; color: #ffffff; font-size: 18px; font-weight: bold;"' 
                elif score_val == 3: 
                    simbol_hub = "○"
                    bg_cell = f'style="background-color: {color_beige}; color: {color_dark}; font-size: 18px; font-weight: bold;"' 
                elif score_val == 1: 
                    simbol_hub = "△"
                    bg_cell = f'style="background-color: {color_cream}; color: {color_maroon}; font-size: 18px; font-weight: bold;"' 
                
                html_hoq += f'<td {bg_cell}>{simbol_hub}</td>'
            html_hoq += '</tr>'
            
        # 4. GENERATE FONDASI RUMAH HOQ
        html_hoq += '<tr class="hoq-score-row">'
        html_hoq += '<td style="text-align: right; font-weight: bold;">Weighted Importance (Score)</td>'
        html_hoq += '<td>-</td>'
        for score in abs_importance:
            html_hoq += f'<td>{int(score)}</td>'
        html_hoq += '</tr>'

        html_hoq += '<tr class="hoq-weight-row">'
        html_hoq += '<td style="text-align: right; font-weight: bold;">Relative Importance (%)</td>'
        html_hoq += '<td>-</td>'
        for weight in rel_importance:
            html_hoq += f'<td>{weight.round(1)}%</td>'
        html_hoq += '</tr>'
        
        html_hoq += '</table>'
        html_hoq += '</div>'
        
        st.markdown(html_hoq, unsafe_allow_html=True)
        
    except Exception as e:
        st.error("Silakan pastikan semua data pada input Tab 1 sampai 4 diisi dengan benar.")
