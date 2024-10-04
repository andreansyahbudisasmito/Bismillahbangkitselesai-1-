import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data dari file CSV
bike_data = pd.read_csv("day.csv")

# Mengubah data season jadi lebih gampang dibaca
season = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

bike_data["season"] = bike_data["season"].map(season)

# Navigasi sidebar buat milih analisis apa yang mau dilihat
st.sidebar.title("Analisis Penyewaan Sepeda")
sections = ["Overview", "Penyewaan Interaktif", "Analisis Penyewaan Harian"]
selected_section = st.sidebar.radio("Pilih Analisis", sections)

# Bagian overview untuk kasih gambaran umum soal data
if selected_section == "Overview":
    st.header("Gambaran Umum Data Penyewaan Sepeda")
    st.write("Ini adalah dashboard yang kasih insight soal penyewaan sepeda berdasarkan cuaca, musim, hari, dan jam.")
    st.dataframe(bike_data)

# Bagian interaktif, pengguna bisa pilih cuaca atau musim dan lihat penyewaannya
if selected_section == "Penyewaan Interaktif":
    st.header("Analisis Penyewaan Sepeda Berdasarkan Cuaca dan Musim")

    # Input buat pilih musim atau cuaca yang mau dianalisis
    selected_filter = st.radio("Pilih Filter:", ["Cuaca", "Musim"])

    if selected_filter == "Cuaca":
        selected_weather = st.selectbox("Pilih Cuaca:", ["Clear", "Mist", "Light Rain", "Heavy Rain"])
        filtered_data = bike_data[bike_data["weather"] == selected_weather]

        # Visualisasi penyewaan berdasarkan cuaca yang dipilih
        if not filtered_data.empty:
            st.write(f"Penyewaan Sepeda Saat Cuaca {selected_weather}")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x="dteday", y="cnt", data=filtered_data, ax=ax, palette="coolwarm")
            ax.set_title(f"Penyewaan Sepeda Berdasarkan Cuaca {selected_weather}", fontsize=14)
            ax.set_ylabel("Jumlah Penyewaan")
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.warning("Data tidak ditemukan untuk cuaca yang dipilih.")

    elif selected_filter == "Musim":
        selected_season = st.selectbox("Pilih Musim:", bike_data['season'].unique())
        filtered_data = bike_data[bike_data["season"] == selected_season]

        # Visualisasi penyewaan berdasarkan musim yang dipilih
        if not filtered_data.empty:
            st.write(f"Penyewaan Sepeda di Musim {selected_season}")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.lineplot(x="dteday", y="cnt", data=filtered_data, marker="o", ax=ax)
            ax.set_title(f"Penyewaan Sepeda di Musim {selected_season}", fontsize=14)
            ax.set_ylabel("Jumlah Penyewaan")
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.warning("Data tidak ditemukan untuk musim yang dipilih.")

# Bagian buat analisis harian, pengguna bisa input hari, bulan, suhu, kelembaban
if selected_section == "Analisis Penyewaan Harian":
    st.header("Analisis Penyewaan Harian")

    # Input untuk hari, bulan, suhu, dan kelembaban
    selected_day = st.number_input("Pilih Hari (1-31):", min_value=1, max_value=31, value=1)
    selected_month = st.number_input("Pilih Bulan (1-12):", min_value=1, max_value=12, value=1)
    avg_temp = st.number_input("Masukkan Suhu Rata-rata (°C):", min_value=-5.0, max_value=40.0, value=20.0)
    avg_humidity = st.number_input("Masukkan Kelembaban Rata-rata (%):", min_value=0.0, max_value=100.0, value=50.0)

    # Filter data berdasarkan hari, bulan, suhu dan kelembaban yang dipilih dengan toleransi
    filtered_data = bike_data[
        (bike_data["mnth"] == selected_month) &
        (bike_data["dteday"].str.split('-').str[2].astype(int) == selected_day) &
        (bike_data["temp"] >= (avg_temp - 1)) & (bike_data["temp"] <= (avg_temp + 1)) &
        (bike_data["hum"] >= (avg_humidity - 2)) & (bike_data["hum"] <= (avg_humidity + 2))
    ]

    # Cek apakah ada data yang cocok dengan filter, kalau ada tampilkan grafisnya
    if not filtered_data.empty:
        st.write(f"Hasil filter untuk Hari {selected_day}, Bulan {selected_month}, Suhu ~ {avg_temp}°C, Kelembaban ~ {avg_humidity}%:")

        # Visualisasi penyewaan harian
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x="dteday", y="cnt", data=filtered_data, palette="coolwarm", ax=ax)
        ax.set_title(f"Penyewaan Harian pada {selected_day}/{selected_month} dengan Suhu ~ {avg_temp}°C dan Kelembaban ~ {avg_humidity}%", fontsize=14)
        ax.set_ylabel("Jumlah Penyewaan")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("Data tidak ditemukan dengan kriteria yang dipilih. Coba sesuaikan nilai suhu atau kelembaban.")

# Footer kecil buat info
st.sidebar.caption("Dashboard Penyewaan Sepeda oleh Andreansyah Budi")
st.caption("Data dari Capital Bikeshare - Washington D.C.")
