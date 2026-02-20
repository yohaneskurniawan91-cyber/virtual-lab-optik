import tkinter as tk
from tkinter import ttk, messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as patches

class VirtualLabTermometer:
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

        # Initialize State
        self.L_bawah = 5.0  # cm (Default simulation value for 0 deg C)
        self.L_atas = 25.0  # cm (Default simulation value for 100 deg C)
        
        self.recorded_Lb = None
        self.recorded_La = None
        
        # Random unknown temp for simulation
        self.current_unknown_temp = 50.0 

        # Tab 1: Simulasi Kalibrasi (Peneraan)
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="1. Simulasi Kalibrasi Termometer")
        self.setup_simulasi()

        # Tab 2: Konversi Skala
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="2. Perbandingan Skala Suhu")
        self.setup_konversi() 

    def create_header(self):
        header_frame = tk.Frame(self.root, bg=self.bg_color, pady=15)
        header_frame.pack(side="top", fill="x")
        tk.Label(header_frame, text="VIRTUAL LAB: PENERAPAN TERMOMETER", 
                 font=("Arial", 24, "bold"), fg="white", bg=self.bg_color).pack()
        tk.Label(header_frame, text="Prinsip Kalibrasi Titik Tetap Bawah dan Atas", 
                 font=("Arial", 14), fg="#bdc3c7", bg=self.bg_color).pack()
        tk.Label(header_frame, text="Pengembang Aplikasi: Yohanes Kurniawan", 
                 font=("Arial", 14, "bold"), fg="white", bg=self.bg_color).pack(pady=(5, 0))

    def create_footer(self):
        footer_frame = tk.Frame(self.root, bg=self.bg_color, pady=8)
        footer_frame.pack(side="bottom", fill="x")
        
        tk.Label(footer_frame, text="VERSI APLIKASI PRO", 
                 font=("Arial", 10, "bold"), fg="#e74c3c", bg=self.bg_color).pack(side="left", padx=20)
        
        tk.Label(footer_frame, text="Modul Fisika Dasar: Panas & Kalor", 
                 font=("Arial", 10), fg="#bdc3c7", bg=self.bg_color).pack(side="right", padx=20)

    # =========================================
    # TAB 1: SIMULASI KALIBRASI
    # =========================================
    def setup_simulasi(self):
        pane = tk.PanedWindow(self.tab1, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(pane, padding=10)
        pane.add(left_frame, stretch="always")
        
        right_frame = ttk.Frame(pane, padding=10)
        pane.add(right_frame, stretch="always")

        # --- CONTROLS ---
        ttk.Label(left_frame, text="LANGKAH 1: PROSES KALIBRASI", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))

        cal_frame = ttk.LabelFrame(left_frame, text="Tentukan Titik Tetap")
        cal_frame.pack(fill="x", pady=5)
        
        ttk.Button(cal_frame, text="1. Celupkan ke Es Mencair (0°C)", command=lambda: self.set_environment(0)).pack(fill='x', padx=5, pady=5)
        ttk.Button(cal_frame, text="2. Celupkan ke Air Mendidih (100°C)", command=lambda: self.set_environment(100)).pack(fill='x', padx=5, pady=5)
        
        self.btn_record = ttk.Button(cal_frame, text="Catat Panjang Raksa Saat Ini", command=self.record_calibration_point)
        self.btn_record.pack(fill='x', padx=5, pady=10)
        
        self.lbl_cal_status_0 = ttk.Label(cal_frame, text="Titik Bawah (Lb): - cm", foreground="red")
        self.lbl_cal_status_0.pack(anchor="w", padx=10)
        self.lbl_cal_status_100 = ttk.Label(cal_frame, text="Titik Atas (La): - cm", foreground="red")
        self.lbl_cal_status_100.pack(anchor="w", padx=10)
        
        ttk.Label(left_frame, text="LANGKAH 2: PENGUKURAN ZAT X", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20, 10))
        
        measure_frame = ttk.LabelFrame(left_frame, text="Ukur Suhu Benda Asing")
        measure_frame.pack(fill="x", pady=5)
        
        ttk.Button(measure_frame, text="Ambil Zat Cair Misterius", command=self.generate_unknown).pack(fill='x', padx=5, pady=5)
        self.lbl_current_length = ttk.Label(measure_frame, text="Panjang Raksa Terukur (Lx): - cm", font=("Arial", 11, "bold"))
        self.lbl_current_length.pack(pady=10)
        
        # Calculation Result
        self.result_frame = ttk.LabelFrame(left_frame, text="Hasil Perhitungan Suhu")
        self.result_frame.pack(fill="x", pady=10)
        
        self.lbl_result_calc = ttk.Label(self.result_frame, text="T = ? °C", font=("Arial", 16, "bold"), foreground="#2980b9")
        self.lbl_result_calc.pack(pady=10)
        ttk.Button(self.result_frame, text="Hitung Suhu (Lx - Lb)/(La - Lb) * 100", command=self.calculate_temperature).pack(fill='x', padx=5)

        # --- VISUALIZATION ---
        self.fig_sim = Figure(figsize=(4, 6), dpi=100)
        self.ax_sim = self.fig_sim.add_subplot(111)
        self.canvas_sim = FigureCanvasTkAgg(self.fig_sim, master=right_frame)
        self.canvas_sim.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.current_sim_temp = 25.0 # Room temp default
        self.draw_thermometer()

    def set_environment(self, temp):
        self.current_sim_temp = temp
        self.draw_thermometer()

    def generate_unknown(self):
        self.current_unknown_temp = random.uniform(10, 90)
        self.current_sim_temp = self.current_unknown_temp
        self.draw_thermometer()

    def get_length_from_temp(self, temp):
        # Linear map: 0C -> 5cm, 100C -> 25cm. Slope = 0.2 cm/C.
        # L = 5 + 0.2*T
        return self.L_bawah + ((self.L_atas - self.L_bawah) / 100.0) * temp

    def record_calibration_point(self):
        L_current = self.get_length_from_temp(self.current_sim_temp)
        
        if self.current_sim_temp == 0:
            self.recorded_Lb = L_current
            self.lbl_cal_status_0.config(text=f"Titik Bawah (Lb): {L_current:.1f} cm", foreground="green")
            messagebox.showinfo("Sukses", f"Titik Tetap Bawah dikalibrasi pada {L_current} cm")
        elif self.current_sim_temp == 100:
            self.recorded_La = L_current
            self.lbl_cal_status_100.config(text=f"Titik Atas (La): {L_current:.1f} cm", foreground="green")
            messagebox.showinfo("Sukses", f"Titik Tetap Atas dikalibrasi pada {L_current} cm")
        else:
            messagebox.showwarning("Peringatan", "Suhu saat ini bukan 0°C atau 100°C. Tidak bisa dijadikan titik tetap standar.")

    def calculate_temperature(self):
        if self.recorded_Lb is None or self.recorded_La is None:
            messagebox.showerror("Error", "Lakukan kalibrasi Titik Bawah dan Titik Atas terlebih dahulu!")
            return
            
        Lx = self.get_length_from_temp(self.current_sim_temp)
        
        # T = (Lx - Lb) / (La - Lb) * 100
        try:
            T_calc = (Lx - self.recorded_Lb) / (self.recorded_La - self.recorded_Lb) * 100
            self.lbl_result_calc.config(text=f"T = {T_calc:.2f} °C")
            
            # Verify accuracy
            error = abs(T_calc - self.current_sim_temp)
            if error < 0.1:
                self.lbl_result_calc.config(foreground="green")
            else:
                 self.lbl_result_calc.config(foreground="red") # Should not happen in ideal math
                 
        except ZeroDivisionError:
            messagebox.showerror("Error", "Rentang kalibrasi nol!")

    def draw_thermometer(self):
        self.ax_sim.clear()
        
        # Draw Glass Tube
        tube_width = 1.0
        tube_height = 30.0 # scale up to 30cm
        self.ax_sim.add_patch(patches.Rectangle((-tube_width/2, 0), tube_width, tube_height, 
                                                facecolor='#ecf0f1', edgecolor='black'))
        
        # Calculate Mercury Height
        mercury_h = self.get_length_from_temp(self.current_sim_temp)
        self.lbl_current_length.config(text=f"Panjang Raksa Terukur (Lx): {mercury_h:.2f} cm")
        
        # Draw Mercury
        self.ax_sim.add_patch(patches.Rectangle((-tube_width/2 + 0.1, 0), tube_width - 0.2, mercury_h, 
                                                facecolor='#e74c3c', edgecolor='black'))
        
        # Analysis info
        self.ax_sim.text(0.8, mercury_h, f"L = {mercury_h:.1f} cm", va='center')
        
        # Draw Bulb at bottom
        bulb_radius = 1.5
        circle = patches.Circle((0, -bulb_radius+0.5), bulb_radius, color='#e74c3c')
        self.ax_sim.add_patch(circle)
        
        # Scale Ticks (Ruler simulation next to it)
        for i in range(0, 31, 1):
            length = 0.5 if i % 5 == 0 else 0.2
            self.ax_sim.plot([-tube_width/2 - length, -tube_width/2], [i, i], 'k-', lw=1)
            if i % 5 == 0:
                self.ax_sim.text(-tube_width/2 - 1.5, i, f"{i}", ha='right', va='center', fontsize=8)

        # Environment Clues
        env_text = ""
        if self.current_sim_temp <= 0:
            env_text = "LINGKUNGAN: ES MENCAIR ❄️"
            self.ax_sim.set_facecolor('#d6eaf8')
        elif self.current_sim_temp >= 100:
            env_text = "LINGKUNGAN: AIR MENDIDIH ♨️"
            self.ax_sim.set_facecolor('#fAD7A0')
        else:
            env_text = "LINGKUNGAN: SUHU RUANG / ZAT CAIR"
        
        self.ax_sim.set_title(env_text, fontsize=10, fontweight='bold')
        self.ax_sim.axis('off')
        self.ax_sim.set_xlim(-5, 5)
        self.ax_sim.set_ylim(-3, 32)
        
        self.canvas_sim.draw()

    # =========================================
    # TAB 2: KONVERSI SUHU
    # =========================================
    def setup_konversi(self):
        pane = tk.PanedWindow(self.tab2, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)
        
        left_frame = ttk.Frame(pane, padding=10)
        pane.add(left_frame, stretch="always")
        
        right_frame = ttk.Frame(pane, padding=10)
        pane.add(right_frame, stretch="always")
        
        ttk.Label(left_frame, text="KOMPARASI 4 TERMOMETER", font=("Arial", 12, "bold")).pack(anchor="w", pady=10)
        
        # Input Slider
        ttk.Label(left_frame, text="Atur Suhu (Celsius):").pack(anchor="w")
        self.var_conv_c = tk.DoubleVar(value=0.0)
        
        scale = tk.Scale(left_frame, from_=-20, to=120, resolution=1, orient="horizontal", 
                         variable=self.var_conv_c, length=300, command=self.update_conversion)
        scale.pack(pady=10)
        
        # Display Values
        self.disp_frame = ttk.LabelFrame(left_frame, text="Bacaan Termometer")
        self.disp_frame.pack(fill="x", pady=10)
        
        self.lbl_C = ttk.Label(self.disp_frame, text="Celcius: 0 °C", font=("Courier", 12))
        self.lbl_C.pack(anchor="w", padx=10, pady=5)
        self.lbl_R = ttk.Label(self.disp_frame, text="Reamur: 0 °R", font=("Courier", 12))
        self.lbl_R.pack(anchor="w", padx=10, pady=5)
        self.lbl_F = ttk.Label(self.disp_frame, text="Fahrenheit: 32 °F", font=("Courier", 12))
        self.lbl_F.pack(anchor="w", padx=10, pady=5)
        self.lbl_K = ttk.Label(self.disp_frame, text="Kelvin: 273 K", font=("Courier", 12))
        self.lbl_K.pack(anchor="w", padx=10, pady=5)

        # Graph
        self.fig_conv = Figure(figsize=(5, 4), dpi=100)
        self.ax_conv = self.fig_conv.add_subplot(111)
        self.canvas_conv = FigureCanvasTkAgg(self.fig_conv, master=right_frame)
        self.canvas_conv.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.update_conversion()

    def update_conversion(self, event=None):
        C = self.var_conv_c.get()
        
        R = (4/5) * C
        F = (9/5) * C + 32
        K = C + 273.15
        
        self.lbl_C.config(text=f"Celcius    (C): {C:6.1f} °")
        self.lbl_R.config(text=f"Reamur     (R): {R:6.1f} °")
        self.lbl_F.config(text=f"Fahrenheit (F): {F:6.1f} °")
        self.lbl_K.config(text=f"Kelvin     (K): {K:6.1f}")
        
        self.draw_comparison_bars(C, R, F, K)

    def draw_comparison_bars(self, C, R, F, K):
        self.ax_conv.clear()
        
        # Normalized view? Hard to normalize because ranges differ.
        # Let's just plot bars with values.
        
        # Adjust F for plotting so it's not huge? No, user wants to see values.
        # But Kelvin is huge (300+). 
        # Let's plot scales relative to boiling/freezing points if possible? 
        # Simpler: Bar chart of numerical values but maybe K is broken scale? 
        # No, bar chart represents numerical value.
        
        scales = ['Celcius', 'Reamur', 'Fahrenheit', 'Kelvin - 273']
        values = [C, R, F, K - 273.15] # Reduce K for visual comparisoin
        colors = ['#3498db', '#9b59b6', '#e67e22', '#2ecc71']
        
        bars = self.ax_conv.bar(scales, values, color=colors)
        
        # Add values on top
        real_values = [C, R, F, K]
        for bar, val in zip(bars, real_values):
            height = bar.get_height()
            y_pos = height + (1 if height >= 0 else -5)
            self.ax_conv.text(bar.get_x() + bar.get_width()/2, y_pos, 
                              f"{val:.1f}", ha='center', va='bottom', fontsize=9, fontweight='bold')

        self.ax_conv.set_ylim(min(0, min(values)-10), max(120, max(values)+20))
        self.ax_conv.set_ylabel("Nilai Skala")
        self.ax_conv.set_title("Perbandingan Nilai Suhu (Kelvin disesuaikan -273)")
        self.ax_conv.grid(axis='y', linestyle='--', alpha=0.5)
        
        self.canvas_conv.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabTermometer(root)
    root.mainloop()
