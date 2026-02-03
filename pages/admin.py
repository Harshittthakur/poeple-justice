import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import json

# ---------------- FIREBASE INIT ----------------
def init_fb():
    if not firebase_admin._apps:
        try:
            firebase_key = json.loads(st.secrets["FIREBASE_KEY"])
            cred = credentials.Certificate(firebase_key)
            firebase_admin.initialize_app(cred, {
                "databaseURL": "https://janseva-app-960e7-default-rtdb.firebaseio.com"
            })
            return True
        except Exception as e:
            st.error(f"❌ Firebase Init Error: {e}")
            return False
    return True


# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="Adhikari Dashboard",
    layout="wide"
)

st.title("👮‍♂️ Adhikari Dashboard")
st.subheader("📥 Aayi hui Shikayatein")
st.markdown("---")


# ---------------- MAIN LOGIC ----------------
if init_fb():
    try:
        ref = db.reference("complaints")
        data = ref.get()

        if data:
            for key in reversed(list(data.keys())):
                val = data[key]

                with st.container(border=True):
                    col1, col2 = st.columns([2, 1])

                    with col1:
                        st.markdown(f"### 📍 {val.get('category', 'Anya')}")
                        st.write(f"**👤 Nagrik:** {val.get('name', 'N/A')}")
                        st.write(f"**📞 Phone:** {val.get('phone', 'N/A')}")
                        st.write(f"**🏠 Pata:** {val.get('address', 'N/A')}")
                        st.info(f"**📝 Vivran:** {val.get('description', 'N/A')}")
                        st.caption(f"📅 Time: {val.get('time', 'N/A')}")

                        if st.button("Resolve Karein ✅", key=key, use_container_width=True):
                            ref.child(key).delete()
                            st.success("✅ Shikayat resolve ho gayi!")
                            st.rerun()

                    with col2:
                        img = val.get("image")
                        if img:
                            st.image(
                                f"data:image/jpeg;base64,{img}",
                                caption="📸 Saboot",
                                use_container_width=True
                            )
                        else:
                            st.warning("📷 Photo nahi hai")

        else:
            st.success("🎉 Koi pending shikayat nahi hai!")
            st.balloons()

    except Exception as e:
        st.error(f"❌ Data Load Error: {e}")

else:
    st.warning("Firebase initialize nahi ho paaya")
