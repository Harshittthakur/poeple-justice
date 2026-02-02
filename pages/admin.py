import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import os

# --- FIREBASE CONNECT (Admin Page Fix) ---
def init_fb():
    if not firebase_admin._apps:
        # Aapka folder path logic
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        p = os.path.join(base_path, "key.json")
        
        if os.path.exists(p):
            try:
                cred = credentials.Certificate(p)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': 'https://janseva-app-960e7-default-rtdb.firebaseio.com'
                })
                return True
            except Exception as e:
                st.error(f"Init Error: {e}")
                return False
        else:
            st.error("❌ 'key.json' file nahi mili!")
            return False
    return True

# Page layout
st.set_page_config(page_title="Adhikari Dashboard", layout="wide")

if init_fb():
    st.title("👨‍✈️ Adhikari Dashboard")
    st.subheader("📥 Aayi hui Shikayatein")
    st.markdown("---")

    try:
        # Database se complaints uthana
        ref = db.reference('complaints')
        data = ref.get()

        if data:
            # Latest shikayat upar dikhane ke liye
            for key in reversed(list(data.keys())):
                val = data[key]
                
                # Ek safed box banana har shikayat ke liye
                with st.container(border=True):
                    col1, col2 = st.columns([2, 1]) # Text left mein, Photo right mein
                    
                    with col1:
                        st.markdown(f"### 📍 {val.get('category', 'Anya')}")
                        st.write(f"**👤 Nagrik:** {val.get('name', 'N/A')}")
                        st.write(f"**📞 Phone:** {val.get('phone', 'N/A')}")
                        st.write(f"**🏠 Pata:** {val.get('address', 'N/A')}")
                        st.info(f"**📝 Vivran:** {val.get('description', 'N/A')}")
                        st.caption(f"📅 Time: {val.get('time', 'N/A')}")
                        
                        # --- RESOLVE BUTTON LOGIC ---
                        if st.button(f"Resolve Karein ✅", key=f"btn_{key}", use_container_width=True):
                            try:
                                # Database se us specific ID ko delete karna
                                ref.child(key).delete()
                                st.success("🎉 Shikayat hal ho gayi aur list se hata di gayi!")
                                st.rerun() # Page refresh taaki wo card gayab ho jaye
                            except Exception as e:
                                st.error(f"Resolve karne mein dikat aayi: {e}")

                    with col2:
                        img_data = val.get('image')
                        if img_data:
                            # Base64 photo ko display karna
                            st.image(f"data:image/jpeg;base64,{img_data}", 
                                     caption="Saboot ki Photo", 
                                     use_container_width=True)
                        else:
                            st.warning("No Photo Available")
        else:
            st.balloons()
            st.success("Sabhi shikayatein hal ho chuki hain! ✨")
            
    except Exception as e:
        st.error(f"Data loading error: {e}")
else:
    st.warning("Firebase initialize nahi hua. Check your key.json path.")