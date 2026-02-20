import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from virtual_lab_data_manager import DataManager, ScrollableFrame

class VirtualLabMilikan(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#f5f6fa")
        
        # --- Constants from Original Script ---
        self.g = 9.807            # m/s^2
        self.rho_oil = 875.0      # kg/m^3
        self.rho_air = 1.204      # kg/m^3
        self.viskositas = 1.83e-5 # kg/m.s
        self.e_real = 1.602e-19   # C
        
        self.d_plate = 7.67e-3    # Distance between plates (m)
        self.grid_dist = 0.5e-3   # Distance of 1 grid line (m)
        
        # State
        self.voltage = 0.0
        self.is_running = False
        self.drops = []  # List of dicts: {id, r, q, y, x, color}
        self.next_drop_id = 0
        self.active_drop = None
        
        self.stopwatch_running = False
        self.stopwatch_start_time = 0.0
        self.stopwatch_elapsed = 0.0
        
        self.data_store = [] # List of (V, t_fall, t_rise, calculated_q)
        
        self.lang = "ID"
        self.setup_translations()
        
        self.create_widgets()
        self.running = True
        self.animation_loop()

    def start_animation(self):
        if not self.running:
            self.running = True
            self.animation_loop()

    def stop_animation(self):
        self.running = False

    def setup_translations(self):
        self.translations = {
            "ID": {
                "title": "Laboratorium Tetes Minyak Millikan",
                "tab_exp": "Eksperimen (Mikroskop)",
                "tab_data": "Analisis Data",
                "tab_guide": "Petunjuk Praktikum",
                "tab_scheme": "Skema Alat & Penjelasan",
                "tab_diagram": "Gambaran Rangkaian Alat",
                "header_control": "Kontrol Eksperimen",
                "grp_oil": "1. Tetesan Minyak",
                "btn_spray": "Semprotkan Minyak (Nebulizer)",
                "btn_clear": "Hapus Semua Tetesan",
                "grp_voltage": "2. Tegangan Plat (V)",
                "grp_stopwatch": "3. Stopwatch",
                "btn_start_stop": "Start / Stop",
                "btn_reset_sw": "Reset",
                "grp_data": "4. Data Recording",
                "btn_record": "Rekam Data (Saat Naik & Turun Selesai)",
                "mic_view": "Pandangan Mikroskop",
                "header_analysis": "Tabel Data Pengamatan",
                "col_volt": "Tegangan (V)",
                "col_t_fall": "t jatuh (s)",
                "col_t_rise": "t naik (s)",
                "col_q_calc": "Muatan (C)",
                "btn_calc_e": "Hitung Muatan Elementer (e)",
                "btn_export": "Simpan ke Database & Excel",
                "btn_reset_data": "Hapus Data",
                "lbl_result": "Hasil Perhitungan:\nMuatan rata-rata (q_avg) = ... C\nPerkiraan n = ...\nNilai e (eksperimen) = ... C\nError = ... %",
                "msg_no_data": "Belum ada data yang direkam.",
                "title_guide": "PETUNJUK PRAKTIKUM TETES MINYAK MILLIKAN",
                "guide_content": """PETUNJUK PRAKTIKUM TETES MINYAK MILLIKAN

A. TUJUAN
Menentukan muatan elementer elektron (e) dengan mengamati gerak tetes minyak dalam medan listrik.

B. CALIBRATION & SPEC
- Jarak antar plat (d) : 7.67 mm
- Jarak antar garis grid : 0.5 mm
- Densitas Minyak : 875 kg/m^3
- Viskositas Udara : 1.83e-5 kg/m.s

C. LANGKAH PERCOBAAN
1. Semprotkan Minyak:
   Klik "Semprotkan Minyak". Anda akan melihat titik-titik kecil jatuh perlahan karena gravitasi.
   
2. Pilih Satu Tetesan:
   Fokuskan perhatian pada satu tetesan spesifik. Tunggu hingga stabil.

3. Ukur Gerak Jatuh (Gravitasi saja, V=0):
   - Pastikan Tegangan 0 Volt.
   - Gunakan Stopwatch untuk mengukur waktu (t_fall) tetesan menempuh 1 skala grid (0.5 mm) atau lebih.
   - Ideal-nya ukur jarak 1 grid (0.5 mm).

4. Ukur Gerak Naik (Medan Listrik, V > 0):
   - Naikkan tegangan slider hingga tetesan berhenti atau naik.
   - Atur tegangan agar tetesan naik dengan kecepatan stabil.
   - Ukur waktu (t_rise) untuk menempuh jarak yang sama (misal 1 grid).

5. Masukkan Data:
   - Klik "Catat Data ke Tabel" dan masukkan nilai t_fall, t_rise, dan jarak tempuh.
   - Tegangan akan terisi otomatis dari setting terakhir.

6. Analisis:
   - Pindah ke tab Analisis.
   - Hitung nilai q untuk setiap pengukuran.
   - Cari nilai e dari kumpulan data q (q = n * e).

7. Simpan Data:
   - Klik tombol "Simpan (Cloud)" di tab Analisis.
   - Data akan tersimpan ke Excel (Hasil_Praktikum) dan Database Online.""",
                "polarity_normal": "Polaritas: Plat Atas (+)",
                "polarity_reverse": "Polaritas: Plat Atas (-)",
                "quick_input": "Input Cepat:",
                "reset_all": "RESET TOTAL",
                "table_no": "No",
                "table_n": "n (approx)",
                "graph_title": "Distribusi Muatan (q)",
                "graph_y": "Muatan (C)",
                "est_e_result": "Estimasi e = {val}",
                "save_cloud": "Simpan (Cloud)",
                "delete_data": "Hapus Data",
                "calc_charge": "Hitung Muatan (q)",
                "reset": "Reset",
                "msg_error": "Error",
                "msg_input_error": "Input harus angka!",
                "msg_warning": "Peringatan",
                "msg_no_data_save": "Belum ada data untuk disimpan.",
                "msg_success": "Sukses",
                "msg_save_success": "Data berhasil disimpan!",
                "msg_save_fail": "Gagal menyimpan data:",
                "msg_reset_confirm_title": "Reset Total",
                "msg_reset_confirm_body": "Apakah Anda yakin ingin mereset semua data dan simulasi?",
                "msg_reset_info": "Simulasi telah di-reset.",
                "popup_title_record": "Catat Data",
                "lbl_volt_now": "Tegangan Saat Ini: {val} V",
                "lbl_t_fall_input": "Waktu Jatuh (s) [V=0]:",
                "lbl_t_rise_input": "Waktu Naik (s) [V>0]:",
                "lbl_dist_input": "Jarak Tempuh (unit grid) [0.5 mm]:",
                "btn_save_popup": "Simpan",
                "graph_x": "Data #",
            },
            "EN": {
                "title": "Millikan Oil Drop Laboratory",
                "tab_exp": "Experiment (Microscope)",
                "tab_data": "Data Analysis",
                "tab_guide": "Laboratory Guide",
                "tab_scheme": "Equipment Scheme & Explanation",
                "tab_diagram": "Apparatus Diagram",
                "header_control": "Experiment Control",
                "grp_oil": "1. Oil Droplets",
                "btn_spray": "Spray Oil (Nebulizer)",
                "btn_clear": "Clear All Droplets",
                "grp_voltage": "2. Plate Voltage (V)",
                "grp_stopwatch": "3. Stopwatch",
                "btn_start_stop": "Start / Stop",
                "btn_reset_sw": "Reset",
                "grp_data": "4. Data Recording",
                "btn_record": "Record Data (After Rise & Fall)",
                "mic_view": "Microscope View",
                "header_analysis": "Observation Data Table",
                "col_volt": "Voltage (V)",
                "col_t_fall": "t fall (s)",
                "col_t_rise": "t rise (s)",
                "col_q_calc": "Charge (C)",
                "btn_calc_e": "Calculate Elementary Charge (e)",
                "btn_export": "Save to Database & Excel",
                "btn_reset_data": "Clear Data",
                "lbl_result": "Calculation Result:\nAverage Charge (q_avg) = ... C\nEstimated n = ...\nValue e (experiment) = ... C\nError = ... %",
                "msg_no_data": "No data recorded yet.",
                "title_guide": "MILLIKAN OIL DROP LAB GUIDE",
                 "guide_content": """MILLIKAN OIL DROP LAB GUIDE

A. OBJECTIVE
Determine the elementary charge of an electron (e) by observing oil drop motion in an electric field.

B. CALIBRATION & SPEC
- Plate Distance (d) : 7.67 mm
- Grid line distance : 0.5 mm
- Oil Density : 875 kg/m^3
- Air Viscosity : 1.83e-5 kg/m.s

C. EXPERIMENT STEPS
1. Spray Oil:
   Click "Spray Oil". You will see small dots falling slowly due to gravity.

2. Select One Droplet:
   Focus on one specific droplet. Wait for it to stabilize.

3. Measure Fall (Gravity only, V=0):
   - Ensure Voltage is 0 Volt.
   - Use Stopwatch to measure time (t_fall) for the drop to travel 1 grid scale (0.5 mm) or more.
   - Ideally measure 1 grid distance (0.5 mm).

4. Measure Rise (Electric Field, V > 0):
   - Increase voltage using the slider until the drop stops or rises.
   - Adjust voltage so the drop rises with steady speed.
   - Measure time (t_rise) to travel the same distance (e.g., 1 grid).

5. Enter Data:
   - Click "Record Data" and input t_fall, t_rise, and distance traveled.
   - Voltage will be auto-filled from the last setting.

6. Analysis:
   - Go to Analysis tab.
   - Calculate q for each measurement.
   - Find e from the collection of q values (q = n * e).

7. Save Data:
   - Click "Save (Cloud)" in Analysis tab.
   - Data will be saved to Excel (Hasil_Praktikum) and Online Database.""",
                "polarity_normal": "Polarity: Top Plate (+)",
                "polarity_reverse": "Polarity: Top Plate (-)",
                "quick_input": "Quick Input:",
                "reset_all": "RESET ALL",
                "table_no": "No",
                "table_n": "n (approx)",
                "graph_title": "Charge Distribution (q)",
                "graph_y": "Charge (C)",
                "est_e_result": "Estimated e = {val}",
                "save_cloud": "Save (Cloud)",
                "delete_data": "Delete Data",
                "calc_charge": "Calculate Charge (q)",
                "reset": "Reset",
                "msg_error": "Error",
                "msg_input_error": "Input must be a number!",
                "msg_warning": "Warning",
                "msg_no_data_save": "No data to save.",
                "msg_success": "Success",
                "msg_save_success": "Data saved successfully!",
                "msg_save_fail": "Failed to save data:",
                "msg_reset_confirm_title": "Reset All",
                "msg_reset_confirm_body": "Are you sure you want to reset all data and simulation?",
                "msg_reset_info": "Simulation has been reset.",
                "popup_title_record": "Record Data",
                "lbl_volt_now": "Current Voltage: {val} V",
                "lbl_t_fall_input": "Fall Time (s) [V=0]:",
                "lbl_t_rise_input": "Rise Time (s) [V>0]:",
                "lbl_dist_input": "Distance (grid units) [0.5 mm]:",
                "btn_save_popup": "Save",
                "graph_x": "Data #",
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
            self.notebook.tab(self.tab_exp, text=self.T("tab_exp"))
            self.notebook.tab(self.tab_data, text=self.T("tab_data"))
            self.notebook.tab(self.tab_guide, text=self.T("tab_guide"))
            self.notebook.tab(self.tab_scheme, text=self.T("tab_scheme"))
            self.notebook.tab(self.tab_diagram, text=self.T("tab_diagram"))
        
        # Experiment Tab
        if hasattr(self, 'lbl_control_title'): self.lbl_control_title.config(text=self.T("header_control"))
        if hasattr(self, 'frame_oil'): self.frame_oil.config(text=self.T("grp_oil"))
        if hasattr(self, 'btn_spray'): self.btn_spray.config(text=self.T("btn_spray"))
        if hasattr(self, 'btn_clear'): self.btn_clear.config(text=self.T("btn_clear"))
        
        if hasattr(self, 'frame_volt'): self.frame_volt.config(text=self.T("grp_voltage"))
        if hasattr(self, 'btn_polarity') and hasattr(self, 'polar_var'): 
            key = "polarity_normal" if self.polar_var.get() == "Normal" else "polarity_reverse"
            self.btn_polarity.config(text=self.T(key))
            
        if hasattr(self, 'frame_timer'): self.frame_timer.config(text=self.T("grp_stopwatch"))
        if hasattr(self, 'btn_start_stop'): self.btn_start_stop.config(text=self.T("btn_start_stop"))
        if hasattr(self, 'btn_reset_timer'): self.btn_reset_timer.config(text=self.T("btn_reset_sw"))
        
        if hasattr(self, 'lbl_quick_input'): self.lbl_quick_input.config(text=self.T("quick_input"))
        if hasattr(self, 'btn_record'): self.btn_record.config(text=self.T("btn_record"))
        if hasattr(self, 'btn_reset_all'): self.btn_reset_all.config(text=self.T("reset_all"))
        if hasattr(self, 'lbl_microscope'): self.lbl_microscope.config(text=self.T("mic_view"))
        
        # Analysis Tab
        if hasattr(self, 'tree') and hasattr(self, 'cols'):
            # zip cols: No, Voltage, t_fall, t_rise, q, n
            # KEYS: table_no, col_volt, col_t_fall, col_t_rise, col_q_calc, table_n
            key_list = ["table_no", "col_volt", "col_t_fall", "col_t_rise", "col_q_calc", "table_n"]
            for col, key in zip(self.cols, key_list):
                 self.tree.heading(col, text=self.T(key))
            
        if hasattr(self, 'btn_calc'): self.btn_calc.config(text=self.T("btn_calc_e"))
        if hasattr(self, 'btn_del'): self.btn_del.config(text=self.T("btn_reset_data"))
        if hasattr(self, 'btn_save'): self.btn_save.config(text=self.T("btn_export"))

        if hasattr(self, 'ax'):
            self.ax.set_title(self.T("graph_title"))
            self.ax.set_ylabel(self.T("graph_y"))
            self.graph_canvas.draw()
            
        if hasattr(self, 'txt_guide'):
             self.txt_guide.config(state="normal")
             self.txt_guide.delete("1.0", "end")
             self.txt_guide.insert("1.0", self.T("guide_content"))
             self.txt_guide.config(state="disabled")
        
    def create_widgets(self):
        # Header
        header = tk.Frame(self, bg="#2c3e50", pady=10)
        header.pack(fill="x")
        self.lbl_title = tk.Label(header, text=self.T("title"), 
                 font=("Helvetica", 18, "bold"), fg="#ecf0f1", bg="#2c3e50")
        self.lbl_title.pack()
        
        # Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Experiment (FULL TAB, NO SCROLL)
        self.tab_exp = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_exp, text=self.T("tab_exp"))
        self.create_experiment_ui()
        
        # Tab 2: Analysis (FULL TAB, NO SCROLL)
        self.tab_data = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab_data, text=self.T("tab_data"))
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
        canvas = tk.Canvas(self.tab_diagram, bg="#fdfefe")
        canvas.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Floor/Bench
        canvas.create_rectangle(0, 420, 800, 500, fill="#8e8e8e", outline="")
        canvas.create_line(0, 420, 800, 420, fill="#696969", width=3)
        
        # Main Chamber (3D box with perspective)
        # Front face
        canvas.create_rectangle(200, 220, 480, 400, fill="#95a5a6", outline="#5d6d7e", width=3)
        # Top face
        canvas.create_polygon(200, 220, 480, 220, 500, 200, 220, 200, 
                            fill="#bdc3c7", outline="#5d6d7e", width=2)
        # Side face
        canvas.create_polygon(480, 220, 500, 200, 500, 380, 480, 400, 
                            fill="#7f8c8d", outline="#5d6d7e", width=2)
        
        # Glass viewing window
        for i in range(3):
            canvas.create_rectangle(230+i*2, 250+i*2, 370-i*2, 370-i*2, 
                                  fill="#d6eaf8", outline="#85c1e9", width=2-i)
        canvas.create_text(300, 260, text="Viewing Window", font=("Arial", 8), fill="#2c3e50")
        
        # Internal plates with electric field indicators
        # Top plate (positive)
        canvas.create_rectangle(240, 280, 450, 285, fill="#e74c3c", outline="")
        for x in range(260, 440, 30):
            canvas.create_line(x, 285, x, 300, fill="#e74c3c", arrow="last", width=2)
        canvas.create_text(390, 270, text="HV (+)", font=("Arial", 9, "bold"), fill="#e74c3c")
        
        # Bottom plate (ground)
        canvas.create_rectangle(240, 340, 450, 345, fill="#2c3e50", outline="")
        canvas.create_text(390, 355, text="GND", font=("Arial", 9, "bold"), fill="#2c3e50")
        
        # Oil droplets (scattered)
        import random
        for _ in range(8):
            x = random.randint(250, 360)
            y = random.randint(290, 335)
            canvas.create_oval(x-2, y-2, x+2, y+2, fill="#f39c12", outline="#d68910")
        
        # Microscope (3D perspective)
        # Objective lens housing
        canvas.create_polygon(480, 300, 520, 295, 520, 325, 480, 330, 
                            fill="#34495e", outline="#2c3e50", width=2)
        # Tube body with gradient effect
        for i in range(10):
            shade = 52 + i*8
            color = f"#{shade:02x}{shade+10:02x}{shade+20:02x}"
            canvas.create_rectangle(520, 295-i*5, 600, 325-i*5, fill=color, outline="")
        # Eyepiece
        canvas.create_oval(595, 240, 625, 260, fill="#7f8c8d", outline="#5d6d7e", width=2)
        canvas.create_oval(600, 243, 620, 257, fill="#2c3e50", outline="")
        
        # Focus knob
        canvas.create_oval(515, 305, 535, 325, fill="#95a5a6", outline="#7f8c8d", width=2)
        canvas.create_line(525, 315, 533, 307, fill="white", width=2)
        
        # Microscope stand
        canvas.create_rectangle(555, 330, 565, 420, fill="#5d6d7e", outline="#34495e", width=2)
        canvas.create_rectangle(540, 410, 580, 425, fill="#7f8c8d", outline="#5d6d7e", width=2)
        
        canvas.create_text(610, 340, text="Viewing\nMicroscope\n(40x)", 
                         font=("Arial", 9), fill="#2c3e50")
        
        # Light Source (LED illuminator)
        # Housing
        canvas.create_rectangle(120, 280, 200, 340, fill="#34495e", outline="#2c3e50", width=2)
        canvas.create_text(160, 295, text="LED", font=("Arial", 8, "bold"), fill="white")
        # Lens
        canvas.create_oval(140, 305, 180, 325, fill="#f1c40f", outline="#f39c12", width=2)
        canvas.create_oval(150, 310, 170, 320, fill="#fff9e6", outline="")
        # Light beam
        for i in range(4):
            canvas.create_line(200, 310-i*5, 230, 310-i*10, fill="#fff9c4", width=3, 
                             stipple="gray50")
        canvas.create_line(200, 310, 240, 310, fill="yellow", dash=(2,2), arrow="last", width=2)
        
        # Atomizer Spray Bulb (3D)
        # Rubber bulb
        canvas.create_oval(300, 140, 360, 200, fill="#d35400", outline="#a04000", width=2)
        # Highlight
        canvas.create_oval(315, 150, 330, 165, fill="#e67e22", outline="")
        # Nozzle tube
        canvas.create_polygon(325, 200, 335, 200, 332, 220, 328, 220, 
                            fill="#7f8c8d", outline="#5d6d7e", width=2)
        # Spray particles
        for i in range(5):
            canvas.create_oval(327+i*3, 218+i*8, 332+i*3, 223+i*8, 
                             fill="#f39c12", outline="", stipple="gray50")
        
        canvas.create_text(380, 165, text="Oil\nAtomizer", font=("Arial", 9), fill="#2c3e50")
        
        # High Voltage Power Supply (Bench unit with 3D effect)
        # Main body
        canvas.create_rectangle(550, 80, 750, 220, fill="#2c3e50", outline="#1a252f", width=3)
        # Top face
        canvas.create_polygon(550, 80, 750, 80, 770, 60, 570, 60, 
                            fill="#34495e", outline="#1a252f", width=2)
        # Side face
        canvas.create_polygon(750, 80, 770, 60, 770, 200, 750, 220, 
                            fill="#1a252f", outline="#1a252f", width=2)
        
        # Front panel
        canvas.create_text(650, 95, text="HIGH VOLTAGE SUPPLY", 
                         font=("Arial", 11, "bold"), fill="#2ecc71")
        
        # Digital display
        canvas.create_rectangle(570, 110, 730, 155, fill="#000000", outline="#3498db", width=2)
        canvas.create_text(650, 125, text="500.0 V", font=("Courier", 26, "bold"), fill="#e74c3c")
        canvas.create_text(650, 145, text="DC OUTPUT", font=("Arial", 8), fill="#2ecc71")
        
        # Control panel
        # Voltage adjust knob
        canvas.create_oval(575, 170, 615, 210, fill="#7f8c8d", outline="#5d6d7e", width=2)
        canvas.create_oval(580, 175, 610, 205, fill="#95a5a6", outline="")
        canvas.create_line(595, 190, 605, 178, fill="white", width=3)
        canvas.create_text(595, 215, text="VOLT", font=("Arial", 7, "bold"), fill="white")
        
        # On/Off switch
        canvas.create_rectangle(640, 180, 660, 200, fill="#e74c3c", outline="#c0392b", width=2)
        canvas.create_text(650, 190, text="ON", font=("Arial", 8, "bold"), fill="white")
        
        # LED indicator
        canvas.create_oval(690, 183, 706, 199, fill="#2ecc71", outline="#27ae60", width=2)
        canvas.create_text(698, 205, text="PWR", font=("Arial", 7), fill="white")
        
        # Ground terminal
        canvas.create_oval(720, 175, 740, 195, fill="#34495e", outline="#2c3e50", width=2)
        canvas.create_text(730, 205, text="⏚", font=("Arial", 14, "bold"), fill="white")
        
        # Electrical Cables (realistic routing)
        # HV cable to top plate (red high voltage)
        canvas.create_line(550, 130, 520, 130, 520, 260, 450, 280, 
                         width=4, fill="#8b0000", smooth=True)
        canvas.create_line(550, 130, 520, 130, 520, 260, 450, 280, 
                         width=2, fill="#e74c3c", smooth=True)
        
        # Ground cable to bottom plate (black)
        canvas.create_line(720, 195, 720, 360, 450, 343, 
                         width=4, fill="#2c3e50", smooth=True)
        
        # Cable labels
        canvas.create_text(510, 250, text="HV+", font=("Arial", 8, "bold"), 
                         fill="#e74c3c", angle=45)
        
        # Chamber label
        canvas.create_text(340, 415, text="Millikan Oil Drop Apparatus", 
                         font=("Arial", 13, "bold"), fill="#2c3e50")


    def create_tab_scheme(self):
        container = self.tab_scheme
        tk.Label(container, text="Skema Alat Eksperimen Tetes Minyak Millikan", 
                 font=("Arial", 16, "bold"), bg="#f5f6fa", fg="#2d3436").pack(pady=15)
        
        frame = tk.Frame(container, bg="white", bd=1, relief="solid")
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        text_area = tk.Text(frame, font=("Arial", 12), wrap="word", padx=20, pady=20, bg="white", relief="flat")
        text_area.pack(fill="both", expand=True)
        
        content = """
SKEMA ALAT DAN PENJELASAN

Peralatan utama terdiri dari ruang tertutup berisi dua pelat kapasitor yang diamati dengan mikroskop.

KOMPONEN ALAT:

1. Atomizer (Pengabut)
   Menyemprotkan minyak khusus densitas tinggi menjadi partikel-partikel kabut (tetesan) yang sangat halus ke dalam chamber. Sebagian tetesan akan mendapatkan muatan listrik statis akibat gesekan saat disemprotkan.

2. Ruang Pengamatan (Chamber)
   Terdiri dari dua pelat logam sejajar (atas dan bawah).
   - Jarak antar pelat (d) diketahui.
   - Pelat dihubungkan ke sumber tegangan tinggi.

3. Mikroskop Pengamat dengan Grid Skala
   Digunakan untuk mengamati gerak tetesan minyak yang sangat kecil. Lensa mikroskop membalikkan bayangan (tetesan jatuh terlihat naik). Di dalam lensa okuler terdapat garis skala (grid) untuk mengukur jarak tempuh tetesan.

4. Power Supply Tegangan Tinggi Variabel
   Menghasilkan beda potensial (V) yang dapat diatur (0-600V) antar pelat untuk menciptakan medan listrik (E = V/d). Medan ini memberikan gaya listrik pada tetesan bermuatan.

5. Sumber Cahaya & Penyerap Panas
   Lampu halogen menerangi tetesan agar terlihat berkilau seperti bintang dengan latar belakang gelap. Filter penyerap panas melindungi chamber agar suhu (konveksi udara) tetap stabil.

TUJUAN:
Menentukan nilai muatan elementer (e) elektron dengan menyeimbangkan gaya berat (kebawah) dan gaya listrik (keatas) pada tetesan minyak.
        """
        text_area.insert("1.0", content)
        text_area.config(state="disabled")


    def create_experiment_ui(self):
        main_layout = tk.Frame(self.tab_exp, bg="#f5f6fa")
        main_layout.pack(fill="both", expand=True, padx=10, pady=10)
        
        # --- Left Control Panel ---
        left_panel = tk.Frame(main_layout, width=300, bg="white", relief="raised", bd=1)
        left_panel.pack(side="left", fill="y", padx=5)
        left_panel.pack_propagate(False)
        
        self.lbl_control_title = tk.Label(left_panel, text=self.T("control_panel"), font=("Arial", 14, "bold"), bg="white")
        self.lbl_control_title.pack(pady=10)
        
        # 1. Nebulizer
        self.frame_oil = tk.LabelFrame(left_panel, text=self.T("oil_drop"), bg="white", font=("Arial", 10, "bold"))
        self.frame_oil.pack(fill="x", padx=10, pady=5)
        
        self.btn_spray = tk.Button(self.frame_oil, text=self.T("spray_oil"), bg="#e67e22", fg="black", 
                  command=self.spray_oil)
        self.btn_spray.pack(fill="x", padx=10, pady=10)
        
        self.btn_clear = tk.Button(self.frame_oil, text=self.T("clear_drops"), bg="#e74c3c", fg="black", 
                  command=self.clear_drops)
        self.btn_clear.pack(fill="x", padx=10, pady=5)
        
        # 2. Voltage
        self.frame_volt = tk.LabelFrame(left_panel, text=self.T("voltage_plate"), bg="white", font=("Arial", 10, "bold"))
        self.frame_volt.pack(fill="x", padx=10, pady=15)
        
        self.lbl_volt = tk.Label(self.frame_volt, text="0.0 V", font=("Ds-Digital", 20), fg="red", bg="black", width=8)
        self.lbl_volt.pack(pady=5)
        
        self.volt_var = tk.DoubleVar(value=0.0)
        self.scale_volt = tk.Scale(self.frame_volt, from_=0, to=600, orient="horizontal", 
                                   variable=self.volt_var, command=self.update_voltage, bg="white")
        self.scale_volt.pack(fill="x", padx=10)
        
        # Polarity
        self.polar_var = tk.StringVar(value="Normal")
        self.btn_polarity = tk.Button(self.frame_volt, text=self.T("polarity_normal"), 
                                      command=self.toggle_polarity, bg="#bdc3c7")
        self.btn_polarity.pack(fill="x", padx=10, pady=5)
        
        # 3. Stopwatch
        self.frame_timer = tk.LabelFrame(left_panel, text=self.T("stopwatch"), bg="white", font=("Arial", 10, "bold"))
        self.frame_timer.pack(fill="x", padx=10, pady=15)
        
        self.lbl_timer = tk.Label(self.frame_timer, text="00.00 s", font=("Courier New", 24, "bold"), bg="#34495e", fg="#2ecc71")
        self.lbl_timer.pack(pady=10, fill="x", padx=20)
        
        btn_box = tk.Frame(self.frame_timer, bg="white")
        btn_box.pack(fill="x", pady=5)
        self.btn_start_stop = tk.Button(btn_box, text=self.T("start_stop"), bg="#27ae60", fg="black", command=self.toggle_stopwatch)
        self.btn_start_stop.pack(side="left", fill="x", expand=True, padx=2)
        
        self.btn_reset_timer = tk.Button(btn_box, text=self.T("reset"), bg="#f39c12", fg="black", command=self.reset_stopwatch)
        self.btn_reset_timer.pack(side="left", fill="x", expand=True, padx=2)

        # 4. Data Entry shortcut
        self.lbl_quick_input = tk.Label(left_panel, text=self.T("quick_input"), bg="white", font=("Arial", 10, "bold"))
        self.lbl_quick_input.pack(pady=(20,5))
        
        self.btn_record = tk.Button(left_panel, text=self.T("record_data"), bg="#3498db", fg="black", command=self.prompt_save_data)
        self.btn_record.pack(fill="x", padx=10)

        # 5. Global Reset
        tk.Frame(left_panel, height=20, bg="white").pack() # Spacer
        self.btn_reset_all = tk.Button(left_panel, text=self.T("reset_all"), bg="#c0392b", fg="black", font=("Arial", 11, "bold"), 
                  command=self.reset_all)
        self.btn_reset_all.pack(fill="x", padx=10, pady=10)

        # --- Center: Microscope View ---
        center_panel = tk.Frame(main_layout, bg="#2c3e50")
        center_panel.pack(side="left", fill="both", expand=True, padx=5)
        
        self.lbl_microscope = tk.Label(center_panel, text=self.T("microscope_view"), fg="white", bg="#2c3e50")
        self.lbl_microscope.pack(pady=5)
        
        self.cv_size = 500
        self.canvas = tk.Canvas(center_panel, width=self.cv_size, height=self.cv_size, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(anchor="center", pady=20)
        
        # Draw Microscope Mask (Circle)
        self.draw_microscope_overlay()
        
    def create_analysis_ui(self):
        # Use PanedWindow for split layout (Left: Data/Controls, Right: Graph)
        paned = tk.PanedWindow(self.tab_data, orient=tk.HORIZONTAL, bg="#f5f6fa", sashwidth=5)
        paned.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left Frame: Table & Controls
        left_frame = tk.Frame(paned, bg="white", width=400)
        paned.add(left_frame, minsize=400)
        
        # Table
        self.cols = ("No", "Volt (V)", "t_fall (s)", "t_rise (s)", "q (C)", "n (approx)")
        self.tree = ttk.Treeview(left_frame, columns=self.cols, show="headings", height=15)
        
        # Initial headings setup
        headers = [ "table_no", "table_volt", "table_t_fall", "table_t_rise", "table_q", "table_n"]
        for col, key in zip(self.cols, headers):
            self.tree.heading(col, text=self.T(key))
            self.tree.column(col, width=65 if col != "No" else 30, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=5, pady=5) 
        
        # Controls below table
        btn_box = tk.Frame(left_frame, bg="white")
        btn_box.pack(fill="x", pady=10, padx=5)
        
        self.btn_calc = tk.Button(btn_box, text=self.T("calc_charge"), command=self.calculate_row, bg="#9b59b6", fg="black")
        self.btn_calc.pack(side="left", padx=5, fill="x", expand=True)
        
        self.btn_del = tk.Button(btn_box, text=self.T("delete_data"), command=self.delete_row, bg="#e74c3c", fg="black")
        self.btn_del.pack(side="left", padx=5, fill="x", expand=True)
        
        self.btn_save = tk.Button(btn_box, text=self.T("save_cloud"), command=self.save_data_unified, bg="#3498db", fg="black")
        self.btn_save.pack(side="left", padx=5, fill="x", expand=True)
        
        self.lbl_result = tk.Label(left_frame, text=self.T("est_e_result").format(val="-"), font=("Arial", 14, "bold"), bg="white", fg="#2980b9")
        self.lbl_result.pack(pady=10)

        # Right Frame: Graph Area
        right_frame = tk.Frame(paned, bg="white", bd=1, relief="solid")
        paned.add(right_frame)

        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.ax.set_title(self.T("graph_title"))
        self.ax.set_ylabel(self.T("graph_y"))
        self.ax.set_xlabel("Data Index")
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

        self.txt_guide.insert("1.0", self.T("guide_content"))
        self.txt_guide.config(state="disabled")

    def draw_microscope_overlay(self):
        cx, cy = self.cv_size//2, self.cv_size//2
        r = self.cv_size//2 - 10
        
        # Background Viewport
        self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="#fdfefe", outline="#95a5a6", width=10, tags="overlay")
        
        # Grid System inside
        # Scale: 100 px = 1 grid unit (0.5mm)? Let's define a scale.
        # If Plate Dist = 7.67mm. 400px height.
        # Then 400px = approx 2mm (zoomed in view).
        # Let's say 1 grid (0.5mm) = 100 pixels.
        self.px_per_mm = 200 # 100px = 0.5mm
        
        grid_spacing = 100
        
        for i in range(-2, 3):
            y = cy + i * grid_spacing
            if i == 0:
                # Center line thicker/different color
                self.canvas.create_line(cx-r+20, y, cx+r-20, y, width=2, fill="#e74c3c", tags="grid")
            else:
                self.canvas.create_line(cx-r+40, y, cx+r-40, y, width=1, fill="#bdc3c7", tags="grid")

    def spray_oil(self):
        if len(self.drops) > 10: return # Limit drops
        
        # Create a new drop
        r = random.uniform(0.5e-6, 1.5e-6) # 0.5 - 1.5 um
        n = random.randint(1, 4) # 1 - 4 e
        if random.random() < 0.3: n = -n # Some are positive charged (rare) -> usually oil picks up negative
        # Negative charge is standard for Millikan oil drop
        n = -abs(n) 
        
        q = n * self.e_real
        
        # Position (Start at top random x)
        cx = self.cv_size // 2
        px_x = random.randint(cx - 150, cx + 150)
        px_y = 50 # Start near top
        
        drop_id = self.next_drop_id
        self.next_drop_id += 1
        
        # Visual size (exaggerated)
        vis_r = 3 + (r - 0.5e-6)*1e6 * 2 
        
        color = "black" if n < 0 else "red" # Black for negative, Red for positive
        
        canvas_item = self.canvas.create_oval(px_x-vis_r, px_y-vis_r, px_x+vis_r, px_y+vis_r, fill=color, tags="drop")
        
        self.drops.append({
            'id': drop_id,
            'item': canvas_item,
            'r': r,
            'q': q,
            'x': px_x,
            'y': px_y, # pixels
            'vy': 0.0, # m/s
            'real_y': 0.0, # m (0 at top plate?)
            'm_eff': (4/3) * math.pi * (r**3) * (self.rho_oil - self.rho_air)
        })

    def clear_drops(self):
        for d in self.drops:
            self.canvas.delete(d['item'])
        self.drops = []

    def update_voltage(self, val):
        self.voltage = float(val)
        pol = "(+)" if self.polar_var.get() == "Normal" else "(-)"
        self.lbl_volt.config(text=f"{self.voltage:.1f} V {pol}")

    def toggle_polarity(self):
        curr = self.polar_var.get()
        new = "Reversed" if curr == "Normal" else "Normal"
        self.polar_var.set(new)
        key = "polarity_normal" if new == "Normal" else "polarity_reverse"
        self.btn_polarity.config(text=self.T(key))
        self.update_voltage(self.volt_var.get())

    def toggle_stopwatch(self):
        if self.stopwatch_running:
            # Stop
            self.stopwatch_running = False
        else:
            # Start
            self.stopwatch_running = True
            self.stopwatch_start_time = time.time() - self.stopwatch_elapsed
            
    def reset_stopwatch(self):
        self.stopwatch_running = False
        self.stopwatch_elapsed = 0.0
        self.lbl_timer.config(text="00.00 s")

    def prompt_save_data(self):
        def save():
            try:
                tf = float(e_tf.get())
                tr = float(e_tr.get())
                dist_mm = float(e_dist.get())
                
                # Auto Calculate q? Or just save raw?
                # User instructions say "Hitung Muatan". Tab Analysis handles calc.
                # Just save raw data.
                
                # Need distance in logic.
                # Logic: v = dist / t.
                # If dist is variable, store it.
                # Or assume standard 1 grid (0.5mm).
                if dist_mm <= 0: return
                
                # Store in Treeview 
                # Calculating tentatively for display
                # We need to reuse the physics logic in 'Kalkulator'
                
                # Assuming Standard params
                term_data = {
                    "V": self.voltage,
                    "tf": tf,
                    "tr": tr,
                    "dist": dist_mm * 1e-3 # Convert to m
                }
                
                self.data_store.append(term_data)
                
                # Insert to Tree
                # ("No", "Volt (V)", "t_fall (s)", "t_rise (s)", "q (C)", "n")
                idx = len(self.tree.get_children()) + 1
                self.tree.insert("", "end", values=(idx, f"{self.voltage:.1f}", f"{tf:.2f}", f"{tr:.2f}", "Hitung...", "?"))
                
                top.destroy()
            except ValueError:
                messagebox.showerror(self.T("msg_error"), self.T("msg_input_error"))

        top = tk.Toplevel(self)
        top.title(self.T("popup_title_record"))
        
        tk.Label(top, text=self.T("lbl_volt_now").format(val=f"{self.voltage:.1f}")).pack(pady=5)
        
        tk.Label(top, text=self.T("lbl_t_fall_input")).pack()
        e_tf = tk.Entry(top)
        e_tf.insert(0, f"{self.stopwatch_elapsed:.2f}") # Auto fill with stopwatch
        e_tf.pack()
        
        tk.Label(top, text=self.T("lbl_t_rise_input")).pack()
        e_tr = tk.Entry(top)
        e_tr.pack()
        
        tk.Label(top, text=self.T("lbl_dist_input")).pack()
        e_dist = tk.Entry(top)
        e_dist.insert(0, "0.5")
        e_dist.pack()
        
        tk.Button(top, text=self.T("btn_save_popup"), command=save, bg="#2ecc71").pack(pady=10)


    def start_animation(self):
        if not self.running:
            self.running = True
            self.animation_loop()

    def stop_animation(self):
        self.running = False

    def animation_loop(self):
        if not self.running: return

        dt = 0.05 # 50ms
        
        # Update Stopwatch
        if self.stopwatch_running:
            self.stopwatch_elapsed = time.time() - self.stopwatch_start_time
            self.lbl_timer.config(text=f"{self.stopwatch_elapsed:.2f} s")
            
        # Update Drops
        drops_to_remove = []
        
        # Electric Field
        # E = V / d
        # Direction: If Plat Atas (+), E points Down. Force on Negative Charge (Up).
        # Standard: Top Plate Positive.
        # E_field magnitude
        E = self.voltage / self.d_plate
        
        # Polarity check
        # Normal (Top +): E points Down. F_elec on (-q) is Up.
        # Reversed (Top -): E points Up. F_elec on (-q) is Down.
        if self.polar_var.get() == "Normal":
            E_vec = 1.0 # E points Down
        else:
            E_vec = -1.0 # E points Up
            
        for d in self.drops:
            # Physics Calculation
            # Forces: Gravity (Down, +y), Buoyancy (Up, -y -> integrated in m_eff), Drag (Opposite v), Electric
            
            # F_gravity_eff = m_eff * g (Down/Positive Y in screen coords usually, but let's do physics coords)
            # Let's use Down as Positive Y (Screen coords)
            
            Fg = d['m_eff'] * self.g
            
            # F_electric = q * E
            # q is e.g. -1.6e-19
            # If Normal (Top +), E is Down (+Y). F = qE = (-)(+) = (-) Up. Correct.
            Fe = d['q'] * (E * E_vec)
            
            F_net = Fg + Fe
            
            # Terminal Velocity Logic
            # F_net = F_drag = 6 * pi * eta * r * v
            # v = F_net / (6 * pi * eta * r)
            # This assumes instant terminal velocity (valid for micro-particles)
            
            k_stokes = 6 * math.pi * self.viskositas * d['r']
            v_term = F_net / k_stokes
            
            # Update Position
            dy = v_term * dt # meters
            d['real_y'] += dy
            
            # Convert m to pixels
            # Scale: 100px = 0.5 mm = 5e-4 m
            # px_per_m = 100 / 5e-4 = 200,000
            px_per_m = 200 / self.grid_dist
            
            pixel_dy = dy * px_per_m
            d['y'] += pixel_dy
            
            self.canvas.move(d['item'], 0, pixel_dy)
            
            # Bounds check (simple)
            if d['y'] > self.cv_size + 20 or d['y'] < -20:
                drops_to_remove.append(d)
                
        for d in drops_to_remove:
            self.canvas.delete(d['item'])
            self.drops.remove(d)
                
        self.after(50, self.animation_loop)

    def calculate_row(self):
        sel = self.tree.selection()
        if not sel: return
        
        idx_str = self.tree.item(sel[0], "values")[0]
        data_idx = int(idx_str) - 1
        data = self.data_store[data_idx]
        
        # Physics Calculation
        # From text script:
        # vf = dist / tf
        # vr = dist / tr
        # vf = mg / k (Fall)
        # qE - mg = k * vr (Rise)
        # q = (mg/E) * (vf+vr)/vf
        
        # Need m (or r) first.
        # r = sqrt( (9 * eta * vf) / (2 * g * (rho_dil - rho_air)) )
        
        dist = data['dist']
        tf = data['tf']
        tr = data['tr']
        V = data['V']
        
        if tf == 0 or tr == 0 or V == 0: return

        vf = dist / tf
        vr = dist / tr
        
        # Calculate Radius (r)
        num = 9 * self.viskositas * vf
        den = 2 * self.g * (self.rho_oil - self.rho_air)
        r = math.sqrt(num / den)
        
        # Calculate Mass eff
        vol = (4/3) * math.pi * (r**3)
        m_eff = vol * (self.rho_oil - self.rho_air)
        
        # Calculate E
        E = V / self.d_plate
        
        # Calculate q
        # From Force Balance:
        # Fall: mg = k * vf
        # Rise: qE - mg = k * vr  => qE = k*vr + mg = k*vr + k*vf = k(vr+vf)
        # q = (k/E) * (vf + vr)
        k = 6 * math.pi * self.viskositas * r
        q = (k / E) * (vf + vr)
        
        n = q / self.e_real
        
        # Update Tree
        self.tree.item(sel[0], values=(idx_str, f"{V:.1f}", f"{tf:.2f}", f"{tr:.2f}", f"{q:.2e}", f"{n:.2f}"))
        self.update_graph()
        
    def update_graph(self):
        qs = []
        indices = []
        for child in self.tree.get_children():
            vals = self.tree.item(child)["values"]
            # q is at index 4. Check if it's calculated.
            q_val = vals[4]
            if q_val != "Hitung...":
                qs.append(float(q_val))
                indices.append(int(vals[0]))
        
        self.ax.clear()
        self.ax.set_title(self.T("graph_title"))
        self.ax.set_ylabel(self.T("graph_y"))
        self.ax.set_xlabel(self.T("graph_x"))
        self.ax.grid(True)
        
        if qs:
            self.ax.scatter(indices, qs, c='blue', marker='o')
            # Draw line for theoretic e
            self.ax.axhline(y=1.602e-19, color='r', linestyle='--', label='e (Theoretic)')
            self.ax.legend()
            
        self.graph_canvas.draw()

    def get_data(self):
        export_data = []
        for child in self.tree.get_children():
            vals = self.tree.item(child)["values"]
            row = {
                "No": vals[0],
                "Volt (V)": vals[1],
                "t_fall (s)": vals[2],
                "t_rise (s)": vals[3],
                "q (C)": vals[4],
                "n": vals[5]
            }
            export_data.append(row)
        return export_data
        
    def save_data_unified(self):
        data = self.get_data()
        if not data:
            messagebox.showwarning(self.T("msg_warning"), self.T("msg_no_data_save"))
            return
        success, msg = DataManager.save_data_unified(data, "Hamburan Milikan")
        if success:
            messagebox.showinfo(self.T("msg_success"), self.T("msg_save_success") + f"\n{msg}")
        else:
            messagebox.showerror(self.T("msg_error"), self.T("msg_save_fail") + f"\n{msg}")

    def estimate_e(self):
        pass # Optional advanced stats
        
    def delete_row(self):
        sel = self.tree.selection()
        for item in sel:
             self.tree.delete(item)

    def reset_all(self):
        ans = messagebox.askyesno(self.T("msg_reset_confirm_title"), self.T("msg_reset_confirm_body"))
        if not ans: return
        
        # 1. Clear Drops
        self.clear_drops()
        
        # 2. Reset Voltage
        self.volt_var.set(0.0)
        self.update_voltage(0.0)
        self.polar_var.set("Normal")
        self.btn_polarity.config(text=self.T("polarity_normal"))
        
        # 3. Reset Stopwatch
        self.reset_stopwatch()
        
        # 4. Clear Data
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.data_store = []
        
        messagebox.showinfo(self.T("reset"), self.T("msg_reset_info"))

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabMilikan(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
