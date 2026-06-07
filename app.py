import streamlit as st
from PIL import Image

st.set_page_config(page_title="Mechanica Schema Analyzer", layout="wide")
st.title("Mechanica Schema Analyzer")

uploaded = st.file_uploader("Upload een afbeelding", type=["png", "jpg", "jpeg", "webp"])

col1, col2 = st.columns(2)

with col1:
    if uploaded is not None:
        uploaded.seek(0)
        img = Image.open(uploaded)
        st.image(img, caption="Geüploade afbeelding", use_container_width=True)
    else:
        st.info("Upload een afbeelding om te beginnen.")

with col2:
    st.subheader("Invoer")
    steunpunten = st.number_input("Aantal steunpunten", min_value=0, value=2, step=1)
    puntlasten = st.number_input("Aantal puntlasten", min_value=0, value=0, step=1)
    verdeelde_lasten = st.number_input("Aantal verdeelde lasten", min_value=0, value=0, step=1)

    bereken = st.button("Toon resultaat")

    if bereken:
        st.success(f"Invoer ontvangen: {steunpunten} steunpunten, {puntlasten} puntlasten, {verdeelde_lasten} verdeelde lasten.")
        st.info("Hier komen later de normaalkrachtlijn, dwarskrachtenlijn en momentenlijn.")
