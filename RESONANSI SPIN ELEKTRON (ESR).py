import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from virtual_lab_data_manager import DataManager, ScrollableFrame

class VirtualLabESR(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#f5f6fa") # Light gray modern background
        
        self.setup_translations()
        self.lang = "ID"

        # --- Physics Constants & Apparatus ---
        self.h = 6.626e-34      # J.s
        self.mu_B = 9.274e-24   # J/T
        self.mu_0 = 4 * math.pi * 1e-7
        
        # Helmholtz Coil Specs
        self.N = 320     # Turns
        self.R = 0.068   # Radius (m)
        # B = (4/5)^(3/2) * (mu_0 * N * I) / R
        self.k_coil_geom = (4/5)**1.5 * (self.mu_0 * self.N) / self.R # T/A
        
        # Sample: DPPH
        # g factor approx 2.0036
        self.g_real = 2.0036
        
        # State
        self.freq_MHz = 45.0
        self.current_A = 0.0
        self.B_field_mT = 0.0
        
        self.is_power_on = False
        self.scan_manual = True # Manual knob or auto scan? Manual is better for "feel"
        
        self.data_points = []
        
        self.create_widgets()
        self.running = True
        self.update_simulation_loop()
        
        self.set_language("ID")

    def start_animation(self):
        if not self.running:
            self.running = True
            self.update_simulation_loop()

    def stop_animation(self):
        self.running = False

    def setup_translations(self):
        self.translations = {
            "ID": {
                "title": "Resonansi Spin Elektron (ESR)",
                "tab_exp": "Eksperimen",
                "tab_ana": "Analisis Data",
                "tab_guide": "Petunjuk Praktikum",
                "tab_scheme": "Skema Alat & Penjelasan",
                "tab_diagram": "Gambaran Rangkaian Alat",
                "osc_title": "Tampilan Osiloskop (Sinyal Absorpsi)",
                "lbl_y_gain": "[Y-Gain]",
                "lbl_x_phase": "[X-Axis: Phase]",
                "ctrl_title": "Kontrol Generator & Medan",
                "btn_record": "Catat Titik Resonansi",
                "lbl_rf": "1. Unit RF (MHz)",
                "lbl_amp": "2. Arus Helmholtz (Amper)",
                "col_freq": "Frekuensi (MHz)",
                "col_i": "Arus (A)",
                "col_b": "Medan B (mT)",
                "col_valid": "Resonansi?",
                "btn_calc": "Hitung Faktor g (Lande)",
                "btn_clear": "Hapus Data",
                "btn_save": "Simpan Data",
                "msg_min_data": "Min 2 data resonansi valid untuk regresi.",
                "msg_res": "Analisis Regresi Linear (f vs B):\nGradien (f/B) = {grad:.2f} GHz/T\nHitungan Faktor g = {g_calc:.4f}\n(Referensi Free Electron g ≈ 2.0023)",
                "msg_rec_ok": "Data dicatat.\nSinyal Resonansi Maksimum terdeteksi? {status}",
                "msg_warn_power": "Nyalakan Power Unit terlebih dahulu!",
                "plt_title": "Kurva Resonansi (Frekuensi vs Medan Magnet)",
                "plt_x": "Medan Magnet B (mT)",
                "plt_y": "Frekuensi RF (MHz)",
                "scheme_title": "Skema Alat Resonansi Spin Elektron (ESR)",
                "scheme_content": """SKEMA ALAT DAN PENJELASAN

Peralatan ESR digunakan untuk mendeteksi transisi spin elektron tak berpasangan dalam medan magnet.

KOMPONEN UTAMA:

1. Unit Osilator Frekuensi Radio (RF Bridge)
   Membangkitkan gelombang elektromagnetik frekuensi tinggi (MHz) yang diumpankan ke kumparan probe.

2. Kumparan Probe (Probe Unit)
   Kumparan kecil yang berisi sampel paramagnetik (biasanya DPPH - Diphenylpicrylhydrazyl). Kumparan ini berfungsi sebagai induktor dari rangkaian osilator.

3. Kumparan Helmholtz
   Sepasang kumparan besar yang identik dan sejajar.
   Fungsi: Menghasilkan medan magnet eksternal (B) yang sangat HOMOGEN di tengah-tengahnya (lokasi sampel). Kuat medan magnet diatur dengan mengubah arus listrik (Ampere).

4. Osiloskop Sinar Katoda (CRO)
   Menampilkan sinyal resonansi. Sumbu X merepresentasikan sapuan medan magnet (modulasi AC 50Hz), dan sumbu Y menampilkan sinyal serapan energi dari probe. Resonansi terlihat sebagai 'lekukan' (dip) pada layar.

PRINSIP KERJA:
Elektron memiliki momen magnetik spin. Dalam medan magnet luar (B), energi spin terbelah (Efek Zeeman). Jika sampel disinari gelombang RF dengan energi foton (hf) yang tepat sama dengan selisih energi spin (g.μB.B), maka terjadi RESONANSI (penyerapan energi maksimum).""",
                "guide_content": """PETUNJUK PRAKTIKUM ESR

A. DASAR TEORI
Resonansi Spin Elektron terjadi ketika frekuensi gelombang mikro (f) cocok dengan pemisahan energi Zeeman elektron dalam medan magnet (B):
h * f = g * μB * B

Dimana:
h  : Konstanta Planck
μB : Magneton Bohr
g  : Faktor g Lande (untuk elektron bebas ~ 2.0023)
B  : Kuat Medan Magnet

B. LANGKAH PERCOBAAN
1. Hidupkan Unit (POWER ON).
2. Tentukan Frekuensi RF (misal 30 MHz s.d 80 MHz).
3. Putar knop "Arus Helmholtz" secara perlahan.
   - Amati layar Osiloskop.
   - Perhatikan munculnya "lekukan" atau puncak sinyal absorpsi.
4. Saat lekukan mencapai MAKSIMUM (paling dalam), itu adalah titik Resonansi.
5. Klik "Catat Titik Resonansi" untuk menyimpan pasangan data (f, I).
6. Ulangi untuk variasi frekuensi yang lain (ambil min. 5 data).

C. ANALISIS
1. Masuk tab Analisis.
2. Klik "Hitung Faktor g".
3. Aplikasi akan membuat grafik f vs B dan menghitung gradien.
   Gradien = (g * μB) / h
   Sehingga g = (Gradien * h) / μB.""",
                "diag_helmholtz": "Helmholtz Coil Pair (9.5 GHz)",
                "diag_sample": "DPPH\nSample",
                "diag_wg": "WG",
                "diag_spec": "ESR SPECTROMETER X-BAND",
                "diag_osci": "OSCILLOSCOPE",
                "diag_ch1": "CH1: 50mV/div",
                "diag_time": "TIME: 10ms/div",
                "diag_freq": "FREQ",
                "diag_field": "FIELD",
                "diag_gain": "GAIN"
            },
            "EN": {
                "title": "Electron Spin Resonance (ESR)",
                "tab_exp": "Experiment",
                "tab_ana": "Data Analysis",
                "tab_guide": "Practical Guide",
                "tab_scheme": "Tool Scheme & Explanation",
                "tab_diagram": "Device Circuit Overview",
                "osc_title": "Oscilloscope Display (Absorption Signal)",
                "lbl_y_gain": "[Y-Gain]",
                "lbl_x_phase": "[X-Axis: Phase]",
                "ctrl_title": "Generator & Field Control",
                "btn_record": "Record Resonance Point",
                "lbl_rf": "1. RF Unit (MHz)",
                "lbl_amp": "2. Helmholtz Current (Ampere)",
                "col_freq": "Frequency (MHz)",
                "col_i": "Current (A)",
                "col_b": "B-Field (mT)",
                "col_valid": "Resonance?",
                "btn_calc": "Calculate g-factor (Lande)",
                "btn_clear": "Clear Data",
                "btn_save": "Save Data",
                "msg_min_data": "Min 2 valid resonance data points for regression.",
                "msg_res": "Linear Regression Analysis (f vs B):\nGradient (f/B) = {grad:.2f} GHz/T\ng-factor Calculation = {g_calc:.4f}\n(Ref Free Electron g ≈ 2.0023)",
                "msg_rec_ok": "Data recorded.\nMaximum Resonance Signal detected? {status}",
                "msg_warn_power": "Turn on Power Unit first!",
                "plt_title": "Resonance Curve (Frequency vs Magnetic Field)",
                "plt_x": "Magnetic Field B (mT)",
                "plt_y": "RF Frequency (MHz)",
                "scheme_title": "ESR Tool Scheme & Explanation",
                "scheme_content": """TOOL SCHEME AND EXPLANATION

ESR equipment is used to detect unpaired electron spin transitions in a magnetic field.

MAIN COMPONENTS:

1. Radio Frequency Oscillator Unit (RF Bridge)
   Generates high frequency electromagnetic waves (MHz) fed to the probe coil.

2. Probe Coil (Probe Unit)
   Small coil containing paramagnetic sample (usually DPPH - Diphenylpicrylhydrazyl). Acts as inductor for the oscillator circuit.

3. Helmholtz Coils
   Pair of identical parallel large coils.
   Function: Generates highly HOMOGENEOUS external magnetic field (B) in the center (sample location). Field strength is adjusted by changing electric current (Ampere).

4. Cathode Ray Oscilloscope (CRO)
   Displays resonance signal. X-axis represents magnetic field sweep (AC 50Hz modulation), and Y-axis displays energy absorption signal from probe. Resonance appears as a 'dip' on screen.

WORKING PRINCIPLE:
Electrons have spin magnetic moment. In external magnetic field (B), spin energy splits (Zeeman Effect). If sample is irradiated by RF wave with photon energy (hf) exactly equal to spin energy difference (g.μB.B), RESONANCE occurs (maximum energy absorption).""",
                "guide_content": """ESR PRACTICAL GUIDE

A. THEORETICAL BASIS
Electron Spin Resonance occurs when microwave frequency (f) matches the Zeeman energy splitting of electrons in magnetic field (B):
h * f = g * μB * B

Where:
h  : Planck's Constant
μB : Bohr Magneton
g  : Lande g-factor (for free electron ~ 2.0023)
B  : Magnetic Field Strength

B. EXPERIMENTAL STEPS
1. Turn Unit ON (POWER ON).
2. Set RF Frequency (e.g. 30 MHz to 80 MHz).
3. Turn "Helmholtz Current" knob slowly.
   - Observe Oscilloscope screen.
   - Look for appearance of "dip" or absorption signal peak.
4. When dip reaches MAXIMUM (deepest), that is the Resonance point.
5. Click "Record Resonance Point" to save data pair (f, I).
6. Repeat for other frequency variations (take min. 5 data points).

C. ANALYSIS
1. Go to Analysis tab.
2. Click "Calculate g-factor".
3. Application will create f vs B graph and calculate gradient.
   Gradient = (g * μB) / h
   So g = (Gradient * h) / μB.""",
                "diag_helmholtz": "Helmholtz Coil Pair (9.5 GHz)",
                "diag_sample": "DPPH\nSample",
                "diag_wg": "WG",
                "diag_spec": "ESR SPECTROMETER X-BAND",
                "diag_osci": "OSCILLOSCOPE",
                "diag_ch1": "CH1: 50mV/div",
                "diag_time": "TIME: 10ms/div",
                "diag_freq": "FREQ",
                "diag_field": "FIELD",
                "diag_gain": "GAIN"
            }
        }

    def T(self, key):
        return self.translations.get(self.lang, self.translations["ID"]).get(key, key)

    def set_language(self, lang):
        self.lang = lang
        self.refresh_ui()

    def refresh_ui(self):
        # Header
        self.lbl_header.config(text=self.T("title"))
        
        # Tabs
        self.notebook.tab(0, text=self.T("tab_exp"))
        self.notebook.tab(1, text=self.T("tab_ana"))
        self.notebook.tab(2, text=self.T("tab_guide"))
        self.notebook.tab(3, text=self.T("tab_scheme"))
        self.notebook.tab(4, text=self.T("tab_diagram"))
        
        # Exp UI
        self.lf_osc.config(text=self.T("osc_title"))
        self.lbl_knob_1.config(text=self.T("lbl_y_gain"))
        self.lbl_knob_2.config(text=self.T("lbl_x_phase"))
        self.lbl_ctrl_title.config(text=self.T("ctrl_title"))
        self.btn_record.config(text=self.T("btn_record"))
        self.lbl_unit_rf.config(text=self.T("lbl_rf"))
        self.lbl_unit_amp.config(text=self.T("lbl_amp"))
        
        # Analysis UI
        headers = [self.T("col_freq"), self.T("col_i"), self.T("col_b"), self.T("col_valid")]
        
        # Update headings only
        if hasattr(self, 'tree_cols'):
            for c, h in zip(self.tree_cols, headers):
                self.tree.heading(c, text=h)
            
        self.btn_calc.config(text=self.T("btn_calc"))
        self.btn_clear.config(text=self.T("btn_clear"))
        self.btn_save.config(text=self.T("btn_save"))
        
        self.ax.set_title(self.T("plt_title"))
        self.ax.set_ylabel(self.T("plt_y"))
        self.ax.set_xlabel(self.T("plt_x"))
        self.graph_canvas.draw()
        
        # Guide & Scheme
        self.txt_guide.config(state="normal")
        self.txt_guide.delete("1.0", tk.END)
        self.txt_guide.insert("1.0", self.T("guide_content"))
        self.txt_guide.config(state="disabled")

        self.lbl_scheme_title.config(text=self.T("scheme_title"))
        self.txt_scheme.config(state="normal")
        self.txt_scheme.delete("1.0", tk.END)
        self.txt_scheme.insert("1.0", self.T("scheme_content"))
        self.txt_scheme.config(state="disabled")
        
        # Diagram (Canvas Text)
        self.canvas_diag.itemconfigure("diag_helmholtz", text=self.T("diag_helmholtz"))
        self.canvas_diag.itemconfigure("diag_sample", text=self.T("diag_sample"))
        self.canvas_diag.itemconfigure("diag_wg", text=self.T("diag_wg"))
        self.canvas_diag.itemconfigure("diag_spec", text=self.T("diag_spec"))
        self.canvas_diag.itemconfigure("diag_osci", text=self.T("diag_osci"))
        self.canvas_diag.itemconfigure("diag_ch1", text=self.T("diag_ch1"))
        self.canvas_diag.itemconfigure("diag_time", text=self.T("diag_time"))
        self.canvas_diag.itemconfigure("diag_freq", text=self.T("diag_freq"))
        self.canvas_diag.itemconfigure("diag_field", text=self.T("diag_field"))
        self.canvas_diag.itemconfigure("diag_gain", text=self.T("diag_gain"))
            
        
    def create_widgets(self):
        # Header
        header = tk.Frame(self, bg="#2c3e50", pady=10)
        header.pack(fill="x")
        self.lbl_header = tk.Label(header, text=self.T("title"), 
                 font=("Helvetica", 18, "bold"), fg="#ecf0f1", bg="#2c3e50")
        self.lbl_header.pack()
        
        # Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Experiment (FULL TAB, NO SCROLL)
        self.tab_exp = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_exp, text=self.T("tab_exp"))
        self.create_experiment_ui()
        
        # Tab 2: Analysis (FULL TAB, NO SCROLL)
        self.tab_ana = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_ana, text=self.T("tab_ana"))
        self.create_analysis_ui()
        
        # Tab 3: Guide
        self.tab_guide = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_guide, text=self.T("tab_guide"))
        self.create_guide_ui()

        # Tab 4: Tools Scheme
        self.tab_scheme = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_scheme, text=self.T("tab_scheme"))
        self.create_tab_scheme()

        # Tab 5: Real Diagram
        self.tab_diagram = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_diagram, text=self.T("tab_diagram"))
        self.create_tab_diagram()

    def create_tab_diagram(self):
        self.canvas_diag = tk.Canvas(self.tab_diagram, bg="#fdfefe")
        self.canvas_diag.pack(fill="both", expand=True, padx=20, pady=20)
        
        import math
        canvas = self.canvas_diag # Alias
        
        canvas.create_rectangle(0, 420, 800, 500, fill="#95a5a6", outline="")
        canvas.create_line(0, 420, 800, 420, fill="#7f8c8d", width=2)
        
        # Helmholtz Coils (3D perspective)
        for i in range(3):
            offset = i * 2
            canvas.create_oval(220-offset, 120+offset, 310+offset, 360-offset, 
                             outline="#d35400", width=6-i)
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            x = 265 + 40 * math.cos(rad)
            y = 240 + 115 * math.sin(rad)
            canvas.create_oval(x-2, y-2, x+2, y+2, fill="#e67e22", outline="")
        
        for i in range(3):
            offset = i * 2
            canvas.create_oval(490-offset, 140+offset, 570+offset, 340-offset, 
                             outline="#d35400", width=6-i)
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            x = 530 + 35 * math.cos(rad)
            y = 240 + 95 * math.sin(rad)
            canvas.create_oval(x-2, y-2, x+2, y+2, fill="#e67e22", outline="")
        
        canvas.create_rectangle(260, 360, 270, 420, fill="#7f8c8d", outline="#5d6d7e", width=2)
        canvas.create_rectangle(525, 340, 535, 420, fill="#7f8c8d", outline="#5d6d7e", width=2)
        canvas.create_rectangle(250, 410, 545, 425, fill="#95a5a6", outline="#7f8c8d", width=2)
        
        canvas.create_text(400, 90, text=self.T("diag_helmholtz"), 
                         font=("Arial", 12, "bold"), fill="#2c3e50", tag="diag_helmholtz")
        
        # ESR Sample Probe
        canvas.create_rectangle(385, 180, 415, 320, fill="#ecf0f1", outline="#bdc3c7", width=2)
        canvas.create_rectangle(387, 230, 413, 270, fill="#8e44ad", outline="#6c3483", width=1)
        canvas.create_text(430, 250, text=self.T("diag_sample"), font=("Arial", 8), fill="#2c3e50", tag="diag_sample")
        canvas.create_rectangle(415, 235, 480, 265, fill="#34495e", outline="#2c3e50", width=2)
        canvas.create_text(447, 250, text=self.T("diag_wg"), font=("Arial", 8, "bold"), fill="white", tag="diag_wg")
        canvas.create_rectangle(395, 320, 405, 420, fill="#5d6d7e", outline="#34495e", width=2)
        
        # ESR Control Unit (Rack mount)
        canvas.create_rectangle(20, 280, 240, 450, fill="#34495e", outline="#2c3e50", width=3)
        canvas.create_rectangle(25, 285, 235, 445, fill="#2c3e50", outline="#1a252f", width=2)
        
        canvas.create_rectangle(30, 290, 230, 310, fill="#1a252f", outline="")
        canvas.create_text(130, 300, text=self.T("diag_spec"), 
                         font=("Arial", 9, "bold"), fill="#2ecc71", tag="diag_spec")
        
        canvas.create_rectangle(35, 320, 140, 350, fill="#000000", outline="#3498db", width=2)
        canvas.create_text(87, 335, text="9.450 GHz", font=("Courier", 12, "bold"), fill="#2ecc71")
        
        canvas.create_rectangle(150, 320, 225, 350, fill="#000000", outline="#3498db", width=2)
        canvas.create_text(187, 335, text="338 mT", font=("Courier", 11, "bold"), fill="#f39c12")
        
        labels = [self.T("diag_freq"), self.T("diag_field"), self.T("diag_gain")]
        tags = ["diag_freq", "diag_field", "diag_gain"]
        
        for i, (x, _) in enumerate([(60, "FREQ"), (120, "FIELD"), (180, "GAIN")]):
            canvas.create_oval(x-18, 370, x+18, 406, fill="#7f8c8d", outline="#5d6d7e", width=2)
            canvas.create_oval(x-15, 373, x+15, 403, fill="#95a5a6", outline="")
            canvas.create_line(x, 380, x+10, 373, fill="white", width=3)
            canvas.create_text(x, 415, text=labels[i], font=("Arial", 8, "bold"), fill="white", tag=tags[i])
        
        for i, (col, lbl) in enumerate([("#e74c3c", "PWR"), ("#2ecc71", "RDY")]):
            canvas.create_oval(35+i*50, 425, 47+i*50, 437, fill=col, outline="#2c3e50", width=2)
            canvas.create_text(55+i*50, 431, text=lbl, font=("Arial", 7, "bold"), fill="white")
        
        # Oscilloscope (Modern LCD)
        canvas.create_rectangle(500, 280, 760, 450, fill="#34495e", outline="#2c3e50", width=3)
        canvas.create_polygon(500, 280, 510, 270, 770, 270, 760, 280, fill="#34495e", outline="#2c3e50")
        canvas.create_polygon(760, 280, 770, 270, 770, 440, 760, 450, fill="#2c3e50", outline="#2c3e50")
        
        canvas.create_rectangle(510, 290, 750, 390, fill="#1a1a1a", outline="#3498db", width=2)
        
        for i in range(6):
            canvas.create_line(510+i*40, 290, 510+i*40, 390, fill="#2c3e50", dash=(2,2))
        for i in range(4):
            canvas.create_line(510, 290+i*25, 750, 290+i*25, fill="#2c3e50", dash=(2,2))
        
        points = []
        for x in range(0, 240, 2):
            phase = (x - 120) / 30.0
            y = 50 * phase * (2.718 ** (-phase**2 / 2))
            points.extend([510 + x, 340 - y])
        canvas.create_line(points, fill="#2ecc71", width=3, smooth=True)
        
        canvas.create_text(550, 310, text=self.T("diag_ch1"), font=("Arial", 8), fill="#2ecc71", anchor="w", tag="diag_ch1")
        canvas.create_text(550, 325, text=self.T("diag_time"), font=("Arial", 8), fill="#f39c12", anchor="w", tag="diag_time")
        
        for i in range(5):
            canvas.create_rectangle(515+i*45, 400, 540+i*45, 420, fill="#95a5a6", 
                                  outline="#7f8c8d", width=2)
        canvas.create_text(630, 435, text=self.T("diag_osci"), font=("Arial", 10, "bold"), fill="white", tag="diag_osci")
        
        # Cables
        canvas.create_line(240, 350, 260, 350, 260, 240, 380, 240, width=4, fill="#2c3e50", smooth=True)
        canvas.create_line(240, 350, 260, 350, 260, 240, 380, 240, width=2, fill="#95a5a6", smooth=True)
        canvas.create_line(240, 370, 250, 370, 250, 390, 260, 390, width=3, fill="#e74c3c", smooth=True)
        canvas.create_line(240, 385, 250, 385, 250, 410, 525, 410, width=3, fill="#e74c3c", smooth=True)
        canvas.create_line(240, 320, 300, 320, 300, 340, 500, 340, width=3, fill="#3498db", smooth=True)
        canvas.create_line(240, 320, 300, 320, 300, 340, 500, 340, width=1, fill="white", smooth=True) 


    def create_tab_scheme(self):
        container = self.tab_scheme
        self.lbl_scheme_title = tk.Label(container, text=self.T("scheme_title"), 
                 font=("Arial", 16, "bold"), bg="#f5f6fa", fg="#2d3436")
        self.lbl_scheme_title.pack(pady=15)
        
        frame = tk.Frame(container, bg="white", bd=1, relief="solid")
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.txt_scheme = tk.Text(frame, font=("Arial", 12), wrap="word", padx=20, pady=20, bg="white", relief="flat")
        self.txt_scheme.pack(fill="both", expand=True)
        
        self.txt_scheme.insert("1.0", self.T("scheme_content"))
        self.txt_scheme.config(state="disabled")


    def create_experiment_ui(self):
        # Full Layout: Top (Simulation) & Bottom (Controls)
        main = tk.Frame(self.tab_exp, bg="#f5f6fa")
        main.pack(fill="both", expand=True, padx=10, pady=10)
        
        # --- Top Panel: Visuals (Apparatus + Oscilloscope) ---
        top_frame = tk.Frame(main, bg="#2c3e50")
        top_frame.pack(side="top", fill="both", expand=True, pady=(0, 10))
        
        # Apparatus Schematic (Left Side of Top)
        app_box = tk.Frame(top_frame, bg="#34495e", width=400)
        app_box.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.canvas_app = tk.Canvas(app_box, bg="#34495e")
        self.canvas_app.pack(fill="both", expand=True)
        self.draw_apparatus()
        
        # Oscilloscope Screen (Right Side of Top)
        self.lf_osc = tk.LabelFrame(top_frame, text=self.T("osc_title"), bg="#2c3e50", fg="white", width=400)
        self.lf_osc.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        self.canvas_osci = tk.Canvas(self.lf_osc, bg="black")
        self.canvas_osci.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Osci Knobs (Visual Only)
        knob_frame = tk.Frame(self.lf_osc, bg="#2c3e50")
        knob_frame.pack(fill="x")
        self.lbl_knob_1 = tk.Label(knob_frame, text=self.T("lbl_y_gain"), fg="white", bg="#2c3e50")
        self.lbl_knob_1.pack(side="left", padx=10)
        self.lbl_knob_2 = tk.Label(knob_frame, text=self.T("lbl_x_phase"), fg="white", bg="#2c3e50")
        self.lbl_knob_2.pack(side="left", padx=10)

        # --- Bottom Panel: Controls ---
        bot_frame = tk.Frame(main, bg="white", relief="raised", bd=1)
        bot_frame.pack(side="bottom", fill="x", padx=5, pady=5)
        
        self.lbl_ctrl_title = tk.Label(bot_frame, text=self.T("ctrl_title"), font=("Arial", 12, "bold"), bg="white")
        self.lbl_ctrl_title.pack(side="top", pady=5)
        
        c_grid = tk.Frame(bot_frame, bg="white")
        c_grid.pack(fill="x", padx=10, pady=5)
        
        # Col 1: Power & Record
        c1 = tk.Frame(c_grid, bg="white")
        c1.pack(side="left", fill="y", padx=10)
        self.btn_power = tk.Button(c1, text="POWER UNIT: OFF", bg="#e74c3c", fg="black", font=("Arial", 10, "bold"),
                                   command=self.toggle_power, width=15)
        self.btn_power.pack(pady=5)
        self.btn_record = tk.Button(c1, text=self.T("btn_record"), command=self.record_point, 
                  bg="#2ecc71", fg="black")
        self.btn_record.pack(pady=5, fill="x")
                  
        # Col 2: Frequency
        c2 = tk.Frame(c_grid, bg="white", bd=1, relief="solid")
        c2.pack(side="left", fill="both", expand=True, padx=10)
        self.lbl_unit_rf = tk.Label(c2, text=self.T("lbl_rf"), bg="#ecf0f1", font=("Arial", 9, "bold"))
        self.lbl_unit_rf.pack(fill="x")
        
        self.lbl_freq = tk.Label(c2, text="45.00 MHz", font=("Ds-Digital", 18), fg="blue", bg="black")
        self.lbl_freq.pack(pady=2)
        self.freq_var = tk.DoubleVar(value=45.0)
        tk.Scale(c2, from_=30, to=100, orient="horizontal", variable=self.freq_var, 
                 bg="white", command=self.update_params, showvalue=0).pack(fill="x", padx=5)
                 
        # Col 3: Current
        c3 = tk.Frame(c_grid, bg="white", bd=1, relief="solid")
        c3.pack(side="left", fill="both", expand=True, padx=10)
        self.lbl_unit_amp = tk.Label(c3, text=self.T("lbl_amp"), bg="#ecf0f1", font=("Arial", 9, "bold"))
        self.lbl_unit_amp.pack(fill="x")
        
        self.lbl_amp = tk.Label(c3, text="0.000 A", font=("Ds-Digital", 18), fg="red", bg="black")
        self.lbl_amp.pack(pady=2)
        self.coil_var = tk.DoubleVar(value=0.0)
        tk.Scale(c3, from_=0.0, to=3.0, resolution=0.001, orient="horizontal", variable=self.coil_var,
                 bg="white", command=self.update_params, showvalue=0).pack(fill="x", padx=5)
        self.lbl_B_calc = tk.Label(c3, text="B ≈ 0.00 mT", font=("Arial", 9), fg="gray", bg="white")
        self.lbl_B_calc.pack(pady=2)

    def create_analysis_ui(self):
        # Paned Window (Split)
        paned = tk.PanedWindow(self.tab_ana, orient=tk.HORIZONTAL, bg="#f5f6fa", sashwidth=5)
        paned.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left Frame: Table
        left_frame = tk.Frame(paned, bg="white", width=400)
        paned.add(left_frame, minsize=400)
        
        tk.Label(left_frame, text="Kalkulator Medan Magnet (B) dari Arus (I)", font=("Arial", 12, "bold"), bg="white").pack(pady=5)
        info_frame = tk.Frame(left_frame, bg="#ecf0f1", pady=5)
        info_frame.pack(fill="x", padx=10)
        tk.Label(info_frame, text=f"Konstanta Coil k = {self.k_coil_geom*1000:.3f} mT/A", font=("Courier", 11), bg="#ecf0f1").pack()
        
        # Table
        self.tree_cols = ("freq", "i", "b", "valid")
        self.tree = ttk.Treeview(left_frame, columns=self.tree_cols, show="headings", height=10)
        
        headers = [self.T("col_freq"), self.T("col_i"), self.T("col_b"), self.T("col_valid")]
        for c, h in zip(self.tree_cols, headers):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        btn_box = tk.Frame(left_frame, bg="white")
        btn_box.pack(fill="x", pady=5)
        self.btn_clear = tk.Button(btn_box, text=self.T("btn_clear"), command=self.clear_data, bg="#c0392b", fg="black")
        self.btn_clear.pack(side="left", padx=5)
        self.btn_save = tk.Button(btn_box, text=self.T("btn_save"), command=self.save_data, bg="#3498db", fg="black")
        self.btn_save.pack(side="left", padx=5)
        self.btn_calc = tk.Button(btn_box, text=self.T("btn_calc"), command=self.calculate_g, bg="#9b59b6", fg="black")
        self.btn_calc.pack(side="right", padx=5)
        
        self.lbl_res = tk.Label(left_frame, text="", font=("Arial", 12), bg="white", fg="#2980b9", justify="left")
        self.lbl_res.pack(fill="x", padx=20, pady=10)

        # Right Frame: Graph Area
        right_frame = tk.Frame(paned, bg="white", bd=1, relief="solid")
        paned.add(right_frame)

        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.ax.set_title(self.T("plt_title"))
        self.ax.set_ylabel(self.T("plt_y"))
        self.ax.set_xlabel(self.T("plt_x"))
        self.ax.grid(True)
        
        self.graph_canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        self.toolbar = NavigationToolbar2Tk(self.graph_canvas, right_frame)
        self.toolbar.update()
        self.graph_canvas.get_tk_widget().pack(fill="both", expand=True)

    def save_data(self):
        if not self.data_points:
            tk.messagebox.showwarning("Warning", "No data to save!")
            return
            
        data_to_save = []
        for d in self.data_points:
            data_to_save.append({
                "frequency_MHz": d[2],
                "current_A": d[0],
                "B_field_mT": d[1],
                "is_resonance": d[3]
            })
            
        DataManager.save_data_unified(data_to_save, module_name="ESR Experiment")

    def create_guide_ui(self):
        self.tab_guide.update_idletasks() # Ensure frame is ready
        frame = tk.Frame(self.tab_guide, bg="#f5f6fa")
        frame.pack(fill="both", expand=True)

        self.txt_guide = tk.Text(frame, font=("Arial", 11), padx=20, pady=20, wrap="word", bg="#f5f6fa", relief="flat")
        scr = ttk.Scrollbar(frame, command=self.txt_guide.yview)
        self.txt_guide.configure(yscrollcommand=scr.set)
        
        scr.pack(side="right", fill="y")
        self.txt_guide.pack(side="left", fill="both", expand=True)

        self.txt_guide.insert("1.0", self.T("guide_content"))
        self.txt_guide.config(state="disabled")

    def toggle_power(self):
        self.is_power_on = not self.is_power_on
        if self.is_power_on:
            self.btn_power.config(text="POWER UNIT: ON", bg="#27ae60")
        else:
            self.btn_power.config(text="POWER UNIT: OFF", bg="#e74c3c")
            # Clear output
            self.canvas_osci.delete("trace")

    def update_params(self, event=None):
        self.current_A = self.coil_var.get()
        self.freq_MHz = self.freq_var.get()
        
        # Calculate B Field
        self.B_field_mT = self.k_coil_geom * self.current_A * 1000 # mT
        
        # Update Displays
        self.lbl_amp.config(text=f"{self.current_A:.3f} A")
        self.lbl_B_calc.config(text=f"B ≈ {self.B_field_mT:.2f} mT")
        self.lbl_freq.config(text=f"{self.freq_MHz:.2f} MHz")

    def draw_apparatus(self):
        self.canvas_app.delete("all")
        w = self.canvas_app.winfo_width()
        h = self.canvas_app.winfo_height() 
        if w<10: w=400
        
        cx, cy = w/2, h/2
        
        # Coils (Helmholtz) - Side view schematic
        # Left Coil
        self.canvas_app.create_oval(cx-60, cy-60, cx-40, cy+60, outline="#bdc3c7", width=3)
        self.canvas_app.create_line(cx-50, cy+60, cx-50, cy+80, fill="red", width=2)
        
        # Right Coil
        self.canvas_app.create_oval(cx+40, cy-60, cx+60, cy+60, outline="#bdc3c7", width=3)
        self.canvas_app.create_line(cx+50, cy+60, cx+50, cy+80, fill="black", width=2)
        
        # Probe / Sample in center
        self.canvas_app.create_rectangle(cx-10, cy-10, cx+10, cy+80, fill="#f1c40f") # Stem
        self.canvas_app.create_oval(cx-5, cy-5, cx+5, cy+5, fill="#e74c3c") # Sample DPPH
        
        self.canvas_app.create_text(cx, cy-80, text="Helmholtz Coils + Probe DPPH", fill="white")

    def update_simulation_loop(self):
        if not self.running: return

        if self.is_power_on:
            self.draw_oscilloscope()
        
        self.after(50, self.update_simulation_loop)
        
    def draw_oscilloscope(self):
        w = self.canvas_osci.winfo_width()
        h = self.canvas_osci.winfo_height()
        if w < 10: return
        
        # ESR Resonance Logic
        f_Hz = self.freq_MHz * 1e6
        B_res_Tesla = (self.h * f_Hz) / (self.g_real * self.mu_B)
        I_res = B_res_Tesla / self.k_coil_geom
        
        # Scan Parameters
        width_A = 0.2  # The scan window width in Amps
        linewidth_A = 0.04
        gamma_sq_inv = 1.0 / ((linewidth_A/2)**2)
        
        cx, cy = w/2, h/2
        points = []
        
        # Optimization: Reuse line object and reduce point density
        step = 4
        inv_w = 1.0 / w
        start_I = self.current_A - width_A
        two_width_A = 2 * width_A
        
        # Optimization: Skip heavy math if resonance is far off-screen
        # Visible range: [self.current_A - width_A, self.current_A + width_A]
        is_visible = (self.current_A - width_A - linewidth_A*2) < I_res < (self.current_A + width_A + linewidth_A*2)

        for px in range(0, w, step):
            if is_visible:
                # Map px to current deviation
                scan_I = start_I + (px * inv_w) * two_width_A
                diff = scan_I - I_res
                
                # Lorentzian: y = 1 / (1 + (diff^2 / (gamma/2)^2))
                y_val = 1.0 / (1 + (diff**2 * gamma_sq_inv))
                signal = y_val * 80
            else:
                signal = 0
            
            # Add noise
            noise = random.uniform(-2, 2)
            
            # Plot Y (Inverted for dip)
            # Original logic: plot_y = cy + signal; y_coord = h - plot_y + noise
            plot_y_raw = cy + signal
            
            points.append(px)
            points.append(h - plot_y_raw + noise)

        if len(points) > 2:
            if self.canvas_osci.find_withtag("trace"):
                self.canvas_osci.coords("trace", *points)
            else:
                self.canvas_osci.create_line(points, fill="#2ecc71", width=2, tags="trace", smooth=True)

    def record_point(self):
        if not self.is_power_on: 
            tk.messagebox.showwarning("Warning", self.T("msg_warn_power"))
            return
        
        # Check if near resonance
        f_Hz = self.freq_MHz * 1e6
        B_res_Tesla = (self.h * f_Hz) / (self.g_real * self.mu_B)
        I_res = B_res_Tesla / self.k_coil_geom
        
        # Status for user
        status = "YES" if abs(self.current_A - I_res) < 0.1 else self.T("col_valid") + ": NO"
        
        # Save data
        self.tree.insert("", "end", values=(f"{self.current_A:.3f}", f"{self.B_field_mT:.2f}", f"{self.freq_MHz:.1f}", status))
        self.data_points.append((self.current_A, self.B_field_mT, self.freq_MHz, status)) 
        # Stored: (I, B, f, status) -> Note: original stored (B, f), but improved to store all for save
        
        self.update_graph()
        tk.messagebox.showinfo("Recorded", self.T("msg_rec_ok").format(status=status))

    def update_graph(self):
        # Relationship: f = (g * mu_B / h) * B
        if not self.data_points:
            self.ax.clear()
            self.ax.grid(True)
            self.graph_canvas.draw()
            return

        # Data structure changed to tuple(4). Index 1 is B, Index 2 is f
        Bs = [p[1] for p in self.data_points]
        fs = [p[2] for p in self.data_points]
        
        self.ax.clear()
        self.ax.set_title(self.T("plt_title"))
        self.ax.set_ylabel(self.T("plt_y"))
        self.ax.set_xlabel(self.T("plt_x"))
        self.ax.grid(True)
        
        self.ax.scatter(Bs, fs, c='red', marker='x', label='Data')
        self.ax.legend()
        self.graph_canvas.draw()
        
    def get_data(self):
        export_data = []
        for child in self.tree.get_children():
            vals = self.tree.item(child)["values"]
            row = {
                "Arus (A)": vals[0],
                "Medan B (mT)": vals[1],
                "Frekuensi (MHz)": vals[2],
                "Valid": vals[3]
            }
            export_data.append(row)
        return export_data

    def save_data_unified(self):
        data = self.get_data()
        success, msg = DataManager.save_data_unified(data, "ESR_Experiment")
        
        if success:
            messagebox.showinfo("Sukses", msg)
        else:
            messagebox.showwarning("Perhatian", msg)

    def clear_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.data_points = []
        self.lbl_res.config(text="")
        self.update_graph()

    def calculate_g(self):
        if len(self.data_points) < 2:
            tk.messagebox.showwarning("Warning", self.T("msg_min_data"))
            return
            
        # Regression f vs B
        # f = (g * mu_B / h) * B
        # y = m * x
        # m = g * mu_B / h  -> g = m * h / mu_B
        
        # Data stored indices: 1=B(mT), 2=f(MHz)
        X = np.array([p[1] * 1e-3 for p in self.data_points]) # Tesla
        Y = np.array([p[2] * 1e6 for p in self.data_points])  # Hz
        
        # Linear Fit through origin (y = mx) => m = sum(xy)/sum(xx)
        m = np.sum(X*Y) / np.sum(X**2)
        
        g_calc = m * self.h / self.mu_B
        grad_GHz_T = m / 1e9
        
        txt = self.T("msg_res").format(grad=grad_GHz_T, g_calc=g_calc)
        self.lbl_res.config(text=txt, fg="green")

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabESR(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
