import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="COVID-19 Dashboard", page_icon="🦠")

st.title("COVID-19 Global Dashboard")

@st.cache_data(ttl=3600)
def load_data():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

countries = df['location'].unique()

try:
    default_idx = list(countries).index("World")
except ValueError:
    default_idx = 0

country = st.selectbox("Pilih negara", countries, index=default_idx)

df_country = df[df['location'] == country].copy()
df_country['date'] = pd.to_datetime(df_country['date'])

# Sidebar filter tanggal
min_date = df_country['date'].min()
max_date = df_country['date'].max()
date_range = st.sidebar.date_input("Pilih rentang tanggal", [min_date, max_date], min_value=min_date, max_value=max_date)

start_date, end_date = date_range
df_country = df_country[(df_country['date'] >= pd.to_datetime(start_date)) & (df_country['date'] <= pd.to_datetime(end_date))]

st.subheader(f"Statistik COVID-19 di {country}")

df_country['total_cases'] = df_country['total_cases'].fillna(0)
df_country['total_deaths'] = df_country['total_deaths'].fillna(0)
df_country['new_cases'] = df_country['new_cases'].fillna(0)

latest = df_country.iloc[-1]

st.write(f"**Per {latest['date'].date()}**")
st.write(f"Total kasus: {int(latest['total_cases']):,}")
st.write(f"Total kematian: {int(latest['total_deaths']):,}")

# Hitung rata-rata 7 hari untuk kasus baru
df_country['new_cases_7day_avg'] = df_country['new_cases'].rolling(window=7).mean().fillna(0)

# Grafik Kasus Baru harian dan rata-rata 7 hari
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(df_country['date'], df_country['new_cases'], color='lightblue', label='Kasus Baru Harian')
ax.plot(df_country['date'], df_country['new_cases_7day_avg'], color='red', linewidth=2, label='Rata-rata 7 Hari')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Kasus Baru")
ax.set_title(f"Kasus COVID-19 Harian di {country}")
ax.legend()
st.pyplot(fig)

# Grafik Total kasus kumulatif dan kematian kumulatif
fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(df_country['date'], df_country['total_cases'], label='Total Kasus Kumulatif', color='blue')
ax2.plot(df_country['date'], df_country['total_deaths'], label='Total Kematian Kumulatif', color='black')
ax2.set_xlabel("Tanggal")
ax2.set_ylabel("Jumlah")
ax2.set_title(f"Kasus & Kematian COVID-19 Kumulatif di {country}")
ax2.legend()
st.pyplot(fig2)
