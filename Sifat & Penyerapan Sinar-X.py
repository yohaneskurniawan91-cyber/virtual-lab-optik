import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from virtual_lab_data_manager import DataManager

class VirtualLabSinarX(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#f5f6fa")
        
        self.setup_translations()
        self.lang = "ID"
        
        # --- Physics Models ---
        self.I0_base = 10000.0 # Base Intensity at max settings
        
        # Material Properties (mu estimate at ~50 keV)
        self.materials = {
            "Udara (Tanpa Absorber)": {"mu": 0.0, "color": ""},
            "Aluminium (Al)": {"mu": 1.0,  "color": "#bdc3c7"},
            "Tembaga (Cu)":   {"mu": 15.0, "color": "#d35400"},
            "Timbal (Pb)":    {"mu": 60.0, "color": "#2c3e50"}
        }
        
        self.is_on = False
        self.thickness_mm = 0.0
        self.voltage_kV = 30.0 # Default
        self.current_mu = 0.0
        
        self.data_points = [] # For analysis
        
        self.running = True
        self.create_widgets()
        
        self.set_language("ID")

    def start_animation(self):
        if not self.running:
            self.running = True
            if self.is_on:
                self.update_simulation_loop()

    def stop_animation(self):
        self.running = False

    def setup_translations(self):
        self.translations = {
            "ID": {
                "title": "Sifat & Penyerapan Sinar-X (Hukum Beer-Lambert)",
                "tab_exp": "Eksperimen Penyerapan",
                "tab_ana": "Analisis Data",
                "tab_guide": "Petunjuk Praktikum",
                "tab_scheme": "Skema Alat & Penjelasan",
                "tab_diagram": "Gambaran Rangkaian Alat",
                "lbl_volt": "Tegangan (kV):",
                "lbl_absorber": "Absorber:",
                "lbl_thick": "Tebal (mm):",
                "lbl_gm": "Output Pencacah GM",
                "btn_record": "Catat Data",
                "btn_calc": "Hitung Mu (μ)",
                "btn_clear": "Hapus Semua",
                "btn_save": "Simpan Data",
                "col_mat": "Bahan",
                "col_th": "Tebal (mm)",
                "col_v": "Tegangan (kV)",
                "col_i": "I_ukur (CPS)",
                "col_log": "Log(I0/I)",
                "msg_reg_err": "Min 2 data utk regresi.",
                "msg_warn_power": "Nyalakan Power terlebih dahulu!",
                "msg_reg_res": "Hasil Regresi untuk {mat}:\nμ = {mu:.3f} cm^-1\nI0 (interpolasi) = {i0:.0f} CPS",
                "plot_title": "Hukum Beer-Lambert (Log I0/I vs Tebal)",
                "plot_y": "Log(I0 / I)",
                "plot_x": "Tebal Absorber (mm)",
                "scheme_title": "Skema Alat Penyerapan Sinar-X",
                "scheme_content": """SKEMA ALAT DAN PENJELASAN

Eksperimen ini menggunakan unit pembangkit sinar-X terlindungi untuk mempelajari atenuasi (pelemahan) radiasi saat melewati materi.

KOMPONEN UTAMA:

1. Tabung Sinar-X (X-Ray Tube)
   Tabung vakum di mana elektron dipercepat oleh tegangan tinggi (20-50 kV) menumbuk target logam (Anoda Tungsten/Molybdenum). Tumbukan ini menghasilkan sinar-X karakteristik dan Bremsstrahlung.

2. Kolimator
   Celah logam tebal (timbal) untuk membatasi berkas sinar-X menjadi satu garis lurus terarah menuju detektor, mencegah hamburan kesegala arah.

3. Slot Absorber (Tempat Sampel)
   Dudukan untuk meletakkan pelat bahan penyerap (Absorber) seperti Aluminium, Tembaga, atau Timbal dengan ketebalan yang bervariasi.

4. Detektor Geiger-Muller (GM Tube)
   Sensor berisi gas mulia yang akan terionisasi saat terkena foton sinar-X, menghasilkan pulsa listrik.

5. Ratemeter / Counter
   Menghitung jumlah pulsa dari detektor GM per satuan waktu (Counts per Second / CPS), yang merepresentasikan INTENSITAS sinar-X yang lolos.

TUJUAN:
Memverifikasi Hukum Beer-Lambert:
  I = I0 * e^(-μx)
Di mana intensitas (I) menurun secara eksponensial seiring bertambahnya ketebalan (x).""",
                "guide_content": """PETUNJUK PRAKTIKUM PENYERAPAN SINAR-X

A. DASAR TEORI
Sinar-X mengalami pelemahan intensitas (atenuasi) saat melewati materi, mengikuti Hukum Beer-Lambert:
I = I0 * e^(-μ * x)

Dimana:
I  : Intensitas akhir (CPS)
I0 : Intensitas awal (tanpa absorber/udara)
μ  : Koefisien atenuasi linear (cm^-1)
x  : Ketebalan bahan (cm)

Nilai μ bergantung pada:
1. Jenis Bahan (Nomor atom Z dan Densitas ρ). Semakin besar Z/ρ, μ semakin besar.
2. Energi Foton (Tegangan kV). Semakin tinggi kV, daya tembus makin besar, sehingga μ efektif mengecil.

B. LANGKAH PERCOBAAN
1. Nyalakan Sumber Sinar-X (Klik tombol POWER).
2. Tentukan Tegangan (misal 30 kV).
3. Pilih Bahan Absorber (misal Aluminium).
4. Variasikan Ketebalan dari 0 mm s.d 10 mm.
   - Amati penurunan nilai CPS (Counts per Second) pada Geiger Counter.
   - Perhatikan visualisasi "sinar" yang meredup di panel tengah.
5. Klik "Catat Data ke Tabel" untuk setiap variasi tebal.
6. Masuk ke Tab Analisis Data.
   - Klik "Hitung Mu" untuk mendapatkan nilai koefisien atenuasi dari gradien grafik semi-logaritmik.""",
                "diag_title": "X-Ray Unit Diagram (Phywe/Leybold Type)",
                "diag_housing": "Safety Housing (Lead Glass)",
                "diag_tube": "X-Ray Tube",
                "diag_absorber": "Absorber\nSlot",
                "diag_gm": "Geiger-Muller Tube",
                "diag_counter": "Counter / Timer"
            },
            "EN": {
                "title": "X-Ray Properties & Absorption (Beer-Lambert Law)",
                "tab_exp": "Absorption Experiment",
                "tab_ana": "Data Analysis",
                "tab_guide": "Practical Guide",
                "tab_scheme": "Tool Scheme & Explanation",
                "tab_diagram": "Device Circuit Overview",
                "lbl_volt": "Voltage (kV):",
                "lbl_absorber": "Absorber:",
                "lbl_thick": "Thickness (mm):",
                "lbl_gm": "GM Counter Output",
                "btn_record": "Record Data",
                "btn_calc": "Calculate Mu (μ)",
                "btn_clear": "Clear All",
                "btn_save": "Save Data",
                "col_mat": "Material",
                "col_th": "Thickness (mm)",
                "col_v": "Voltage (kV)",
                "col_i": "I_meas (CPS)",
                "col_log": "Log(I0/I)",
                "msg_reg_err": "Min 2 data points for regression.",
                "msg_warn_power": "Turn on Power first!",
                "msg_reg_res": "Regression Result for {mat}:\nμ = {mu:.3f} cm^-1\nI0 (interpolated) = {i0:.0f} CPS",
                "plot_title": "Beer-Lambert Law (Log I0/I vs Thickness)",
                "plot_y": "Log(I0 / I)",
                "plot_x": "Absorber Thickness (mm)",
                "scheme_title": "X-Ray Absorption Tool Scheme",
                "scheme_content": """TOOL SCHEME AND EXPLANATION

This experiment uses a shielded X-ray generation unit to study radiation attenuation as it passes through matter.

MAIN COMPONENTS:

1. X-Ray Tube
   Vacuum tube where electrons accelerated by high voltage (20-50 kV) strike a metal target (Tungsten/Molybdenum Anode). This collision produces characteristic X-rays and Bremsstrahlung.

2. Collimator
   Thick metal slit (lead) to limit the X-ray beam to a single directed straight line towards the detector, preventing scattering in all directions.

3. Absorber Slot (Sample Holder)
   Holder for placing absorber plates such as Aluminium, Copper, or Lead with varying thicknesses.

4. Geiger-Muller Detector (GM Tube)
   Sensor containing noble gas that ionizes when hit by X-ray photons, producing electrical pulses.

5. Ratemeter / Counter
   Counts pulses from GM detector per unit time (Counts per Second / CPS), representing the INTENSITY of passing X-rays.

OBJECTIVE:
Verify Beer-Lambert Law:
  I = I0 * e^(-μx)
Where intensity (I) decreases exponentially with increasing thickness (x).""",
                "guide_content": """PRACTICAL GUIDE: X-RAY ABSORPTION

A. THEORETICAL BASIS
X-rays undergo intensity attenuation when passing through matter, following Beer-Lambert Law:
I = I0 * e^(-μ * x)

Where:
I  : Final intensity (CPS)
I0 : Initial intensity (without absorber/air)
μ  : Linear attenuation coefficient (cm^-1)
x  : Material thickness (cm)

Value of μ depends on:
1. Material Type (Atomic number Z and Density ρ). Higher Z/ρ, larger μ.
2. Photon Energy (Voltage kV). Higher kV, greater penetration power, so effective μ decreases.

B. EXPERIMENTAL STEPS
1. Turn on X-Ray Source (Click POWER button).
2. Set Voltage (e.g. 30 kV).
3. Select Absorber Material (e.g. Aluminium).
4. Vary Thickness from 0 mm to 10 mm.
   - Observe CPS (Counts per Second) decrease on Geiger Counter.
   - Observe "ray" dimming visualization in center panel.
5. Click "Record Data" for each thickness variation.
6. Go to Data Analysis Tab.
   - Click "Calculate Mu" to get attenuation coefficient from semi-logarithmic graph slope.""",
                "diag_title": "X-Ray Unit Diagram (Phywe/Leybold Type)",
                "diag_housing": "Safety Housing (Lead Glass)",
                "diag_tube": "X-Ray Tube",
                "diag_absorber": "Absorber\nSlot",
                "diag_gm": "Geiger-Muller Tube",
                "diag_counter": "Counter / Timer"
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
        self.lbl_v_txt.config(text=self.T("lbl_volt"))
        self.lbl_abs_txt.config(text=self.T("lbl_absorber"))
        self.lbl_th_txt.config(text=self.T("lbl_thick"))
        self.btn_record.config(text=self.T("btn_record"))
        self.lbl_gm_title.config(text=self.T("lbl_gm"))
        
        # Analysis UI
        headers = [self.T("col_mat"), self.T("col_th"), self.T("col_v"), self.T("col_i"), self.T("col_log")]
        # Only update headings, do not reset columns
        if hasattr(self, 'tree_cols'):
            for col, header in zip(self.tree_cols, headers):
                self.tree.heading(col, text=header)
            
        self.btn_calc.config(text=self.T("btn_calc"))
        self.btn_clear.config(text=self.T("btn_clear"))
        self.btn_save.config(text=self.T("btn_save"))
        self.lbl_result.config(text=self.T("msg_reg_err"))
        
        self.ax.set_title(self.T("plot_title"))
        self.ax.set_ylabel(self.T("plot_y"))
        self.ax.set_xlabel(self.T("plot_x"))
        self.graph_canvas.draw()
        
        # Guide & Scheme
        self.txt_guide.config(state="normal")
        self.txt_guide.delete("1.0", tk.END)
        self.txt_guide.insert("1.0", self.T("guide_content"))
        self.txt_guide.config(state="disabled")

        self.lbl_scheme_title.config(text=self.T("scheme_title"))
        # Scheme content refresh if needed (it is static in create usually, need to refactor)
        self.txt_scheme.config(state="normal")
        self.txt_scheme.delete("1.0", tk.END)
        self.txt_scheme.insert("1.0", self.T("scheme_content"))
        self.txt_scheme.config(state="disabled")
        
        # Diagram
        self.canvas_diag.itemconfigure("diag_title", text=self.T("diag_title"))
        self.canvas_diag.itemconfigure("diag_housing", text=self.T("diag_housing"))
        self.canvas_diag.itemconfigure("diag_tube", text=self.T("diag_tube"))
        self.canvas_diag.itemconfigure("diag_absorber", text=self.T("diag_absorber"))
        self.canvas_diag.itemconfigure("diag_gm", text=self.T("diag_gm"))
        self.canvas_diag.itemconfigure("diag_counter", text=self.T("diag_counter"))
            
        
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
        
        # Tab 1: Experiment Simulation
        self.tab_exp = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_exp, text=self.T("tab_exp"))
        self.create_experiment_ui()
        
        # Tab 2: Analysis
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
        self.canvas_diag = tk.Canvas(self.tab_diagram, bg="white")
        self.canvas_diag.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.canvas_diag.create_text(400, 50, text=self.T("diag_title"), font=("Arial", 14, "bold"), tag="diag_title")
        
        # 1. Main Housing (Lead Glass Box)
        self.canvas_diag.create_rectangle(150, 100, 650, 400, outline="gray", width=4) # Transparent door frame
        self.canvas_diag.create_text(400, 80, text=self.T("diag_housing"), font=("Arial", 10), tag="diag_housing")
        
        # 2. X-Ray Tube Tower
        self.canvas_diag.create_rectangle(200, 150, 280, 350, fill="#7f8c8d", outline="black")
        self.canvas_diag.create_text(240, 365, text=self.T("diag_tube"), font=("Arial", 11, "bold"), tag="diag_tube")
        # Anode
        self.canvas_diag.create_line(240, 180, 260, 220, fill="#e74c3c", width=3) # Target angle
        
        # Collimator exit
        self.canvas_diag.create_line(280, 220, 320, 220, fill="orange", width=2, dash=(2,2), arrow="last")
        
        # 3. Sample/Absorber Holder
        self.canvas_diag.create_rectangle(320, 180, 340, 260, fill="#95a5a6", outline="black")
        self.canvas_diag.create_text(330, 275, text=self.T("diag_absorber"), font=("Arial", 9), tag="diag_absorber")
        
        # 4. Detector Goniometer Arm
        self.canvas_diag.create_line(330, 350, 500, 350, width=5, fill="black") # Base
        self.canvas_diag.create_line(500, 350, 500, 220, width=5, fill="black") # Post
        
        # GM Tube Sensor
        self.canvas_diag.create_rectangle(450, 200, 550, 240, fill="#34495e", outline="black")
        self.canvas_diag.create_text(500, 190, text=self.T("diag_gm"), font=("Arial", 10, "bold"), tag="diag_gm")
        self.canvas_diag.create_oval(450, 205, 460, 235, fill="black") # Window
        
        # 5. Connection to Counter
        self.canvas_diag.create_line(550, 220, 680, 220, width=2, fill="black", smooth=True)
        
        # Rate Meter Unit
        self.canvas_diag.create_rectangle(680, 150, 780, 300, fill="#ecf0f1", outline="black")
        self.canvas_diag.create_text(730, 170, text=self.T("diag_counter"), font=("Arial", 9), tag="diag_counter")
        self.canvas_diag.create_rectangle(690, 180, 770, 220, fill="black")
        self.canvas_diag.create_text(730, 200, text="455 CPS", font=("Ds-Digital", 16), fill="red")


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
        # Full Tab Layout: Top (Simulation) and Bottom (Controls)
        main_layout = tk.Frame(self.tab_exp, bg="#f5f6fa")
        main_layout.pack(fill="both", expand=True, padx=10, pady=10)
        
        # --- Top: Visualization ---
        top_frame = tk.Frame(main_layout, bg="#2c3e50")
        top_frame.pack(side="top", fill="both", expand=True, pady=(0, 10))
        
        self.canvas = tk.Canvas(top_frame, bg="#2c3e50", height=400)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        # --- Bottom: Controls & Detector ---
        bottom_frame = tk.Frame(main_layout, bg="white", relief="raised", bd=1)
        bottom_frame.pack(side="bottom", fill="x", padx=5, pady=5)
        
        # Split Bottom into Left (Controls) and Right (Detector Display)
        
        # Left: Controls
        ctrl_frame = tk.Frame(bottom_frame, bg="white")
        ctrl_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Row 1: Power & Voltage
        r1 = tk.Frame(ctrl_frame, bg="white")
        r1.pack(fill="x", pady=5)
        
        self.btn_power = tk.Button(r1, text="POWER: OFF", bg="#e74c3c", fg="black", font=("Arial", 12, "bold"),
                                   command=self.toggle_power, width=15)
        self.btn_power.pack(side="left", padx=10)
        
        self.lbl_v_txt = tk.Label(r1, text=self.T("lbl_volt"), bg="white")
        self.lbl_v_txt.pack(side="left", padx=5)
        self.kv_var = tk.DoubleVar(value=30.0)
        tk.Scale(r1, from_=20.0, to=50.0, variable=self.kv_var, orient="horizontal", length=200,
                 bg="white", command=self.update_params).pack(side="left", padx=5)
        self.lbl_kV = tk.Label(r1, text="30.0 kV", font=("Ds-Digital", 16), fg="#e67e22", bg="black", width=8)
        self.lbl_kV.pack(side="left", padx=5)
        
        # Row 2: Absorber
        r2 = tk.Frame(ctrl_frame, bg="white")
        r2.pack(fill="x", pady=5)
        
        self.lbl_abs_txt = tk.Label(r2, text=self.T("lbl_absorber"), bg="white", width=12, anchor="w")
        self.lbl_abs_txt.pack(side="left", padx=5)
        self.mat_var = tk.StringVar(value="Udara (Tanpa Absorber)")
        cb_mat = ttk.Combobox(r2, textvariable=self.mat_var, values=list(self.materials.keys()), state="readonly", width=25)
        cb_mat.pack(side="left", padx=5)
        cb_mat.bind("<<ComboboxSelected>>", self.update_params)
        
        self.lbl_th_txt = tk.Label(r2, text=self.T("lbl_thick"), bg="white")
        self.lbl_th_txt.pack(side="left", padx=10)
        self.thick_var = tk.DoubleVar(value=0.0)
        tk.Scale(r2, from_=0.0, to=10.0, resolution=0.1, variable=self.thick_var, orient="horizontal", length=200,
                 bg="white", command=self.update_params).pack(side="left", padx=5)

        self.btn_record = tk.Button(r2, text=self.T("btn_record"), bg="#3498db", fg="black", command=self.record_data)
        self.btn_record.pack(side="left", padx=20)

        # Right: Detector Display (GM Counter)
        det_frame = tk.Frame(bottom_frame, bg="#ecf0f1", relief="sunken", bd=1, width=250)
        det_frame.pack(side="right", fill="y", padx=10, pady=10)
        det_frame.pack_propagate(False)
        
        self.lbl_gm_title = tk.Label(det_frame, text=self.T("lbl_gm"), font=("Arial", 10, "bold"), bg="#ecf0f1")
        self.lbl_gm_title.pack(pady=5)
        self.lbl_counts = tk.Label(det_frame, text="0", font=("Courier New", 28, "bold"), fg="#2ecc71", bg="black")
        self.lbl_counts.pack(padx=10, pady=5, fill="x")
        tk.Label(det_frame, text="CPS", bg="#ecf0f1").pack()
        
        self.bar_intensity = ttk.Progressbar(det_frame, orient="horizontal", length=200, mode="determinate")
        self.bar_intensity.pack(pady=10, padx=10)

    def create_analysis_ui(self):
        # Paned Window (Split)
        paned = tk.PanedWindow(self.tab_ana, orient=tk.HORIZONTAL, bg="#f5f6fa", sashwidth=5)
        paned.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left Frame: Table
        left_frame = tk.Frame(paned, bg="white", width=400)
        paned.add(left_frame, minsize=400)

        # Table
        self.tree_cols = ("mat", "th", "v", "i", "log")
        self.tree = ttk.Treeview(left_frame, columns=self.tree_cols, show="headings", height=15)
        
        # Initial headings setup
        headers = [self.T("col_mat"), self.T("col_th"), self.T("col_v"), self.T("col_i"), self.T("col_log")]
        for col, header in zip(self.tree_cols, headers):
            self.tree.heading(col, text=header)
            width = 80 if "mm" in header or "Bahan" in header or "Material" in header else 70
            if col == "mat": width = 120
            self.tree.column(col, width=width, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        btn_box = tk.Frame(left_frame, bg="white")
        btn_box.pack(fill="x", pady=10, padx=5)
        
        self.btn_calc = tk.Button(btn_box, text=self.T("btn_calc"), command=self.calculate_mu, bg="#9b59b6", fg="black")
        self.btn_calc.pack(side="left", padx=5, fill="x", expand=True)
        self.btn_clear = tk.Button(btn_box, text=self.T("btn_clear"), command=self.clear_data, bg="#c0392b", fg="black")
        self.btn_clear.pack(side="left", padx=5, fill="x", expand=True)
        self.btn_save = tk.Button(btn_box, text=self.T("btn_save"), command=self.save_data_unified, bg="#3498db", fg="black")
        self.btn_save.pack(side="left", padx=5, fill="x", expand=True)
        
        self.lbl_result = tk.Label(left_frame, text=self.T("msg_reg_err"), bg="white", font=("Arial", 11), fg="#2c3e50")
        self.lbl_result.pack(pady=10)

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
        self.txt_guide = tk.Text(self.tab_guide, font=("Arial", 12), padx=20, pady=20, wrap="word")
        self.txt_guide.pack(fill="both", expand=True)
        self.txt_guide.insert("1.0", self.T("guide_content"))
        self.txt_guide.config(state="disabled")

    def toggle_power(self):
        self.is_on = not self.is_on
        if self.is_on:
            self.btn_power.config(text="POWER: ON", bg="#2ecc71")
            self.update_simulation_loop()
        else:
            self.btn_power.config(text="POWER: OFF", bg="#e74c3c")
            self.lbl_counts.config(text="0")
            self.bar_intensity['value'] = 0
            self.canvas.delete("beam")

    def update_params(self, event=None):
        self.voltage_kV = self.kv_var.get()
        self.thickness_mm = self.thick_var.get()
        self.lbl_kV.config(text=f"{self.voltage_kV:.1f} kV")
        
        mat_name = self.mat_var.get()
        self.current_mu = self.materials[mat_name]["mu"]
        
        # Adjust mu slightly based on kV (Physics correction: Higher kV -> Lower mu)
        # Reference at 30kV.
        # Approx: mu ~ E^-3. But let's use simpler inverse.
        factor = (30.0 / self.voltage_kV) ** 2 
        self.effective_mu = self.current_mu * factor

        self.draw_apparatus()
        
    def draw_apparatus(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w<10: w=400; h=400
        
        cy = h/2
        
        # 1. Source (Tube)
        self.canvas.create_rectangle(50, cy-40, 150, cy+40, fill="#7f8c8d", outline="white", width=2)
        self.canvas.create_text(100, cy, text="X-RAY\nTUBE", fill="white", font=("Arial", 10, "bold"))
        
        # 2. Detector
        self.canvas.create_rectangle(w-100, cy-30, w-50, cy+30, fill="#27ae60", outline="white", width=2)
        self.canvas.create_text(w-75, cy, text="GM\nTUBE", fill="white", font=("Arial", 8))
        
        # 3. Absorber
        mat_name = self.mat_var.get()
        if "Udara" not in mat_name:
            color = self.materials[mat_name]["color"]
            # Visual thicknes exaggeration
            vis_thick = max(5, self.thickness_mm * 5)
            
            x_absorber = w/2
            self.canvas.create_rectangle(x_absorber - vis_thick/2, cy-60, 
                                         x_absorber + vis_thick/2, cy+60, 
                                         fill=color, outline="white")
            self.canvas.create_text(x_absorber, cy-75, text=f"{self.thickness_mm}mm", fill="white")

    def update_simulation_loop(self):
        if not self.is_on or not self.running: return
        
        # Physics Calculation
        # I_source approx prop to kV^2
        # Use 30kV as baseline 10,000 cps
        I_source = self.I0_base * ((self.voltage_kV / 30.0) ** 2)
        
        # Attenuation I = I0 * exp(-mu * x_cm)
        x_cm = self.thickness_mm / 10.0
        I_detected = I_source * math.exp(-self.effective_mu * x_cm)
        
        # Poisson Noise
        noise = random.gauss(0, math.sqrt(I_detected)) if I_detected > 0 else 0
        final_cps = max(0, I_detected + noise)
        
        # Update UI
        self.lbl_counts.config(text=f"{int(final_cps)}")
        
        # Progress Bar (Relative to max possible ~ 30000)
        max_cps = self.I0_base * ((50/30)**2)
        self.bar_intensity['value'] = (final_cps / max_cps) * 100
        
        # Visual Beam
        self.draw_beam(I_source, I_detected)
        
        self.after(200, self.update_simulation_loop)
        
    def draw_beam(self, I_src, I_det):
        self.canvas.delete("beam")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        cy = h/2
        
        # Beam 1: Source to Absorber
        # Brightness proportional to I_src
        # Assume max brightness = 255
        
        def intensity_to_hex(val):
            # mapping 0-30000 to 0-255
            norm = min(1.0, val / 25000.0)
            c = int(255 * norm)
            return f"#{c:02x}{c:02x}00" # Yellowish
            
        col_src = intensity_to_hex(I_src)
        col_det = intensity_to_hex(I_det)
        
        x_absorber = w/2
        
        # Segment 1 (Pre-absorber)
        if "Udara" in self.mat_var.get():
            # Full path
            self.canvas.create_line(150, cy, w-100, cy, fill=col_src, width=5, arrow="last", tags="beam")
        else:
            vis_thick = max(5, self.thickness_mm * 5)
            x_start_abs = x_absorber - vis_thick/2
            x_end_abs = x_absorber + vis_thick/2
            
            # Source -> Abs
            self.canvas.create_line(150, cy, x_start_abs, cy, fill=col_src, width=5, arrow="last", tags="beam")
            
            # Abs -> Det (Attenuated)
            self.canvas.create_line(x_end_abs, cy, w-100, cy, fill=col_det, width=5, arrow="last", tags="beam")

    def record_data(self):
        if not self.is_on:
            messagebox.showwarning("Warning", self.T("msg_warn_power"))
            return
            
        cps = int(self.lbl_counts.cget("text"))
        mat = self.mat_var.get().split(' ')[0]
        
        # Calculate log ratio for checking
        # Assuming I0 is approximately the value at same voltage with 0 thickness
        # Roughly I0_source calculated
        I0_est = self.I0_base * ((self.voltage_kV / 30.0) ** 2)
        try:
            val_log = math.log(I0_est / (cps if cps > 0 else 0.1))
        except:
            val_log = 0.0
            
        self.tree.insert("", "end", values=(mat, f"{self.thickness_mm}", f"{self.voltage_kV}", f"{cps}", f"{val_log:.2f}"))
        self.data_points.append({
            "mat": mat, "x": self.thickness_mm, "I": cps, "kV": self.voltage_kV
        })
        self.update_graph()

    def calculate_mu(self):
        # Filter data for current material and voltage
        curr_mat = self.mat_var.get().split(' ')[0]
        # Collect (x cm, ln I) pairs
        points = []
        
        # Get data from tree or internal list
        # Using internal list is safer.
        # Needs I0 (at x=0).
        
        # Heuristic: Find Max I in the dataset for this material/kV, assume it's I0 (approx x=0)
        # Better: Perform regression on ln(I) = ln(I0) - mu*x
        
        xy_pairs = []
        for d in self.data_points:
            if d['mat'] == curr_mat: # Simple: ignore kV variation for now or assume user kept it const
                x_cm = d['x'] / 10.0
                if d['I'] > 0:
                    y = math.log(d['I'])
                    xy_pairs.append((x_cm, y))
                    
        if len(xy_pairs) < 2:
            self.lbl_result.config(text=self.T("msg_reg_err"))
            return
            
        # Linear Regression: y = mx + c -> ln(I) = -mu * x + ln(I0)
        # Slope m = -mu
        
        sum_x = sum(p[0] for p in xy_pairs)
        sum_y = sum(p[1] for p in xy_pairs)
        sum_xy = sum(p[0]*p[1] for p in xy_pairs)
        sum_xx = sum(p[0]**2 for p in xy_pairs)
        n = len(xy_pairs)
        
        denom = (n * sum_xx - sum_x**2)
        if denom == 0: return
        
        slope = (n * sum_xy - sum_x * sum_y) / denom
        intercept = (sum_y - slope * sum_x) / n
        
        mu_res = -slope
        I0_res = math.exp(intercept)
        
        res_txt = self.T("msg_reg_res").format(mat=curr_mat, mu=mu_res, i0=I0_res)
        self.lbl_result.config(text=res_txt, fg="green")

    def clear_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.data_points = []
        self.lbl_result.config(text="")
        self.update_graph()

    def update_graph(self):
        # Plot Log(I0/I) vs Thickness
        xs = [] # Thickness
        ys = [] # Log ratio
        
        for child in self.tree.get_children():
            vals = self.tree.item(child)["values"]
            # Thickness is index 1 (mm)
            # Log ratio is index 4
            try:
                x = float(vals[1])
                y = float(vals[4])
                xs.append(x)
                ys.append(y)
            except:
                pass
                
        self.ax.clear()
        self.ax.set_title(self.T("plot_title"))
        self.ax.set_ylabel(self.T("plot_y"))
        self.ax.set_xlabel(self.T("plot_x"))
        self.ax.grid(True)
        
        if xs:
            self.ax.scatter(xs, ys, c='red', marker='x')
        
        # Draw fit line if regression result exists in label?
        # Too parsing-heavy. Leave as scatter.
            
        self.graph_canvas.draw()
        
    def get_data(self):
        export_data = []
        for child in self.tree.get_children():
            vals = self.tree.item(child)["values"]
            row = {
                "Bahan": vals[0],
                "Tebal (mm)": vals[1],
                "Tegangan (kV)": vals[2],
                "I_ukur (CPS)": vals[3],
                "Log(I0/I)": vals[4]
            }
            export_data.append(row)
        return export_data

    def save_data_unified(self):
        data = self.get_data()
        success, msg = DataManager.save_data_unified(data, "SifatSinarX")
        
        if success:
            messagebox.showinfo("Sukses", msg)
        else:
            messagebox.showwarning("Perhatian", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabSinarX(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
