import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from virtual_lab_data_manager import DataManager, ScrollableFrame

class VirtualLabEfekFotolistrik(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#f5f6fa")
        
        # Translations
        self.lang = "ID"
        self.setup_translations()
        
        # Physics Constants
        self.h_real = 6.626e-34
        self.c = 2.998e8
        self.e = 1.602e-19
        
        # Data Model
        self.materials_data = {
            "cesium": {"val": 2.14, "id": "Bahan A (Cesium)", "en": "Material A (Cesium)"},
            "kalium": {"val": 2.30, "id": "Bahan B (Kalium)", "en": "Material B (Potassium)"},
            "natrium": {"val": 2.36, "id": "Bahan C (Natrium)", "en": "Material C (Sodium)"},
            "mystery": {"val": random.uniform(2.0, 2.5), "id": "Bahan X (Misterius)", "en": "Material X (Mystery)"}
        }
        self.selected_material_key = "cesium"
        self.phi_eV = self.materials_data[self.selected_material_key]["val"]
        
        # Filters Map (key -> nm)
        self.filters_data = {
            "uv": 365,
            "violet": 405,
            "blue": 436,
            "green": 546,
            "yellow": 577
        }
        self.current_filter_key = "green"
        
        # State
        self.voltage = 0.0
        self.is_light_on = False
        self.is_calibrated = False
        self.measured_current = 0.0
        self.data_points = []
        self.electrons = []
        
        # Parsing Layout
        self.scale_factor = 2.0
        self.offset_x = 100
        self.offset_y = 50
        
        self.running = True
        self.create_widgets()

    def start_animation(self):
        if not self.running:
            self.running = True
            if self.is_light_on:
                self.animate_electrons()

    def stop_animation(self):
        self.running = False

    def setup_translations(self):
        self.translations = {
            "ID": {
                "title": "Laboratorium Efek Fotolistrik & Fungsi Kerja Logam",
                "tab_exp": "Eksperimen",
                "tab_analysis": "Analisis & Grafik",
                "tab_guide": "Petunjuk Praktikum",
                "tab_scheme": "Skema Alat & Penjelasan",
                "tab_diagram": "Gambaran Rangkaian Alat",
                "header_device": "1. Pengaturan Alat",
                "btn_calibrate": "Kalibrasi Ammeter (Zeroing)",
                "lbl_not_calibrated": "Belum Dikalibrasi",
                "lbl_calibrated": "Terkalibrasi",
                "lbl_material": "Material Katoda:",
                "btn_light_on": "NYALAKAN SUMBER CAHAYA",
                "btn_light_off": "MATIKAN SUMBER CAHAYA",
                "header_filter": "2. Filter / Panjang Gelombang",
                "header_voltage": "3. Tegangan Penghenti (Volt)",
                "btn_save": "Simpan Data (Catat V stop)",
                "col_filter": "Filter",
                "col_vs": "Vs (V)",
                "header_analysis": "Tabel Analisis",
                "col_freq": "Frekuensi (Hz)",
                "btn_calc": "Hitung Fungsi Kerja (W0)",
                "filter_uv": "UV (365 nm)",
                "filter_violet": "Ungu (405 nm)",
                "filter_blue": "Biru (436 nm)",
                "filter_green": "Hijau (546 nm)",
                "filter_yellow": "Kuning (577 nm)",
                "mat_cesium": "Bahan A (Cesium)",
                "mat_kalium": "Bahan B (Kalium)",
                "mat_natrium": "Bahan C (Natrium)",
                "mat_mystery": "Bahan X (Misterius)",
                "header_scheme": "Skema Alat Efek Fotolistrik",
                "text_scheme": """SKEMA ALAT DAN PENJELASAN

Eksperimen ini dirancang untuk menyelidiki karakteristik emisi elektron dari berbagai jenis logam katoda.

DAFTAR PERALATAN:

1. Modul Lampu Merkuri
   Menghasilkan cahaya polikromatik kuat yang mengandung spektrum garis merkuri yang tajam (UV hingga Kuning).

2. Roda Filter (Filter Wheel)
   Berisi filter interverensi sempit yang memungkinkan pemilihan panjang gelombang tunggal dari spektrum lampu merkuri untuk menyinari katoda.

3. Sel Fotolistrik (Vacuum Photocell)
   Komponen inti berupa tabung hampa udara berisi:
   - Katoda dapat diganti (Simulasi): Permukaan logam peka cahaya (seperti Cesium, Kalium).
   - Anoda Kawat: Elektroda tipis untuk menangkap elektron tanpa menghalangi cahaya masuk.

4. Unit Kontrol Tegangan & Ammeter (Picoammeter) (Unit h/e)
   Mengatur tegangan bias pada sel fotolistrik dan mengukur arus yang sangat kecil yang dihasilkan oleh fotoelektron (orde 10^-9 hingga 10^-13 Ampere).

FUNGSI UTAMA:
Menentukan 'Fungsi Kerja' (Work Function) dari berbagai material logam, yaitu energi minimum yang diperlukan elektron untuk lepas dari ikatan logam.""",
                "text_guide": """PETUNJUK PRAKTIKUM EFEK FOTOLISTRIK

A. TUJUAN
1. Menentukan potensial penghenti (Stopping Potential) untuk berbagai panjang gelombang cahaya.
2. Menghitung konstanta Planck (h).
3. Menghitung Fungsi Kerja (Work Function) dari material katoda.

B. CALIBRATION (PENTING)
Sebelum memulai pengukuran, tekan tombol "Kalibrasi Ammeter". Ini memastikan pembacaan arus nol saat gelap.

C. PROSEDUR PERCOBAAN
1. Pilih Jenis Bahan Katoda (misal: Bahan A).
2. Pilih Filter Warna pertama (misal: Kuning).
3. Nyalakan Sumber Cahaya. Cek Ammeter, seharusnya ada arus (nA) jika energi foton cukup.
4. Naikkan Tegangan Penghenti (Volts) secara perlahan.
   - Perhatikan nilai arus yang semakin turun.
   - Cari tegangan terkecil dimana arus TEPAT menjadi 0.000 nA.
   - Nilai tegangan ini adalah Potensial Penghenti (Vs).
5. Klik "Simpan Data (Catat V stop)". Data akan masuk ke tabel.
6. Ulangi untuk filter warna lain (Hijau, Biru, Ungu, UV).

D. ANALISIS
1. Pindah ke tab "Analisis & Grafik".
2. Klik "Hitung Fungsi Kerja".
3. Grafik Vs vs Frekuensi akan muncul. Perpotongan garis dengan sumbu X adalah Frekuensi Ambang (f0).
4. Fungsi Kerja (W0) = h * f0.
5. Bandingkan nilai W0 hasil eksperimen dengan teori.

E. PENYIMPANAN DATA
1. Pastikan data sudah terkumpul di tabel Analisis.
2. Klik tombol "☁️ Simpan Database & Excel" di tab Analisis.""",
                "msg_calibrate": "Ammeter berhasil dikalibrasi (Zero Point Set).",
                "msg_material_change": "Mengganti material akan menghapus data saat ini. Lanjutkan?",
                "msg_min_data": "Butuh minimal 2 titik data.",
                "lbl_result": "Hasil Analysis: (Klik Hitung)",
                "res_fmt": "Slope = {slope:.2e}\nh (Calc) = {h_calc:.2e} J.s\nError h = {err:.2f}%\n\nW0 (Fungsi Kerja) = {W_calc_eV:.2f} eV\nf0 (Threshold) = {f0:.2e} Hz",
                "graph_title": "Hubungan Frekuensi Cahaya vs Tegangan Penghenti",
                "graph_xlabel": "Frekuensi (Hz)",
                "graph_ylabel": "Tegangan Penghenti / V_stop (Volt)",
                "simpan_data": "Simpan Data",
                "simpan_db": "☁️ Simpan Database & Excel",
                "reset_data": "Reset Data",
                "diag_hg_lamp": "Hg Lamp Housing",
                "diag_filter": "Filter Wheel",
                "diag_photocell": "Photocell Head",
                "diag_measure": "h/e Measurement Base",
                "diag_stop_volt": "STOPPING VOLTAGE",
                "diag_zero": "Zero Current",
                "diag_volt_adj": "Voltage Adj",
                "diag_cathode": "Cathode (-)",
                "diag_anode": "Anode (+)",
                "diag_housing": "Phototube Unit",
                "diag_lamp": "Hg Lamp"
            },
            "EN": {
                "title": "Photoelectric Effect & Work Function Laboratory",
                "tab_exp": "Experiment",
                "tab_analysis": "Analysis & Graph",
                "tab_guide": "Guide",
                "tab_scheme": "Apparatus Scheme",
                "tab_diagram": "Apparatus Diagram",
                "header_device": "1. Device Setup",
                "btn_calibrate": "Calibrate Ammeter (Zeroing)",
                "lbl_not_calibrated": "Not Calibrated",
                "lbl_calibrated": "Calibrated",
                "lbl_material": "Cathode Material:",
                "btn_light_on": "TURN ON LIGHT SOURCE",
                "btn_light_off": "TURN OFF LIGHT SOURCE",
                "header_filter": "2. Filter / Wavelength",
                "header_voltage": "3. Stopping Voltage (Volt)",
                "btn_save": "Save Data (Record Vs)",
                "col_filter": "Filter",
                "col_vs": "Vs (V)",
                "header_analysis": "Analysis Table",
                "col_freq": "Frequency (Hz)",
                "btn_calc": "Calculate Work Function (W0)",
                "filter_uv": "UV (365 nm)",
                "filter_violet": "Violet (405 nm)",
                "filter_blue": "Blue (436 nm)",
                "filter_green": "Green (546 nm)",
                "filter_yellow": "Yellow (577 nm)",
                "mat_cesium": "Material A (Cesium)",
                "mat_kalium": "Material B (Potassium)",
                "mat_natrium": "Material C (Sodium)",
                "mat_mystery": "Material X (Mystery)",
                "header_scheme": "Photoelectric Effect Scheme",
                "text_scheme": """APPARATUS SCHEME AND EXPLANATION

This experiment is designed to investigate the electron emission characteristics of various cathode metals.

EQUIPMENT LIST:

1. Mercury Lamp Module
   Produces strong polychromatic light containing sharp mercury line spectrum (UV to Yellow).

2. Filter Wheel
   Contains narrow interference filters allowing selection of a single wavelength from the mercury spectrum to illuminate the cathode.

3. Photoelectric Cell (Vacuum Photocell)
   Core component consisting of a vacuum tube containing:
   - Replaceable Cathode (Simulated): Light-sensitive metal surface (like Cesium, Potassium).
   - Wire Anode: Thin electrode to capture electrons without blocking incoming light.

4. Voltage Control & Ammeter Unit (Picoammeter) (h/e Unit)
   Regulates bias voltage on the photocell and measures the very small current generated by photoelectrons (order of 10^-9 to 10^-13 Amperes).

MAIN FUNCTION:
Determining the 'Work Function' of various metal materials, which is the minimum energy required for an electron to escape from the metal bond.""",
                "text_guide": """PHOTOELECTRIC EFFECT LAB GUIDE

A. OBJECTIVE
1. Determine the Stopping Potential for various light wavelengths.
2. Calculate Planck's constant (h).
3. Calculate the Work Function of the cathode material.

B. CALIBRATION (IMPORTANT)
Before starting measurements, press "Calibrate Ammeter". This ensures zero current reading when dark.

C. EXPERIMENT PROCEDURE
1. Select Cathode Material Type (e.g., Material A).
2. Select first Color Filter (e.g., Yellow).
3. Turn On Light Source. Check Ammeter, there should be current (nA) if photon energy is sufficient.
4. Increase Stopping Voltage (Volts) slowly.
   - Observe the current value decreasing.
   - Find the smallest voltage where current EXACTLY becomes 0.000 nA.
   - This voltage is the Stopping Potential (Vs).
5. Click "Save Data (Record Vs)". Data will be added to the table.
6. Repeat for other color filters (Green, Blue, Violet, UV).

D. ANALYSIS
1. Switch to "Analysis & Graph" tab.
2. Click "Calculate Work Function".
3. Vs vs Frequency graph will appear. The intersection with X-axis is the Threshold Frequency (f0).
4. Work Function (W0) = h * f0.
5. Compare experimental W0 value with theory.

E. DATA SAVING
1. Ensure data is collected in the Analysis table.
2. Click "☁️ Save Database & Excel" button in the Analysis tab.""",
                "msg_calibrate": "Ammeter calibrated successfully (Zero Point Set).",
                "msg_material_change": "Changing material will clear current data. Continue?",
                "msg_min_data": "Need at least 2 data points.",
                "lbl_result": "Analysis Result: (Click Calculate)",
                "res_fmt": "Slope = {slope:.2e}\nh (Calc) = {h_calc:.2e} J.s\nError h = {err:.2f}%\n\nW0 (Work Func) = {W_calc_eV:.2f} eV\nf0 (Threshold) = {f0:.2e} Hz",
                "graph_title": "Light Frequency vs Stopping Voltage",
                "graph_xlabel": "Frequency (Hz)",
                "graph_ylabel": "Stopping Voltage / V_stop (Volt)",
                "simpan_data": "Save Data",
                "simpan_db": "☁️ Save Database & Excel",
                "reset_data": "Reset Data",
                "diag_hg_lamp": "Hg Lamp Housing",
                "diag_filter": "Filter Wheel",
                "diag_photocell": "Photocell Head",
                "diag_measure": "h/e Measurement Base",
                "diag_stop_volt": "STOPPING VOLTAGE",
                "diag_zero": "Zero Current",
                "diag_volt_adj": "Voltage Adj",
                "diag_cathode": "Cathode (-)",
                "diag_anode": "Anode (+)",
                "diag_housing": "Phototube Unit",
                "diag_lamp": "Hg Lamp"
            }
        }

    def T(self, key):
        return self.translations.get(self.lang, self.translations["ID"]).get(key, key)

    def set_language(self, lang):
        self.lang = lang
        self.refresh_ui()

    def refresh_ui(self):
        # Tabs
        if hasattr(self, 'notebook'):
            self.notebook.tab(self.tab_exp, text=self.T("tab_exp"))
            self.notebook.tab(self.tab_analysis, text=self.T("tab_analysis"))
            self.notebook.tab(self.tab_guide, text=self.T("tab_guide"))
            self.notebook.tab(self.tab_scheme, text=self.T("tab_scheme"))
            self.notebook.tab(self.tab_diagram, text=self.T("tab_diagram"))
        
        # Header & Controls
        if hasattr(self, 'lbl_title'): self.lbl_title.config(text=self.T("title"))
        if hasattr(self, 'lbl_device'): self.lbl_device.config(text=self.T("header_device"))
        if hasattr(self, 'btn_cal'): self.btn_cal.config(text=self.T("btn_calibrate"))
        if hasattr(self, 'status_lbl'):
             state_key = "lbl_calibrated" if self.is_calibrated else "lbl_not_calibrated"
             self.status_lbl.config(text=self.T(state_key))
        if hasattr(self, 'lbl_mat'): self.lbl_mat.config(text=self.T("lbl_material"))
        
        # Material Combo
        if hasattr(self, 'mat_menu'):
             vals = [self.materials_data[k][self.lang.lower()] for k in self.materials_data]
             self.mat_menu.config(values=vals)
             current_key = self.selected_material_key
             self.mat_var.set(self.materials_data[current_key][self.lang.lower()])
        
        # Light Button
        if hasattr(self, 'btn_light'):
             state_key = "btn_light_off" if self.is_light_on else "btn_light_on"
             self.btn_light.config(text=self.T(state_key))
        
        # Filter & Voltage Label
        if hasattr(self, 'lbl_filter_head'): self.lbl_filter_head.config(text=self.T("header_filter"))
        if hasattr(self, 'filter_rbtns'):
             for key, rbtn in self.filter_rbtns.items():
                 rbtn.config(text=self.T(f"filter_{key}"))
        if hasattr(self, 'lbl_volt_head'): self.lbl_volt_head.config(text=self.T("header_voltage"))
        if hasattr(self, 'btn_save'): self.btn_save.config(text=self.T("btn_save"))
        
        # Mini Table
        if hasattr(self, 'tree_mini'):
            self.tree_mini.heading("Filter", text=self.T("col_filter"))
            self.tree_mini.heading("Vs", text=self.T("col_vs"))
            # Update rows content if needed (filter names) - skipping for simplicity as it records historical
            
        # Analysis Tab
        if hasattr(self, 'lbl_analysis_head'): self.lbl_analysis_head.config(text=self.T("header_analysis"))
        if hasattr(self, 'tree_full'):
             self.tree_full.heading("Freq", text=self.T("col_freq"))
             self.tree_full.heading("Vs", text=self.T("col_vs"))
        if hasattr(self, 'btn_calc_w0'): self.btn_calc_w0.config(text=self.T("btn_calc"))
        
        if hasattr(self, 'frame_save_lbl'): self.frame_save_lbl.config(text=self.T("simpan_data"))
        if hasattr(self, 'btn_simpan_all'): self.btn_simpan_all.config(text=self.T("simpan_db"))
        if hasattr(self, 'btn_reset'): self.btn_reset.config(text=self.T("reset_data"))
        
        # Scheme Tab
        if hasattr(self, 'lbl_scheme_title'): self.lbl_scheme_title.config(text=self.T("header_scheme"))
        if hasattr(self, 'text_scheme'):
            self.text_scheme.config(state="normal")
            self.text_scheme.delete("1.0", "end")
            self.text_scheme.insert("1.0", self.T("text_scheme"))
            self.text_scheme.config(state="disabled")
            
        # Guide Tab
        if hasattr(self, 'text_guide'):
            self.text_guide.config(state="normal")
            self.text_guide.delete("1.0", "end")
            self.text_guide.insert("1.0", self.T("text_guide"))
            self.text_guide.config(state="disabled")

        # Diagram Tab - Redraw
        if hasattr(self, 'canvas'): self.draw_apparatus()
        if hasattr(self, 'canvas_diagram'): # Separate canvas for tab_diagram
            self.draw_tab_diagram_canvas()

        # Update Graph Titles
        if hasattr(self, 'ax'):
            self.ax.set_title(self.T("graph_title"))
            self.ax.set_xlabel(self.T("graph_xlabel"))
            self.ax.set_ylabel(self.T("graph_ylabel"))
            self.canvas_graph.draw()
        
    def create_widgets(self):
        # Header
        header = tk.Frame(self, bg="#2d3436", pady=10)
        header.pack(fill="x")
        self.lbl_title = tk.Label(header, text=self.T("title"), 
                 font=("Helvetica", 18, "bold"), fg="white", bg="#2d3436")
        self.lbl_title.pack()
        
        # Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Experiment
        self.tab_exp = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_exp, text=self.T("tab_exp"))
        self.create_tab_experiment()
        
        # Tab 2: Analysis
        self.tab_analysis = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_analysis, text=self.T("tab_analysis"))
        self.create_tab_analysis()
        
        # Tab 3: Guide
        self.tab_guide = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_guide, text=self.T("tab_guide"))
        self.create_tab_guide()

        # Tab 4: Tools Scheme
        self.tab_scheme = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_scheme, text=self.T("tab_scheme"))
        self.create_tab_scheme()

        # Tab 5: Real Diagram
        self.tab_diagram = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_diagram, text=self.T("tab_diagram"))
        self.create_tab_diagram()

    def create_tab_scheme(self):
        # Full Layout text
        container = self.tab_scheme
        self.lbl_scheme_title = tk.Label(container, text=self.T("header_scheme"), 
                 font=("Arial", 16, "bold"), bg="#f5f6fa", fg="#2d3436")
        self.lbl_scheme_title.pack(pady=15)
        
        frame = tk.Frame(container, bg="white", bd=1, relief="solid")
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.text_scheme = tk.Text(frame, font=("Arial", 12), wrap="word", padx=20, pady=20, bg="white", relief="flat")
        self.text_scheme.pack(fill="both", expand=True)

        self.text_scheme.insert("1.0", self.T("text_scheme"))
        self.text_scheme.config(state="disabled")

    def create_tab_diagram(self):
        # Full Layout Canvas
        self.canvas_diagram = tk.Canvas(self.tab_diagram, bg="white")
        self.canvas_diagram.pack(fill="both", expand=True, padx=20, pady=20)
        self.draw_tab_diagram_canvas()
        
    def draw_tab_diagram_canvas(self):
        self.canvas_diagram.delete("all")
        canvas = self.canvas_diagram
        
        # Draw Diagram (Static)
        # 1. Light Source (Mercury Lamp)
        canvas.create_rectangle(50, 200, 180, 350, fill="#7f8c8d", outline="black")
        canvas.create_text(115, 365, text=self.T("diag_hg_lamp"), font=("Arial", 11, "bold"))
        # Lamp window
        canvas.create_rectangle(180, 250, 200, 300, fill="#f1c40f") # Beam Exit
        
        # 2. Filter Wheel
        canvas.create_oval(210, 200, 250, 350, fill="#3498db", outline="black")
        canvas.create_text(230, 365, text=self.T("diag_filter"), font=("Arial", 10))
        
        # 3. Main Unit (Photodiode Box)
        canvas.create_rectangle(270, 220, 450, 330, fill="#ecf0f1", outline="black", width=2)
        canvas.create_text(360, 210, text=self.T("diag_photocell"), font=("Arial", 11, "bold"))
        
        # Aperture
        canvas.create_rectangle(270, 260, 280, 290, fill="black")
        
        # 4. Measurement Console (Pasco style h/e unit)
        canvas.create_rectangle(500, 150, 750, 350, fill="#2c3e50")
        canvas.create_text(625, 365, text=self.T("diag_measure"), font=("Arial", 11, "bold"))
        
        # Digital Display
        canvas.create_rectangle(530, 180, 720, 240, fill="#27ae60")
        canvas.create_text(625, 210, text=self.T("diag_stop_volt"), fill="#2ecc71", font=("Arial", 10))
        canvas.create_text(625, 230, text="1.45 V", font=("Ds-Digital", 20), fill="black")
        
        # Null Indicator (Zero Current)
        canvas.create_oval(550, 260, 600, 310, fill="white", outline="gray")
        canvas.create_line(575, 285, 575, 265, width=2, fill="red") # Needle
        canvas.create_text(575, 320, text=self.T("diag_zero"), font=("Arial", 9), fill="white")
        
        # Knobs
        canvas.create_oval(650, 270, 690, 310, fill="gray", outline="white")
        canvas.create_text(670, 320, text=self.T("diag_volt_adj"), fill="white", font=("Arial", 9))
        
        # Connections
        canvas.create_line(450, 275, 500, 275, width=4, fill="#34495e") # Multi-pin cable
        
        # Beam path
        canvas.create_line(200, 275, 275, 275, fill="cyan", width=2, dash=(6,2), arrow="last")



    def create_tab_experiment(self):
        # NEW LAYOUT: Top (Canvas) and Bottom (Controls) for better visualization
        container = self.tab_exp
        
        # 1. Visualization Area (Top, Large)
        viz_frame = tk.Frame(container, bg="#2d3436", bd=2, relief="sunken")
        viz_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(viz_frame, bg="#2d3436", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.draw_apparatus()
        
        # 2. Control Panel (Bottom, Fixed Height)
        control_panel = tk.Frame(container, bg="white", bd=2, relief="raised", height=250)
        control_panel.pack(side="bottom", fill="x", padx=5, pady=5)
        # control_panel.pack_propagate(False) # Let it shrink to fit content
        
        # Use Grid for control columns
        control_panel.columnconfigure(0, weight=1)
        control_panel.columnconfigure(1, weight=1)
        control_panel.columnconfigure(2, weight=1)
        
        # --- Column 1: Setup Device ---
        col1 = tk.Frame(control_panel, bg="white")
        col1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.lbl_device = tk.Label(col1, text=self.T("header_device"), font=("Arial", 12, "bold"), bg="white", fg="#2980b9")
        self.lbl_device.pack(anchor="w")
        
        # Calibration
        self.btn_cal = tk.Button(col1, text=self.T("btn_calibrate"), bg="#bdc3c7", 
                  command=self.calibrate_instrument)
        self.btn_cal.pack(fill="x", pady=5)
        self.status_lbl = tk.Label(col1, text=self.T("lbl_not_calibrated"), fg="red", bg="white", font=("Arial", 9))
        self.status_lbl.pack()
        
        # Material
        self.lbl_mat = tk.Label(col1, text=self.T("lbl_material"), bg="white")
        self.lbl_mat.pack(anchor="w", pady=(5,0))
        
        # Material Combobox
        # Initial Value
        initial_val = self.materials_data[self.selected_material_key][self.lang.lower()]
        self.mat_var = tk.StringVar(value=initial_val)
        
        vals = [self.materials_data[k][self.lang.lower()] for k in self.materials_data]
        self.mat_menu = ttk.Combobox(col1, textvariable=self.mat_var, values=vals, state="readonly")
        self.mat_menu.pack(fill="x")
        self.mat_menu.bind("<<ComboboxSelected>>", self.change_material)
        
        # Lamp Switch
        self.btn_light = tk.Button(col1, text=self.T("btn_light_on"), bg="#f1c40f", font=("Arial", 10, "bold"),
                                   command=self.toggle_light)
        self.btn_light.pack(fill="x", pady=(10,0))

        # --- Column 2: Experiment vars ---
        col2 = tk.Frame(control_panel, bg="white")
        col2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Filter
        self.lbl_filter_head = tk.Label(col2, text=self.T("header_filter"), font=("Arial", 12, "bold"), bg="white", fg="#2980b9")
        self.lbl_filter_head.pack(anchor="w")
        
        self.filter_var = tk.StringVar(value=self.current_filter_key)
        
        f_frame = tk.Frame(col2, bg="white")
        f_frame.pack(fill="x", pady=5)
        
        # Grid filters 2 cols
        self.filter_rbtns = {}
        sorted_keys = sorted(self.filters_data.keys(), key=lambda k: self.filters_data[k])
        for i, k in enumerate(sorted_keys):
            display_txt = self.T(f"filter_{k}")
            if k == self.current_filter_key:
                # Ensure correct check
                self.filter_var.set(k)
                
            rb = tk.Radiobutton(f_frame, text=display_txt, variable=self.filter_var, value=k, bg="white", 
                           command=self.update_simulation)
            rb.grid(row=i//2, column=i%2, sticky="w")
            self.filter_rbtns[k] = rb
                           
        # Voltage
        self.lbl_volt_head = tk.Label(col2, text=self.T("header_voltage"), font=("Arial", 12, "bold"), bg="white", fg="#2980b9")
        self.lbl_volt_head.pack(anchor="w", pady=(10,0))
        self.volt_var = tk.DoubleVar(value=0.0)
        tk.Scale(col2, from_=0.0, to=4.0, resolution=0.01, orient="horizontal", 
                 variable=self.volt_var, bg="white", length=300,
                 command=lambda x: self.update_simulation()).pack(fill="x")

        # --- Column 3: Data & Readings ---
        col3 = tk.Frame(control_panel, bg="white")
        col3.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        
        # Ammeter Display
        disp_frame = tk.Frame(col3, bg="black", bd=3, relief="sunken")
        disp_frame.pack(fill="x")
        self.lbl_ammeter = tk.Label(disp_frame, text="0.000 nA", font=("Courier New", 20, "bold"), fg="#00ff00", bg="black")
        self.lbl_ammeter.pack(pady=5)
        
        # Save Button
        self.btn_save = tk.Button(col3, text=self.T("btn_save"), bg="#3498db", fg="black", font=("Arial", 11, "bold"),
                  command=self.record_data)
        self.btn_save.pack(fill="x", pady=10)
                  
        # Mini Table
        cols = ("Filter", "Vs")
        self.tree_mini = ttk.Treeview(col3, columns=cols, show="headings", height=4)
        self.tree_mini.heading("Filter", text=self.T("col_filter"))
        self.tree_mini.heading("Vs", text=self.T("col_vs"))
        self.tree_mini.column("Filter", width=120)
        self.tree_mini.column("Vs", width=80)
        self.tree_mini.pack(fill="both", expand=True)

    def create_tab_analysis(self):
        # NEW LAYOUT: Table Left (Smaller), Graph Right (Larger)
        container = self.tab_analysis
        
        # Left: Table & Analysis
        left_panel = tk.Frame(container, bg="white", bd=1, relief="solid", width=350)
        left_panel.pack(side="left", fill="y", padx=10, pady=10)
        
        self.lbl_analysis_head = tk.Label(left_panel, text=self.T("header_analysis"), font=("Arial", 14, "bold"), bg="white")
        self.lbl_analysis_head.pack(pady=10)
        
        cols = ("Freq", "Vs")
        self.tree_full = ttk.Treeview(left_panel, columns=cols, show="headings", height=10)
        self.tree_full.heading("Freq", text=self.T("col_freq"))
        self.tree_full.heading("Vs", text=self.T("col_vs"))
        self.tree_full.pack(fill="x", padx=10)
        
        self.btn_calc_w0 = tk.Button(left_panel, text=self.T("btn_calc"), bg="#9b59b6", fg="black", font=("Arial", 12, "bold"),
                  command=self.analyze_data)
        self.btn_calc_w0.pack(fill="x", padx=20, pady=20)
                  
        self.lbl_analysis_res = tk.Label(left_panel, text=self.T("lbl_result"), 
                                         font=("Arial", 12), bg="white", justify="left")
        self.lbl_analysis_res.pack(pady=10, padx=20, anchor="w")
        
        # Save Buttons (Database & Excel)
        self.frame_save_lbl = tk.LabelFrame(left_panel, text=self.T("simpan_data"), bg="white", font=("Arial", 10, "bold"))
        self.frame_save_lbl.pack(fill="x", padx=20, pady=10)
        
        self.btn_simpan_all = tk.Button(self.frame_save_lbl, text=self.T("simpan_db"), command=self.save_to_all, 
                  bg="#27ae60", fg="black")
        self.btn_simpan_all.pack(fill="x", padx=10, pady=5)
        
        self.btn_reset = tk.Button(left_panel, text=self.T("reset_data"), bg="#e74c3c", fg="black", command=self.reset_data)
        self.btn_reset.pack(fill="x", padx=20, pady=30, side="bottom")

        # Right: Graph Area (Matplotlib)
        right_panel = tk.Frame(container, bg="white")
        right_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.ax.set_title(self.T("graph_title"))
        self.ax.set_xlabel(self.T("graph_xlabel"))
        self.ax.set_ylabel(self.T("graph_ylabel"))
        self.ax.grid(True)
        
        self.canvas_graph = FigureCanvasTkAgg(self.fig, master=right_panel)
        self.canvas_graph.get_tk_widget().pack(fill="both", expand=True)
        
        # Toolbar
        toolbar = NavigationToolbar2Tk(self.canvas_graph, right_panel)
        toolbar.update()
        toolbar.pack(side="bottom", fill="x")

    def save_to_all(self):
        data = self.get_data()
        success, msg = DataManager.save_data_unified(data, "EfekFotolistrik")
        if success:
            messagebox.showinfo("Status", msg)
        else:
            messagebox.showwarning("Status", msg)

    def create_tab_guide(self):
        container = self.tab_guide
        
        frame = tk.Frame(container)
        frame.pack(fill="both", expand=True)

        self.text_guide = tk.Text(frame, font=("Arial", 12), padx=20, pady=20, wrap="word")
        scr = ttk.Scrollbar(frame, command=self.text_guide.yview)
        self.text_guide.configure(yscrollcommand=scr.set)
        
        scr.pack(side="right", fill="y")
        self.text_guide.pack(side="left", fill="both", expand=True)

        self.text_guide.insert("1.0", self.T("text_guide"))
        self.text_guide.config(state="disabled")

    def draw_apparatus(self):
        self.canvas.delete("all")
        
        W = self.canvas.winfo_width()
        H = self.canvas.winfo_height()
        if W < 100: W = 800
        if H < 100: H = 400
        
        CY = H / 2
        S = 1.2 
        
        # Draw Optical Bench (Rail)
        self.canvas.create_rectangle(50, CY + 80, W - 50, CY + 100, fill="#7f8c8d", outline="#95a5a6")
        
        # --- 1. Light Source (Left) ---
        lamp_x = 100
        lamp_w = 120
        lamp_h = 140
        self.canvas.create_rectangle(lamp_x, CY - lamp_h/2, lamp_x + lamp_w, CY + lamp_h/2, 
                                     fill="#2c3e50", outline="#bdc3c7", width=2, tags="lamp_housing")
        # Lamp Bulb Icon
        self.canvas.create_oval(lamp_x + 40, CY - 20, lamp_x + 80, CY + 20, fill="#f1c40f", outline="#f39c12")
        self.canvas.create_text(lamp_x + lamp_w/2, CY + lamp_h/2 + 20, text=self.T("diag_lamp"), fill="white", font=("Arial", 11, "bold"))
        
        # --- 2. Filter Wheel (Middle) ---
        filter_x = lamp_x + lamp_w + 60
        filter_r = 45
        # Draw Holder
        self.canvas.create_oval(filter_x, CY - filter_r, filter_x + 2*filter_r, CY + filter_r, 
                                fill="#34495e", outline="white", width=2, tags="filter_holder")
        self.canvas.create_text(filter_x + filter_r, CY + filter_r + 25, text=self.T("col_filter"), fill="white", font=("Arial", 11))

        # --- 3. Vacuum Phototube (Right) ---
        tube_cx = filter_x + 280
        tube_rx = 90
        tube_ry = 90
        
        # Glass Bulb
        self.canvas.create_oval(tube_cx - tube_rx, CY - tube_ry, tube_cx + tube_rx, CY + tube_ry,
                                outline="#a29bfe", width=3, fill="#2d3436") 
        
        # Cathode (C-shaped Plate) - Target for light
        # Left side of bulb
        self.canvas.create_arc(tube_cx - tube_rx + 15, CY - tube_ry + 15, tube_cx + tube_rx - 15, CY + tube_ry - 15,
                               start=110, extent=140, style="arc", outline="#bdc3c7", width=6, tags="cathode")
        
        # Anode (Thin Rod) - Collector
        anode_x = tube_cx + 50
        self.canvas.create_line(anode_x, CY - 40, anode_x, CY + 40, fill="#e74c3c", width=4, tags="anode")
        
        self.canvas.create_text(tube_cx, CY + tube_ry + 25, text=self.T("diag_photocell"), fill="white", font=("Arial", 11, "bold"))
        
        # Store key coords for update
        self.coords = {
            'lamp_out_x': lamp_x + lamp_w,
            'filter_in_x': filter_x,
            'filter_out_x': filter_x + 2*filter_r,
            'filter_center_x': filter_x + filter_r,
            'filter_center_y': CY,
            'cathode_hit_x': tube_cx - tube_rx/2 + 10, 
            'anode_x': anode_x,
            'beam_y': CY,
            'tube_rx': tube_rx,
            'tube_cx': tube_cx
        }

    def animate_electrons(self):
        if not self.running: return

        if not self.is_light_on:
            self.canvas.delete("electron")
            self.electrons = []
            return

        # 1. Move existing electrons
        surviving_electrons = []
        for e in self.electrons:
            # Move
            e['x'] += e['vx']
            # Draw
            self.canvas.coords(e['id'], e['x']-3, e['y']-3, e['x']+3, e['y']+3)
            
            # Check collision
            if e['x'] >= self.coords['anode_x']:
                self.canvas.delete(e['id']) # Absorbed
            elif e['x'] < self.coords['cathode_hit_x']:
                self.canvas.delete(e['id']) # Backwards?
            else:
                surviving_electrons.append(e)
        self.electrons = surviving_electrons
        
        # 2. Spawn new electrons if V < Vstop
        # spawn rate proportional to current
        measure = getattr(self, 'measured_current', 0)
        spawn_chance = min(0.8, measure * 0.15) 
        
        if random.random() < spawn_chance:
            y_spread = random.uniform(-20, 20)
            y = self.coords['beam_y'] + y_spread
            x = self.coords['cathode_hit_x']
            
            vx = 6 # Speed
            
            e_id = self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="#2ecc71", outline="#27ae60", tags="electron")
            self.electrons.append({'id': e_id, 'x': x, 'y': y, 'vx': vx})
            
        self.after(30, self.animate_electrons)
        
    def calibrate_instrument(self):
        # Fake delay
        self.is_calibrated = True
        self.status_lbl.config(text=self.T("lbl_calibrated"), fg="green")
        messagebox.showinfo("Kalibrasi", self.T("msg_calibrate"))
        self.update_simulation()
        
    def change_material(self, event):
        selected_val = self.mat_var.get()
        found_key = self.selected_material_key
        for k, v in self.materials_data.items():
            if v[self.lang.lower()] == selected_val:
                found_key = k
                break
        
        if found_key != self.selected_material_key:
             if self.data_points:
                ans = messagebox.askyesno("Ganti Material", self.T("msg_material_change"))
                if ans:
                    self.reset_data()
                    self.selected_material_key = found_key
                    self.phi_eV = self.materials_data[found_key]["val"]
                else:
                    self.mat_var.set(self.materials_data[self.selected_material_key][self.lang.lower()])
                    return
             else:
                self.selected_material_key = found_key
                self.phi_eV = self.materials_data[found_key]["val"]
                
        self.update_simulation()

    def toggle_light(self):
        self.is_light_on = not self.is_light_on
        if self.is_light_on:
            self.btn_light.config(text=self.T("btn_light_off"), bg="#e74c3c")
            self.animate_electrons()
        else:
            self.btn_light.config(text=self.T("btn_light_on"), bg="#f1c40f")
        self.update_simulation()
        
    def update_simulation(self):
        self.canvas.delete("beam")
        self.canvas.delete("filter_glass")
        
        if not hasattr(self, 'coords') or 'filter_center_x' not in self.coords:
            return

        wavelength_nm = self.filters_data.get(self.filter_var.get(), 546)
        voltage = self.volt_var.get()
        
        colors_hex = {365: "#8e44ad", 405: "#9b59b6", 436: "#3498db", 546: "#2ecc71", 577: "#f1c40f"}
        c_hex = colors_hex.get(wavelength_nm, "white")
        
        # Visual Filter
        fcx = self.coords['filter_center_x']
        fcy = self.coords['filter_center_y']
        r = 30
        self.canvas.create_oval(fcx-r, fcy-r, fcx+r, fcy+r, fill=c_hex, outline="", tags="filter_glass")
        self.canvas.tag_raise("filter_glass")
        
        if self.is_light_on:
            y = self.coords['beam_y']
            # Beam from Lamp to Filter
            self.canvas.create_line(self.coords['lamp_out_x'], y, self.coords['filter_in_x'], y, 
                                    fill=c_hex, width=8, arrow="last", tags="beam") 
            # Beam from Filter to Cathode
            self.canvas.create_line(self.coords['filter_out_x'], y, self.coords['cathode_hit_x'], y, 
                                    fill=c_hex, width=8, arrow="last", tags="beam")

            # Physics
            freq = self.c / (wavelength_nm * 1e-9)
            E_photon = self.h_real * freq
            Phi_J = self.phi_eV * self.e
            
            Ek_max = E_photon - Phi_J
            Vs = Ek_max / self.e
            
            if Ek_max > 0:
                if voltage >= Vs:
                    curr = 0.0
                else:
                    diff = Vs - voltage
                    curr = 10.0 * (1 - math.exp(-0.5 * diff)) if diff > 0 else 0
                    if curr < 0: curr = 0
            else:
                curr = 0.0
                
            self.measured_current = curr
        else:
            self.measured_current = 0.0
            
        # Display
        if not self.is_calibrated and self.is_light_on:
             self.lbl_ammeter.config(text=f"{random.uniform(-0.5, 0.5):.3f} nA (ERR)")
        elif not self.is_calibrated:
             self.lbl_ammeter.config(text="--.--")
        else:
            noise = random.uniform(-0.01, 0.01) if self.measured_current > 0 else 0.0
            val = max(0, self.measured_current + noise)
            self.lbl_ammeter.config(text=f"{val:.3f} nA")

    def record_data(self):
        if not self.is_calibrated:
            messagebox.showwarning("Warning", self.T("lbl_not_calibrated"))
            return
            
        f_key = self.filter_var.get()
        wav = self.filters_data.get(f_key, 546)
        freq = self.c / (wav * 1e-9)
        vs = self.volt_var.get()
        
        # Check if Vs is close to correct stopping potential? 
        # In real lab we record whatever. Here?
        # Let's just record whatever user set.
        
        self.data_points.append((freq, vs))
        
        f_label = self.T(f"filter_{f_key}")
        
        self.tree_mini.insert("", "end", values=(f_label, f"{vs:.2f}"))
        self.tree_full.insert("", "end", values=(f"{freq:.2e}", f"{vs:.2f}"))
        self.update_graph()

    def update_graph(self):
        self.ax.clear()
        self.ax.set_title(self.T("graph_title"))
        self.ax.set_xlabel(self.T("graph_xlabel"))
        self.ax.set_ylabel(self.T("graph_ylabel"))
        self.ax.grid(True)
        
        if not self.data_points:
            self.canvas_graph.draw()
            return
        
        # Plot Scatter Points
        freqs, vs = zip(*self.data_points)
        self.ax.scatter(freqs, vs, color='blue', label='Data Eksperimen')
        
        # Limit axes nicely
        self.ax.set_xlim(left=3e14, right=10e14)
        self.ax.set_ylim(bottom=0, top=max(vs)*1.2 if vs else 3.0)
        
        self.ax.legend()
        self.canvas_graph.draw()

    def reset_data(self):
        self.data_points = []
        for item in self.tree_mini.get_children(): self.tree_mini.delete(item)
        for item in self.tree_full.get_children(): self.tree_full.delete(item)
        
        self.ax.clear()
        self.ax.grid(True)
        self.canvas_graph.draw()
        self.lbl_analysis_res.config(text=self.T("lbl_result"))
        
    def analyze_data(self):
        if len(self.data_points) < 2:
            messagebox.showwarning("Error", self.T("msg_min_data"))
            return
            
        # Linear Reg
        freqs, vs = zip(*self.data_points)
        n = len(freqs)
        
        sum_x = sum(freqs)
        sum_y = sum(vs)
        sum_xy = sum(f*v for f, v in self.data_points)
        sum_xx = sum(f**2 for f in freqs)
        
        denom = (n * sum_xx - sum_x**2)
        if denom == 0: return
        
        slope = (n * sum_xy - sum_x * sum_y) / denom
        intercept = (sum_y - slope * sum_x) / n
        
        # Physics Results
        h_calc = slope * self.e
        W_calc_J = -intercept * self.e
        W_calc_eV = W_calc_J / self.e
        f0 = -intercept / slope
        
        # Display Result
        res = self.T("res_fmt").format(slope=slope, h_calc=h_calc, err=abs(h_calc-self.h_real)/self.h_real*100, W_calc_eV=W_calc_eV, f0=f0)
        self.lbl_analysis_res.config(text=res)
        
        # Draw Line on Matplotlib
        self.draw_regression(slope, intercept)
        
    def draw_regression(self, m, c):
        # Update Plot with Line
        self.update_graph() # Clear and redraw points first
        
        import numpy as np
        x_line = np.linspace(3e14, 10e14, 100)
        y_line = m * x_line + c
        
        self.ax.plot(x_line, y_line, 'r--', label=f'Regresi (h={m*self.e:.2e})')
        self.ax.legend()
        self.canvas_graph.draw()


    def get_data(self):
        export_data = []
        for freq, v_stop in self.data_points:
            export_data.append({
                "Modul": "Efek Fotolistrik",
                "Material": self.selected_material_name,
                "Frekuensi (Hz)": f"{freq:.2e}",
                "Tegangan Penghenti (V)": f"{v_stop:.4f}",
                "Fungsi Kerja (eV)": self.materials.get(self.selected_material_name, 0)
            })
        return export_data

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabEfekFotolistrik(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
