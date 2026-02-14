import streamlit as st
import pytesseract
import cv2
import numpy as np
from PIL import Image
import re

st.set_page_config(page_title="AI Football Scout", page_icon="⚽")

st.title("⚽ AI Football Scout")
st.write("Scanează fișa → primești analiză completă ca un scout real.")

# =========================================================
# CAMERA / UPLOAD
# =========================================================

img_file = st.camera_input("Fă poză la fișă") or st.file_uploader(
    "sau Upload", type=["jpg","png","jpeg"]
)

if img_file:

    image = Image.open(img_file)
    img = np.array(image)

    st.image(image, caption="Scan", use_column_width=True)

    # =====================================================
    # OCR
    # =====================================================

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=1.5, fy=1.5)
    gray = cv2.GaussianBlur(gray, (5,5), 0)

    text = pytesseract.image_to_string(gray, lang="spa")

    # =====================================================
    # EXTRAGERE DATE
    # =====================================================

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

    # =====================================================
    # 🧠 AI SCOUT ENGINE
    # =====================================================

    analiza = []

    # ---- WONDERKID CHECK ----
    if potential_max and potential_max >= 88:
        analiza.append("🌟 Elite Wonderkid")
    elif potential_max and potential_max >= 85:
        analiza.append("⭐ High Wonderkid")
    elif potential_max and potential_max >= 82:
        analiza.append("🟡 Solid Prospect")
    else:
        analiza.append("❌ Low Ceiling")

    # ---- CEILING ESTIMATE ----
    if media and potential_max:
        growth = potential_max - media

        if growth >= 12:
            ceiling = "Explozie mare de creștere"
        elif growth >= 8:
            ceiling = "Creștere bună"
        else:
            ceiling = "Creștere limitată"

        analiza.append(f"📈 Ceiling: {ceiling}")

    # =====================================================
    # ROLE DETECTION
    # =====================================================

    role = "Necunoscut"

    if regates and ritmo and pases:
        if regates >= 80 and ritmo >= 80:
            role = "Winger / Inside Forward"
        elif pases >= 80 and regates >= 75:
            role = "Interior / Mezzala"
        elif pases >= 82:
            role = "Deep Playmaker"
        elif tiros >= 75:
            role = "Attacking Mid / Shadow Striker"

    analiza.append(f"🎯 Rol optim: {role}")

    # =====================================================
    # BARÇA TIKI-TAKA FIT
    # =====================================================

    tiki = 0

    if pases:
        tiki += (pases - 60) * 0.2
    if regates:
        tiki += (regates - 60) * 0.15
    if edad and edad <= 21:
        tiki += 2

    if tiki >= 10:
        tiki_verdict = "🔵🔴 Perfect Barça profile"
    elif tiki >= 7:
        tiki_verdict = "🟡 Dezvoltabil pentru Barça"
    else:
        tiki_verdict = "❌ Nu e profil tiki-taka"

    analiza.append(f"🔵🔴 Barça fit: {tiki_verdict}")

    # =====================================================
    # STARTER / LOAN / ROTATION
    # =====================================================

    squad_role = ""

    if media >= 80:
        squad_role = "Starter imediat"
    elif media >= 75:
        squad_role = "Rotation player"
    else:
        squad_role = "Loan / Bench"

    analiza.append(f"👕 Squad role: {squad_role}")

    # =====================================================
    # DEVELOPMENT PLAN
    # =====================================================

    dev = ""

    if role == "Winger / Inside Forward":
        dev = "Winger → Pace + Dribbling"
    elif role == "Interior / Mezzala":
        dev = "Playmaker → Passing + Vision"
    else:
        dev = "Balanced Development"

    analiza.append(f"🛠 Development: {dev}")

    # =====================================================
    # FINAL VERDICT
    # =====================================================

    score = 0

    if potential_max >= 85:
        score += 3
    if edad <= 20:
        score += 2
    if regates >= 75:
        score += 1
    if pases >= 75:
        score += 1

    if score >= 6:
        final = "🔥 BUY NOW"
    elif score >= 4:
        final = "🟡 BUY IF CHEAP"
    else:
        final = "❌ SKIP"

    # =====================================================
    # AFIȘARE
    # =====================================================

    st.subheader("🧠 AI Scout Report")

    for a in analiza:
        st.write(a)

    st.subheader("Verdict Final")
    st.success(final)
