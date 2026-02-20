import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

class VirtualLabGerakMenggelinding:
    def __init__(self, parent):
        self.parent = parent
        
        # --- UI Styling ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#f5f6fa")
        style.configure("TLabel", background="#f5f6fa", foreground="#2c3e50", font=("Arial", 11))
        style.configure("Header.TLabel", font=("Arial", 14, "bold"), foreground="#e67e22")
        style.configure("TButton", font=("Arial", 11, "bold"), padding=6)
        
        self.setup_translations()
        self.lang = "ID"
        
        # Main Layout
        self.setup_ui()
        
        # Physics State
        self.running = False
        self.time = 0.0
        self.dt = 0.05
        
        # Parameters
        self.theta = 30.0 # degrees
        self.mass = 2.0   # kg
        self.radius = 0.5 # m
        self.k = 0.5      # Silinder Pejal (1/2) default
        self.g = 9.8
        
        # Initial State
        self.pos_s = 0.0  # distance along incline
        self.vel = 0.0
        self.theta_rot = 0.0 # rotation angle
        
        self.ani = None
        # Arrays for graphing
        self.t_data = []
        self.v_data = []

        self.update_params()

    def setup_translations(self):
        self.translations = {
            "ID": {
                "title_main": "GERAK MENGGELINDING",
                "lbl_shape": "Bentuk Benda:",
                "lbl_theta": "Sudut Kemiringan (θ°):",
                "lbl_mass": "Massa (kg):",
                "lbl_radius": "Jari-jari (m):",
                "btn_start": "MULAI",
                "btn_resume": "LANJUTKAN",
                "btn_pause": "PAUSE",
                "btn_reset": "RESET",
                "btn_done": "MULAI (Selesai)",
                "graph_title_vel": "Kecepatan vs Waktu",
                "graph_title_eng": "Energi Kinetik (J)",
                "graph_sim_title": "Simulasi Gerak Menggelinding",
                "axis_t": "t (s)",
                "axis_v": "v (m/s)",
                "eng_trans": "Trans.",
                "eng_rot": "Rotasi",
                "info_time": "Waktu: {:.2f} s\n",
                "info_dist": "Jarak: {:.2f} m\n",
                "info_vel": "Kecepatan: {:.2f} m/s\n",
                "info_acc": "Percepatan: {:.2f} m/s²\n",
                "info_sep": "-----------------\n",
                "info_ket": "KE Trans: {:.2f} J\n",
                "info_ker": "KE Rotasi: {:.2f} J\n",
                "info_ketot": "KE Total: {:.2f} J",
                "shape1": "Silinder Pejal (k=0.5)",
                "shape2": "Silinder Berongga (k=1.0)",
                "shape3": "Bola Pejal (k=0.4)",
                "shape4": "Bola Berongga (k=0.67)"
            },
            "EN": {
                "title_main": "ROLLING MOTION",
                "lbl_shape": "Object Shape:",
                "lbl_theta": "Incline Angle (θ°):",
                "lbl_mass": "Mass (kg):",
                "lbl_radius": "Radius (m):",
                "btn_start": "START",
                "btn_resume": "RESUME",
                "btn_pause": "PAUSE",
                "btn_reset": "RESET",
                "btn_done": "START (Done)",
                "graph_title_vel": "Velocity vs Time",
                "graph_title_eng": "Kinetic Energy (J)",
                "graph_sim_title": "Rolling Motion Simulation",
                "axis_t": "t (s)",
                "axis_v": "v (m/s)",
                "eng_trans": "Trans.",
                "eng_rot": "Rotation",
                "info_time": "Time: {:.2f} s\n",
                "info_dist": "Distance: {:.2f} m\n",
                "info_vel": "Velocity: {:.2f} m/s\n",
                "info_acc": "Acceleration: {:.2f} m/s²\n",
                "info_sep": "-----------------\n",
                "info_ket": "KE Trans: {:.2f} J\n",
                "info_ker": "KE Rot: {:.2f} J\n",
                "info_ketot": "KE Total: {:.2f} J",
                "shape1": "Solid Cylinder (k=0.5)",
                "shape2": "Hollow Cylinder (k=1.0)",
                "shape3": "Solid Sphere (k=0.4)",
                "shape4": "Hollow Sphere (k=0.67)"
            }
        }
        self.shape_keys = ["shape1", "shape2", "shape3", "shape4"]
        self.shape_k = { "shape1": 0.5, "shape2": 1.0, "shape3": 0.4, "shape4": 2/3 }

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
        self.update_info()
        self.draw_frame()

    def setup_controls(self):
        lbl_title = ttk.Label(self.left_panel, text=self.T("title_main"), style="Header.TLabel")
        lbl_title.pack(pady=(0, 20), anchor="w")
        
        # 1. Shape Selection (Constant k)
        ttk.Label(self.left_panel, text=self.T("lbl_shape")).pack(anchor="w")
        
        shapes = [self.T(k) for k in self.shape_keys]
        self.cb_shape = ttk.Combobox(self.left_panel, values=shapes, state="readonly")
        self.cb_shape.current(0)
        self.cb_shape.pack(fill="x", pady=(0, 15))
        self.cb_shape.bind("<<ComboboxSelected>>", self.update_params)
        
        # 2. Angle Slider
        ttk.Label(self.left_panel, text=self.T("lbl_theta")).pack(anchor="w")
        if not hasattr(self, 'var_theta'): self.var_theta = tk.DoubleVar(value=30.0)
        self.slider_theta = ttk.Scale(self.left_panel, from_=5.0, to=60.0, variable=self.var_theta, command=self.update_params)
        self.slider_theta.pack(fill="x", pady=(0, 5))
        self.lbl_theta = ttk.Label(self.left_panel, text="30.0°", font=("Consolas", 10))
        self.lbl_theta.pack(anchor="e", pady=(0, 15))
        
        # 3. Mass Slider
        ttk.Label(self.left_panel, text=self.T("lbl_mass")).pack(anchor="w")
        if not hasattr(self, 'var_mass'): self.var_mass = tk.DoubleVar(value=2.0)
        ttk.Scale(self.left_panel, from_=0.1, to=10.0, variable=self.var_mass, command=self.update_params).pack(fill="x")
        self.lbl_mass = ttk.Label(self.left_panel, text="2.0 kg", font=("Consolas", 10))
        self.lbl_mass.pack(anchor="e", pady=(0, 15))
        
        # 4. Radius Slider
        ttk.Label(self.left_panel, text=self.T("lbl_radius")).pack(anchor="w")
        if not hasattr(self, 'var_rad'): self.var_rad = tk.DoubleVar(value=0.5)
        ttk.Scale(self.left_panel, from_=0.1, to=1.0, variable=self.var_rad, command=self.update_params).pack(fill="x")
        self.lbl_rad = ttk.Label(self.left_panel, text="0.5 m", font=("Consolas", 10))
        self.lbl_rad.pack(anchor="e", pady=(0, 20))
        
        # Buttons
        btn_frame = ttk.Frame(self.left_panel)
        btn_frame.pack(fill="x", pady=10)
        
        self.btn_start = ttk.Button(btn_frame, text=self.T("btn_start"), command=self.toggle_simulation)
        self.btn_start.pack(side="left", fill="x", expand=True, padx=2)
        
        self.btn_reset = ttk.Button(btn_frame, text=self.T("btn_reset"), command=self.reset_simulation)
        self.btn_reset.pack(side="left", fill="x", expand=True, padx=2)
        
        # Info Box
        self.info_box = tk.Text(self.left_panel, height=8, bg="#ecf0f1", relief="flat", font=("Consolas", 9))
        self.info_box.pack(fill="both", expand=True, pady=10)

    def setup_visualization(self):
        # Create Figure
        self.fig = plt.Figure(figsize=(8, 6), dpi=100)
        self.fig.patch.set_facecolor('#f5f6fa')
        
        gs = self.fig.add_gridspec(2, 2, height_ratios=[2, 1])
        
        # 1. Main Simulation (Top)
        self.ax_sim = self.fig.add_subplot(gs[0, :])
        self.ax_sim.set_facecolor('white')
        
        # 2. Velocity Graph (Bottom Left)
        self.ax_vel = self.fig.add_subplot(gs[1, 0])
        self.ax_vel.set_facecolor('#f5f6fa')
        
        # 3. Energy Graph (Bottom Right)
        self.ax_eng = self.fig.add_subplot(gs[1, 1])
        self.ax_eng.set_facecolor('#f5f6fa')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_params(self, event=None):
        self.theta = self.var_theta.get()
        self.mass = self.var_mass.get()
        self.radius = self.var_rad.get()
        
        idx = self.cb_shape.current()
        if idx < 0: idx = 0
        key = self.shape_keys[idx]
        self.k = self.shape_k[key]
        
        self.lbl_theta.config(text=f"{self.theta:.1f}°")
        self.lbl_mass.config(text=f"{self.mass:.1f} kg")
        self.lbl_rad.config(text=f"{self.radius:.2f} m")
        
        if not self.running:
            self.reset_simulation()

    def reset_simulation(self):
        self.running = False
        self.btn_start.config(text=self.T("btn_start"))
        self.time = 0.0
        self.pos_s = 0.0
        self.vel = 0.0
        self.theta_rot = 0.0
        
        # Arrays for graphing
        self.t_data = []
        self.v_data = []
        
        # self.update_params() - Removed to avoid recursion loop
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
            
        # Physics Update
        # a = (g * sin(theta)) / (1 + k)
        rad_theta = np.radians(self.theta)
        acc = (self.g * np.sin(rad_theta)) / (1 + self.k)
        
        self.vel += acc * self.dt
        ds = self.vel * self.dt
        self.pos_s += ds
        
        # Rotation: ds = R * d_theta -> d_theta = ds / R
        d_theta_rot = ds / self.radius
        self.theta_rot -= d_theta_rot # Rotate clockwise (negative)
        
        self.time += self.dt
        
        # Data recording
        self.t_data.append(self.time)
        self.v_data.append(self.vel)
        
        # Stop if off screen (approx 10m track visually)
        if self.pos_s > 12.0:
            self.running = False
            self.btn_start.config(text=self.T("btn_done"))
            
        self.draw_frame()
        self.update_info()

    def update_info(self):
        # Calculate Energies
        ke_trans = 0.5 * self.mass * self.vel**2
        ke_rot = 0.5 * self.k * self.mass * self.vel**2
        ke_total = ke_trans + ke_rot
        
        # Theoretical Acceleration
        rad_theta = np.radians(self.theta)
        acc = (self.g * np.sin(rad_theta)) / (1 + self.k)
        
        txt = self.T("info_time").format(self.time)
        txt += self.T("info_dist").format(self.pos_s)
        txt += self.T("info_vel").format(self.vel)
        txt += self.T("info_acc").format(acc)
        txt += self.T("info_sep")
        txt += self.T("info_ket").format(ke_trans)
        txt += self.T("info_ker").format(ke_rot)
        txt += self.T("info_ketot").format(ke_total)
        
        self.info_box.delete("1.0", tk.END)
        self.info_box.insert("1.0", txt)

    def draw_frame(self):
        self.ax_sim.clear()
        self.ax_vel.clear()
        self.ax_eng.clear()
        
        # 1. Main Simulation (Inclined Plane)
        self.ax_sim.set_xlim(-1, 11)
        self.ax_sim.set_ylim(-1, 7)
        self.ax_sim.set_aspect('equal')
        self.ax_sim.axis('off')
        self.ax_sim.set_title(self.T("graph_sim_title"), fontweight='bold')
        
        # Draw Slope (Triangle)
        L = 10.0
        rad_theta = np.radians(self.theta)
        H = L * np.sin(rad_theta)
        W = L * np.cos(rad_theta)
        
        self.ax_sim.plot([0, W], [H, 0], color='#2c3e50', linewidth=3) # The Slope
        self.ax_sim.plot([0, W], [0, 0], color='black', linewidth=1, linestyle='--') # Floor ground reference
        
        curr_s = self.pos_s
        x_surf = curr_s * np.cos(rad_theta)
        y_surf = H - curr_s * np.sin(rad_theta)
        
        nx = np.sin(rad_theta)
        ny = np.cos(rad_theta)
        
        cx = x_surf + self.radius * nx
        cy = y_surf + self.radius * ny
        
        circle_col = '#e67e22'
        circle = patches.Circle((cx, cy), self.radius, facecolor=circle_col, edgecolor='black', linewidth=1.5)
        self.ax_sim.add_patch(circle)
        
        marker_x = cx + self.radius * np.cos(self.theta_rot)
        marker_y = cy + self.radius * np.sin(self.theta_rot)
        self.ax_sim.plot([cx, marker_x], [cy, marker_y], color='white', linewidth=2)
        
        # 2. Velocity Graph
        self.ax_vel.set_title(self.T("graph_title_vel"), fontsize=9)
        self.ax_vel.set_xlabel(self.T("axis_t"), fontsize=8)
        self.ax_vel.set_ylabel(self.T("axis_v"), fontsize=8)
        self.ax_vel.grid(True, alpha=0.3)
        if len(self.t_data) > 0:
            self.ax_vel.plot(self.t_data, self.v_data, color='#e74c3c', linewidth=2)
            
        # 3. Energy Bar Chart (Instantaneous)
        ke_trans = 0.5 * self.mass * self.vel**2
        ke_rot = 0.5 * self.k * self.mass * self.vel**2
        
        names = [self.T("eng_trans"), self.T("eng_rot")]
        vals = [ke_trans, ke_rot]
        colors = ['#3498db', '#9b59b6']
        
        self.ax_eng.bar(names, vals, color=colors, width=0.5)
        self.ax_eng.set_title(self.T("graph_title_eng"), fontsize=9)
        # Dynamic limit
        total_ke = ke_trans + ke_rot
        if total_ke > 0:
            self.ax_eng.set_ylim(0, total_ke * 1.5)
        else:
            self.ax_eng.set_ylim(0, 10)

        self.canvas.draw()
