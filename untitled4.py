import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
bike_data = pd.read_csv("day.csv")

# Memetakan data cuaca dan musim
weather = {
    1: "Cerah",
    2: "Kabut",
    3: "Hujan Ringan",
    4: "Hujan Berat"
}

season = {
    1: "Musim Semi",
    2: "Musim Panas",
    3: "Musim Gugur",
    4: "Musim Dingin"
}

# Menambahkan kolom baru untuk cuaca dan musim
bike_data["weather"] = bike_data["weathersit"].map(weather)
bike_data["season"] = bike_data["season"].map(season)

# Sidebar navigasi
st.sidebar.title("Analisis Penyewaan Sepeda")
sections = ["Overview", "Perbandingan Penyewaan", "Penyewaan per Jam dan Musim", "Analisis Penyewaan Interaktif"]
selected_section = st.sidebar.radio("Pilih Analisis", sections)

# Bagian Overview
if selected_section == "Overview":
    st.header("Sekilas Tentang Data Penyewaan Sepeda")
    st.write("Dashboard ini memberikan wawasan tentang penyewaan sepeda berdasarkan cuaca, musim, hari, dan jam.")
    st.dataframe(bike_data)

# Perbandingan Penyewaan
if selected_section == "Perbandingan Penyewaan":
    st.subheader("Bandingin Penyewaan Kamu dengan Rata-rata")

    # Input dari pengguna untuk penyewaan mereka
    user_rentals = st.number_input("Masukkan Total Penyewaan Kamu:", min_value=0, step=1)

    # Rata-rata penyewaan berdasarkan kondisi cuaca
    avg_rentals_by_weather = bike_data.groupby('weather')['cnt'].mean().reset_index()

    # Buat grafik batang untuk bandingin penyewaan pengguna dengan rata-rata
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="weather", y="cnt", data=avg_rentals_by_weather, palette="coolwarm", ax=ax)

    # Tambahin penyewaan pengguna sebagai garis di grafik batang
    ax.axhline(user_rentals, color='red', linestyle='--', label='Penyewaan Kamu')
    ax.set_title("Rata-rata Penyewaan Berdasarkan Kondisi Cuaca", fontsize=16)
    ax.set_ylabel("Rata-rata Jumlah Penyewaan")
    ax.legend()
    st.pyplot(fig)

# Penyewaan per Jam dan Musim
if selected_section == "Penyewaan per Jam dan Musim":
    st.subheader("Penyewaan Sepeda per Jam dan Musim")

    # Pilih jam
    selected_hour = st.slider("Pilih Jam (0-23):", 0, 23, 12)

    # Filter data untuk jam yang dipilih
    rentals_by_hour = bike_data[bike_data['hr'] == selected_hour]
    
    # Memastikan ada data untuk jam yang dipilih
    if not rentals_by_hour.empty:
        avg_rentals_by_season = rentals_by_hour.groupby('season')['cnt'].mean().reset_index()

        # Tampilkan rata-rata penyewaan di jam yang dipilih
        st.write(f"**Rata-rata Penyewaan di {selected_hour}:00:** {rentals_by_hour['cnt'].mean():.2f}")

        # Grafik batang penyewaan di jam yang dipilih
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x="season", y="cnt", data=rentals_by_hour, palette="Set2", ax=ax)
        ax.set_title(f"Penyewaan di {selected_hour}:00 per Musim", fontsize=16)
        ax.set_ylabel("Jumlah Penyewaan")
        st.pyplot(fig)
    else:
        st.write("Tidak ada data untuk jam yang dipilih.")

# Analisis Penyewaan Interaktif
if selected_section == "Analisis Penyewaan Interaktif":
    st.subheader("Analisis Penyewaan yang Interaktif")

    # Form untuk memilih kondisi analisis
    with st.form(key='interactive_analysis_form'):
        st.write("Pilih Kriteria untuk Analisis:")
        
        # Pilih tahun dan bulan
        selected_year = st.selectbox("Pilih Tahun:", bike_data['yr'].unique())
        selected_month = st.selectbox("Pilih Bulan:", bike_data['mnth'].unique())
        
        # Pilih kondisi cuaca
        selected_weather = st.selectbox("Pilih Kondisi Cuaca:", bike_data['weather'].unique())
        
        # Tombol submit
        submit_button = st.form_submit_button(label='Lihat Analisis')

    if submit_button:
        # Filter data berdasarkan input pengguna
        filtered_data = bike_data[
            (bike_data['yr'] == selected_year) &
            (bike_data['mnth'] == selected_month) &
            (bike_data['weather'] == selected_weather)
        ]

        # Menampilkan rata-rata penyewaan
        if not filtered_data.empty:
            avg_rentals = filtered_data['cnt'].mean()
            st.write(f"**Rata-rata Penyewaan untuk {selected_weather} pada bulan {selected_month} tahun {selected_year}:** {avg_rentals:.2f}")

            # Tampilkan data penyewaan yang detail
            st.write("Data Penyewaan yang Detail:")
            st.dataframe(filtered_data[['dteday', 'cnt']])

            # Visualisasi: Histogram penyewaan
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(filtered_data['cnt'], bins=20, kde=True, ax=ax, color='purple')
            ax.set_title(f"Distribusi Penyewaan untuk {selected_weather} pada bulan {selected_month} tahun {selected_year}", fontsize=16)
            ax.set_xlabel("Jumlah Penyewaan")
            st.pyplot(fig)
        else:
            st.write("Tidak ada data untuk kombinasi yang dipilih.")

# Footer
st.sidebar.caption("Dashboard Penyewaan Sepeda oleh Andreansyah Budi")
st.caption("Data dari Capital Bikeshare - Washington D.C.")
