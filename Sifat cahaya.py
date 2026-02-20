import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import time
from virtual_lab_data_manager import DataManager

class VirtualLabSifatCahaya(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#f5f6fa")
        
        # Physics Constants
        self.h = 6.626e-34
        self.c = 2.998e8
        self.e = 1.602e-19
        self.W0_eV = 2.1 # Cesium/Potassium typical
        self.W0_J = self.W0_eV * self.e
        
        # Components
        self.filters = {
            "Biru (436 nm)": 436,
            "Hijau (546 nm)": 546,
            "Kuning (577 nm)": 577
        }
        
        self.apertures = {
            "2 mm (Low)": 1.0,  # Scale factor
            "4 mm (Med)": 4.0,  # 2^2 : 4^2 -> 1 : 4
            "8 mm (High)": 16.0 # 2^2 : 8^2 -> 1 : 16
        }
        
        # State
        self.current_nm = 436
        self.current_aperture_scale = 1.0
        self.voltage = 0.0
        self.measured_current = 0.0
        self.trace_data = [] # List of (V, I)
        self.active_trace_color = "blue"
        self.saved_traces = [] # List of dicts {label, color, data: [(v,i)]}
        
        self.lang = "ID"
        self.setup_translations()
        self.create_widgets()

    def setup_translations(self):
        self.translations = {
            "ID": {
                "title": "Karakteristik Fotodioda (Sifat Partikel Cahaya)",
                "tab_exp": "Eksperimen I-V",
                "tab_guide": "Petunjuk Praktikum",
                "tab_scheme": "Skema Alat & Penjelasan",
                "tab_diag": "Gambaran Rangkaian Alat",
                "header_setup": "Pengaturan Alat",
                "grp_optic": "Komponen Optik",
                "lbl_filter": "Filter Warna:",
                "lbl_aper": "Diameter Aperture:",
                "grp_voltage": "Sumber Tegangan Bias",
                "lbl_volt": "Tegangan (V):",
                "lbl_coarse": "Coarse Adj (-5 to 30V)",
                "lbl_fine": "Fine Adj (+/- 1V)",
                "grp_graph": "Kontrol Grafik",
                "btn_plot": "Plot Titik (Manual)",
                "btn_sweep": "Auto-Sweep (Gambar Kurva)",
                "btn_hold": "Simpan Kurva (Hold)",
                "btn_clear": "Hapus Grafik",
                "btn_save_db": "☁️ Simpan (DB & Excel)",
                "graph_title": "Kurva Karakteristik I-V",
                "header_multi": "Multimeter",
                "lbl_current": "Arus Fotodioda (I)",
                "lbl_rail": "Optical Rail / Bangku Optik",
                "lbl_lamp": "Hg Lamp",
                "lbl_filter_item": "Filter",
                "lbl_aperture": "Aperture",
                "lbl_photodiode": "Photodiode",
                "lbl_unit": "Electrometer Unit",
                "lbl_current_disp": "CURRENT (nA)",
                "lbl_legend": "Legenda Kurva:",
                "scheme_title": "Skema Alat Karakteristik Fotodioda",
                "scheme_content": """SKEMA ALAT DAN PENJELASAN

Eksperimen ini mempelajari hubungan antara intensitas cahaya, frekuensi, dan arus fotolistrik pada tabung vakum (fotodioda).

KOMPONEN UTAMA:

1. Sumber Cahaya Polikromatik
   Lampu merkuri tekanan tinggi yang memancarkan spektrum cahaya tampak dan UV yang kuat.

2. Diafragma (Aperture)
   Celah lingkaran dengan ukuran variabel (misal 2mm, 4mm, 8mm).
   Fungsi: Mengatur INTENSITAS cahaya yang masuk ke detektor tanpa mengubah frekuensi.
   - Peningkatkan diameter 2x lipat akan meningkatkan intensitas (luas area) sebesar 4x lipat.

3. Filter Warna Interverensi
   Fungsi: Memilih satu panjang gelombang (FREKUENSI) spesifik dari cahaya lampu. Menentukan energi paket foton (E = hf).

4. Tabung Vakum Fotolistrik
   - Katoda peka cahaya: Melepaskan elektron saat disinari.
   - Anoda Kolektor: Menangkap elektron.

5. Rangkaian Pengukur I-V
   - Sumber Tegangan Bias Variabel: Dapat memberikan bias maju (mempercepat elektron) atau bias mundur (menghambat elektron/stopping potential).
   - Nanoammeter: Mengukur arus saturasi.

TUJUAN:
Membuktikan bahwa arus jenuh sebanding dengan intensitas (jumlah foton), sedangkan potensial penghenti (energi kinetik elektron) hanya bergantung pada frekuensi cahaya, bukan intensitasnya (Bukti sifat partikel cahaya).""",
                 "guide_title": "PETUNJUK PRAKTIKUM",
                 "guide_content": "Petunjuk Praktikum..." # I'll verify this later
            },
            "EN": {
                "title": "Photodiode Characteristics (Particle Nature of Light)",
                "tab_exp": "I-V Experiment",
                "tab_guide": "Lab Guide",
                "tab_scheme": "Apparatus Scheme & Explanation",
                "tab_diag": "Circuit Diagram",
                "header_setup": "Equipment Setup",
                "grp_optic": "Optical Components",
                "lbl_filter": "Color Filter:",
                "lbl_aper": "Aperture Diameter:",
                "grp_voltage": "Bias Voltage Source",
                "lbl_volt": "Voltage (V):",
                "lbl_coarse": "Coarse Adj (-5 to 30V)",
                "lbl_fine": "Fine Adj (+/- 1V)",
                "grp_graph": "Graph Control",
                "btn_plot": "Plot Point (Manual)",
                "btn_sweep": "Auto-Sweep (Draw Curve)",
                "btn_hold": "Save Curve (Hold)",
                "btn_clear": "Clear Graph",
                "btn_save_db": "☁️ Save (DB & Excel)",
                "graph_title": "I-V Characteristic Curve",
                "header_multi": "Multimeter",
                "lbl_current": "Photodiode Current (I)",
                "lbl_rail": "Optical Rail",
                "lbl_lamp": "Hg Lamp",
                "lbl_filter_item": "Filter",
                "lbl_aperture": "Aperture",
                "lbl_photodiode": "Photodiode",
                "lbl_unit": "Electrometer Unit",
                "lbl_current_disp": "CURRENT (nA)",
                "lbl_legend": "Graph Legend:",
                "scheme_title": "Photodiode Characteristics Apparatus Scheme",
                "scheme_content": """APPARATUS SCHEME AND EXPLANATION

This experiment studies the relationship between light intensity, frequency, and photoelectric current in a vacuum tube (photodiode).

MAIN COMPONENTS:

1. Polychromatic Light Source
   High-pressure mercury lamp emitting strong visible and UV spectrum.

2. Diaphragm (Aperture)
   Circular slit with variable size (e.g., 2mm, 4mm, 8mm).
   Function: Controls light INTENSITY entering detector without changing frequency.
   - Increasing diameter 2x increases intensity (area) by 4x.

3. Interference Color Filter
   Function: Selects specific wavelength (FREQUENCY) from lamp light. Determines photon packet energy (E = hf).

4. Photoelectric Vacuum Tube
   - Photosensitive Cathode: Releases electrons when illuminated.
   - Collector Anode: Captures electrons.

5. I-V Measurement Circuit
   - Variable Bias Voltage Source: Can provide forward bias (accelerating electrons) or reverse bias (retarding electrons/stopping potential).
   - Nanoammeter: Measures saturation current.

OBJECTIVE:
Prove that saturation current is proportional to intensity (number of photons), while stopping potential (electron kinetic energy) depends only on light frequency, not intensity (Proof of particle nature of light).""",
                 "guide_title": "LABORATORY GUIDE",
                 "guide_content": "Laboratory Guide..."
            }
        }

    def T(self, key):
        return self.translations.get(self.lang, self.translations["ID"]).get(key, key)

    def set_language(self, lang):
        self.lang = lang
        self.refresh_ui()

    def refresh_ui(self):
        # Header
        if hasattr(self, 'lbl_title'): self.lbl_title.config(text=self.T("title"))
        
        # Tabs
        if hasattr(self, 'notebook'):
            self.notebook.tab(self.tab_exp, text=self.T("tab_exp"))
            self.notebook.tab(self.tab_guide, text=self.T("tab_guide"))
            self.notebook.tab(self.tab_scheme, text=self.T("tab_scheme"))
            self.notebook.tab(self.tab_diagram, text=self.T("tab_diag"))
            
        # Expriment Tab
        if hasattr(self, 'lbl_setup_title'): self.lbl_setup_title.config(text=self.T("header_setup"))
        if hasattr(self, 'frame_setup'): self.frame_setup.config(text=self.T("grp_optic"))
        if hasattr(self, 'lbl_filter'): self.lbl_filter.config(text=self.T("lbl_filter"))
        if hasattr(self, 'lbl_aper'): self.lbl_aper.config(text=self.T("lbl_aper"))
        
        if hasattr(self, 'frame_pwr'): self.frame_pwr.config(text=self.T("grp_voltage"))
        if hasattr(self, 'lbl_volt_title'): self.lbl_volt_title.config(text=self.T("lbl_volt"))
        if hasattr(self, 'lbl_coarse'): self.lbl_coarse.config(text=self.T("lbl_coarse"))
        if hasattr(self, 'lbl_fine'): self.lbl_fine.config(text=self.T("lbl_fine"))
        
        if hasattr(self, 'frame_act'): self.frame_act.config(text=self.T("grp_graph"))
        if hasattr(self, 'btn_plot'): self.btn_plot.config(text=self.T("btn_plot"))
        if hasattr(self, 'btn_sweep'): self.btn_sweep.config(text=self.T("btn_sweep"))
        if hasattr(self, 'btn_hold'): self.btn_hold.config(text=self.T("btn_hold"))
        if hasattr(self, 'btn_clear'): self.btn_clear.config(text=self.T("btn_clear"))
        if hasattr(self, 'btn_save_db'): self.btn_save_db.config(text=self.T("btn_save_db"))
        
        if hasattr(self, 'lbl_center_title'): self.lbl_center_title.config(text=self.T("graph_title"))
        if hasattr(self, 'lbl_readings_title'): self.lbl_readings_title.config(text=self.T("header_multi"))
        if hasattr(self, 'lbl_current'): self.lbl_current.config(text=self.T("lbl_current"))
        if hasattr(self, 'lbl_legend_title'): self.lbl_legend_title.config(text=self.T("lbl_legend"))
        
        # Scheme Tab
        if hasattr(self, 'lbl_scheme'): self.lbl_scheme.config(text=self.T("scheme_title"))
        if hasattr(self, 'txt_scheme'):
             self.txt_scheme.config(state="normal")
             self.txt_scheme.delete("1.0", "end")
             self.txt_scheme.insert("1.0", self.T("scheme_content"))
             self.txt_scheme.config(state="disabled")

        # Diagram Tab (Canvas tags)
        if hasattr(self, 'canvas_diag'):
            self.canvas_diag.itemconfigure("lbl_rail", text=self.T("lbl_rail"))
            self.canvas_diag.itemconfigure("lbl_lamp", text=self.T("lbl_lamp"))
            self.canvas_diag.itemconfigure("lbl_filter_item", text=self.T("lbl_filter_item"))
            self.canvas_diag.itemconfigure("lbl_aperture", text=self.T("lbl_aperture"))
            self.canvas_diag.itemconfigure("lbl_photodiode", text=self.T("lbl_photodiode"))
            self.canvas_diag.itemconfigure("lbl_unit", text=self.T("lbl_unit"))
            self.canvas_diag.itemconfigure("lbl_current_disp", text=self.T("lbl_current_disp")) 
        
    def create_widgets(self):
        # Header
        header = tk.Frame(self, bg="#2d3436", pady=10)
        header.pack(fill="x")
        self.lbl_title = tk.Label(header, text=self.T("title"), 
                 font=("Helvetica", 18, "bold"), fg="#dfe6e9", bg="#2d3436")
        self.lbl_title.pack()
        
        # Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_exp = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_exp, text=self.T("tab_exp"))
        self.create_experiment_ui()
        
        self.tab_guide = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_guide, text=self.T("tab_guide"))
        self.create_guide_ui()

        # Tab 3: Tools Scheme
        self.tab_scheme = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_scheme, text=self.T("tab_scheme"))
        self.create_tab_scheme()

        # Tab 4: Real Diagram
        self.tab_diagram = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_diagram, text=self.T("tab_diag"))
        self.create_tab_diagram()

    def create_tab_diagram(self):
        self.canvas_diag = tk.Canvas(self.tab_diagram, bg="white")
        self.canvas_diag.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Optical Bench Setup
        self.canvas_diag.create_line(50, 300, 750, 300, width=5, fill="#95a5a6") # Rail
        self.canvas_diag.create_text(400, 320, text=self.T("lbl_rail"), font=("Arial", 10), tags="lbl_rail")
        
        # 1. Mercury Lamp
        self.canvas_diag.create_rectangle(50, 200, 150, 300, fill="#7f8c8d", outline="black")
        self.canvas_diag.create_text(100, 190, text=self.T("lbl_lamp"), font=("Arial", 11, "bold"), tags="lbl_lamp")
        
        # 2. Lens/Collimator
        self.canvas_diag.create_oval(180, 220, 200, 280, fill="#aab7b8", outline="black")
        self.canvas_diag.create_line(190, 300, 190, 280, width=4, fill="black") # Post
        
        # 3. Filter Holder
        self.canvas_diag.create_rectangle(250, 220, 270, 280, fill="#e74c3c")
        self.canvas_diag.create_line(260, 300, 260, 280, width=4, fill="black")
        self.canvas_diag.create_text(260, 200, text=self.T("lbl_filter_item"), font=("Arial", 9), tags="lbl_filter_item")
        
        # 4. Aperture (Iris)
        self.canvas_diag.create_rectangle(320, 220, 340, 280, fill="#2c3e50")
        self.canvas_diag.create_oval(325, 240, 335, 260, fill="black") # Hole
        self.canvas_diag.create_line(330, 300, 330, 280, width=4, fill="black")
        self.canvas_diag.create_text(330, 200, text=self.T("lbl_aperture"), font=("Arial", 9), tags="lbl_aperture")
        
        # 5. Photodiode Sensor
        self.canvas_diag.create_rectangle(400, 230, 480, 270, fill="#ecf0f1", outline="black")
        self.canvas_diag.create_line(440, 300, 440, 270, width=4, fill="black")
        self.canvas_diag.create_text(440, 210, text=self.T("lbl_photodiode"), font=("Arial", 10, "bold"), tags="lbl_photodiode")
        
        # 6. Measurement Unit box
        self.canvas_diag.create_rectangle(550, 150, 750, 350, fill="#2c3e50")
        self.canvas_diag.create_text(650, 370, text=self.T("lbl_unit"), font=("Arial", 11, "bold"), tags="lbl_unit")
        
        # Displays
        self.canvas_diag.create_rectangle(570, 180, 730, 230, fill="#27ae60")
        self.canvas_diag.create_text(650, 205, text=self.T("lbl_current_disp"), fill="#2ecc71", font=("Arial", 8), tags="lbl_current_disp")
        self.canvas_diag.create_text(650, 220, text="12.50", font=("Ds-Digital", 20), fill="black")
        
        # Cables
        self.canvas_diag.create_line(480, 250, 550, 250, width=3, fill="black")


    def create_tab_scheme(self):
        container = self.tab_scheme
        self.lbl_scheme = tk.Label(container, text=self.T("scheme_title"), 
                 font=("Arial", 16, "bold"), bg="#f5f6fa", fg="#2d3436")
        self.lbl_scheme.pack(pady=15)
        
        frame = tk.Frame(container, bg="white", bd=1, relief="solid")
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.txt_scheme = tk.Text(frame, font=("Arial", 12), wrap="word", padx=20, pady=20, bg="white", relief="flat")
        self.txt_scheme.pack(fill="both", expand=True)
        
        self.txt_scheme.insert("1.0", self.T("scheme_content"))
        self.txt_scheme.config(state="disabled")


    def create_experiment_ui(self):
        # Layout: Left (Controls), Center (Graph), Right (Data/Readings)
        main_layout = tk.Frame(self.tab_exp, bg="#f5f6fa")
        main_layout.pack(fill="both", expand=True, padx=5, pady=5)
        
        # --- Left Panel: Controls ---
        left_panel = tk.Frame(main_layout, width=300, bg="white", relief="raised", bd=1)
        left_panel.pack(side="left", fill="y", padx=5)
        
        self.lbl_setup_title = tk.Label(left_panel, text=self.T("header_setup"), font=("Arial", 14, "bold"), bg="white")
        self.lbl_setup_title.pack(pady=10)
        
        # Setup Frame
        self.frame_setup = tk.LabelFrame(left_panel, text=self.T("grp_optic"), bg="white", font=("Arial", 10, "bold"))
        self.frame_setup.pack(fill="x", padx=10, pady=10)
        
        # Filter Selection
        self.lbl_filter = tk.Label(self.frame_setup, text=self.T("lbl_filter"), bg="white")
        self.lbl_filter.pack(anchor="w", padx=10)
        self.filter_var = tk.StringVar(value="Biru (436 nm)")
        cb_filter = ttk.Combobox(self.frame_setup, textvariable=self.filter_var, values=list(self.filters.keys()), state="readonly")
        cb_filter.pack(fill="x", padx=10, pady=5)
        cb_filter.bind("<<ComboboxSelected>>", self.update_params)
        
        # Aperture Selection
        self.lbl_aper = tk.Label(self.frame_setup, text=self.T("lbl_aper"), bg="white")
        self.lbl_aper.pack(anchor="w", padx=10)
        self.aper_var = tk.StringVar(value="2 mm (Low)")
        cb_aper = ttk.Combobox(self.frame_setup, textvariable=self.aper_var, values=list(self.apertures.keys()), state="readonly")
        cb_aper.pack(fill="x", padx=10, pady=5)
        cb_aper.bind("<<ComboboxSelected>>", self.update_params)
        
        # Variable Voltage Source
        self.frame_pwr = tk.LabelFrame(left_panel, text=self.T("grp_voltage"), bg="white", font=("Arial", 10, "bold"))
        self.frame_pwr.pack(fill="x", padx=10, pady=20)
        
        # Voltage Slider (-2 to 30)
        self.volt_var = tk.DoubleVar(value=0.0)
        
        self.lbl_volt_title = tk.Label(self.frame_pwr, text=self.T("lbl_volt"), bg="white")
        self.lbl_volt_title.pack()
        self.lbl_volt = tk.Label(self.frame_pwr, text="0.00 V", font=("Ds-Digital", 20), fg="red", bg="black")
        self.lbl_volt.pack(pady=5, fill="x", padx=20)

        # Fine and Coarse Sliders
        self.lbl_coarse = tk.Label(self.frame_pwr, text=self.T("lbl_coarse"), bg="white", font=("Arial", 8))
        self.lbl_coarse.pack()
        tk.Scale(self.frame_pwr, from_=-5, to=30, orient="horizontal", variable=self.volt_var, 
                 command=self.update_reading, bg="white").pack(fill="x", padx=10)
                 
        self.lbl_fine = tk.Label(self.frame_pwr, text=self.T("lbl_fine"), bg="white", font=("Arial", 8))
        self.lbl_fine.pack()
        self.fine_var = tk.DoubleVar(value=0.0)
        tk.Scale(self.frame_pwr, from_=-1.0, to=1.0, resolution=0.01, orient="horizontal", 
                 variable=self.fine_var, command=self.update_reading, bg="white").pack(fill="x", padx=10)

        # Actions
        self.frame_act = tk.LabelFrame(left_panel, text=self.T("grp_graph"), bg="white", font=("Arial", 10, "bold"))
        self.frame_act.pack(fill="x", padx=10, pady=20)
        
        self.btn_plot = tk.Button(self.frame_act, text=self.T("btn_plot"), command=self.plot_point, 
                  bg="#3498db", fg="black")
        self.btn_plot.pack(fill="x", padx=10, pady=5)
                  
        self.btn_sweep = tk.Button(self.frame_act, text=self.T("btn_sweep"), command=self.auto_sweep, 
                  bg="#e67e22", fg="black")
        self.btn_sweep.pack(fill="x", padx=10, pady=5)
                  
        self.btn_hold = tk.Button(self.frame_act, text=self.T("btn_hold"), command=self.save_trace, 
                  bg="#27ae60", fg="black")
        self.btn_hold.pack(fill="x", padx=10, pady=5)
        
        self.btn_clear = tk.Button(self.frame_act, text=self.T("btn_clear"), command=self.clear_graph,
                  bg="#c0392b", fg="black")
        self.btn_clear.pack(fill="x", padx=10, pady=5)

        self.btn_save_db = tk.Button(self.frame_act, text=self.T("btn_save_db"), command=self.save_to_all, 
                  bg="#27ae60", fg="black")
        self.btn_save_db.pack(fill="x", padx=10, pady=5)

        # --- Center Panel: Graph ---
        center_panel = tk.Frame(main_layout, bg="white", relief="sunken", bd=1)
        center_panel.pack(side="left", fill="both", expand=True, padx=5)
        
        self.lbl_center_title = tk.Label(center_panel, text=self.T("graph_title"), font=("Arial", 12, "bold"), bg="white")
        self.lbl_center_title.pack(pady=5)
        self.canvas_graph = tk.Canvas(center_panel, bg="white")
        self.canvas_graph.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas_graph.bind("<Configure>", self.draw_grid)
        
        # --- Right Panel: Readings ---
        right_panel = tk.Frame(main_layout, width=200, bg="white", relief="raised", bd=1)
        right_panel.pack(side="right", fill="y", padx=5)
        
        self.lbl_readings_title = tk.Label(right_panel, text=self.T("header_multi"), font=("Arial", 14, "bold"), bg="white")
        self.lbl_readings_title.pack(pady=10)
        
        # Ammeter Display
        mm_frame = tk.Frame(right_panel, bg="#2d3436", bd=5, relief="raised")
        mm_frame.pack(padx=10, pady=10)
        
        self.lbl_current = tk.Label(mm_frame, text=self.T("lbl_current"), fg="white", bg="#2d3436")
        self.lbl_current.pack()
        self.lbl_amp = tk.Label(mm_frame, text="00.00", font=("Courier New", 28, "bold"), fg="#00ff00", bg="black")
        self.lbl_amp.pack(padx=10, pady=5)
        tk.Label(mm_frame, text="x 10^-11 A", fg="white", bg="#2d3436").pack()
        
        # Legend
        self.lbl_legend_title = tk.Label(right_panel, text=self.T("lbl_legend"), font=("Arial", 10, "bold"), bg="white")
        self.lbl_legend_title.pack(pady=(20,5))
        self.legend_frame = tk.Frame(right_panel, bg="white")
        self.legend_frame.pack(fill="x", padx=10)

    def create_guide_ui(self):
        txt = tk.Text(self.tab_guide, font=("Arial", 12), padx=20, pady=20, wrap="word")
        txt.pack(fill="both", expand=True)
        content = """
PETUNJUK PRAKTIKUM SIFAT PARTIKEL CAHAYA

A. TUJUAN
Mempelajari karakteristik fotodioda dan membuktikan sifat partikel cahaya melalui hubungan kurva I-V.

B. TEORI SINGKAT
1. Cahaya terdiri dari paket energi (Foton) dengan E = h*f.
2. Efek Fotolistrik terjadi saat energi foton mampu melepaskan elektron dari katoda.
3. Arus Saturasi (I_max) bergantung pada INTENSITAS (jumlah foton).
4. Potensial Penghenti (V_stop) bergantung pada FREKUENSI/WARNA (energi per foton), bukan intensitas.

C. PROSEDUR 1: VARIASI INTENSITAS
1. Pilih Filter "Biru (436 nm)".
2. Pilih Aperture "2 mm" (Intensitas Rendah).
3. Klik "Auto-Sweep" untuk menggambar kurva I-V.
4. Klik "Simpan Kurva" untuk menahan grafik.
5. Ubah Aperture ke "4 mm" dan "8 mm", lakukan sweep dan simpan lagi.
6. Amati: Apakah V_stop (titik potong sumbu X negatif) berubah? Apakah tinggi kurva (saturasi) berubah?

D. PROSEDUR 2: VARIASI FREKUENSI
1. Hapus Grafik.
2. Pasang Aperture "4 mm".
3. Pilih Filter "Biru", lakukan Sweep, Simpan.
4. Ganti ke filter "Hijau", lakukan Sweep, Simpan.
5. Ganti ke filter "Kuning", lakukan Sweep, Simpan.
6. Amati: Kurva mana yang membutuhkan tegangan negatif paling besar (paling kiri) untuk menghentikan arus?

E. PENYIMPANAN DATA
Klik tombol "☁️ Simpan (DB & Excel)" di tab kiri bawah untuk menyimpan data kurva dan hasil eksperimen.
"""
        txt.insert("1.0", content)
        txt.config(state="disabled")

    def update_params(self, event=None):
        f_name = self.filter_var.get()
        a_name = self.aper_var.get()
        
        self.current_nm = self.filters[f_name]
        self.current_aperture_scale = self.apertures[a_name]
        
        # Set active trace color based on filter
        if "Biru" in f_name: self.active_trace_color = "blue"
        elif "Hijau" in f_name: self.active_trace_color = "green"
        elif "Kuning" in f_name: self.active_trace_color = "#f1c40f" # Dark yellow
        
        self.update_reading()

    def calculate_physics(self, voltage):
        # Physics Logic (Same as original script but localized)
        freq = self.c / (self.current_nm * 1e-9)
        E_photon = self.h * freq
        K_max = E_photon - self.W0_J
        
        V_stop = K_max / self.e
        
        I_sat_base = 5.0 # in 10^-11 A unit effectively
        I_sat = I_sat_base * self.current_aperture_scale
        
        if voltage < -V_stop:
            curr = 0.0
        else:
            V_eff = voltage - (-V_stop)
            # Sigmoid/Exponential approach to saturation
            curr = I_sat * (1 - math.exp(-1.5 * V_eff))
            if curr < 0: curr = 0
            # Past 5V roughly flat
            if voltage > 5.0:
                slope = 0.01 * I_sat # Slight slope due to experimental imperfections
                curr = I_sat + (voltage - 5.0) * slope

        noise = random.uniform(-0.05, 0.05)
        return max(0.0, curr + noise)

    def update_reading(self, val=None):
        # Combined voltage
        v_coarse = self.volt_var.get()
        v_fine = self.fine_var.get()
        self.voltage = v_coarse + v_fine
        
        self.lbl_volt.config(text=f"{self.voltage:.2f} V")
        
        self.measured_current = self.calculate_physics(self.voltage)
        self.lbl_amp.config(text=f"{self.measured_current:.2f}")
    
    def plot_point(self):
        self.trace_data.append((self.voltage, self.measured_current))
        self.draw_plot()
        
    def auto_sweep(self):
        # Quickly calculate points from -2 to +10 roughly
        self.trace_data = []
        
        # Range 1: -3 to 0 (Fine steps for V_stop)
        v = -3.0
        while v <= 0:
            i = self.calculate_physics(v)
            self.trace_data.append((v, i))
            v += 0.1
            
        # Range 2: 0 to 30 (Coarse)
        v = 0.5
        while v <= 30.0:
            i = self.calculate_physics(v)
            self.trace_data.append((v, i))
            v += 1.0 # Step 1V
            
        self.draw_plot()

    def get_data(self):
        export = []
        # Add saved traces
        for trace in self.saved_traces:
            lbl = trace["label"]
            for v, i in trace["data"]:
                export.append({
                    "Modul": "Sifat Partikel Cahaya",
                    "Label": lbl,
                    "Voltage (V)": f"{v:.2f}",
                    "Current (nA)": f"{i:.2f}"
                })
        
        # Add active trace if any
        if self.trace_data:
            lbl = "Unsaved Trace"
            for v, i in self.trace_data:
                export.append({
                    "Modul": "Sifat Partikel Cahaya",
                    "Label": lbl,
                    "Voltage (V)": f"{v:.2f}",
                    "Current (nA)": f"{i:.2f}"
                })
        
        return export

    def save_trace(self):
        lbl = f"{self.filter_var.get().split(' ')[0]} - {self.aper_var.get().split(' ')[0]}"
        trace = {
            "label": lbl,
            "color": self.active_trace_color,
            "data": list(self.trace_data)
        }
        self.saved_traces.append(trace)
        self.trace_data = [] # Clear active
        self.draw_plot()
        self.update_legend()
        
    def clear_graph(self):
        self.saved_traces = []
        self.trace_data = []
        self.draw_plot()
        self.update_legend()

    def save_to_all(self):
        data = self.get_data()
        success, msg = DataManager.save_data_unified(data, "SifatCahaya")
        if success:
            messagebox.showinfo("Status Penyimpanan", msg)
        else:
            messagebox.showwarning("Status Penyimpanan", msg)

    def get_data(self):
        export_data = []
        # If there are saved traces
        for trace in self.saved_traces:
            lbl = trace.get('label', 'Trace')
            for (v, i) in trace.get('data', []):
                export_data.append({
                    "Trace Label": lbl,
                    "Voltage (V)": v,
                    "Current (nA)": i
                })
        
        # Also include current trace if not empty
        if self.trace_data:
             for (v, i) in self.trace_data:
                export_data.append({
                    "Trace Label": "Current Trace",
                    "Voltage (V)": v,
                    "Current (nA)": i
                })
        # If no traces but we have points? I assume trace_data covers it.
        return export_data
        
    def update_legend(self):
        for w in self.legend_frame.winfo_children(): w.destroy()
        
        for t in self.saved_traces:
            f = tk.Frame(self.legend_frame, bg="white")
            f.pack(fill="x")
            tk.Label(f, text="◼", fg=t['color'], bg="white").pack(side="left")
            tk.Label(f, text=t['label'], bg="white", font=("Arial", 9)).pack(side="left")

    def draw_grid(self, event=None):
        self.draw_plot()

    def draw_plot(self):
        self.canvas_graph.delete("all")
        w = self.canvas_graph.winfo_width()
        h = self.canvas_graph.winfo_height()
        if w < 50: return # too small
        
        padding = 40
        
        # Axis Ranges
        min_x, max_x = -3.0, 30.0
        min_y, max_y = 0.0, 100.0 # scale for current (max aperture=16 * 5 = 80 + bits)
        
        # Transform functions
        def to_scr_x(x):
            return padding + ((x - min_x) / (max_x - min_x)) * (w - 2*padding)
        def to_scr_y(y):
            return (h - padding) - ((y - min_y) / (max_y - min_y)) * (h - 2*padding)
            
        # Draw Axes
        origin_x = to_scr_x(0)
        origin_y = to_scr_y(0)
        
        # X Axis (Voltage)
        self.canvas_graph.create_line(padding, origin_y, w-padding, origin_y, width=2)
        # Y Axis (Current)
        self.canvas_graph.create_line(origin_x, h-padding, origin_x, padding, width=2)
        
        # Ticks & Grid
        # X Ticks (every 5V)
        for i in range(-5, 35, 5):
            if i < min_x or i > max_x: continue
            x = to_scr_x(i)
            self.canvas_graph.create_line(x, origin_y-3, x, origin_y+3)
            self.canvas_graph.create_text(x, origin_y+15, text=str(i))
            # Grid
            self.canvas_graph.create_line(x, padding, x, h-padding, fill="#eeeeee", dash=(2,2))
            
        # Y Ticks (every 20)
        for i in range(0, 120, 20):
            y = to_scr_y(i)
            self.canvas_graph.create_line(origin_x-3, y, origin_x+3, y)
            self.canvas_graph.create_text(origin_x-20, y, text=str(i))
            # Grid
            self.canvas_graph.create_line(padding, y, w-padding, y, fill="#eeeeee", dash=(2,2))
            
        # Label Axes
        self.canvas_graph.create_text(w-padding, origin_y-15, text="V (Volt)", anchor="e")
        self.canvas_graph.create_text(origin_x+10, padding, text="I (nA)", anchor="w")
        
        # Plot Saved Traces
        for trace in self.saved_traces:
            pts = []
            for vx, iy in trace['data']:
                pts.append(to_scr_x(vx))
                pts.append(to_scr_y(iy))
            if len(pts) >= 4:
                self.canvas_graph.create_line(pts, fill=trace['color'], width=2, smooth=True)
                
        # Plot Active Trace
        if len(self.trace_data) > 0:
            pts = []
            for vx, iy in self.trace_data:
                pts.append(to_scr_x(vx))
                pts.append(to_scr_y(iy))
                # Draw dots
                sx, sy = to_scr_x(vx), to_scr_y(iy)
                self.canvas_graph.create_oval(sx-2, sy-2, sx+2, sy+2, fill=self.active_trace_color, outline="")
                
            if len(pts) >= 4:
                self.canvas_graph.create_line(pts, fill=self.active_trace_color, width=2, dash=(4,2))

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabSifatCahaya(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
