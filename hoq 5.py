import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SETTING HALAMAN
st.set_page_config(page_title="Digital HoQ - UKM Tahu", layout="wide")

st.markdown("""
    <style>
    .main-header { font-size: 28px; font-weight: bold; color: #1E3A8A; margin-bottom: 10px; }
    .sub-header { font-size: 18px; color: #64748b; margin-bottom: 20px; }
    [data-testid="stMetricValue"] { font-size: 24px; color: #1E3A8A; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-header">🏠 Digital House of Quality (HoQ)</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Optimalisasi Spesifikasi Teknis berdasarkan Voice of Customer (UKM Tahu Endang)</p>', unsafe_allow_html=True)

# 2. INISIALISASI DATA (Session State Utama agar Sinkron Antar-Tab)
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

# Filter data bersih agar baris kosong tidak merusak matriks
whats_list = [x for x in st.session_state.df_whats["Customer Requirement (WHATs)"].tolist() if pd.notna(x) and x != ""]
hows_list = [x for x in st.session_state.df_hows["Technical Requirement (HOWs)"].tolist() if pd.notna(x) and x != ""]

# TAB 3 (Correlation - The Roof)
with t3:
    st.subheader("Matriks Korelasi Atap (HOWs vs HOWs)")
    st.caption("Tentukan trade-off antar spesifikasi teknis.")
    
    if 'roof_matrix' not in st.session_state or list(st.session_state.roof_matrix.columns) != hows_list:
        st.session_state.roof_matrix = pd.DataFrame("No Correlation (0)", index=hows_list, columns=hows_list)
    
    roof_column_config = {
        col: st.column_config.SelectboxColumn(col, options=["Strong Positive (++)", "Positive (+)", "No Correlation (0)", "Negative (-)", "Strong Negative (--)"], required=True)
        for col in hows_list
    }
    
    st.session_state.roof_matrix = st.data_editor(
        st.session_state.roof_matrix, 
        use_container_width=True, 
        column_config=roof_column_config,
        key="ed_roof"
    )

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
    
    st.session_state.rel_matrix = st.data_editor(
        st.session_state.rel_matrix, 
        use_container_width=True, 
        column_config=rel_column_config,
        key="ed_rel"
    )

# --- TAB 5: THE FINAL HOUSE (Bento Box & Perhitungan Otomatis) ---
with t5:
    try:
        # Mengambil data valid untuk perhitungan matematika
        valid_whats = st.session_state.df_whats[st.session_state.df_whats["Customer Requirement (WHATs)"].isin(whats_list)]
        weights = valid_whats["Importance (1-5)"].values.astype(float)
        matrix_values = st.session_state.rel_matrix.loc[whats_list, hows_list].values.astype(float)
        
        # Perhitungan Nilai Absolut & Relatif
        abs_importance = weights @ matrix_values
        total = abs_importance.sum()
        rel_importance = (abs_importance / total * 100) if total > 0 else abs_importance * 0

        # DataFrame Hasil Akhir
        res_df = pd.DataFrame({
            "Requirement": hows_list,
            "Score": abs_importance,
            "Weight %": rel_importance.round(1)
        }).sort_values(by="Score", ascending=False)

        # 1. HIGHLIGHTS METRICS (Konsep UI Bento Box)
        st.write("### Rekomendasi Prioritas Utama")
        if len(res_df) >= 3:
            m1, m2, m3 = st.columns(3)
            m1.metric(label="🥇 Prioritas 1", value=res_df.iloc[0]["Requirement"], delta=f"{res_df.iloc[0]['Weight %']}% Weight")
            m2.metric(label="🥈 Prioritas 2", value=res_df.iloc[1]["Requirement"], delta=f"{res_df.iloc[1]['Weight %']}% Weight")
            m3.metric(label="🥉 Prioritas 3", value=res_df.iloc[2]["Requirement"], delta=f"{res_df.iloc[2]['Weight %']}% Weight")
        
        st.write("---")

        # Layout Utama Berdampingan (Matriks vs Chart)
        col_left, col_right = st.columns([1.2, 1.3])
        
        with col_left:
            st.success("🏢 **Matriks Utama (WHATs vs HOWs)**")
            st.dataframe(st.session_state.rel_matrix.loc[whats_list, hows_list], use_container_width=True)
            
            st.info("🛖 **Matriks Korelasi Atap**")
            st.dataframe(st.session_state.roof_matrix.loc[hows_list, hows_list], use_container_width=True)
            
        with col_right:
            st.warning("⚓ **Grafik Kontribusi Prioritas Teknis**")
            fig = px.bar(res_df, x="Score", y="Requirement", orientation='h', text="Weight %",
                         color="Score", color_continuous_scale="Blugrn")
            fig.update_layout(height=350, margin=dict(t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)
            
            st.write("**Tabel Peringkat**")
            st.dataframe(res_df, hide_index=True, use_container_width=True)

    except Exception as e:
        st.error("Silakan lengkapi atau periksa kembali data inputan di tab sebelumnya!")