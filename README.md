# 🇲🇦 Darija NLP Classifier

Classification automatique de textes en Darija marocaine.

## Stack
Python | DarijaBERT | FastAPI | Streamlit | Scikit-learn | W&B

## Résultats
- Dataset : 23k textes annotés | 7 classes
- Meilleur modèle : Linear SVC + TF-IDF char 2-4grams | F1-macro = 0.74
- Annotation : Google Gemini + validation manuelle Label Studio (20% correction)

## ⚠️ Modèles requis

Télécharger les fichiers .pkl depuis Google Drive :
((https://drive.google.com/drive/folders/18Gg2DhWUUNJexjmTW5PrJbqhQLXI3DFb?usp=sharing))

Placer dans : app/models/ 
  

## Lancer l'API
pip install -r requirements.txt
uvicorn app/main:app --reload

## Lancer l'interface
streamlit run app/app.py
