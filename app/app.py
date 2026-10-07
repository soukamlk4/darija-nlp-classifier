import streamlit as st
import requests

st.set_page_config(page_title="Darija Classifier", page_icon="🇲🇦")

st.title("🇲🇦 Classification de Textes en Darija")
st.markdown("Entrez un texte en Darija — arabe, latin ou Arabizi")

text = st.text_area("Texte à classifier", height=120,
                     placeholder="ex: wach had lwasfa zwina...")

if st.button("Classifier", type="primary"):
    if text.strip():
        with st.spinner("Analyse en cours..."):
            response = requests.post(
                "http://localhost:8000/predict",
                json={"text": text}
            )
            result = response.json()

        # Résultat principal
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Catégorie", result["prediction"])
        with col2:
            st.metric("Confiance", f"{result['confidence']*100:.1f}%")

        # Top 3
        st.subheader("Top 3 catégories")
        for item in result["top3"]:
            st.progress(item["score"],
                        text=f"{item['label']} — {item['score']*100:.1f}%")
    else:
        st.warning("Entrez un texte d'abord")