import streamlit as st

st.set_page_config(page_title="Mechanica Schema Analyzer", layout="wide")
st.title("Mechanica Schema Analyzer")
st.write("Upload een foto van je mechanicaschema. In deze eerste versie kun je de afbeelding tonen en alvast de basis klaarzetten voor analyse.")

uploaded = st.file_uploader("Upload een afbeelding", type=["png", "jpg", "jpeg", "webp"])

col1, col2 = st.columns(2)
with col1:
    if uploaded:
        st.image(uploaded, caption="Geüploade afbeelding", use_container_width=True)
    else:
        st.info("Nog geen afbeelding geüpload.")

with col2:
    st.subheader("Invoer")
    st.number_input("Aantal steunpunten", min_value=0, value=2, step=1)
    st.number_input("Aantal puntlasten", min_value=0, value=0, step=1)
    st.number_input("Aantal verdeelde lasten", min_value=0, value=0, step=1)
    st.text_area("Opmerking", value="Hier kun je later lasten, afstanden en opleggingen invoeren.", height=150)

st.subheader("Resultaten")
st.info("Hier komen later de normaalkrachtlijn, dwarskrachtenlijn en momentenlijn.")
