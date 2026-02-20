import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
from virtual_lab_data_manager import DataManager

class VirtualLabRadiasiBendaHitam(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#f5f6fa")
        
        # Physics Constants
        self.h = 6.626e-34    # Planck's constant
        self.c = 3.0e8        # Speed of light
        self.k = 1.38e-23     # Boltzmann constant
        self.b = 2.898e-3     # Wien's displacement constant
        self.sigma = 5.67e-8  # Stefan-Boltzmann constant
        
        self.setup_translations()
        self.lang = "ID"

        # State variables
        self.temperature = 3000.0 # Kelvin
        self.data_points = [] # List of Dicts
        
        self.create_widgets()

    def setup_translations(self):
        self.translations = {
            "ID": {
                "title": "Simulasi Radiasi Benda Hitam & Hukum Wien",
                "tab_sim": "Simulasi & Eksperimen",
                "tab_analisis": "Analisis Data (Hukum Wien)",
                "tab_guide": "Petunjuk Praktikum",
                "tab_scheme": "Skema Alat & Penjelasan",
                "tab_diagram": "Gambaran Rangkaian Alat",
                "header_control": "Panel Kontrol",
                "lbl_temp": "Temperatur (Kelvin)",
                "lbl_color": "Perkiraan Warna Benda:",
                "header_capture": "Pengambilan Data:",
                "btn_record": "Catat Puncak (Lambda Max)",
                "btn_save": "☁️ Simpan (DB & Excel)",
                "header_graph": "Kurva Radiasi Spektral (Intensitas vs Panjang Gelombang)",
                "header_table": "Tabel Data Eksperimen",
                "col_temp": "T (Kelvin)",
                "col_lam": "λ max (nm)",
                "btn_calc": "Hitung Konstanta Wien (b)",
                "btn_reset": "Reset Data",
                "header_analysis_graph": "Grafik Analisis Hukum Wien",
                "lbl_analysis_axis": "Sumbu Y: λ max (m) | Sumbu X: 1/T (1/K)",
                "lbl_result": "Hasil: b = ...",
                "res_fmt": "b (Hitung) = {0:.4e} m.K\nError = {1:.2f}%",
                "msg_data_min": "Butuh minimal 2 titik data untuk analisis linier.",
                "msg_save_success": "Berhasil menyimpan data.",
                "msg_save_fail": "Gagal menyimpan data.",
                "lbl_axis_x_spec": "Panjang Gelombang (nm)",
                "lbl_axis_y_spec": "Intensitas",
                "axis_x_anl": "1/T (K^-1)",
                "axis_y_anl": "λ max (nm)",
                "lbl_temp_fmt": "T = {0} K",
                "lbl_lambda_fmt": "Puncak λ ≈ {0} nm",
                "graph_peak_label": "λmax\n{0} nm",
                "diag_oven": "Oven Benda Hitam",
                "diag_sensor": "Sensor Spektrofotometer",
                "diag_ctrl": "Kontrol & Pengukuran",
                "diag_temp_disp": "{0} K",
                "diag_int_disp": "Intensitas: {0}",
                "scheme_title": "Skema Alat Eksperimen Radiasi Benda Hitam",
                "scheme_content": """SKEMA ALAT DAN PENJELASAN

Eksperimen ini mensimulasikan pengukuran spektrum radiasi dari benda hitam ideal.

KOMPONEN UTAMA:

1. Benda Hitam (Blackbody Simulator)
   Sumber radiasi berupa rongga dengan lubang kecil yang dipanaskan. Dinding rongga memancarkan dan menyerap radiasi secara sempurna, sehingga radiasi yang keluar lewat lubang memiliki karakteristik spektrum benda hitam ideal.

2. Kontrol & Sensor Temperatur
   Digunakan untuk mengatur suhu benda hitam dalam rentang tertentu (misal 1000 K - 10000 K). Termokopel digunakan untuk memantau suhu aktual.

3. Sistem Optik Dispersi (Spektrometer)
   Cahaya yang keluar dari lubang benda hitam dilewatkan melalui prisma atau kisi difraksi. Komponen ini memecah cahaya polikromatik menjadi panjang gelombang penyusunnya (spektrum).

4. Detektor Intensitas
   Sebuah sensor yang dapat digerakkan (scanning) sepanjang spektrum untuk mengukur intensitas radiasi pada setiap panjang gelombang spesifik.

MODEL FISIS:
Eksperimen ini menunjukkan Hukum Stefan-Boltzmann (Total daya radiasi ~ T^4) dan Hukum Pergeseran Wien, di mana panjang gelombang dengan intensitas maksimum bergeser ke arah yang lebih pendek (warna biru/UV) seiring kenaikan suhu.""",
                "guide_content": """PETUNJUK PRAKTIKUM RADIASI BENDA HITAM

A. TUJUAN
1. Mengamati pengaruh suhu terhadap distribusi intensitas radiasi benda hitam.
2. Menentukan panjang gelombang dengan intensitas maksimum (λ max) pada berbagai suhu.
3. Memverifikasi Hukum Pergeseran Wien dan menentukan Konstanta Wien.

B. TEORI DASAR
Setiap benda dengan suhu T > 0 K memancarkan radiasi termal. Spektrum radiasi benda hitam dijelaskan oleh Hukum Planck.
Kurva intensitas radiasi memiliki puncak pada panjang gelombang tertentu (λ max).

Hukum Pergeseran Wien menyatakan bahwa:
λ max . T = b

Dimana:
λ max = Panjang gelombang intensitas maksimum (meter)
T = Suhu mutlak benda (Kelvin)
b = Konstanta pergeseran Wien (sekitar 2.898 x 10^-3 m.K)

Artinya, semakin tinggi suhu benda, puncak radiasinya bergeser ke panjang gelombang yang lebih pendek (warna bergeser dari merah ke biru).

C. LANGKAH PERCOBAAN
1. Buka Tab "Simulasi & Eksperimen".
2. Atur slider temperatur ke nilai terendah atau nilai tertentu (misal 3000 K).
3. Perhatikan bentuk kurva dan posisi puncaknya. Warna kotak di panel kiri menunjukkan perkiraan warna benda pijar tersebut.
4. Klik tombol "Catat Puncak (Lambda Max)" untuk menyimpan data suhu dan panjang gelombang puncak.
5. Naikkan suhu secara bertahap (misal kelipatan 1000 K) dan catat datanya setiap kali mengubah suhu.
6. Ambil minimal 5 titik data.

D. ANALISIS DATA
1. Buka Tab "Analisis Data".
2. Periksa tabel data yang telah Anda kumpulkan.
3. Klik "Hitung Konstanta Wien".
4. Program akan membuat grafik hubungan λ max vs 1/T dan menghitung gradien kemiringannya.
5. Bandingkan hasil perhitungan konstanta b dengan nilai referensi teori.

E. PENYIMPANAN DATA
Klik tombol "☁️ Simpan (DB & Excel)" pada tab Analisis untuk menyimpan hasil praktikum ke Excel dan Database."""
            },
            "EN": {
                "title": "Blackbody Radiation & Wien's Law Simulation",
                "tab_sim": "Simulation & Experiment",
                "tab_analisis": "Data Analysis (Wien's Law)",
                "tab_guide": "Laboratory Guide",
                "tab_scheme": "Equipment Scheme & Explanation",
                "tab_diagram": "Apparatus Diagram",
                "header_control": "Control Panel",
                "lbl_temp": "Temperature (Kelvin)",
                "lbl_color": "Approximate Object Color:",
                "header_capture": "Data Capture:",
                "btn_record": "Record Peak (Lambda Max)",
                "btn_save": "☁️ Save (DB & Excel)",
                "header_graph": "Spectral Radiation Curve (Intensity vs Wavelength)",
                "header_table": "Experimental Data Table",
                "col_temp": "T (Kelvin)",
                "col_lam": "λ max (nm)",
                "btn_calc": "Calculate Wien's Constant (b)",
                "btn_reset": "Reset Data",
                "header_analysis_graph": "Wien's Law Analysis Graph",
                "lbl_analysis_axis": "Y Axis: λ max (m) | X Axis: 1/T (1/K)",
                "lbl_result": "Result: b = ...",
                "res_fmt": "b (Calc) = {0:.4e} m.K\nError = {1:.2f}%",
                "msg_data_min": "Need at least 2 data points for linear analysis.",
                "msg_save_success": "Data saved successfully.",
                "msg_save_fail": "Failed to save data.",
                "lbl_axis_x_spec": "Wavelength (nm)",
                "lbl_axis_y_spec": "Intensity",
                "axis_x_anl": "1/T (K^-1)",
                "axis_y_anl": "λ max (nm)",
                "lbl_temp_fmt": "T = {0} K",
                "lbl_lambda_fmt": "Peak λ ≈ {0} nm",
                "graph_peak_label": "λmax\n{0} nm",
                "diag_oven": "Blackbody Oven",
                "diag_sensor": "Spectrophotometer Sensor",
                "diag_ctrl": "Control & Measurement",
                "diag_temp_disp": "{0} K",
                "diag_int_disp": "Intensity: {0}",
                "scheme_title": "Blackbody Radiation Experiment Scheme",
                "scheme_content": """APPARATUS SCHEME & EXPLANATION

This experiment simulates measuring the radiation spectrum of an ideal blackbody.

MAIN COMPONENTS:

1. Blackbody Simulator
   A radiation source consisting of a heated cavity with a small hole. The cavity walls emit and absorb radiation perfectly, so radiation exiting the hole has ideal blackbody spectrum characteristics.

2. Temperature Control & Sensor
   Used to adjust blackbody temperature (e.g. 1000 K - 10000 K). A thermocouple monitors actual temperature.

3. Dispersion Optical System (Spectrometer)
   Light from the blackbody passes through a prism or diffraction grating, splitting polychromatic light into its constituent wavelengths (spectrum).

4. Intensity Detector
   A sensor that scans along the spectrum to measure radiation intensity at specific wavelengths.

PHYSICAL MODEL:
Demonstrates Stefan-Boltzmann Law (Total Power ~ T^4) and Wien's Displacement Law, where peak intensity wavelength shifts shorter (red to blue) as temperature rises.""",
                "guide_content": """BLACKBODY RADIATION LAB GUIDE

A. OBJECTIVES
1. Observe effect of temperature on blackbody radiation intensity distribution.
2. Determine peak wavelength (lambda max) at various temperatures.
3. Verify Wien's Displacement Law and determine Wien's Constant.

B. BASIC THEORY
Every object with T > 0 K emits thermal radiation. Blackbody spectrum is described by Planck's Law.
The intensity curve has a peak at specific wavelength.
Wien's Displacement Law: lambda_max * T = b
Where b approx 2.898e-3 m.K.
As T increases, peak shifts to shorter wavelength (red to blue).

C. PROCEDURE
1. Open "Simulation" tab.
2. Adjust temperature slider (e.g. 3000 K).
3. Observe curve shape and peak. "Object Color" shows approximate color.
4. Click "Record Peak" to save T and lambda_max.
5. Increase temperature (e.g. steps of 1000 K).
6. Take at least 5 data points.

D. DATA ANALYSIS
1. Open "Data Analysis" tab.
2. Check data table.
3. Click "Calculate Wien's Constant".
4. Program graphs lambda_max vs 1/T and finds slope.
5. Compare result with theory.

E. SAVE DATA
Click "Save" button to export to Excel/DB."""
            }
        }

    def T(self, key):
        return self.translations.get(self.lang, self.translations["ID"]).get(key, key)

    def set_language(self, lang):
        self.lang = lang
        self.refresh_ui()

    def refresh_ui(self):
        if hasattr(self, 'lbl_title'): self.lbl_title.config(text=self.T("title"))
        if hasattr(self, 'notebook'):
            self.notebook.tab(self.tab_simulasi, text=self.T("tab_sim"))
            self.notebook.tab(self.tab_analisis, text=self.T("tab_analisis"))
            self.notebook.tab(self.tab_petunjuk, text=self.T("tab_guide"))
            self.notebook.tab(self.tab_scheme, text=self.T("tab_scheme"))
            self.notebook.tab(self.tab_diagram, text=self.T("tab_diagram"))
        
        if hasattr(self, 'lbl_panel_title'): self.lbl_panel_title.config(text=self.T("header_control"))
        if hasattr(self, 'lbl_temp_input'): self.lbl_temp_input.config(text=self.T("lbl_temp"))
        if hasattr(self, 'lbl_color_title'): self.lbl_color_title.config(text=self.T("lbl_color"))
        if hasattr(self, 'lbl_capture_title'): self.lbl_capture_title.config(text=self.T("header_capture"))
        if hasattr(self, 'btn_record'): self.btn_record.config(text=self.T("btn_record"))
        if hasattr(self, 'btn_save_sim'): self.btn_save_sim.config(text=self.T("btn_save"))
        if hasattr(self, 'lbl_graph_title'): self.lbl_graph_title.config(text=self.T("header_graph"))
        
        if hasattr(self, 'lbl_table_title'): self.lbl_table_title.config(text=self.T("header_table"))
        if hasattr(self, 'tree'):
            self.tree.heading("Temp", text=self.T("col_temp"))
            self.tree.heading("Lambda", text=self.T("col_lam"))
        if hasattr(self, 'btn_calc'): self.btn_calc.config(text=self.T("btn_calc"))
        if hasattr(self, 'btn_reset'): self.btn_reset.config(text=self.T("btn_reset"))
        if hasattr(self, 'btn_save_anl'): self.btn_save_anl.config(text=self.T("btn_save"))
        if hasattr(self, 'lbl_anl_graph_title'): self.lbl_anl_graph_title.config(text=self.T("header_analysis_graph"))
        if hasattr(self, 'lbl_anl_axis'): self.lbl_anl_axis.config(text=self.T("lbl_analysis_axis"))
        
        # Scheme
        if hasattr(self, 'lbl_scheme_title'): self.lbl_scheme_title.config(text=self.T("scheme_title"))
        if hasattr(self, 'txt_scheme'):
            self.txt_scheme.config(state="normal")
            self.txt_scheme.delete("1.0", tk.END)
            self.txt_scheme.insert("1.0", self.T("scheme_content"))
            self.txt_scheme.config(state="disabled")

        # Diagram
        if hasattr(self, 'canvas_diag'):
            self.canvas_diag.itemconfigure("diag_oven", text=self.T("diag_oven"))
            self.canvas_diag.itemconfigure("diag_sensor", text=self.T("diag_sensor"))
            self.canvas_diag.itemconfigure("diag_ctrl", text=self.T("diag_ctrl"))

        # Guide
        if hasattr(self, 'txt_guide'):
            self.txt_guide.config(state="normal")
            self.txt_guide.delete("1.0", tk.END)
            self.txt_guide.insert("1.0", self.T("guide_content"))
            self.txt_guide.config(state="disabled")

        self.update_graph()
        
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
        self.tab_simulasi = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_simulasi, text=self.T("tab_sim"))
        self.create_tab_simulasi()
        
        # Tab 2: Analysis (Wien's Law)
        self.tab_analisis = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_analisis, text=self.T("tab_analisis"))
        self.create_tab_analisis()
        
        # Tab 3: Guide
        self.tab_petunjuk = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_petunjuk, text=self.T("tab_guide"))
        self.create_tab_petunjuk()

        # Tab 4: Tools Scheme
        self.tab_scheme = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_scheme, text=self.T("tab_scheme"))
        self.create_tab_scheme()

        # Tab 5: Real Diagram
        self.tab_diagram = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_diagram, text=self.T("tab_diagram"))
        self.create_tab_diagram()

    def create_tab_diagram(self):
        self.canvas_diag = tk.Canvas(self.tab_diagram, bg="white")
        self.canvas_diag.pack(fill="both", expand=True, padx=20, pady=20)
        canvas = self.canvas_diag
        
        # Blackbody Oven Diagram
        # 1. Oven Unit
        canvas.create_rectangle(100, 150, 300, 350, fill="#7f8c8d", outline="black", width=2)
        canvas.create_rectangle(120, 170, 280, 330, fill="#bdc3c7", outline="black") # Inner insulation
        canvas.create_oval(180, 230, 220, 270, fill="black") # Aperture Hole
        canvas.create_text(200, 370, text=self.T("diag_oven"), font=("Arial", 12, "bold"), tags="diag_oven")
        
        # Heating Element Spirals (Symbolic)
        canvas.create_line(130, 180, 130, 320, fill="red", width=2, dash=(2,2)) 
        canvas.create_line(270, 180, 270, 320, fill="red", width=2, dash=(2,2)) 
        
        # 2. Spectrophotometer / Prism Sensor on Rail
        canvas.create_line(50, 400, 750, 400, width=5, fill="#34495e") # Optical Rail
        
        # Sensor Arm
        canvas.create_polygon(350, 400, 400, 250, 450, 400, fill="#3498db", outline="black")
        canvas.create_oval(380, 240, 420, 280, fill="black", outline="gray") # Lens
        canvas.create_text(400, 420, text=self.T("diag_sensor"), font=("Arial", 12, "bold"), tags="diag_sensor")
        
        # Light Rays
        canvas.create_line(220, 250, 380, 260, fill="orange", width=2, dash=(4,2))
        
        # 3. Control Unit
        canvas.create_rectangle(550, 150, 750, 300, fill="#2c3e50")
        canvas.create_text(650, 140, text=self.T("diag_ctrl"), font=("Arial", 11, "bold"), tags="diag_ctrl")
        
        # Display Temp
        canvas.create_rectangle(570, 170, 730, 220, fill="#16a085")
        canvas.create_text(650, 195, text=self.T("diag_temp_disp").format(3000), font=("Ds-Digital", 20), fill="white", tags="diag_temp_disp")
        
        # Display Intensity
        canvas.create_rectangle(570, 240, 730, 280, fill="#e67e22")
        canvas.create_text(650, 260, text=self.T("diag_int_disp").format(450), font=("Arial", 12, "bold"), fill="white", tags="diag_int_disp")
        
        # Cables
        canvas.create_line(300, 300, 550, 250, width=3, fill="black", smooth=True) # Power/Temp cable
        canvas.create_line(450, 350, 580, 290, width=2, fill="blue", smooth=True) # Sensor cable


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


    def create_tab_simulasi(self):
        container = self.tab_simulasi
        
        # Layout: Control Panel (Left), Spectrum Visualization (Center/Right)
        
        # --- Left Panel: Controls ---
        control_panel = tk.Frame(container, bg="white", bd=1, relief="solid", width=300)
        control_panel.pack(side="left", fill="y", padx=10, pady=10)
        control_panel.pack_propagate(False)
        
        self.lbl_panel_title = tk.Label(control_panel, text=self.T("header_control"), font=("Arial", 14, "bold"), bg="white")
        self.lbl_panel_title.pack(pady=20)
        
        # Temperature Slider
        self.lbl_temp_input = tk.Label(control_panel, text=self.T("lbl_temp"), font=("Arial", 12), bg="white")
        self.lbl_temp_input.pack(anchor="w", padx=20)
        self.temp_var = tk.DoubleVar(value=3000)
        self.temp_slider = tk.Scale(control_panel, from_=1000, to=10000, resolution=50, 
                                    orient="horizontal", variable=self.temp_var,
                                    command=lambda x: self.update_graph())
        self.temp_slider.pack(fill="x", padx=20, pady=5)
        
        self.lbl_temp = tk.Label(control_panel, text="T = 3000 K", font=("Courier New", 14, "bold"), bg="white", fg="#d63031")
        self.lbl_temp.pack(pady=5)
        
        # Color Preview (Approximation)
        self.lbl_color_title = tk.Label(control_panel, text=self.T("lbl_color"), font=("Arial", 11), bg="white")
        self.lbl_color_title.pack(anchor="w", padx=20, pady=(20, 5))
        self.color_preview = tk.Label(control_panel, bg="orange", width=20, height=3)
        self.color_preview.pack(pady=5)
        
        # Data Capture
        self.lbl_capture_title = tk.Label(control_panel, text=self.T("header_capture"), font=("Arial", 12, "bold"), bg="white")
        self.lbl_capture_title.pack(anchor="w", padx=20, pady=(30, 5))
        
        self.btn_record = tk.Button(control_panel, text=self.T("btn_record"), bg="#0984e3", fg="black", highlightbackground="#0984e3", font=("Arial", 11, "bold"),
                  command=self.record_data)
        self.btn_record.pack(fill="x", padx=20, pady=5)

        self.btn_save_sim = tk.Button(control_panel, text=self.T("btn_save"), bg="#27ae60", fg="black", highlightbackground="#27ae60", font=("Arial", 11, "bold"),
                  command=self.save_to_all)
        self.btn_save_sim.pack(fill="x", padx=20, pady=5)
                  
        self.lbl_lambda_max = tk.Label(control_panel, text="Peak λ = ... nm", font=("Arial", 12), bg="white")
        self.lbl_lambda_max.pack(pady=5)

        # --- Right Panel: Graph ---
        graph_wrapper = tk.Frame(container, bg="white", bd=1, relief="solid")
        graph_wrapper.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.lbl_graph_title = tk.Label(graph_wrapper, text=self.T("header_graph"), 
                 font=("Arial", 14), bg="white")
        self.lbl_graph_title.pack(pady=10)
                 
        self.canvas_plot = tk.Canvas(graph_wrapper, bg="#f1f2f6", width=600, height=400)
        self.canvas_plot.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Initial Draw
        self.update_graph()

    def create_tab_analisis(self):
        container = self.tab_analisis
        
        # Left: Table & Calc
        left_panel = tk.Frame(container, bg="white", bd=1, relief="solid", width=350)
        left_panel.pack(side="left", fill="y", padx=10, pady=10)
        left_panel.pack_propagate(False)
        
        self.lbl_table_title = tk.Label(left_panel, text=self.T("header_table"), font=("Arial", 14, "bold"), bg="white")
        self.lbl_table_title.pack(pady=15)
        
        # Treeview
        cols = ("Temp", "Lambda")
        self.tree = ttk.Treeview(left_panel, columns=cols, show="headings", height=10)
        self.tree.heading("Temp", text=self.T("col_temp"))
        self.tree.heading("Lambda", text=self.T("col_lam"))
        self.tree.column("Temp", width=100, anchor="center")
        self.tree.column("Lambda", width=120, anchor="center")
        self.tree.pack(fill="x", padx=10, pady=5)
        
        # Buttons
        self.btn_calc = tk.Button(left_panel, text=self.T("btn_calc"), bg="#6c5ce7", fg="black", highlightbackground="#6c5ce7", font=("Arial", 11, "bold"),
                  command=self.calculate_constant)
        self.btn_calc.pack(fill="x", padx=20, pady=20)
                  
        self.btn_reset = tk.Button(left_panel, text=self.T("btn_reset"), bg="#d63031", fg="black", highlightbackground="#d63031", font=("Arial", 11),
                  command=self.reset_data)
        self.btn_reset.pack(fill="x", padx=20, pady=5)

        self.btn_save_anl = tk.Button(left_panel, text=self.T("btn_save"), bg="#27ae60", fg="black", highlightbackground="#27ae60", font=("Arial", 11),
                  command=self.save_to_all)
        self.btn_save_anl.pack(fill="x", padx=20, pady=5)
                  
        self.lbl_result = tk.Label(left_panel, text=self.T("lbl_result"), font=("Arial", 12), bg="white", justify="left", wraplength=300)
        self.lbl_result.pack(pady=20)

        # Right: Graph (1/T vs Lambda or similar)
        
        right_panel = tk.Frame(container, bg="white", bd=1, relief="solid")
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.lbl_anl_graph_title = tk.Label(right_panel, text=self.T("header_analysis_graph"), font=("Arial", 14, "bold"), bg="white")
        self.lbl_anl_graph_title.pack(pady=10)
        self.lbl_anl_axis = tk.Label(right_panel, text=self.T("lbl_analysis_axis"), font=("Arial", 11), bg="white")
        self.lbl_anl_axis.pack()
        
        self.canvas_analysis = tk.Canvas(right_panel, bg="#f1f2f6")
        self.canvas_analysis.pack(fill="both", expand=True, padx=20, pady=20)

    def create_tab_petunjuk(self):
        container = self.tab_petunjuk
        self.txt_guide = tk.Text(container, font=("Arial", 12), padx=20, pady=20, wrap="word")
        self.txt_guide.pack(fill="both", expand=True)
        
        self.txt_guide.insert("1.0", self.T("guide_content"))
        self.txt_guide.config(state="disabled")

    # --- LOGIC METHODS ---

    def planck_law(self, wav_nm, T):
        lam = wav_nm * 1e-9
        if lam == 0: return 0
        try:
            p1 = (2 * self.h * self.c**2) / (lam**5)
            # Clip exponent to avoid overflow
            exponent = (self.h * self.c) / (lam * self.k * T)
            if exponent > 700: 
                intensity = 0
            else:
                p2 = math.exp(exponent) - 1
                intensity = p1 / p2
        except (OverflowError, ZeroDivisionError):
            intensity = 0
        return intensity

    def record_data(self):
        T = self.temp_var.get()
        lambda_max_m = self.b / T
        lambda_max_nm = lambda_max_m * 1e9
        
        # Add to table
        vals = (int(T), f"{lambda_max_nm:.1f}")
        self.tree.insert("", "end", values=vals)
        
        # Save to list
        # Using dict approach for unified saver
        self.data_points.append({
            "Modul": "Radiasi Benda Hitam",
            "Temperature (K)": T,
            "Lambda Peak (nm)": lambda_max_nm,
            "Konstanta Wien (m.K)": self.b
        })
        self.update_analysis_graph()
        
    def get_data(self):
        return self.data_points

    def get_color_from_temp(self, temp):
        if temp < 1000: return "#ff3300" # Deep red
        if temp < 3000: return "#ff6600" # Orange red
        if temp < 5000: return "#ffcc00" # Orange yellow
        if temp < 6000: return "#ffffcc" # Yellowish white
        if temp < 8000: return "#ccffff" # Bluish white
        return "#99ccff" # Blueish

    def update_graph(self):
        T = self.temp_var.get()
        self.lbl_temp.config(text=self.T("lbl_temp_fmt").format(int(T)))
        col = self.get_color_from_temp(T)
        self.color_preview.config(bg=col)
        
        lambda_max_m = self.b / T
        lambda_max_nm = lambda_max_m * 1e9
        
        self.lbl_lambda_max.config(text=self.T("lbl_lambda_fmt").format(int(lambda_max_nm)))
        
        self.canvas_plot.delete("all")
        
        w = self.canvas_plot.winfo_width()
        h = self.canvas_plot.winfo_height()
        if w==1: w=600  
        if h==1: h=400
        padding = 40
        
        # Axes
        self.canvas_plot.create_line(padding, h-padding, w-padding, h-padding, width=2, arrow="last") 
        self.canvas_plot.create_line(padding, h-padding, padding, padding, width=2, arrow="last") 
        
        # Axis Labels
        lbl_x = self.T("lbl_axis_x_spec")
        lbl_y = self.T("lbl_axis_y_spec")
        
        self.canvas_plot.create_text(w-padding, h-padding+20, text=lbl_x)
        self.canvas_plot.create_text(padding, padding-20, text=lbl_y)
        
        min_x_nm = 100
        max_x_nm = 3000
        
        def to_screen_x(nm):
            return padding + ((nm - min_x_nm) / (max_x_nm - min_x_nm)) * (w - 2*padding)
            
        vis_start = to_screen_x(380)
        vis_end = to_screen_x(750)
        rainbow_colors = ["#8B00FF", "#4B0082", "#0000FF", "#00FF00", "#FFFF00", "#FF7F00", "#FF0000"]
        rect_w = (vis_end - vis_start) / len(rainbow_colors)
        for i, c in enumerate(rainbow_colors):
            x1 = vis_start + i*rect_w
            self.canvas_plot.create_rectangle(x1, h-padding-5, x1+rect_w, h-padding, fill=c, outline="")

        if self.temp_var.get() < 100: return 

        peak_int = self.planck_law(lambda_max_nm, T)
        if peak_int == 0: return

        points = []
        step = 20 # nm resolution
        for lam in range(min_x_nm, max_x_nm, step):
            intensity = self.planck_law(lam, T)
            x = to_screen_x(lam)
            y_norm = intensity / peak_int 
            y = (h - padding) - (y_norm * (h - 2*padding) * 0.9)
            points.append(x)
            points.append(y)
            
        if len(points) > 4:
            self.canvas_plot.create_line(points, fill="black", width=2, smooth=True)
            
        px = to_screen_x(lambda_max_nm)
        py = (h - padding) - (1.0 * (h - 2*padding) * 0.9)
        self.canvas_plot.create_oval(px-4, py-4, px+4, py+4, fill="red")
        
        label_txt = self.T("graph_peak_label").format(int(lambda_max_nm))
        self.canvas_plot.create_text(px, py-15, text=label_txt, fill="red", font=("Arial", 9))

    def reset_data(self):
        self.data_points = []
        for x in self.tree.get_children():
            self.tree.delete(x)
        self.lbl_result.config(text=self.T("lbl_result"))
        self.canvas_analysis.delete("all")

    def save_to_all(self):
        data = self.get_data()
        saved, msg = DataManager.save_data_unified(data, "RadiasiBendaHitam")
        if saved:
            messagebox.showinfo(self.T("btn_save"), self.T("msg_save_success") + f"\n{msg}")
        else:
            messagebox.showerror(self.T("btn_save"), self.T("msg_save_fail") + f"\n{msg}")

    def update_analysis_graph(self):
        self.canvas_analysis.delete("all")
        if not self.data_points: return
        
        w = self.canvas_analysis.winfo_width()
        h = self.canvas_analysis.winfo_height()
        if w==1: w=400
        if h==1: h=300
        padding = 40
        
        min_x = 0
        max_x = 0.0012 
        max_y = 3000   
        
        self.canvas_analysis.create_line(padding, h-padding, w-padding, h-padding, width=2) 
        self.canvas_analysis.create_line(padding, h-padding, padding, padding, width=2)     
        self.canvas_analysis.create_text(w-padding, h-padding+20, text=self.T("axis_x_anl"))
        self.canvas_analysis.create_text(padding, padding-20, text=self.T("axis_y_anl"))

        for item in self.data_points:
            T = item["Temperature (K)"]
            lam_nm = item["Lambda Peak (nm)"]
            
            inv_T = 1.0 / T
            screen_x = padding + (inv_T / max_x) * (w - 2*padding)
            screen_y = (h - padding) - (lam_nm / max_y) * (h - 2*padding)
            self.canvas_analysis.create_oval(screen_x-3, screen_y-3, screen_x+3, screen_y+3, fill="blue")

    def calculate_constant(self):
        if len(self.data_points) < 2:
            messagebox.showwarning("Error", self.T("msg_data_min"))
            return
        sum_x = sum_y = sum_xy = sum_xx = 0
        n = len(self.data_points)
        for item in self.data_points:
            T = item["Temperature (K)"]
            lam_nm = item["Lambda Peak (nm)"]
            
            x = 1.0 / T
            y = lam_nm * 1e-9 
            sum_x += x; sum_y += y; sum_xy += x*y; sum_xx += x*x
        denominator = (n * sum_xx - sum_x**2)
        if denominator == 0: return
        slope_b = (n * sum_xy - sum_x * sum_y) / denominator
        error = abs(slope_b - self.b) / self.b * 100
        
        res = self.T("res_fmt").format(slope_b, error)
        self.lbl_result.config(text=res)
        self.draw_regression_line(slope_b)
        
    def draw_regression_line(self, slope):
        w = self.canvas_analysis.winfo_width()
        h = self.canvas_analysis.winfo_height()
        padding = 40
        max_x = 0.0012
        max_y_nm = 3000
        x2 = 0.001
        y2_nm = slope * x2 * 1e9
        
        def to_scr(x, y_nm):
             sx = padding + (x / max_x) * (w - 2*padding)
             sy = (h - padding) - (y_nm / max_y_nm) * (h - 2*padding)
             return sx, sy
        sx1, sy1 = to_scr(0, 0)
        sx2, sy2 = to_scr(x2, y2_nm)
        self.canvas_analysis.create_line(sx1, sy1, sx2, sy2, fill="red", dash=(4,4), width=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabRadiasiBendaHitam(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
