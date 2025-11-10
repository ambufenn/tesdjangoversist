import streamlit as st
import pandas as pd
from model import load_model
from handler import get_response

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="JKNKLIN", layout="wide")

# ---------- HEADER ----------
st.markdown("""
    <h2 style='color:#0A8F5B; text-align:center;'>JKNKLIN</h2>
""", unsafe_allow_html=True)

st.markdown("""
    <h3 style='color:#007F3D;'>Selamat Datang, <b>Budi Santoso</b></h3>
    <p>No. Peserta: <b>000123456789</b></p>
""", unsafe_allow_html=True)

# ---------- QUICK ACTIONS ----------
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("🗂️ Lihat Riwayat Layanan")
with col2:
    st.button("📊 Bandingkan Tarif & Tindakan")
with col3:
    st.button("💬 Kirim Masukan / Sanggahan")
with col4:
    chat_toggle = st.button("🤖 Chatbot Bantuan")

# ---------- FAIRNESS INDEX ----------
st.markdown("""
<div style="border:1px solid #D9F0E4; background-color:#F2FBF7; padding:10px; border-radius:8px;">
<b>Indeks Keandalan:</b> <span style="color:#007F3D;">89/100</span><br>
<i>Akses Anda: Sehat & Transparan</i>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------- TRANSPARENCY PANEL ----------
st.success("✅ **Transparansi AI** — Sistem tidak menemukan kejanggalan dalam layanan terakhir Anda. Semua data sesuai dengan standar JKN.")
st.markdown("[Pelajari lebih lanjut ›](#)")

# ---------- LAST VISITS ----------
st.markdown("### 🏥 3 Kunjungan Terakhir")

data = pd.DataFrame({
    "Fasilitas": ["RS Mitra Sehat", "Klinik Sejahtera", "RS Cinta Kasih"],
    "Tanggal": ["15 Mei 2023", "2 April 2023", "10 Maret 2023"],
    "Layanan": ["Pemeriksaan Umum", "Konsultasi Spesialis", "Rawat Inap"],
    "Status": ["Terverifikasi", "Dalam Review", "Catatan Ditambahkan"]
})

def status_color(status):
    color_map = {
        "Terverifikasi": "#D4EDDA",
        "Dalam Review": "#D1ECF1",
        "Catatan Ditambahkan": "#FFF3CD"
    }
    return f"background-color: {color_map.get(status, 'white')};"

st.dataframe(
    data.style.apply(lambda s: [status_color(v) for v in s], subset=["Status"])
)

st.markdown("<center><a href='#' style='color:#0A8F5B;'>Lihat Semua Riwayat</a></center>", unsafe_allow_html=True)

# ---------- CHATBOT SECTION ----------
if chat_toggle:
    st.markdown("### 🤖 Chatbot FairCare Assistant")

    @st.cache_resource
    def init_model():
        return load_model()

    tokenizer, model = init_model()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Tanyakan sesuatu tentang layanan JKN..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = get_response(prompt, tokenizer, model)
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
