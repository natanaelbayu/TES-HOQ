import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SETTING HALAMAN & STYLE HOQ RUMAH
st.set_page_config(page_title="Digital HoQ - UKM Tahu", layout="wide")

st.markdown("""
    <style>
    .main-header { font-size: 28px; font-weight: bold; color: #38bdf8; margin-bottom: 10px; }
    .sub-header { font-size: 18px; color: #94a3b8; margin-bottom: 20px; }
    .hoq-table {
        border-collapse: collapse;
        margin: 20px 0;
        font-family: sans-serif;
        width: 100%;
        background-color: #0f172a;
    }
    .hoq-table th, .hoq-table td {
        border: 1px solid #334155;
        padding: 12px;
        text-align: center;
        font-size: 14px;
        color: #ffffff !important;
    }
    .hoq-th-corner, .hoq-th-hows, .hoq-importance-header {
        background-color: #1e293b !important;
        font-weight: 600;
        color: #ffffff !important;
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
    .hoq-score-row, .hoq-weight-row {
        background-color: #1e293b;
        font-weight: bold;
        color: #ffffff !important;
    }
    .hoq-table td:not([style]) {
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
    }
    .roof-blank { background-color: transparent !important; border: none !important; }
    .roof-cell { background-color: #1e293b; border: 1px solid #475569 !important; font-weight: bold; }
    .legend-box { background-color: #1e293b; padding: 15px; border-radius: 8px; border: 1px solid #334155; margin-bottom: 15px; }
    .hoq-scroll-container { width: 100%; overflow-x: auto; padding-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🏠 Digital House of Quality (HoQ)</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Optimalisasi Spesifikasi Teknis berdasarkan Voice of Customer (UKM Tahu Endang)</p>', unsafe_allow_html=True)


# =====================================================================
# 2. INISIALISASI DATA DATA AWAL (NAMA KEY FIXED & AMAN)
# =====================================================================
if "df_whats" not in st.session_state:
    st.session_state["df_whats"] = pd.DataFrame({
        "Customer Requirement (WHATs)": ["Tahu tidak mudah hancur", "Rasa kedelai terasa", "Warna kuning cerah", "Harga terjangkau"],
        "Importance (1-5)": [5, 4, 3, 5]
    })

if "df_hows" not in st.session_state:
    st.session_state["df_hows"] = pd.DataFrame({
        "Technical Requirement (HOWs)": ["Tekanan Mesin Pres", "Kualitas Kedelai", "Lama Perebusan", "Takaran Kunyit"],
        "Direction": ["Max", "Max", "Target", "Max"]
    })

# Filter list dinamis agar sel kosong tidak ikut terbaca
whats_list = [x for x in st.session_state["df_whats"]["Customer Requirement (WHATs)"].tolist() if pd.notna(x) and x != ""]
hows_list = [x for x in st.session_state["df_hows"]["Technical Requirement (HOWs)"].tolist() if pd.notna(x) and x != ""]


# --- INISIALISASI MATRIKS LANJUTAN ---
if "roof_matrix" not in st.session_state:
    st.session_state["roof_matrix"] = pd.DataFrame("No Correlation (0)", index=hows_list, columns=hows_list)
else:
    old_roof = st.session_state["roof_matrix"]
    if list(old_roof.columns) != hows_list or list(old_roof.index) != hows_list:
        new_roof = pd.DataFrame("No Correlation (0)", index=hows_list, columns=hows_list)
        new_roof.update(old_roof)
        st.session_state["roof_matrix"] = new_roof

if "rel_matrix" not in st.session_state:
    st.session_state["rel_matrix"] = pd.DataFrame(0, index=whats_list, columns=hows_list)
else:
    old_rel = st.session_state["rel_matrix"]
    if list(old_rel.columns) != hows_list or list(old_rel.index) != whats_list:
        new_rel = pd.DataFrame(0, index=whats_list, columns=hows_list)
        for col in new_rel.columns:
            for row in new_rel.index:
                if col in old_rel.columns and row in old_rel.index:
                    new_rel.at[row, col] = old_rel.at[row, col]
        st.session_state["rel_matrix"] = new_rel


# =====================================================================
# 3. STRUKTUR TABS INTERFACES
# =====================================================================
t1, t2, t3, t4, t5, t6 = st.tabs([
    "1. WHATs", "2. HOWs", "3. Correlation", "4. Matrix", "5. 🏆 FINAL HOUSE & ACTION PLAN", "🏛️ 6. FULL HOQ ARCHITECTURE"
])

# TAB 1: Input WHATs
with t1:
    st.subheader("Masukkan Voice of Customer (WHATs)")
    st.caption("Isi dengan kebutuhan pelanggan dan bobot pentingnya dari 1 hingga 5.")
    # Kita pisahkan key widget (w_whats) dengan data state asli (df_whats)
    edited_whats = st.data_editor(
        st.session_state["df_whats"], 
        num_rows="dynamic", 
        use_container_width=True, 
        column_config={
            "Importance (1-5)": st.column_config.NumberColumn("Importance (1-5)", min_value=1, max_value=5, step=1)
        },
        key="w_whats" 
    )
    st.session_state["df_whats"] = edited_whats # Simpan hasil edit secara manual ke state utama

# TAB 2: Input HOWs
with t2:
    st.subheader("Masukkan Spesifikasi Teknis (HOWs)")
    st.caption("Pilih arah spesifikasi teknis: Max, Min, atau Target.")
    edited_hows = st.data_editor(
        st.session_state["df_hows"], 
        num_rows="dynamic", 
        use_container_width=True, 
        column_config={
            "Direction": st.column_config.SelectboxColumn("Direction", options=["Max", "Min", "Target"], required=True)
        },
        key="w_hows"
    )
    st.session_state["df_hows"] = edited_hows

# TAB 3: Correlation (The Roof)
with t3:
    st.subheader("Matriks Korelasi Atap (HOWs vs HOWs)")
    st.caption("Pilih nilai hubungan korelasi antar sesama spesifikasi produksi teknis.")
    roof_column_config = {
        col: st.column_config.SelectboxColumn(col, options=["Strong Positive (++)", "Positive (+)", "No Correlation (0)", "Negative (-)", "Strong Negative (--)"], required=True)
        for col in hows_list
    }
    edited_roof = st.data_editor(st.session_state["roof_matrix"], use_container_width=True, column_config=roof_column_config, key="w_roof")
    st.session_state["roof_matrix"] = edited_roof

# TAB 4: Relationship Matrix
with t4:
    st.subheader("♾️ Hubungan Kebutuhan Konsumen vs Spesifikasi Teknis")
    st.info("""💡 **Panduan Skor :** **9 (Kuat)** | **3 (Sedang)** | **1 (Lemah)** | **0 (Tidak Ada Hubungan)**""")
    rel_column_config = {
        col: st.column_config.SelectboxColumn(col, options=[0, 1, 3, 9], required=True)
        for col in hows_list
    }
    edited_rel = st.data_editor(st.session_state["rel_matrix"], use_container_width=True, column_config=rel_column_config, key="w_rel")
    st.session_state["rel_matrix"] = edited_rel


# TAB 5: THE FINAL HOUSE & ACTION PLAN
with t5:
    try:
        valid_whats = st.session_state["df_whats"][st.session_state["df_whats encampment" if False else "Customer Requirement (WHATs)"].isin(whats_list)]
        weights = valid_whats["Importance (1-5)"].values.astype(float)
        
        matrix_values = st.session_state["rel_matrix"].loc[whats_list, hows_list].values.astype(float)
        
        abs_importance = weights @ matrix_values
        total = abs_importance.sum()
        rel_importance = (abs_importance / total * 100) if total > 0 else abs_importance * 0

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
            Fokuskan biaya dan resource teknis tim Anda saat ini pada pengembangan: **{priority_names[0]}**.
            Spesifikasi ini memegang kontribusi terbesar, yaitu sebesar **{priority_weights[0]}%** dari total ekspektasi pelanggan.
            """)
            
        with col_summary:
            st.warning("⚠️ **Urutan Urgensi Rencana Aksi (Action Plan):**")
            st.write(f"1. **Prioritas Utama:** Optimalisasi penuh parameter pada `{priority_names[0]}`.")
            if len(priority_names) > 1:
                st.write(f"2. **Prioritas Sekunder:** Jaga stabilitas kualitas `{priority_names[1]}`.")
            if len(priority_names) > 2:
                st.write(f"3. **Prioritas Tersier:** Pengawasan standarisasi pada `{priority_names[2]}`.")

        st.write("---")

        # Visualisasi Atap
        st.write("### 🛖 Bagian Atap: Matriks Korelasi Antar Persyaratan Teknis")
        html_roof = '<table class="hoq-table"><tr><th class="hoq-th-corner" style="width: 30%;">Spesifikasi Teknis</th>'
        for col in hows_list: html_roof += f'<th class="hoq-th-hows">{col}</th>'
        html_roof += '</tr>'
        
        for row_name in hows_list:
            html_roof += f'<tr><td class="hoq-td-whats">{row_name}</td>'
            for col_name in hows_list:
                val = st.session_state["roof_matrix"].at[row_name, col_name]
                simbol, bg_cell = "0", 'style="background-color: #0f172a; color: #64748b;"'
                if "Strong Positive" in val: simbol, bg_cell = "++", 'style="background-color: #1e3a8a; color: #ffffff; font-weight: 600;"'
                elif "Positive" in val: simbol, bg_cell = "+", 'style="background-color: #14532d; color: #ffffff; font-weight: 600;"'
                elif "Strong Negative" in val: simbol, bg_cell = "--", 'style="background-color: #7f1d1d; color: #ffffff; font-weight: 600;"'
                elif "Negative" in val: simbol, bg_cell = "-", 'style="background-color: #7c2d12; color: #ffffff; font-weight: 600;"'
                html_roof += f'<td {bg_cell}>{simbol}</td>'
            html_roof += '</tr>'
        html_roof += '</table>'
        st.markdown(html_roof, unsafe_allow_html=True)

        # Visualisasi Badan Utama Matriks
        st.write("### 🏢 Bagian Utama & Fondasi: Matriks Hubungan Terintegrasi")
        html_body = f'<table class="hoq-table"><tr><th class="hoq-th-corner" style="width: 30%;">Customer Requirements (WHATs)</th><th class="hoq-importance-header" style="width: 10%;">Importance</th>'
        for col in hows_list: html_body += f'<th class="hoq-th-hows">{col}</th>'
        html_body += '</tr>'
        
        for idx, row_name in enumerate(whats_list):
            imp_val = weights[idx]
            html_body += f'<tr><td class="hoq-td-whats">{row_name}</td><td class="hoq-importance">{int(imp_val)}</td>'
            for col_name in hows_list:
                score_val = st.session_state["rel_matrix"].at[row_name, col_name]
                bg_cell = 'style="background-color: #0f172a; color: #64748b;"'
                if score_val == 9: bg_cell = 'style="background-color: #881337; color: #ffffff; font-weight: 600;"'
                elif score_val == 3: bg_cell = 'style="background-color: #7c2d12; color: #ffffff; font-weight: 600;"'
                elif score_val == 1: bg_cell = 'style="background-color: #713f12; color: #ffffff; font-weight: 600;"'
                html_body += f'<td {bg_cell}>{int(score_val)}</td>'
            html_body += '</tr>'
            
        # Fondasi
        html_body += '<tr class="hoq-score-row"><td style="text-align: right; color: #38bdf8;">Weighted Importance (Score)</td><td style="color: #38bdf8;">-</td>'
        for score in abs_importance: html_body += f'<td style="background-color: #1e293b; color: #38bdf8 !important;">{int(score)}</td>'
        html_body += '</tr><tr class="hoq-weight-row"><td style="text-align: right; color: #2dd4bf;">Relative Importance (%)</td><td style="color: #2dd4bf;">-</td>'
        for weight in rel_importance: html_body += f'<td style="background-color: #1e293b; color: #2dd4bf !important;">{weight.round(1)}%</td>'
        html_body += f'</tr></table>'
        st.markdown(html_body, unsafe_allow_html=True)
        
        # Grid Grafik Bar
        col_chart, col_rank = st.columns([1.5, 1])
        with col_chart:
            st.write("#### 📈 Grafik Kontribusi Prioritas Teknis")
            fig = px.bar(res_df, x="Requirement", y="Score", text="Weight %", color="Score", color_continuous_scale="Blues")
            fig.update_layout(height=400, margin=dict(t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)
            
        with col_rank:
            st.write("#### 🏆 Urutan Rekomendasi Tindakan")
            for i, row in enumerate(res_df.itertuples()):
                medal = "🥇 PRIORITAS UTAMA" if i == 0 else "🥈 KEDUA" if i == 1 else "🥉 KETIGA" if i == 2 else "🔹 PENDUKUNG"
                st.info(f"**{medal}**\n\n**{row.Requirement}** — Skor: *{int(row.Score)}* ({row._3}%)")

    except Exception as e:
        st.error("Silakan lengkapi atau periksa kembali seluruh inputan di tab sebelumnya!")


# TAB 6: FULL HOQ ARCHITECTURE
with t6:
    try:
        st.write("### 🏛️ Arsitektur Matriks House of Quality (HoQ) Komplit")
        st.markdown('<div class="legend-box"><strong>ℹ️ Keterangan Simbol:</strong> <span style="color:#38bdf8;"><strong>◎</strong> Kuat (9)</span> | <span style="color:#4ade80;"><strong>○</strong> Sedang (3)</span> | <span style="color:#fef08a;"><strong>△</strong> Lemah (1)</span></div>', unsafe_allow_html=True)
        
        n_hows = len(hows_list)
        html_hoq = '<div class="hoq-scroll-container"><table class="hoq-table" style="width:auto; margin:auto;">'
        
        # Generate Segitiga Atap Piramida
        for i in range(n_hows - 1):
            html_hoq += '<tr><td class="roof-blank" style="width:250px;"></td><td class="roof-blank" style="width:80px;"></td>'
            for j in range(n_hows):
                if j < (n_hows - 1 - i): html_hoq += '<td class="roof-blank"></td>'
                else:
                    row_target, col_target = hows_list[j], hows_list[n_hows - 1 - i]
                    val = st.session_state["roof_matrix"].at[row_target, col_target]
                    simbol, bg_color, text_color = "", "#1e293b", "#64748b"
                    if "Strong Positive" in val: simbol, bg_color, text_color = "++", "#1e3a8a", "#38bdf8"
                    elif "Positive" in val: simbol, bg_color, text_color = "+", "#14532d", "#4ade80"
                    elif "Strong Negative" in val: simbol, bg_color, text_color = "--", "#7f1d1d", "#f87171"
                    elif "Negative" in val: simbol, bg_color, text_color = "-", "#7c2d12", "#fb923c"
                    elif "No Correlation" in val: simbol, bg_color, text_color = "0", "#0f172a", "#475569"
                    html_hoq += f'<td class="roof-cell" style="background-color: {bg_color}; color: {text_color} !important;">{simbol}</td>'
            html_hoq += '</tr>'

        html_hoq += f'<tr><td colspan="{n_hows + 2}" style="background-color:#334155; padding:2px; border:none;"></td></tr>'

        # Kepala Tabel Utama
        html_hoq += '<tr><th class="hoq-th-corner">Customer Requirements (WHATs)</th><th class="hoq-importance-header">Importance</th>'
        for col in hows_list: html_hoq += f'<th class="hoq-th-hows">{col}</th>'
        html_hoq += '</tr>'
        
        # Isian Badan Menggunakan Simbol Jepang standard QFD (◎, ○, △)
        for idx, row_name in enumerate(whats_list):
            imp_val = weights[idx]
            html_hoq += f'<tr><td class="hoq-td-whats">{row_name}</td><td class="hoq-importance">{int(imp_val)}</td>'
            for col_name in hows_list:
                score_val = st.session_state["rel_matrix"].at[row_name, col_name]
                bg_cell = 'style="background-color: #0f172a; color: #64748b;"'
                simbol_hub = ""
                if score_val == 9: simbol_hub, bg_cell = "◎", 'style="background-color: #1e3a8a; color: #38bdf8; font-size: 18px; font-weight: bold;"'
                elif score_val == 3: simbol_hub, bg_cell = "○", 'style="background-color: #1e293b; color: #4ade80; font-size: 18px; font-weight: bold;"'
                elif score_val == 1: simbol_hub, bg_cell = "△", 'style="background-color: #1e293b; color: #fef08a; font-size: 18px; font-weight: bold;"'
                html_hoq += f'<td {bg_cell}>{simbol_hub}</td>'
            html_hoq += '</tr>'
            
        # Fondasi Bawah Rumah
        html_hoq += '<tr class="hoq-score-row"><td style="text-align: right; color: #38bdf8;">Weighted Importance (Score)</td><td style="color: #38bdf8;">-</td>'
        for score in abs_importance: html_hoq += f'<td style="background-color: #1e293b; color: #38bdf8 !important;">{int(score)}</td>'
        html_hoq += '</tr><tr class="hoq-weight-row"><td style="text-align: right; color: #2dd4bf;">Relative Importance (%)</td><td style="color: #2dd4bf;">-</td>'
        for weight in rel_importance: html_hoq += f'<td style="background-color: #1e293b; color: #2dd4bf !important;">{weight.round(1)}%</td>'
        html_hoq += '</tr></table></div>'
        
        st.markdown(html_hoq, unsafe_allow_html=True)
        
    except Exception as e:
        st.error("Silakan pastikan semua data input diisi dengan benar.")