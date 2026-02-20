import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Virtual Lab Optik - Streamlit",
    page_icon="🔬",
    layout="wide"
)

# --- CSS CUSTOM ---
st.markdown("""
<style>
    .reportview-container {
        background: #0e1117;
    }
    .main-header {
        font-size: 2.5rem;
        color: #4facfe;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- JUDUL ---
st.markdown("<h1 class='main-header'>🔬 Virtual Lab Fisika: Optik Geometri</h1>", unsafe_allow_html=True)

# --- SIDEBAR KONTROL ---
with st.sidebar:
    st.header("⚙️ Panel Kontrol")
    
    # Pilihan Jenis Optik
    jenis_optik = st.selectbox(
        "Pilih Komponen Optik:",
        [
            "Lensa Cembung (Konvergen)",
            "Lensa Cekung (Divergen)",
            "Cermin Cekung (Konvergen)",
            "Cermin Cembung (Divergen)",
            "Cermin Datar"
        ]
    )
    
    st.markdown("---")
    
    # Slider Parameter
    f_val = st.slider("Jarak Fokus (f) [cm]", min_value=5.0, max_value=50.0, value=15.0, step=0.5)
    s_val = st.slider("Jarak Benda (s) [cm]", min_value=0.0, max_value=80.0, value=20.0, step=0.5)
    h_obj = st.slider("Tinggi Benda (h) [cm]", min_value=1.0, max_value=10.0, value=3.0, step=0.5)
    
    st.markdown("---")
    
    # Checkbox Visualisasi
    st.subheader("Opsi Visualisasi")
    show_ray1 = st.checkbox("Sinar Istimewa 1 (Sejajar -> Fokus)", value=True)
    show_ray2 = st.checkbox("Sinar Istimewa 2 (Pusat Optik)", value=True)
    
    # Tombol Simpan (Simulasi)
    if st.button("💾 Simpan Data ke Tabel"):
        # Hitung data saat ini untuk disimpan
        # (Logika perhitungan ada di bawah, kita ambil nanti)
        pass # Streamlit reruns script, button logic usually needs session state handling

# --- LOGIKA FISIKA ---
# Adaptasi dari OptikGeometriFrame
is_mirror = "Cermin" in jenis_optik
is_flat = "Datar" in jenis_optik

if "Konvergen" in jenis_optik:
    f = f_val
elif "Divergen" in jenis_optik:
    f = -f_val
else:
    f = float('inf') # Cermin Datar / Fallback

# Hitung Bayangan (s', M, h')
sifat_bayangan = []
s_img = 0.0
m = 0.0
h_img = 0.0
x_img = 0.0
real = False

if is_flat:
    s_img = -s_val
    m = 1
    h_img = h_obj
    real = False # Maya
    x_img = -s_img # s' negatif, jadi posisi x positif (Kanan cermin)
    sifat_bayangan = ["Maya", "Tegak", "Sama Besar"]
else:
    if abs(s_val - f) < 0.1: # Di titik fokus
        s_img = float('inf') 
        m = float('inf')
        h_img = float('inf')
        real = False
        sifat_bayangan = ["Bayangan di Tak Hingga"]
    else:
        # Rumus utama: 1/f = 1/s + 1/s'  => 1/s' = 1/f - 1/s = (s-f)/Sf
        s_img = (s_val * f) / (s_val - f)
        m = -s_img / s_val
        h_img = m * h_obj
        
        # Penentuan Sifat Nyata/Maya & Posisi X
        if is_mirror:
            # Cermin: 
            # s' > 0 (Nyata) -> Depan cermin (Kiri, x < 0)
            # s' < 0 (Maya) -> Belakang cermin (Kanan, x > 0)
            real = s_img > 0
            x_img = -s_img 
        else:
            # Lensa:
            # s' > 0 (Nyata) -> Belakang lensa (Kanan, x > 0)
            # s' < 0 (Maya) -> Depan lensa (Kiri, x < 0)
            real = s_img > 0
            x_img = s_img

        sifat_bayangan.append("Nyata" if real else "Maya")
        sifat_bayangan.append("Tegak" if m > 0 else "Terbalik")
        sifat_bayangan.append(f"Perbesaran {abs(m):.2f}x")

# --- KOLOM UTAMA (PLOT & DATA) ---
col1, col2 = st.columns([2, 1])

with col1:
    # --- PLOTTING MATPLOTLIB ---
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Setup Axis
    ax.axhline(0, color='white', linewidth=1)
    ax.axvline(0, color='#00d2ff', linewidth=3, alpha=0.4) # Sumbu Optik
    
    # Styling Matplotlib Gelap (Agar cocok dengan Streamlit Dark Mode)
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    for spine in ax.spines.values():
        spine.set_color('white')

    # Gambar Lensa/Cermin
    if not is_flat:
        y_curve = np.linspace(-15, 15, 100)
        # Kurva visual saja (tidak presisi matematis optik)
        if "Cembung" in jenis_optik:
            curve = - (y_curve**2) / 100 if "Lensa" in jenis_optik else (y_curve**2) / 100
        else:
            curve = (y_curve**2) / 100 if "Lensa" in jenis_optik else - (y_curve**2) / 100
            
        if "Lensa" in jenis_optik:
            # Gambar Elips Lensa
            ax.add_patch(patches.Ellipse((0,0), width=2, height=30, color='skyblue', alpha=0.3))
            # Titik Fokus
            ax.scatter([f, -f], [0, 0], color='#ff4757', zorder=5)
            ax.text(f, -3, 'F2', color='#ff4757', ha='center')
            ax.text(-f, -3, "F1", color='#ff4757', ha='center')
        else:
            # Gambar Cermin Lengkung
            x_arc = curve
            ax.plot(x_arc, y_curve, color='cyan', linewidth=2)
            # Posisi Fokus Real pada Cermin
            # Cekung: Fokus di depan (Kiri, -f). Cembung: Fokus di belakang (Kanan, +f)
            # Logika f kita: Cekung (+), Cembung (-).
            # Geometris X:
            if "Cekung" in jenis_optik:
                real_f_pos = -abs(f) # Kiri
            else:
                real_f_pos = abs(f) # Kanan
                
            ax.scatter([real_f_pos], [0], color='#ff4757', zorder=5)
            ax.text(real_f_pos, -3, 'F', color='#ff4757', ha='center')
            ax.scatter([2*real_f_pos], [0], color='white', marker='x', label='Pusat (R)')

    # Fungsi Gambar Panah (Benda/Bayangan)
    def draw_arrow(x, y, h, color, label):
        ax.arrow(x, 0, 0, h, head_width=1.5, head_length=1.5, fc=color, ec=color, width=0.3, label=label)

    # 1. Gambar Benda (Selalu di Kiri / -x)
    x_obj = -s_val
    draw_arrow(x_obj, 0, h_obj, '#2ed573', "Benda")
    
    # 2. Gambar Bayangan
    if s_img != float('inf'):
        color_img = '#eccc68' if real else '#a29bfe'
        draw_arrow(x_img, 0, h_img, color_img, "Bayangan")
        
        # 3. Sinar Istimewa (Visualisasi)
        # Sinar 1: Sejajar -> Fokus
        if show_ray1:
            ax.plot([x_obj, 0], [h_obj, h_obj], 'w--', alpha=0.3) # Datang sejajar
            
            if not is_flat:
                if is_mirror:
                    # Pantul ke Fokus
                    target_x = -f if real else f # Cekung(Real) -> -f, Cembung -> +f? 
                    # Simplifikasi visual cermin:
                    # Cermin Cekung (f+): Pantul lewat Fokus di depan (-f)
                    # Cermin Cembung (f-): Pantul seolah dari Fokus di belakang (+f)
                    if "Cekung" in jenis_optik: focus_x = -abs(f)
                    else: focus_x = abs(f)
                    
                    # Persamaan garis dari (0, h_obj) lewat (focus_x, 0)
                    # y - 0 = m (x - fx)
                    m_ray = (h_obj - 0) / (0 - focus_x)
                    # Gambar perpanjangan
                    y_end = m_ray * (x_img - focus_x)
                    ax.plot([0, x_img], [h_obj, y_end], 'w--', alpha=0.3)
                    
                else: 
                    # Lensa: Bias ke F seberang (+f)
                    # Garis dari (0, h_obj) ke (f, 0)
                    ax.plot([0, x_img], [h_obj, h_img], 'w--', alpha=0.3)

        # Sinar 2: Lewat Pusat Optik
        if show_ray2:
             if is_mirror:
                 # Cermin: Pantul simetris di verteks
                 ax.plot([x_obj, 0], [h_obj, 0], 'c--', alpha=0.3)
                 ax.plot([0, x_obj], [0, -h_obj], 'c--', alpha=0.3) # Pantulan
             else:
                 # Lensa: Terus lurus lewat (0,0)
                 ax.plot([x_obj, x_img], [h_obj, h_img], 'c--', alpha=0.3)

    # Set Limit Plot
    limit = max(80, abs(x_obj) + 10, abs(x_img) + 10 if s_img != float('inf') else 0)
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-20, 20)
    ax.legend(facecolor='#2b2b2b', labelcolor='white')
    ax.set_title(f"Visualisasi: {jenis_optik}", color='white')
    
    st.pyplot(fig)

with col2:
    st.subheader("📊 Hasil Perhitungan")
    
    # Tampilkan Metrics
    c1, c2 = st.columns(2)
    c1.metric("Jarak Bayangan (s')", f"{s_img:.2f} cm" if s_img != float('inf') else "∞")
    c2.metric("Perbesaran (M)", f"{abs(m):.2f} x" if m != float('inf') else "∞")
    
    st.info(f"**Sifat Bayangan:**\n\n" + ", ".join(sifat_bayangan))
    
    # Debug info (Opsional)
    with st.expander("Detail Matematis"):
        st.write(f"""
        - Fokus (f): {f} cm
        - Posisi Benda (x): {-s_val} cm
        - Posisi Bayangan (x'): {x_img if s_img != float('inf') else 'Inf'} cm
        """)

# --- TABEL DATA & PANDUAN ---
tab1, tab2 = st.tabs(["📝 Data Praktikum", "📖 Panduan Modul"])

with tab1:
    st.write("Tabel ini simulasi penyimpanan data sementara.")
    # Inisialisasi session state untuk data jika belum ada
    if 'optik_data' not in st.session_state:
        st.session_state.optik_data = pd.DataFrame(columns=["Jenis", "f (cm)", "s (cm)", "h (cm)", "s' (cm)", "M (x)", "Sifat"])
    
    # Tombol Tambah Data (Triggered manual di sini untuk demonya)
    if st.button("➕ Masukkan Data ke Tabel"):
        new_data = {
            "Jenis": jenis_optik,
            "f (cm)": f,
            "s (cm)": s_val,
            "h (cm)": h_obj,
            "s' (cm)": round(s_img, 2) if s_img != float('inf') else "Inf",
            "M (x)": round(abs(m), 2) if m != float('inf') else "Inf",
            "Sifat": ", ".join(sifat_bayangan)
        }
        st.session_state.optik_data = pd.concat([st.session_state.optik_data, pd.DataFrame([new_data])], ignore_index=True)
        st.success("Data berhasil ditambahkan!")

    st.dataframe(st.session_state.optik_data, use_container_width=True)

with tab2:
    st.markdown("""
    ### HUKUM PEMANTULAN & PEMBIASAN (OPTIK GEOMETRI)
    
    **1. Hukum Gauss (Lensa & Cermin Tipis):**
    $$ \\frac{1}{f} = \\frac{1}{s} + \\frac{1}{s'} $$
    
    **2. Perbesaran Linear (Magnification):**
    $$ M = \\frac{h'}{h} = -\\frac{s'}{s} $$
    
    **3. Konvensi Tanda:**
    - **Benda Nyata (s > 0):** Benda di depan lensa/cermin.
    - **Bayangan Nyata (s' > 0):** Dapat ditangkap layar (terbalik).
    - **Bayangan Maya (s' < 0):** Tidak dapat ditangkap layar (tegak).
    """)
