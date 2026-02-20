import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

class VirtualLabKatrol:
    def __init__(self, parent):
        self.parent = parent
        # Style Config
        self.bg_color = "#2c3e50"
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.setup_translations()
        self.lang = "ID"
        
        # --- MAIN NOTEBOOK ---
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Tab 1: Simulasi
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text=self.T("tab_1"))
        self.setup_simulasi()

        # Tab 2: Analisis Data
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text=self.T("tab_2"))
        self.setup_analisis()

    def setup_translations(self):
        self.translations = {
            "ID": {
                "tab_1": "1. Simulasi Mesin Atwood",
                "tab_2": "2. Analisis Hukum Newton II",
                "header_title": "VIRTUAL LAB: SISTEM KATROL",
                "header_sub": "Dinamika Gerak Lurus dan Hukum Newton pada Katrol Tetap",
                "footer_ver": "VERSI APLIKASI PRO",
                "footer_modul": "Modul Fisika Dasar: Mekanika Klasik",
                "params_title": "PARAMETER SISTEM",
                "lbl_m1": "Massa 1 (Kiri) [kg]:",
                "lbl_m2": "Massa 2 (Kanan) [kg]:",
                "lbl_g": "Gravitasi (g) [m/s²]:",
                "lbl_h": "Jarak Tempuh (h) [m]:",
                "btn_start": "▶ Mulai Simulasi",
                "btn_reset": "⏹ Reset Sistem",
                "info_title": "Kalkulasi Fisika (Real-Time)",
                "info_acc": "Percepatan Sistem (a): {:.3f} m/s²",
                "info_acc_ph": "Percepatan Sistem (a): - m/s²",
                "info_ten": "Tegangan Tali (T): {:.2f} N",
                "info_ten_ph": "Tegangan Tali (T): - N",
                "info_time": "Waktu Tempuh (t): {:.3f} s",
                "info_time_inf": "Waktu Tempuh (t): ∞ s",
                "info_time_ph": "Waktu Tempuh (t): - s",
                "fbd_title": "Diagram Bebas Benda",
                "graph_title_fbd": "Besar Gaya pada Beban",
                "lbl_w1": "W1 (Kiri)",
                "lbl_w2": "W2 (Kanan)",
                "lbl_ground": "Tanah (0m)",
                "title_log": "LOG DATA PERCOBAAN",
                "lbl_input_box": "Input Data",
                "lbl_m1_in": "Massa 1 (kg):",
                "lbl_m2_in": "Massa 2 (kg):",
                "lbl_f_net_auto": "Gaya Net (F = |m2-m1|g) diproses otomatis",
                "lbl_a_meas": "Percepatan Terukur (a) [m/s²]:",
                "btn_add_data": "Tambah Data",
                "btn_clear_data": "Hapus Semua Data",
                "col_m1": "m1",
                "col_m2": "m2",
                "col_mtot": "M_total",
                "col_fnet": "F_net",
                "col_auk": "a_ukur",
                "graph_an_title": "Verifikasi Hukum Newton II (F vs m·a)",
                "axis_x_an": "Massa Total × Percepatan (kg·m/s²)",
                "axis_y_an": "Gaya Bersih Teoritis (N)",
                "legend_data": "Data",
                "legend_fit": "Fit Slope = {:.2f}",
                "err_valid": "Masukkan data angka yang valid"
            },
            "EN": {
                "tab_1": "1. Atwood Machine Simulation",
                "tab_2": "2. Analysis of Newton's 2nd Law",
                "header_title": "VIRTUAL LAB: PULLEY SYSTEM",
                "header_sub": "Linear Dynamics and Newton's Laws on Fixed Pulleys",
                "footer_ver": "APP VERSION PRO",
                "footer_modul": "Basic Physics Module: Classical Mechanics",
                "params_title": "SYSTEM PARAMETERS",
                "lbl_m1": "Mass 1 (Left) [kg]:",
                "lbl_m2": "Mass 2 (Right) [kg]:",
                "lbl_g": "Gravity (g) [m/s²]:",
                "lbl_h": "Distance (h) [m]:",
                "btn_start": "▶ Start Simulation",
                "btn_reset": "⏹ Reset System",
                "info_title": "Physics Calculation (Real-Time)",
                "info_acc": "System Acceleration (a): {:.3f} m/s²",
                "info_acc_ph": "System Acceleration (a): - m/s²",
                "info_ten": "Rope Tension (T): {:.2f} N",
                "info_ten_ph": "Rope Tension (T): - N",
                "info_time": "Travel Time (t): {:.3f} s",
                "info_time_inf": "Travel Time (t): ∞ s",
                "info_time_ph": "Travel Time (t): - s",
                "fbd_title": "Free Body Diagram",
                "graph_title_fbd": "Forces on Load",
                "lbl_w1": "W1 (Left)",
                "lbl_w2": "W2 (Right)",
                "lbl_ground": "Ground (0m)",
                "title_log": "EXPERIMENT LOG",
                "lbl_input_box": "Data Input",
                "lbl_m1_in": "Mass 1 (kg):",
                "lbl_m2_in": "Mass 2 (kg):",
                "lbl_f_net_auto": "Net Force (F = |m2-m1|g) auto-processed",
                "lbl_a_meas": "Measured Acceleration (a) [m/s²]:",
                "btn_add_data": "Add Data",
                "btn_clear_data": "Clear All Data",
                "col_m1": "m1",
                "col_m2": "m2",
                "col_mtot": "M_total",
                "col_fnet": "F_net",
                "col_auk": "a_meas",
                "graph_an_title": "Newton II Law Verification (F vs m·a)",
                "axis_x_an": "Total Mass × Acceleration (kg·m/s²)",
                "axis_y_an": "Theoretical Net Force (N)",
                "legend_data": "Data",
                "legend_fit": "Fit Slope = {:.2f}",
                "err_valid": "Please enter valid numeric data"
            }
        }

    def T(self, key):
        return self.translations[self.lang].get(key, key)

    def set_language(self, lang):
        self.lang = lang
        # Recreate Notebook and tabs
        for widget in self.notebook.winfo_children():
            widget.destroy()
        
        self.notebook.add(self.tab1, text=self.T("tab_1")) # This won't work simply because tab1 destroyed
        # Need to rebuild full UI
        self.notebook.destroy()
        
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text=self.T("tab_1"))
        self.setup_simulasi()
        
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text=self.T("tab_2"))
        self.setup_analisis()
        
        self.update_preview() # Refresh sim

    # =========================================
    # TAB 1: SIMULASI
    # =========================================
    def setup_simulasi(self):
        pane = tk.PanedWindow(self.tab1, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)

        # Container Kiri (Kontrol)
        left_frame = ttk.Frame(pane, padding=10)
        pane.add(left_frame, stretch="always")

        # Container Kanan (Visualisasi)
        right_frame = ttk.Frame(pane, padding=10)
        pane.add(right_frame, stretch="always")

        # --- CONTROLS ---
        ttk.Label(left_frame, text=self.T("params_title"), font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))

        # Variabel
        if not hasattr(self, 'var_m1'): self.var_m1 = tk.DoubleVar(value=2.0)
        if not hasattr(self, 'var_m2'): self.var_m2 = tk.DoubleVar(value=4.0)
        if not hasattr(self, 'var_g'): self.var_g = tk.DoubleVar(value=9.8)
        if not hasattr(self, 'var_h'): self.var_h = tk.DoubleVar(value=2.0)

        form = ttk.Frame(left_frame)
        form.pack(fill="x", pady=5)

        # Slider m1
        ttk.Label(form, text=self.T("lbl_m1")).grid(row=0, column=0, sticky="w", pady=5)
        self.scale_m1 = tk.Scale(form, from_=0.1, to=10.0, resolution=0.1, orient="horizontal", 
                                 variable=self.var_m1, length=250, command=self.update_preview)
        self.scale_m1.grid(row=0, column=1)

        # Slider m2
        ttk.Label(form, text=self.T("lbl_m2")).grid(row=1, column=0, sticky="w", pady=5)
        self.scale_m2 = tk.Scale(form, from_=0.1, to=10.0, resolution=0.1, orient="horizontal", 
                                 variable=self.var_m2, length=250, command=self.update_preview)
        self.scale_m2.grid(row=1, column=1)

        # Slider g
        ttk.Label(form, text=self.T("lbl_g")).grid(row=2, column=0, sticky="w", pady=5)
        self.scale_g = tk.Scale(form, from_=1.6, to=20.0, resolution=0.1, orient="horizontal", 
                                variable=self.var_g, length=250, command=self.update_preview)
        self.scale_g.grid(row=2, column=1)
        
        # Slider h (Jarak Simulasi)
        ttk.Label(form, text=self.T("lbl_h")).grid(row=3, column=0, sticky="w", pady=5)
        self.scale_h = tk.Scale(form, from_=1.0, to=10.0, resolution=0.5, orient="horizontal", 
                                variable=self.var_h, length=250, command=self.update_preview)
        self.scale_h.grid(row=3, column=1)

        # Buttons
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill="x", pady=20)
        self.btn_run = ttk.Button(btn_frame, text=self.T("btn_start"), command=self.run_animation)
        self.btn_run.pack(side="left", padx=5)
        self.btn_reset = ttk.Button(btn_frame, text=self.T("btn_reset"), command=self.reset_animation)
        self.btn_reset.pack(side="left", padx=5)

        # Info Box
        self.info_frame = ttk.LabelFrame(left_frame, text=self.T("info_title"))
        self.info_frame.pack(fill="x", pady=10)
        
        self.lbl_acc = ttk.Label(self.info_frame, text=self.T("info_acc_ph"))
        self.lbl_acc.pack(anchor="w", padx=10, pady=2)
        
        self.lbl_tension = ttk.Label(self.info_frame, text=self.T("info_ten_ph"))
        self.lbl_tension.pack(anchor="w", padx=10, pady=2)
        
        self.lbl_time = ttk.Label(self.info_frame, text=self.T("info_time_ph"))
        self.lbl_time.pack(anchor="w", padx=10, pady=2)

        # Diagram Gaya Box
        self.fbd_frame = ttk.LabelFrame(left_frame, text=self.T("fbd_title"))
        self.fbd_frame.pack(fill="both", expand=True, pady=10)
        
        self.fig_fbd = Figure(figsize=(4, 3), dpi=80)
        self.ax_fbd = self.fig_fbd.add_subplot(111)
        self.canvas_fbd = FigureCanvasTkAgg(self.fig_fbd, master=self.fbd_frame)
        self.canvas_fbd.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # --- VISUALIZATION SETUP ---
        self.fig_sim = Figure(figsize=(5, 5), dpi=100)
        self.ax_sim = self.fig_sim.add_subplot(111)
        self.ax_sim.set_aspect('equal')
        self.canvas_sim = FigureCanvasTkAgg(self.fig_sim, master=right_frame)
        self.canvas_sim.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.ani = None
        self.is_running = False
        # self.update_preview() will be called by slider binding or manually

    def calculate_physics(self):
        m1 = self.var_m1.get()
        m2 = self.var_m2.get()
        g  = self.var_g.get()
        h  = self.var_h.get()
        
        total_mass = m1 + m2
        net_force = (m2 - m1) * g # Assuming m2 > m1 direction positive
        
        a = net_force / total_mass
        T = (2 * m1 * m2 * g) / total_mass
        
        # t = sqrt(2h / |a|)
        if abs(a) > 0.001:
            t_fall = np.sqrt(2 * h / abs(a))
        else:
            t_fall = float('inf')
            
        return a, T, t_fall

    def update_info_labels(self):
        a, T, t = self.calculate_physics()
        self.lbl_acc.config(text=self.T("info_acc").format(abs(a)))
        self.lbl_tension.config(text=self.T("info_ten").format(T))
        if t == float('inf'):
            self.lbl_time.config(text=self.T("info_time_inf"))
        else:
            self.lbl_time.config(text=self.T("info_time").format(t))
            
        # Update FBD
        self.draw_fbd(a)

    def draw_fbd(self, a):
        self.ax_fbd.clear()
        self.ax_fbd.axis('off')
        self.ax_fbd.set_title(self.T("graph_title_fbd"))
        
        m1 = self.var_m1.get()
        m2 = self.var_m2.get()
        g = self.var_g.get()
        
        w1 = m1 * g
        w2 = m2 * g
        
        # Simple bars comparison
        labels = [self.T("lbl_w1"), self.T("lbl_w2")]
        values = [w1, w2]
        colors = ['#3498db', '#e74c3c'] if w2 > w1 else ['#e74c3c', '#3498db']
        
        self.ax_fbd.bar(labels, values, color=colors)
        if max(w1, w2) > 0:
            self.ax_fbd.set_ylim(0, max(w1, w2)*1.2)
        else:
            self.ax_fbd.set_ylim(0, 10)

        for i, v in enumerate(values):
            self.ax_fbd.text(i, v + 0.5, f"{v:.1f} N", ha='center')
            
        self.canvas_fbd.draw()

    def draw_system(self, pos_left, pos_right, pulley_angle=0):
        self.ax_sim.clear()
        # Pulley settings
        pulley_radius = 0.5
        pulley_x = 0
        pulley_y = 8
        # Draw Pulley (with simple 3D effect)
        circle = patches.Circle((pulley_x, pulley_y), pulley_radius, fill=True, color='#7f8c8d', zorder=2)
        self.ax_sim.add_patch(circle)
        # Pulley shadow
        shadow = patches.Ellipse((pulley_x, pulley_y-0.1), pulley_radius*2, 0.18, color='#555', alpha=0.2, zorder=1)
        self.ax_sim.add_patch(shadow)
        # Pulley axis
        self.ax_sim.plot([pulley_x], [pulley_y], 'ko', markersize=8, zorder=3)
        # Pulley spokes (rotating)
        for i in range(4):
            angle = pulley_angle + i*np.pi/2
            x0 = pulley_x + 0.1 * np.cos(angle)
            y0 = pulley_y + 0.1 * np.sin(angle)
            x1 = pulley_x + pulley_radius * np.cos(angle)
            y1 = pulley_y + pulley_radius * np.sin(angle)
            self.ax_sim.plot([x0, x1], [y0, y1], color='#333', lw=2, zorder=4)
        # Ceiling support
        self.ax_sim.plot([0, 0], [pulley_y, 10], 'k-', lw=3, zorder=0)
        self.ax_sim.plot([-2, 2], [10, 10], 'k-', lw=4, zorder=0)
        # Draw Ropes (dynamic, follow blocks)
        # Left rope
        rope_left_x = [-pulley_radius, -pulley_radius]
        rope_left_y = [pulley_y, pos_left + 0.4]
        self.ax_sim.plot(rope_left_x, rope_left_y, 'saddlebrown', lw=3, zorder=2)
        # Right rope
        rope_right_x = [pulley_radius, pulley_radius]
        rope_right_y = [pulley_y, pos_right + 0.4]
        self.ax_sim.plot(rope_right_x, rope_right_y, 'saddlebrown', lw=3, zorder=2)
        # Rope over pulley (arc, dynamic)
        theta = np.linspace(0, np.pi, 30)
        x_arc = pulley_radius * np.cos(theta)
        y_arc = pulley_y + pulley_radius * np.sin(theta)
        self.ax_sim.plot(x_arc, y_arc, 'saddlebrown', lw=3, zorder=2)
        # Draw Masses (Blocks) with 3D effect
        box_w = 0.8
        box_h = 0.8
        # Left Mass (m1)
        rect1 = patches.FancyBboxPatch((-pulley_radius - box_w/2, pos_left - box_h), box_w, box_h,
            boxstyle="round,pad=0.08", facecolor='#3498db', edgecolor='black', linewidth=2, zorder=5)
        self.ax_sim.add_patch(rect1)
        # Shadow
        self.ax_sim.add_patch(patches.Ellipse((-pulley_radius, pos_left - box_h - 0.1), 0.5, 0.08, color='#222', alpha=0.18, zorder=4))
        self.ax_sim.text(-pulley_radius, pos_left - box_h/2, f"m1\n{self.var_m1.get()}kg", ha='center', va='center', color='white', weight='bold', zorder=6)
        # Right Mass (m2)
        rect2 = patches.FancyBboxPatch((pulley_radius - box_w/2, pos_right - box_h), box_w, box_h,
            boxstyle="round,pad=0.08", facecolor='#e74c3c', edgecolor='black', linewidth=2, zorder=5)
        self.ax_sim.add_patch(rect2)
        self.ax_sim.add_patch(patches.Ellipse((pulley_radius, pos_right - box_h - 0.1), 0.5, 0.08, color='#222', alpha=0.18, zorder=4))
        self.ax_sim.text(pulley_radius, pos_right - box_h/2, f"m2\n{self.var_m2.get()}kg", ha='center', va='center', color='white', weight='bold', zorder=6)
        # Limit lines
        self.ax_sim.plot([-3, 3], [0, 0], 'k--', alpha=0.3, zorder=0)
        self.ax_sim.text(3.2, 0, self.T("lbl_ground"), fontsize=8, zorder=0)
        # Height labels
        self.ax_sim.text(-pulley_radius-1.1, pos_left, f"{pos_left:.2f} m", fontsize=9, color='#2980b9', va='center', zorder=7)
        self.ax_sim.text(pulley_radius+1.1, pos_right, f"{pos_right:.2f} m", fontsize=9, color='#c0392b', va='center', zorder=7)
        self.ax_sim.set_xlim(-4, 4)
        self.ax_sim.set_ylim(-1, 11)
        self.ax_sim.axis('off')
        self.canvas_sim.draw()

    def update_preview(self, event=None):
        if not self.is_running:
            self.draw_system(5.0, 5.0, pulley_angle=0) # Start positions equal
            self.update_info_labels()

    def run_animation(self):
        if self.ani is not None:
            self.ani.event_source.stop()
        self.is_running = True
        a, _, t_total = self.calculate_physics()
        start_y = 5.0
        h_limit = self.var_h.get()
        dt = 0.05
        total_time = t_total + 1.0
        if total_time > 10: total_time = 10
        frames = int(total_time / dt)
        def update(frame):
            t = frame * dt
            displacement = 0.5 * abs(a) * t**2
            # Pulley rotation: angle proportional to displacement
            pulley_angle = displacement / (np.pi * 0.5) * 2 * np.pi
            if a > 0:
                pos_left = start_y + displacement
                pos_right = start_y - displacement
            else:
                pos_left = start_y - displacement
                pos_right = start_y + displacement
            # Floor collision check
            if pos_left < 0: pos_left = 0
            if pos_right < 0: pos_right = 0
            # Pulley collision check
            if pos_left > 7: pos_left = 7
            if pos_right > 7: pos_right = 7
            # Rope bounce effect (simple)
            if pos_left == 0 or pos_right == 0:
                bounce = 0.1 * np.sin(10 * t) * np.exp(-2 * t)
                if pos_left == 0:
                    pos_left += bounce
                if pos_right == 0:
                    pos_right += bounce
            self.draw_system(pos_left, pos_right, pulley_angle=pulley_angle)
            self.ax_sim.set_title(f"t: {t:.2f}s | d: {displacement:.2f}m")
            if displacement >= h_limit:
                self.ani.event_source.stop()
                self.is_running = False
        self.ani = FuncAnimation(self.fig_sim, update, frames=frames, interval=dt*1000, repeat=False)
        self.canvas_sim.draw()

    def reset_animation(self):
        if self.ani is not None:
            self.ani.event_source.stop()
        self.is_running = False
        self.update_preview()

    # =========================================
    # TAB 2: ANALISIS DATA
    # =========================================
    def setup_analisis(self):
        pane = tk.PanedWindow(self.tab2, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(pane, padding=10)
        pane.add(left_frame, stretch="always")
        
        right_frame = ttk.Frame(pane, padding=10)
        pane.add(right_frame, stretch="always")

        # --- INPUTS ---
        ttk.Label(left_frame, text=self.T("title_log"), font=("Arial", 12, "bold")).pack(anchor="w", pady=10)
        
        input_box = ttk.LabelFrame(left_frame, text=self.T("lbl_input_box"))
        input_box.pack(fill="x", pady=5)
        
        # Grid input
        ttk.Label(input_box, text=self.T("lbl_m1_in")).grid(row=0, column=0, padx=5, pady=5)
        self.entry_m1_an = ttk.Entry(input_box, width=10)
        self.entry_m1_an.grid(row=0, column=1)
        
        ttk.Label(input_box, text=self.T("lbl_m2_in")).grid(row=1, column=0, padx=5, pady=5)
        self.entry_m2_an = ttk.Entry(input_box, width=10)
        self.entry_m2_an.grid(row=1, column=1) 
        
        ttk.Label(input_box, text=self.T("lbl_f_net_auto"), font=("Arial", 9, "italic")).grid(row=2, column=0, columnspan=2, pady=2)
        
        ttk.Label(input_box, text=self.T("lbl_a_meas")).grid(row=3, column=0, padx=5, pady=5)
        self.entry_a_an = ttk.Entry(input_box, width=10)
        self.entry_a_an.grid(row=3, column=1)

        ttk.Button(input_box, text=self.T("btn_add_data"), command=self.add_data_point).grid(row=4, column=0, columnspan=2, pady=10, sticky='ew')

        # Table
        cols = (self.T("col_m1"), self.T("col_m2"), self.T("col_mtot"), self.T("col_fnet"), self.T("col_auk"))
        self.tree = ttk.Treeview(left_frame, columns=cols, show="headings", height=12)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=60, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=10)
        
        ttk.Button(left_frame, text=self.T("btn_clear_data"), command=self.clear_data).pack(fill='x')

        # Graph
        self.fig_graph = Figure(figsize=(5, 4), dpi=100)
        self.ax_graph = self.fig_graph.add_subplot(111)
        self.canvas_graph = FigureCanvasTkAgg(self.fig_graph, master=right_frame)
        self.canvas_graph.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        if not hasattr(self, 'data_points'):
            self.data_points = [] # list of dicts

    def add_data_point(self):
        try:
            m1 = float(self.entry_m1_an.get().replace(',', '.'))
            m2 = float(self.entry_m2_an.get().replace(',', '.'))
            a_meas = float(self.entry_a_an.get().replace(',', '.'))
            g = 9.8
            
            m_total = m1 + m2
            f_net = abs(m2 - m1) * g
            
            self.data_points.append({'force': f_net, 'acc': a_meas, 'mass': m_total})
            self.tree.insert("", "end", values=(f"{m1:.2f}", f"{m2:.2f}", f"{m_total:.2f}", f"{f_net:.2f}", f"{a_meas:.2f}"))
            
            self.update_graph()
            
            # Clear inputs
            self.entry_a_an.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", self.T("err_valid"))

    def clear_data(self):
        self.data_points = []
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.ax_graph.clear()
        self.canvas_graph.draw()

    def update_graph(self):
        if len(self.data_points) < 2:
            return
            
        f_nets = np.array([d['force'] for d in self.data_points])
        ma_s   = np.array([d['mass'] * d['acc'] for d in self.data_points])
        
        coef = np.polyfit(ma_s, f_nets, 1)
        slope = coef[0]
        
        self.ax_graph.clear()
        self.ax_graph.scatter(ma_s, f_nets, color='blue', label=self.T("legend_data"))
        
        x_line = np.linspace(0, max(ma_s)*1.1, 50)
        y_line = coef[0]*x_line + coef[1]
        self.ax_graph.plot(x_line, y_line, 'r--', label=self.T("legend_fit").format(slope))
        
        self.ax_graph.set_title(self.T("graph_an_title"))
        self.ax_graph.set_xlabel(self.T("axis_x_an"))
        self.ax_graph.set_ylabel(self.T("axis_y_an"))
        self.ax_graph.legend()
        self.ax_graph.grid(True)
        self.canvas_graph.draw()
