import tkinter as tk
from tkinter import ttk, messagebox
import math
import numpy as np
from virtual_lab_data_manager import DataManager

class VirtualLabSpektrumAtom(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#f5f6fa")
        
        # Physics Constants
        self.R_H = 1.097e7      # m^-1
        self.h = 6.626e-34      # J.s
        self.c = 2.998e8        # m/s
        self.eV = 1.602e-19     # J
        
        self.setup_translations()
        self.lang = "ID"
        
        # Database
        self.spectra_db = {
            "Hidrogen (H)": {
                "lines": [656.3, 486.1, 434.0, 410.2], 
                "desc": "Deret Balmer (Tampak)",
                "transitions": ["3 -> 2", "4 -> 2", "5 -> 2", "6 -> 2"]
            },
            "Helium (He)": {
                "lines": [706.5, 667.8, 587.6, 501.6, 492.2, 471.3, 447.1],
                "desc": "Transisi Gas Mulia",
                "transitions": []
            },
            "Neon (Ne)": {
                "lines": [640.2, 633.4, 614.3, 609.6, 585.2, 540.1],
                "desc": "Cahaya Merah-Oranye Khas",
                "transitions": []
            },
            "Merkuri (Hg)": {
                "lines": [579.1, 577.0, 546.1, 435.8, 404.7],
                "desc": "Lampu Fluoresens",
                "transitions": []
            },
            "Natrium (Na)": {
                "lines": [589.0, 589.6], # Doublet
                "desc": "Doublet Kuning Dominan",
                "transitions": []
            }
        }
        
        self.selected_gas = "Hidrogen (H)"
        self.measured_lines = []
        
        self.setup_ui()
        self.set_language("id")
        self.draw_spectrum()
    
    def setup_translations(self):
        self.translations = {
            "ID": {
                "title": "SPEKTRUM ATOM & MODEL BOHR",
                "subtitle": "Analisis Spektrum Emisi & Transisi Elektron",
                "tab_exp": "Eksperimen Spektrometer",
                "tab_ana": "Analisis & Kalkulator Bohr",
                "tab_guide": "Petunjuk Praktikum",
                "tab_scheme": "Skema Alat & Penjelasan",
                "tab_diagram": "Gambaran Rangkaian Alat",
                "lbl_spec_view": "TAMPILAN SPEKTROMETER (VIRTUAL SPECTROMETER VIEW)",
                "lbl_info_start": "Pilih gas dan nyalakan tabung untuk melihat spektrum.",
                "lbl_select_gas": "PILIH SAMPEL GAS:",
                "btn_start": "NYALAKAN TABUNG",
                "btn_record": "CATAT SPEKTRUM",
                "btn_save": "☁️ Simpan (DB & Excel)",
                "col_gas": "Gas",
                "col_wl": "Pjg Gelombang (nm)",
                "col_color": "Warna",
                "btn_clear": "Hapus Data",
                "grp_photon": "Kalkulator Foton (E = h*c/lambda)",
                "lbl_lambda_in": "Lambda (nm):",
                "btn_calc_photon": "Hitung E & f",
                "res_photon_default": "Energi: - eV\nFrekuensi: - Hz",
                "grp_bohr": "Kalkulator Model Bohr (1/lambda = R_H * ...)",
                "lbl_ni": "Kulit Awal (ni):",
                "lbl_nf": "Kulit Akhir (nf):",
                "btn_calc_bohr": "Hitung Lambda Teoritis",
                "res_bohr_default": "Lambda Hitung: - nm\nSpektrum: -",
                "header_scheme": "Skema Alat Spektrometer Prisma/Kisi",
                "diag_table": "Meja Goniometer Spektrometer",
                "diag_collimator": "Kolimator",
                "diag_lamp": "Lampu\nSpektral",
                "diag_telescope": "Telescope",
                "diag_hv": "Catu Daya\nTegangan Tinggi (5kV)",
                "msg_saved": "Data berhasil disimpan!",
                "msg_no_data": "Belum ada data.",
                "err_invalid": "Masukkan angka valid",
                "err_bohr": "Syarat emisi: ni > nf dan nf >= 1",
                "lbl_data_log": "Data Pengamatan",
                "txt_guide": """PETUNJUK PRAKTIKUM SPEKTRUM ATOM (EMISSION SPECTROSCOPY)

A. TUJUAN
1. Mengamati spektrum emisi diskrit dari berbagai elemen (Hidrogen, Helium, Neon, dll).
2. Memahami hubungan panjang gelombang dengan transisi tingkat energi elektron.
3. Memverifikasi rumus Rydberg untuk atom Hidrogen.

B. DASAR TEORI
Menurut Model Bohr, elektron mengorbit inti pada tingkat energi diskrit. Ketika elektron "jatuh" dari kulit energi tinggi (ni) ke kulit energi rendah (nf), atom memancarkan foton dengan energi:
E = hf = h * c / lambda

Untuk Hidrogen, panjang gelombang dihitung dengan Rumus Rydberg:
1 / lambda = R_H * (1/nf^2 - 1/ni^2)

Dimana R_H = 1.097 x 10^7 m^-1.

C. PROSEDUR SIMULASI
1. Pilih Tabung Gas pada panel kontrol (misal: Hidrogen).
2. Klik tombol "NYALAKAN TABUNG".
3. Amati garis-garis berwarna yang muncul pada layar Spektrometer.
   - Posisi garis menunjukkan panjang gelombang.
   - Warna garis merepresentasikan energi foton (Ungu = Energi Tinggi, Merah = Energi Rendah).
4. Klik "CATAT SPEKTRUM" untuk menyimpan data ke tabel analisis.
5. Coba gas lain seperti Neon atau Merkuri untuk melihat perbedaan pola sidik jari (fingerprint) spektrum atom.

D. ANALISIS DATA
1. Gunakan 'Kalkulator Foton' untuk mengubah panjang gelombang (nm) menjadi Energi (eV).
2. Gunakan 'Kalkulator Model Bohr' untuk memprediksi panjang gelombang transisi (misal n=3 ke n=2). Bandingkan dengan hasil pengamatan Sinar Merah Hidrogen.""",
                "txt_scheme": """SKEMA ALAT DAN PENJELASAN

Eksperimen ini menggunakan spektrometer optik untuk menganalisis cahaya yang dipancarkan oleh atom tereksitasi.

KOMPONEN UTAMA:

1. Tabung Pelepasan Gas (Spectral Lamp)
   Tabung kaca berisi gas murni (Hidrogen, Helium, Neon, dll) pada tekanan rendah.
   Elektroda tegangan tinggi (High Voltage Power Supply ~5000V) memicu pelepasan muatan listrik dalam gas, menyebabkan elektron atom tereksitasi. Saat elektron kembali ke tingkat energi rendah, mereka memancarkan foton dengan panjang gelombang spesifik berwarna-warni.

2. Kolimator dengan Celah Sempit (Slit)
   Lensa kolimator berfungsi mensejajarkan berkas cahaya yang keluar dari celah sempit agar menjadi sinar paralel sebelum mengenai prisma/kisi.

3. Elemen Dispersi (Prisma Segitiga atau Kisi Difraksi)
   Komponen optik yang membiaskan cahaya berdasarkan panjang gelombangnya.
   - Cahaya merah (panjang gelombang panjang) dibelokkan paling sedikit (pada kisi) atau paling banyak (pada prisma - tergantung indeks bias).
   - Cahaya ungu/biru dibelokkan berbeda.
   Hal ini memecah cahaya polikromatik menjadi garis-garis spektrum terpisah.

4. Teleskop Pengamat
   Teleskop yang dapat diputar mengelilingi meja spektrometer untuk mengamati garis-garis spektrum yang tersebar pada sudut-sudut tertentu.

5. Skala Vernier
   Skala derajat presisi pada meja spektrometer untuk mengukur sudut deviasi setiap garis warna.

TUJUAN:
Menentukan panjang gelombang emisi atom dan memverifikasi model atom Bohr serta Konstanta Rydberg (khususnya untuk Hidrogen)."""
            },
            "EN": {
                "title": "ATOMIC SPECTRUM & BOHR MODEL",
                "subtitle": "Emission Spectrum Analysis & Electron Transitions",
                "tab_exp": "Spectrometer Experiment",
                "tab_ana": "Analysis & Bohr Calculator",
                "tab_guide": "User Guide",
                "tab_scheme": "Apparatus Scheme",
                "tab_diagram": "Circuit Diagram",
                "lbl_spec_view": "SPECTROMETER VIEW (VIRTUAL)",
                "lbl_info_start": "Select gas and turn on tube to view spectrum.",
                "lbl_select_gas": "SELECT GAS SAMPLE:",
                "btn_start": "TURN ON TUBE",
                "btn_record": "RECORD SPECTRUM",
                "btn_save": "☁️ Save (DB & Excel)",
                "col_gas": "Gas",
                "col_wl": "Wavelength (nm)",
                "col_color": "Color",
                "btn_clear": "Clear Data",
                "grp_photon": "Photon Calculator (E = h*c/lambda)",
                "lbl_lambda_in": "Lambda (nm):",
                "btn_calc_photon": "Calculate E & f",
                "res_photon_default": "Energy: - eV\nFrequency: - Hz",
                "grp_bohr": "Bohr Model Calculator",
                "lbl_ni": "Initial Shell (ni):",
                "lbl_nf": "Final Shell (nf):",
                "btn_calc_bohr": "Calc Theor. Lambda",
                "res_bohr_default": "Calc Lambda: - nm\nSpectrum: -",
                "header_scheme": "Prism/Grating Spectrometer Scheme",
                "diag_table": "Spectrometer Goniometer Table",
                "diag_collimator": "Collimator",
                "diag_lamp": "Spectral\nLamp",
                "diag_telescope": "Telescope",
                "diag_hv": "High Voltage\nSupply (5kV)",
                "msg_saved": "Data saved successfully!",
                "msg_no_data": "No data.",
                "err_invalid": "Enter valid number",
                "err_bohr": "Emission condition: ni > nf and nf >= 1",
                "lbl_data_log": "Observation Data",
                "txt_guide": """ATOMIC SPECTRUM LAB GUIDE (EMISSION SPECTROSCOPY)

A. OBJECTIVES
1. Observe discrete emission spectra of various elements (Hydrogen, Helium, Neon, etc).
2. Understand relation between wavelength and electron energy transitions.
3. Verify Rydberg formula for Hydrogen.

B. THEORY
According to Bohr Model, electrons orbit nucleus at discrete energy levels. When electrons "fall" from high energy (ni) to lower energy (nf), atoms emit photons with energy:
E = hf = h * c / lambda

For Hydrogen, wavelength is calculated by Rydberg Formula:
1 / lambda = R_H * (1/nf^2 - 1/ni^2)

Where R_H = 1.097 x 10^7 m^-1.

C. SIMULATION PROCEDURE
1. Select Gas Tube on control panel.
2. Click "TURN ON TUBE".
3. Observe colored lines on Spectrometer screen.
   - Position indicates wavelength.
   - Color represents photon energy.
4. Click "RECORD SPECTRUM" to save data.
5. Try other gases to see their unique fingerprints.

D. DATA ANALYSIS
1. Use 'Photon Calculator' to convert wavelength (nm) to Energy (eV).
2. Use 'Bohr Model Calculator' to predict transition wavelengths. Compare with observed Hydrogen Red Line.""",
                "txt_scheme": """APPARATUS SCHEME AND EXPLANATION

This experiment uses an optical spectrometer to analyze light emitted by excited atoms.

MAIN COMPONENTS:
1. Discharge Tube (Spectral Lamp)
   Glass tube with pure gas at low pressure. HV Supply triggers electrical discharge, exciting atoms. Returning electrons emit specific photons.

2. Collimator with Slit
   Aligns light into parallel beams.

3. Dispersion Element (Prism/Grating)
   Refracts light based on wavelength. Splitting polychromatic light into spectral lines.

4. Telescope
   Rotatable telescope to observe spectral lines at specific angles.

5. Vernier Scale
   For measuring deviation angles."""
            }
        }

    def T(self, key):
        return self.translations.get(self.lang, self.translations["ID"]).get(key, key)

    def set_language(self, lang):
        self.lang = lang
        self.refresh_ui()

    def refresh_ui(self):
        # Header
        self.lbl_title.config(text=self.T("title"))
        self.lbl_subtitle.config(text=self.T("subtitle"))
        
        # Tabs
        self.notebook.tab(self.tab_exp, text=self.T("tab_exp"))
        self.notebook.tab(self.tab_ana, text=self.T("tab_ana"))
        self.notebook.tab(self.tab_guide, text=self.T("tab_guide"))
        self.notebook.tab(self.tab_scheme, text=self.T("tab_scheme"))
        self.notebook.tab(self.tab_diagram, text=self.T("tab_diagram"))
        
        # Exp
        self.lbl_spec_view.config(text=self.T("lbl_spec_view"))
        self.lbl_select_gas.config(text=self.T("lbl_select_gas"))
        self.btn_start.config(text=self.T("btn_start"))
        self.btn_record.config(text=self.T("btn_record"))
        self.btn_save.config(text=self.T("btn_save"))
        
        # Ana
        self.lbl_data_log.config(text=self.T("lbl_data_log"))
        self.tree.heading("Gas", text=self.T("col_gas"))
        self.tree.heading("Pjg Gelombang (nm)", text=self.T("col_wl"))
        self.tree.heading("Warna", text=self.T("col_color"))
        self.btn_clear.config(text=self.T("btn_clear"))
        
        self.lf_photon.config(text=self.T("grp_photon"))
        self.lbl_lambda_in.config(text=self.T("lbl_lambda_in"))
        self.btn_calc_photon.config(text=self.T("btn_calc_photon"))
        
        self.lf_bohr.config(text=self.T("grp_bohr"))
        self.lbl_ni.config(text=self.T("lbl_ni"))
        self.lbl_nf.config(text=self.T("lbl_nf"))
        self.btn_calc_bohr.config(text=self.T("btn_calc_bohr"))
        
        # Guide
        self.txt_guide.config(state="normal")
        self.txt_guide.delete("1.0", tk.END)
        self.txt_guide.insert("1.0", self.T("txt_guide"))
        self.txt_guide.config(state="disabled")
        
        # Scheme
        self.lbl_scheme_title.config(text=self.T("header_scheme"))
        self.txt_scheme.config(state="normal")
        self.txt_scheme.delete("1.0", tk.END)
        self.txt_scheme.insert("1.0", self.T("txt_scheme"))
        self.txt_scheme.config(state="disabled")

        # Diagram Canvas items
        self.canvas_diag.itemconfigure("diag_table", text=self.T("diag_table"))
        self.canvas_diag.itemconfigure("diag_collimator", text=self.T("diag_collimator"))
        self.canvas_diag.itemconfigure("diag_lamp", text=self.T("diag_lamp"))
        self.canvas_diag.itemconfigure("diag_telescope", text=self.T("diag_telescope"))
        self.canvas_diag.itemconfigure("diag_hv", text=self.T("diag_hv"))

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg="#2c3e50", pady=15)
        header.pack(fill="x")
        self.lbl_title = tk.Label(header, text=self.T("title"), font=("Tw Cen MT", 20, "bold"), fg="#00cec9", bg="#2c3e50")
        self.lbl_title.pack()
        self.lbl_subtitle = tk.Label(header, text=self.T("subtitle"), font=("Arial", 11), fg="#dfe6e9", bg="#2c3e50")
        self.lbl_subtitle.pack()
        
        # Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_exp = tk.Frame(self.notebook, bg="#f5f6fa")
        self.tab_ana = tk.Frame(self.notebook, bg="#f5f6fa")
        self.tab_guide = tk.Frame(self.notebook, bg="#f5f6fa")
        self.tab_scheme = tk.Frame(self.notebook, bg="#f5f6fa")
        self.tab_diagram = tk.Frame(self.notebook, bg="#f5f6fa")
        
        self.notebook.add(self.tab_exp, text=self.T("tab_exp"))
        self.notebook.add(self.tab_ana, text=self.T("tab_ana"))
        self.notebook.add(self.tab_guide, text=self.T("tab_guide"))
        self.notebook.add(self.tab_scheme, text=self.T("tab_scheme"))
        self.notebook.add(self.tab_diagram, text=self.T("tab_diagram"))

        self.create_experiment_ui()
        self.create_analysis_ui()
        self.create_guide_ui()
        self.create_scheme_ui()
        self.create_diagram_ui()


    def create_diagram_ui(self):
        self.canvas_diag = tk.Canvas(self.tab_diagram, bg="white")
        self.canvas_diag.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Spectrometer Table Diagram (Top View)
        cx, cy = 400, 250
        r_table = 100
        
        # Circular Table
        self.canvas_diag.create_oval(cx-r_table, cy-r_table, cx+r_table, cy+r_table, fill="#95a5a6", outline="black")
        self.canvas_diag.create_text(cx, cy+r_table+20, text=self.T("diag_table"), font=("Arial", 11), tags="diag_table")
        
        # Prism
        self.canvas_diag.create_polygon(cx-20, cy-10, cx+20, cy-10, cx, cy+30, fill="#bdc3c7", outline="black") # Prism
        
        # Collimator Arm (Fixed)
        self.canvas_diag.create_line(150, 250, cx-r_table, 250, width=8, fill="black") # Tube
        self.canvas_diag.create_rectangle(140, 230, 160, 270, fill="black") # Slit holder
        self.canvas_diag.create_text(200, 270, text=self.T("diag_collimator"), font=("Arial", 10), tags="diag_collimator")
        
        # Light Source
        self.canvas_diag.create_rectangle(50, 220, 120, 280, fill="#e74c3c")
        self.canvas_diag.create_text(85, 250, text=self.T("diag_lamp"), font=("Arial", 9, "bold"), fill="white", tags="diag_lamp")
        
        # Telescope Arm (Rotatable)
        # Angled at ~45 deg
        tx = cx + 150
        ty = cy - 100
        self.canvas_diag.create_line(cx + 30, cy - 20, tx, ty, width=8, fill="black")
        self.canvas_diag.create_rectangle(tx, ty-10, tx+40, ty+10, fill="black") # Eyepiece
        self.canvas_diag.create_text(tx, ty+30, text=self.T("diag_telescope"), font=("Arial", 10), tags="diag_telescope")
        
        # Light Path
        self.canvas_diag.create_line(120, 250, cx, 250, fill="red", dash=(2,2)) # Incident
        self.canvas_diag.create_line(cx, 250, tx, ty, fill="blue", dash=(2,2)) # Refracted
        
        # HV Power Supply
        self.canvas_diag.create_rectangle(50, 350, 200, 450, fill="#2c3e50")
        self.canvas_diag.create_text(125, 400, text=self.T("diag_hv"), font=("Arial", 10, "bold"), fill="white", tags="diag_hv")
        self.canvas_diag.create_line(125, 350, 85, 280, fill="red", width=2, smooth=True)

    def create_scheme_ui(self):
        container = self.tab_scheme
        self.lbl_scheme_title = tk.Label(container, text=self.T("header_scheme"), 
                 font=("Arial", 16, "bold"), bg="#f5f6fa", fg="#2d3436")
        self.lbl_scheme_title.pack(pady=15)
        
        frame = tk.Frame(container, bg="white", bd=1, relief="solid")
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.txt_scheme = tk.Text(frame, font=("Arial", 12), wrap="word", padx=20, pady=20, bg="white", relief="flat")
        self.txt_scheme.pack(fill="both", expand=True)
        
        self.txt_scheme.insert("1.0", self.T("txt_scheme"))
        self.txt_scheme.config(state="disabled")


    def create_experiment_ui(self):
        layout = tk.Frame(self.tab_exp, bg="#f5f6fa")
        layout.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 1. Visualization Frame (TOP)
        viz_frame = tk.Frame(layout, bg="#2d3436")
        viz_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        
        # Emission Tube Viz
        self.canvas_tube = tk.Canvas(viz_frame, height=80, bg="#2d3436", highlightthickness=0)
        self.canvas_tube.pack(fill="x", padx=20, pady=10)
        
        # Spectrum Scale Viz
        self.lbl_spec_view = tk.Label(viz_frame, text=self.T("lbl_spec_view"), fg="white", bg="#2d3436", font=("Courier", 12))
        self.lbl_spec_view.pack(pady=(10, 0))
        
        self.canvas_spec = tk.Canvas(viz_frame, height=150, bg="black")
        self.canvas_spec.pack(fill="x", padx=20, pady=5)
        
        # Wavelength Scale
        self.canvas_scale = tk.Canvas(viz_frame, height=40, bg="#2d3436", highlightthickness=0)
        self.canvas_scale.pack(fill="x", padx=20, pady=0)
        
        # Info Box
        self.lbl_info = tk.Label(viz_frame, text=self.T("lbl_info_start"), 
                                 font=("Arial", 12, "italic"), fg="#f1c40f", bg="#2d3436")
        self.lbl_info.pack(pady=20)

        # 2. Controls Frame (BOTTOM)
        controls = tk.Frame(layout, bg="white", relief="raised", bd=1)
        controls.pack(side="bottom", fill="x", padx=5, pady=5)
        
        self.lbl_select_gas = tk.Label(controls, text=self.T("lbl_select_gas"), font=("Arial", 12, "bold"), bg="white")
        self.lbl_select_gas.pack(side="left", padx=20, pady=15)
        
        self.gas_var = tk.StringVar(value=self.selected_gas)
        gas_cb = ttk.Combobox(controls, values=list(self.spectra_db.keys()), textvariable=self.gas_var, state="readonly", font=("Arial", 12), width=20)
        gas_cb.pack(side="left", padx=10)
        gas_cb.bind("<<ComboboxSelected>>", self.on_gas_change)
        
        self.btn_start = tk.Button(controls, text=self.T("btn_start"), bg="#e74c3c", fg="black", highlightbackground="#e74c3c", font=("Arial", 11, "bold"),
                  command=self.animate_discharge)
        self.btn_start.pack(side="left", padx=20)
        
        self.btn_record = tk.Button(controls, text=self.T("btn_record"), bg="#3498db", fg="black", highlightbackground="#3498db", font=("Arial", 11, "bold"),
                  command=self.record_spectrum)
        self.btn_record.pack(side="right", padx=20)

        self.btn_save = tk.Button(controls, text=self.T("btn_save"), bg="#27ae60", fg="black", highlightbackground="#27ae60", font=("Arial", 11, "bold"),
                  command=self.save_to_all)
        self.btn_save.pack(side="right", padx=20)

    def create_analysis_ui(self):
        layout = tk.Frame(self.tab_ana, bg="white")
        layout.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left: Data Logger
        left = tk.Frame(layout, bg="white", width=400)
        left.pack(side="left", fill="y", padx=10)
        
        self.lbl_data_log = tk.Label(left, text=self.T("lbl_data_log"), font=("Arial", 12, "bold"), bg="white")
        self.lbl_data_log.pack(pady=10)
        cols = ("Gas", "Pjg Gelombang (nm)", "Warna")
        self.tree = ttk.Treeview(left, columns=cols, show="headings", height=15)
        for c in cols:
            self.tree.heading(c, text=c) # Translated in refresh_ui
            self.tree.column(c, width=120)
        self.tree.pack(fill="both", expand=True)
        
        self.btn_clear = tk.Button(left, text=self.T("btn_clear"), command=self.clear_data, bg="#c0392b", fg="black", highlightbackground="#c0392b")
        self.btn_clear.pack(fill="x", pady=5)
        
        # Right: Calculators
        right = tk.Frame(layout, bg="#f5f6fa", relief="sunken", bd=1)
        right.pack(side="left", fill="both", expand=True, padx=10)
        
        # Calculator 1: Energy & Frequency
        self.lf_photon = tk.LabelFrame(right, text=self.T("grp_photon"), bg="#f5f6fa", font=("Arial", 11, "bold"), padx=10, pady=10)
        self.lf_photon.pack(fill="x", padx=10, pady=10)
        
        self.lbl_lambda_in = tk.Label(self.lf_photon, text=self.T("lbl_lambda_in"), bg="#f5f6fa")
        self.lbl_lambda_in.grid(row=0, column=0, sticky="w")
        self.ent_lambda = tk.Entry(self.lf_photon)
        self.ent_lambda.grid(row=0, column=1, padx=5)
        
        self.btn_calc_photon = tk.Button(self.lf_photon, text=self.T("btn_calc_photon"), command=self.calc_photon, bg="#27ae60", fg="black", highlightbackground="#27ae60")
        self.btn_calc_photon.grid(row=0, column=2, padx=10)
        
        self.lbl_res_photon = tk.Label(self.lf_photon, text=self.T("res_photon_default"), justify="left", bg="#ecf0f1", width=30, relief="solid", bd=1)
        self.lbl_res_photon.grid(row=1, column=0, columnspan=3, pady=10, sticky="ew")
        
        # Calculator 2: Bohr Model (Hydrogen Only)
        self.lf_bohr = tk.LabelFrame(right, text=self.T("grp_bohr"), bg="#f5f6fa", font=("Arial", 11, "bold"), padx=10, pady=10)
        self.lf_bohr.pack(fill="x", padx=10, pady=10)
        
        self.lbl_ni = tk.Label(self.lf_bohr, text=self.T("lbl_ni"), bg="#f5f6fa")
        self.lbl_ni.grid(row=0, column=0, sticky="w")
        self.ent_ni = tk.Entry(self.lf_bohr, width=10)
        self.ent_ni.grid(row=0, column=1)
        
        self.lbl_nf = tk.Label(self.lf_bohr, text=self.T("lbl_nf"), bg="#f5f6fa")
        self.lbl_nf.grid(row=1, column=0, sticky="w")
        self.ent_nf = tk.Entry(self.lf_bohr, width=10)
        self.ent_nf.grid(row=1, column=1)
        
        self.btn_calc_bohr = tk.Button(self.lf_bohr, text=self.T("btn_calc_bohr"), command=self.calc_bohr, bg="#e67e22", fg="black", highlightbackground="#e67e22")
        self.btn_calc_bohr.grid(row=0, rowspan=2, column=2, padx=10) 
        
        self.lbl_res_bohr = tk.Label(self.lf_bohr, text=self.T("res_bohr_default"), justify="left", bg="#ecf0f1", width=30, relief="solid", bd=1)
        self.lbl_res_bohr.grid(row=2, column=0, columnspan=3, pady=10, sticky="ew")

    def create_guide_ui(self):
        self.txt_guide = tk.Text(self.tab_guide, font=("Arial", 12), padx=20, pady=20)
        self.txt_guide.pack(fill="both", expand=True)
        self.txt_guide.insert("1.0", self.T("txt_guide"))
        self.txt_guide.config(state="disabled")

    # --- Logic Methods ---
    
    def wavelength_to_hex(self, wl):
        """Simple approximation of Wavelength (nm) to RGB Hex"""
        gamma = 0.8
        intensity_max = 255
        
        if 380 <= wl <= 440:
            attenuation = 0.3 + 0.7 * (wl - 380) / (440 - 380)
            R = (-(wl - 440) / (440 - 380)) * attenuation
            G = 0.0
            B = 1.0 * attenuation
        elif 440 <= wl <= 490:
            R = 0.0
            G = (wl - 440) / (490 - 440)
            B = 1.0
        elif 490 <= wl <= 510:
            R = 0.0
            G = 1.0
            B = -(wl - 510) / (510 - 490)
        elif 510 <= wl <= 580:
            R = (wl - 510) / (580 - 510)
            G = 1.0
            B = 0.0
        elif 580 <= wl <= 645:
            R = 1.0
            G = -(wl - 645) / (645 - 580)
            B = 0.0
        elif 645 <= wl <= 780:
            attenuation = 0.3 + 0.7 * (780 - wl) / (780 - 645)
            R = 1.0 * attenuation
            G = 0.0
            B = 0.0
        else:
            return "#333333" # Invisible/UV/IR
            
        color = (int(R * 255), int(G * 255), int(B * 255))
        return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"

    def on_gas_change(self, event):
        self.canvas_spec.delete("lines")
        self.canvas_tube.delete("glow")
        self.lbl_info.config(text=self.T("lbl_info_start"))

    def save_to_all(self):
        data = self.get_data()
        success, msg = DataManager.save_data_unified(data, "SpektrumAtom")
        if success:
            messagebox.showinfo(self.T("msg_saved"), self.T("msg_saved"))
        else:
            messagebox.showwarning("Error", msg)

    def get_data(self):
        export = []
        # Tree columns: Gas, Pjg Gelombang (nm), Warna
        for child in self.tree.get_children():
            vals = self.tree.item(child)["values"]
            if vals:
                export.append({
                    "Gas": vals[0],
                    "Panjang Gelombang (nm)": vals[1],
                    "Warna": vals[2]
                })
        return export

    def animate_discharge(self):
        self.is_on = True # State tracking for refresh_ui
        gas_data = self.spectra_db[self.gas_var.get()]
        
        # 1. Tube Glow Animation
        # Average color of spectrum
        lines = gas_data["lines"]
        if lines:
            avg_wl = sum(lines)/len(lines)
            glow_col = self.wavelength_to_hex(avg_wl)
        else:
            glow_col = "#ffffff"
            
        w_tube = self.canvas_tube.winfo_width()
        cy_tube = 40
        
        self.canvas_tube.create_rectangle(100, 20, w_tube-100, 60, fill="#222", outline="gray", width=2, tags="tube")
        self.canvas_tube.create_rectangle(105, 25, w_tube-105, 55, fill=glow_col, outline="", tags="glow", stipple="gray50")
        
        # 2. Draw Spectrum Lines
        self.draw_spectrum_lines(lines)
        
        desc = gas_data["desc"]
        self.lbl_info.config(text=f"{self.gas_var.get()}: {desc}")

    def draw_spectrum_lines(self, lines):
        self.canvas_spec.delete("lines")
        
        w = self.canvas_spec.winfo_width()
        h = self.canvas_spec.winfo_height()
        
        # Visible Range: 380 - 750 nm on X axis
        min_wl = 380
        max_wl = 750
        range_wl = max_wl - min_wl
        
        for wl in lines:
            if min_wl <= wl <= max_wl:
                x_pos = ((wl - min_wl) / range_wl) * w
                color = self.wavelength_to_hex(wl)
                
                # Draw Line
                # Glow effect
                self.canvas_spec.create_line(x_pos, 0, x_pos, h, fill=color, width=4, tags="lines", stipple="gray50")
                self.canvas_spec.create_line(x_pos, 0, x_pos, h, fill=color, width=2, tags="lines")
                
                # Label
                self.canvas_spec.create_text(x_pos, h-10, text=f"{wl:.1f}", fill="white", angle=90, anchor="e", tags="lines", font=("Arial", 8))

    def draw_spectrum(self):
        # Initial draw of scale
        self.update() # Ensure dimensions
        w = self.canvas_scale.winfo_width()
        if w < 10: w = 400
        
        min_wl = 380
        max_wl = 750
        
        # Draw ticks
        for wl in range(400, 751, 50):
            x = ((wl - min_wl) / (max_wl - min_wl)) * w
            self.canvas_scale.create_line(x, 0, x, 15, fill="gray")
            self.canvas_scale.create_text(x, 25, text=str(wl), fill="gray", font=("Arial", 9))

    def record_spectrum(self):
        gas = self.gas_var.get()
        lines = self.spectra_db[gas]["lines"]
        
        for wl in lines:
            # Check if approximate data already there to avoid dupes? Nah just add
            c_hex = self.wavelength_to_hex(wl)
            # Map hex to simple name if possible, or just use hex
            self.tree.insert("", "end", values=(gas, f"{wl:.1f}", c_hex))
            
            # Save to list for export
            self.measured_lines.append({
                "Modul": "Spektrum Atom",
                "Element": gas,
                "Wavelength (nm)": wl,
                "Color (Hex)": c_hex
            })
    
    def get_data(self):
        return self.measured_lines

    def clear_data(self):
        self.measured_lines = []
        for i in self.tree.get_children():
            self.tree.delete(i)

    def calc_photon(self):
        try:
            wl_nm = float(self.ent_lambda.get())
            if wl_nm <= 0: return
            
            # E = hc / lambda
            wl_m = wl_nm * 1e-9
            E_joule = self.h * self.c / wl_m
            E_eV = E_joule / self.eV
            f_Hz = self.c / wl_m
            
            res = f"Energi: {E_eV:.3f} eV\nFrekuensi: {f_Hz/1e14:.2f} x10^14 Hz"
            self.lbl_res_photon.config(text=res, fg="blue")
        except ValueError:
            messagebox.showerror(self.T("error"), self.T("err_invalid"))

    def calc_bohr(self):
        try:
            ni = int(self.ent_ni.get())
            nf = int(self.ent_nf.get())
            
            if nf >= ni or nf < 1:
                messagebox.showwarning("Fisika Error", self.T("err_bohr"))
                return
            
            # 1/lambda = R * (1/nf^2 - 1/ni^2)
            term = (1.0/nf**2) - (1.0/ni**2)
            inv_lambda = self.R_H * term
            lambda_m = 1.0 / inv_lambda
            lambda_nm = lambda_m * 1e9
            
            # Determine Series
            series = "Lyman (UV)" if nf==1 else "Balmer (Tampak)" if nf==2 else "Paschen (IR)" if nf==3 else "Lainnya"
            
            res = f"Lambda: {lambda_nm:.2f} nm\nDeret: {series}"
            self.lbl_res_bohr.config(text=res, fg="green")
            
        except ValueError:
            messagebox.showerror(self.T("error"), self.T("err_invalid"))

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabSpektrumAtom(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
