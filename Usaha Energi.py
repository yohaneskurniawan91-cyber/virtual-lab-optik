import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

class VirtualLabUsahaEnergi:
    def __init__(self, parent):
        self.parent = parent
        
        # --- UI Styling ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#f5f6fa")
        style.configure("TLabel", background="#f5f6fa", foreground="#2c3e50", font=("Arial", 11))
        style.configure("Header.TLabel", font=("Arial", 14, "bold"), foreground="#2980b9")
        style.configure("TButton", font=("Arial", 11, "bold"), padding=6)
        
        self.setup_translations()
        self.lang = "ID"
        
        # Main Layout
        self.setup_ui()
        
        # Physics State
        self.running = False
        self.time = 0.0
        self.dt = 0.05
        self.mass = 10.0 # kg
        self.gravity = 9.8 
        self.friction_coef = 0.0
        
        # Track definition: Parabola y = 0.1 * x^2
        # Range x: -10 to 10
        self.track_x = np.linspace(-10, 10, 200)
        self.track_y = 0.05 * self.track_x**2
        
        # Initial State
        self.current_x = -8.0
        self.current_v = 0.0
        self.current_y = 0.05 * self.current_x**2
        self.thermal_energy = 0.0
        
        self.ani = None
        self.update_params()

    def setup_translations(self):
        self.translations = {
            "ID": {
                "title_control": "KONTROL SIMULASI",
                "lbl_mass": "Massa Benda (kg):",
                "lbl_pos_start": "Posisi Awal (X):",
                "lbl_gravity": "Gravitasi (m/s²):",
                "lbl_friction": "Koefisien Gesek Komposit:",
                "lbl_friction_val": "{:.2f} (Licin)",
                "btn_start": "MULAI",
                "btn_resume": "LANJUTKAN",
                "btn_pause": "PAUSE",
                "btn_reset": "RESET",
                "btn_done": "MULAI (Selesai)",
                "info_ready": "Siap Simulasi...",
                "info_pos_x": "Posisi X : {:.2f} m\n",
                "info_pos_y": "Posisi Y : {:.2f} m\n",
                "info_vel": "Kecepatan: {:.2f} m/s\n",
                "info_sep": "-----------------\n",
                "info_pe": "Energi Potensial : {:.1f} J\n",
                "info_ke": "Energi Kinetik   : {:.1f} J\n",
                "info_heat": "Energi Panas     : {:.1f} J\n",
                "info_total": "TOTAL ENERGI     : {:.1f} J",
                "graph_title": "Simulasi Lintasan Skate (Hukum Kekekalan Energi)",
                "axis_x": "Jarak Horizontal (m)",
                "axis_y": "Ketinggian (m)",
                "axis_eng": "Energi (Joule)",
                "cat_ke": "Kinetik",
                "cat_pe": "Potensial",
                "cat_heat": "Panas",
                "cat_total": "Total"
            },
            "EN": {
                "title_control": "SIMULATION CONTROL",
                "lbl_mass": "Object Mass (kg):",
                "lbl_pos_start": "Start Position (X):",
                "lbl_gravity": "Gravity (m/s²):",
                "lbl_friction": "Friction Coefficient:",
                "lbl_friction_val": "{:.2f} (Smooth)",
                "btn_start": "START",
                "btn_resume": "RESUME",
                "btn_pause": "PAUSE",
                "btn_reset": "RESET",
                "btn_done": "START (Done)",
                "info_ready": "Ready to Simulate...",
                "info_pos_x": "Position X : {:.2f} m\n",
                "info_pos_y": "Position Y : {:.2f} m\n",
                "info_vel": "Velocity: {:.2f} m/s\n",
                "info_sep": "-----------------\n",
                "info_pe": "Potential Energy : {:.1f} J\n",
                "info_ke": "Kinetic Energy   : {:.1f} J\n",
                "info_heat": "Thermal Energy   : {:.1f} J\n",
                "info_total": "TOTAL ENERGY     : {:.1f} J",
                "graph_title": "Skate Path Simulation (Conservation of Energy)",
                "axis_x": "Horizontal Distance (m)",
                "axis_y": "Height (m)",
                "axis_eng": "Energy (Joule)",
                "cat_ke": "Kinetic",
                "cat_pe": "Potential",
                "cat_heat": "Thermal",
                "cat_total": "Total"
            }
        }

    def T(self, key):
        return self.translations[self.lang].get(key, key)

    def setup_ui(self):
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Split: Controls (Left) vs Visualization (Right)
        paned = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True)
        
        self.left_panel = ttk.Frame(paned, width=350, relief="groove", padding=15)
        self.right_panel = ttk.Frame(paned, relief="flat")
        paned.add(self.left_panel, weight=1)
        paned.add(self.right_panel, weight=3)
        
        self.setup_controls()
        self.setup_visualization()

    def set_language(self, lang):
        self.lang = lang
        if self.running:
            self.toggle_simulation()
        self.main_frame.destroy()
        self.setup_ui()
        self.update_params()
        self.draw_frame()
        self.update_info()

    def setup_controls(self):
        lbl_title = ttk.Label(self.left_panel, text=self.T("title_control"), style="Header.TLabel")
        lbl_title.pack(pady=(0, 20), anchor="w")
        
        # 1. Slider Massa
        ttk.Label(self.left_panel, text=self.T("lbl_mass")).pack(anchor="w")
        if not hasattr(self, 'var_mass'): self.var_mass = tk.DoubleVar(value=10.0)
        sld_mass = ttk.Scale(self.left_panel, from_=1.0, to=50.0, variable=self.var_mass, command=self.update_params)
        sld_mass.pack(fill="x", pady=(0, 5))
        self.lbl_mass = ttk.Label(self.left_panel, text="10.0 kg", font=("Consolas", 10))
        self.lbl_mass.pack(anchor="e", pady=(0, 15))
        
        # 2. Slider Posisi Awal (Height control via X)
        ttk.Label(self.left_panel, text=self.T("lbl_pos_start")).pack(anchor="w")
        if not hasattr(self, 'var_start_x'): self.var_start_x = tk.DoubleVar(value=-8.0)
        sld_pos = ttk.Scale(self.left_panel, from_=-9.5, to=-1.0, variable=self.var_start_x, command=self.update_params)
        sld_pos.pack(fill="x", pady=(0, 5))
        self.lbl_pos = ttk.Label(self.left_panel, text="x = -8.0 m", font=("Consolas", 10))
        self.lbl_pos.pack(anchor="e", pady=(0, 15))
        
        # 3. Slider Gravitasi
        ttk.Label(self.left_panel, text=self.T("lbl_gravity")).pack(anchor="w")
        if not hasattr(self, 'var_grav'): self.var_grav = tk.DoubleVar(value=9.8)
        sld_grav = ttk.Scale(self.left_panel, from_=1.6, to=20.0, variable=self.var_grav, command=self.update_params)
        sld_grav.pack(fill="x", pady=(0, 5))
        self.lbl_grav = ttk.Label(self.left_panel, text="9.8 m/s²", font=("Consolas", 10))
        self.lbl_grav.pack(anchor="e", pady=(0, 15))
        
        # 4. Slider Gesekan
        ttk.Label(self.left_panel, text=self.T("lbl_friction")).pack(anchor="w")
        if not hasattr(self, 'var_fric'): self.var_fric = tk.DoubleVar(value=0.0)
        sld_fric = ttk.Scale(self.left_panel, from_=0.0, to=0.5, variable=self.var_fric, command=self.update_params)
        sld_fric.pack(fill="x", pady=(0, 5))
        self.lbl_fric = ttk.Label(self.left_panel, text=self.T("lbl_friction_val").format(0.0), font=("Consolas", 10))
        self.lbl_fric.pack(anchor="e", pady=(0, 20))
        
        # Buttons
        btn_frame = ttk.Frame(self.left_panel)
        btn_frame.pack(fill="x", pady=10)
        
        self.btn_start = ttk.Button(btn_frame, text=self.T("btn_start"), command=self.toggle_simulation)
        self.btn_start.pack(side="left", fill="x", expand=True, padx=2)
        
        self.btn_reset = ttk.Button(btn_frame, text=self.T("btn_reset"), command=self.reset_simulation)
        self.btn_reset.pack(side="left", fill="x", expand=True, padx=2)
        
        # Info Box
        self.info_box = tk.Text(self.left_panel, height=8, bg="#ecf0f1", relief="flat", font=("Consolas", 10))
        self.info_box.pack(fill="both", expand=True, pady=10)
        self.info_box.insert("1.0", self.T("info_ready"))

    def setup_visualization(self):
        # Create Figure with 2 subplots: 1. Main Animation, 2. Energy Bars
        self.fig = plt.Figure(figsize=(8, 6), dpi=100)
        self.fig.patch.set_facecolor('#f5f6fa')
        
        # GridSpec layout
        gs = self.fig.add_gridspec(2, 1, height_ratios=[3, 1])
        
        # Main Visual (Track)
        self.ax_sim = self.fig.add_subplot(gs[0])
        self.ax_sim.set_facecolor('#dff9fb')
        
        # Energy Chart
        self.ax_bar = self.fig.add_subplot(gs[1])
        self.ax_bar.set_facecolor('#f5f6fa')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_params(self, event=None):
        m = self.var_mass.get()
        x0 = self.var_start_x.get()
        g = self.var_grav.get()
        mu = self.var_fric.get()
        
        self.lbl_mass.config(text=f"{m:.1f} kg")
        self.lbl_pos.config(text=f"x = {x0:.1f} m")
        self.lbl_grav.config(text=f"{g:.1f} m/s²")
        if mu == 0:
             self.lbl_fric.config(text=self.T("lbl_friction_val").format(mu))
        else:
             self.lbl_fric.config(text=f"{mu:.2f}")
        
        if not self.running:
            self.reset_simulation()

    def reset_simulation(self):
        self.running = False
        self.btn_start.config(text=self.T("btn_start"))
        
        # Set Values
        self.mass = self.var_mass.get()
        self.current_x = self.var_start_x.get()
        self.current_y = 0.05 * self.current_x**2
        self.current_v = 0.0
        self.gravity = self.var_grav.get()
        self.friction_coef = self.var_fric.get()
        self.thermal_energy = 0.0
        
        self.draw_frame()
        self.update_info()

    def toggle_simulation(self):
        if self.running:
            self.running = False
            self.btn_start.config(text=self.T("btn_resume"))
            if self.ani:
                self.ani.event_source.stop()
        else:
            self.running = True
            self.btn_start.config(text=self.T("btn_pause"))
            self.ani = FuncAnimation(self.fig, self.animate_step, interval=30, blit=False, cache_frame_data=False)

    def animate_step(self, frame):
        if not self.running:
            return
            
        # Physics Update (Simple Euler Integration for demonstration)
        # Slope angle theta
        # dy/dx = 0.1 * x
        slope = 0.1 * self.current_x
        angle = np.arctan(slope)
        
        # Forces
        # Gravity along slope: mg sin(theta)
        f_grav = -self.mass * self.gravity * np.sin(angle)
        
        # Friction: - mu * N * direction of v
        # N = mg cos(theta) + Centripetal Force (mv^2/R) -- simplified to just mg cos(theta) for stability in this demos
        normal_force = self.mass * self.gravity * np.cos(angle)
        f_fric_mag = self.friction_coef * normal_force
        
        if abs(self.current_v) > 0.01:
            f_fric = -np.sign(self.current_v) * f_fric_mag
        else:
            f_fric = 0 # Static friction simplified
            
        f_total = f_grav + f_fric
        acc = f_total / self.mass
        
        # Update motion
        self.current_v += acc * self.dt
        
        # Move along x projected (approximation for small slope changes)
        # dx = ds * cos(theta) = (v * dt) * cos(theta)
        dx = self.current_v * self.dt * np.cos(angle)
        self.current_x += dx
        
        # Clamp bounds
        if self.current_x > 10: 
            self.current_x = 10
            self.current_v = 0
            self.running = False
            self.btn_start.config(text=self.T("btn_done"))
        elif self.current_x < -10:
            self.current_x = -10
            self.current_v = 0
        
        self.current_y = 0.05 * self.current_x**2
        
        # Energy Calc
        # Work done by friction -> Thermal
        # W = F * d
        ds = abs(self.current_v * self.dt)
        if abs(self.current_v) > 0.001:
            d_thermal = f_fric_mag * ds
            self.thermal_energy += d_thermal
        
        self.draw_frame()
        self.update_info()

    def update_info(self):
        ke = 0.5 * self.mass * self.current_v**2
        pe = self.mass * self.gravity * (self.current_y + 5) # Offset +5 visual reference
        # Note: simulation y is 0 at bottom.
        
        te = ke + pe + self.thermal_energy
        
        txt = self.T("info_pos_x").format(self.current_x)
        txt += self.T("info_pos_y").format(self.current_y)
        txt += self.T("info_vel").format(self.current_v)
        txt += self.T("info_sep")
        txt += self.T("info_pe").format(pe)
        txt += self.T("info_ke").format(ke)
        txt += self.T("info_heat").format(self.thermal_energy)
        txt += self.T("info_total").format(te)
        
        self.info_box.delete("1.0", tk.END)
        self.info_box.insert("1.0", txt)

    def draw_frame(self):
        self.ax_sim.clear()
        self.ax_bar.clear()
        
        # 1. Visualization
        self.ax_sim.set_xlim(-11, 11)
        self.ax_sim.set_ylim(-1, 8)
        self.ax_sim.set_aspect('equal')
        self.ax_sim.set_title(self.T("graph_title"), fontsize=12, fontweight='bold')
        self.ax_sim.grid(True, alpha=0.3, which='both', linestyle='--')
        self.ax_sim.set_xlabel(self.T("axis_x"))
        self.ax_sim.set_ylabel(self.T("axis_y"))
        
        # Draw Track
        self.ax_sim.plot(self.track_x, self.track_y, color='#7f8c8d', linewidth=5) # Track tebal
        self.ax_sim.fill_between(self.track_x, -2, self.track_y, color='#ecf0f1', alpha=0.5) # Tanah
        
        # Draw Skater/Ball
        circle = patches.Circle((self.current_x, self.current_y + 0.3), 0.4, facecolor='#e74c3c', edgecolor='black', zorder=5)
        self.ax_sim.add_patch(circle)
        
        # 2. Bar Chart
        pe = self.mass * self.gravity * (self.current_y + 5) # PE relative to -5m
        ke = 0.5 * self.mass * self.current_v**2
        th = self.thermal_energy
        total = pe + ke + th
        
        categories = [self.T("cat_ke"), self.T("cat_pe"), self.T("cat_heat"), self.T("cat_total")]
        values = [ke, pe, th, total]
        colors = ['#2ecc71', '#3498db', '#e67e22', '#9b59b6']
        
        bars = self.ax_bar.barh(categories, values, color=colors, height=0.6)
        
        # Dynamic X Limit for Bar Chart
        max_val = max(100, total * 1.3)
        self.ax_bar.set_xlim(0, max_val) 
        self.ax_bar.set_xlabel(self.T("axis_eng"))
        self.ax_bar.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            self.ax_bar.text(width + (max_val*0.02), bar.get_y() + bar.get_height()/2, f'{width:.0f}', va='center', fontsize=9, fontweight='bold')

        self.canvas.draw()
