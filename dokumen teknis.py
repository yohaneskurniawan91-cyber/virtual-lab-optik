import os
import glob
import ast
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

# --- UTILITY: DYNAMIC MODULE SCANNER ---
def get_dynamic_module_catalog(search_path="."):
    modules = []
    # Manual categorization map for Modern Physics topics
    topic_map = {
        # Fisika Kuantum
        "fotoefek": "Kuantisasi Energi", "planck": "Radiasi Benda Hitam", 
        "compton": "Hamburan Foton", "stefan": "Radiasi Termal", "wien": "Radiasi Termal",
        # Fisika Atom
        "bohr": "Model Atom", "rydberg": "Spektroskopi Atom", 
        "frank": "Tingkat Energi", "hertz": "Tingkat Energi",
        "zeeman": "Medan Magnet Atomik", "stern": "Spin Elektron", "gerlach": "Spin Elektron",
        # Relativitas
        "relativitas": "Relativitas Khusus", "lorentz": "Transformasi Koordinat", 
        "michelson": "Interferometri", "morley": "Interferometri",
        # Inti & Zat Padat
        "radioaktif": "Fisika Inti", "peluruh": "Fisika Inti", "waktu_paruh": "Fisika Inti",
        "geiger": "Deteksi Radiasi", "muller": "Deteksi Radiasi",
        "hall": "Efek Hall (Zat Padat)", "band_gap": "Pita Energi"
    }

    try:
        files = sorted(glob.glob(os.path.join(search_path, "*.py")))
        module_counter = 0
        for filepath in files:
            filename = os.path.basename(filepath)
            if filename in ["dokumen teknis.py", "setup.py", "virtual_lab_data_manager.py", 
                           "virtual_lab_fisika_dasar.py", "virtual_lab_fisika_modern.py"]:
                continue
                
            topic = ""
            lower_name = filename.lower()
            mapped = False
            for key, val in topic_map.items():
                if key in lower_name:
                    topic = val
                    mapped = True
                    break
            
            if not mapped: continue # STRICT FILTER

            module_counter += 1
            focus = "Simulasi Fenomena Kuantum & Subatomik"
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())
                    docstring = ast.get_docstring(tree)
                    if docstring:
                        clean_doc = docstring.strip().split('\n')[0]
                        focus = (clean_doc[:75] + '..') if len(clean_doc) > 75 else clean_doc
            except Exception: pass
            
            modules.append([str(module_counter), filename, topic, focus])
    except Exception as e:
        print(f"Warning: {e}")
        modules.append(["1", "efek_fotolistrik.py", "Kuantisasi Energi", "Simulasi Emisi Elektron akibat Foton"])

    if not modules:
        modules.append(["-", "Tidak ditemukan modul terinstall", "-", "-"])
    return modules

# --- PDF GENERATION HELPERS ---
def on_cover_page(canvas, doc):
    canvas.saveState()
    # Background Accent
    canvas.setFillColorRGB(0.17, 0.24, 0.31) # #2c3e50
    canvas.rect(0, A4[1]*0.7, A4[0], A4[1]*0.3, fill=1, stroke=0)
    
    # Text Elements
    canvas.setFont("Helvetica-Bold", 36)
    canvas.setFillColor(colors.white)
    canvas.drawRightString(A4[0] - 2*cm, A4[1]*0.85, "DOKUMENTASI TEKNIS")
    
    canvas.setFont("Helvetica-Bold", 18)
    canvas.setFillColorRGB(0.1, 0.74, 0.61) # #1abc9c
    canvas.drawRightString(A4[0] - 2*cm, A4[1]*0.82, "VIRTUAL LAB FISIKA MODERN")
    
    canvas.setStrokeColor(colors.white)
    canvas.setLineWidth(4)
    canvas.line(2*cm, A4[1]*0.80, A4[0]-2*cm, A4[1]*0.80)
    
    canvas.setFont("Times-Roman", 16)
    canvas.setFillColor(colors.black)
    canvas.drawString(2*cm, A4[1]*0.60, "Platform Simulasi Eksperimen Fisika Kuantum & Relativitas")
    canvas.setFont("Times-Italic", 14)
    canvas.drawString(2*cm, A4[1]*0.57, "Comprehensive Technical Reference v2.1")
    
    # Bottom Footer
    canvas.setFillColorRGB(0.17, 0.24, 0.31)
    canvas.rect(0, 0, A4[0], 1.5*cm, fill=1, stroke=0)
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.white)
    canvas.drawCentredString(A4[0]/2, 0.5*cm, "© 2026 Laboratorium Fisika Modern - JK Learning Media")
    canvas.restoreState()

def on_content_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.gray)
    canvas.drawCentredString(A4[0]/2, 1*cm, f"Halaman {doc.page} | Virtual Lab Fisika Modern")
    canvas.restoreState()

def build_pdf(output_filename="Dokumentasi_Teknis_VL_Modern.pdf"):
    doc = SimpleDocTemplate(output_filename, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    
    # Custom Styles
    style_h1 = ParagraphStyle('Header1', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=24, textColor=colors.HexColor('#2c3e50'), spaceAfter=20, alignment=TA_CENTER)
    style_h2 = ParagraphStyle('Header2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=16, textColor=colors.HexColor('#2c3e50'), spaceBefore=20, spaceAfter=10, borderPadding=5, borderBottomColor=colors.gray, borderBottomWidth=1)
    style_h3 = ParagraphStyle('Header3', parent=styles['Heading3'], fontName='Helvetica-Bold', fontSize=13, textColor=colors.HexColor('#16a085'), spaceBefore=15, spaceAfter=5)
    style_body = ParagraphStyle('BodyCustom', parent=styles['Normal'], fontName='Times-Roman', fontSize=11, leading=16, alignment=TA_JUSTIFY, spaceAfter=10)
    style_code = ParagraphStyle('CodeCustom', parent=styles['Code'], fontName='Courier', fontSize=9, backColor=colors.HexColor('#f0f0f0'), borderPadding=10, spaceAfter=10)
    style_toc = ParagraphStyle('TOC', parent=styles['Normal'], fontName='Helvetica', fontSize=11, spaceAfter=5)
    
    story = []
    
    # --- PAGE 1: COVER INFO ---
    story.append(Spacer(1, 12*cm)) 
    data_info = [
        ['Nama Sistem', 'Virtual Lab Fisika Modern (VL-Modern)'],
        ['Versi Rilis', '2.1.0 (Stable Build 2026)'],
        ['Basis Teknologi', 'Python 3.11, SciPy, Tkinter'],
        ['Pengembang', 'Yohanes Kurniawan & Tim R&D'],
        ['Institusi', 'Unika Santu Paulus Ruteng']
    ]
    t_info = Table(data_info, colWidths=[5*cm, 10*cm])
    t_info.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#2c3e50')),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
    ]))
    story.append(t_info)
    story.append(PageBreak())
    
    # --- PAGE 2: APPROVAL ---
    story.append(Paragraph("LEMBAR PENGESAHAN & VALIDASI", style_h2))
    story.append(Paragraph("Dokumen ini menyatakan bahwa perangkat lunak telah melalui tahap pengujian alpha dan beta, serta memenuhi standar kurikulum Fisika Modern KKNI Level 6.", style_body))
    story.append(Spacer(1, 2*cm))
    
    data_sig = [
        ["Disetujui Oleh,\nKaprodi Pendidikan Fisika\n\n\n\n______________________\nDr. Nurussaniah, M.Si", 
         "Divalidasi Oleh,\nKepala Lab. Komputasi\n\n\n\n______________________\nYohanes Kurniawan, M.Pd"]
    ]
    t_sig = Table(data_sig, colWidths=[8*cm, 8*cm])
    t_sig.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold')]))
    story.append(t_sig)
    story.append(PageBreak())
    
    # --- PAGE 3: ABSTRACT ---
    story.append(Paragraph("RINGKASAN EKSEKUTIF (EXECUTIVE SUMMARY)", style_h2))
    story.append(Paragraph("Virtual Lab Fisika Modern adalah solusi perangkat lunak pendidikan yang dirancang untuk mengatasi kesenjangan antara teori abstrak fisika kuantum dengan fenomena teramati. Menggunakan mesin komputasi numerik Python (SciPy), sistem ini mampu mensimulasikan perilaku probabilistik partikel subatomik dengan akurasi tinggi.", style_body))
    story.append(Paragraph("Fitur kunci meliputi: (1) Simulasi Real-time, (2) Visualisasi Grafik Dinamis, (3) Manajemen Data Mahasiswa Terpusat, dan (4) Skalabilitas Modul Plugin. Sistem dioptimalkan untuk berjalan pada perangkat desktop standar dengan overhead komputasi minimal.", style_body))
    story.append(PageBreak())
    
    # --- PAGE 4: TOC ---
    story.append(Paragraph("DAFTAR ISI LENGKAP", style_h2))
    chapters = [
        "1. PENDAHULUAN & LATAR BELAKANG", "2. ARSITEKTUR TEKNIS SISTEM", 
        "3. PETA KONSEP & KATALOG MODUL", "4. STRUKTUR DATABASE & CLOUD", 
        "5. ALUR KERJA PENGGUNA (USER JOURNEY)", "6. SPESIFIKASI API & PAYLOAD", 
        "7. JAMINAN KUALITAS (QA & VALIDASI)", "8. PANDUAN PENGEMBANGAN MODUL", 
        "9. ANALISIS RISIKO & MITIGASI", "10. MAINTENANCE & SUPPORT", 
        "11. SPESIFIKASI LINGKUNGAN", "12. LISENSI & HAK CIPTA"
    ]
    for ch in chapters: story.append(Paragraph(ch, style_toc))
    story.append(PageBreak())

    # --- CH 1 ---
    story.append(Paragraph("1. PENDAHULUAN & LATAR BELAKANG", style_h2))
    story.append(Paragraph("Fisika Modern mencakup fenomena yang terjadi pada skala atomik atau kecepatan relativistik, yang tidak dapat diakses melalui indera manusia secara langsung. Laboratorium konvensional untuk materi ini (seperti Tabung Sinar Katoda, Sumber Radioaktif, Interferometer Michelson) memiliki harga sangat mahal dan risiko keselamatan tinggi.", style_body))
    
    story.append(Paragraph("Tujuan Pengembangan:", style_h3))
    goals = [
        "• Menyediakan alat visualisasi konsep abstrak (fungsi gelombang, dilatasi waktu).",
        "• Menggantikan peralatan praktikum berisiko tinggi (zat radioaktif) dengan simulasi aman.",
        "• Memfasilitasi pengambilan data kuantitatif untuk analisis mahasiswa.",
        "• Integrasi penilaian otomatis melalui sinkronisasi data cloud."
    ]
    for g in goals: story.append(Paragraph(g, style_body))

    # --- CH 2 ---
    story.append(Paragraph("2. ARSITEKTUR TEKNIS SISTEM", style_h2))
    story.append(Paragraph("Sistem dibangun di atas arsitektur <b>Plugin-based Monolith</b>. Core Application (Runner) menangani window management, navigasi, dan I/O, sementara setiap eksperimen adalah modul terpisah yang dimuat saat runtime.", style_body))
    
    story.append(Paragraph("Struktur Direktori Proyek:", style_h3))
    dir_struct = """
ROOT_PROJECT/
├── virtual_lab_fisika_modern.py  [CORE RUNNER]
├── virtual_lab_data_manager.py   [DATA CONTROLLER]
├── db_config.json                [CONFIG]
├── student_profile.json          [LOCAL SESSION]
├── modules/ (Logical Grouping)
│   ├── efek_fotolistrik.py       [PLUGIN MODULE]
│   ├── hamburan_compton.py       [PLUGIN MODULE]
│   └── ...
├── assets/                       [IMAGES/ICONS]
└── setup.py                      [BUILD SCRIPT]
"""
    story.append(Preformatted(dir_struct, style_code))

    # --- CH 3 ---
    story.append(Paragraph("3. PETA KONSEP & KATALOG MODUL", style_h2))
    story.append(Paragraph("Berikut adalah matriks kesesuaian antara modul eksperimen dengan Capaian Pembelajaran Mata Kuliah (CPMK) Fisika Modern:", style_body))
    
    modules = get_dynamic_module_catalog()
    header = ['No', 'File Modul', 'Topik Utama', 'Fokus Simulasi']
    t_mod = Table([header] + modules, colWidths=[1.5*cm, 5*cm, 4*cm, 6.5*cm])
    t_mod.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (1,0), (-1,-1), [colors.whitesmoke, colors.white])
    ]))
    story.append(t_mod)
    story.append(PageBreak())

    # --- CH 4 ---
    story.append(Paragraph("4. STRUKTUR DATABASE & CLOUD", style_h2))
    story.append(Paragraph("Sistem menggunakan pendekatan <b>Hybrid Persistence</b> untuk menjamin ketersediaan data dalam kondisi online maupun offline.", style_body))
    
    db_table = [
        ['Layer', 'Teknologi', 'Fungsi Utama', 'Keterkondisian'],
        ['L1: Session', 'JSON/RAM', 'Menyimpan State Identitas Sementara', 'Saat Aplikasi Jalan'],
        ['L2: Local', 'Excel (.xlsx)', 'Backup Fisik Data Eksperimen', 'Offline Support'],
        ['L3: Cloud', 'Google Sheets API', 'Sentralisasi Data Kelas', 'Online Only']
    ]
    t_db = Table(db_table, colWidths=[3*cm, 4*cm, 6*cm, 4*cm])
    t_db.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
    ]))
    story.append(t_db)

    # --- CH 5 ---
    story.append(Paragraph("5. ALUR KERJA PENGGUNA (USER JOURNEY)", style_h2))
    story.append(Paragraph("Panduan langkah-demi-langkah penggunaan aplikasi oleh mahasiswa:", style_body))
    
    steps = [
        "<b>1. Autentikasi Awal:</b> Pengguna membuka aplikasi dan wajib mengisi form identitas (Nama, NIM, Kelas). Data ini dikunci selama sesi berlangsung.",
        "<b>2. Seleksi Eksperimen:</b> Pengguna memilih topik eksperimen dari Tab Navigasi.",
        "<b>3. Manipulasi Variabel:</b> Pengguna mengubah 'Independent Variable' (misal: Tegangan) menggunakan slider.",
        "<b>4. Observasi Data:</b> Pengguna mengamati perubahan pada 'Dependent Variable' (misal: Arus) melalui grafik real-time.",
        "<b>5. Recording:</b> Klik 'Ambil Data' untuk membekukan nilai sesaat ke dalam tabel sementara.",
        "<b>6. Finalisasi:</b> Klik 'Simpan Data' untuk memicu ekspor ke Excel dan Cloud."
    ]
    for s in steps: story.append(Paragraph(s, style_body))

    # --- CH 6 ---
    story.append(Paragraph("6. SPESIFIKASI API & PAYLOAD", style_h2))
    story.append(Paragraph("Endpoint Google Apps Script:", style_code))
    story.append(Paragraph("Method: <code>POST</code> (application/json)", style_body))
    story.append(Paragraph("JSON Payload Sample:", style_h3))
    
    json_sample = """{
  "nama": "Mahasiswa A",
  "nim": "2020001",
  "kelas": "FIS-A",
  "module": "Efek Fotolistrik",
  "timestamp": "2026-02-10T10:00:00",
  "experiment_data": [
    {"v_stop": 1.2, "frequency": 5.4e14, "current": 0.0},
    {"v_stop": 1.5, "frequency": 6.0e14, "current": 0.1}
  ]
}"""
    story.append(Preformatted(json_sample, style_code))

    # --- CH 7 ---
    story.append(Paragraph("7. JAMINAN KUALITAS (QA & VALIDASI)", style_h2))
    story.append(Paragraph("Tabel berikut merangkum skenario pengujian yang dilakukan sebelum rilis:", style_body))
    qa_data = [
        ['Kode', 'Komponen', 'Metode Uji', 'Hasil / Toleransi'],
        ['QA-PHY-01', 'Konstanta Planck', 'Validasi Numerik', 'Error < 0.5% vs CODATA'],
        ['QA-PHY-02', 'Peluruhan Inti', 'Monte Carlo Test', 'Distribusi Poisson Sesuai'],
        ['QA-SYS-01', 'Offline Mode', 'Network Interruption', 'Data tersimpan di Excel'],
        ['QA-SYS-02', 'High Load Plotting', 'Stress Test', 'Maks 1000 titik data @ 60fps'],
        ['QA-UX-01', 'Responsivitas UI', 'Resize Window', 'Elemen UI tata letak otomatis']
    ]
    t_qa = Table(qa_data, colWidths=[3*cm, 4*cm, 4*cm, 6*cm])
    t_qa.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2980b9')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTSIZE', (0,0), (-1,-1), 9)
    ]))
    story.append(t_qa)
    story.append(PageBreak())

    # --- CH 8 ---
    story.append(Paragraph("8. PANDUAN PENGEMBANGAN MODUL", style_h2))
    story.append(Paragraph("Untuk menambahkan eksperimen baru, ikuti kontrak antarmuka berikut:", style_body))
    dev_steps = [
        "1. Buat file .py baru di direktori root.",
        "2. Buat class dengan nama yang mengandung kata 'Lab' atau 'Virtual'.",
        "3. Konstruktor <code>__init__</code> harus menerima argumen <code>parent</code>.",
        "4. Gunakan <code>ScrollableFrame</code> sebagai container utama.",
        "5. Daftarkan file ke dalam list <code>LAB_MODULES</code> di Runner."
    ]
    for d in dev_steps: story.append(Paragraph(d, style_body))

    # --- CH 9 (NEW) ---
    story.append(Paragraph("9. ANALISIS RISIKO & MITIGASI", style_h2))
    risk_data = [
        ['Risiko', 'Dampak', 'Strategi Mitigasi'],
        ['Kehilangan Koneksi', 'Data cloud gagal terkirim', 'Implementasi fallback ke Excel Lokal'],
        ['Bug Perhitungan', 'Miskonsepsi mahasiswa', 'Unit Testing pada modul fisika inti'],
        ['Kompatibilitas OS', 'Tampilan UI rusak', 'Penggunaan standar Tkinter cross-platform'],
        ['Injeksi Data', 'Kerusakan data kelas', 'Validasi token API pada sisi Server (GAS)']
    ]
    t_risk = Table(risk_data, colWidths=[4*cm, 5*cm, 8*cm])
    t_risk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#c0392b')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_risk)

    # --- CH 10 (NEW) ---
    story.append(Paragraph("10. MAINTENANCE & SUPPORT", style_h2))
    story.append(Paragraph("Jadwal pemeliharaan berkala meliputi:", style_body))
    story.append(Paragraph("• <b>Update Dependensi:</b> Setiap 6 bulan (numpy, scipy, matplotlib).", style_body))
    story.append(Paragraph("• <b>Clear Cache:</b> Pembersihan folder __pycache__ sebelum rilis baru.", style_body))
    story.append(Paragraph("• <b>Kontak Support:</b> helpdesk@labfisika-modern.ac.id", style_body))

    # --- CH 11 ---
    story.append(Paragraph("11. SPESIFIKASI LINGKUNGAN", style_h2))
    spec_data = [
        ['Komponen', 'Minimum', 'Rekomendasi'],
        ['OS', 'Windows 10 / macOS 11', 'Windows 11 / macOS 14 (Sonoma)'],
        ['CPU', 'Intel Core i3 (2.0 GHz)', 'Intel Core i5 / Apple Silicon M1'],
        ['RAM', '4 GB', '8 GB'],
        ['Display', '1366 x 768', '1920 x 1080 (Full HD)']
    ]
    t_spec = Table(spec_data, colWidths=[4*cm, 6*cm, 7*cm])
    t_spec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
    ]))
    story.append(t_spec)

    # --- CH 12 ---
    story.append(Paragraph("12. LISENSI & HAK CIPTA", style_h2))
    story.append(Paragraph("Copyright © 2026 Laboratorium Fisika Modern.", style_body))
    story.append(Paragraph("Aplikasi ini didistribusikan untuk kalangan internal Universitas di bawah lisensi pendidikan tertutup. Dilarang keras memperbanyak, memodifikasi, atau menjual kembali kode sumber tanpa izin tertulis dari pengembang utama.", style_body))

    # Generate
    doc.build(story, onFirstPage=on_cover_page, onLaterPages=on_content_page)
    print(f"Success! PDF generated: {output_filename}")

if __name__ == "__main__":
    build_pdf()
