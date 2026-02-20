import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as patches

class VirtualLabResonansi:
    def __init__(self, parent):
        self.parent = parent
        # Style Config
        self.bg_color = "#2c3e50"
        self.style = ttk.Style()
        self.style.theme_use('clam')
        # --- MAIN NOTEBOOK ---
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        # ...lanjutkan inisialisasi lain, tanpa header/footer window dan tanpa set title/geometry...

        # Tab 1: Simulasi
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="1. Simulasi Kolom Udara")
        self.setup_simulasi()

        # Tab 2: Analisis Data
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="2. Analisis Cepat Rambat Bunyi")
        self.setup_analisis()

    def create_header(self):
        header_frame = tk.Frame(self.root, bg=self.bg_color, pady=15)
        header_frame.pack(side="top", fill="x")
        
        tk.Label(header_frame, text="VIRTUAL LAB: RESONANSI GELOMBANG BUNYI", 
                 font=("Arial", 24, "bold"), fg="white", bg=self.bg_color).pack()
        tk.Label(header_frame, text="Penentuan Cepat Rambat Bunyi Menggunakan Tabung Resonansi", 
                 font=("Arial", 14), fg="#bdc3c7", bg=self.bg_color).pack()
        tk.Label(header_frame, text="Pengembang Aplikasi: Yohanes Kurniawan", 
                 font=("Arial", 14, "bold"), fg="white", bg=self.bg_color).pack(pady=(5, 0))

    def create_footer(self):
        footer_frame = tk.Frame(self.root, bg=self.bg_color, pady=8)
        footer_frame.pack(side="bottom", fill="x")
        
        tk.Label(footer_frame, text="VERSI APLIKASI PRO", 
                 font=("Arial", 10, "bold"), fg="#e74c3c", bg=self.bg_color).pack(side="left", padx=20)
        
        tk.Label(footer_frame, text="Modul Fisika Dasar: Gelombang & Bunyi", 
                 font=("Arial", 10), fg="#bdc3c7", bg=self.bg_color).pack(side="right", padx=20)

    # =========================================
    # TAB 1: SIMULASI
    # =========================================
    def setup_simulasi(self):
        pane = tk.PanedWindow(self.tab1, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)

        # Left Container (Controls & Feedback)
        left_frame = ttk.Frame(pane, padding=10)
        pane.add(left_frame, stretch="always")

        # Right Container (Visualization)
        right_frame = ttk.Frame(pane, padding=10)
        pane.add(right_frame, stretch="always")

        # --- CONTROLS ---
        ttk.Label(left_frame, text="PENGATURAN EKSPERIMEN", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))

        # Variables
        self.var_freq = tk.DoubleVar(value=512.0)
        self.var_length = tk.DoubleVar(value=0.1) # m (Air column length)
        self.var_temp = tk.DoubleVar(value=27.0) # Celsius

        form = ttk.Frame(left_frame)
        form.pack(fill="x", pady=5)

        # Frequency
        ttk.Label(form, text="Frekuensi Garpu Tala (f) [Hz]:").grid(row=0, column=0, sticky="w", pady=5)
        self.scale_f = tk.Scale(form, from_=256, to=1024, resolution=1, orient="horizontal", 
                                variable=self.var_freq, length=250, command=self.update_simulation)
        self.scale_f.grid(row=0, column=1)

        # Column Length (L)
        ttk.Label(form, text="Panjang Kolom Udara (L) [m]:").grid(row=1, column=0, sticky="w", pady=5)
        self.scale_l = tk.Scale(form, from_=0.0, to=1.0, resolution=0.001, orient="horizontal", 
                                variable=self.var_length, length=250, command=self.update_simulation)
        self.scale_l.grid(row=1, column=1)
        
        # Temperature
        ttk.Label(form, text="Suhu Ruangan (T) [°C]:").grid(row=2, column=0, sticky="w", pady=5)
        self.scale_t = tk.Scale(form, from_=0, to=40, resolution=1, orient="horizontal", 
                                variable=self.var_temp, length=250, command=self.update_simulation)
        self.scale_t.grid(row=2, column=1)

        # Info Box
        self.info_frame = ttk.LabelFrame(left_frame, text="Indikator Resonansi")
        self.info_frame.pack(fill="x", pady=20)
        
        self.lbl_v_theory = ttk.Label(self.info_frame, text="Cepat Rambat Bunyi (v): - m/s")
        self.lbl_v_theory.pack(anchor="w", padx=10, pady=2)
        
        self.lbl_lambda = ttk.Label(self.info_frame, text="Panjang Gelombang (λ): - m")
        self.lbl_lambda.pack(anchor="w", padx=10, pady=2)
        
        # Volume Meter
        ttk.Label(self.info_frame, text="Tingkat Kekerasan Suara (Loudness):").pack(anchor="w", padx=10, pady=(10,0))
        self.volume_bar = ttk.Progressbar(self.info_frame, orient="horizontal", length=300, mode="determinate")
        self.volume_bar.pack(anchor="w", padx=10, pady=5)
        self.lbl_resonance_status = ttk.Label(self.info_frame, text="Status: Tidak Resonansi", foreground="red")
        self.lbl_resonance_status.pack(anchor="w", padx=10)

        # Instructions
        note_frame = ttk.LabelFrame(left_frame, text="Petunjuk")
        note_frame.pack(fill='x', pady=10)
        ttk.Label(note_frame, text="1. Geser 'Panjang Kolom Udara' perlahan.\n2. Perhatikan grafik gelombang dan volume meter.\n3. Resonansi terjadi saat Volume Maksimum.\n4. Gelombang Berdiri terbentuk sempurna saat resonansi.", 
                  justify="left").pack(padx=5, pady=5)

        # --- VISUALIZATION SETUP ---
        self.fig_sim = Figure(figsize=(5, 6), dpi=100)
        self.ax_sim = self.fig_sim.add_subplot(111)
        self.canvas_sim = FigureCanvasTkAgg(self.fig_sim, master=right_frame)
        self.canvas_sim.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.update_simulation()

    def calculate_theory(self):
        f = self.var_freq.get()
        T = self.var_temp.get()
        
        # v = 331 + 0.6 * T
        v = 331 + (0.6 * T)
        wl = v / f # wavelength
        
        return v, wl

    def update_simulation(self, event=None):
        L_current = self.var_length.get()
        v, wl = self.calculate_theory()
        
        self.lbl_v_theory.config(text=f"Cepat Rambat Bunyi (v): {v:.1f} m/s")
        self.lbl_lambda.config(text=f"Panjang Gelombang (λ): {wl:.3f} m")
        
        # Check Resonance Condition
        # Resonance occurs at L = (2n-1)/4 * lambda
        # n = 1 -> 1/4 lambda
        # n = 2 -> 3/4 lambda
        # n = 3 -> 5/4 lambda
        
        resonance_points = []
        max_n = int((1.0 / (wl/4)) + 1)
        for n in range(1, max_n + 2):
            l_res = ((2*n - 1) / 4) * wl
            if l_res <= 1.2: # Limit meaningful range
                resonance_points.append(l_res)
                
        # Calculate loudness factor based on proximity to ANY resonance point
        min_dist = min([abs(L_current - res) for res in resonance_points])
        
        # Gaussian resonance curve width
        width = 0.02 # 2 cm sensitivity
        loudness = np.exp(- (min_dist**2) / (2 * width**2))
        
        self.volume_bar['value'] = loudness * 100
        
        if loudness > 0.8:
            self.lbl_resonance_status.config(text="Status: RESONANSI KUAT!", foreground="green", font=("Arial", 12, "bold"))
        elif loudness > 0.4:
            self.lbl_resonance_status.config(text="Status: Resonansi Lemah", foreground="#d35400", font=("Arial", 10))
        else:
            self.lbl_resonance_status.config(text="Status: Tidak Resonansi", foreground="black", font=("Arial", 10))
            
        self.draw_system(L_current, wl, loudness)

    def draw_system(self, L, wl, loudness):
        self.ax_sim.clear()
        
        tube_radius = 0.1
        tube_height = 1.0
        
        # Draw Tube Walls
        self.ax_sim.plot([-tube_radius, -tube_radius], [0, tube_height], 'k-', lw=3)
        self.ax_sim.plot([tube_radius, tube_radius], [0, tube_height], 'k-', lw=3)
        
        # Draw Water Level
        water_level = tube_height - L
        water_rect = patches.Rectangle((-tube_radius, 0), 2*tube_radius, water_level, 
                                       facecolor='#3498db', alpha=0.5)
        self.ax_sim.add_patch(water_rect)
        self.ax_sim.text(0, water_level/2, "AIR", ha='center', color='blue')
        
        # Draw Air Column Wave
        # Vertical axis y from water_level to tube_height
        y_air = np.linspace(water_level, tube_height, 100)
        
        # Standing measure: Node at water surface (closed end), Antinode at open end (top)
        # We simulate the pressure wave or displacement wave visually
        # Displacement Node at Water (closed), Displacement Antinode at Open
        # k = 2pi / wl
        k = 2 * np.pi / wl
        
        # Displacement y(x) = A sin(k x) where x=0 is closed end.
        # x corresponds to (val - water_level)
        x_dist = y_air - water_level
        
        # Amplitude of visualization depends on simulated 'loudness'
        base_amp = 0.2 * loudness 
        if base_amp < 0.02: base_amp = 0.02 # minimum visibility
        
        # Left and Right wave envelopes
        wave_displacement = base_amp * np.sin(k * x_dist)
        
        # Visualize inside the tube range [-0.1, 0.1]
        # We scale it to fit inside
        scaled_disp = wave_displacement * (tube_radius * 0.8)
        
        self.ax_sim.plot(scaled_disp, y_air, 'r-', alpha=0.7)
        self.ax_sim.plot(-scaled_disp, y_air, 'r-', alpha=0.7)
        
        # Fill between for standing wave effect
        self.ax_sim.fill_betweenx(y_air, -scaled_disp, scaled_disp, color='red', alpha=0.1)

        # Draw Tuning Fork
        fork_y = tube_height + 0.05
        self.ax_sim.plot([-0.02, -0.02], [fork_y, fork_y+0.15], 'k-', lw=4) # Stem
        self.ax_sim.plot([-0.05, -0.05], [fork_y+0.15, fork_y+0.3], 'k-', lw=3) # Left prong
        self.ax_sim.plot([0.01, 0.01], [fork_y+0.15, fork_y+0.3], 'k-', lw=3) # Right prong
        self.ax_sim.plot([-0.05, 0.01], [fork_y+0.15, fork_y+0.15], 'k-', lw=4) # Base
        
        # Vibration marks if loud
        if loudness > 0.1:
            self.ax_sim.text(0.1, fork_y+0.25, "((( )))", fontsize=12, color='red')

        # Annotation
        self.ax_sim.axhline(water_level, color='blue', linestyle='--')
        self.ax_sim.text(0.15, water_level, f"L = {L:.3f} m", color='blue', va='center')

        self.ax_sim.set_xlim(-0.3, 0.3)
        self.ax_sim.set_ylim(0, 1.4)
        self.ax_sim.axis('off')
        self.ax_sim.set_title("Simulasi Gelombang Berdiri dalam Tabung")
        
        self.canvas_sim.draw()

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
        ttk.Label(left_frame, text="LOG DATA PERCOBAAN", font=("Arial", 12, "bold")).pack(anchor="w", pady=10)
        
        input_box = ttk.LabelFrame(left_frame, text="Input Data")
        input_box.pack(fill="x", pady=5)
        
        ttk.Label(input_box, text="Frekuensi (f) [Hz]:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_freq = ttk.Entry(input_box, width=12)
        self.entry_freq.grid(row=0, column=1)
        
        ttk.Label(input_box, text="Panjang Resonansi 1 (L1) [m]:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_L = ttk.Entry(input_box, width=12)
        self.entry_L.grid(row=1, column=1)
        
        ttk.Button(input_box, text="Tambah Data", command=self.add_data_point).grid(row=2, column=0, columnspan=2, pady=10, sticky='ew')

        # Table
        cols = ("f (Hz)", "1/f (s)", "L (m)", "v_ukur (m/s)")
        self.tree = ttk.Treeview(left_frame, columns=cols, show="headings", height=12)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=80, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=10)
        
        ttk.Button(left_frame, text="Hapus Semua Data", command=self.clear_data).pack(fill='x')

        # Graph
        self.fig_graph = Figure(figsize=(5, 4), dpi=100)
        self.ax_graph = self.fig_graph.add_subplot(111)
        self.canvas_graph = FigureCanvasTkAgg(self.fig_graph, master=right_frame)
        self.canvas_graph.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.lbl_result_v = ttk.Label(right_frame, text="Cepat Rambat Bunyi (v): - m/s", 
                          font=("Arial", 14, "bold"), foreground="#2980b9")
        self.lbl_result_v.pack(pady=10)
        self.lbl_result_f = ttk.Label(right_frame, text="Frekuensi (f): - Hz", 
                          font=("Arial", 12), foreground="#16a085")
        self.lbl_result_f.pack(pady=2)

        self.data_points = []

    def add_data_point(self):
        try:
            f = float(self.entry_freq.get().replace(',', '.'))
            L = float(self.entry_L.get().replace(',', '.'))
            
            # Assuming L is the FIRST Resonance length (lambda/4)
            # v = f * lambda = f * 4L
            v_calc = f * 4 * L
            inv_f = 1/f
            
            self.data_points.append({'f': f, 'L': L, 'inv_f': inv_f})
            self.tree.insert("", "end", values=(f"{f:.1f}", f"{inv_f:.4f}", f"{L:.3f}", f"{v_calc:.1f}"))
            
            self.update_graph()
            
            # Calculate average v and f
            vs = [d['f'] * 4 * d['L'] for d in self.data_points]
            avg_v = sum(vs) / len(vs)
            fs = [d['f'] for d in self.data_points]
            avg_f = sum(fs) / len(fs)
            self.lbl_result_v.config(text=f"Rata-rata v: {avg_v:.1f} m/s")
            self.lbl_result_f.config(text=f"Rata-rata f: {avg_f:.1f} Hz")
            
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid")

    def clear_data(self):
        self.data_points = []
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.ax_graph.clear()
        self.canvas_graph.draw()
        self.lbl_result_v.config(text="Cepat Rambat Bunyi (v): - m/s")
        self.lbl_result_f.config(text="Frekuensi (f): - Hz")

    def update_graph(self):
        if len(self.data_points) < 2:
            return
            
        # Plot L vs 1/f
        # Theory: L = (v/4) * (1/f)
        # Slope = v/4
        # v = 4 * slope
        
        inv_fs = np.array([d['inv_f'] for d in self.data_points])
        Ls = np.array([d['L'] for d in self.data_points])
        
        coef = np.polyfit(inv_fs, Ls, 1)
        slope = coef[0]
        v_reg = slope * 4
        
        self.ax_graph.clear()
        self.ax_graph.scatter(inv_fs, Ls, color='blue', label='Data')
        
        x_line = np.linspace(0, max(inv_fs)*1.1, 50)
        y_line = coef[0]*x_line + coef[1]
        self.ax_graph.plot(x_line, y_line, 'r--', label=f'Fit Slope = {slope:.2f}')
        
        self.ax_graph.set_title(f"Hubungan Panjang Resonansi vs 1/f (v = {v_reg:.1f} m/s)")
        self.ax_graph.set_xlabel("Periode atau 1/f (s)")
        self.ax_graph.set_ylabel("Panjang Kolom Udara L (m)")
        self.ax_graph.legend()
        self.ax_graph.grid(True)
        self.canvas_graph.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabResonansi(root)
    root.mainloop()
