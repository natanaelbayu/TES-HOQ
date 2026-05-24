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

# TAB 5: FINAL HOUSE & ACTION PLAN (SUDAH INCLUDE BAR CHART DI SINI)
with t5:
    try:
        valid_whats = st.session_state.df_whats[st.session_state.df_whats["Customer Requirement (WHATs)"].isin(whats_list)]
        weights = valid_whats["Importance (1-5)"].values.astype(float)
        matrix_values = st.session_state.rel_matrix.loc[whats_list, hows_list].values.astype(float)
        
        abs_importance = weights @ matrix_values
        total = abs_importance.sum()
        
        if total == 0:
            st.info("💡 **Matriks Hubungan Belum Diisi:** Silakan isi nilai hubungan (1, 3, atau 9) pada **Tab 4. Matrix** terlebih dahulu untuk melihat analisis kesimpulan dan grafik prioritas strategi.")
        else:
            rel_importance = (abs_importance / total * 100)
            res_df = pd.DataFrame({
                "Technical Requirement": hows_list, 
                "Absolute Score": abs_importance, 
                "Relative Weight (%)": rel_importance.round(1)
            }).sort_values(by="Absolute Score", ascending=False)

            st.write("### 💡 Kesimpulan Strategis & Arah Pengembangan")
            top_priorities = res_df.head(3)
            priority_names = top_priorities["Technical Requirement"].tolist()
            priority_weights = top_priorities["Relative Weight (%)"].tolist()
            
            col_rec, col_summary = st.columns([1.2, 1])
            with col_rec:
                st.success(f"✍️ **Rekomendasi Utama For Business:** Fokus penuh pada pengembangan teknis **{priority_names[0]}** yang memiliki kontribusi terbesar ({priority_weights[0]}%).")
            with col_summary:
                st.warning("⚠️ **Urutan Urgensi Rencana Aksi:**")
                for rank, name in enumerate(priority_names, 1):
                    st.write(f"{rank}. **Prioritas {rank}:** `{name}`")
            
            # --- PENAMBAHAN GRAFIK BAR ---
            st.write("---")
            st.write("### 📊 Grafik Kontribusi Prioritas Teknis (Relative Weight %)")
            
            # Membuat Bar Chart menggunakan Plotly Express
            fig = px.bar(
                res_df.sort_values(by="Relative Weight (%)", ascending=True), # Diurutkan agar yang terbesar di atas
                x="Relative Weight (%)",
                y="Technical Requirement",
                orientation='h', # Grafik horizontal agar teks label terbaca jelas
                text="Relative Weight (%)",
                color="Relative Weight (%)",
                color_continuous_scale="Blues"
            )
            
            fig.update_traces(texttemplate='%{text}%', textposition='outside', marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.85)
            fig.update_layout(
                xaxis_title="Kontribusi (%)",
                yaxis_title="Spesifikasi Teknis (HOWs)",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="white"),
                showlegend=False,
                height=350
            )
            
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error("Silakan lengkapi input data pada tab-tab sebelumnya!")

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
        
        legend_html = (
            '<div class="legend-box">'
            '<strong>ℹ️ Keterangan Simbol & Warna:</strong><br>'
            '<span><strong>◎</strong> Kuat (9) | <strong>○</strong> Sedang (3) | <strong>△</strong> Lemah (1)</span><br>'
            '<span style="border: 1px solid #475569; padding: 2px 5px; background-color: #1e3a8a;">++</span> Strong Positive &nbsp;|&nbsp; '
            '<span style="border: 1px solid #475569; padding: 2px 5px; background-color: #14532d;">+</span> Positive &nbsp;|&nbsp; '
            '<span style="border: 1px solid #475569; padding: 2px 5px; background-color: #7c2d12;">-</span> Negative &nbsp;|&nbsp; '
            '<span style="border: 1px solid #475569; padding: 2px 5px; background-color: #7f1d1d;">--</span> Strong Negative'
            '</div>'
        )
        st.markdown(legend_html, unsafe_allow_html=True)
        
        html_hoq = '<div class="hoq-scroll-container">'
        html_hoq += '<table class="hoq-table" style="width:auto; margin:auto;">'
        
        # -------------------------------------------------------------
        # 1. GENERATE ATAP ATAS (HOWs vs HOWs)
        # -------------------------------------------------------------
        for i in range(n_hows - 1):
            html_hoq += '<tr>'
            for _ in range(n_side_cols):
                html_hoq += '<td class="roof-blank"></td>'
            html_hoq += '<td class="roof-blank" style="width:250px;"></td>'  
            html_hoq += '<td class="roof-blank" style="width:80px;"></td>'   
            
            for j in range(n_hows):
                if j < (n_hows - 1 - i):
                    html_hoq += '<td class="roof-blank"></td>'
                else:
                    row_target = hows_list[j]
                    col_target = hows_list[n_hows - 1 - i]
                    val = st.session_state.roof_matrix.at[row_target, col_target]
                    
                    simbol, bg_color, text_color = "0", "#0f172a", "#475569"
                    if "Strong Positive" in val: simbol, bg_color, text_color = "++", "#1e3a8a", "#38bdf8"
                    elif "Positive" in val: simbol, bg_color, text_color = "+", "#14532d", "#4ade80"
                    elif "Strong Negative" in val: simbol, bg_color, text_color = "--", "#7f1d1d", "#f87171"
                    elif "Negative" in val: simbol, bg_color, text_color = "-", "#7c2d12", "#fb923c"
                    
                    html_hoq += f'<td class="roof-cell" style="background-color: {bg_color}; color: {text_color} !important;">{simbol}</td>'
            html_hoq += '</tr>'

        html_hoq += '<tr><td colspan="{}" style="background-color:#334155; padding:2px; border:none;"></td></tr>'.format(n_side_cols + 2 + n_hows)

        # -------------------------------------------------------------
        # 2. GENERATE KEPALA TABEL BADAN UTAMA
        # -------------------------------------------------------------
        html_hoq += '<tr>'
        for k in range(n_side_cols):
            html_hoq += f'<th class="side-roof-header">Korelasi L-{k+1}</th>'
            
        html_hoq += '<th class="hoq-th-corner">Customer Requirements (WHATs)</th>'
        html_hoq += '<th class="hoq-importance-header">Importance</th>'
        for col in hows_list:
            html_hoq += f'<th class="hoq-th-hows">{col}</th>'
        html_hoq += '</tr>'
        
        # -------------------------------------------------------------
        # 3. GENERATE BADAN UTAMA + ROOF SAMPING KIRI (WHATs vs WHATs)
        # -------------------------------------------------------------
        for idx, row_name in enumerate(whats_list):
            imp_val = weights[idx]
            html_hoq += '<tr>'
            
            for s_idx in range(n_side_cols):
                target_col_idx = idx + s_idx + 1
                if target_col_idx < n_whats:
                    target_whats_name = whats_list[target_col_idx]
                    val_side = st.session_state.whats_roof_matrix.at[row_name, target_whats_name]
                    
                    simbol_s, bg_s, text_s = "0", "#0f172a", "#475569"
                    if "Strong Positive" in val_side: simbol_s, bg_s, text_s = "++", "#1e3a8a", "#38bdf8"
                    elif "Positive" in val_side: simbol_s, bg_s, text_s = "+", "#14532d", "#4ade80"
                    elif "Strong Negative" in val_side: simbol_s, bg_s, text_s = "--", "#7f1d1d", "#f87171"
                    elif "Negative" in val_side: simbol_s, bg_s, text_s = "-", "#7c2d12", "#fb923c"
                    
                    html_hoq += f'<td class="side-roof-cell" style="background-color: {bg_s}; color: {text_s} !important;">{simbol_s}</td>'
                else:
                    html_hoq += '<td class="roof-blank"></td>'
            
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
        # 4. GENERATE FONDASI RUMAH HOQ
        # -------------------------------------------------------------
        html_hoq += '<tr class="hoq-score-row">'
        for _ in range(n_side_cols): html_hoq += '<td class="roof-blank"></td>'
        html_hoq += '<td style="text-align: right; color: #38bdf8;">Weighted Importance (Score)</td>'
        html_hoq += '<td style="color: #38bdf8;">-</td>'
        for score in abs_importance:
            html_hoq += f'<td style="background-color: #1e293b; color: #38bdf8 !important;">{int(score)}</td>'
        html_hoq += '</tr>'

        html_hoq += '<tr class="hoq-weight-row">'
        for _ in range(n_side_cols): html_hoq += '<td class="roof-blank"></td>'
        html_hoq += '<td style="text-align: right; color: #2dd4bf;">Relative Importance (%)</td>'
        html_hoq += '<td style="color: #2dd4bf;">-</td>'
        for weight in rel_importance:
            html_hoq += f'<td style="background-color: #1e293b; color: #2dd4bf !important;">{weight.round(1)}%</td>'
        html_hoq += '</tr>'
        
        html_hoq += '</table>'
        html_hoq += '</div>' 
        
        st.markdown(html_hoq, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Gagal memuat arsitektur penuh: {e}")
