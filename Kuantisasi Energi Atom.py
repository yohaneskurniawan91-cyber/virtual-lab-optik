import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from virtual_lab_data_manager import DataManager

class VirtualLabFranckHertz(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#f5f6fa")
        
        self.setup_translations()
        self.lang = "ID"

        self.gases = {
            "Uap Merkuri (Hg)": {"E_exc": 4.9, "color": "#3498db", "desc": "Eksitasi UV ~253.7nm"},
            "Gas Neon (Ne)":    {"E_exc": 18.3, "color": "#e74c3c", "desc": "Emisi Cahaya Merah"}
        }
        
        self.selected_gas = "Uap Merkuri (Hg)"
        self.voltage_V = 0.0
        self.current_nA = 0.0
        self.is_running = False
        
        self.data_points = [] # (V, I)
        
        # Peak Detection State
        self.auto_record_var = tk.BooleanVar(value=False)
        self.last_clean_I = None
        self.trend = 0 # 1 Up, -1 Down
        self.last_V_state = 0.0
        self.last_I_noisy = 0.0

        self.setup_ui()
        self.set_language("id")

    def stop_animation(self):
        self.is_running = False

    def setup_translations(self):
        self.translations = {
            "id": {
                "title": "PERCOBAAN FRANCK-HERTZ",
                "subtitle": "Bukti Kuantisasi Energi Atom | Tumbukan Inelastis Elektron",
                "tab_exp": "Eksperimen",
                "tab_ana": "Analisis Data",
                "tab_guide": "Petunjuk Praktikum",
                "tab_scheme": "Skema Alat & Penjelasan",
                "tab_diagram": "Gambaran Rangkaian Alat",
                "ctrl_title": "KONTROL TEGANGAN (V)",
                "lbl_gas": "Tabung Gas:",
                "lbl_volt_ctrl": "Tegangan Percepatan (V2):",
                "btn_record_manual": "Catat Data (Manual)",
                "chk_auto_peak": "Rekam Otomatis (Saat Puncak)",
                "btn_reset": "Reset",
                "btn_save": "☁️ Simpan Data (DB & Excel)",
                "btn_sweep": "AUTO SWEEP (Start)",
                "lbl_pico": "PICOAMMETER",
                "lbl_volt_meter": "VOLTMETER",
                "plt_title": "Kurva Franck-Hertz (I vs V)",
                "plt_x": "Tegangan Percepatan (V)",
                "plt_y": "Arus Anoda (nA)",
                "ana_title": "Analisis Puncak Arus",
                "col_peak": "Puncak Ke-",
                "col_volt": "Tegangan V (Volt)",
                "col_diff": "Selisih dV",
                "btn_analyze": "Cari Puncak Otomatis & Hitung Energi",
                "res_default": "Hasil Analisis: -",
                "msg_data_short": "Lakukan Sweep data terlebih dahulu.",
                "msg_saved": "Data berhasil disimpan!",
                "header_scheme": "Skema Alat Franck-Hertz",
                "diag_tube": "Tabung Trioda Franck-Hertz",
                "diag_oven": "Oven Pemanas",
                "diag_psu": "Unit Catu Daya",
                "diag_ammeter": "Picoammeter",
                "txt_guide": """PETUNJUK PRAKTIKUM FRANCK-HERTZ

A. TUJUAN
Membuktikan kuantisasi energi dalam atom melalui percobaan Franck-Hertz.

B. DASAR TEORI
Dalam tabung berisi gas (misal Hg), elektron dipercepat oleh tegangan V.
- Tumbukan Elastis: Jika E_elektron < Energi Eksitasi atom, elektron hanya memantul, arus terus naik.
- Tumbukan Inelastis: Jika E_elektron = Energi Eksitasi, elektron menyerahkan energinya pada atom Hg. Elektron kehilangan energi kinetik -> Arus turun drastis (Drop).
- Fenomena ini berulang pada V = 1*E, 2*E, 3*E... menghasilkan kurva 'khas' Franck-Hertz yang bergelombang.

Jarak antar puncak tegangan (Delta V) setara dengan Potensial Eksitasi atom tersebut.

C. PROSEDUR
1. Pilih Tabung Gas (Merkuri atau Neon).
2. Gunakan "AUTO SWEEP" untuk menaikkan tegangan secara otomatis dan merekam grafik Arus vs Tegangan.
3. Amati pola naik-turun arus.
4. Buka tab Analisis.
5. Klik "Cari Puncak Otomatis" untuk menghitung rata-rata jarak antar puncak.
6. Bandingkan nilai hasil eksperimen dengan teori (Hg ~ 4.9 eV, Ne ~ 18.3 eV).""",
                "txt_scheme": """SKEMA ALAT DAN PENJELASAN

Eksperimen Franck-Hertz membuktikan adanya tingkat energi energi diskrit dalam atom melalui tumbukan elektron.

KOMPONEN UTAMA:

1. Tabung Franck-Hertz
   Tabung trioda yang berisi tetesan gas Merkuri (Hg) atau Neon (Ne) bertekanan rendah yang dipanaskan dalam oven. Tabung ini memiliki 3 elektroda:
   - Katoda (K): Dipanaskan untuk memancarkan elektron (emisi termionik).
   - Grid Kontrol/Kisi (G): Jaring kawat di tengah tabung.
   - Anoda/Keping Pengumpul (A/P): Menangkap elektron.

2. Sumber Tegangan Percepatan (V2)
   Memberikan beda potensial positif variabel antara Katoda dan Grid (V_GK). Ini berfungsi mempercepat elektron menuju grid.

3. Sumber Tegangan Penghambat (V3 / Retarding Potential)
   Memberikan beda potensial kecil (sekitar 1.5 V) yang berlawanan arah antara Grid dan Anoda. Hanya elektron dengan sisa energi kinetik cukup besar yang bisa melewati penghalang ini dan mencapai anoda.

4. Picoammeter / Elektrometer
   Mengukur arus elektron yang sangat kecil (nA) yang berhasil mencapai anoda.

PRINSIP KERJA:
Saat tegangan percepatan dinaikkan, arus naik. Namun, saat energi elektron mencapai energi eksitasi atom (misal 4.9 eV untuk Hg), elektron memberikan energinya ke atom melalui tumbukan inelastis dan kehilangan kecepatan, sehingga tidak mampu melewati potensial penghambat. Akibatnya arus turun (Drop/Valley). Ini berulang pada kelipatan energi eksitasi."""
            },
            "en": {
                "title": "FRANCK-HERTZ EXPERIMENT",
                "subtitle": "Proof of Atomic Energy Quantization | Inelastic Electron Collisions",
                "tab_exp": "Experiment",
                "tab_ana": "Data Analysis",
                "tab_guide": "User Guide",
                "tab_scheme": "Apparatus Scheme",
                "tab_diagram": "Circuit Diagram",
                "ctrl_title": "VOLTAGE CONTROL (V)",
                "lbl_gas": "Gas Tube:",
                "lbl_volt_ctrl": "Accelerating Voltage (V2):",
                "btn_record_manual": "Record Point (Manual)",
                "chk_auto_peak": "Auto Record (At Peaks)",
                "btn_reset": "Reset",
                "btn_save": "☁️ Save Data (DB & Excel)",
                "btn_sweep": "AUTO SWEEP (Start)",
                "lbl_pico": "PICOAMMETER",
                "lbl_volt_meter": "VOLTMETER",
                "plt_title": "Franck-Hertz Curve (I vs V)",
                "plt_x": "Accelerating Voltage (V)",
                "plt_y": "Anode Current (nA)",
                "ana_title": "Current Peak Analysis",
                "col_peak": "Peak #",
                "col_volt": "Voltage V (Volt)",
                "col_diff": "Diff dV",
                "btn_analyze": "Auto Find Peaks & Calc Energy",
                "res_default": "Analysis Result: -",
                "msg_data_short": "Perform data sweep first.",
                "msg_saved": "Data saved successfully!",
                "header_scheme": "Franck-Hertz Apparatus Scheme",
                "diag_tube": "Franck-Hertz Triode Tube",
                "diag_oven": "Heating Oven",
                "diag_psu": "Power Supply Unit",
                "diag_ammeter": "Picoammeter",
                "txt_guide": """FRANCK-HERTZ LAB GUIDE

A. OBJECTIVES
Prove energy quantization in atoms via Franck-Hertz experiment.

B. THEORY
In a gas-filled tube (e.g. Hg), electrons are accelerated by voltage V.
- Elastic Collision: If E_electron < Excitation Energy, electron bounces, current rises.
- Inelastic Collision: If E_electron = Excitation Energy, electron transfers energy to Hg atom. Electron loses Kinetic Energy -> Current Drops.
- This repeats at V = 1*E, 2*E, 3*E... creating the 'characteristic' wavy Franck-Hertz curve.

Distance between peaks (Delta V) equals the Excitation Potential.

C. PROCEDURE
1. Select Gas Tube (Mercury or Neon).
2. Use "AUTO SWEEP" to increase voltage automatically and record Current vs Voltage graph.
3. Observe current rise-and-fall pattern.
4. Go to Analysis tab.
5. Click "Auto Find Peaks" to calculate average peak spacing.
6. Compare with theory (Hg ~ 4.9 eV, Ne ~ 18.3 eV).""",
                "txt_scheme": """APPARATUS SCHEME AND EXPLANATION

Franck-Hertz experiment proves discrete energy levels in atoms via electron collisions.

MAIN COMPONENTS:
1. Franck-Hertz Tube
   Triode tube with low-pressure Mercury (Hg) or Neon (Ne) gas heated in an oven. 3 Electrodes:
   - Cathode (K): Heated to emit electrons.
   - Control Grid (G): Wire mesh.
   - Anode (A): Collects electrons.

2. Accelerating Voltage (V2)
   Positive potential between Cathode and Grid. Accelerates electrons.

3. Retarding Voltage (V3)
   Small opposing potential (~1.5 V) between Grid and Anode. Only electrons with sufficient KE pass this barrier.

4. Picoammeter
   Measures tiny electron current (nA)."""
            }
        }

    def T(self, key):
        return self.translations.get(self.lang, self.translations["id"]).get(key, key)

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
        self.lbl_ctrl_title.config(text=self.T("ctrl_title"))
        self.lbl_gas.config(text=self.T("lbl_gas"))
        self.lbl_volt_ctrl.config(text=self.T("lbl_volt_ctrl"))
        self.btn_rec_man.config(text=self.T("btn_record_manual"))
        if hasattr(self, 'chk_auto_peak'):
             self.chk_auto_peak.config(text=self.T("chk_auto_peak"))
        self.btn_reset.config(text=self.T("btn_reset"))
        self.btn_save.config(text=self.T("btn_save"))
        self.btn_sweep.config(text=self.T("btn_sweep"))
        self.lbl_pico_title.config(text=self.T("lbl_pico"))
        self.lbl_volt_meter.config(text=self.T("lbl_volt_meter"))
        
        self.ax.set_title(self.T("plt_title"))
        self.ax.set_xlabel(self.T("plt_x"))
        self.ax.set_ylabel(self.T("plt_y"))
        self.canvas_graph.draw()
        
        # Ana
        self.lbl_ana_title.config(text=self.T("ana_title"))
        self.tree.heading("Puncak Ke-", text=self.T("col_peak"))
        self.tree.heading("Tegangan V (Volt)", text=self.T("col_volt"))
        self.tree.heading("Selisih dV", text=self.T("col_diff"))
        self.btn_analyze.config(text=self.T("btn_analyze"))
        self.btn_save_ana.config(text=self.T("btn_save"))
        
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
        
        # Diagram
        self.canvas_diag.itemconfigure("diag_tube", text=self.T("diag_tube"))
        self.canvas_diag.itemconfigure("diag_oven", text=self.T("diag_oven"))
        self.canvas_diag.itemconfigure("diag_psu", text=self.T("diag_psu"))
        self.canvas_diag.itemconfigure("diag_ammeter", text=self.T("diag_ammeter"))
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg="#2c3e50", pady=15)
        header.pack(fill="x")
        self.lbl_title = tk.Label(header, text=self.T("title"), font=("Tw Cen MT", 20, "bold"), fg="#f1c40f", bg="#2c3e50")
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
        
        # Franck-Hertz Tube
        self.canvas_diag.create_oval(300, 150, 500, 350, outline="black", width=2) # Glass Bulb
        self.canvas_diag.create_text(400, 130, text=self.T("diag_tube"), font=("Arial", 12, "bold"), tags="diag_tube")
        
        # Electrodes
        # Cathode
        self.canvas_diag.create_line(350, 250, 350, 300, width=3, fill="red")
        self.canvas_diag.create_text(350, 320, text="K", font=("Arial", 10, "bold"), fill="red")
        # Grid
        self.canvas_diag.create_line(400, 200, 400, 300, width=1, fill="black", dash=(2,2))
        self.canvas_diag.create_text(400, 320, text="G", font=("Arial", 10, "bold"))
        # Anode
        self.canvas_diag.create_line(450, 200, 450, 300, width=3, fill="blue")
        self.canvas_diag.create_text(450, 320, text="A", font=("Arial", 10, "bold"), fill="blue")
        
        # Gas dots
        for _ in range(20):
            x = random.randint(320, 480)
            y = random.randint(180, 320)
            self.canvas_diag.create_oval(x, y, x+3, y+3, fill="#95a5a6", outline="")
            
        # Oven Box around tube
        self.canvas_diag.create_rectangle(280, 140, 520, 360, outline="#e67e22", dash=(4,4), width=2)
        self.canvas_diag.create_text(540, 150, text=self.T("diag_oven"), fill="#e67e22", tags="diag_oven")
        
        # Control Unit
        self.canvas_diag.create_rectangle(50, 150, 250, 350, fill="#2c3e50")
        self.canvas_diag.create_text(150, 170, text=self.T("diag_psu"), font=("Arial", 11, "bold"), fill="white", tags="diag_psu")
        
        # Meters
        self.canvas_diag.create_rectangle(70, 200, 230, 250, fill="black")
        self.canvas_diag.create_text(150, 225, text="45.0 V", font=("Ds-Digital", 20), fill="#3498db") # V2
        
        # Picoammeter External
        self.canvas_diag.create_rectangle(600, 200, 750, 300, fill="#34495e")
        self.canvas_diag.create_text(675, 220, text=self.T("diag_ammeter"), font=("Arial", 10, "bold"), fill="white", tags="diag_ammeter")
        self.canvas_diag.create_rectangle(620, 240, 730, 280, fill="black")
        self.canvas_diag.create_text(675, 260, text="2.1 nA", font=("Ds-Digital", 20), fill="#e74c3c")
        
        # Wiring
        self.canvas_diag.create_line(250, 225, 350, 300, fill="red", width=2, smooth=True) # V2 to K
        self.canvas_diag.create_line(250, 250, 400, 300, fill="black", width=2, smooth=True) # V2 to G
        self.canvas_diag.create_line(450, 300, 600, 250, fill="blue", width=2, smooth=True) # A to Ammeter


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
        main = tk.Frame(self.tab_exp, bg="#f5f6fa")
        main.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left: Controls
        left = tk.Frame(main, bg="white", width=300, relief="raised", bd=1)
        left.pack(side="left", fill="y", padx=5, pady=5)
        
        self.lbl_ctrl_title = tk.Label(left, text=self.T("ctrl_title"), font=("Arial", 12, "bold"), bg="white")
        self.lbl_ctrl_title.pack(pady=15)
        
        # Gas Select
        self.lbl_gas = tk.Label(left, text=self.T("lbl_gas"), bg="white")
        self.lbl_gas.pack(anchor="w", padx=20)
        self.gas_var = tk.StringVar(value=self.selected_gas)
        cb = ttk.Combobox(left, textvariable=self.gas_var, values=list(self.gases.keys()), state="readonly")
        cb.pack(fill="x", padx=20, pady=5)
        cb.bind("<<ComboboxSelected>>", self.reset_data)
        
        # Voltage Control (Slider)
        self.lbl_volt_ctrl = tk.Label(left, text=self.T("lbl_volt_ctrl"), bg="white")
        self.lbl_volt_ctrl.pack(anchor="w", padx=20, pady=(15, 0))
        self.scale_V = tk.Scale(left, from_=0, to=60, resolution=0.1, orient="horizontal", bg="white",
                                command=self.update_simulation)
        self.scale_V.pack(fill="x", padx=20)
        
        # Manual Data Controls
        manual_frame = tk.Frame(left, bg="white", pady=5)
        manual_frame.pack(fill="x", padx=20, pady=5)
        
        self.btn_rec_man = tk.Button(manual_frame, text=self.T("btn_record_manual"), command=self.record_manual_point,
                  bg="#3498db", fg="black", width=15)
        self.btn_rec_man.pack(side="left", fill="x", expand=True, padx=(0,2))
        
        self.btn_reset = tk.Button(manual_frame, text=self.T("btn_reset"), command=self.reset_data_manual,
                  bg="#e74c3c", fg="black", width=6)
        self.btn_reset.pack(side="left", padx=(2,0))

        # Auto Peak Checkbox
        self.chk_auto_peak = tk.Checkbutton(left, text=self.T("chk_auto_peak"), variable=self.auto_record_var, 
                                            bg="white", anchor="w")
        self.chk_auto_peak.pack(fill="x", padx=20, pady=(5,0))

        self.btn_save = tk.Button(left, text=self.T("btn_save"), command=self.save_to_all, 
                  bg="#27ae60", fg="black", font=("Arial", 11))
        self.btn_save.pack(fill="x", padx=20, pady=(5,0))

        # Auto Sweep
        self.btn_sweep = tk.Button(left, text=self.T("btn_sweep"), command=self.start_auto_sweep,
                  bg="#2ecc71", fg="black", font=("Arial", 11, "bold"))
        self.btn_sweep.pack(fill="x", padx=20, pady=20)
        
        # Readings
        meter_frame = tk.Frame(left, bg="#34495e", pady=10)
        meter_frame.pack(fill="x", padx=10, pady=20)
        self.lbl_pico_title = tk.Label(meter_frame, text=self.T("lbl_pico"), fg="#f1c40f", bg="#34495e", font=("Courier", 12))
        self.lbl_pico_title.pack()
        self.lbl_amp = tk.Label(meter_frame, text="0.00 nA", fg="#e74c3c", bg="black", font=("Ds-Digital", 24))
        self.lbl_amp.pack(fill="x", padx=10, pady=5)
        
        self.lbl_volt_meter = tk.Label(meter_frame, text=self.T("lbl_volt_meter"), fg="#f1c40f", bg="#34495e", font=("Courier", 12))
        self.lbl_volt_meter.pack(pady=(10,0))
        self.lbl_volt = tk.Label(meter_frame, text="0.00 V", fg="#3498db", bg="black", font=("Ds-Digital", 24))
        self.lbl_volt.pack(fill="x", padx=10, pady=5)
        
        # Right: Graph & Tube Viz
        right = tk.Frame(main, bg="#f5f6fa")
        right.pack(side="left", fill="both", expand=True, padx=5)
        
        # Mplt Graph
        self.fig, self.ax = plt.subplots(figsize=(5, 3), dpi=100)
        self.ax.set_title(self.T("plt_title"))
        self.ax.set_xlabel(self.T("plt_x"))
        self.ax.set_ylabel(self.T("plt_y"))
        self.ax.grid(True)
        self.canvas_graph = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas_graph.get_tk_widget().pack(fill="both", expand=True)

        # Matplotlib Toolbar
        toolbar = NavigationToolbar2Tk(self.canvas_graph, right)
        toolbar.update()
        toolbar.pack(side="bottom", fill="x")

    def create_analysis_ui(self):
        layout = tk.Frame(self.tab_ana, bg="white")
        layout.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.lbl_ana_title = tk.Label(layout, text=self.T("ana_title"), font=("Arial", 14, "bold"), bg="white")
        self.lbl_ana_title.pack(pady=10)
        
        cols = ("Puncak Ke-", "Tegangan V (Volt)", "Selisih dV")
        self.tree = ttk.Treeview(layout, columns=cols, show="headings", height=8)
        for c in cols:
            # We map header text in refresh_ui
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150, anchor="center")
        self.tree.pack(fill="x")
        
        btn_frame = tk.Frame(layout, bg="white")
        btn_frame.pack(fill="x", pady=10)
        
        self.btn_analyze = tk.Button(btn_frame, text=self.T("btn_analyze"), command=self.analyze_peaks, 
                  bg="#9b59b6", fg="black")
        self.btn_analyze.pack(side="left", padx=5)

        self.btn_save_ana = tk.Button(btn_frame, text=self.T("btn_save"), command=self.save_to_all, 
                  bg="#27ae60", fg="black")
        self.btn_save_ana.pack(side="left", padx=5)
        
        self.lbl_result = tk.Label(layout, text=self.T("res_default"), font=("Courier", 12), bg="#ecf0f1", relief="sunken", pady=10)
        self.lbl_result.pack(fill="x", pady=10)

    def save_to_all(self):
        data = self.get_data()
        # Franx-Hertz is often called Kuantisasi Energi
        success, msg = DataManager.save_data_unified(data, "FranckHertz")
        if success:
            messagebox.showinfo(self.T("btn_save"), msg)
        else:
            messagebox.showwarning(self.T("btn_save"), msg)

    def create_guide_ui(self):
        self.txt_guide = tk.Text(self.tab_guide, font=("Arial", 12), padx=20, pady=20)
        self.txt_guide.pack(fill="both", expand=True)
        
        # Load text based on current language
        self.txt_guide.insert("1.0", self.T("txt_guide"))
        self.txt_guide.config(state="disabled")

    def update_simulation(self, val):
        V = float(val)
        gas_info = self.gases[self.gas_var.get()]
        E_exc = gas_info["E_exc"]
        
        # Franck-Hertz Math Model
        # Base Current (Space Charge)
        if V < 0.5:
            I = 0
        else:
            I_base = 0.5 * (V**1.2)
            # Oscillation Term (Inelastic Collisions)
            # Dips at Multiples of E_exc
            phase = (V / E_exc) * 2 * math.pi
            # Damping factor: dips become less deep relatively but I_base grows
            # Actually drops are periodic.
            # Simple model: Sinusoidal modulation on top of base
            
            modulation = math.sin(phase - math.pi/2) * (V * 0.25)
            # Ensure we don't go negative and maintain general upward trend with dips
            
            # Better physics phenomenological model:
            # Drop happens just AFTER V = n * E_exc
            # Let's stick to the previous model logic but refined
            
            dip_depth = 0.3 * V
            osc = np.cos(2 * np.pi * V / E_exc - np.pi) # dips at integers
            # Map osc (-1 to 1) to reduction
            # When osc is -1 (dip), we substract.
            
            # Simplified:
            current = I_base + (osc * dip_depth * 0.5)
            clean_I = current
            I = max(0, current + random.uniform(-0.5, 0.5))

        if V < 0.5:
             clean_I = 0

        # Peak Detection Logic
        if self.auto_record_var.get() and self.last_clean_I is not None:
            # Check for Peak (Rising -> Falling)
            if clean_I > self.last_clean_I:
                self.trend = 1
            elif clean_I < self.last_clean_I:
                if self.trend == 1:
                    # Peak Detected at last state
                    # Check if point already exists (approx) to prevent spam
                    duplicate = False
                    if self.data_points:
                        last_pt = self.data_points[-1]
                        if abs(last_pt[0] - self.last_V_state) < 0.01:
                            duplicate = True
                    
                    if not duplicate:
                        self.data_points.append((self.last_V_state, self.last_I_noisy))
                        self.update_plot()
                self.trend = -1
        
        self.last_clean_I = clean_I
        self.last_I_noisy = I
        self.last_V_state = V

        self.voltage_V = V
        self.current_nA = I
        
        self.lbl_volt.config(text=f"{V:.2f} V")
        self.lbl_amp.config(text=f"{I:.2f} nA")
        
        # If running Auto Sweep, append automatically (Filtered by checkbox)
        if self.is_running:
            if not self.auto_record_var.get():
                self.data_points.append((V, I))
                self.update_plot()

    def record_manual_point(self):
        """Manually record the current Voltage/Current reading."""
        # Check duplicates if necessary, or just append
        if not hasattr(self, 'current_nA') or not hasattr(self, 'voltage_V'):
            return
            
        # Avoid duplicate precise points if user clicks twice, but floating point diff might make it rare
        # Just append for simplicity
        self.data_points.append((self.voltage_V, self.current_nA))
        
        # Sort data points by Voltage so graph looks correct if they go back and forth
        self.data_points.sort(key=lambda x: x[0])
        
        self.update_plot()
        
    def reset_data_manual(self):
        self.reset_data(None)

    def get_peak_indices(self):
        """Helper to identify indices of peaks in the current data set."""
        if not self.data_points or len(self.data_points) < 3:
            return []
            
        xs, ys = zip(*self.data_points)
        peaks_idx = []
        for i in range(1, len(ys)-1):
            # Check strictly greater than neighbors (local maxima)
            if ys[i-1] < ys[i] and ys[i] > ys[i+1]:
                # Threshold to avoid noise peaks (e.g., extremely low current)
                if ys[i] > 1.0: 
                    peaks_idx.append(i)
        return peaks_idx

    def get_data(self):
        export_data = []
        data_source = self.data_points if self.data_points else []
        
        # Identify peaks to mark them in the export
        peak_indices = set(self.get_peak_indices())
        
        current_gas = self.gas_var.get() if hasattr(self, 'gas_var') else self.selected_gas
        
        for idx, (v, i) in enumerate(data_source):
            note = "PUNCAK" if idx in peak_indices else ""
            export_data.append({
                "Modul": "Franck-Hertz",
                "Gas": current_gas,
                "Tegangan Percepatan (V)": f"{v:.2f}",
                "Arus Anoda (nA)": f"{i:.2f}",
                "Keterangan": note
            })
        return export_data

    def start_auto_sweep(self):
        self.data_points = []
        self.ax.clear()
        self.ax.set_title(f"{self.T('plt_title')} {self.gas_var.get()}")
        self.ax.set_xlabel(self.T("plt_x"))
        self.ax.set_ylabel(self.T("plt_y"))
        self.ax.grid(True)
        self.canvas_graph.draw()
        
        self.is_running = True
        self.current_sweep_v = 0.0
        self.do_sweep_step()
        
    def do_sweep_step(self):
        if not self.is_running: return
        
        if self.current_sweep_v >= 60.0:
            self.is_running = False
            return
            
        self.current_sweep_v += 0.5
        self.scale_V.set(self.current_sweep_v) # This triggers update_simulation and appends data
        
        self.after(50, self.do_sweep_step)

    def update_plot(self):
        if len(self.data_points) < 2: return
        
        xs, ys = zip(*self.data_points)
        self.ax.clear()
        self.ax.plot(xs, ys, '-', color=self.gases[self.gas_var.get()]["color"])
        self.ax.set_title(f"{self.T('plt_title')} ({self.gas_var.get()})")
        self.ax.set_xlabel(self.T("plt_x"))
        self.ax.set_ylabel(self.T("plt_y"))
        self.ax.grid(True)
        self.canvas_graph.draw()

    def reset_data(self, event):
        self.data_points = []
        self.last_clean_I = None
        self.trend = 0
        self.ax.clear()
        self.ax.set_title(self.T("plt_title"))
        self.ax.set_xlabel(self.T("plt_x"))
        self.ax.set_ylabel(self.T("plt_y"))
        self.ax.grid(True)
        self.canvas_graph.draw()
        self.scale_V.set(0)

    def analyze_peaks(self):
        if len(self.data_points) < 10:
            messagebox.showwarning("Info", self.T("msg_data_short"))
            return

        xs, ys = zip(*self.data_points)
        xs = np.array(xs)
        
        # Reuse helper
        peaks_idx = self.get_peak_indices()
        
        # Clear tree
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        peak_voltages = xs[peaks_idx]
        
        diffs = []
        for i, v in enumerate(peak_voltages):
            d = 0
            if i > 0:
                d = v - peak_voltages[i-1]
                diffs.append(d)
            
            self.tree.insert("", "end", values=(i+1, f"{v:.2f}", f"{d:.2f}" if d else "-"))
            
        if diffs:
            avg_diff = sum(diffs)/len(diffs)
            
            # Theoretical check
            gas = self.gases[self.gas_var.get()]
            err = abs(avg_diff - gas["E_exc"]) / gas["E_exc"] * 100
            
            if self.lang == "en":
                 res_str = f"Avg Peak Spacing (Delta V): {avg_diff:.2f} Volt\n"
                 res_str += f"Measured Excitation Energy: {avg_diff:.2f} eV\n"
                 res_str += f"Theoretical Value: {gas['E_exc']} eV (Error {err:.2f}%)"
            else:
                 res_str = f"Rata-rata Jarak Puncak (Delta V): {avg_diff:.2f} Volt\n"
                 res_str += f"Energi Eksitasi Terukur: {avg_diff:.2f} eV\n"
                 res_str += f"Nilai Teori: {gas['E_exc']} eV (Error {err:.2f}%)"
            
            self.lbl_result.config(text=res_str, fg="blue")
        else:
             msg = "Current peaks not detected clearly." if self.lang == "en" else "Puncak arus tidak terdeteksi dengan jelas."
             self.lbl_result.config(text=msg, fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabFranckHertz(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
