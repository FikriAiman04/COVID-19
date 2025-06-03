import streamlit as st
import pandas as pd
import streamlit as st
import base64

def set_background_scaled(jpg_file, size="80%"):
    with open(jpg_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: {size};         /* Saiz gambar — ubah sini */
            background-repeat: no-repeat;
            background-position: center;
            background-attachment: fixed;
            color: white;
        }}

        /* Jadikan container & sidebar transparent */
        .block-container {{
            background-color: rgba(0, 0, 0, 0) !important;
        }}
        .css-18e3th9, .css-1d391kg {{
            background-color: rgba(0, 0, 0, 0) !important;
            backdrop-filter: none !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
    """
    <style>
    /* Tukar teks ke warna putih */
    .stApp {
        color: white;
    }

    /* Jadikan semua container utama & sidebar transparent */
    .block-container {
        background-color: rgba(0, 0, 0, 0) !important;
    }

    .css-18e3th9, .css-1d391kg {
        background-color: rgba(0, 0, 0, 0) !important;
        backdrop-filter: none !important;
    }

    header, footer {
        background-color: rgba(0, 0, 0, 0);
    }

    /* Buang kabur (blur) yang mungkin dipaksa oleh Streamlit default */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: none !important;
        z-index: -1;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .stApp {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Guna fungsi tu dengan nama fail gambar kamu
set_background_scaled("covid.jpg", size="80%")


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
df_negara['people_vaccinated'] = df_negara['people_vaccinated'].fillna(0)
df_negara['people_fully_vaccinated'] = df_negara['people_fully_vaccinated'].fillna(0)

terkini = df_negara.iloc[-1]

st.write(f"**Setakat {terkini['date'].date()}**")
st.write(f"Jumlah kes: {int(terkini['total_cases']):,}")
st.write(f"Jumlah kematian: {int(terkini['total_deaths']):,}")

# Kira kadar kematian dan kadar sembuh (%)
if terkini['total_cases'] > 0:
    kadar_kematian = (terkini['total_deaths'] / terkini['total_cases']) * 100
    kadar_sembuh = ((terkini['total_cases'] - terkini['total_deaths']) / terkini['total_cases']) * 100
else:
    kadar_kematian = 0
    kadar_sembuh = 0

st.write(f"Kadar kematian: {kadar_kematian:.2f}%")
st.write(f"Kadar sembuh (anggaran): {kadar_sembuh:.2f}%")

# Statistik vaksinasi
st.subheader("Statistik Vaksinasi")

st.write(f"Jumlah orang telah divaksin (sekurang-kurangnya satu dos): {int(terkini['people_vaccinated']):,}")
st.write(f"Jumlah orang lengkap divaksin: {int(terkini['people_fully_vaccinated']):,}")

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
