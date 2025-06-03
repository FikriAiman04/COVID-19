import streamlit as st

# Data model Perodua & gambar (dari laman rasmi)
perodua_data = {
    "Axia": "https://upload.wikimedia.org/wikipedia/commons/8/8b/Perodua_Axia_1.0_SE_(2014)_in_JB_Malaysia_(cropped).jpg",
    "Bezza": "https://upload.wikimedia.org/wikipedia/commons/4/42/Perodua_Bezza_1.3_Advance_(2016)_in_JB_Malaysia.jpg",
    "Myvi": "https://upload.wikimedia.org/wikipedia/commons/a/a1/Perodua_Myvi_1.5_AV_facelift_2021.jpg",
    "Ativa": "https://upload.wikimedia.org/wikipedia/commons/e/e2/2021_Perodua_Ativa_1.0_AV.jpg",
    "Alza": "https://upload.wikimedia.org/wikipedia/commons/8/8b/2022_Perodua_Alza_1.5_AV.jpg",
    "Aruz": "https://upload.wikimedia.org/wikipedia/commons/9/91/2019_Perodua_Aruz_1.5_AV.jpg",
}


# Tetapan Streamlit
st.set_page_config(page_title="Perodua Car Search", page_icon="🚗")
st.title("🚗 Carian Model Kereta Perodua Malaysia")
st.markdown("[Laman rasmi Perodua Malaysia](https://www.perodua.com.my/our-models/choose-model.html)")

# Kotak carian
query = st.text_input("🔍 Cari model (contoh: Axia, SUV, Alza):")

# Papar hasil carian
if query:
    matches = {model: img for model, img in perodua_data.items() if query.lower() in model.lower()}

    if matches:
        st.success(f"{len(matches)} model dijumpai:")
        for model, img_url in matches.items():
            st.subheader(model)
            st.image(img_url, width=400)
    else:
        st.warning("❌ Tiada model ditemui.")
else:
    st.info("Sila masukkan nama model untuk mula mencari.")
