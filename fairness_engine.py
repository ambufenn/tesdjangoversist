# fairness_engine.py

# Data simulasi INA-CBGs (bisa diganti dengan CSV/DB nanti)
INA_CBGs = {
    "ISPA": 850000,
    "Diare": 720000,
    "Hipertensi": 1200000,
    "Diabetes": 1500000,
    "Fraktur Tulang": 3500000,
    "Rawat Jalan Umum": 150000,
    "Rawat Inap Umum": 980000  # per kasus, bukan per hari
}

# Rata-rata klaim historis (simulasi)
REGIONAL_AVG = {
    "ISPA": 820000,
    "Diare": 700000,
    "Hipertensi": 1100000,
    "Diabetes": 1450000,
    "Fraktur Tulang": 3300000,
    "Rawat Jalan Umum": 140000,
    "Rawat Inap Umum": 950000
}

def analyze_claim(diagnosis, claimed_amount, facility_type="Rumah Sakit", days=1):
    """
    Analisis klaim berdasarkan diagnosis dan nilai klaim.
    Returns: dict dengan perbandingan & warning
    """
    diagnosis_key = diagnosis if diagnosis in INA_CBGs else "Rawat Jalan Umum"
    
    tarif_bpjs = INA_CBGs.get(diagnosis_key, 0)
    avg_claim = REGIONAL_AVG.get(diagnosis_key, tarif_bpjs)
    
    warning = []
    is_suspicious = False

    # Cek selisih vs tarif BPJS
    if tarif_bpjs > 0:
        over_bpjs_pct = (claimed_amount - tarif_bpjs) / tarif_bpjs * 100
        if over_bpjs_pct > 20:
            warning.append(f"Klaim {over_bpjs_pct:.1f}% di atas tarif INA-CBGs BPJS.")
            is_suspicious = True
        elif over_bpjs_pct > 10:
            warning.append(f"Klaim sedikit di atas tarif BPJS (+{over_bpjs_pct:.1f}%).")
    else:
        warning.append("Diagnosis tidak ditemukan dalam daftar tarif — perlu verifikasi manual.")

    # Cek vs rata-rata regional
    if avg_claim > 0 and claimed_amount > avg_claim * 1.25:
        over_avg_pct = (claimed_amount - avg_claim) / avg_claim * 100
        warning.append(f"Klaim {over_avg_pct:.1f}% di atas rata-rata regional untuk diagnosis ini.")
        is_suspicious = True

    # Cek pola tidak lazim (contoh sederhana)
    if days > 3 and diagnosis in ["ISPA", "Diare"]:
        warning.append("Rawat inap >3 hari tidak lazim untuk diagnosis ringan ini.")
        is_suspicious = True

    return {
        "diagnosis": diagnosis,
        "claimed_amount": claimed_amount,
        "tarif_bpjs": tarif_bpjs,
        "regional_avg": avg_claim,
        "warning": warning,
        "is_suspicious": is_suspicious,
        "facility_type": facility_type,
        "days": days
    }

def generate_appeal_suggestion(analysis_result):
    """Buat saran sanggahan berdasarkan analisis"""
    if analysis_result["is_suspicious"]:
        return (
            "Berdasarkan analisis FairCare, klaim ini memiliki indikasi ketidaksesuaian. "
            "Anda dapat mengajukan sanggahan dengan menyertakan:\n"
            "- Salinan rincian klaim dari rumah sakit\n"
            "- Bukti diagnosis (hasil lab/resep)\n"
            "- Pertanyaan spesifik: mengapa biaya melebihi tarif BPJS?"
        )
    else:
        return (
            "Klaim ini sesuai dengan standar tarif dan pola pelayanan. "
            "Jika Anda tetap ingin mengajukan sanggahan, silakan jelaskan alasan spesifik Anda."
        )
