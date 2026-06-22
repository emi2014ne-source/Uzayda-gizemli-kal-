import streamlit as st

st.title("Uzayda Gizemli Kalis")
st.write("Hos geldin kaptan! Uzayin derinliklerinde bir macera basliyor.")

secim = st.radio("Ne yapmak istersin?", ["Motorlari calistir", "Radar taramasi yap"])

if secim == "Motorlari calistir":
    st.success("Motorlar calisti! Uzay bosluguna dogru ilerliyoruz...")
elif secim == "Radar taramasi yap":
    st.warning("Radar tarandi... Yakinlarda bilinmeyen bir sinyal tespit edildi!")
