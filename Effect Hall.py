import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
# import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from virtual_lab_data_manager import DataManager

class VirtualLabHall(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#f5f6fa")
        
        # --- Physics Constants ---
        self.e = 1.602e-19  # C
        
        # Materials Database
        # Rh values in m^3/C
        self.materials = {
            "Germanium n-type": {"Rh": -8.0e-3, "type": "n", "carrier": "electron"},
            "Germanium p-type": {"Rh": +6.0e-3, "type": "p", "carrier": "hole"},
            "Tembaga (Cu)":     {"Rh": -5.4e-11, "type": "metal", "carrier": "electron"},
            "Seng (Zn)":        {"Rh": +6.0e-11, "type": "metal", "carrier": "hole"} # Anomaly
        }
        
        # State Variables
        self.selected_material = "Germanium n-type"
        self.current_mA = 5.0    # for semiconductors
        self.current_A  = 2.0    # for metals
        self.B_field_mT = 100.0
        self.thickness_mm = 0.5
        
        self.is_on = False
        self.particles = []
        self.data_points = []
        
        self.lang = "ID"
        self.setup_translations()
        
        self.setup_ui()
        self.running = True
        
        # Bind resize event to redraw background
        self.canvas_sim.bind("<Configure>", lambda e: self.draw_hall_probe())
        
        self.animate_particles()

    def start_animation(self):
        if not self.running:
            self.running = True
            self.animate_particles()

    def stop_animation(self):
        self.running = False

    def setup_translations(self):
        self.translations = {
            "ID": {
                "title": "EFEK HALL (HALL EFFECT)",
                "subtitle": "Penentuan Jenis Pembawa Muatan & Konsentrasi",
                "tab_exp": "Eksperimen",
                "tab_ana": "Analisis Data",
                "tab_guide": "Petunjuk",
                "tab_scheme": "Skema Alat & Penjelasan",
                "tab_diagram": "Gambaran Rangkaian Alat",
                "lbl_material": "Pilih Bahan Sampel (Keping):",
                "lbl_current": "Arus Listrik Is:",
                "lbl_b_field": "Medan Magnet B (mT):",
                "lbl_thick": "Tebal Keping d (mm):",
                "lbl_anim": "Tampilan Mikroskopik:",
                "btn_start": "Mulai/Stop Arus",
                "btn_record": "Catat Data (I, B, Vh)",
                "btn_reset": "Reset",
                "grp_volt": "Voltmeter Hall (Vh)",
                "col_mat": "Bahan",
                "col_i": "Arus (mA)",
                "col_b": "Medan B (mT)",
                "col_vh": "Tegangan Hall (mV)",
                "btn_clear": "Hapus Data",
                "btn_calc": "Hitung Konstanta Hall (Rh)",
                "btn_save": "Simpan Data",
                "lbl_res_default": "Hasil Analisis: Belum ada data",
                "plt_title": "Kurva Vh vs B (Pada Arus Konstan)",
                "plt_x": "Medan Magnet B (mT)",
                "plt_y": "Tegangan Hall Vh (mV)",
                "diag_probe": "Hall Probe",
                "diag_curr": "SUMBER ARUS",
                "diag_volt": "VOLTMETER",
                "diag_psu": "PSU MAGNET",
                "diag_core": "Elektromagnet (Medan Variabel)",
                "diag_current": "Aliran Arus (Elektron/Lobang)",
                "col_thick": "Tebal (mm)",
                "col_vh_full": "Tegangan Hall Vh (mV)",
                "header_ctrl": "Papan Kontrol",
                "lbl_mode_semicon": "Mode: Semikonduktor (mA)",
                "lbl_mode_metal": "Mode: Logam (Amper)",
                "msg_no_data": "Tidak ada data!",
                "lbl_res_header": "Jurnal Analisis",
                "lbl_conc": "Konsentrasi (n)",
                "lbl_type": "Tipe",
                "btn_stop": "Hentikan Arus",
                "msg_rec": "Data dicatat:\nI = {I} mA\nB = {B} mT\nVh = {Vh} mV",
                "msg_min_data": "Butuh minimal 2 titik data untuk regresi!",
                "msg_res": "Analisis Regresi Linear (Vh vs B):\nSlope (m) = {slope:.4f} mV/mT\n\nHasil Perhitungan:\nKonstanta Hall (Rh) = {Rh:.2e} m³/C\nTipe Pembawa: {ctype}\nKonsentrasi (n) = {n_conc:.2e} /m³",
                "guide_content": """PETUNJUK PRAKTIKUM EFEK HALL

A. TUJUAN
1. Mengamati fenomena Efek Hall pada semikonduktor atau logam.
2. Menentukan jenis pembawa muatan (Elektron atau Hole).
3. Menghitung Konstanta Hall (Rh) dan konsentrasi pembawa muatan (n).

B. DASAR TEORI
Tegangan Hall (Vh) muncul tegak lurus terhadap arah arus (I) dan medan magnet (B).
Rumus:
Vh = (Rh * I * B) / d

Dimana:
Rh = Konstanta Hall (negatif untuk elektron, positif untuk hole)
I  = Arus listrik (Ampere)
B  = Medan Magnet (Tesla)
d  = Ketebalan keping (meter)

C. PROSEDUR
1. Pilih Jenis Bahan (misal: Germanium n-type).
2. Atur ketebalan keping (d) jika perlu.
3. Nyalakan Arus (Klik 'Mulai/Stop Arus').
4. Variasikan Medan Magnet (B) dari 0 s.d 500 mT.
5. Pada setiap nilai B, amati nilai Vh pada Voltmeter.
   - Klik "Catat Data" untuk menyimpan tabel.
   - Amati arah gerak pembawa muatan pada visualisasi.
6. Ulangi untuk variasi Arus (I) jika diinginkan.
7. Masuk tab "Analisis Data", klik "Hitung Konstanta Hall" untuk mendapatkan hasil Rh dan konsentrasi.

D. ANALISIS
Gradien grafik Vh vs B adalah: m = (Rh * I) / d
Maka: Rh = (m * d) / I
""",
                "scheme_title": "SKEMA ALAT DAN PENJELASAN",
                "scheme_content": """SKEMA ALAT DAN PENJELASAN

Peralatan Efek Hall digunakan untuk menentukan sifat listrik bahan semikonduktor atau logam.

KOMPONEN UTAMA:

1. Keping Sampel Hall (Hall Probe)
   Lempengan tipis bahan konduktor/semikonduktor (biasanya Germanium tipe-p atau n) yang memiliki 4 kontak terminal:
   - 2 Terminal Arus (Kiri-Kanan): Mengalirkan arus bias (Is).
   - 2 Terminal Tegangan (Atas-Bawah): Mengukur Tegangan Hall (Vh).

2. Elektromagnet (Kumparan Besar)
   Sepasang kumparan dengan inti besi yang menghasilkan medan magnet (B) yang kuat dan seragam di celah udara tempat sampel diletakkan. Arah B tegak lurus terhadap permukaan sampel.

3. Sumber Arus Konstan (Current Source)
   Menyuplai arus listrik (I) yang stabil melewati sampel.

4. Voltmeter Presisi (Mili/Mikrovoltmeter)
   Mengukur beda potensial transversal yang sangat kecil (Tegangan Hall) yang muncul akibat pembelokan pembawa muatan oleh gaya Lorentz. Tanda positif/negatif tegangan ini menunjukkan jenis pembawa muatan (Hole atau Elektron).

5. Teslameter (Gaussmeter)
   Alat untuk mengukur kuat medan magnet (B) yang diberikan.

PRINSIP FISIS:
Gaya Lorentz (F = qv x B) membelokkan pembawa muatan yang bergerak ke satu sisi keping, menciptakan akumulasi muatan dan medan listrik internal (Medan Hall) hingga gaya listrik menyeimbangkan gaya magnet."""
            },
            "EN": {
                "title": "HALL EFFECT",
                "subtitle": "Determination of Charge Carrier Type & Concentration",
                "tab_exp": "Experiment",
                "tab_ana": "Data Analysis",
                "tab_guide": "Guide",
                "tab_scheme": "Tool Scheme & Explanation",
                "tab_diagram": "Circuit Diagram",
                "lbl_material": "Select Sample Material:",
                "lbl_current": "Current Is:",
                "lbl_b_field": "Magnetic Field B (mT):",
                "lbl_thick": "Thickness d (mm):",
                "lbl_anim": "Microscopic View:",
                "btn_start": "Start/Stop Current",
                "btn_record": "Record Data (I, B, Vh)",
                "btn_reset": "Reset",
                "grp_volt": "Hall Voltmeter (Vh)",
                "col_mat": "Material",
                "col_i": "Current (mA)",
                "col_b": "B-Field (mT)",
                "col_vh": "Hall Voltage (mV)",
                "btn_clear": "Clear Data",
                "btn_calc": "Calculate Hall Constant (Rh)",
                "btn_save": "Save Data",
                "lbl_res_default": "Analysis Result: No data yet",
                "plt_title": "Vh vs B Curve (Constant Current)",
                "plt_x": "Magnetic Field B (mT)",
                "plt_y": "Hall Voltage Vh (mV)",
                "diag_probe": "Hall Probe",
                "diag_curr": "CURRENT SOURCE",
                "diag_volt": "VOLTMETER",
                "diag_psu": "MAGNET PSU",
                "diag_core": "Electromagnet (Variable Field)",
                "diag_current": "Current Flow (Electron/Hole)",
                "col_thick": "Thickness (mm)",
                "col_vh_full": "Hall Voltage Vh (mV)",
                "header_ctrl": "Control Board",
                "lbl_mode_semicon": "Mode: Semiconductor (mA)",
                "lbl_mode_metal": "Mode: Metal (Ampere)",
                "msg_no_data": "No data!",
                "lbl_res_header": "Analysis Journal",
                "lbl_conc": "Concentration (n)",
                "lbl_type": "Type",
                "btn_stop": "Stop Current",
                "msg_rec": "Data recorded:\nI = {I} mA\nB = {B} mT\nVh = {Vh} mV",
                "msg_min_data": "Need at least 2 data points for regression!",
                "msg_res": "Linear Regression Analysis (Vh vs B):\nSlope (m) = {slope:.4f} mV/mT\n\nCalculation Results:\nHall Constant (Rh) = {Rh:.2e} m³/C\nCarrier Type: {ctype}\nConcentration (n) = {n_conc:.2e} /m³",
                "guide_content": """HALL EFFECT PRACTICAL GUIDE

A. OBJECTIVE
1. Observe Hall Effect phenomenon in semiconductor or metal.
2. Determine charge carrier type (Electron or Hole).
3. Calculate Hall Constant (Rh) and carrier concentration (n).

B. THEORY
Hall Voltage (Vh) appears perpendicular to current direction (I) and magnetic field (B).
Formula:
Vh = (Rh * I * B) / d

Where:
Rh = Hall Constant (negative for electrons, positive for holes)
I  = Electric Current (Ampere)
B  = Magnetic Field (Tesla)
d  = Plate Thickness (meter)

C. PROCEDURE
1. Select Material Type (e.g., Germanium n-type).
2. Set plate thickness (d) if needed.
3. Turn ON Current (Click 'Start/Stop Current').
4. Vary Magnetic Field (B) from 0 to 500 mT.
5. At each B value, observe Vh on Voltmeter.
   - Click "Record Data" to save the table.
   - Observe charge carrier motion in visualization.
6. Repeat for Current (I) variations if desired.
7. Go to "Data Analysis" tab, click "Calculate Hall Constant" to get Rh and concentration.

D. ANALYSIS
Gradient of Vh vs B graph is: m = (Rh * I) / d
So: Rh = (m * d) / I
""",
                "scheme_title": "TOOL SCHEME AND EXPLANATION",
                "scheme_content": """TOOL SCHEME AND EXPLANATION

Hall Effect equipment is used to determine electrical properties of semiconductor or metal materials.

MAIN COMPONENTS:

1. Hall Probe (Sample Plate)
   Thin plate of conductor/semiconductor (usually Germanium p-type or n-type) having 4 contacts:
   - 2 Current Terminals (Left-Right): Flow bias current (Is).
   - 2 Voltage Terminals (Top-Bottom): Measure Hall Voltage (Vh).

2. Electromagnet (Large Coil)
   Pair of coils with iron core producing strong uniform magnetic field (B) in the air gap where sample is placed. B direction is perpendicular to sample surface.

3. Constant Current Source
   Supplies stable electric current (I) passing through the sample.

4. Precision Voltmeter (Milli/Microvoltmeter)
   Measures very small transverse potential difference (Hall Voltage) arising from charge carrier deflection by Lorentz force. Positive/negative sign indicates carrier type (Hole or Electron).

5. Teslameter (Gaussmeter)
   Tool to measure applied magnetic field strength (B).

PHYSICAL PRINCIPLE:
Lorentz Force (F = qv x B) deflects moving charge carriers to one side of the plate, creating charge accumulation and internal electric field (Hall Field) until electric force balances magnetic force."""
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
        self.notebook.tab(0, text=self.T("tab_exp"))
        self.notebook.tab(1, text=self.T("tab_ana"))
        self.notebook.tab(2, text=self.T("tab_guide"))
        self.notebook.tab(3, text=self.T("tab_scheme"))
        self.notebook.tab(4, text=self.T("tab_diagram"))
        
        # Experiments
        self.lbl_mat.config(text=self.T("lbl_material"))
        self.lbl_cur.config(text=self.T("lbl_current"))
        self.lbl_mag.config(text=self.T("lbl_b_field"))
        self.btn_power.config(text=self.T("btn_start"))
        self.btn_record.config(text=self.T("btn_record"))
        self.lbl_volt_title.config(text=self.T("grp_volt"))
        
        # Analysis
        self.btn_clear.config(text=self.T("btn_clear"))
        self.btn_calc.config(text=self.T("btn_calc"))
        self.btn_save.config(text=self.T("btn_save"))
        
        cols = (self.T("col_mat"), self.T("col_i"), self.T("col_b"), self.T("col_vh"))
        self.tree.heading("mat", text=self.T("col_mat"))
        self.tree.heading("thick", text=self.T("col_thick"))
        self.tree.heading("i", text=self.T("col_i"))
        self.tree.heading("b", text=self.T("col_b"))
        self.tree.heading("vh", text=self.T("col_vh"))
            
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

        # Diagram
        # Need to re-create or itemconfig tags. The diagram is static Canvas.
        # I'll enable itemconfig by adding tags in create_diagram_tab
        self.canvas_diag.itemconfigure("diag_probe", text=self.T("diag_probe"))
        self.canvas_diag.itemconfigure("diag_curr", text=self.T("diag_curr"))
        self.canvas_diag.itemconfigure("diag_volt", text=self.T("diag_volt"))
        self.canvas_diag.itemconfigure("diag_psu", text=self.T("diag_psu"))
        self.canvas_diag.itemconfigure("diag_core", text=self.T("diag_core"))

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg="#2c3e50", pady=15)
        header.pack(fill="x")
        self.lbl_title = tk.Label(header, text=self.T("title"), font=("Helvetica", 20, "bold"), fg="white", bg="#2c3e50")
        self.lbl_title.pack()
        self.lbl_subtitle = tk.Label(header, text=self.T("subtitle"), font=("Helvetica", 12), fg="#bdc3c7", bg="#2c3e50")
        self.lbl_subtitle.pack()
        
        # Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_exp = tk.Frame(self.notebook, bg="#f5f6fa")
        self.tab_ana = tk.Frame(self.notebook, bg="#f5f6fa")
        self.tab_guide = tk.Frame(self.notebook, bg="#f5f6fa")
        
        self.notebook.add(self.tab_exp, text=self.T("tab_exp"))
        self.notebook.add(self.tab_ana, text=self.T("tab_ana"))
        self.notebook.add(self.tab_guide, text=self.T("tab_guide"))
        
        self.tab_scheme = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_scheme, text=self.T("tab_scheme"))

        self.tab_diagram = tk.Frame(self.notebook, bg="#f5f6fa") # New Tab
        self.notebook.add(self.tab_diagram, text=self.T("tab_diagram"))

        self.create_experiment_tab()
        self.create_analysis_tab()
        self.create_guide_tab()
        self.create_scheme_tab()
        self.create_diagram_tab() # New Function

    def create_diagram_tab(self):
        self.canvas_diag = tk.Canvas(self.tab_diagram, bg="#fdfefe")
        self.canvas_diag.pack(fill="both", expand=True, padx=20, pady=20)
        canvas = self.canvas_diag
        
        # Helper function for 3D box effect
        def draw_3d_box(x1, y1, w, h, depth, color, label="", tag=""):
            canvas.create_rectangle(x1, y1, x1+w, y1+h, fill=color, outline="#2c3e50", width=2)
            canvas.create_polygon(x1, y1, x1+w, y1, x1+w+depth, y1-depth, x1+depth, y1-depth, 
                                fill=color, outline="#2c3e50", width=1, stipple="gray50")
            canvas.create_polygon(x1+w, y1, x1+w+depth, y1-depth, x1+w+depth, y1+h-depth, x1+w, y1+h, 
                                fill=color, outline="#2c3e50", width=1, stipple="gray25")
            if label:
                canvas.create_text(x1+w/2, y1+20, text=label, font=("Arial", 10, "bold"), fill="white", tag=tag)
        
        canvas.create_rectangle(0, 420, 800, 500, fill="#bdc3c7", outline="")
        
        # Electromagnet C-Core (3D)
        canvas.create_rectangle(240, 100, 280, 400, fill="#34495e", outline="#2c3e50", width=2)
        canvas.create_polygon(240, 100, 280, 100, 560, 100, 520, 100, fill="#34495e", outline="#2c3e50", width=2)
        canvas.create_polygon(280, 100, 560, 100, 560, 140, 280, 140, fill="#2c3e50", outline="#2c3e50", width=2)
        canvas.create_polygon(240, 360, 280, 360, 560, 360, 520, 360, fill="#34495e", outline="#2c3e50", width=2)
        canvas.create_polygon(280, 360, 560, 360, 560, 400, 280, 400, fill="#2c3e50", outline="#2c3e50", width=2)
        canvas.create_rectangle(520, 100, 560, 400, fill="#34495e", outline="#2c3e50", width=2)
        
        for i in range(5):
            shade = 40 + i*8
            color = f"#{shade:02x}{shade:02x}{shade:02x}"
            canvas.create_rectangle(370+i*2, 140+i*2, 430-i*2, 200-i*2, fill=color, outline="")
        canvas.create_text(400, 170, text="N", fill="#e74c3c", font=("Arial", 18, "bold"))
        
        for i in range(5):
            shade = 40 + i*8
            color = f"#{shade:02x}{shade:02x}{shade:02x}"
            canvas.create_rectangle(370+i*2, 300+i*2, 430-i*2, 360-i*2, fill=color, outline="")
        canvas.create_text(400, 330, text="S", fill="#3498db", font=("Arial", 18, "bold"))
        
        # Hall Probe Assembly
        canvas.create_rectangle(350, 235, 450, 265, fill="#27ae60", outline="#1e8449", width=2)
        for x in [360, 390, 410, 440]:
            canvas.create_rectangle(x-3, 240, x+3, 260, fill="#f39c12", outline="#d68910")
        canvas.create_rectangle(390, 242, 410, 258, fill="#2c3e50", outline="black")
        canvas.create_oval(397, 249, 403, 255, fill="white", outline="")
        
        canvas.create_rectangle(395, 265, 405, 420, fill="#7f8c8d", outline="#5d6d7e", width=2)
        canvas.create_rectangle(380, 410, 420, 425, fill="#95a5a6", outline="#5d6d7e", width=2)
        canvas.create_text(400, 285, text=self.T("diag_probe"), font=("Arial", 9), fill="#2c3e50", tag="diag_probe")
        
        draw_3d_box(50, 280, 150, 80, 15, "#e67e22", self.T("diag_curr"), "diag_curr")
        canvas.create_rectangle(65, 300, 185, 330, fill="#1a1a1a", outline="")
        canvas.create_text(125, 315, text="5.000 mA", font=("Courier", 16, "bold"), fill="#2ecc71")
        canvas.create_oval(70, 340, 90, 360, fill="#95a5a6", outline="#7f8c8d", width=2)
        canvas.create_line(80, 350, 88, 342, fill="white", width=2)
        for i, col in enumerate(["#e74c3c", "#2ecc71"]):
            canvas.create_oval(110+i*30, 345, 118+i*30, 353, fill=col, outline="")
        
        draw_3d_box(600, 280, 150, 80, 15, "#9b59b6", self.T("diag_volt"), "diag_volt")
        canvas.create_rectangle(615, 300, 735, 330, fill="#1a1a1a", outline="")
        canvas.create_text(675, 315, text="12.34 mV", font=("Courier", 16, "bold"), fill="#3498db")
        canvas.create_rectangle(625, 340, 655, 355, fill="#34495e", outline="#2c3e50")
        canvas.create_text(640, 347, text="mV", font=("Arial", 8, "bold"), fill="white")
        
        draw_3d_box(50, 380, 150, 60, 12, "#34495e", self.T("diag_psu"), "diag_psu")
        canvas.create_rectangle(65, 405, 185, 425, fill="#1a1a1a", outline="")
        canvas.create_text(125, 415, text="2.500 A", font=("Courier", 14, "bold"), fill="#f39c12")
        
        canvas.create_line(200, 320, 220, 320, 220, 250, 350, 250, width=3, fill="#e74c3c", smooth=True)
        canvas.create_line(200, 340, 210, 340, 210, 260, 450, 250, width=3, fill="#2c3e50", smooth=True)
        canvas.create_line(400, 235, 400, 220, 580, 220, 600, 300, width=2, fill="#3498db", smooth=True)
        canvas.create_line(400, 265, 420, 280, 580, 280, 600, 320, width=2, fill="#3498db", smooth=True)
        canvas.create_line(200, 400, 230, 400, 230, 380, 240, 350, width=3, fill="#e74c3c", smooth=True)
        canvas.create_line(200, 420, 240, 420, 240, 400, width=3, fill="#2c3e50", smooth=True)
        
        canvas.create_text(400, 80, text=self.T("diag_core"), font=("Arial", 12, "bold"), fill="#2c3e50", tag="diag_core")
        canvas.create_line(400, 90, 400, 100, arrow="last", fill="#2c3e50", width=2)


    def create_scheme_tab(self):
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


    def create_experiment_tab(self):
        # Full Layout: Top (Sim) & Bottom (Controls)
        main_layout = tk.Frame(self.tab_exp, bg="#f5f6fa")
        main_layout.pack(fill="both", expand=True, padx=10, pady=10)
        
        # --- Top: Visualization ---
        top_frame = tk.Frame(main_layout, bg="#34495e")
        top_frame.pack(side="top", fill="both", expand=True, pady=(0, 10))
        
        # Split Top: Left (Canvas) and Right (Voltmeter)
        
        # Left: Probe Visualization
        self.lf_anim = tk.LabelFrame(top_frame, text=self.T("lbl_anim"), bg="#34495e", fg="white")
        self.lf_anim.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        self.canvas_sim = tk.Canvas(self.lf_anim, bg="#34495e", height=300)
        self.canvas_sim.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Right: Multimeter Display
        self.lf_mult = tk.Frame(top_frame, bg="#2c3e50", width=300, relief="sunken", bd=2)
        self.lf_mult.pack(side="right", fill="y", padx=10, pady=10)
        self.lf_mult.pack_propagate(False)
        
        self.lbl_volt_title = tk.Label(self.lf_mult, text=self.T("grp_volt"), font=("Courier", 14, "bold"), fg="#f1c40f", bg="#2c3e50")
        self.lbl_volt_title.pack(pady=20)
        self.lbl_voltage = tk.Label(self.lf_mult, text="+0.000 mV", font=("Ds-Digital", 36), fg="#e74c3c", bg="black", width=10)
        self.lbl_voltage.pack(pady=20)
        self.lbl_vh_sub = tk.Label(self.lf_mult, text=self.T("col_vh_full"), font=("Arial", 12), fg="white", bg="#2c3e50")
        self.lbl_vh_sub.pack()

        # --- Bottom: Controls ---
        bot_frame = tk.Frame(main_layout, bg="white", relief="raised", bd=1, height=200)
        bot_frame.pack(side="bottom", fill="x", padx=5, pady=5)
        
        self.lbl_ctrl_title = tk.Label(bot_frame, text=self.T("header_ctrl"), font=("Arial", 12, "bold"), bg="white")
        self.lbl_ctrl_title.pack(side="top", pady=5)
        
        # Columns for controls
        c_grid = tk.Frame(bot_frame, bg="white")
        c_grid.pack(fill="x", padx=10, pady=5)
        
        # Col 1: Material & Thickness
        c1 = tk.Frame(c_grid, bg="white")
        c1.pack(side="left", fill="y", padx=10)
        
        self.lbl_mat = tk.Label(c1, text=self.T("lbl_material"), bg="white", anchor="w")
        self.lbl_mat.pack(fill="x")
        self.mat_var = tk.StringVar(value=self.selected_material)
        mat_cb = ttk.Combobox(c1, values=list(self.materials.keys()), textvariable=self.mat_var, state="readonly", width=25)
        mat_cb.pack(fill="x", pady=2)
        mat_cb.bind("<<ComboboxSelected>>", self.on_material_change)
        
        self.lbl_thick = tk.Label(c1, text=self.T("lbl_thick"), bg="white", anchor="w")
        self.lbl_thick.pack(fill="x", pady=(5,0))
        self.thick_var = tk.DoubleVar(value=0.5)
        tk.Scale(c1, from_=0.1, to=2.0, resolution=0.1, orient="horizontal", 
                 variable=self.thick_var, bg="white").pack(fill="x")
                 
        # Col 2: Current & Field
        c2 = tk.Frame(c_grid, bg="white", bd=1, relief="solid")
        c2.pack(side="left", fill="both", expand=True, padx=20)
        
        self.lbl_cur = tk.Label(c2, text=self.T("lbl_current"), bg="#ecf0f1", anchor="w")
        self.lbl_cur.pack(fill="x")
        self.current_scale = tk.Scale(c2, from_=0.0, to=20.0, resolution=0.1, orient="horizontal", 
                                      bg="white", label="Is (mA)", command=self.update_readings)
        self.current_scale.set(5.0)
        self.current_scale.pack(fill="x", padx=5)
        self.lbl_current_mode = tk.Label(c2, text=self.T("lbl_mode_semicon"), font=("Arial", 8), fg="gray", bg="white")
        self.lbl_current_mode.pack(anchor="w", padx=5)
        
        self.lbl_mag = tk.Label(c2, text=self.T("lbl_b_field"), bg="#ecf0f1", anchor="w")
        self.lbl_mag.pack(fill="x")
        self.mag_scale = tk.Scale(c2, from_=-500, to=500, resolution=10, orient="horizontal", 
                                  bg="white", label="B (mT)", command=self.update_readings)
        self.mag_scale.set(100)
        self.mag_scale.pack(fill="x", padx=5)

        # Col 3: Actions
        c3 = tk.Frame(c_grid, bg="white")
        c3.pack(side="left", fill="y", padx=10)
        
        self.btn_power = tk.Button(c3, text=self.T("btn_start"), bg="#e74c3c", fg="black", highlightbackground="#e74c3c", font=("Arial", 11, "bold"),
                                   command=self.toggle_power, width=15)
        self.btn_power.pack(pady=10)
        
        self.btn_record = tk.Button(c3, text=self.T("btn_record"), bg="#2980b9", fg="black", highlightbackground="#2980b9", font=("Arial", 11, "bold"),
                  command=self.record_data, width=15)
        self.btn_record.pack(pady=5)

    def create_analysis_tab(self):
        # Use PanedWindow for adjustable split
        pw = tk.PanedWindow(self.tab_ana, orient=tk.HORIZONTAL, sashwidth=4, bg="#dcdde1")
        pw.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left: Data Table & Buttons
        left_frame = tk.Frame(pw, bg="white")
        pw.add(left_frame, minsize=480)
        
        # DataFrame controls
        ctrl_frame = tk.Frame(left_frame, bg="white")
        ctrl_frame.pack(fill="x", padx=5, pady=10)
        
        # Changed fg to black for macOS readability, added highlightbackground
        btn_base = {"font": ("Arial", 10, "bold"), "fg": "black", "padx": 10, "pady": 2}
        
        self.btn_clear = tk.Button(ctrl_frame, text=self.T("btn_clear"), bg="#c0392b", highlightbackground="#c0392b",
                  command=self.clear_data, **btn_base)
        self.btn_clear.pack(side="left", padx=5)
        self.btn_save = tk.Button(ctrl_frame, text=self.T("btn_save"), bg="#3498db", highlightbackground="#3498db",
                  command=self.save_data_unified, **btn_base)
        self.btn_save.pack(side="left", padx=5)
        self.btn_calc = tk.Button(ctrl_frame, text=self.T("btn_calc"), bg="#27ae60", highlightbackground="#27ae60", 
                  command=self.calculate_rh, **btn_base)
        self.btn_calc.pack(side="left", padx=5)
                  
        # Table Container (for Scrollbars)
        table_frame = tk.Frame(left_frame, bg="white")
        table_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        
        # Configure Grid for Scrollbars
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Style for Treeview
        style = ttk.Style()
        style.configure("Hall.Treeview", font=("Arial", 11), rowheight=28)
        style.configure("Hall.Treeview.Heading", font=("Arial", 11, "bold"))

        cols = ("mat", "thick", "i", "b", "vh")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", style="Hall.Treeview", selectmode="extended")
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        
        self.tree.configure(yscroll=v_scroll.set, xscroll=h_scroll.set)
        
        # Layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        
        # Configure columns
        self.tree.heading("mat", text=self.T("col_mat"))
        self.tree.heading("thick", text=self.T("col_thick"))
        self.tree.heading("i", text=self.T("col_i"))
        self.tree.heading("b", text=self.T("col_b"))
        self.tree.heading("vh", text=self.T("col_vh"))

        for c in cols:
            self.tree.column(c, width=100, anchor="center")
        self.tree.column("mat", width=140, anchor="w")
        
        # Result Text with clearer font
        self.lbl_res = tk.Label(left_frame, text=self.T("lbl_res_default"), font=("Arial", 11, "bold"), bg="white", anchor="w")
        self.lbl_res.pack(fill="x", padx=5)
        self.result_text = tk.Text(left_frame, height=6, font=("Consolas", 11), bg="#f1f2f6", relief="solid", bd=1)
        self.result_text.pack(side="bottom", fill="x", padx=5, pady=10)
        
        # Right: Graph
        right_frame = tk.Frame(pw, bg="white", bd=1, relief="solid")
        pw.add(right_frame, minsize=400)
        
        self.fig, self.ax = plt.subplots(figsize=(5, 3), dpi=100)
        self.ax.set_title(self.T("plt_title"))
        self.ax.set_ylabel(self.T("plt_y"))
        self.ax.set_xlabel(self.T("plt_x"))
        self.ax.grid(True, linestyle="--", alpha=0.6)
        
        self.graph_canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        self.toolbar = NavigationToolbar2Tk(self.graph_canvas, right_frame)
        self.toolbar.update()
        self.graph_canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_guide_tab(self):
        self.txt_guide = tk.Text(self.tab_guide, font=("Arial", 12), padx=20, pady=20)
        self.txt_guide.pack(fill="both", expand=True)
        self.txt_guide.insert("1.0", self.T("txt_guide"))
        self.txt_guide.config(state="disabled")

    def on_material_change(self, event):
        mat = self.materials[self.mat_var.get()]
        if mat["type"] == "metal":
            self.current_scale.config(label="Is (Ampere)", from_=0.0, to=10.0)
            self.lbl_current_mode.config(text=self.T("lbl_mode_metal"))
        else:
            self.current_scale.config(label="Is (mA)", from_=0.0, to=20.0)
            self.lbl_current_mode.config(text=self.T("lbl_mode_semicon"))
        self.update_readings()

    def toggle_power(self):
        self.is_on = not self.is_on
        if self.is_on:
            self.btn_power.config(text=self.T("btn_stop"), bg="#27ae60", highlightbackground="#27ae60")
        else:
            self.btn_power.config(text=self.T("btn_start"), bg="#e74c3c", highlightbackground="#e74c3c")
            self.lbl_voltage.config(text="+0.000 mV")
        self.update_readings()
        
    def update_readings(self, event=None):
        self.draw_hall_probe() # Update background/indicators when sliders change
        if not self.is_on:
            return
            
        mat_name = self.mat_var.get()
        mat_data = self.materials[mat_name]
        
        # Get Inputs
        # Current
        val_i = self.current_scale.get()
        if mat_data["type"] == "metal":
            I_real = val_i # Ampere
            curr_str = f"{val_i} A"
        else:
            I_real = val_i * 1e-3 # mA to A
            curr_str = f"{val_i} mA"
            
        # B Field
        B_mT = self.mag_scale.get()
        B_real = B_mT * 1e-3 # Tesla
        
        # Thickness
        t_mm = self.thick_var.get()
        t_real = t_mm * 1e-3 # meter
        
        # Calculate Vh
        Rh = mat_data["Rh"]
        
        # Ideal Vh
        Vh_volts = (Rh * I_real * B_real) / t_real
        
        # Add slight noise (1-2%)
        noise_factor = random.uniform(0.99, 1.01)
        Vh_read = Vh_volts * noise_factor
        
        # Update UI
        mV_display = Vh_read * 1000
        self.lbl_voltage.config(text=f"{mV_display:+.3f} mV")
        
        # Update Visuals params
        self.current_sim_speed = (val_i / 20.0) * 5 if val_i > 0 else 0
        self.mag_sim_strength = B_mT
        
        self.curr_I_disp = curr_str

    def record_data(self):
        if not self.is_on: return
        
        mat = self.mat_var.get()
        thick = self.thick_var.get()
        
        val_i = self.current_scale.get()
        if self.materials[mat]["type"] != "metal":
            i_str = f"{val_i} mA"
            i_val_A = val_i * 1e-3
        else:
            i_str = f"{val_i} A"
            i_val_A = val_i
            
        b_mT = self.mag_scale.get()
        vh_mv_str = self.lbl_voltage.cget("text").replace(" mV", "")
        vh_val_V = float(vh_mv_str) * 1e-3
        
        self.tree.insert("", "end", values=(mat, thick, i_str, b_mT, vh_mv_str))
        
        # Store for calc: (Rh_theory, t_m, I_A, B_T, Vh_V)
        self.data_points.append({
            "mat": mat,
            "t": thick * 1e-3,
            "I": i_val_A,
            "B": b_mT * 1e-3,
            "Vh": vh_val_V
        })
        self.update_graph()

    def calculate_rh(self):
        if not self.data_points:
            messagebox.showwarning(self.T("msg_no_data"), self.T("msg_no_data"))
            return
            
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, f"{self.T('lbl_res_header')}\n================\n")
        
        # Group by material
        grouped = {}
        for p in self.data_points:
            m = p['mat']
            if m not in grouped: grouped[m] = []
            grouped[m].append(p)
            
        for mat, points in grouped.items():
            # Rh = (Vh * t) / (I * B)
            total_Rh = 0
            count = 0
            
            for p in points:
                if abs(p['I'] * p['B']) > 1e-10: # Avoid div by zero
                    rh_calc = (p['Vh'] * p['t']) / (p['I'] * p['B'])
                    total_Rh += rh_calc
                    count += 1
            
            if count > 0:
                avg_Rh = total_Rh / count
                real_Rh = self.materials[mat]['Rh']
                err = abs(avg_Rh - real_Rh)/abs(real_Rh) * 100
                
                # Carrier Density n = 1 / (Rh * e) (approx magnitude)
                n_calc = 1.0 / (avg_Rh * self.e)
                
                res_str = f"{self.T('col_mat')}: {mat}\n"
                res_str += f"  > Rh HS : {avg_Rh:.4e} m^3/C\n"
                res_str += f"  > Rh Th : {real_Rh:.4e} m^3/C\n"
                res_str += f"  > Error : {err:.2f} %\n"
                res_str += f"  > {self.T('lbl_conc')} : {abs(n_calc):.2e} m^-3\n"
                res_str += f"  > {self.T('lbl_type')}: {'p-type' if avg_Rh > 0 else 'n-type'}\n\n"
                
                self.result_text.insert(tk.END, res_str)

    def clear_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.data_points = []
        self.result_text.delete("1.0", tk.END)
        self.update_graph()

    def animate_particles(self):
        # Optimization: Don't redraw background every frame
        # self.draw_hall_probe() 
        self.canvas_sim.delete("anim")
        
        if self.is_on:
            w = self.canvas_sim.winfo_width()
            h = self.canvas_sim.winfo_height()
            if w < 100: w = 400
            
            cx, cy = w/2, h/2
            slab_w, slab_h = 300, 150
            start_x = cx - slab_w/2
            end_x = cx + slab_w/2
            
            mat_data = self.materials[self.mat_var.get()]
            charge_type = mat_data["carrier"] 
            
            # Optimization: Limit max particles
            if len(self.particles) < 20:
                p_y = random.uniform(cy - slab_h/2 + 10, cy + slab_h/2 - 10)
                # Reuse lists instead of objects if possible, but simplified here
                self.particles.append([start_x, p_y]) 
                
            speed = 5 
            deflection_strength = self.mag_scale.get() / 500.0 * 3.0 
            
            dy = deflection_strength
            
            surviving_particles = []
            col = "#e74c3c" if charge_type == "hole" else "#3498db"
            
            # Optimization: Batch creation? (Tkinter doesn't support batch create well, but we can minimize logic)
            # Actually, using move() is better than delete/create for existing particles
            # But since we deleted "anim", we must recreate.
            # To optimize further, we should keep IDs.
            
            # Let's switch to ID-based movement for "Smart Calculation/Rendering"
            # However, since we deleted "anim", let's stick to recreation for now but ensure background isn't redrawn.
            
            for p in self.particles:
                p[0] += speed 
                p[1] -= dy 
                
                # Manual clipping to slab area
                if (cy - slab_h/2) < p[1] < (cy + slab_h/2):
                     self.canvas_sim.create_oval(p[0]-3, p[1]-3, p[0]+3, p[1]+3, fill=col, outline=col, tags="anim")
                
                if p[0] < end_x and (cy - slab_h/2) < p[1] < (cy + slab_h/2):
                    surviving_particles.append(p)
            
            self.particles = surviving_particles

        if self.running:
            self.after(50, self.animate_particles)

    def draw_hall_probe(self):
        # This draws the static background + B field indicators
        self.canvas_sim.delete("all")
        # self.canvas_sim.delete("anim") # "all" deletes "anim" too
        
        w = self.canvas_sim.winfo_width()
        h = self.canvas_sim.winfo_height()

        if w<100: w=400
        cx, cy = w/2, h/2
        
        # Slab
        sw, sh = 300, 150
        self.canvas_sim.create_rectangle(cx-sw/2, cy-sh/2, cx+sw/2, cy+sh/2, fill="#95a5a6", outline="white", width=2, tags="hall_diags")
        
        # Connections (Current)
        self.canvas_sim.create_line(0, cy, cx-sw/2, cy, fill="#e67e22", width=4, arrow="last", tags="hall_diags") 
        self.canvas_sim.create_line(cx+sw/2, cy, w, cy, fill="#e67e22", width=4, arrow="last", tags="hall_diags") 
        
        # Voltmeter Leads
        self.canvas_sim.create_line(cx, cy-sh/2, cx, cy-sh/2 - 40, fill="#f1c40f", width=2, tags="hall_diags")
        self.canvas_sim.create_line(cx, cy+sh/2, cx, cy+sh/2 + 40, fill="#f1c40f", width=2, tags="hall_diags")
        self.canvas_sim.create_oval(cx-5, cy-sh/2-5, cx+5, cy-sh/2+5, fill="red", tags="hall_diags") 
        self.canvas_sim.create_oval(cx-5, cy+sh/2-5, cx+5, cy+sh/2+5, fill="black", tags="hall_diags") 
        
        # B Field Indicators
        b_val = self.mag_scale.get()
        symbol = "X" if b_val >= 0 else "." 
        
        for i in range(-1, 2):
            for j in range(-1, 2):
                bx = cx + i*80
                by = cy + j*40
                self.canvas_sim.create_oval(bx-10, by-10, bx+10, by+10, outline="#2ecc71", tags="hall_diags")
                self.canvas_sim.create_text(bx, by, text=symbol, fill="#2ecc71", font=("Arial", 12, "bold"), tags="hall_diags")
                
        # Labels
        self.canvas_sim.create_text(cx, cy-sh/2-50, text="V+", fill="#f1c40f", tags="hall_diags")
        self.canvas_sim.create_text(cx, cy+sh/2+50, text="V-", fill="#f1c40f", tags="hall_diags")
        self.canvas_sim.create_text(30, cy-20, text=self.T("diag_current"), fill="#e67e22", anchor="w", tags="diag_current")

    def update_graph(self):
        # We want to plot Vh (mV) vs B (mT) 
        Bs = []
        Vhs = []
        
        for d in self.data_points:
            Bs.append(d['B'] * 1000) # mT
            Vhs.append(d['Vh'] * 1000) # mV
            
        self.ax.clear()
        self.ax.set_title(self.T("plt_title"))
        self.ax.set_ylabel(self.T("plt_y"))
        self.ax.set_xlabel(self.T("plt_x"))
        self.ax.grid(True)
        
        if Bs:
            self.ax.scatter(Bs, Vhs, c='green', marker='o')
            
        self.graph_canvas.draw()

    def get_data(self):
        export_data = []
        for child in self.tree.get_children():
            vals = self.tree.item(child)["values"]
            row = {
                "Material": vals[0],
                "Tebal (mm)": vals[1],
                "Arus": vals[2],
                "Medan B (mT)": vals[3],
                "Vh (mV)": vals[4]
            }
            export_data.append(row)
        return export_data

    def save_data_unified(self):
        data = self.get_data()
        success, msg = DataManager.save_data_unified(data, "EffectHall")
        
        if success:
            messagebox.showinfo("Sukses", msg)
        else:
            messagebox.showwarning("Perhatian", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabHall(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
