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
    compare_clicked = st.button("📊 Bandingkan Tarif & Tindakan")
with col3:
    appeal_clicked = st.button("💬 Kirim Masukan / Sanggahan")
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

    model = init_model()  # ← HANYA MODEL, TIDAK ADA TOKENIZER

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Tanyakan sesuatu tentang layanan JKN..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = get_response(prompt, model)  # ← HANYA KIRIM MODEL
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
# ---------- FITUR PERBANDINGAN TARIF ----------
if compare_clicked:
    st.markdown("### 📊 Bandingkan Tarif & Tindakan")
    
    with st.form("claim_analysis_form"):
        diagnosis = st.selectbox(
            "Diagnosis Utama",
            ["ISPA", "Diare", "Hipertensi", "Diabetes", "Fraktur Tulang", "Lainnya"],
            help="Pilih diagnosis sesuai klaim"
        )
        if diagnosis == "Lainnya":
            diagnosis = st.text_input("Masukkan diagnosis lain")
        
        claimed_amount = st.number_input(
            "Nilai Klaim (Rp)", 
            min_value=0, 
            value=1000000, 
            step=100000,
            format="%d"
        )
        days = st.number_input("Lama Rawat Inap (hari)", min_value=0, max_value=30, value=1)
        facility = st.text_input("Nama Fasilitas", value="RS Umum Daerah")
        
        submitted = st.form_submit_button("Analisis Klaim")
    
    if submitted and diagnosis:
        from fairness_engine import analyze_claim, generate_appeal_suggestion
        
        result = analyze_claim(diagnosis, claimed_amount, facility, days)
        
        # Tampilkan hasil
        st.markdown("#### 📌 Hasil Analisis")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Klaim RS", f"Rp{result['claimed_amount']:,}".replace(",", "."))
        with col_b:
            st.metric("Tarif BPJS", f"Rp{result['tarif_bpjs']:,}".replace(",", "."))
        with col_c:
            if result["is_suspicious"]:
                st.warning("⚠️ Perlu Tinjauan")
            else:
                st.success("✅ Wajar")
        
        if result["warning"]:
            st.markdown("#### ⚠️ Peringatan")
            for w in result["warning"]:
                st.warning(w)
        
        st.markdown("#### 💬 Saran Sanggahan")
        suggestion = generate_appeal_suggestion(result)
        st.info(suggestion)

# ---------- FITUR SANGGAHAN ----------
if appeal_clicked or st.session_state.get("show_appeal_form", False):
    st.session_state["show_appeal_form"] = True
    st.markdown("### 💬 Kirim Sanggahan atau Masukan")
    
    with st.form("appeal_form"):
        st.text_area("Jelaskan sanggahan Anda", height=150, 
                     placeholder="Contoh: Klaim rawat inap ISPA selama 5 hari terlalu mahal...")
        uploaded = st.file_uploader("Unggah dokumen pendukung (opsional)", type=["pdf", "jpg", "png"])
        submit_appeal = st.form_submit_button("Kirim Sanggahan")
    
    if submit_appeal:
        st.success("✅ Sanggahan Anda telah dikirim! Nomor tiket: FC-2025-11451")
        st.session_state["show_appeal_form"] = False
