import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Data Statistik COVID-19", page_icon="🦠")

st.title("Papan Pemuka Global COVID-19")

@st.cache_data(ttl=3600)
def load_data():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

negara_list = df['location'].unique()

try:
    default_idx = list(negara_list).index("World")
except ValueError:
    default_idx = 0

negara = st.selectbox("Pilih negara", negara_list, index=default_idx)

df_negara = df[df['location'] == negara].copy()
df_negara['date'] = pd.to_datetime(df_negara['date'])

# Sidebar untuk pilih julat tarikh
tarikh_min = df_negara['date'].min()
tarikh_max = df_negara['date'].max()
julattarikh = st.sidebar.date_input("Pilih julat tarikh", [tarikh_min, tarikh_max], min_value=tarikh_min, max_value=tarikh_max)

tarikh_mula, tarikh_akhir = julattarikh
df_negara = df_negara[(df_negara['date'] >= pd.to_datetime(tarikh_mula)) & (df_negara['date'] <= pd.to_datetime(tarikh_akhir))]

st.subheader(f"Statistik COVID-19 di {negara}")

df_negara['total_cases'] = df_negara['total_cases'].fillna(0)
df_negara['total_deaths'] = df_negara['total_deaths'].fillna(0)
df_negara['new_cases'] = df_negara['new_cases'].fillna(0)

terkini = df_negara.iloc[-1]

st.write(f"**Setakat {terkini['date'].date()}**")
st.write(f"Jumlah kes: {int(terkini['total_cases']):,}")
st.write(f"Jumlah kematian: {int(terkini['total_deaths']):,}")

# Kira purata 7 hari kes baru
df_negara['purata_7hari_kes_baru'] = df_negara['new_cases'].rolling(window=7).mean().fillna(0)

# Carta Kes Baru Harian & Purata 7 Hari
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(df_negara['date'], df_negara['new_cases'], color='lightblue', label='Kes Baru Harian')
ax.plot(df_negara['date'], df_negara['purata_7hari_kes_baru'], color='red', linewidth=2, label='Purata 7 Hari')
ax.set_xlabel("Tarikh")
ax.set_ylabel("Kes Baru")
ax.set_title(f"Kes COVID-19 Harian di {negara}")
ax.legend()
st.pyplot(fig)

# Carta jumlah kes kumulatif dan kematian kumulatif
fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(df_negara['date'], df_negara['total_cases'], label='Jumlah Kes Kumulatif', color='blue')
ax2.plot(df_negara['date'], df_negara['total_deaths'], label='Jumlah Kematian Kumulatif', color='black')
ax2.set_xlabel("Tarikh")
ax2.set_ylabel("Jumlah")
ax2.set_title(f"Kes & Kematian COVID-19 Kumulatif di {negara}")
ax2.legend()
st.pyplot(fig2)
