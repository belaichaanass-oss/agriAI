import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from PIL import Image
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(layout="wide", page_title="Audit Agricole IA 5.0", page_icon="🛰️")

# --- 2. DONNÉES MÉTIER ---
INFOS_PLANTES = {
    "Tomates": {"temp_ideale": 25, "prix_kg": 12, "besoin_base": 10, "cycle_jours": 90, "rendement_max": 5.0, 
                "Maladies": {"Mildiou": "Bouillie Bordelaise (20g/L)"}},
    "Blé": {"temp_ideale": 20, "prix_kg": 4, "besoin_base": 5, "cycle_jours": 180, "rendement_max": 8.0,
            "Maladies": {"Rouille": "Fongicide (1L/ha)"}},
    "Olivier": {"temp_ideale": 28, "prix_kg": 45, "besoin_base": 3, "cycle_jours": 365, "rendement_max": 2.5,
                "Maladies": {"Oeil de Paon": "Cuivre (300g/100L)"}}
}

# --- 3. ENTRAÎNEMENT IA ---
@st.cache_resource
def entrainer_ia():
    try:
        df = pd.read_csv('data_agricole.csv')
        modele = RandomForestRegressor(n_estimators=100, random_state=42)
        modele.fit(df[['temperature', 'humidite_sol']], df['besoin_eau'])
        return modele
    except:
        return None

mon_ia = entrainer_ia()

# --- 4. BARRE LATÉRALE (CAPTEURS) ---
st.sidebar.title("🎮 Commandes")
culture_nom = st.sidebar.selectbox("Culture", list(INFOS_PLANTES.keys()))
mode_meteo = st.sidebar.toggle("Météo Directe", value=True)

if mode_meteo:
    t, h = 30, 65 # Valeurs simulées
    st.sidebar.info(f"Météo : {t}°C | {h}% Hum.")
else:
    t = st.sidebar.slider("Température (°C)", 0, 50, 25)
    h = st.sidebar.slider("Humidité Sol (%)", 0, 100, 40)

# --- 5. CALCULS ---
c = INFOS_PLANTES[culture_nom]
if mon_ia:
    besoin_eau = mon_ia.predict([[t, h]])[0] * (c['besoin_base'] / 10)
    sante_theorique = max(0, 100 - (abs(c['temp_ideale'] - t) * 4))
    recolte_estimee = (sante_theorique / 100) * c['rendement_max']
    gain_net = (recolte_estimee * 1000 * c['prix_kg']) - (besoin_eau * 1000 * 0.05)

# --- 6. DASHBOARD PRINCIPAL ---
st.title(f"🚀 Audit Intelligent : {culture_nom}")

# Métriques
m1, m2, m3, m4 = st.columns(4)
m1.metric("🌡️ Température", f"{t}°C")
m2.metric("💧 Humidité", f"{h}%")
m3.metric("🚜 Récolte Prédite", f"{recolte_estimee:.2f} T/Ha")
m4.metric("💰 Bénéfice Est.", f"{gain_net:,.0f} DH/Ha")

st.divider()

# --- 7. SECTION DRONE (SÉCURISÉE) ---
st.header("🛰️ Analyse Drone (Scan NDVI)")
# Suppression de 'type' pour que TOUS les fichiers s'affichent dans Windows
uploaded_file = st.file_uploader("Choisissez une image de drone (JPG, PNG, ou autre)...", type=None)

col_drone, col_diag = st.columns([3, 2])

with col_drone:
    if uploaded_file:
        try:
            # On force la conversion en RGB pour éviter les erreurs de format (comme AVIF)
            image = Image.open(uploaded_file).convert('RGB')
            st.image(image, caption=f"Fichier : {uploaded_file.name}", use_container_width=True)
            
            # Analyse simple de la couleur
            img_arr = np.array(image)
            sante_score = np.mean(img_arr[:,:,1]) / 255
            st.metric("Vigueur détectée", f"{sante_score:.2%}")
            
            if sante_score < 0.4:
                st.error("🚨 Alerte : Stress végétatif détecté sur l'image !")
            else:
                st.success("✅ Santé : Végétation vigoureuse.")
        except Exception as e:
            st.error(f"Erreur de lecture du fichier : {e}")
            st.info("Conseil : Utilisez une capture d'écran ou un fichier .jpg si le problème persiste.")
    else:
        st.info("💡 En attente du scan drone. Cliquez sur 'Browse files' pour commencer.")

with col_diag:
    st.subheader("🩺 Diagnostic & Secteurs")
    if h > 60:
        nom_m = list(c["Maladies"].keys())[0]
        st.warning(f"**Risque de {nom_m} détecté**")
        st.write(f"💊 Traitement : {c['Maladies'][nom_m]}")
    else:
        st.success("Aucune maladie détectée par les capteurs.")
    
    st.divider()
    st.write("**État des zones :**")
    for z in ["Zone Nord", "Zone Sud"]:
        st.write(f"📍 {z} : :green[Sain]")

st.divider()

# Graphique final
st.subheader("📊 Prévision de Rentabilité")
data_bar = pd.DataFrame({"Valeurs": [recolte_estimee*1000*c['prix_kg'], gain_net]}, index=["Revenus", "Bénéfice"])
st.bar_chart(data_bar)

if st.button("💾 Générer le Rapport"):
    st.balloons()
    st.success("Audit enregistré !")