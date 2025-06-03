import streamlit as st

# Data model Perodua & gambar (dari laman rasmi)
perodua_data = {
    "Axia": "https://www.perodua.com.my/images/car-model/axia.png",
    "Bezza": "https://www.perodua.com.my/images/car-model/bezza.png",
    "Myvi": "https://www.perodua.com.my/images/car-model/myvi.png",
    "Ativa": "https://www.perodua.com.my/images/car-model/ativa.png",
    "Alza": "https://www.perodua.com.my/images/car-model/alza.png",
    "Aruz": "https://www.perodua.com.my/images/car-model/aruz.png",
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
