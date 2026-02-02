import streamlit as st

st.set_page_config(page_title="Jan Seva Portal", layout="centered")

st.title("🏛️ Jan Seva Portal")
st.write("Kripya chunein ki aap kaise aage badhna chahte hain:")

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("📢 Nagrik Portal (User)", use_container_width=True, type="primary"):
        st.switch_page("pages/app.py")

with col2:
    if st.button("👨‍✈️ Adhikari Portal (Admin)", use_container_width=True):
        st.switch_page("pages/admin.py")