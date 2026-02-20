import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class VirtualLabGayaGesek(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#f5f6fa")
        
        self.setup_translations()
        self.lang = "ID"
        
        # Physics Constants
        self.g = 9.8
        self.surfaces = {
            "wood_wood": {"mu_s": 0.50, "mu_k": 0.30, "color": "#d35400"},
            "rubber_concrete": {"mu_s": 0.80, "mu_k": 0.60, "color": "#7f8c8d"},
            "ice_ice": {"mu_s": 0.10, "mu_k": 0.03, "color": "#a29bfe"},
            "teflon_teflon": {"mu_s": 0.04, "mu_k": 0.04, "color": "#dfe6e9"}
        }
        self.surface_keys = list(self.surfaces.keys())
        
        self.selected_surface_key = "wood_wood"
        self.mass_kg = 0.5
        self.is_running = False
        self.time_step = 0.0
        self.pull_force = 0.0
        self.friction_force = 0.0
        
        self.data_series_t = []
        self.data_series_P = [] # Pull
        self.data_series_f = [] # Friction
        
        self.recorded_data = []
        
        self.setup_ui()
        
    def setup_translations(self):
        self.translations = {
            "ID": {
                "title": "LABORATORIUM GAYA GESEK (FRICTION)",
                "subtitle": "Analisis Gaya Gesek Statis dan Kinetis",
                "tab_exp": "Eksperimen",
                "tab_ana": "Analisis Data",
                "tab_guide": "Petunjuk Praktikum",
                "set_body": "PENGATURAN BENDA",
                "surf_type": "Jenis Permukaan:",
                "mass_block": "Massa Balok (kg):",
                "norm_force": "Gaya Normal (N) =",
                "start_btn": "MULAI TARIK (START)",
                "reset_btn": "RESET SIMULASI",
                "record_btn": "CATAT HASIL",
                "sensor_title": "Sensor Gaya (Force Sensor)",
                "pull_lbl": "Gaya Tarik (Pull):",
                "status_lbl": "Status Benda:",
                "status_still": "DIAM",
                "status_move": "BERGERAK",
                "graph_title": "Grafik Gaya vs Waktu",
                "axis_x": "Waktu (s)",
                "axis_y": "Gaya (N)",
                "legend_pull": "F Tarik",
                "legend_frict": "F Gesek",
                "ana_title": "Data Pengamatan Gaya Gesek",
                "col_surf": "Permukaan",
                "col_mass": "Massa (kg)",
                "col_norm": "Normal (N)",
                "col_fs": "fs Max (N)",
                "col_fk": "fk (N)",
                "btn_clear": "Hapus Data",
                "btn_calc": "Hitung Koefisien Gesek (μ)",
                "wood_wood": "Kayu pada Kayu",
                "rubber_concrete": "Karet pada Beton",
                "ice_ice": "Es pada Es",
                "teflon_teflon": "Teflon pada Teflon",
                "surface_lbl": "Permukaan:",
                "msg_empty": "Data Kosong",
                "msg_run_first": "Jalankan simulasi terlebih dahulu!",
                "msg_recorded": "Tercatat",
                "msg_success": "Data berhasil direkam ke tabel Analisis.",
                "res_header": "HASIL PERHITUNGAN KOEFISIEN:\n",
                "guide_header": "PETUNJUK PRAKTIKUM GAYA GESEK (FRICTION)",
                "guide_content": """A. TUJUAN
1. Mengamati perbedaan antara Gaya Gesek Statis (fs) dan Kinetis (fk).
2. Menentukan Koefisien Gesek Statis (μs) dan Kinetis (μk) suatu permukaan.

B. DASAR TEORI
- Gaya Gesek Statis (fs): Gaya yang menahan benda agar tetap diam saat ditarik. Nilainya mengikuti gaya tarik sampai mencapai batas maksimum:
  fs_max = μs * N
- Gaya Gesek Kinetis (fk): Gaya gesek yang bekerja saat benda sudah bergerak (meluncur). Nilainya relatif konstan dan lebih kecil dari fs_max:
  fk = μk * N

Grafik Gaya vs Waktu biasanya menunjukkan kenaikan linear (saat diam), mencapai puncak (fs_max), lalu turun mendadak menjadi datar (fk) saat benda bergerak.

C. PROSEDUR
1. Pilih Jenis Permukaan dan Massa Balok.
2. Klik "MULAI TARIK". Simulasi akan menarik balok dengan gaya yang bertambah perlahan.
3. Amati Grafik:
   - Garis Merah (Gaya Gesek) akan naik berimpit dengan gaya tarik (selama diam).
   - Tiba-tiba garis merah turun (Drop) -> Itu tanda benda mulai bergerak (Breakaway point).
   - Nilai puncak sebelum turun adalah fs_max.
   - Nilai datar setelah turun adalah fk.
4. Klik "CATAT HASIL" untuk menyimpan data puncak (fs) dan kinetis (fk) terakhir ke tabel Analisis.
5. Ulangi dengan variasi massa untuk membuktikan hubungan linear fs_max vs N."""
            },
            "EN": {
                "title": "FRICTION FORCE LAB",
                "subtitle": "Static and Kinetic Friction Analysis",
                "tab_exp": "Experiment",
                "tab_ana": "Data Analysis",
                "tab_guide": "Lab Guide",
                "set_body": "OBJECT SETTINGS",
                "surf_type": "Surface Type:",
                "mass_block": "Block Mass (kg):",
                "norm_force": "Normal Force (N) =",
                "start_btn": "START PULL",
                "reset_btn": "RESET SIMULATION",
                "record_btn": "RECORD RESULT",
                "sensor_title": "Force Sensor",
                "pull_lbl": "Pull Force:",
                "status_lbl": "Object Status:",
                "status_still": "STATIONARY",
                "status_move": "MOVING",
                "graph_title": "Force vs Time Graph",
                "axis_x": "Time (s)",
                "axis_y": "Force (N)",
                "legend_pull": "F Pull",
                "legend_frict": "F Friction",
                "ana_title": "Friction Observation Data",
                "col_surf": "Surface",
                "col_mass": "Mass (kg)",
                "col_norm": "Normal (N)",
                "col_fs": "fs Max (N)",
                "col_fk": "fk (N)",
                "btn_clear": "Clear Data",
                "btn_calc": "Calculate Coefficient (μ)",
                "wood_wood": "Wood on Wood",
                "rubber_concrete": "Rubber on Concrete",
                "ice_ice": "Ice on Ice",
                "teflon_teflon": "Teflon on Teflon",
                "surface_lbl": "Surface:",
                "msg_empty": "Empty Data",
                "msg_run_first": "Run simulation first!",
                "msg_recorded": "Recorded",
                "msg_success": "Data successfully recorded to Analysis table.",
                "res_header": "COEFFICIENT CALCULATION RESULTS:\n",
                "guide_header": "FRICTION FORCE LAB GUIDE",
                 "guide_content": """A. OBJECTIVE
1. Observe the difference between Static Friction (fs) and Kinetic Friction (fk).
2. Determine Static (μs) and Kinetic (μk) Friction Coefficients of a surface.

B. THEORY
- Static Friction (fs): Force holding the object still when pulled. Value matches pull force until max limit:
  fs_max = μs * N
- Kinetic Friction (fk): Friction force when object is moving (sliding). Value is relatively constant and smaller than fs_max:
  fk = μk * N

Force vs Time graph usually shows linear rise (while stationary), peak (fs_max), then sudden drop to flat (fk) when moving.

C. PROCEDURE
1. Select Surface Type and Block Mass.
2. Click "START PULL". Simulation pulls block with slowly increasing force.
3. Observe Graph:
   - Red Line (Friction) rises matching pull force (while stationary).
   - Suddenly red line drops -> Sign object starts moving (Breakaway point).
   - Peak value before drop is fs_max.
   - Flat value after drop is fk.
4. Click "RECORD RESULT" to save peak (fs) and kinetic (fk) data to Analysis table.
5. Repeat with varied mass to prove linear relation of fs_max vs N."""
            }
        }

    def T(self, key):
        return self.translations[self.lang].get(key, key)
        
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
        
        self.notebook.add(self.tab_exp, text=self.T("tab_exp"))
        self.notebook.add(self.tab_ana, text=self.T("tab_ana"))
        self.notebook.add(self.tab_guide, text=self.T("tab_guide"))
        
        self.create_experiment_ui()
        self.create_analysis_ui()
        self.create_guide_ui()
        
    def create_experiment_ui(self):
        layout = tk.Frame(self.tab_exp, bg="#f5f6fa")
        layout.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left Control Panel
        left = tk.Frame(layout, width=300, bg="white", relief="raised", bd=1)
        left.pack(side="left", fill="y", padx=5)
        
        self.lbl_set_body = tk.Label(left, text=self.T("set_body"), font=("Arial", 12, "bold"), bg="white")
        self.lbl_set_body.pack(pady=15)
        
        # Surface Selector
        self.lbl_surf_type = tk.Label(left, text=self.T("surf_type"), bg="white")
        self.lbl_surf_type.pack(anchor="w", padx=20)
        
        self.surf_var = tk.StringVar()
        self.cb_surf = ttk.Combobox(left, textvariable=self.surf_var, state="readonly")
        self.cb_surf.pack(fill="x", padx=20, pady=5)
        self.cb_surf.bind("<<ComboboxSelected>>", self.on_surface_change)
        
        # Populate Combobox
        self.update_surface_combobox()
        
        # Mass Slider
        self.lbl_mass_block = tk.Label(left, text=self.T("mass_block"), bg="white")
        self.lbl_mass_block.pack(anchor="w", padx=20, pady=(15, 0))
        self.mass_scale = tk.Scale(left, from_=0.1, to=2.0, resolution=0.1, orient="horizontal", bg="white")
        self.mass_scale.set(self.mass_kg)
        self.mass_scale.pack(fill="x", padx=20)
        
        # Normal Force Display
        self.lbl_normal = tk.Label(left, text=f"{self.T('norm_force')} {self.mass_kg*self.g:.2f} N", fg="blue", bg="white")
        self.lbl_normal.pack(pady=5)
        
        tk.Frame(left, height=2, bg="#ecf0f1").pack(fill="x", pady=15, padx=10)
        
        # Action Buttons
        self.btn_start = tk.Button(left, text=self.T("start_btn"), command=self.start_simulation,
                  bg="#2ecc71", fg="black", font=("Arial", 11, "bold"))
        self.btn_start.pack(fill="x", padx=20, pady=5)
                  
        self.btn_reset = tk.Button(left, text=self.T("reset_btn"), command=self.reset_simulation,
                  bg="#e74c3c", fg="black", font=("Arial", 11, "bold"))
        self.btn_reset.pack(fill="x", padx=20, pady=5)
                  
        self.btn_record = tk.Button(left, text=self.T("record_btn"), command=self.record_result_manual,
                  bg="#3498db", fg="black", font=("Arial", 11, "bold"))
        self.btn_record.pack(fill="x", padx=20, pady=20)
                  
        monitor = tk.LabelFrame(left, text=self.T("sensor_title"), bg="white", padx=10, pady=10)
        monitor.pack(fill="x", padx=10, pady=10)
        self.f_monitor_frame = monitor # Keep ref
        
        self.lbl_pull_title = tk.Label(monitor, text=self.T("pull_lbl"), bg="white")
        self.lbl_pull_title.pack(anchor="w")
        self.lbl_pull = tk.Label(monitor, text="0.00 N", font=("Ds-Digital", 20), fg="#27ae60", bg="black", width=10)
        self.lbl_pull.pack()
        
        self.lbl_status_title = tk.Label(monitor, text=self.T("status_lbl"), bg="white")
        self.lbl_status_title.pack(anchor="w", pady=(10,0))
        self.lbl_status = tk.Label(monitor, text=self.T("status_still"), font=("Arial", 14, "bold"), fg="red", bg="white")
        self.lbl_status.pack()
        
        # Right Visualization Panel
        right = tk.Frame(layout, bg="#f5f6fa")
        right.pack(side="left", fill="both", expand=True, padx=5)
        
        # Top: Canvas Animation
        self.canvas_anim = tk.Canvas(right, height=250, bg="white", relief="sunken", bd=1)
        self.canvas_anim.pack(fill="x", pady=5)
        
        # Bottom: Matplotlib Graph
        self.fig, self.ax = plt.subplots(figsize=(5, 3), dpi=100)
        self.setup_graph()
        
        self.canvas_graph = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas_graph.get_tk_widget().pack(fill="both", expand=True)
        
        self.draw_scene_static()

    def update_surface_combobox(self):
        display_values = [self.T(k) for k in self.surface_keys]
        self.cb_surf['values'] = display_values
        # Restore selection
        if self.selected_surface_key in self.surface_keys:
            idx = self.surface_keys.index(self.selected_surface_key)
            self.cb_surf.current(idx)

    def setup_graph(self):
        self.ax.clear()
        self.ax.set_title(self.T("graph_title"))
        self.ax.set_xlabel(self.T("axis_x"))
        self.ax.set_ylabel(self.T("axis_y"))
        self.ax.grid(True)
        self.line_pull, = self.ax.plot([], [], 'g--', label=self.T("legend_pull"))
        self.line_frict, = self.ax.plot([], [], 'r-', label=self.T("legend_frict"))
        self.ax.legend()

    def create_analysis_ui(self):
        layout = tk.Frame(self.tab_ana, bg="white")
        layout.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.lbl_ana_title = tk.Label(layout, text=self.T("ana_title"), font=("Arial", 14, "bold"), bg="white")
        self.lbl_ana_title.pack(pady=10)
        
        cols = ("col_surf", "col_mass", "col_norm", "col_fs", "col_fk")
        self.tree = ttk.Treeview(layout, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=self.T(c))
            self.tree.column(c, width=120, anchor="center")
        self.tree.pack(fill="x")
        self.tree_cols = cols # Save to update headings later
        
        btn_box = tk.Frame(layout, bg="white")
        btn_box.pack(fill="x", pady=10)
        
        self.btn_clear = tk.Button(btn_box, text=self.T("btn_clear"), command=self.clear_data, bg="#c0392b", fg="black")
        self.btn_clear.pack(side="left", padx=5)
        self.btn_calc = tk.Button(btn_box, text=self.T("btn_calc"), command=self.calculate_coeff, bg="#8e44ad", fg="black")
        self.btn_calc.pack(side="left", padx=5)
        
        self.lbl_result = tk.Label(layout, text="", font=("Courier", 11), bg="#ecf0f1", justify="left", relief="sunken", width=60)
        self.lbl_result.pack(pady=10)

    def create_guide_ui(self):
        self.txt_guide = tk.Text(self.tab_guide, font=("Arial", 12), padx=20, pady=20, wrap="word")
        self.txt_guide.pack(fill="both", expand=True)
        self.update_guide_content()

    def update_guide_content(self):
        self.txt_guide.config(state="normal")
        self.txt_guide.delete("1.0", "end")
        self.txt_guide.insert("1.0", self.T("guide_header") + "\n\n" + self.T("guide_content"))
        self.txt_guide.config(state="disabled")

    def on_surface_change(self, event):
        idx = self.cb_surf.current()
        if idx >= 0:
            self.selected_surface_key = self.surface_keys[idx]
            self.reset_simulation()
        
    def draw_scene_static(self):
        self.canvas_anim.delete("all")
        w = self.canvas_anim.winfo_width()
        if w < 10: w=400
        h = 250
        cy = h - 50 # Floor y
        
        if self.selected_surface_key in self.surfaces:
            surf_color = self.surfaces[self.selected_surface_key]["color"]
        else:
            surf_color = "#95a5a6" # Default
            
        self.canvas_anim.create_rectangle(0, cy, w, h, fill=surf_color, outline="")
        
        # Text display surface
        surf_display_text = f"{self.T('surface_lbl')} {self.T(self.selected_surface_key)}"
        self.canvas_anim.create_text(w/2, h-20, text=surf_display_text, fill="white")
        
        # Block
        bx_w = 80
        bx_h = 50
        bx_x = 100 # Initial pos
        bx_y = cy - bx_h
        
        self.canvas_anim.create_rectangle(bx_x, bx_y, bx_x+bx_w, bx_y+bx_h, fill="#3498db", outline="black", width=2, tags="block")
        self.canvas_anim.create_text(bx_x+bx_w/2, bx_y+bx_h/2, text=f"{self.mass_scale.get()} kg", fill="white", tags="block_txt")

    def start_simulation(self):
        if self.is_running: return
        self.is_running = True
        self.time_step = 0.0
        self.data_series_t = []
        self.data_series_P = []
        self.data_series_f = []
        
        # Prepare Physics
        m = self.mass_scale.get()
        g = self.g
        N = m * g
        self.lbl_normal.config(text=f"{self.T('norm_force')} {N:.2f} N")
        
        surf = self.surfaces[self.selected_surface_key]
        self.fs_max = surf["mu_s"] * N
        self.fk = surf["mu_k"] * N
        
        self.has_moved = False
        
        # Reset Plot limits
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, self.fs_max * 1.5)
        
        self.animate_loop()

    def reset_simulation(self):
        self.is_running = False
        self.time_step = 0.0
        self.pull_force = 0.0
        self.friction_force = 0.0
        self.lbl_pull.config(text="0.00 N")
        self.lbl_status.config(text=self.T("status_still"), fg="red")
        
        self.data_series_t = []
        self.data_series_P = []
        self.data_series_f = []
        
        self.line_pull.set_data([], [])
        self.line_frict.set_data([], [])
        self.canvas_graph.draw()
        self.draw_scene_static()

    def animate_loop(self):
        if not self.is_running: return
        
        # Increment time
        dt = 0.1
        self.time_step += dt
        
        # Increase Pull Force Linearly
        pull_rate = self.fs_max / 3.0
        
        current_P = pull_rate * self.time_step
        
        # Physics Logic
        if not self.has_moved:
            if current_P <= self.fs_max:
                # Static
                current_f = current_P
                status = self.T("status_still")
                stat_col = "red"
            else:
                # Breakaway!
                self.has_moved = True
                current_f = self.fk
                status = self.T("status_move")
                stat_col = "green"
        else:
            # Kinetic
            current_f = self.fk
            status = self.T("status_move")
            stat_col = "green"
            
        self.pull_force = current_P
        self.friction_force = current_f
        
        # Update Data
        self.data_series_t.append(self.time_step)
        self.data_series_P.append(current_P)
        self.data_series_f.append(current_f)
        
        # Update UI Labels
        self.lbl_pull.config(text=f"{current_P:.2f} N")
        self.lbl_status.config(text=status, fg=stat_col)
        
        # Update Plot
        self.line_pull.set_data(self.data_series_t, self.data_series_P)
        self.line_frict.set_data(self.data_series_t, self.data_series_f)
        
        # Auto-scroll axes if needed
        if self.time_step > 10:
            self.ax.set_xlim(self.time_step - 10, self.time_step)
        if current_P > self.ax.get_ylim()[1]:
            self.ax.set_ylim(0, current_P * 1.2)
            
        self.canvas_graph.draw()
        
        # Update Animation (Block)
        self.canvas_anim.delete("vectors")
        
        # Get coords
        bx_coords = self.canvas_anim.coords("block") # [x1, y1, x2, y2]
        if self.has_moved:
            # Move block visually to the right
            move_speed = 5 # pixels per frame
            w_canv = self.canvas_anim.winfo_width()
            if bx_coords[2] > w_canv:
                self.canvas_anim.move("block", -w_canv, 0)
                self.canvas_anim.move("block_txt", -w_canv, 0)
            else:
                self.canvas_anim.move("block", move_speed, 0)
                self.canvas_anim.move("block_txt", move_speed, 0)
                
            bx_coords = self.canvas_anim.coords("block") # Update coords

        # Draw Vectors attached to block center
        cx = (bx_coords[0] + bx_coords[2]) / 2
        cy = (bx_coords[1] + bx_coords[3]) / 2
        
        # Vector P (Right)
        len_p = current_P * 10 # scale
        self.canvas_anim.create_line(bx_coords[2], cy, bx_coords[2]+len_p, cy, fill="#2ecc71", width=4, arrow="last", tags="vectors")
        self.canvas_anim.create_text(bx_coords[2]+len_p+10, cy, text=f"F_tarik", fill="#2ecc71", tags="vectors")
        
        # Vector f (Left) - attached to bottom
        bottom_y = bx_coords[3]
        len_f = current_f * 10
        self.canvas_anim.create_line(cx, bottom_y, cx-len_f, bottom_y, fill="red", width=4, arrow="last", tags="vectors")
        self.canvas_anim.create_text(cx-len_f-10, bottom_y, text=f"f_gesek", fill="red", tags="vectors")

        if self.time_step < 10.0: # Run for 10 sim seconds
            self.after(100, self.animate_loop)
        else:
            self.is_running = False

    def record_result_manual(self):
        if len(self.data_series_f) == 0:
            messagebox.showwarning(self.T("msg_empty"), self.T("msg_run_first"))
            return
            
        # Analyze data series
        fs_max_measured = max(self.data_series_f)
        fk_measured = self.data_series_f[-1] # Simple approximation
        
        mass = self.mass_scale.get()
        N = mass * self.g
        
        # Use translated string for treeview
        surf_display = self.T(self.selected_surface_key)
        
        self.tree.insert("", "end", values=(surf_display, mass, f"{N:.2f}", f"{fs_max_measured:.2f}", f"{fk_measured:.2f}"))
        self.recorded_data.append({"surf": self.selected_surface_key, "N": N, "fs": fs_max_measured, "fk": fk_measured})
        
        messagebox.showinfo(self.T("msg_recorded"), self.T("msg_success"))

    def clear_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.recorded_data = []
        self.lbl_result.config(text="")

    def calculate_coeff(self):
        if not self.recorded_data: return
        
        # Group by surface
        by_surf = {}
        for d in self.recorded_data:
            s = d["surf"]
            if s not in by_surf: by_surf[s] = {"N": [], "fs": [], "fk": []}
            by_surf[s]["N"].append(d["N"])
            by_surf[s]["fs"].append(d["fs"])
            by_surf[s]["fk"].append(d["fk"])
            
        res_str = self.T("res_header")
        
        for s, dat in by_surf.items():
            N_arr = np.array(dat["N"])
            fs_arr = np.array(dat["fs"])
            fk_arr = np.array(dat["fk"])
            
            mu_s_calc = np.sum(N_arr * fs_arr) / np.sum(N_arr**2)
            mu_k_calc = np.sum(N_arr * fk_arr) / np.sum(N_arr**2)
            
            # Theoretical
            mu_s_teo = self.surfaces[s]["mu_s"]
            mu_k_teo = self.surfaces[s]["mu_k"]
            
            res_str += f"\n>> {self.T(s)}:\n"
            res_str += self.T("res_u_s").format(mu_s_calc, mu_s_teo, abs(mu_s_calc-mu_s_teo)/mu_s_teo*100)
            res_str += self.T("res_u_k").format(mu_k_calc, mu_k_teo, abs(mu_k_calc-mu_k_teo)/mu_k_teo*100)
            
        self.lbl_result.config(text=res_str)
        
    def set_language(self, language):
        self.lang = language
        
        # Update texts
        self.lbl_title.config(text=self.T("title"))
        self.lbl_subtitle.config(text=self.T("subtitle"))
        
        self.notebook.tab(self.tab_exp, text=self.T("tab_exp"))
        self.notebook.tab(self.tab_ana, text=self.T("tab_ana"))
        self.notebook.tab(self.tab_guide, text=self.T("tab_guide"))
        
        self.lbl_set_body.config(text=self.T("set_body"))
        self.lbl_surf_type.config(text=self.T("surf_type"))
        self.lbl_mass_block.config(text=self.T("mass_block"))
        self.lbl_normal.config(text=f"{self.T('norm_force')} {self.mass_kg*self.g:.2f} N")
        
        self.update_surface_combobox()
        
        self.btn_start.config(text=self.T("start_btn"))
        self.btn_reset.config(text=self.T("reset_btn"))
        self.btn_record.config(text=self.T("record_btn"))
        
        self.f_monitor_frame.config(text=self.T("sensor_title"))
        self.lbl_pull_title.config(text=self.T("pull_lbl"))
        self.lbl_status_title.config(text=self.T("status_lbl"))
        
        # Update Status Text (tricky, depends on state)
        if self.has_moved:
            self.lbl_status.config(text=self.T("status_move"))
        else:
            self.lbl_status.config(text=self.T("status_still"))
            
        self.setup_graph() # Redraw graph labels
        
        self.lbl_ana_title.config(text=self.T("ana_title"))
        for c in self.tree_cols:
            self.tree.heading(c, text=self.T(c))
            
        self.btn_clear.config(text=self.T("btn_clear"))
        self.btn_calc.config(text=self.T("btn_calc"))
        
        self.update_guide_content()
        self.draw_scene_static() # Redraw canvas text (surface label)

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabGayaGesek(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
