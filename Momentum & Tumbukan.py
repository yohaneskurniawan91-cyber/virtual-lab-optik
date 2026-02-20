import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

class VirtualLabMomentum:
    def __init__(self, parent):
        self.parent = parent
        
        # --- UI Styling ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#f5f6fa")
        style.configure("TLabel", background="#f5f6fa", foreground="#2c3e50", font=("Arial", 11))
        style.configure("Header.TLabel", font=("Arial", 14, "bold"), foreground="#e74c3c")
        style.configure("TButton", font=("Arial", 11, "bold"), padding=6)
        
        self.setup_translations()
        self.lang = "ID"
        
        # Main Layout
        self.setup_ui()
        
        # Physics State
        self.running = False
        self.time = 0.0
        self.dt = 0.05
        
        # Initial Parameters (Default)
        self.m1 = 2.0; self.v1_init = 3.0
        self.m2 = 2.0; self.v2_init = -3.0
        self.e = 1.0 # Elasticity
        
        # Current State
        self.x1 = -5.0; self.v1 = self.v1_init
        self.x2 = 5.0;  self.v2 = self.v2_init
        self.collided = False
        
        self.ani = None
        self.reset_simulation()
        
    def setup_translations(self):
        self.translations = {
            "ID": {
                "title_controls": "KONTROL TUMBUKAN",
                "obj1_title": "Benda 1 (Merah)",
                "obj2_title": "Benda 2 (Biru)",
                "lbl_mass": "Massa (kg):",
                "lbl_vel": "Kecepatan Awal (m/s):",
                "lbl_e": "Koefisien Restitusi (e):",
                "e_perfect": "Elastis Sempurna",
                "e_part": "Elastis Sebagian",
                "e_inelastic": "Tidak Elastis Sama Sekali",
                "btn_start": "MULAI",
                "btn_continue": "LANJUTKAN",
                "btn_pause": "PAUSE",
                "btn_reset": "RESET",
                "btn_done": "MULAI (Selesai)",
                "graph_mom_title": "Momentum (kg·m/s)",
                "graph_eng_title": "Energi Kinetik (J)",
                "graph_sim_title": "Simulasi Tumbukan",
                "info_time": "Waktu: {:.2f} s\n",
                "info_obj1": "----- Benda 1 (Merah) -----\n",
                "info_v1": "V1: {:.2f} m/s\n",
                "info_p1": "P1: {:.2f} kg.m/s\n",
                "info_obj2": "----- Benda 2 (Biru) -----\n",
                "info_v2": "V2: {:.2f} m/s\n",
                "info_p2": "P2: {:.2f} kg.m/s\n",
                "info_line": "-------------------\n",
                "info_ptot": "Momentum Total: {:.2f}\n",
                "info_ketot": "Energi Kinetik: {:.2f} J"
            },
            "EN": {
                "title_controls": "COLLISION CONTROLS",
                "obj1_title": "Object 1 (Red)",
                "obj2_title": "Object 2 (Blue)",
                "lbl_mass": "Mass (kg):",
                "lbl_vel": "Initial Velocity (m/s):",
                "lbl_e": "Restitution Coeff (e):",
                "e_perfect": "Perfectly Elastic",
                "e_part": "Partially Elastic",
                "e_inelastic": "Perfectly Inelastic",
                "btn_start": "START",
                "btn_continue": "RESUME",
                "btn_pause": "PAUSE",
                "btn_reset": "RESET",
                "btn_done": "START (Done)",
                "graph_mom_title": "Momentum (kg·m/s)",
                "graph_eng_title": "Kinetic Energy (J)",
                "graph_sim_title": "Collision Simulation",
                "info_time": "Time: {:.2f} s\n",
                "info_obj1": "----- Object 1 (Red) -----\n",
                "info_v1": "V1: {:.2f} m/s\n",
                "info_p1": "P1: {:.2f} kg.m/s\n",
                "info_obj2": "----- Object 2 (Blue) -----\n",
                "info_v2": "V2: {:.2f} m/s\n",
                "info_p2": "P2: {:.2f} kg.m/s\n",
                "info_line": "-------------------\n",
                "info_ptot": "Total Momentum: {:.2f}\n",
                "info_ketot": "Kinetic Energy: {:.2f} J"
            }
        }
        
    def T(self, key):
        return self.translations[self.lang].get(key, key)
        
    def setup_ui(self):
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
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
        
        # Re-set strings... but complex here since labels are anonymous.
        # But setup_controls recreates labels IF we clear left_panel children.
        # Let's simple DESTROY main_frame and rebuild.
        
        if self.running:
             self.toggle_simulation()
             
        self.main_frame.destroy()
        self.setup_ui()
        # Restore params visualization
        self.update_params()
        self.update_info()
        self.draw_frame()

    def setup_controls(self):
        lbl_title = ttk.Label(self.left_panel, text=self.T("title_controls"), style="Header.TLabel")
        lbl_title.pack(pady=(0, 20), anchor="w")
        
        # Object 1 (Red)
        lbl_obj1 = ttk.Label(self.left_panel, text=self.T("obj1_title"), font=("Arial", 11, "bold"), foreground="#e74c3c")
        lbl_obj1.pack(anchor="w", pady=(5,0))
        
        ttk.Label(self.left_panel, text=self.T("lbl_mass")).pack(anchor="w")
        if not hasattr(self, 'var_m1'): self.var_m1 = tk.DoubleVar(value=2.0)
        ttk.Scale(self.left_panel, from_=0.5, to=10.0, variable=self.var_m1, command=self.update_params).pack(fill="x")
        self.lbl_m1 = ttk.Label(self.left_panel, text="2.0 kg", font=("Consolas", 10))
        self.lbl_m1.pack(anchor="e")
        
        ttk.Label(self.left_panel, text=self.T("lbl_vel")).pack(anchor="w")
        if not hasattr(self, 'var_v1'): self.var_v1 = tk.DoubleVar(value=3.0)
        ttk.Scale(self.left_panel, from_=0.0, to=10.0, variable=self.var_v1, command=self.update_params).pack(fill="x")
        self.lbl_v1 = ttk.Label(self.left_panel, text="3.0 m/s", font=("Consolas", 10))
        self.lbl_v1.pack(anchor="e", pady=(0, 10))

        # Object 2 (Blue)
        lbl_obj2 = ttk.Label(self.left_panel, text=self.T("obj2_title"), font=("Arial", 11, "bold"), foreground="#3498db")
        lbl_obj2.pack(anchor="w", pady=(5,0))
        
        ttk.Label(self.left_panel, text=self.T("lbl_mass")).pack(anchor="w")
        if not hasattr(self, 'var_m2'): self.var_m2 = tk.DoubleVar(value=2.0)
        ttk.Scale(self.left_panel, from_=0.5, to=10.0, variable=self.var_m2, command=self.update_params).pack(fill="x")
        self.lbl_m2 = ttk.Label(self.left_panel, text="2.0 kg", font=("Consolas", 10))
        self.lbl_m2.pack(anchor="e")
        
        ttk.Label(self.left_panel, text=self.T("lbl_vel")).pack(anchor="w")
        if not hasattr(self, 'var_v2'): self.var_v2 = tk.DoubleVar(value=-3.0)
        ttk.Scale(self.left_panel, from_=-10.0, to=0.0, variable=self.var_v2, command=self.update_params).pack(fill="x")
        self.lbl_v2 = ttk.Label(self.left_panel, text="-3.0 m/s", font=("Consolas", 10))
        self.lbl_v2.pack(anchor="e", pady=(0, 10))
        
        # Coefficient of Restitution
        ttk.Label(self.left_panel, text=self.T("lbl_e")).pack(anchor="w")
        if not hasattr(self, 'var_e'): self.var_e = tk.DoubleVar(value=1.0)
        ttk.Scale(self.left_panel, from_=0.0, to=1.0, variable=self.var_e, command=self.update_params).pack(fill="x")
        self.lbl_e = ttk.Label(self.left_panel, text=f"1.00 ({self.T('e_perfect')})", font=("Consolas", 10))
        self.lbl_e.pack(anchor="e", pady=(0, 20))
        
        # Buttons
        btn_frame = ttk.Frame(self.left_panel)
        btn_frame.pack(fill="x", pady=10)
        
        self.btn_start = ttk.Button(btn_frame, text=self.T("btn_start"), command=self.toggle_simulation)
        self.btn_start.pack(side="left", fill="x", expand=True, padx=2)
        
        self.btn_reset = ttk.Button(btn_frame, text=self.T("btn_reset"), command=self.reset_simulation)
        self.btn_reset.pack(side="left", fill="x", expand=True, padx=2)
        
        # Info Box
        self.info_box = tk.Text(self.left_panel, height=10, bg="#ecf0f1", relief="flat", font=("Consolas", 9))
        self.info_box.pack(fill="both", expand=True, pady=10)

    def setup_visualization(self):
        # Create Figure
        self.fig = plt.Figure(figsize=(8, 6), dpi=100)
        self.fig.patch.set_facecolor('#f5f6fa')
        
        gs = self.fig.add_gridspec(2, 2, height_ratios=[1, 1])
        
        # 1. Animation Track (Top)
        self.ax_anim = self.fig.add_subplot(gs[0, :])
        self.ax_anim.set_facecolor('white')
        
        # 2. Momentum Graph (Bottom Left)
        self.ax_mom = self.fig.add_subplot(gs[1, 0])
        self.ax_mom.set_facecolor('#f5f6fa')
        
        # 3. Energy Graph (Bottom Right)
        self.ax_eng = self.fig.add_subplot(gs[1, 1])
        self.ax_eng.set_facecolor('#f5f6fa')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_params(self, event=None):
        self.m1 = self.var_m1.get()
        self.v1_init = self.var_v1.get()
        self.m2 = self.var_m2.get()
        self.v2_init = self.var_v2.get()
        self.e = self.var_e.get()
        
        self.lbl_m1.config(text=f"{self.m1:.1f} kg")
        self.lbl_v1.config(text=f"{self.v1_init:.1f} m/s")
        self.lbl_m2.config(text=f"{self.m2:.1f} kg")
        self.lbl_v2.config(text=f"{self.v2_init:.1f} m/s")
        
        if self.e > 0.99: e_text = self.T("e_perfect")
        elif self.e < 0.01: e_text = self.T("e_inelastic")
        else: e_text = self.T("e_part")
        self.lbl_e.config(text=f"{self.e:.2f} ({e_text})")
        
        if not self.running:
            self.reset_simulation()

    def reset_simulation(self):
        self.running = False
        self.btn_start.config(text=self.T("btn_start"))
        
        self.m1 = self.var_m1.get()
        self.v1_init = self.var_v1.get()
        self.m2 = self.var_m2.get()
        self.v2_init = self.var_v2.get()
        self.e = self.var_e.get()
        
        self.x1 = -5.0
        self.x2 = 5.0
        self.v1 = self.v1_init
        self.v2 = self.v2_init
        self.collided = False
        self.time = 0.0
        
        self.draw_frame()
        self.update_info()

    def toggle_simulation(self):
        if self.running:
            self.running = False
            self.btn_start.config(text=self.T("btn_continue"))
            if self.ani:
                self.ani.event_source.stop()
        else:
            self.running = True
            self.btn_start.config(text=self.T("btn_pause"))
            self.ani = FuncAnimation(self.fig, self.animate_step, interval=30, blit=False, cache_frame_data=False)

    def animate_step(self, frame):
        if not self.running:
            return
            
        # Update Position
        new_x1 = self.x1 + self.v1 * self.dt
        new_x2 = self.x2 + self.v2 * self.dt
        
        # Check Collision
        radius = 0.5
        dist = new_x2 - new_x1
        
        if dist <= (2 * radius) and not self.collided:
            self.collided = True
            
            v_rel = self.v2 - self.v1
            
            v1_final = (self.m1 * self.v1 + self.m2 * self.v2 + self.m2 * self.e * (v_rel * -1)) / (self.m1 + self.m2)
            v2_final = (self.m1 * self.v1 + self.m2 * self.v2 + self.m1 * self.e * (self.v1 - self.v2)) / (self.m1 + self.m2)
            
            self.v1 = v1_final
            self.v2 = v2_final
            
        elif dist > (2 * radius) + 0.1: 
            self.collided = False

        if not self.collided:
             self.x1 = new_x1
             self.x2 = new_x2
        else:
             self.x1 = new_x1
             self.x2 = new_x2

        self.time += self.dt
        
        # Bounds Check
        if self.x1 < -9 or self.x2 > 9:
            self.running = False
            self.btn_start.config(text=self.T("btn_done"))
            
        self.draw_frame()
        self.update_info()

    def update_info(self):
        p1 = self.m1 * self.v1
        p2 = self.m2 * self.v2
        p_total = p1 + p2
        
        ke1 = 0.5 * self.m1 * self.v1**2
        ke2 = 0.5 * self.m2 * self.v2**2
        ke_total = ke1 + ke2
        
        txt = self.T("info_time").format(self.time)
        txt += self.T("info_obj1")
        txt += self.T("info_v1").format(self.v1)
        txt += self.T("info_p1").format(p1)
        txt += self.T("info_obj2")
        txt += self.T("info_v2").format(self.v2)
        txt += self.T("info_p2").format(p2)
        txt += self.T("info_line")
        txt += self.T("info_ptot").format(p_total)
        txt += self.T("info_ketot").format(ke_total)
        
        self.info_box.delete("1.0", tk.END)
        self.info_box.insert("1.0", txt)

    def draw_frame(self):
        self.ax_anim.clear()
        self.ax_mom.clear()
        self.ax_eng.clear()
        
        # 1. Animation
        self.ax_anim.set_xlim(-10, 10)
        self.ax_anim.set_ylim(-2, 2)
        self.ax_anim.set_aspect('equal')
        self.ax_anim.set_xticks([]) 
        self.ax_anim.set_yticks([])
        self.ax_anim.set_title(self.T("graph_sim_title"), fontsize=10, fontweight='bold')
        self.ax_anim.grid(True, axis='x', alpha=0.2)
        
        self.ax_anim.plot([-10, 10], [0, 0], color='black', linewidth=2)
        
        radius = 0.5
        c1 = patches.Circle((self.x1, 0.5), radius, facecolor='#e74c3c', edgecolor='black') # Red
        c2 = patches.Circle((self.x2, 0.5), radius, facecolor='#3498db', edgecolor='black') # Blue
        self.ax_anim.add_patch(c1)
        self.ax_anim.add_patch(c2)
        
        if abs(self.v1) > 0.1:
            self.ax_anim.arrow(self.x1, 0.5, self.v1*0.5, 0, head_width=0.3, head_length=0.4, facecolor='#c0392b', zorder=10)
        if abs(self.v2) > 0.1:
            self.ax_anim.arrow(self.x2, 0.5, self.v2*0.5, 0, head_width=0.3, head_length=0.4, facecolor='#2980b9', zorder=10)

        # 2. Momentum Bar Chart
        p1 = self.m1 * self.v1
        p2 = self.m2 * self.v2
        p_tot = p1 + p2
        
        names = ['P1', 'P2', 'Total']
        vals = [p1, p2, p_tot]
        colors = ['#e74c3c', '#3498db', '#2c3e50']
        
        self.ax_mom.bar(names, vals, color=colors)
        self.ax_mom.set_title(self.T("graph_mom_title"), fontsize=9)
        self.ax_mom.axhline(0, color='black', linewidth=0.5)
        
        max_p = max(50, abs(p_tot)*1.5, abs(p1)*1.5, abs(p2)*1.5)
        self.ax_mom.set_ylim(-max_p, max_p)
        
        # 3. Energy Bar Chart
        ke1 = 0.5 * self.m1 * self.v1**2
        ke2 = 0.5 * self.m2 * self.v2**2
        ke_tot = ke1 + ke2
        
        names_e = ['KE1', 'KE2', 'Total']
        vals_e = [ke1, ke2, ke_tot]
        colors_e = ['#e74c3c', '#3498db', '#27ae60']
        
        self.ax_eng.bar(names_e, vals_e, color=colors_e)
        self.ax_eng.set_title(self.T("graph_eng_title"), fontsize=9)
        
        max_e = max(100, ke_tot * 1.5)
        self.ax_eng.set_ylim(0, max_e)

        self.canvas.draw()
