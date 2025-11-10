import streamlit as st
import pandas as pd

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="FairCare Pulse", layout="wide")

# ---------- HEADER ----------
st.markdown("""
    <h2 style='color:#0A8F5B; text-align:center;'>FairCare Pulse</h2>
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
    st.button("🤖 Chatbot Bantuan")

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

# styling custom
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
