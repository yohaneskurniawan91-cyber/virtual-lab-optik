import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class VirtualLabMassaJenis:
    def __init__(self, parent):
        self.parent = parent
        # --- MATERIAL DATABASE (g/cm^3) ---
        self.materials = {
            "Styrofoam": 0.05,
            "Kayu (Pinus)": 0.65,
            "Es": 0.92,
            "Air (Referensi)": 1.0,
            "Aluminium": 2.7,
            "Besi": 7.87,
            "Tembaga": 8.96,
            "Emas": 19.3
        }
        
        # Color Map for Visualization
        self.colors = {
            "Styrofoam": "#ecf0f1",
            "Kayu (Pinus)": "#d35400",
            "Es": "#a9cce3",
            "Air (Referensi)": "#3498db",
            "Aluminium": "#bdc3c7",
            "Besi": "#7f8c8d",
            "Tembaga": "#d35400",
            "Emas": "#f1c40f"
        }

        # Style Config
        self.bg_color = "#2c3e50"
        # --- MAIN NOTEBOOK ---
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        # Tab 1: Simulasi Pengukuran & Keapungan
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="1. Simulasi Pengukuran & Keapungan")
        self.setup_simulasi()
        # Tab 2: Kalkulator & Laporan
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="2. Analisis Data Mass-Volume")
        self.setup_analisis()

    # def create_header(self):
    #     pass  # Dihilangkan untuk integrasi tab
        
    #     tk.Label(header_frame, text="VIRTUAL LAB: MASSA JENIS ZAT PADAT", 
    #              font=("Arial", 22, "bold"), fg="white", bg=self.bg_color).pack()
    #     tk.Label(header_frame, text="Simulasi Pengukuran Dimensi, Massa, dan Hukum Archimedes", 
    #              font=("Arial", 12), fg="#bdc3c7", bg=self.bg_color).pack()
    #     tk.Label(header_frame, text="Pengembang Aplikasi: Yohanes Kurniawan", 
    #              font=("Arial", 14, "bold"), fg="white", bg=self.bg_color).pack(pady=(5, 0))

    # def create_footer(self):
    #     pass  # Dihilangkan untuk integrasi tab
        
    #     tk.Label(footer_frame, text="VERSI APLIKASI PRO", 
    #              font=("Arial", 8, "bold"), fg="#e74c3c", bg=self.bg_color).pack(side="left", padx=20)

    # =========================================
    # TAB 1: SIMULASI PENGUKURAN
    # =========================================
    def setup_simulasi(self):
        pane = tk.PanedWindow(self.tab1, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)

        # Left: Controls
        left_frame = ttk.Frame(pane, padding=10)
        pane.add(left_frame, stretch="always") # Use stretch instead of weight

        # Right: Visualization
        right_frame = ttk.Frame(pane, padding=10)
        pane.add(right_frame, stretch="always") # Use stretch instead of weight

        # --- INPUT CONTROLS ---
        ttk.Label(left_frame, text="KONFIGURASI BENDA", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))
        
        # Material Selection
        ttk.Label(left_frame, text="Pilih Material:").pack(anchor="w")
        self.var_mat = tk.StringVar(value="Kayu (Pinus)")
        mat_combo = ttk.Combobox(left_frame, textvariable=self.var_mat, 
                               values=list(self.materials.keys()), state="readonly")
        mat_combo.pack(fill="x", pady=5)
        mat_combo.bind("<<ComboboxSelected>>", self.update_sim)

        # Shape Selection
        ttk.Label(left_frame, text="Pilih Bentuk:").pack(anchor="w", pady=(10, 0))
        self.var_shape = tk.StringVar(value="Balok")
        shape_combo = ttk.Combobox(left_frame, textvariable=self.var_shape, 
                                 values=["Balok", "Silinder", "Bola"], state="readonly")
        shape_combo.pack(fill="x", pady=5)
        shape_combo.bind("<<ComboboxSelected>>", self.update_inputs)

        # Dimension Inputs (Dynamic)
        self.frame_dims = ttk.LabelFrame(left_frame, text="Dimensi (cm)")
        self.frame_dims.pack(fill="x", pady=10)
        self.entries = {}
        self.update_inputs() # Init inputs

        # Action Button
        ttk.Button(left_frame, text="▶ UKUR & CELUPKAN KE AIR", command=self.run_measurement).pack(fill="x", pady=20)

        # Results Display
        self.res_text = tk.Text(left_frame, height=12, bg="#ecf0f1", font=("Consolas", 10))
        self.res_text.pack(fill="both", expand=True)

        # --- VISUALIZATION ---
        self.fig_sim = Figure(figsize=(6, 6), dpi=100)
        self.ax_sim = self.fig_sim.add_subplot(111)
        self.canvas_sim = FigureCanvasTkAgg(self.fig_sim, master=right_frame)
        self.canvas_sim.get_tk_widget().pack(fill="both", expand=True)
        
        # Init View
        self.draw_container()

    def update_inputs(self, event=None):
        # Clear previous inputs
        for widget in self.frame_dims.winfo_children():
            widget.destroy()
        self.entries = {}
        
        shape = self.var_shape.get()
        params = []
        if shape == "Balok": params = [("Panjang (p)", 5), ("Lebar (l)", 4), ("Tinggi (t)", 3)]
        elif shape == "Silinder": params = [("Jari-jari (r)", 3), ("Tinggi (t)", 6)]
        elif shape == "Bola": params = [("Jari-jari (r)", 3)]

        for i, (label, default) in enumerate(params):
            ttk.Label(self.frame_dims, text=label).grid(row=i, column=0, padx=5, pady=2, sticky="w")
            ent = ttk.Entry(self.frame_dims)
            ent.insert(0, str(default))
            ent.grid(row=i, column=1, padx=5, pady=2)
            # Store reference by parameter key (first letter usually enough for logic)
            key = label.split('(')[1][0] 
            self.entries[key] = ent

    def update_sim(self, event=None):
        # Just update color or basic info if needed, but run_measurement does the heavy lifting
        pass

    def run_measurement(self):
        try:
            mat_name = self.var_mat.get()
            rho_obj = self.materials[mat_name]
            shape = self.var_shape.get()
            
            # 1. Calculate Volume & Dimensions
            vol = 0
            dims_text = ""
            
            if shape == "Balok":
                p = float(self.entries['p'].get())
                l = float(self.entries['l'].get())
                t = float(self.entries['t'].get())
                vol = p * l * t
                dims_text = f"p={p} cm, l={l} cm, t={t} cm"
                width_vis = p; height_vis = t # Simplified for 2D view
                
            elif shape == "Silinder":
                r = float(self.entries['r'].get())
                t = float(self.entries['t'].get())
                vol = math.pi * (r**2) * t
                dims_text = f"r={r} cm, t={t} cm"
                width_vis = 2*r; height_vis = t
                
            elif shape == "Bola":
                r = float(self.entries['r'].get())
                vol = (4/3) * math.pi * (r**3)
                dims_text = f"r={r} cm"
                width_vis = 2*r; height_vis = 2*r

            # 2. Add Measurement Noise
            mass_real = vol * rho_obj
            mass_measured = mass_real + random.uniform(-0.05, 0.05)
            
            # 3. Archimedes Logic
            rho_fluid = 1.0 # Water
            sinks = rho_obj > rho_fluid
            
            # Fraction submerged
            if sinks:
                v_sub = vol
                percent_sub = 100.0
                buoyancy = vol * rho_fluid * 9.8 # Archimedes Force
            else:
                v_sub = (rho_obj / rho_fluid) * vol
                percent_sub = (rho_obj / rho_fluid) * 100.0
                buoyancy = mass_real * 9.8 # Equilibrium (Weight = Buoyancy)

            # Vol Displacement in simulated Graduated Cylinder
            vol_awal = 100.0 # mL
            vol_akhir = vol_awal + v_sub + random.uniform(-0.5, 0.5)

            # --- DISPLAY RESULTS ---
            res = f"--- DATA PENGUKURAN ---\n"
            res += f"Benda        : {mat_name}\n"
            res += f"Bentuk       : {shape} ({dims_text})\n"
            res += f"Massa (m)    : {mass_measured:.2f} g (Neraca)\n"
            res += f"Volume Hitung: {vol:.2f} cm³ (Rumus Geometri)\n"
            res += f"\n--- DATA GELAS UKUR (ARCHIMEDES) ---\n"
            res += f"Vol Awal Air : {vol_awal:.1f} mL\n"
            res += f"Vol Akhir    : {vol_akhir:.1f} mL\n"
            res += f"Vol Benda Celup: {vol_akhir - vol_awal:.1f} mL\n"
            res += f"\n--- ANALISIS FISIKA ---\n"
            res += f"Rho Benda    : {rho_obj} g/cm³\n"
            res += f"Kondisi      : {'TENGGELAM' if sinks else f'TERAPUNG ({percent_sub:.1f}%)'}\n"
            
            self.res_text.delete(1.0, tk.END)
            self.res_text.insert(tk.END, res)
            
            # --- DRAW SIMULATION ---
            self.draw_archimedes(width_vis, height_vis, sinks, percent_sub, mat_name, shape)

        except ValueError:
            messagebox.showerror("Input Error", "Masukkan dimensi angka yang valid.")

    def draw_container(self):
        self.ax_sim.clear()
        self.ax_sim.set_axis_off()
        self.ax_sim.set_xlim(-10, 10)
        self.ax_sim.set_ylim(-2, 18)
        self.ax_sim.set_title("Visualisasi Gelas Ukur")
        
        # Draw Beaker
        # Bottom
        self.ax_sim.plot([-8, 8], [0, 0], 'k-', linewidth=3)
        # Sides
        self.ax_sim.plot([-8, -8], [0, 15], 'k-', linewidth=3)
        self.ax_sim.plot([8, 8], [0, 15], 'k-', linewidth=3)
        
        # Water Level (Initial)
        water_h = 10
        self.ax_sim.add_patch(plt.Rectangle((-8, 0), 16, water_h, color='#3498db', alpha=0.3))
        self.ax_sim.text(0, water_h/2, "AIR (1 g/cm³)", ha='center', color='blue', alpha=0.5)
        
        self.canvas_sim.draw()

    def draw_archimedes(self, w_vis, h_vis, sinks, percent_sub, mat_name, shape):
        self.ax_sim.clear()
        self.ax_sim.set_axis_off()
        
        # Scale visualization size to fit beaker nicely (max width ~10 units)
        # Assuming input cm mapped to units roughly 1:1 but clamped
        scale = 1.0
        if w_vis > 12: scale = 12/w_vis
        
        w_draw = w_vis * scale
        h_draw = h_vis * scale
        
        # Water properties
        water_level_base = 10
        # Rise in water level (Visual only, exaggerated)
        rise = (percent_sub / 100) * 1.5 
        water_level_new = water_level_base + rise
        
        self.ax_sim.set_xlim(-10, 10)
        self.ax_sim.set_ylim(-2, 18)
        self.ax_sim.set_title(f"Visualisasi: {mat_name} ({'Tenggelam' if sinks else 'Terapung'})")

        # Draw Beaker
        self.ax_sim.plot([-8, 8], [0, 0], 'k-', linewidth=3)
        self.ax_sim.plot([-8, -8], [0, 15], 'k-', linewidth=3)
        self.ax_sim.plot([8, 8], [0, 15], 'k-', linewidth=3)
        
        # Draw Water
        self.ax_sim.add_patch(plt.Rectangle((-8, 0), 16, water_level_new, color='#3498db', alpha=0.4))
        self.ax_sim.plot([-8, 8], [water_level_new, water_level_new], color='blue', linestyle='--')
        self.ax_sim.text(9, water_level_new, "Level Air", color='blue', fontsize=8)

        # Draw Object
        # Calculate Y position
        if sinks:
            # Sitting on bottom
            y_pos = 0
            if shape == "Bola": y_pos = h_draw/2 # Center offset
        else:
            # Floating
            # Submerged height = h * (rho_obj/rho_fluid)
            h_sub = h_draw * (percent_sub / 100)
            # Center of object logic?
            # If floating, bottom of object is at (water_level - h_sub)
            bottom_y = water_level_new - h_sub
            y_pos = bottom_y
            if shape == "Bola": y_pos = bottom_y + h_draw/2

        color = self.colors.get(mat_name, 'gray')
        
        if shape == "Bola":
            circle = plt.Circle((0, y_pos), w_draw/2, color=color, ec='black')
            self.ax_sim.add_patch(circle)
        elif shape == "Silinder" or shape == "Balok":
            # Draw as Rectangle for 2D view
            rect = plt.Rectangle((-w_draw/2, y_pos), w_draw, h_draw, color=color, ec='black')
            self.ax_sim.add_patch(rect)
            
        # Forces Arrows (Free Body Diagram)
        # Gravity (Down)
        cx, cy = 0, y_pos + h_draw/2
        if shape == "Bola": cy = y_pos
        
        self.ax_sim.arrow(cx, cy, 0, -3, head_width=0.5, color='red', label='W (Berat)')
        self.ax_sim.text(cx + 0.5, cy - 2, "W", color='red')
        
        # Buoyancy (Up) - Always exists in fluid
        self.ax_sim.arrow(cx, cy, 0, 3 if sinks else 3, head_width=0.5, color='green')
        self.ax_sim.text(cx + 0.5, cy + 2, "Fa (Archimedes)", color='green')
        
        if sinks:
            # Normal Force (Up from bottom)
            self.ax_sim.arrow(cx - 1, 0, 0, 2, head_width=0.3, color='purple')
            self.ax_sim.text(cx - 2, 1, "N", color='purple')

        self.canvas_sim.draw()

    # =========================================
    # TAB 2: ANALISIS DATA
    # =========================================
    def setup_analisis(self):
        frame = ttk.Frame(self.tab2, padding=20)
        frame.pack(fill="both", expand=True)

        # Controls
        input_frame = ttk.LabelFrame(frame, text="Input Data Eksperimen")
        input_frame.pack(fill="x")
        
        ttk.Label(input_frame, text="Massa (g):").grid(row=0, column=0, padx=5, pady=5)
        self.ent_m = ttk.Entry(input_frame)
        self.ent_m.grid(row=0, column=1)
        
        ttk.Label(input_frame, text="Volume (cm³):").grid(row=0, column=2, padx=5, pady=5)
        self.ent_v = ttk.Entry(input_frame)
        self.ent_v.grid(row=0, column=3)
        
        ttk.Button(input_frame, text="Tambahkan Data ke Grafik", command=self.add_data_point).grid(row=0, column=4, padx=10)
        ttk.Button(input_frame, text="Reset Data", command=self.reset_data).grid(row=0, column=5)

        # Plot Area
        self.fig_graph = Figure(figsize=(6, 4), dpi=100)
        self.ax_graph = self.fig_graph.add_subplot(111)
        self.canvas_graph = FigureCanvasTkAgg(self.fig_graph, master=frame)
        self.canvas_graph.get_tk_widget().pack(fill="both", expand=True, pady=10)
        
        self.data_points = [] # List of (m, v)
        self.draw_empty_graph()

    def draw_empty_graph(self):
        self.ax_graph.clear()
        self.ax_graph.set_xlabel("Volume (cm³)")
        self.ax_graph.set_ylabel("Massa (g)")
        self.ax_graph.set_title("Grafik Massa vs Volume (Kemiringan = Massa Jenis)")
        self.ax_graph.grid(True)
        self.canvas_graph.draw()

    def add_data_point(self):
        try:
            m = float(self.ent_m.get())
            v = float(self.ent_v.get())
            self.data_points.append((v, m)) # x=v, y=m
            self.update_graph()
        except ValueError:
            messagebox.showerror("Error", "Input angka valid.")

    def reset_data(self):
        self.data_points = []
        self.draw_empty_graph()

    def update_graph(self):
        if not self.data_points:
            return
            
        self.ax_graph.clear()
        
        # Scatter Plot
        V_vals = [p[0] for p in self.data_points]
        M_vals = [p[1] for p in self.data_points]
        
        self.ax_graph.scatter(V_vals, M_vals, color='red', label='Data Mentah')
        
        # Linear Regression (Fit Through Origin usually preferred for Density, but basic fit here)
        if len(self.data_points) >= 2:
            coef = np.polyfit(V_vals, M_vals, 1) # y = mx + c
            poly1d_fn = np.poly1d(coef) 
            
            x_line = np.linspace(0, max(V_vals)*1.1, 50)
            self.ax_graph.plot(x_line, poly1d_fn(x_line), '--k', label=f'Regresi: ρ ≈ {coef[0]:.2f} g/cm³')
        
        self.ax_graph.set_xlabel("Volume (cm³)")
        self.ax_graph.set_ylabel("Massa (g)")
        self.ax_graph.set_title("Analisis Regresi Massa Jenis")
        self.ax_graph.legend()
        self.ax_graph.grid(True)
        self.canvas_graph.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabMassaJenis(root)
    root.mainloop()
