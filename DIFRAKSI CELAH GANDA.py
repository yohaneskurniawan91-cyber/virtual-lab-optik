import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from virtual_lab_data_manager import DataManager, ScrollableFrame

class VirtualLabDifraksiGanda(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#f5f6fa")
        
        self.setup_translations()
        self.lang = "ID"
        
        # Spectrum Data
        self.spektrum = {
            "Ungu (400 nm)": {"nm": 400, "rgb": "#8e44ad"},
            "Biru (450 nm)": {"nm": 450, "rgb": "#3498db"},
            "Hijau (530 nm)": {"nm": 530, "rgb": "#2ecc71"},
            "Kuning (580 nm)": {"nm": 580, "rgb": "#f1c40f"},
            "Jingga (600 nm)": {"nm": 600, "rgb": "#e67e22"},
            "Merah (650 nm)": {"nm": 650, "rgb": "#e74c3c"}
        }
        
        # Default State
        self.current_wavelength = 530e-9 # m
        self.current_color = "#2ecc71"
        self.L = 1.0 # m (Distance to screen)
        self.d = 0.2e-3 # m (Slit separation 0.2mm)
        self.analysis_data = []

        self.create_widgets()
        self.update_params()
        
        self.set_language("ID")

    def setup_translations(self):
        self.translations = {
            "ID": {
                "title": "Difraksi Celah Ganda (Young Experiment)",
                "tab_sim": "Simulasi Pola Interferensi",
                "tab_ana": "Analisis Data",
                "tab_guide": "Petunjuk Praktikum",
                "tab_scheme": "Skema Alat & Penjelasan",
                "tab_diagram": "Gambaran Rangkaian Alat",
                "sim_param_title": "Parameter Laser & Celah",
                "grp_source": "1. Sumber Cahaya",
                "grp_d": "2. Jarak Antar Celah (d)",
                "grp_L": "3. Jarak Layar (L)",
                "grp_res": "Hasil Teoretis",
                "lbl_delta_y": "Jarak Pita (Δy):",
                "btn_record": "Catat Data ke Tabel",
                "btn_clear": "Hapus Semua Data",
                "btn_save": "Simpan Data (Unified)",
                "col_color": "Warna",
                "col_d": "d (mm)",
                "col_L": "L (m)",
                "col_dy": "Δy Teori (mm)",
                "col_y": "y_ukur (mm) [m=1]",
                "col_err": "Error %",
                "plot_title": "Hubungan L vs Δy",
                "plot_x": "Jarak Layar L (m)",
                "plot_y": "Δy (mm)",
                "msg_rec_success": "Data berhasil dicatat!",
                "msg_clear_confirm": "Hapus semua data dalam tabel?",
                "scheme_title": "Skema Percobaan Celah Ganda Young",
                "scheme_content": """SKEMA ALAT DAN PENJELASAN

Percobaan ini menggunakan prinsip interferensi gelombang cahaya untuk membuktikan sifat gelombang dari cahaya.

KOMPONEN ALAT:

1. Sumber Cahaya Laser (Monokromatik Koheren)
   Mengemisikan berkas cahaya dengan satu panjang gelombang (warna) yang fasa gelombangnya seragam (koheren). Pilihan warna: Merah (650nm), Hijau (532nm), dll.

2. Celah Ganda (Double Slit)
   Sebuah plat halangan optik yang memiliki dua celah sangat sempit yang berdekatan (jarak pisah 'd', biasanya orde 0.1 - 0.5 mm).
   Fungsi: Memecah satu muka gelombang menjadi dua sumber gelombang baru yang koheren (Prinsip Huygens).

3. Bangku Optik (Optical Rail)
   Rel panjang untuk meletakkan dan mensejajarkan komponen optik (Laser, Celah, Layar).

4. Layar Pengamat
   Bidang putih tempat pola interferensi (garis terang-gelap) terbentuk. Terletak pada jarak 'L' dari celah ganda (biasanya 1 - 3 meter).

PRINSIP KERJA:
Dua gelombang cahaya yang keluar dari celah ganda akan merambat dan bertemu di layar.
- Interferensi Konstruktif (Pita Terang): Terjadi jika selisih lintasan optik adalah kelipatan bulat dari panjang gelombang (ΔS = nλ).
- Interferensi Destruktif (Pita Gelap): Terjadi jika selisih lintasan adalah kelipatan ganjil setengah panjang gelombang.""",
                "guide_content": """PETUNJUK PRAKTIKUM DIFRAKSI CELAH GANDA (YOUNG)

A. DASAR TEORI
Percobaan celah ganda Young membuktikan sifat gelombang cahaya melalui fenomena interferensi.
Dua gelombang cahaya koheren dari celah sempit (S1 dan S2) bertemu di layar dan saling berinterferensi.

Rumus Interferensi Konstruktif (Pita Terang):
d sin(θ) = m λ
Untuk sudut kecil, y/L ≈ sin(θ) ≈ tan(θ), maka:
y = (m λ L) / d

Dimana:
y = Jarak pita terang ke-m dari terang pusat
d = Jarak antar celah
L = Jarak celah ke layar
λ = Panjang gelombang
m = Orde interferensi (0, 1, 2...)

B. LANGKAH PERCOBAAN
1. Atur Warna (Panjang Gelombang) laser.
2. Atur Variabel Bebas:
   - Jarak Celah (d)
   - Jarak Layar (L)
3. Amati Pola Interferensi pada layar simulasi.
   - Grafik Intensitas menunjukkan distribusi terang-gelap.
   - Pita visual di bawah grafik menunjukkan apa yang terlihat mata.
4. Perhatikan nilai Δy (jarak antar pita terang) di panel kiri.
5. Klik "Catat Data" untuk menyimpan konfigurasi saat ini ke tabel Analisis.
6. Coba variasikan 'd' dan 'L' untuk melihat hubungannya dengan Δy.
   - Jika 'd' diperbesar, pola semakin rapat (Δy mengecil).
   - Jika 'L' diperbesar, pola semakin lebar (Δy membesar).

C. ANALISIS & PENYIMPANAN
1. Masuk ke tab Analisis untuk melihat tabel data.
2. Lakukan perhitungan manual atau ekspor data.
3. Klik tombol "Simpan Data (Unified)" pada tab Analisis untuk menyimpan laporan ke Excel/Database.""",
                "diag_title": "Young's Double Slit Experiment Setup",
                "diag_laser": "Laser Source",
                "diag_slit": "Double Slit",
                "diag_screen": "Observation Screen",
                "diag_dist": "Distance (L)"
            },
            "EN": {
                "title": "Double Slit Diffraction (Young's Experiment)",
                "tab_sim": "Interference Pattern Simulation",
                "tab_ana": "Data Analysis",
                "tab_guide": "Practical Guide",
                "tab_scheme": "Tool Scheme & Explanation",
                "tab_diagram": "Device Circuit Overview",
                "sim_param_title": "Laser & Slit Parameters",
                "grp_source": "1. Light Source",
                "grp_d": "2. Slit Distance (d)",
                "grp_L": "3. Screen Distance (L)",
                "grp_res": "Theoretical Results",
                "lbl_delta_y": "Fringe Spacing (Δy):",
                "btn_record": "Record Data to Table",
                "btn_clear": "Clear All Data",
                "btn_save": "Save Data (Unified)",
                "col_color": "Color",
                "col_d": "d (mm)",
                "col_L": "L (m)",
                "col_dy": "Theory Δy (mm)",
                "col_y": "Measured y (mm) [m=1]",
                "col_err": "Error %",
                "plot_title": "Relationship L vs Δy",
                "plot_x": "Screen Distance L (m)",
                "plot_y": "Δy (mm)",
                "msg_rec_success": "Data successfully recorded!",
                "msg_clear_confirm": "Clear all data in table?",
                "scheme_title": "Young's Double Slit Experiment Scheme",
                "scheme_content": """TOOL SCHEME AND EXPLANATION

This experiment uses the principle of light wave interference to prove the wave nature of light.

TOOL COMPONENTS:

1. Laser Light Source (Coherent Monochromatic)
   Emits a light beam with a single wavelength (color) where wave phases are uniform (coherent). Color options: Red (650nm), Green (532nm), etc.

2. Double Slit
   An optical barrier plate having two very narrow adjacent slits (separation distance 'd', usually order 0.1 - 0.5 mm).
   Function: Splits one wavefront into two new coherent wave sources (Huygens Principle).

3. Optical Rail
   Long rail for placing and aligning optical components (Laser, Slit, Screen).

4. Observation Screen
   White plane where the interference pattern (bright-dark lines) is formed. Located at distance 'L' from the double slit (usually 1 - 3 meters).

WORKING PRINCIPLE:
Two light waves exiting the double slit will propagate and meet at the screen.
- Constructive Interference (Bright Fringe): Occurs if optical path difference is an integer multiple of wavelength (ΔS = nλ).
- Destructive Interference (Dark Fringe): Occurs if path difference is an odd multiple of half wavelength.""",
                "guide_content": """PRACTICAL GUIDE: DOUBLE SLIT DIFFRACTION (YOUNG)

A. THEORETICAL BASIS
Young's double slit experiment proves the wave nature of light through interference phenomena.
Two coherent light waves from narrow slits (S1 and S2) meet at the screen and interfere with each other.

Constructive Interference Formula (Bright Fringe):
d sin(θ) = m λ
For small angles, y/L ≈ sin(θ) ≈ tan(θ), so:
y = (m λ L) / d

Where:
y = Distance of m-th bright fringe from central bright fringe
d = Slit distance
L = Slit to screen distance
λ = Wavelength
m = Interference order (0, 1, 2...)

B. EXPERIMENTAL STEPS
1. Set Laser Color (Wavelength).
2. Set Independent Variables:
   - Slit Distance (d)
   - Screen Distance (L)
3. Observe Interference Pattern on simulation screen.
   - Intensity Graph shows bright-dark distribution.
   - Visual Band below graph shows what the eye sees.
4. Note the Δy value (fringe spacing) in left panel.
5. Click "Record Data" to save current config to Analysis table.
6. Try varying 'd' and 'L' to see their relationship with Δy.
   - If 'd' increases, pattern gets denser (Δy decreases).
   - If 'L' increases, pattern gets wider (Δy increases).

C. ANALYSIS & SAVING
1. Go to Analysis tab to view data table.
2. Perform manual calculations or export data.
3. Click "Save Data (Unified)" on Analysis tab to save report to Excel/Database.""",
                "diag_title": "Young's Double Slit Experiment Setup",
                "diag_laser": "Laser Source",
                "diag_slit": "Double Slit",
                "diag_screen": "Observation Screen",
                "diag_dist": "Distance (L)"
            }
        }

    def T(self, key):
        return self.translations.get(self.lang, self.translations["ID"]).get(key, key)

    def set_language(self, lang):
        self.lang = lang
        self.refresh_ui()

    def refresh_ui(self):
        # Header
        self.lbl_main_title.config(text=self.T("title"))
        
        # Tabs
        self.notebook.tab(0, text=self.T("tab_sim"))
        self.notebook.tab(1, text=self.T("tab_ana"))
        self.notebook.tab(2, text=self.T("tab_guide"))
        self.notebook.tab(3, text=self.T("tab_scheme"))
        self.notebook.tab(4, text=self.T("tab_diagram"))
        
        # Sim UI
        self.lbl_sim_param_title.config(text=self.T("sim_param_title"))
        self.lf_source.config(text=self.T("grp_source"))
        self.lf_d.config(text=self.T("grp_d"))
        self.lf_L.config(text=self.T("grp_L"))
        self.lf_res.config(text=self.T("grp_res"))
        self.btn_record.config(text=self.T("btn_record"))
        self.update_params() # Re-update dynamic labels (L, d, deltay)
        
        # Analysis UI
        col_ids = ("color", "d", "L", "dy", "y", "err")
        headers = (
            self.T("col_color"), self.T("col_d"), self.T("col_L"), 
            self.T("col_dy"), self.T("col_y"), self.T("col_err")
        )
        # self.tree.configure(columns=col_ids) # Do NOT reconfigure columns
        for c, text in zip(col_ids, headers):
            self.tree.heading(c, text=text)

        self.btn_clear.config(text=self.T("btn_clear"))
        self.btn_save.config(text=self.T("btn_save"))
        self.ax.set_title(self.T("plot_title"))
        self.ax.set_xlabel(self.T("plot_x"))
        self.ax.set_ylabel(self.T("plot_y"))
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
        
        # Diagram
        self.canvas_diag.itemconfigure("diag_title", text=self.T("diag_title"))
        self.canvas_diag.itemconfigure("diag_laser", text=self.T("diag_laser"))
        self.canvas_diag.itemconfigure("diag_slit", text=self.T("diag_slit"))
        self.canvas_diag.itemconfigure("diag_screen", text=self.T("diag_screen"))
        self.canvas_diag.itemconfigure("diag_dist", text=self.T("diag_dist"))
            
        
    def create_widgets(self):
        # Header
        header = tk.Frame(self, bg="#2c3e50", pady=10)
        header.pack(fill="x")
        self.lbl_main_title = tk.Label(header, text=self.T("title"), 
                 font=("Helvetica", 18, "bold"), fg="#ecf0f1", bg="#2c3e50")
        self.lbl_main_title.pack()
        
        # Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Simulation
        self.tab_sim = tk.Frame(self.notebook, bg="#f5f6fa") # Full Tab
        self.notebook.add(self.tab_sim, text=self.T("tab_sim"))
        self.create_sim_ui()
        
        # Tab 2: Analysis
        self.tab_ana = tk.Frame(self.notebook, bg="#f5f6fa") # Full Tab
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
        self.canvas_diag = tk.Canvas(self.tab_diagram, bg="white")
        self.canvas_diag.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Interference Setup Diagram
        self.canvas_diag.create_text(400, 50, text=self.T("diag_title"), font=("Arial", 14, "bold"), tag="diag_title")
        
        # Rail
        self.canvas_diag.create_line(50, 250, 750, 250, width=5, fill="#bdc3c7")
        
        # 1. Laser
        self.canvas_diag.create_rectangle(50, 220, 150, 250, fill="#e74c3c", outline="black")
        self.canvas_diag.create_text(100, 210, text=self.T("diag_laser"), font=("Arial", 11, "bold"), tag="diag_laser")
        self.canvas_diag.create_line(150, 235, 250, 235, fill="red", width=2) # Beam
        
        # 2. Slit Holder
        self.canvas_diag.create_rectangle(250, 200, 260, 270, fill="black")
        self.canvas_diag.create_line(255, 270, 255, 290, width=4, fill="black") # Post
        self.canvas_diag.create_text(255, 185, text=self.T("diag_slit"), font=("Arial", 10), tag="diag_slit")
        
        # Beam spread (fan out)
        self.canvas_diag.create_polygon(260, 235, 650, 150, 650, 320, fill="", outline="red", dash=(2,4))
        
        # 3. Screen
        self.canvas_diag.create_rectangle(650, 150, 660, 320, fill="white", outline="black")
        self.canvas_diag.create_line(655, 320, 655, 340, width=4, fill="black") # Post
        self.canvas_diag.create_text(655, 130, text=self.T("diag_screen"), font=("Arial", 11, "bold"), tag="diag_screen")
        
        # Pattern on screen (Symbolic)
        for y in range(160, 310, 10):
            self.canvas_diag.create_line(662, y, 662, y+5, fill="red", width=3)

        # Distance labels
        self.canvas_diag.create_line(255, 300, 655, 300, arrow="both", fill="blue")
        self.canvas_diag.create_text(455, 315, text=self.T("diag_dist"), fill="blue", tag="diag_dist")


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


    def create_sim_ui(self):
        main_layout = tk.Frame(self.tab_sim, bg="#f5f6fa")
        main_layout.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left: Controls
        left_panel = tk.Frame(main_layout, width=300, bg="white", relief="raised", bd=1)
        left_panel.pack(side="left", fill="y", padx=5)
        
        self.lbl_sim_param_title = tk.Label(left_panel, text=self.T("sim_param_title"), font=("Arial", 12, "bold"), bg="white")
        self.lbl_sim_param_title.pack(pady=10)
        
        # 1. Wavelength
        self.lf_source = tk.LabelFrame(left_panel, text=self.T("grp_source"), bg="white")
        self.lf_source.pack(fill="x", padx=10, pady=5)
        
        self.wav_var = tk.StringVar(value="Hijau (530 nm)")
        cb_wav = ttk.Combobox(self.lf_source, textvariable=self.wav_var, values=list(self.spektrum.keys()), state="readonly")
        cb_wav.pack(fill="x", padx=10, pady=5)
        cb_wav.bind("<<ComboboxSelected>>", self.update_params)
        
        # 2. Slit Separation (d)
        self.lf_d = tk.LabelFrame(left_panel, text=self.T("grp_d"), bg="white")
        self.lf_d.pack(fill="x", padx=10, pady=5)
        
        self.lbl_d = tk.Label(self.lf_d, text="d = 0.20 mm", bg="white", fg="blue")
        self.lbl_d.pack()
        self.d_var = tk.DoubleVar(value=0.2)
        tk.Scale(self.lf_d, from_=0.05, to=0.8, resolution=0.01, orient="horizontal", 
                 variable=self.d_var, command=self.update_params, bg="white").pack(fill="x", padx=10)
                 
        # 3. Screen Distance (L)
        self.lf_L = tk.LabelFrame(left_panel, text=self.T("grp_L"), bg="white")
        self.lf_L.pack(fill="x", padx=10, pady=5)
        
        self.lbl_L = tk.Label(self.lf_L, text="L = 1.00 m", bg="white", fg="blue")
        self.lbl_L.pack()
        self.L_var = tk.DoubleVar(value=1.0)
        tk.Scale(self.lf_L, from_=0.5, to=3.0, resolution=0.1, orient="horizontal", 
                 variable=self.L_var, command=self.update_params, bg="white").pack(fill="x", padx=10)
                 
        # Info Box
        self.lf_res = tk.LabelFrame(left_panel, text=self.T("grp_res"), bg="#ecf0f1")
        self.lf_res.pack(fill="x", padx=10, pady=20)
        self.lbl_delta_y = tk.Label(self.lf_res, text=f"{self.T('lbl_delta_y')} -- mm", font=("Arial", 14, "bold"), bg="#ecf0f1")
        self.lbl_delta_y.pack(pady=10)
        
        self.btn_record = tk.Button(left_panel, text=self.T("btn_record"), bg="#3498db", fg="black", command=self.record_data)
        self.btn_record.pack(fill="x", padx=10, pady=20)

        # Center: Visualization
        right_panel = tk.Frame(main_layout, bg="#2d3436")
        right_panel.pack(side="left", fill="both", expand=True, padx=5)
        
        # Canvas for Pattern + Graph
        self.cv_w = 600
        self.cv_h = 500
        self.canvas = tk.Canvas(right_panel, bg="black", width=self.cv_w, height=self.cv_h)
        self.canvas.pack(fill="both", expand=True)

    def create_analysis_ui(self):
        # Paned Window Split (Left: Table/Controls, Right: Graph)
        paned = tk.PanedWindow(self.tab_ana, orient=tk.HORIZONTAL, bg="#f5f6fa", sashwidth=5)
        paned.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left Frame
        left_frame = tk.Frame(paned, bg="white", width=450)
        paned.add(left_frame, minsize=450)

        # Table
        self.col_ids = ("color", "d", "L", "dy", "y", "err")
        self.tree = ttk.Treeview(left_frame, columns=self.col_ids, show="headings", height=15)
        
        headers = (
            self.T("col_color"), self.T("col_d"), self.T("col_L"), 
            self.T("col_dy"), self.T("col_y"), self.T("col_err")
        )
        
        for c, text in zip(self.col_ids, headers):
            self.tree.heading(c, text=text)
            width = 80 if c in ["d", "dy", "y"] else 60
            if c == "color": width = 100
            self.tree.column(c, width=width, anchor="center")
            
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        btn_box = tk.Frame(left_frame, bg="white")
        btn_box.pack(fill="x", pady=10, padx=5)
        
        self.btn_clear = tk.Button(btn_box, text=self.T("btn_clear"), command=self.clear_data, bg="#c0392b", fg="black")
        self.btn_clear.pack(side="left", padx=5, fill="x", expand=True)
        self.btn_save = tk.Button(btn_box, text=self.T("btn_save"), command=self.save_data_unified, bg="#3498db", fg="black")
        self.btn_save.pack(side="left", padx=5, fill="x", expand=True)

        # Right Frame: Graph Area
        right_frame = tk.Frame(paned, bg="white", bd=1, relief="solid")
        paned.add(right_frame)

        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.ax.set_title(self.T("plot_title"))
        self.ax.set_ylabel(self.T("plot_y"))
        self.ax.set_xlabel(self.T("plot_x"))
        self.ax.grid(True)
        
        self.graph_canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        self.toolbar = NavigationToolbar2Tk(self.graph_canvas, right_frame)
        self.toolbar.update()
        self.graph_canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_guide_ui(self):
        frame = tk.Frame(self.tab_guide)
        frame.pack(fill="both", expand=True)

        self.txt_guide = tk.Text(frame, font=("Arial", 12), padx=20, pady=20, wrap="word")
        scr = ttk.Scrollbar(frame, command=self.txt_guide.yview)
        self.txt_guide.configure(yscrollcommand=scr.set)
        
        scr.pack(side="right", fill="y")
        self.txt_guide.pack(side="left", fill="both", expand=True)
        content = """
PETUNJUK PRAKTIKUM DIFRAKSI CELAH GANDA (YOUNG)

A. DASAR TEORI
Percobaan celah ganda Young membuktikan sifat gelombang cahaya melalui fenomena interferensi.
Dua gelombang cahaya koheren dari celah sempit (S1 dan S2) bertemu di layar dan saling berinterferensi.

Rumus Interferensi Konstruktif (Pita Terang):
d sin(θ) = m λ
Untuk sudut kecil, y/L ≈ sin(θ) ≈ tan(θ), maka:
y = (m λ L) / d

Dimana:
y = Jarak pita terang ke-m dari terang pusat
d = Jarak antar celah
L = Jarak celah ke layar
λ = Panjang gelombang
m = Orde interferensi (0, 1, 2...)

B. LANGKAH PERCOBAAN
1. Atur Warna (Panjang Gelombang) laser.
2. Atur Variabel Bebas:
   - Jarak Celah (d)
   - Jarak Layar (L)
3. Amati Pola Interferensi pada layar simulasi.
   - Grafik Intensitas menunjukkan distribusi terang-gelap.
   - Pita visual di bawah grafik menunjukkan apa yang terlihat mata.
4. Perhatikan nilai Δy (jarak antar pita terang) di panel kiri.
5. Klik "Catat Data" untuk menyimpan konfigurasi saat ini ke tabel Analisis.
6. Coba variasikan 'd' dan 'L' untuk melihat hubungannya dengan Δy.
   - Jika 'd' diperbesar, pola semakin rapat (Δy mengecil).
   - Jika 'L' diperbesar, pola semakin lebar (Δy membesar).

C. ANALISIS & PENYIMPANAN
1. Masuk ke tab Analisis untuk melihat tabel data.
2. Lakukan perhitungan manual atau ekspor data.
3. Klik tombol "Simpan Data (Unified)" pada tab Analisis untuk menyimpan laporan ke Excel/Database.
"""
        self.txt_guide.insert("1.0", content)
        self.txt_guide.config(state="disabled")

    def update_params(self, event=None):
        # Read Inputs
        spec_name = self.wav_var.get()
        # If spec_name contains color name, it might be translated?
        # The key is from self.spektrum which is fixed keys. 
        # But the combobox values are from spektrum.keys().
        
        # If I translate combo box values, I need to map back to logic.
        # Current impl uses "Ungu (400 nm)" as key.
        # I won't translate the color keys for now to keep logic simple, 
        # or I will assume English keys if I did. But I didn't translate spektrum keys.
        
        if spec_name in self.spektrum:
            self.current_wavelength = self.spektrum[spec_name]["nm"] * 1e-9
            self.current_color = self.spektrum[spec_name]["rgb"]
        
        val_d_mm = self.d_var.get()
        self.d = val_d_mm * 1e-3
        self.lbl_d.config(text=f"d = {val_d_mm:.2f} mm")
        
        val_L_m = self.L_var.get()
        self.L = val_L_m
        self.lbl_L.config(text=f"L = {val_L_m:.2f} m")
        
        # Calculate Delta y (m=1)
        # y = lambda * L / d
        self.dy = (self.current_wavelength * self.L) / self.d
        self.lbl_delta_y.config(text=f"{self.T('lbl_delta_y')} {self.dy*1000:.2f} mm")
        
        self.update_simulation()
        
    def update_simulation(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10: w=600; h=500
        
        # Coordinate System
        # x-axis on screen corresponds to physical position y on screen (confusing?)
        # Let's map Canvas X to Physical Y position on screen.
        # Center x = 0 physical position.
        
        cx = w / 2
        cy_graph = h / 2 - 50 # Base line for intensity graph
        cy_screen = h - 80    # Y position for visual bands
        
        # Scale Factor: We need to see few bands.
        # Typically dy is around 1-5 mm.
        # Let's make the canvas width represent about 40 mm (4 cm).
        screen_width_mm = 40.0 
        px_per_mm = w / screen_width_mm
        
        # Draw Axis
        self.canvas.create_line(0, cy_graph, w, cy_graph, fill="white", width=1)
        self.canvas.create_line(cx, 0, cx, h, fill="gray", dash=(2,2)) # Center Line
        
        # Generate Pattern Points
        points = []
        
        # Calculate Intensity for each pixel X column
        for px in range(0, w, 2): # Step 2 px for speed
            # Convert px to physical position y (meters)
            mm_from_center = (px - cx) / px_per_mm
            y_meters = mm_from_center * 1e-3
            
            # Physics Formula: I = I0 * cos^2( (pi * d * y) / (lambda * L) )
            beta = (math.pi * self.d * y_meters) / (self.current_wavelength * self.L)
            intensity = math.cos(beta)**2
            
            # Graph Plot (Height 150px max)
            plot_y = cy_graph - (intensity * 150)
            points.append(px)
            points.append(plot_y)
            
            # Visual Band Plot (Gradient)
            # Simulate brightness by color alpha or lines
            if intensity > 0.05:
                # Tkinter doesn't support alpha well on lines easily.
                # Use hex color shading toward black? simpler to just draw lines if bright.
                # Or use stipple.
                # Let's use simple threshold lines for visual bands
                
                # Color blending black to self.current_color
                # Simple HACK: just draw line if intensity > threshold, width proportional?
                # Better: Convert hex to RGB, scale by intensity.
                
                clr = self.adjust_brightness(self.current_color, intensity)
                self.canvas.create_line(px, cy_screen - 30, px, cy_screen + 30, fill=clr, width=2)
                
        # Draw Graph Line
        if len(points) > 2:
            self.canvas.create_line(points, fill=self.current_color, width=2, smooth=True)
            
        # Labels
        self.canvas.create_text(cx, cy_graph + 20, text="0 mm", fill="white")
        
        # Mark the theoretical max positions (m=1, m=2)
        dy_mm = self.dy * 1000
        for m in [1, 2, -1, -2]:
            pos_mm = m * dy_mm
            px_pos = cx + pos_mm * px_per_mm
            self.canvas.create_line(px_pos, cy_graph, px_pos, cy_graph-160, fill="white", dash=(2,4))
            self.canvas.create_text(px_pos, cy_graph - 170, text=f"m={m}", fill="white")
            self.canvas.create_text(px_pos, cy_graph + 20, text=f"{pos_mm:.1f}mm", fill="gray")

    def adjust_brightness(self, hex_color, factor):
        # Factor 0 to 1
        r = int(int(hex_color[1:3], 16) * factor)
        g = int(int(hex_color[3:5], 16) * factor)
        b = int(int(hex_color[5:7], 16) * factor)
        return f"#{r:02x}{g:02x}{b:02x}"

    def record_data(self):
        # ("Warna", "d (mm)", "L (m)", "Δy Teori (mm)", "y_ukur (mm) [m=1]", "Error %")
        color = self.wav_var.get().split(' ')[0]
        d_val = self.d_var.get()
        L_val = self.L_var.get()
        dy_mm = self.dy * 1000
        
        # Simulate measurement noise? No, theoretical for now as it's a "Calculator/Sim"
        y_meas = dy_mm 
        
        self.tree.insert("", "end", values=(color, f"{d_val:.2f}", f"{L_val:.2f}", f"{dy_mm:.2f}", f"{y_meas:.2f}", "0.0%"))
        self.update_graph()
        messagebox.showinfo("Info", self.T("msg_rec_success"))

    def clear_data(self):
        if not messagebox.askyesno("Confirm", self.T("msg_clear_confirm")):
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.update_graph()
            
    def update_graph(self):
        # Plot L vs dy for checking linearity
        Ls = []
        dys = []
        for child in self.tree.get_children():
            vals = self.tree.item(child)["values"]
            # L is index 2, dy is index 3
            try:
                Ls.append(float(vals[2]))
                dys.append(float(vals[3]))
            except:
                pass
                
        self.ax.clear()
        self.ax.set_title(self.T("plot_title"))
        self.ax.set_ylabel(self.T("plot_y"))
        self.ax.set_xlabel(self.T("plot_x"))
        self.ax.grid(True)
        
        if Ls:
            self.ax.scatter(Ls, dys, c='blue', marker='o')
            
        self.graph_canvas.draw()

    def get_data(self):
        export_data = []
        for child in self.tree.get_children():
            vals = self.tree.item(child)["values"]
            row = {
                "Warna": vals[0],
                "d (mm)": vals[1],
                "L (m)": vals[2],
                "dy_teori (mm)": vals[3],
                "y_ukur (mm)": vals[4]
            }
            export_data.append(row)
        return export_data

    def save_data_unified(self):
        data = self.get_data()
        success, msg = DataManager.save_data_unified(data, "DifraksiCelahGanda")
        
        if success:
            messagebox.showinfo(self.T("msg_saved") if hasattr(self, "T") else "Sukses", msg)
        else:
            messagebox.showwarning(self.T("msg_warning") if hasattr(self, "T") else "Perhatian", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabDifraksiGanda(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
