import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from PIL import Image
import cv2

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(layout="wide", page_title="Audit IA Agricole 4.0", page_icon="🛸")

# --- 2. BASE DE DONNÉES : CULTURES & MÉDICAMENTS ---
INFOS_PLANTES = {
    "Tomates": {
        "temp_ideale": 25, "prix_kg": 12, "besoin_base": 10,
        "Maladies": {
            "Mildiou": {"Symptôme": "Taches brunes", "Médicament": "Bouillie Bordelaise", "Dosage": "20g/L"},
            "Pucerons": {"Symptôme": "Feuilles enroulées", "Médicament": "Savon Noir", "Dosage": "5%"}
        },
        "Conseil": "Aérer les pieds et éviter d'arroser le feuillage pour prévenir les champignons."
    },
    "Blé": {
        "temp_ideale": 20, "prix_kg": 4, "besoin_base": 5,
        "Maladies": {
            "Rouille": {"Symptôme": "Pustules orangées", "Médicament": "Fongicide systémique", "Dosage": "1L/ha"},
            "Septoriose": {"Symptôme": "Taches jaunâtres", "Médicament": "Triazole", "Dosage": "0.8L/ha"}
        },
        "Conseil": "Surveiller l'humidité au moment de l'épiaison pour maximiser le rendement."
    },
    "Olivier": {
        "temp_ideale": 28, "prix_kg": 45, "besoin_base": 3,
        "Maladies": {
            "Oeil de Paon": {"Symptôme": "Taches circulaires", "Médicament": "Fongicide cuprique", "Dosage": "300g/100L"},
            "Mouche": {"Symptôme": "Piqûres sur fruits", "Médicament": "Argile blanche", "Dosage": "50kg/ha"}
        },
        "Conseil": "Une taille d'éclaircie régulière limite la propagation des parasites."
    }
}

# --- 3. CHARGEMENT DU MODÈLE IA ---
@st.cache_resource
def entrainer_ia():
    try:
        df = pd.read_csv('data_agricole.csv')
        modele = RandomForestRegressor(n_estimators=100, random_state=42)
        modele.fit(df[['temperature', 'humidite_sol']], df['besoin_eau'])
        return modele
    except Exception as e:
        st.error(f"Erreur de données : {e}")
        return None

mon_ia = entrainer_ia()

# --- 4. BARRE LATÉRALE (SIDEBAR) ---
st.sidebar.header("🕹️ Paramètres du Terrain")
culture_nom = st.sidebar.selectbox("Choisir la Culture", list(INFOS_PLANTES.keys()))
t = st.sidebar.slider("Température (°C)", 0, 50, 25)
h = st.sidebar.slider("Humidité Sol (%)", 0, 100, 40)

# --- 5. LOGIQUE DE CALCUL ---
c = INFOS_PLANTES[culture_nom]
if mon_ia:
    besoin_eau = mon_ia.predict([[t, h]])[0] * (c['besoin_base'] / 10)
    # Calcul du rendement selon l'écart à la température idéale
    rendement_pourcent = max(0, 100 - (abs(c['temp_ideale'] - t) * 3))
    gain_net = (rendement_pourcent * c['prix_kg']) - (besoin_eau * 0.05)
else:
    besoin_eau, rendement_pourcent, gain_net = 0, 0, 0

# --- 6. AFFICHAGE PRINCIPAL ---
st.title(f"🌍 Audit Intelligent du Terrain : {culture_nom}")
st.markdown("---")

# Métriques du tableau de bord
m1, m2, m3, m4 = st.columns(4)
m1.metric("🌡️ Température", f"{t}°C")
m2.metric("💧 Humidité", f"{h}%")
m3.metric("🚰 Besoin Eau IA", f"{besoin_eau:.1f} L/m²")
m4.metric("💰 Bénéfice Est.", f"{gain_net:.0f} DH", delta=f"{rendement_pourcent:.1f}% Rendement")

st.markdown("---")

# --- 7. SECTION ANALYSE DRONE (AU CENTRE) ---
st.header("🛸 Analyse d'Imagerie Drone (Scan NDVI)")
uploaded_file = st.file_uploader("Veuillez charger une photo aérienne du drone pour l'analyse spectrale...", type=["jpg", "png", "jpeg"])

col_drone, col_diag = st.columns([3, 2])

with col_drone:
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Vue Drone du secteur", use_container_width=True)
        # Analyse de santé basée sur la couleur verte
        img_array = np.array(image)
        sante_score = np.mean(img_array[:, :, 1]) / 255 # Analyse du canal vert
        st.write(f"**Indice de Vitalité détecté par Drone :** `{sante_score:.2%}`")
        if sante_score < 0.4:
            st.error("🚨 ALERTE : Zones de stress végétatif détectées sur le scan !")
        else:
            st.success("✅ SANTÉ : La végétation analysée est vigoureuse.")
    else:
        st.info("💡 En attente du scan drone pour l'analyse visuelle du terrain.")

# --- 8. DIAGNOSTIC MÉDICAL & ORDONNANCE ---
with col_diag:
    st.subheader("🩺 Diagnostic & Traitement")
    if h > 70:
        # On choisit la maladie principale selon la culture
        maladie_nom = "Mildiou" if culture_nom == "Tomates" else ("Rouille" if culture_nom == "Blé" else "Oeil de Paon")
        medoc = c["Maladies"][maladie_nom]
        
        st.warning(f"**Pathologie suspectée : {maladie_nom}**")
        st.write(f"**Symptômes :** {medoc['Symptôme']}")
        st.markdown(f"**💊 Médicament :** `{medoc['Médicament']}`")
        st.markdown(f"**⚖️ Dosage recommandé :** `{medoc['Dosage']}`")
    else:
        st.success("Aucune maladie détectée. Conditions climatiques saines.")
    
    st.info(f"**💡 Conseil de l'Audit :** {c['Conseil']}")

# --- 9. GRAPHIQUE DE PERFORMANCE ---
st.markdown("---")
st.subheader("📊 Prévisions de Profitabilité")
chart_data = pd.DataFrame({
    'Catégories': ['Revenus (DH)', 'Charges (Eau/DH)', 'Bénéfice Net (DH)'],
    'Valeurs': [rendement_pourcent * c['prix_kg'], besoin_eau * 0.05, gain_net]
})
st.bar_chart(chart_data.set_index('Catégories'))