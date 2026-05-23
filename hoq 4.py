import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SETTING HALAMAN
st.set_page_config(page_title="Digital HoQ - UKM Tahu", layout="wide")

st.markdown("""
    <style>
    .main-header { font-size: 28px; font-weight: bold; color: #1E3A8A; margin-bottom: 10px; }
    .sub-header { font-size: 18px; color: #64748b; margin-bottom: 20px; }
    .section-box { padding: 20px; border-radius: 10px; background-color: #f8fafc; border: 1px solid #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-header">🏠 Digital House of Quality (HoQ)</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Optimalisasi Spesifikasi Teknis berdasarkan Voice of Customer (UKM Tahu Endang)</p>', unsafe_allow_html=True)

# 2. INISIALISASI DATA (Default Value ditaruh di session_state yang berbeda agar tidak tabrakan saat diapus)
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
    # Menggunakan ed_whats sebagai penampung permanen, tombol hapus (bila baris dicentang lalu tekan del) sekarang akan bekerja
    whats_data = st.data_editor(
    st.session_state.df_whats,
    num_rows="dynamic",
    use_container_width=True,
    key="ed_whats",
    column_config={
        "Importance (1-5)": st.column_config.NumberColumn(
            "Importance (1-5)",
            min_value=1,
            max_value=5,
            step=1
        )
    }
    )

# TAB 2: Input HOWs
with t2:
    st.subheader("Masukkan Spesifikasi Teknis (HOWs)")
    st.caption("Pilih arah spesifikasi teknis: Max (maksimum), Min (minimum), atau Target (target).")
    
    # Mengedit data HOWs dengan konfigurasi dropdown pada kolom Direction
    hows_data = st.data_editor(
        st.session_state.df_hows, 
        num_rows="dynamic", 
        use_container_width=True, 
        column_config={
            "Direction": st.column_config.SelectboxColumn(
                "Direction",
                help="Arah optimasi spesifikasi teknis",
                options=["Max", "Min", "Target"],
                required=True
            )
        },
        key="ed_hows"
    )

# Mengambil list terbaru dari data_editor secara langsung (bukan dari session state lama)
whats_list = [x for x in whats_data["Customer Requirement (WHATs)"].tolist() if pd.notna(x) and x != ""]
hows_list = [x for x in hows_data["Technical Requirement (HOWs)"].tolist() if pd.notna(x) and x != ""]

# TAB 3 (Correlation - The Roof)
with t3:
    st.subheader("Matriks Korelasi Atap (HOWs vs HOWs)")
    st.caption("Pilih nilai korelasi: 9 (Kuat), 3 (Sedang), 1 (Lemah), atau 0/Kosong.")
    
    # Buat dataframe kosongan baru sesuai jumlah HOWs yang aktif saat ini
    # Gunakan nilai default 0 agar sesuai dengan pilihan dropdown
    roof_df = pd.DataFrame(0, index=hows_list, columns=hows_list)
    
    # Membuat konfigurasi dropdown (0, 1, 3, 9) otomatis untuk SEMUA kolom teknis
    roof_column_config = {
        col: st.column_config.SelectboxColumn(
            col,
            options=[0, 1, 3, 9],
            required=True
        )
        for col in hows_list
    }
    
    # Mengedit korelasi atap dengan konfigurasi dropdown
    roof_data = st.data_editor(
        roof_df, 
        use_container_width=True, 
        column_config=roof_column_config,
        key="ed_roof"
    )

# TAB 4 (Relationship Matrix)
with t4:
    st.subheader("Matriks Hubungan (WHATs vs HOWs)")
    st.caption("Pilih nilai hubungan: 9 (Kuat), 3 (Sedang), 1 (Lemah), atau 0 jika tidak berhubungan.")
    
    # Buat dataframe kosongan baru sesuai WHATs dan HOWs yang aktif
    rel_df = pd.DataFrame(0, index=whats_list, columns=hows_list)
    
    # Membuat konfigurasi dropdown (0, 1, 3, 9) otomatis untuk SEMUA kolom teknis
    rel_column_config = {
        col: st.column_config.SelectboxColumn(
            col,
            options=[0, 1, 3, 9],
            required=True
        )
        for col in hows_list
    }
    
    # Mengedit matriks hubungan dengan konfigurasi dropdown
    rel_data = st.data_editor(
        rel_df, 
        use_container_width=True, 
        column_config=rel_column_config,
        key="ed_rel"
    )

--- TAB 5: THE FINAL HOUSE ---
with t5:
    try:
        # 1. Ambil nilai bobot Importance dari Tab 1 secara dinamis
        # Gunakan filter yang sama dengan whats_list agar baris kosong tidak ikut terhitung
        valid_whats_df = whats_data[whats_data["Customer Requirement (WHATs)"].notna() & (whats_data["Customer Requirement (WHATs)"] != "")]
        weights = valid_whats_df["Importance (1-5)"].values.astype(float)
        
        # 2. Ambil matriks nilai terbaru dari Tab 4
        matrix_values = rel_data.values.astype(float)
        
        # 3. Perhitungan Nilai Absolut & Relatif menggunakan Perkalian Matriks (Dot Product)
        # Langkah ini mengalikan bobot Importance dengan skor hubungan (9, 3, 1, 0)
        abs_importance = weights @ matrix_values
        total = abs_importance.sum()
        rel_importance = (abs_importance / total * 100) if total > 0 else abs_importance * 0

        # --- LAYOUT RUMAH ---
        
        # 1. ATAP (Correlation)
        st.info("🛖 **Bagian Atap:** Korelasi Antar Persyaratan Teknis (Trade-offs)")
        st.dataframe(roof_data, use_container_width=True)

        st.write("")

        # 2. BADAN RUMAH (Relationship)
        st.success("🏢 **Bagian Utama:** Hubungan WHATs vs HOWs")
        col_voc, col_mat = st.columns([1, 2.5])
        with col_voc:
            st.write("**Customer Requirements**")
            # Menampilkan data WHATs terbaru yang diinput dari dashboard
            st.dataframe(valid_whats_df, hide_index=True, use_container_width=True)
        with col_mat:
            st.write("**Relationship Matrix (Scores)**")
            # Menampilkan matriks relasi dropdown terbaru
            st.dataframe(rel_data, use_container_width=True)

        st.write("")

        # 3. FONDASI (Scores & Pareto)
        st.warning("⚓ **Bagian Fondasi:** Prioritas Spesifikasi Teknis")
        
        res_df = pd.DataFrame({
            "Requirement": hows_list,
            "Score": abs_importance,
            "Weight %": rel_importance.round(1)
        }).sort_values(by="Score", ascending=False)

        f1, f2 = st.columns([1, 1.5])
        with f1:
            st.write("**Peringkat Prioritas**")
            st.dataframe(res_df, hide_index=True, use_container_width=True)
        with f2:
            fig = px.bar(res_df, x="Requirement", y="Score", text="Weight %", 
                         color="Score", color_continuous_scale="Viridis")
            fig.update_layout(height=300, margin=dict(t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        # Jika terjadi error saat user sedang mengetik atau menghapus data di dashboard
        st.error("Silakan pastikan semua data di tab sebelumnya sudah terisi dengan benar!")