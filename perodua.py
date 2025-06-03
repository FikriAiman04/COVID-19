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
country = st.selectbox("Pilih negara", countries, index=list(countries).tolist().index("World"))

df_country = df[df['location'] == country].copy()
df_country['date'] = pd.to_datetime(df_country['date'])

st.subheader(f"Statistik COVID-19 di {country}")

latest = df_country.iloc[-1]

st.write(f"**Tanggal:** {latest['date'].date()}")
st.write(f"Total kasus: {int(latest['total_cases'] or 0):,}")
st.write(f"Total kematian: {int(latest['total_deaths'] or 0):,}")

fig, ax = plt.subplots()
ax.plot(df_country['date'], df_country['new_cases'].fillna(0), label="Kasus Baru")

