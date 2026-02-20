import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from virtual_lab_data_manager import DataManager, ScrollableFrame

class VirtualLabKonstantaPlanck(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#f5f6fa")

        # Physics Constants (Hidden)
        self.h_real = 6.626e-34
        self.c = 3.0e8
        self.e = 1.602e-19
        
        # Work function for Cesium approx 2.1 eV
        self.phi_eV = 2.1 + random.uniform(-0.1, 0.1)
        self.phi_J = self.phi_eV * self.e
        
        # State variables
        self.current_wavelength_nm = 500 # Default
        self.intensity = 50
        self.voltage = 0.0 # Applied voltage (retarding)
        self.is_light_on = False
        self.measured_current = 0.0
        self.data_points = [] # List of (freq, Vs)
        self.running = True

        # Scale Factor
        self.S = 1.5
        
        self.setup_translations()
        self.lang = "ID"
        self.create_widgets()

    def start_animation(self):
        self.running = True
        # Restart animation loops if they were running
        if self.is_light_on:
             self.animate_photons()
             self.animate_electrons()

    def stop_animation(self):
        self.running = False
        if self.is_light_on:
            self.toggle_light()

    def setup_translations(self):
        self.translations = {
            "ID": {
                "title": "Eksperimen Efek Fotolistrik & Konstanta Planck",
                "tab_sim": "Simulasi & Pengambilan Data",
                "tab_anl": "Analisis Data",
                "tab_guide": "Petunjuk Praktikum",
                "tab_scheme": "Skema Alat & Penjelasan",
                "tab_diag": "Gambaran Rangkaian Alat",
                "src_light": "1. Sumber Cahaya (Frekuensi)",
                "btn_light_on": "NYALAKAN LAMPU",
                "btn_light_off": "MATIKAN LAMPU",
                "intensity": "Intensitas",
                "voltage_ctrl": "2. Tegangan Penghambat (Retarding)",
                "voltage_slide": "Atur Tegangan (Volt)",
                "measure": "3. Alat Ukur",
                "current": "Arus Terukur",
                "btn_take": "Ambil Data (Catat Arus)",
                "col_freq": "Frekuensi (Hz)",
                "col_vstop": "V Stop (V)",
                "anl_title": "Tabel Analisis",
                "btn_calc": "Hitung Konstanta Planck",
                "btn_reset": "Reset Semua Data",
                "save_grp": "Simpan Data",
                "btn_save_all": "☁️ Simpan Database & Excel",
                "res_default": "Hasil Perhitungan:\nh = ... \nError = ... %",
                "theory": "Teori: eVs = hf - W",
                "graph_title": "Grafik Frekuensi (f) vs Potensial Henti (Vs)",
                "xlab": "Frekuensi (Hz)",
                "ylab": "Potensial Henti / Vs (Volts)",
                "msg_data_min": "Butuh minimal 2 titik data untuk menghitung gradien.",
                "msg_reset": "Apakah Anda yakin ingin menghapus semua data?",
                "msg_saved": "Data berhasil disimpan.",
                "msg_current_warning": "Arus masih terdeteksi cukup besar. Data Stopping Potential mungkin tidak akurat. Tetap catat?",
                "lbl_lamp": "Sumber Cahaya",
                "lbl_filter": "Filter",
                "lbl_photocell": "Unit Photocell",
                "lbl_cathode": "Katoda (Cs)",
                "lbl_anode": "Anoda",
                "lbl_measure": "Unit Pengukuran",
                "lbl_zero": "Zero",
                "lbl_volt_adj": "Pengatur Volt",
                "color_red": "Merah (635 nm)",
                "color_yellow": "Kuning (570 nm)",
                "color_green": "Hijau (540 nm)",
                "color_blue": "Biru (460 nm)",
                "color_violet": "Ungu (405 nm)",
                "color_uv": "UV (350 nm)",
                "guide_content": """PETUNJUK PRAKTIKUM VIRTUAL
EFEK FOTOLISTRIK & KONSTANTA PLANCK

A. TUJUAN
1. Mempelajari fenomena efek fotolistrik.
2. Menentukan nilai konstanta Planck (h) melalui eksperimen virtual.
3. Memahami hubungan antara energi foton, fungsi kerja logam, dan energi kinetik elektron.

B. DASAR TEORI
Efek fotolistrik adalah peristiwa terlepasnya elektron dari permukaan logam ketika disinari cahaya. 
Menurut Einstein, energi cahaya terquantisasi dalam paket-paket energi yang disebut foton.
Energi satu foton dirumuskan sebagai: E = h.f

Hubungan energi dalam efek fotolistrik:
Ek_max = h.f - Phi
Dimana:
- Ek_max = Energi kinetik maksimum elektron (Joule)
- h = Konstanta Planck (J.s)
- f = Frekuensi cahaya (Hz)
- Phi = Fungsi kerja logam (Work Function)

Untuk mengukur energi kinetik maksimum, digunakan potensial penghenti (Stopping Potential, Vs).
e.Vs = h.f - Phi

C. LANGKAH PERCOBAAN
1. Masuk ke Tab "Simulasi & Pengambilan Data".
2. Pilih "Sumber Cahaya" dengan panjang gelombang tertentu.
3. "NYALAKAN LAMPU".
4. Perhatikan apakah ada arus yang mengalir.
5. Jika arus mengalir, naikkan "Tegangan Penghambat" secara perlahan.
6. Cari "Potensial Henti" (Stopping Potential), yaitu tegangan TEPAT saat arus menjadi nol.
7. Klik tombol "Ambil Data (Catat Arus)".
8. Ulangi untuk variasi warna cahaya yang lain.
9. Pindah ke Tab "Analisis Data" untuk melakukan perhitungan.""", 
                "scheme_title": "SKEMA ALAT DAN PENJELASAN",
                "scheme_content": """SKEMA ALAT DAN PENJELASAN

1. Sumber Cahaya Monokromatik
   Lampu yang dilengkapi filter atau monokromator untuk menghasilkan cahaya dengan panjang gelombang tertentu.

2. Tabung Fotolistrik (Phototube)
   Tabung vakum yang berisi dua elektroda:
   - Katoda: Logam sasaran yang akan melepaskan elektron.
   - Anoda: Logam pengumpul elektron.

3. Sumber Tegangan Variabel (Retarding Voltage)
   Berfungsi memberikan beda potensial terbalik untuk menghambat laju elektron.

4. Alat Ukur (Ammeter & Voltmeter)
   Mengukur arus fotolistrik yang sangat kecil dan tegangan penghambat."""
            },
            "EN": {
                "title": "Photoelectric Effect & Planck's Constant",
                "tab_sim": "Simulation & Data Collection",
                "tab_anl": "Data Analysis",
                "tab_guide": "Lab Guide",
                "tab_scheme": "Apparatus Scheme & Explanation",
                "tab_diag": "Circuit Diagram",
                "src_light": "1. Light Source (Freq)",
                "btn_light_on": "TURN ON LIGHT",
                "btn_light_off": "TURN OFF LIGHT",
                "intensity": "Intensity",
                "voltage_ctrl": "2. Retarding Voltage",
                "voltage_slide": "Adjust Voltage (Volt)",
                "measure": "3. Measurement",
                "current": "Measured Current",
                "btn_take": "Record Data (Current)",
                "col_freq": "Frequency (Hz)",
                "col_vstop": "V Stop (V)",
                "anl_title": "Analysis Table",
                "btn_calc": "Calculate Planck Constant",
                "btn_reset": "Reset All Data",
                "save_grp": "Save Data",
                "btn_save_all": "☁️ Save Database & Excel",
                "res_default": "Result:\nh = ... \nError = ... %",
                "theory": "Theory: eVs = hf - W",
                "graph_title": "Graph Frequency (f) vs Stopping Potential (Vs)",
                "xlab": "Frequency (Hz)",
                "ylab": "Stopping Potential / Vs (Volts)",
                "msg_data_min": "Need at least 2 data points to calculate gradient.",
                "msg_reset": "Are you sure you want to delete all data?",
                "msg_saved": "Data saved successfully.",
                "msg_current_warning": "Current is still detected. Stopping Potential data might be inaccurate. Record anyway?",
                "lbl_lamp": "Light Source",
                "lbl_filter": "Filter",
                "lbl_photocell": "Photocell Unit",
                "lbl_cathode": "Cathode (Cs)",
                "lbl_anode": "Anode",
                "lbl_measure": "Measurement Unit",
                "lbl_zero": "Zero",
                "lbl_volt_adj": "Volt Adj",
                "color_red": "Red (635 nm)",
                "color_yellow": "Yellow (570 nm)",
                "color_green": "Green (540 nm)",
                "color_blue": "Blue (460 nm)",
                "color_violet": "Violet (405 nm)",
                "color_uv": "UV (350 nm)",
                "guide_content": """VIRTUAL LAB GUIDE
PHOTOELECTRIC EFFECT & PLANCK CONSTANT

A. OBJECTIVES
1. Study the photoelectric effect.
2. Determine Planck's constant (h).
3. Understand the relation between photon energy and work function.

B. THEORY
The photoelectric effect is the emission of electrons when light hits a material.
Einstein proposed: E = h.f

The energy relationship is:
Ek_max = h.f - Phi
Where:
- Ek_max = Max kinetic energy (Joule)
- h = Planck's constant (J.s)
- f = Light frequency (Hz)
- Phi = Work Function

Using Stopping Potential (Vs):
e.Vs = h.f - Phi

C. PROCEDURE
1. Go to "Simulation" tab.
2. Select "Light Source" wavelength.
3. "TURN ON LIGHT".
4. Observe if current flows.
5. Increase "Retarding Voltage" slowly.
6. Find "Stopping Potential" (Vs) where current becomes EXACTLY zero.
7. Click "Record Data".
8. Repeat for other colors.
9. Go to "Analysis" tab to calculate.""",
                "scheme_title": "EQUIPMENT SCHEME",
                "scheme_content": """EQUIPMENT SCHEME & EXPLANATION

1. Monochromatic Light Source
   Lamp with filters to produce specific wavelengths.

2. Phototube
   Vacuum tube containing:
   - Cathode: Target metal emitting electrons.
   - Anode: Collector metal.

3. Variable Retarding Voltage
   Provides reverse potential to stop electron flow.

4. Measurement Tools
   Sensitive ammeter and voltmeter."""
            }
        }

    def T(self, key):
        return self.translations.get(self.lang, self.translations["ID"]).get(key, key)

    def set_language(self, lang):
        self.lang = lang
        self.refresh_ui()

    def refresh_ui(self):
        # Header
        if hasattr(self, 'lbl_title'):
             self.lbl_title.config(text=self.T("title"))
        
        # Tabs
        if hasattr(self, 'notebook'):
            self.notebook.tab(self.tab_simulasi, text=self.T("tab_sim"))
            self.notebook.tab(self.tab_analisis, text=self.T("tab_anl"))
            self.notebook.tab(self.tab_petunjuk, text=self.T("tab_guide"))
            self.notebook.tab(self.tab_scheme, text=self.T("tab_scheme"))
            self.notebook.tab(self.tab_diagram, text=self.T("tab_diag"))

        # Tab Simulation
        if hasattr(self, 'lbl_src_light'): self.lbl_src_light.config(text=self.T("src_light"))
        if hasattr(self, 'radio_btns'):
             for i, btn in enumerate(self.radio_btns):
                  key = self.color_keys[i][0]
                  btn.config(text=self.T(key))
        
        if hasattr(self, 'btn_light'):
             # We need to respect current state
             btn_text = self.T("btn_light_off") if self.is_light_on else self.T("btn_light_on")
             self.btn_light.config(text=btn_text)
             
        if hasattr(self, 'lbl_voltage_ctrl'): self.lbl_voltage_ctrl.config(text=self.T("voltage_ctrl"))
        if hasattr(self, 'volt_slider'): self.volt_slider.config(label=self.T("voltage_slide"))
        if hasattr(self, 'lbl_current_title'): self.lbl_current_title.config(text=self.T("current"))
        if hasattr(self, 'btn_take'): self.btn_take.config(text=self.T("btn_take"))
        
        if hasattr(self, 'tree'):
             self.tree.heading("Freq", text=self.T("col_freq"))
             self.tree.heading("Voltage", text=self.T("col_vstop"))

        # Tab Analysis
        if hasattr(self, 'lbl_anl_title'): self.lbl_anl_title.config(text=self.T("anl_title"))
        if hasattr(self, 'tree_full'):
             self.tree_full.heading("Freq", text=self.T("col_freq"))
             self.tree_full.heading("Voltage", text=self.T("col_vstop"))
             
        if hasattr(self, 'btn_calc'): self.btn_calc.config(text=self.T("btn_calc"))
        
        if hasattr(self, 'lbl_theory'): self.lbl_theory.config(text=self.T("theory"))
        if hasattr(self, 'save_frame'): self.save_frame.config(text=self.T("save_grp"))
        if hasattr(self, 'btn_save_all'): self.btn_save_all.config(text=self.T("btn_save_all"))
        if hasattr(self, 'btn_reset'): self.btn_reset.config(text=self.T("btn_reset"))
        
        if hasattr(self, 'lbl_graph_title'): self.lbl_graph_title.config(text=self.T("graph_title"))
        if hasattr(self, 'ax'):
             self.ax.set_xlabel(self.T("xlab"))
             self.ax.set_ylabel(self.T("ylab"))
             self.graph_canvas.draw()

        # Tab Guide & Scheme
        if hasattr(self, 'txt_guide'):
            self.txt_guide.config(state="normal")
            self.txt_guide.delete("1.0", tk.END)
            self.txt_guide.insert("1.0", self.T("guide_content"))
            self.txt_guide.config(state="disabled")
            
        if hasattr(self, 'lbl_scheme_title'): self.lbl_scheme_title.config(text=self.T("scheme_title"))
        if hasattr(self, 'txt_scheme'):
            self.txt_scheme.config(state="normal")
            self.txt_scheme.delete("1.0", tk.END)
            self.txt_scheme.insert("1.0", self.T("scheme_content"))
            self.txt_scheme.config(state="disabled")

        # Tab Diagram
        if hasattr(self, 'canvas_diag'):
             self.canvas_diag.itemconfigure("lbl_lamp", text=self.T("lbl_lamp"))
             self.canvas_diag.itemconfigure("lbl_filter", text=self.T("lbl_filter"))
             self.canvas_diag.itemconfigure("lbl_photocell", text=self.T("lbl_photocell"))
             self.canvas_diag.itemconfigure("lbl_measure", text=self.T("lbl_measure"))
             self.canvas_diag.itemconfigure("lbl_zero", text=self.T("lbl_zero"))
             self.canvas_diag.itemconfigure("lbl_volt_adj", text=self.T("lbl_volt_adj"))
             
        # Refresh Simulation Canvas (Labels)
        self.draw_setup()
        
    def create_widgets(self):
        # Top Header
        header = tk.Frame(self, bg="#2d3436", pady=10)
        header.pack(fill="x")
        self.lbl_title = tk.Label(header, text=self.T("title"), 
                 font=("Helvetica", 18, "bold"), fg="white", bg="#2d3436")
        self.lbl_title.pack()
        
        # Create Notebook for Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # --- TAB 1: EFEK FOTOLISTRIK (SIMULASI) ---
        self.tab_simulasi = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_simulasi, text=self.T("tab_sim"))
        self.create_tab_simulasi()
        
        # --- TAB 2: ANALISIS DATA ---
        self.tab_analisis = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_analisis, text=self.T("tab_anl"))
        self.create_tab_analisis()
        
        # --- TAB 3: PETUNJUK PRAKTIKUM ---
        self.tab_petunjuk = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_petunjuk, text=self.T("tab_guide"))
        self.create_tab_petunjuk()

        # --- TAB 4: SKEMA ALAT & PENJELASAN ---
        self.tab_scheme = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_scheme, text=self.T("tab_scheme"))
        self.create_tab_scheme()

        # --- TAB 5: GAMBARAN RANGKAIAN ALAT ---
        self.tab_diagram = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_diagram, text=self.T("tab_diag"))
        self.create_tab_diagram()

    def create_tab_diagram(self):
        self.canvas_diag = tk.Canvas(self.tab_diagram, bg="white")
        self.canvas_diag.pack(fill="both", expand=True, padx=20, pady=20)
        canvas = self.canvas_diag
        
        # Draw "Real" Setup Diagram (Vector style)
        w, h = 800, 500
        
        # 1. Mercury Lamp Box
        canvas.create_rectangle(50, 200, 200, 350, fill="#bdc3c7", outline="black", width=2)
        canvas.create_text(125, 275, text=self.T("lbl_lamp"), font=("Arial", 12, "bold"), tag="lbl_lamp")
        canvas.create_rectangle(200, 260, 230, 290, fill="black")
        
        # 2. Filter Wheel / Box
        canvas.create_rectangle(250, 220, 300, 330, fill="#3498db", outline="black")
        canvas.create_text(275, 210, text=self.T("lbl_filter"), font=("Arial", 10), tag="lbl_filter")
        
        # 3. Phototube Unit (h/e Apparatus)
        canvas.create_rectangle(350, 180, 550, 370, fill="#ecf0f1", outline="black", width=2)
        canvas.create_text(450, 385, text=self.T("lbl_photocell"), font=("Arial", 11, "bold"), tag="lbl_photocell")
        
        # Phototube internal
        canvas.create_oval(400, 230, 500, 330, outline="gray", width=2) 
        canvas.create_arc(410, 240, 490, 320, start=90, extent=180, style="arc", outline="red", width=3) 
        canvas.create_line(450, 280, 480, 280, fill="black", width=2) 
        canvas.create_text(420, 250, text="K", fill="red", font=("Arial", 10, "bold"))
        canvas.create_text(470, 270, text="A", fill="black", font=("Arial", 10, "bold"))
        
        # Light Path
        canvas.create_line(230, 275, 410, 275, fill="yellow", width=3, arrow="last", dash=(5,2))
        
        # 4. Measuring Unit (Voltmeter & Ammeter)
        canvas.create_rectangle(600, 200, 780, 350, fill="#2c3e50", outline="black")
        canvas.create_text(690, 365, text=self.T("lbl_measure"), font=("Arial", 11, "bold"), tag="lbl_measure")
        
        # Screen / Meters
        canvas.create_rectangle(620, 220, 760, 270, fill="#27ae60", outline="#2ecc71") # Display
        canvas.create_text(690, 245, text="0.00 V  |  0.00 nA", font=("Courier", 14), fill="#f1c40f")
        
        # Knobs
        canvas.create_oval(630, 290, 660, 320, fill="gray", outline="white") # Zero
        canvas.create_oval(720, 290, 750, 320, fill="gray", outline="white") # Voltage
        canvas.create_text(645, 330, text=self.T("lbl_zero"), fill="white", font=("Arial", 8), tag="lbl_zero")
        canvas.create_text(735, 330, text=self.T("lbl_volt_adj"), fill="white", font=("Arial", 8), tag="lbl_volt_adj")
        
        # Cables
        canvas.create_line(550, 250, 600, 250, fill="black", width=2) # Cable 1
        canvas.create_line(550, 300, 600, 300, fill="red", width=2)   # Cable 2


    def create_tab_scheme(self):
        container = self.tab_scheme
        # Title
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
        
        # --- TOP PANEL: VISUALIZATION ---
        viz_frame = tk.Frame(container, bg="#2d3436", bd=2, relief="sunken")
        viz_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(viz_frame, bg="#2d3436", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.draw_setup() 
        
        # --- BOTTOM PANEL: CONTROLS ---
        control_panel = tk.Frame(container, bg="white", bd=2, relief="raised", height=280)
        control_panel.pack(side="bottom", fill="x", padx=5, pady=5)
        
        control_panel.columnconfigure(0, weight=1)
        control_panel.columnconfigure(1, weight=1)
        control_panel.columnconfigure(2, weight=1)
        
        # COL 1: Light Source
        col1 = tk.Frame(control_panel, bg="white")
        col1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.lbl_src_light = tk.Label(col1, text=self.T("src_light"), font=("Arial", 12, "bold"), bg="white", fg="#0984e3")
        self.lbl_src_light.pack(anchor="w")
        
        # Bilingual Colors via T() mapping keys
        # Store keys to refresh text later
        self.color_keys = [
            ("color_red", 635, "#e17055"),
            ("color_yellow", 575, "#fdcb6e"),
            ("color_green", 540, "#00b894"),
            ("color_blue", 460, "#0984e3"),
            ("color_violet", 405, "#6c5ce7"),
            ("color_uv", 350, "#55efc4")
        ]
        
        # Preserve state if exists
        val = 540
        if hasattr(self, 'wk_var'): val = self.wk_var.get()
        self.wk_var = tk.IntVar(value=val)

        color_frame = tk.Frame(col1, bg="white")
        color_frame.pack(fill="x", pady=5)
        
        self.radio_btns = []
        for i, (key, wavelen, hex_col) in enumerate(self.color_keys):
            text = self.T(key)
            btn = tk.Radiobutton(color_frame, text=text, variable=self.wk_var, value=wavelen, 
                                 command=self.update_simulation, bg="white", 
                                 selectcolor="white", width=18, anchor="w")
            btn.grid(row=i//2, column=i%2, sticky="w")
            self.radio_btns.append(btn)
            
        btn_text = self.T("btn_light_off") if self.is_light_on else self.T("btn_light_on")

        self.btn_light = tk.Button(col1, text=btn_text, bg="#fab1a0", font=("Arial", 11, "bold"), 
                                   command=self.toggle_light)
        self.btn_light.pack(pady=10, fill="x")

        # COL 2: Voltage & Current Display
        col2 = tk.Frame(control_panel, bg="white")
        col2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.lbl_voltage_ctrl = tk.Label(col2, text=self.T("voltage_ctrl"), font=("Arial", 12, "bold"), bg="white", fg="#0984e3")
        self.lbl_voltage_ctrl.pack(anchor="w")
        
        val_v = 0.0
        if hasattr(self, 'volt_var'): val_v = self.volt_var.get()
        self.volt_var = tk.DoubleVar(value=val_v)
        
        self.volt_slider = tk.Scale(col2, from_=0.0, to=3.0, resolution=0.01, 
                                    orient="horizontal", variable=self.volt_var, length=250,
                                    bg="white", label=self.T("voltage_slide"), command=lambda x: self.update_simulation())
        self.volt_slider.pack(fill="x")
        
        self.lbl_current_title = tk.Label(col2, text=self.T("current"), font=("Arial", 11, "bold"), bg="white")
        self.lbl_current_title.pack(anchor="w", pady=(15,0))
        disp_frame = tk.Frame(col2, bg="black", bd=2, relief="sunken")
        disp_frame.pack(fill="x", pady=5)
        
        self.lbl_current = tk.Label(disp_frame, text="0.00 μA", font=("Courier New", 20, "bold"), bg="black", fg="#00ff00")
        self.lbl_current.pack(pady=5)
        
        # COL 3: Data Recording
        col3 = tk.Frame(control_panel, bg="white")
        col3.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        
        self.btn_take = tk.Button(col3, text=self.T("btn_take"), bg="#74b9ff", font=("Arial", 11, "bold"),
                  command=self.record_data)
        self.btn_take.pack(fill="x", pady=5)
         
        # Mini Table
        columns = ("Freq", "Voltage")
        self.tree = ttk.Treeview(col3, columns=columns, show="headings", height=6)
        self.tree.heading("Freq", text=self.T("col_freq"))
        self.tree.heading("Voltage", text=self.T("col_vstop"))
        self.tree.column("Freq", width=120, anchor="center")
        self.tree.column("Voltage", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)

        if hasattr(self, 'data_points'):
             for item in self.tree.get_children():
                  self.tree.delete(item)
             for f, v in self.data_points:
                  self.tree.insert("", "end", values=(f"{f/1e14:.2f}", f"{v:.2f}"))
                 
    def create_tab_analisis(self):
        container = self.tab_analisis
        
        # Split: Left (Table & Basic Calc), Right (Big Graph)
        left_ctrl = tk.Frame(container, bg="white", bd=1, relief="solid", width=350)
        left_ctrl.pack(side="left", fill="y", padx=10, pady=10)
        
        self.lbl_anl_title = tk.Label(left_ctrl, text=self.T("anl_title"), font=("Arial", 14, "bold"), bg="white")
        self.lbl_anl_title.pack(pady=10)
        
        # Full Table on Left
        cols = ("Freq", "Voltage")
        self.tree_full = ttk.Treeview(left_ctrl, columns=cols, show="headings", height=8)
        self.tree_full.heading("Freq", text=self.T("col_freq"))
        self.tree_full.heading("Voltage", text=self.T("col_vstop"))
        self.tree_full.column("Freq", width=120)
        self.tree_full.column("Voltage", width=100)
        self.tree_full.pack(fill="x", padx=10)

        if hasattr(self, 'data_points'):
             for f, v in self.data_points:
                  self.tree_full.insert("", "end", values=(f"{f/1e14:.2f}", f"{v:.2f}"))
        
        self.btn_calc = tk.Button(left_ctrl, text=self.T("btn_calc"), bg="#a29bfe", font=("Arial", 12, "bold"),
                  command=self.calculate_h, pady=10)
        self.btn_calc.pack(fill="x", padx=20, pady=10)
        
        self.lbl_result = tk.Label(left_ctrl, text=self.T("res_default"), font=("Arial", 12), bg="white", fg="red", justify="left")
        self.lbl_result.pack(pady=10, padx=20, anchor="w")
        
        self.lbl_theory = tk.Label(left_ctrl, text=self.T("theory"), font=("Arial", 11, "bold"), bg="white")
        self.lbl_theory.pack(pady=(10,5))
        
        self.save_frame = tk.LabelFrame(left_ctrl, text=self.T("save_grp"), bg="white", font=("Arial", 10, "bold"))
        self.save_frame.pack(fill="x", padx=20, pady=10)
        
        self.btn_save_all = tk.Button(self.save_frame, text=self.T("btn_save_all"), bg="#27ae60", fg="black", font=("Arial", 11),
                  command=self.save_to_all, pady=5)
        self.btn_save_all.pack(fill="x", padx=10, pady=5)
        
        self.btn_reset = tk.Button(left_ctrl, text=self.T("btn_reset"), bg="#ff7675", font=("Arial", 12, "bold"),
          command=self.reset_data)
        self.btn_reset.pack(side="bottom", fill="x", padx=20, pady=20)
        
        # Right: Graph
        graph_frame = tk.Frame(container, bg="white", bd=1, relief="solid")
        graph_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.lbl_graph_title = tk.Label(graph_frame, text=self.T("graph_title"), font=("Arial", 14, "bold"), bg="white")
        self.lbl_graph_title.pack(pady=10)
        
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.ax.set_xlabel(self.T("xlab"))
        self.ax.set_ylabel(self.T("ylab"))
        self.ax.grid(True)
        
        self.graph_canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.graph_canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
        
        toolbar = NavigationToolbar2Tk(self.graph_canvas, graph_frame)
        toolbar.update()
        toolbar.pack(side="bottom", fill="x")

    def create_tab_petunjuk(self):
        container = self.tab_petunjuk
        scrollbar = tk.Scrollbar(container)
        scrollbar.pack(side="right", fill="y")
        
        self.txt_guide = tk.Text(container, font=("Arial", 12), bg="white", padx=20, pady=20, 
                            yscrollcommand=scrollbar.set, wrap="word")
        self.txt_guide.pack(fill="both", expand=True)
        scrollbar.config(command=self.txt_guide.yview)
        
        self.txt_guide.insert("1.0", self.T("guide_content"))
        self.txt_guide.config(state="disabled")

    def draw_setup(self):
        self.canvas.delete("all")
        
        S = self.S  
        dx = 200    
        dy = 50     

        def sc(x, y):
            return (x * S + dx, y * S + dy)
        
        # --- TABUNG VAKUM ---
        t1 = sc(30, 80)
        t2 = sc(490, 320)
        self.canvas.create_oval(t1[0], t1[1], t2[0], t2[1], outline="#74b9ff", width=3, tags="tube")
        
        l_pos = sc(260, 65)
        self.canvas.create_text(l_pos[0], l_pos[1], text="Vacuum Tube", fill="#74b9ff", font=("Arial", 12, "italic"), tags="label")

        # --- ELECTRODES ---
        # Cathode
        c1 = sc(50, 120)
        c2 = sc(70, 280)
        self.canvas.create_rectangle(c1[0], c1[1], c2[0], c2[1], fill="#636e72", outline="#2d3436", tags="cathode_back")
        
        a1 = sc(45, 120)
        a2 = sc(75, 280)
        self.canvas.create_arc(a1[0], a1[1], a2[0], a2[1], start=-90, extent=180, fill="#b2bec3", outline="#636e72", style="chord", tags="cathode")
        
        cl_pos = sc(60, 300)
        self.canvas.create_text(cl_pos[0], cl_pos[1], text=self.T("lbl_cathode"), fill="white", font=("Arial", 10), tags="label")
        
        # Anode
        an1 = sc(450, 140)
        an2 = sc(460, 260)
        self.canvas.create_rectangle(an1[0], an1[1], an2[0], an2[1], fill="#b2bec3", outline="white", tags="anode")
        
        as1 = sc(455, 260)
        as2 = sc(455, 300)
        self.canvas.create_line(as1[0], as1[1], as2[0], as2[1], fill="#b2bec3", width=4) 
        
        al_pos = sc(460, 310)
        self.canvas.create_text(al_pos[0], al_pos[1], text=self.T("lbl_anode"), fill="white", font=("Arial", 10), tags="label")

        # --- CIRCUIT ---
        w1 = sc(60, 300) 
        w2 = sc(60, 360)
        w3 = sc(150, 360)
        self.canvas.create_line(w1[0], w1[1], w2[0], w2[1], fill="#dfe6e9", width=3, tags="wire")
        self.canvas.create_line(w2[0], w2[1], w3[0], w3[1], fill="#dfe6e9", width=3, tags="wire")
        
        am1 = sc(150, 335)
        am2 = sc(200, 385)
        self.canvas.create_oval(am1[0], am1[1], am2[0], am2[1], fill="#2d3436", outline="#dfe6e9", width=2, tags="ammeter")
        
        amt = sc(175, 350)
        self.canvas.create_text(amt[0], amt[1], text="A", fill="#dfe6e9", font=("Arial", 16, "bold"))
        self.canvas.create_text(amt[0], amt[1]+20, text="μA Meter", fill="#b2bec3", font=("Arial", 8))
        
        w4 = sc(200, 360)
        w5 = sc(320, 360)
        self.canvas.create_line(w4[0], w4[1], w5[0], w5[1], fill="#dfe6e9", width=3, tags="wire")
        
        v1 = sc(320, 335)
        v2 = sc(370, 385)
        self.canvas.create_oval(v1[0], v1[1], v2[0], v2[1], fill="#2d3436", outline="#dfe6e9", width=2, tags="source")
        
        vt = sc(345, 350)
        self.canvas.create_text(vt[0], vt[1], text="V", fill="#dfe6e9", font=("Arial", 16, "bold"))
        self.canvas.create_text(vt[0], vt[1]+20, text="Variable", fill="#b2bec3", font=("Arial", 8))
        
        w6 = sc(370, 360) 
        w7 = sc(460, 360) 
        w8 = sc(455, 300) 
        self.canvas.create_line(w6[0], w6[1], w7[0], w7[1], w7[0], w8[1], fill="#dfe6e9", width=3, tags="wire") 

        # --- LAMP ---
        l1 = sc(5, 130)
        l2 = sc(50, 130)
        l3 = sc(50, 180)
        l4 = sc(5, 180)
        self.canvas.create_polygon(l1[0], l1[1], l2[0], l2[1], l3[0], l3[1], l4[0], l4[1], fill="#2d3436", outline="#636e72", width=2, tags="lamp_body")
        
        lt = sc(28, 115)
        self.canvas.create_text(lt[0], lt[1], text="Hg Lamp", fill="white", font=("Arial", 9))
        
        b1 = sc(40, 140)
        b2 = sc(65, 170)
        self.canvas.create_oval(b1[0], b1[1], b2[0], b2[1], fill="#4b4b4b", outline="#2d3436", width=1, tags="bulb")
        
        f1 = sc(45, 150)
        f2 = sc(50, 160)
        f3 = sc(55, 150)
        f4 = sc(60, 160)
        self.canvas.create_line(f1[0], f1[1], f2[0], f2[1], f3[0], f3[1], f4[0], f4[1], fill="gray", smooth=True, width=1, tags="filament")
        
    def toggle_light(self):
        self.is_light_on = not self.is_light_on
        if self.is_light_on:
            self.btn_light.config(text=self.T("btn_light_off"), bg="#ff7675")
            self.animate_photons()
            self.animate_electrons()
            self.update_simulation()
        else:
            self.btn_light.config(text=self.T("btn_light_on"), bg="#fab1a0")
            self.measured_current = 0.0
            self.update_current_display()
            self.canvas.delete("photon")
            self.canvas.delete("electron")
            self.canvas.delete("light_glow") 
            self.canvas.delete("beam")
            self.canvas.itemconfigure("bulb", fill="#4b4b4b") 
            self.canvas.itemconfigure("filament", fill="gray")
            
        self.update_simulation()
            
    def update_simulation(self, _=None):
        self.canvas.delete("beam")
        self.canvas.delete("light_glow")
        
        if not self.is_light_on:
            return
            
        wavelength_nm = self.wk_var.get()
        voltage = self.volt_var.get()
        
        colors_map = {
            635: "#e17055", 575: "#fdcb6e", 540: "#00b894", 460: "#0984e3", 405: "#6c5ce7", 350: "#b2bec3"
        }
        color = colors_map.get(wavelength_nm, "white")
        
        self.canvas.itemconfigure("bulb", fill=color)
        self.canvas.itemconfigure("filament", fill="white")
        
        self.canvas.create_oval(35, 135, 70, 175, fill=color, outline="", stipple="gray50", tags="light_glow")
        self.canvas.create_oval(25, 125, 80, 185, fill=color, outline="", stipple="gray25", tags="light_glow")
        
        S = self.S; dx_ = 200; dy_ = 50
        def sc_(x, y): return (x*S + dx_, y*S + dy_)
        
        b_c = sc_(55, 155)
        c_top = sc_(75, 120)
        c_bot = sc_(75, 280)
        self.canvas.create_polygon(b_c[0], b_c[1], c_top[0], c_top[1], c_bot[0], c_bot[1], fill=color, stipple="gray50", outline="", tags="beam")
        
        self.canvas.tag_lower("beam", "cathode")
        self.canvas.tag_lower("light_glow", "bulb")
        
        freq = self.c / (wavelength_nm * 1e-9)
        energy_photon_J = self.h_real * freq
        ek_max_J = energy_photon_J - self.phi_J
        
        vs_theoretical = ek_max_J / self.e
        
        if ek_max_J > 0:
            if voltage < vs_theoretical:
                current = 10.0 * (1 - (voltage / vs_theoretical)) 
                self.measured_current = max(0.01, current)
            else:
                self.measured_current = 0.0
        else:
            self.measured_current = 0.0
            
        self.update_current_display()

    def update_current_display(self):
        noise = random.uniform(-0.05, 0.05) if self.measured_current > 0 else 0
        display_val = max(0, self.measured_current + noise)
        self.lbl_current.config(text=f"{display_val:.2f} μA")

    def animate_photons(self):
        if not self.is_light_on or not self.running: return

        S = self.S
        dx = 200
        dy = 50
        def sc(x, y): return (x * S + dx, y * S + dy)
        
        start = sc(55, 155)
        y_target_raw = random.randint(120, 280)
        target = sc(75, y_target_raw)
        
        vx = target[0] - start[0]
        vy = target[1] - start[1]
        dist = (vx**2 + vy**2)**0.5
        if dist == 0: dist = 1
        
        speed = 10 * S
        steps = dist / speed
        dx_step = vx / steps
        dy_step = vy / steps
        
        photon = self.canvas.create_oval(start[0], start[1], start[0]+4, start[1]+4, fill="white", outline="white", tags="photon")
        self.move_photon(photon, dx_step, dy_step, steps)
        
        self.after(150, self.animate_photons)

    def move_photon(self, p, dx, dy, steps):
        if not self.running: return
        if not self.canvas.find_withtag(p): return
        if steps <= 0:
            self.canvas.delete(p)
            return
        self.canvas.move(p, dx, dy)
        self.after(20, lambda: self.move_photon(p, dx, dy, steps-1))

    def animate_electrons(self):
        if not self.running: return

        if self.is_light_on and self.measured_current > 0:
            S = self.S
            dx = 200
            dy = 50
            def sc(x, y): return (x * S + dx, y * S + dy)

            y_raw = random.randint(130, 270)
            pos = sc(75, y_raw)
            sz = 8
            electron = self.canvas.create_oval(pos[0], pos[1], pos[0]+sz, pos[1]+sz, fill="yellow", outline="yellow", tags="electron")
            self.move_electron(electron, 5 * S) 
        
        self.after(100, self.animate_electrons)
        
    def move_electron(self, el, speed):
        if not self.running: return
        if not self.canvas.find_withtag(el): return 
        coords = self.canvas.coords(el)
        if not coords: return
        x1 = coords[0]
        
        anode_x = 450 * self.S + 200
        
        if x1 > anode_x: 
            self.canvas.delete(el)
            return
            
        self.canvas.move(el, speed, 0)
        self.after(20, lambda: self.move_electron(el, speed))

    def record_data(self):
        if self.measured_current > 0.5: 
            confirm = messagebox.askyesno("Warning", self.T("msg_current_warning"))
            if not confirm: return
            
        freq_hz = (self.c / (self.wk_var.get() * 1e-9))
        freq_viz = freq_hz / 1e14
        voltage = self.volt_var.get()
        
        self.data_points.append((freq_hz, voltage))
        self.tree.insert("", "end", values=(f"{freq_viz:.2f}", f"{voltage:.2f}"))
        self.tree_full.insert("", "end", values=(f"{freq_hz:.2e}", f"{voltage:.2f}"))
        
        self.update_graph()

    def update_graph(self, slope=None, intercept=None):
        self.ax.clear()
        self.ax.set_title(self.T("graph_title"))
        self.ax.set_xlabel(self.T("xlab"))
        self.ax.set_ylabel(self.T("ylab"))
        self.ax.grid(True)
        
        if not self.data_points:
            self.graph_canvas.draw()
            return
            
        fs = [d[0] for d in self.data_points]
        vs = [d[1] for d in self.data_points]
        self.ax.scatter(fs, vs, color='blue', label='Data')
        
        if slope is not None and intercept is not None:
             import numpy as np
             f_min = min(fs) * 0.9
             f_max = max(fs) * 1.1
             x_line = np.linspace(f_min, f_max, 100)
             y_line = slope * x_line + intercept
             self.ax.plot(x_line, y_line, 'r--', label='Model')
        
        self.ax.legend()
        self.graph_canvas.draw()

    def calculate_h(self):
        if len(self.data_points) < 2:
            messagebox.showwarning("Error", self.T("msg_data_min"))
            return
            
        n = len(self.data_points)
        sum_x = sum(d[0] for d in self.data_points) # f
        sum_y = sum(d[1] for d in self.data_points) # Vs
        sum_xy = sum(d[0]*d[1] for d in self.data_points)
        sum_xx = sum(d[0]**2 for d in self.data_points)
        
        try:
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x**2)
            intercept = (sum_y - slope * sum_x) / n
            
            h_calc = slope * self.e
            error = abs(h_calc - self.h_real) / self.h_real * 100
            
            result_text = f"{self.T('res_default').split(':')[0]}:\nh (Calc) = {h_calc:.2e} J.s\nError = {error:.2f}%"
            self.lbl_result.config(text=result_text)
            
            self.update_graph(slope, intercept)
            
        except ZeroDivisionError:
             messagebox.showerror("Error", "Math Error")

    def save_to_all(self):
        data = self.get_data()
        success, msg = DataManager.save_data_unified(data, "KonstantaPlanck")
        if success:
            messagebox.showinfo("Simpan", self.T("msg_saved") + f"\n{msg}")
        else:
            messagebox.showwarning("Simpan", f"Error: {msg}")

    def get_data(self):
        export = []
        for f, v in self.data_points:
            export.append({
                "Modul": "Konstanta Planck",
                "Frekuensi (Hz)": f,
                "V Stopping (V)": v
            })
        return export

    def reset_data(self):
        if not self.data_points: return
        confirm = messagebox.askyesno("Reset", self.T("msg_reset"))
        if not confirm: return
        
        self.data_points = []
        for item in self.tree.get_children(): self.tree.delete(item)
        for item in self.tree_full.get_children(): self.tree_full.delete(item)
            
        self.update_graph()
        self.lbl_result.config(text=self.T("res_default"))

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabKonstantaPlanck(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
