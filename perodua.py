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

st.subheader(f"Statistik COVID-19 di {country}")


fig, ax = plt.subplots()
ax.plot(df_country['date'], df_country['new_cases'].fillna(0), label="Kasus Baru")

df_country['total_cases'] = df_country['total_cases'].fillna(0)
df_country['total_deaths'] = df_country['total_deaths'].fillna(0)

latest = df_country.iloc[-1]

st.write(f"Total kasus: {int(latest['total_cases']):,}")
st.write(f"Total kematian: {int(latest['total_deaths']):,}")
