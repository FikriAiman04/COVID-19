import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

st.set_page_config(page_title="COVID-19 Dashboard", page_icon="🦠")

st.title("COVID-19 Global Dashboard")

@st.cache_data(ttl=3600)
def load_data():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# Pilih negara
countries = df['location'].unique()
country = st.selectbox("Pilih negara", countries, index=list(countries).index("World"))

df_country = df[df['location'] == country]

st.write(f"### Statistik COVID-19 di {country}")

# Statistik terkini
latest = df_country.iloc[-1]
st.write(f"**Tanggal:** {latest['date']}")
st.write(f"Total kasus: {int(latest['total_cases']):,}")
st.write(f"Total kematian: {int(latest['total_deaths']):,}")
st.write(f"Total sembuh (recovered) tidak tersedia di dataset ini.")

# Visualisasi kasus harian
fig, ax = plt.subplots()
ax.plot(pd.to_datetime(df_country['date']), df_country['new_cases'], label='Kasus Baru')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Kasus Baru")
ax.set_title(f"Kasus COVID-19 Harian di {country}")
ax.legend()
st.pyplot(fig)
