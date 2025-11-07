# =========================================================
# 🎓 SPK Kelayakan Beasiswa Menggunakan Fuzzy Tsukamoto (Streamlit)
# Versi Estetik & Elegan by Fonda
# =========================================================
import streamlit as st

# ======== Tampilan CSS ========
st.markdown("""
<style>
/* Background gradient lembut dengan warna utama */
.stApp {
    background: linear-gradient(135deg, #8FABD4 0%, #cbd9ec 100%);
    font-family: 'Poppins', sans-serif;
}

/* Judul besar */
h1 {
    color: #0a3d62;
    text-align: center;
    font-weight: 700;
    margin-bottom: 0.5em;
}

/* Subtitle */
h3 {
    color: #1f4e79;
    text-align: center;
    font-weight: 400;
    margin-top: -0.5em;
}

/* Label input */
div[data-testid="stNumberInput"] > label,
div[data-testid="stTextInput"] > label {
    color: #1f4e79;
    font-weight: 600;
}

/* Tombol utama */
div[data-testid="stButton"] > button {
    background: linear-gradient(90deg, #8FABD4, #6d92c9);
    color: white;
    font-weight: 600;
    border-radius: 12px;
    transition: 0.3s;
    border: none;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
}
div[data-testid="stButton"] > button:hover {
    background: linear-gradient(90deg, #6d92c9, #8FABD4);
    transform: scale(1.05);
}

/* Box hasil penilaian */
.result-box {
    background-color: #f8fbff;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.15);
    border-left: 6px solid #8FABD4;
    margin-top: 25px;
}

/* Paragraf di dalam hasil */
.result-box p {
    color: #1f4e79;
    font-weight: 500;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)


# ======== Fungsi Keanggotaan (Membership Function) ========

def linear_up(x, x0, x1):
    if x <= x0: return 0
    elif x >= x1: return 1
    else: return (x - x0) / (x1 - x0)

def linear_down(x, x0, x1):
    if x <= x0: return 1
    elif x >= x1: return 0
    else: return (x1 - x) / (x1 - x0)

# IPK
def ipk_rendah(x):  return linear_down(x, 2.0, 3.0)
def ipk_tinggi(x):  return linear_up(x, 2.75, 4.0)

# Penghasilan orang tua
def income_rendah(x):  return linear_down(x, 3000000, 7000000)
def income_tinggi(x):  return linear_up(x, 4000000, 12000000)

# Jumlah tanggungan
def tanggungan_sedikit(x):  return linear_down(x, 1, 3)
def tanggungan_banyak(x):   return linear_up(x, 2, 5)

# Fungsi output Tsukamoto
def z_rendah(alpha): return 100 - (alpha * 100)
def z_tinggi(alpha): return alpha * 100

# ======== Proses Inferensi Fuzzy Tsukamoto ========

def tsukamoto(ipk, income, tanggungan):
    rules = []

    alpha1 = min(ipk_tinggi(ipk), income_rendah(income))
    z1 = z_tinggi(alpha1)
    rules.append((alpha1, z1))

    alpha2 = min(ipk_rendah(ipk), income_tinggi(income))
    z2 = z_rendah(alpha2)
    rules.append((alpha2, z2))

    alpha3 = min(ipk_tinggi(ipk), tanggungan_banyak(tanggungan))
    z3 = z_tinggi(alpha3)
    rules.append((alpha3, z3))

    alpha4 = min(income_rendah(income), tanggungan_banyak(tanggungan))
    z4 = z_tinggi(alpha4)
    rules.append((alpha4, z4))

    numerator = sum(a * z for a, z in rules)
    denominator = sum(a for a, _ in rules)
    return numerator / denominator if denominator != 0 else 0


# =========================================================
# STREAMLIT APP
# =========================================================

st.title("🎓 Sistem Penilaian Kelayakan Penerima Beasiswa Kuliah Berbasis Komputer")
st.markdown("### Menggunakan Metode Fuzzy Tsukamoto")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    nama = st.text_input("👤 Nama Lengkap")
    ipk = st.number_input("📊 IPK", min_value=0.0, max_value=4.0, step=0.01)
with col2:
    income = st.number_input("💰 Penghasilan Orang Tua (Rp)", min_value=0, step=500000)
    tanggungan = st.number_input("👨‍👩‍👧 Jumlah Tanggungan", min_value=0, step=1)

st.markdown("")

if st.button("📝 Cek Status Beasiswa"):
    skor = tsukamoto(ipk, income, tanggungan)

    if skor < 40:
        status = "Tidak Layak Menerima Beasiswa ❌ "
        warna = "#c0392b"
    elif skor < 70:
        status = "Layak Menerima Beasiswa ⚖️"
        warna = "#f39c12"
    else:
        status = "Prioritas Mendapat Beasiswa 🏅"
        warna = "#27ae60"

    st.markdown(f"""
    <div class='result-box'>
        <h3 style='color:{warna}; text-align:center;'>Hasil Penilaian</h3>
        <p><b>Nama:</b> {nama}</p>
        <p><b>Skor Kelayakan:</b> {skor:.2f}</p>
        <p><b>Status Beasiswa:</b> <span style='color:{warna}; font-weight:600;'>{status}</span></p>
    </div>
    """, unsafe_allow_html=True)
