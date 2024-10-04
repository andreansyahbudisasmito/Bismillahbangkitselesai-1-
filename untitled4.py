# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
bike_data = pd.read_csv("day.csv")

# Map weather and season data
weather = {
    1: "Clear",
    2: "Mist",
    3: "Light Rain",
    4: "Heavy Rain"
}

season = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

bike_data["weather"] = bike_data["weathersit"].map(weather)
bike_data["season"] = bike_data["season"].map(season)

# Sidebar navigation
st.sidebar.title("Analisis Penyewaan Sepeda")
sections = ["Overview", "Penyewaan per Musim", "Penyewaan per Bulan", "Penyewaan Harian"]
selected_section = st.sidebar.radio("Pilih Analisis", sections)

# Overview section
if selected_section == "Overview":
    st.header("Overview Data Penyewaan Sepeda")
    st.write("Dashboard ini memberikan wawasan tentang penyewaan sepeda berdasarkan kondisi cuaca, musim, hari, dan jam.")
    st.dataframe(bike_data)

# Penyewaan per Musim
if selected_section == "Penyewaan per Musim":
    st.subheader("Penyewaan Sepeda Berdasarkan Musim")

    # Select season
    selected_season = st.selectbox("Pilih Musim:", bike_data['season'].unique())

    # Filter data by selected season
    filtered_data = bike_data[bike_data["season"] == selected_season]

    # Average rentals by season
    avg_rentals = filtered_data["cnt"].mean()
    st.write(f"**Rata-rata Penyewaan di Musim {selected_season}:** {avg_rentals:.2f}")

    # Bar plot of rentals by season
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x="season", y="cnt", data=bike_data, palette="viridis", ax=ax)
    ax.set_title("Penyewaan Sepeda per Musim", fontsize=14)
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)

# Penyewaan per Bulan
if selected_section == "Penyewaan per Bulan":
    st.subheader("Penyewaan Sepeda Berdasarkan Bulan")
    st.write("Silahkan pilih grafik yang ingin anda munculkan berdasarkan variabel berikut:")
    st.markdown('<span style="color:red">Note: ketika plot tidak muncul atau muncul sebagian berarti tidak ada data pada variabel yang anda masukan</span>', unsafe_allow_html=True)

    # Select month
    selected_month = st.selectbox("Pilih Bulan:", bike_data['mnth'].unique(), format_func=lambda x: ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"][x-1])

    # Filter data by selected month
    filtered_data = bike_data[bike_data["mnth"] == selected_month]

    # Average rentals by month
    avg_rentals = filtered_data["cnt"].mean()
    st.write(f"**Rata-rata Penyewaan di Bulan {selected_month}:** {avg_rentals:.2f}")

    # Line plot of rentals by month
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.lineplot(x="dteday", y="cnt", data=filtered_data, marker="o", palette="coolwarm")
    ax.set_title(f"Penyewaan Sepeda di Bulan {selected_month}", fontsize=14)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Penyewaan")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Penyewaan Harian Berdasarkan Hari, Bulan, dan Cuaca
if selected_section == "Penyewaan Harian":
    st.subheader("Penyewaan Harian Berdasarkan Hari, Bulan, dan Cuaca")

    # Input hari dan bulan dari pengguna
    selected_day = st.selectbox("Pilih Hari:", bike_data['weekday'].unique(), format_func=lambda x: ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"][x])
    selected_month = st.selectbox("Pilih Bulan:", bike_data['mnth'].unique(), format_func=lambda x: ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"][x-1])

    # Input cuaca dari pengguna
    selected_weather = st.selectbox("Pilih Cuaca:", ["Panas", "Normal", "Dingin"])

    # Filter data berdasarkan hari, bulan, dan cuaca
    if selected_weather == "Panas":
        filtered_data = bike_data[(bike_data['weekday'] == selected_day) & (bike_data['mnth'] == selected_month) & (bike_data['temp'] > 0.3)]
    elif selected_weather == "Dingin":
        filtered_data = bike_data[(bike_data['weekday'] == selected_day) & (bike_data['mnth'] == selected_month) & (bike_data['temp'] < 0.1)]
    else:
        filtered_data = bike_data[(bike_data['weekday'] == selected_day) & (bike_data['mnth'] == selected_month) & (bike_data['temp'].between(0.1, 0.3))]

    # Cek apakah ada data yang sesuai
    if not filtered_data.empty:
        # Rata-rata penyewaan harian berdasarkan filter
        avg_rentals = filtered_data["cnt"].mean()
        st.write(f"**Rata-rata Penyewaan pada {selected_day}, Bulan {selected_month} dengan Cuaca {selected_weather}:** {avg_rentals:.2f}")

        # Plot grafik penyewaan harian
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(x="dteday", y="cnt", data=filtered_data, palette="coolwarm", ax=ax)
        ax.set_title(f"Penyewaan Sepeda pada Hari {selected_day}, Bulan {selected_month} dengan Cuaca {selected_weather}", fontsize=14)
        ax.set_xlabel("Tanggal")
        ax.set_ylabel("Jumlah Penyewaan")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.write("Tidak ada data yang ditemukan untuk input yang diberikan.")

# Footer
st.sidebar.caption("Dashboard Penyewaan Sepeda oleh Andreansyah Budi")
st.caption("Data dari Capital Bikeshare - Washington D.C.")
