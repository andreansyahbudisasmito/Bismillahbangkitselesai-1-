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

# Penyewaan Harian
if selected_section == "Penyewaan Harian":
    st.subheader("Penyewaan Sepeda Berdasarkan Hari")

    # Input for day, month, temperature, and humidity
    selected_day = st.number_input("Masukkan Hari (1-31):", min_value=1, max_value=31)
    selected_month = st.number_input("Masukkan Bulan (1-12):", min_value=1, max_value=12)
    selected_temp = st.number_input("Masukkan Suhu (Celsius):")
    selected_hum = st.number_input("Masukkan Kelembaban (%):")

    # Filter data for the specific day and month
    filtered_data = bike_data[(bike_data["dteday"].str.contains(f"-{selected_month:02d}-{selected_day:02d}")) &
                               (bike_data["temp"] >= selected_temp - 5) & 
                               (bike_data["temp"] <= selected_temp + 5) & 
                               (bike_data["hum"] >= selected_hum - 10) & 
                               (bike_data["hum"] <= selected_hum + 10)]

    # Average rentals for the selected day and month
    if not filtered_data.empty:
        avg_rentals = filtered_data["cnt"].mean()
        st.write(f"**Rata-rata Penyewaan di Hari {selected_day} Bulan {selected_month}:** {avg_rentals:.2f}")

        # Line plot of daily rentals
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.lineplot(x="dteday", y="cnt", data=filtered_data, marker="o", palette="plasma")
        ax.set_title(f"Penyewaan Harian untuk Suhu {selected_temp}°C dan Kelembaban {selected_hum}%", fontsize=14)
        ax.set_xlabel("Tanggal")
        ax.set_ylabel("Jumlah Penyewaan")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.write("Tidak ada data yang sesuai dengan parameter yang diberikan.")

# Footer
st.sidebar.caption("Dashboard Penyewaan Sepeda oleh Andreansyah Budi")
st.caption("Data dari Capital Bikeshare - Washington D.C.")
