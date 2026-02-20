import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as patches

class VirtualLabKalorimeter:
    def __init__(self, parent):
        self.parent = parent
        # Style Config
        self.bg_color = "#2c3e50"
        self.style = ttk.Style()
        self.style.theme_use('clam')
        # Constants
        self.c_air = 4.2           # J/g°C
        self.c_alumunium = 0.9     # J/g°C (specific heat of calorimeter material)
        # --- MAIN NOTEBOOK ---
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        # ...lanjutkan inisialisasi lain, tanpa header/footer window dan tanpa set title/geometry...

        # Tab 1: Menentukan Kapasitas Kalor (H)
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="1. T2: Kapasitas Kalor Kalorimeter (H)")
        self.setup_simulasi_h()

        # Tab 2: Menentukan Kalor Lebur Es (Les)
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="2. T3: Kalor Lebur Es (L)")
        self.setup_simulasi_L()

        # Initial State
        self.update_preview_h()

    def create_header(self):
        header_frame = tk.Frame(self.root, bg=self.bg_color, pady=15)
        header_frame.pack(side="top", fill="x")
        
        tk.Label(header_frame, text="VIRTUAL LAB: KAPASITAS KALOR & KALOR LEBUR ES", 
                 font=("Arial", 24, "bold"), fg="white", bg=self.bg_color).pack()
        tk.Label(header_frame, text="Penerapan Azas Black dalam Kalorimeter", 
                 font=("Arial", 14), fg="#bdc3c7", bg=self.bg_color).pack()
        tk.Label(header_frame, text="Pengembang Aplikasi: Yohanes Kurniawan", 
                 font=("Arial", 14, "bold"), fg="white", bg=self.bg_color).pack(pady=(5, 0))

    def create_footer(self):
        footer_frame = tk.Frame(self.root, bg=self.bg_color, pady=8)
        footer_frame.pack(side="bottom", fill="x")
        
        tk.Label(footer_frame, text="VERSI APLIKASI PRO", 
                 font=("Arial", 10, "bold"), fg="#e74c3c", bg=self.bg_color).pack(side="left", padx=20)
        
        tk.Label(footer_frame, text="Modul Fisika Dasar: Termodinamika", 
                 font=("Arial", 10), fg="#bdc3c7", bg=self.bg_color).pack(side="right", padx=20)

    # =========================================
    # TAB 1: KAPASITAS KALOR KALORIMETER (H)
    # =========================================
    def setup_simulasi_h(self):
        pane = tk.PanedWindow(self.tab1, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(pane, padding=10)
        pane.add(left_frame, stretch="always")
        
        right_frame = ttk.Frame(pane, padding=10)
        pane.add(right_frame, stretch="always")

        # --- INPUTS ---
        ttk.Label(left_frame, text="PERCOBAAN T2: PENCAMPURAN AIR PANAS & DINGIN", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))

        # 1. Calorimeter Params
        grp1 = ttk.LabelFrame(left_frame, text="1. Persiapan Kalorimeter & Air Dingin")
        grp1.pack(fill="x", pady=5)
        
        ttk.Label(grp1, text="Massa Kalorimeter Kosong (mk) [g]:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.scale_mk = tk.Scale(grp1, from_=50, to=200, orient="horizontal", length=200)
        self.scale_mk.set(120)
        self.scale_mk.grid(row=0, column=1)
        
        ttk.Label(grp1, text="Massa Air Dingin (ma) [g]:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.scale_ma = tk.Scale(grp1, from_=50, to=300, orient="horizontal", length=200)
        self.scale_ma.set(100)
        self.scale_ma.grid(row=1, column=1)
        
        ttk.Label(grp1, text="Suhu Awal Sistem (T1) [°C]:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.scale_t1 = tk.Scale(grp1, from_=20, to=35, orient="horizontal", length=200)
        self.scale_t1.set(25)
        self.scale_t1.grid(row=2, column=1)

        # 2. Hot Water Params
        grp2 = ttk.LabelFrame(left_frame, text="2. Penambahan Air Panas")
        grp2.pack(fill="x", pady=10)
        
        ttk.Label(grp2, text="Massa Air Panas (mp) [g]:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.scale_mp = tk.Scale(grp2, from_=50, to=300, orient="horizontal", length=200)
        self.scale_mp.set(100)
        self.scale_mp.grid(row=0, column=1)
        
        ttk.Label(grp2, text="Suhu Air Panas (T2) [°C]:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.scale_t2 = tk.Scale(grp2, from_=40, to=90, orient="horizontal", length=200)
        self.scale_t2.set(60)
        self.scale_t2.grid(row=1, column=1)

        # Action
        self.btn_mix_h = ttk.Button(left_frame, text="Campurkan & Ukur Suhu Akhir", command=self.run_experiment_h)
        self.btn_mix_h.pack(fill="x", pady=10)

        # Results
        self.result_frame_h = ttk.LabelFrame(left_frame, text="Hasil Pengamatan")
        self.result_frame_h.pack(fill="x", pady=5)
        
        self.lbl_tf_h = ttk.Label(self.result_frame_h, text="Suhu Campuran (Tc): - °C", font=("Arial", 14, "bold"), foreground="blue")
        self.lbl_tf_h.pack(pady=5)
        
        self.lbl_calc_h = ttk.Label(self.result_frame_h, text="Nilai H (Kapasitas Kalor) Terhitung: - J/°C")
        self.lbl_calc_h.pack(pady=5)

        # --- VISUALIZATION ---
        self.fig_h = Figure(figsize=(5, 5), dpi=100)
        self.ax_h = self.fig_h.add_subplot(111)
        self.canvas_h = FigureCanvasTkAgg(self.fig_h, master=right_frame)
        self.canvas_h.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def run_experiment_h(self):
        # Retrieve values
        mk = self.scale_mk.get()
        ma = self.scale_ma.get()
        t1 = self.scale_t1.get()
        mp = self.scale_mp.get()
        t2 = self.scale_t2.get()
        
        # Calculate Theoretical Final Temp (Tc)
        # Q_lepas = Q_terima
        # mp * c_air * (t2 - Tc) = ma * c_air * (Tc - t1) + mk * c_alum * (Tc - t1)
        # Note: Usually H = mk * c_alum. So term is H * (Tc - t1).
        
        H_theoretical = mk * self.c_alumunium
        
        # mp*c*(t2) + ma*c*t1 + H*t1 = Tc * (mp*c + ma*c + H)
        numerator = (mp * self.c_air * t2) + (ma * self.c_air * t1) + (H_theoretical * t1)
        denominator = (mp * self.c_air) + (ma * self.c_air) + H_theoretical
        
        Tc_ideal = numerator / denominator
        
        # Add slight experimental noise (+- 0.5 deg) 
        # But for 'perfect' virtual lab, maybe clean data is better for verifying formula?
        # Let's add tiny noise to make it realistic but calculable.
        noise = np.random.normal(0, 0.1) 
        Tc_measured = Tc_ideal + noise
        
        self.lbl_tf_h.config(text=f"Suhu Campuran (Tc): {Tc_measured:.2f} °C")
        
        # Reverse Calculate H from measured Tc to show user the 'experimental' H
        # H = [ mp*c*(t2-Tc) - ma*c*(Tc-t1) ] / (Tc - t1)
        delta_T_cold = Tc_measured - t1
        delta_T_hot = t2 - Tc_measured
        
        if delta_T_cold > 0.1:
            Q_lepas = mp * self.c_air * delta_T_hot
            Q_terima_air = ma * self.c_air * delta_T_cold
            H_exp = (Q_lepas - Q_terima_air) / delta_T_cold
            self.lbl_calc_h.config(text=f"Kapasitas Kalor (H) Eksperimen: {H_exp:.2f} J/°C")
        else:
            self.lbl_calc_h.config(text="Delta T terlalu kecil!")

        self.update_preview_h(level_cold=ma, level_added=mp, temp=Tc_measured, color="#9b59b6")

    def update_preview_h(self, level_cold=100, level_added=0, temp=25, color="#3498db"):
        self.ax_h.clear()
        
        # Draw Calorimeter (Outer + Insulation + Inner)
        cal_width = 3.0
        cal_height = 5.0
        
        # Outer Shell
        self.ax_h.add_patch(patches.Rectangle((-cal_width/2 - 0.2, 0), cal_width + 0.4, cal_height, facecolor="#95a5a6", edgecolor="black"))
        # Inner Cup
        self.ax_h.add_patch(patches.Rectangle((-cal_width/2, 0.2), cal_width, cal_height-0.2, facecolor="#ecf0f1", edgecolor="black"))
        
        # Water Level
        # Scale mass to height roughly. Say 500g max fills cup.
        total_mass = level_cold + level_added
        water_height = (total_mass / 500.0) * (cal_height - 0.5)
        if water_height > cal_height - 0.5: water_height = cal_height - 0.5
        
        self.ax_h.add_patch(patches.Rectangle((-cal_width/2 + 0.1, 0.2), cal_width - 0.2, water_height, facecolor=color, alpha=0.7))
        self.ax_h.text(0, water_height/2 + 0.2, f"Air: {total_mass:.0f}g", ha="center")

        # Thermometer
        self.ax_h.plot([0.5, 0.5], [1, cal_height+1], 'k-', lw=3)
        self.ax_h.plot([0.5], [1], 'ro', markersize=8)
        self.ax_h.text(0.7, cal_height, f"{temp:.1f}°C", fontsize=12, fontweight='bold', color='red')
        
        # Stirrer
        self.ax_h.plot([-0.5, -0.5], [0.5, cal_height+1.5], 'k-', lw=2)
        self.ax_h.plot([-0.8, -0.2], [0.5, 0.5], 'k-', lw=2) # Stirrer loop

        self.ax_h.set_xlim(-3, 3)
        self.ax_h.set_ylim(0, 7)
        self.ax_h.axis('off')
        self.ax_h.set_title("Visualisasi Kalorimeter")
        self.canvas_h.draw()

    # =========================================
    # TAB 2: KALOR LEBUR ES
    # =========================================
    def setup_simulasi_L(self):
        pane = tk.PanedWindow(self.tab2, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(pane, padding=10)
        pane.add(left_frame, stretch="always")
        
        right_frame = ttk.Frame(pane, padding=10)
        pane.add(right_frame, stretch="always")

        # --- INPUTS ---
        ttk.Label(left_frame, text="PERCOBAAN T3: PENCAMPURAN ES & AIR HANGAT", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))

        # 1. System Params (Assume H is known from T2, let's allow user set H)
        grp_sys = ttk.LabelFrame(left_frame, text="1. Parameter Kalorimeter")
        grp_sys.pack(fill="x", pady=5)
        ttk.Label(grp_sys, text="Kapasitas Kalor (H) [J/°C]:").grid(row=0, column=0, sticky="w", padx=5)
        self.entry_H = ttk.Entry(grp_sys, width=10)
        self.entry_H.insert(0, "108.0") # approx for 120g Al
        self.entry_H.grid(row=0, column=1, padx=5, pady=5)

        # 2. Warm Water
        grp_warm = ttk.LabelFrame(left_frame, text="2. Air Hangat dalam Kalorimeter")
        grp_warm.pack(fill="x", pady=5)
        
        ttk.Label(grp_warm, text="Massa Air (ma) [g]:").grid(row=0, column=0, sticky="w", padx=5)
        self.scale_ma_L = tk.Scale(grp_warm, from_=100, to=400, orient="horizontal", length=200)
        self.scale_ma_L.set(200)
        self.scale_ma_L.grid(row=0, column=1)
        
        ttk.Label(grp_warm, text="Suhu Awal (T1) [°C]:").grid(row=1, column=0, sticky="w", padx=5)
        self.scale_t1_L = tk.Scale(grp_warm, from_=25, to=60, orient="horizontal", length=200)
        self.scale_t1_L.set(40)
        self.scale_t1_L.grid(row=1, column=1)

        # 3. Ice Block
        grp_ice = ttk.LabelFrame(left_frame, text="3. Penambahan Es Batu (0°C)")
        grp_ice.pack(fill="x", pady=5)
        
        ttk.Label(grp_ice, text="Massa Es (m_es) [g]:").grid(row=0, column=0, sticky="w", padx=5)
        self.scale_mes = tk.Scale(grp_ice, from_=10, to=100, orient="horizontal", length=200)
        self.scale_mes.set(30)
        self.scale_mes.grid(row=0, column=1)

        self.btn_mix_L = ttk.Button(left_frame, text="Masukkan Es & Ukur Suhu Akhir", command=self.run_experiment_L)
        self.btn_mix_L.pack(fill="x", pady=15)

        # Results
        self.result_frame_L = ttk.LabelFrame(left_frame, text="Hasil Pengamatan")
        self.result_frame_L.pack(fill="x", pady=5)
        
        self.lbl_tf_L = ttk.Label(self.result_frame_L, text="Suhu Akhir Campuran (Tc): - °C", font=("Arial", 14, "bold"), foreground="blue")
        self.lbl_tf_L.pack(pady=5)
        self.lbl_calc_L = ttk.Label(self.result_frame_L, text="Kalor Lebur Es (L) Eksperimen: - J/g")
        self.lbl_calc_L.pack(pady=5)
        
        # --- GRAPH ---
        self.fig_L = Figure(figsize=(5, 4), dpi=100)
        self.ax_L = self.fig_L.add_subplot(111)
        self.canvas_L = FigureCanvasTkAgg(self.fig_L, master=right_frame)
        self.canvas_L.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def run_experiment_L(self):
        try:
            H = float(self.entry_H.get())
            ma = self.scale_ma_L.get()
            t1 = self.scale_t1_L.get()
            mes = self.scale_mes.get()
            
            # Theoretical Calculation
            # Q_lepas = (ma * c_air + H) * (t1 - Tc)
            # Q_terima = mes * L_es + mes * c_air * (Tc - 0)
            
            # Solving for Tc:
            # (ma*c + H)*t1 - (ma*c + H)*Tc = mes*L + mes*c*Tc
            # (ma*c + H)*t1 - mes*L = Tc * (mes*c + ma*c + H)
            
            L_theory = 334.0
            
            numerator = ((ma * self.c_air + H) * t1) - (mes * L_theory)
            denominator = (mes * self.c_air) + (ma * self.c_air) + H
            
            Tc_sim = numerator / denominator
            
            if Tc_sim < 0:
                self.lbl_tf_L.config(text="Es tidak mencair sepenuhnya (Suhu < 0)!")
                self.lbl_calc_L.config(text="Gunakan lebih banyak air hangat.")
                self.plot_graph_L(t1, 0, mes, melt_full=False)
                return
                
            # Add noise
            Tc_measured = Tc_sim + np.random.normal(0, 0.1)
            
            self.lbl_tf_L.config(text=f"Suhu Akhir Campuran (Tc): {Tc_measured:.2f} °C")
            
            # Recalculate L from data
            # L = [ (ma*c + H)(t1 - Tc) - mes*c*Tc ] / mes
            Q_lepas = (ma * self.c_air + H) * (t1 - Tc_measured)
            Q_terima_air_es = mes * self.c_air * (Tc_measured - 0)
            
            L_exp = (Q_lepas - Q_terima_air_es) / mes
            self.lbl_calc_L.config(text=f"Kalor Lebur Es (L) Eksperimen: {L_exp:.2f} J/g\n(Teori: 334 J/g)")
            
            self.plot_graph_L(t1, Tc_measured, mes, melt_full=True)
            
        except ValueError:
            messagebox.showerror("Error", "Nilai H harus angka valid!")

    def plot_graph_L(self, t_start, t_end, m_es, melt_full=True):
        self.ax_L.clear()
        
        # Simple Temperature vs Time schematic
        # Phase 1: Rapid drop as ice melts? No, usually linear approximation for education
        
        time = [0, 2, 8, 10]
        temp = [t_start, t_end, t_end, t_end] 
        # Actually it goes from t1 down to t_end asymptotically.
        
        # Let's generate a cooling curve
        t_vals = np.linspace(0, 30, 100)
        # T(t) = T_end + (T_start - T_end) * exp(-k*t)
        temp_curve = t_end + (t_start - t_end) * np.exp(-0.2 * t_vals)
        
        self.ax_L.plot(t_vals, temp_curve, 'r-', lw=2, label='Suhu Sistem')
        self.ax_L.axhline(t_end, color='blue', linestyle='--', label=f'Te setimbang: {t_end:.1f}°C')
        
        self.ax_L.set_xlabel("Waktu (detik/relatif)")
        self.ax_L.set_ylabel("Suhu (°C)")
        self.ax_L.set_title("Grafik Perubahan Suhu Sistem Pencampuran")
        self.ax_L.legend()
        self.ax_L.grid(True)
        self.canvas_L.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabKalorimeter(root)
    root.mainloop()
