import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import os
import base64
from datetime import datetime

# --- FIREBASE CONNECT (Updated for Streamlit Cloud) ---
def init_fb():
    if not firebase_admin._apps:
        try:
            # Check karein ki kya hum Streamlit Cloud par hain
            if "gcp_service_account" in st.secrets:
                # Online: Secrets se data uthayega
                creds_dict = dict(st.secrets["gcp_service_account"])
                cred = credentials.Certificate(creds_dict)
            else:
                # Local: Aapke computer ki key.json use karega
                cred = credentials.Certificate("key.json")
            
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://janseva-app-960e7-default-rtdb.firebaseio.com'
            })
            return True
        except Exception as e:
            st.error(f"Connection Error: {e}")
            return False
    return True

def get_base64(file):
    if file:
        return base64.b64encode(file.getvalue()).decode()
    return None

# App shuru ho rahi hai
if init_fb():
    st.title("📢 Jan-Seva Portal")
    st.subheader("Shikayat Darj Karein")

    with st.form("shikayat_form", clear_on_submit=True):
        naam = st.text_input("Aapka Naam")
        mobile = st.text_input("Mobile Number", max_chars=10)
        vibhag = st.selectbox("Shikayat ka Prakar", [
            "Students Problem (Shiksha)", 
            "Gandi Naali / Safai", 
            "Logon ke sath Anyay (Justice)", 
            "Bijli / Paani", 
            "Anya"
        ])
        pata = st.text_input("Area/Pata")
        vivran = st.text_area("Samasya ki poori jankari")

        st.write("---")
        st.write("📸 **Saboot ke liye Photo dein (Camera ya Gallery)**")
        cam_photo = st.camera_input("Live Photo Khichein")
        file_photo = st.file_uploader("Ya Gallery se upload karein", type=['jpg', 'png', 'jpeg'])
        
        submit = st.form_submit_button("Shikayat Submit Karein")

    if submit:
        photo = cam_photo if cam_photo else file_photo
        if naam and mobile and vivran and photo:
            img_str = get_base64(photo)
            try:
                ref = db.reference('complaints')
                ref.push({
                    "name": naam,
                    "phone": mobile,
                    "category": vibhag,
                    "address": pata,
                    "description": vivran,
                    "image": img_str,
                    "status": "Pending",
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.success("✅ Aapki shikayat safaltapoorvak darj ho gayi!")
                st.balloons()
            except Exception as e:
                st.error(f"Database Error: {e}")
        else:
            st.warning("⚠️ Kripya Naam, Mobile, Details aur ek Photo zaroor bharein!")
