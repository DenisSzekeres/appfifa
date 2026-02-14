import streamlit as st
import easyocr
import cv2
import numpy as np
from PIL import Image
import re

st.set_page_config(page_title="AI Football Scout", page_icon="⚽")

st.title("⚽ AI Football Scout")
st.write("Scanează fișa jucătorului.")

# =====================================================
# CAMERA / UPLOAD
# =====================================================

img_file = st.camera_input("Fă poză") or st.file_uploader(
    "Upload", type=["jpg","png","jpeg"]
)

if img_file:

    image = Image.open(img_file)
    img = np.array(image)

    st.image(image, caption="Scan", use_column_width=True)

    # =================================================
    # OCR EASYOCR
    # =================================================

    reader = easyocr.Reader(['en','es'])

    results = reader.readtext(img, detail=0)
    text = " ".join(results)

    st.subheader("📄 Text detectat")
    st.text(text)

    # =================================================
    # EXTRAGERE
    # =================================================

    def extrage(pattern):
        match = re.search(pattern, text)
        return int(match.group(1)) if match else None

    media = extrage(r"\b(\d{2})\b\s*\|")

    potential = re.search(r"(\d{2})\s*-\s*(\d{2})", text)
    potential_max = int(potential.group(2)) if potential else None

    edad = extrage(r"Edad\s*(\d{1,2})")

    ritmo = extrage(r"Ritmo\s*(\d{2})")
    tiros = extrage(r"Tiros\s*(\d{2})")
    pases = extrage(r"Pases\s*(\d{2})")
    regates = extrage(r"Regates\s*(\d{2})")
    defensa = extrage(r"Defensa\s*(\d{2})")
    fisico = extrage(r"Físico\s*(\d{2})")

    stats = {
        "Media": media,
        "Potential": potential_max,
        "Edad": edad,
        "Ritmo": ritmo,
        "Tiros": tiros,
        "Pases": pases,
        "Regates": regates,
        "Defensa": defensa,
        "Fisico": fisico
    }

    st.subheader("📊 Stats")
    st.json(stats)

    # =================================================
    # AI SCOUT
    # =================================================

    analiza = []

    if potential_max and potential_max >= 85:
        analiza.append("🌟 Wonderkid")
    elif potential_max and potential_max >= 82:
        analiza.append("🟡 Prospect bun")
    else:
        analiza.append("❌ Ceiling mic")

    if media and potential_max:
        growth = potential_max - media
        analiza.append(f"📈 Growth potential: +{growth}")

    role = "Rotation"

    if regates and ritmo and regates >= 78 and ritmo >= 78:
        role = "Winger"
    elif pases and pases >= 78:
        role = "Playmaker"

    analiza.append(f"🎯 Rol: {role}")

    tiki = "❌"
    if pases and regates and (pases + regates)/2 >= 75:
        tiki = "🔵🔴 Fit Barça"

    analiza.append(f"Barça fit: {tiki}")

    st.subheader("🧠 Scout Report")

    for a in analiza:
        st.write(a)
