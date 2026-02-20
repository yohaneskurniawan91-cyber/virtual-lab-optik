import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

class VirtualLabHukumNewton:
    def __init__(self, parent):
        self.parent = parent
        self.bg_color = "#2c3e50"
        self.text_color = "white"
        self.accent_color = "#3498db"
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.setup_translations()
        self.lang = "ID"
        
        self.init_vars()
        self.setup_ui()
        
    def setup_translations(self):
        self.translations = {
            "ID": {
                "tab1_title": "1. Hukum Newton I & II (Gerak Lurus)",
                "tab2_title": "2. Hukum Newton III (Aksi-Reaksi)",
                "tab3_title": "3. Analisis Data & Ketidakpastian",
                
                # Tab 1
                "t1_param_title": "PARAMETER BENDA & GAYA",
                "t1_mass": "1. Massa Benda (kg):",
                "t1_force": "2. Gaya Dorong (N):",
                "t1_mu": "3. Koef. Gesek (μ):",
                "t1_btn_run": "▶ Jalankan Simulasi",
                "t1_btn_reset": "⟲ Reset",
                "t1_legend_title": "Analisis Hitungan (F = m.a)",
                "t1_res_weight": "Berat (W = m.g): {:.1f} N",
                "t1_res_normal": "Gaya Normal (N): {:.1f} N",
                "t1_res_friction": "Gaya Gesek (f): {:.1f} N",
                "t1_res_net": "Resultan Gaya (ΣF): {:.1f} N",
                "t1_res_acc": "Percepatan (a): {:.2f} m/s²",
                "t1_lbl_weight_ph": "Berat (W = m.g): - N",
                "t1_lbl_normal_ph": "Gaya Normal (N): - N",
                "t1_lbl_fric_ph": "Gaya Gesek (f = μ.N): - N",
                "t1_lbl_net_ph": "Resultan Gaya (ΣF): - N",
                "t1_lbl_acc_ph": "Percepatan (a): - m/s²",
                "t1_graph_title": "Preview Sistem",
                "t1_graph_title_sim": "t={:.2f}s | v={:.2f} m/s | x={:.2f} m",
                
                # Tab 2
                "t2_title": "INTERAKSI DUA BENDA",
                "t2_desc": "Simulasi gaya dorong balik (Recoil) saat dua benda saling menolak.",
                "t2_m1": "Massa Benda A (Kiri) [kg]:",
                "t2_m2": "Massa Benda B (Kanan) [kg]:",
                "t2_f12": "Gaya F12 (N) [A ke B]:",
                "t2_btn_push": "▶ LEMPAR / DORONG",
                "t2_res_wait": "Hasil: Menunggu...",
                "t2_res_fmt": "F12: {} N (A ke B) | F21: {} N (B ke A)\nPercepatan A: {:.2f} m/s² | Percepatan B: {:.2f} m/s²",
                "t2_ana_frame": "Analisis Data Tumbukan",
                "t2_ana_header": "--- ANALISIS DATA TUMBUKAN ---\n",
                "t2_line1": "F12 = {:.2f} N (A ke B), F21 = {:.2f} N (B ke A)\n",
                "t2_table_head": "{:<6}{:>8}{:>10}{:>10}{:>8}{:>10}{:>10}\n",
                "t2_total_init": "\nTotal Momentum Awal: 0.00\n",
                "t2_total_final": "Total Momentum Akhir: {:.2f}\n",
                "t2_conserved": "Kekekalan momentum: {}\n",
                "t2_conserved_yes": "Terpenuhi",
                "t2_conserved_no": "Tidak terpenuhi",
                "t2_graph_title": "Animasi Tumbukan (Aksi-Reaksi)",
                "t2_g_mom_title": "Momentum Total vs Waktu",
                "t2_g_mom_x": "Waktu (s)",
                "t2_g_mom_y": "Momentum (kg m/s)",
                "t2_g_mom_legend": "Total Momentum",

                # Tab 3
                "t3_input_title": "INPUT DATA PENGUKURAN",
                "t3_input_desc": "Masukkan data percobaan (misal: waktu, jarak) secara berulang.",
                "t3_btn_add": "+ Tambah Data",
                "t3_btn_clear": "Hapus Semua",
                "t3_col_no": "No",
                "t3_col_val": "Nilai Data (x)",
                "t3_col_dev": "Simpang (x - x̄)",
                "t3_col_sq": "Kuadrat Simpang (x - x̄)²",
                "t3_stats_title": "HASIL ANALISIS STATISTIK",
                "t3_stats_frame": "Ringkasan Statistik",
                "t3_lbl_N": "Jumlah Data (N): {}",
                "t3_lbl_mean": "Rata-rata (x̄): {:.4f}",
                "t3_lbl_std": "Standar Deviasi (s): {:.4f}",
                "t3_lbl_unc": "Ketidakpastian (Δx): {:.4f}",
                "t3_lbl_ralat": "Ralat Relatif (KR): {:.2f}%",
                "t3_res_report": "Laporan: x = ( {} ± {} ) unit",
                "t3_res_ph": "Laporan: x = ( ... ± ... )",
                "t3_hist_title": "Distribusi Data Pengukuran",
                "t3_hist_x": "Nilai Data",
                "t3_hist_y": "Frekuensi",
                "t3_hist_legend": "Rata-rata: {:.2f}",
                
                "msg_error": "Error",
                "msg_invalid": "Input tidak valid!",
                "msg_num_only": "Input harus berupa angka"
            },
            "EN": {
                "tab1_title": "1. Newton's I & II Laws (Linear Motion)",
                "tab2_title": "2. Newton's III Law (Action-Reaction)",
                "tab3_title": "3. Data Analysis & Uncertainty",
                
                # Tab 1
                "t1_param_title": "OBJECT & FORCE PARAMETERS",
                "t1_mass": "1. Object Mass (kg):",
                "t1_force": "2. Push Force (N):",
                "t1_mu": "3. Friction Coeff (μ):",
                "t1_btn_run": "▶ Run Simulation",
                "t1_btn_reset": "⟲ Reset",
                "t1_legend_title": "Calculation Analysis (F = m.a)",
                "t1_res_weight": "Weight (W = m.g): {:.1f} N",
                "t1_res_normal": "Normal Force (N): {:.1f} N",
                "t1_res_friction": "Friction Force (f): {:.1f} N",
                "t1_res_net": "Net Force (ΣF): {:.1f} N",
                "t1_res_acc": "Acceleration (a): {:.2f} m/s²",
                "t1_lbl_weight_ph": "Weight (W = m.g): - N",
                "t1_lbl_normal_ph": "Normal Force (N): - N",
                "t1_lbl_fric_ph": "Friction Force (f = μ.N): - N",
                "t1_lbl_net_ph": "Net Force (ΣF): - N",
                "t1_lbl_acc_ph": "Acceleration (a): - m/s²",
                "t1_graph_title": "System Preview",
                "t1_graph_title_sim": "t={:.2f}s | v={:.2f} m/s | x={:.2f} m",
                
                # Tab 2
                "t2_title": "TWO OBJECT INTERACTION",
                "t2_desc": "Recoil force simulation when two objects repel each other.",
                "t2_m1": "Mass Object A (Left) [kg]:",
                "t2_m2": "Mass Object B (Right) [kg]:",
                "t2_f12": "Force F12 (N) [A to B]:",
                "t2_btn_push": "▶ THROW / PUSH",
                "t2_res_wait": "Result: Waiting...",
                "t2_res_fmt": "F12: {} N (A to B) | F21: {} N (B to A)\nAcceleration A: {:.2f} m/s² | Acceleration B: {:.2f} m/s²",
                "t2_ana_frame": "Collision Data Analysis",
                "t2_ana_header": "--- COLLISION DATA ANALYSIS ---\n",
                "t2_line1": "F12 = {:.2f} N (A to B), F21 = {:.2f} N (B to A)\n",
                "t2_table_head": "{:<6}{:>8}{:>10}{:>10}{:>8}{:>10}{:>10}\n",
                "t2_total_init": "\nTotal Initial Momentum: 0.00\n",
                "t2_total_final": "Total Final Momentum: {:.2f}\n",
                "t2_conserved": "Momentum conservation: {}\n",
                "t2_conserved_yes": "Fulfilled",
                "t2_conserved_no": "Not fulfilled",
                "t2_graph_title": "Collision Animation (Action-Reaction)",
                "t2_g_mom_title": "Total Momentum vs Time",
                "t2_g_mom_x": "Time (s)",
                "t2_g_mom_y": "Momentum (kg m/s)",
                "t2_g_mom_legend": "Total Momentum",

                # Tab 3
                "t3_input_title": "MEASUREMENT DATA INPUT",
                "t3_input_desc": "Enter experiment data (e.g., time, distance) repeatedly.",
                "t3_btn_add": "+ Add Data",
                "t3_btn_clear": "Delete All",
                "t3_col_no": "No",
                "t3_col_val": "Data Value (x)",
                "t3_col_dev": "Deviation (x - x̄)",
                "t3_col_sq": "Sq Deviation (x - x̄)²",
                "t3_stats_title": "STATISTICAL ANALYSIS RESULTS",
                "t3_stats_frame": "Statistical Summary",
                "t3_lbl_N": "Data Count (N): {}",
                "t3_lbl_mean": "Mean (x̄): {:.4f}",
                "t3_lbl_std": "Std Deviation (s): {:.4f}",
                "t3_lbl_unc": "Uncertainty (Δx): {:.4f}",
                "t3_lbl_ralat": "Relative Error (KR): {:.2f}%",
                "t3_res_report": "Report: x = ( {} ± {} ) unit",
                "t3_res_ph": "Report: x = ( ... ± ... )",
                "t3_hist_title": "Measurement Data Distribution",
                "t3_hist_x": "Data Value",
                "t3_hist_y": "Frequency",
                "t3_hist_legend": "Mean: {:.2f}",
                
                "msg_error": "Error",
                "msg_invalid": "Invalid input!",
                "msg_num_only": "Input must be a number"
            }
        }
        
    def T(self, key):
        return self.translations[self.lang].get(key, key)
        
    def init_vars(self):
        # Tab 1 Vars
        self.var_mass = tk.DoubleVar(value=5.0)
        self.var_force = tk.DoubleVar(value=20.0)
        self.var_friction = tk.DoubleVar(value=0.2)
        self.var_gravity = tk.DoubleVar(value=9.8)
        
        # Tab 2 Vars
        self.var_m1 = tk.DoubleVar(value=2.0)
        self.var_m2 = tk.DoubleVar(value=4.0)
        self.var_force_explode = tk.DoubleVar(value=50.0)
        
        # Tab 3 Vars
        self.var_data_input = tk.DoubleVar()
        self.data_values = []
        
        # Animation refs
        self.ani = None
        self.ani_recoil = None
        
    def setup_ui(self):
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text=self.T("tab1_title"))
        self.setup_simulasi_gerak()
        
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text=self.T("tab2_title"))
        self.setup_aksi_reaksi()
        
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text=self.T("tab3_title"))
        self.setup_analisis_data() 
        
        # Restore data view if it exists
        if hasattr(self, 'data_values') and self.data_values:
            self.update_analysis_table()
        
    def set_language(self, lang):
        self.lang = lang
        # Stop animations if running
        if self.ani and self.ani.event_source:
            self.ani.event_source.stop()
        if self.ani_recoil and self.ani_recoil.event_source:
             self.ani_recoil.event_source.stop()
             
        # Destroy notebook
        self.notebook.destroy()
        
        # Rebuild
        self.setup_ui()

    def create_header(self):
        # Stub or legacy
        pass

    def create_footer(self):
        # Stub or legacy
        pass

    # =========================================
    # TAB 1: SIMULASI HUKUM NEWTON I & II
    # =========================================
    def setup_simulasi_gerak(self):
        pane = tk.PanedWindow(self.tab1, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)

        # Panel Kiri (Input)
        left_frame = ttk.Frame(pane, padding=10)
        pane.add(left_frame, stretch="always")

        # Panel Kanan (Visualisasi)
        right_frame = ttk.Frame(pane, padding=10)
        pane.add(right_frame, stretch="always")

        # --- INPUT CONTROLS ---
        ttk.Label(left_frame, text=self.T("t1_param_title"), font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))

        # Form Layout
        form_frame = ttk.Frame(left_frame)
        form_frame.pack(fill="x", pady=5)

        # Massa
        ttk.Label(form_frame, text=self.T("t1_mass")).grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(form_frame, textvariable=self.var_mass, width=10).grid(row=0, column=1, sticky="w")

        # Gaya Dorong
        ttk.Label(form_frame, text=self.T("t1_force")).grid(row=1, column=0, sticky="w", pady=5)
        self.scale_force = tk.Scale(form_frame, from_=0, to=100, orient="horizontal", 
                                    variable=self.var_force, length=200)
        self.scale_force.grid(row=1, column=1, sticky="w")

        # Koefisien Gesek
        ttk.Label(form_frame, text=self.T("t1_mu")).grid(row=2, column=0, sticky="w", pady=5)
        self.scale_friction = tk.Scale(form_frame, from_=0.0, to=1.0, resolution=0.05, 
                                       orient="horizontal", variable=self.var_friction, length=200)
        self.scale_friction.grid(row=2, column=1, sticky="w")

        # Buttons
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill="x", pady=20)
        
        ttk.Button(btn_frame, text=self.T("t1_btn_run"), command=self.run_simulation_gerak).pack(side="left", padx=5)
        ttk.Button(btn_frame, text=self.T("t1_btn_reset"), command=self.reset_simulasi_gerak).pack(side="left", padx=5)

        # Legend Info
        info_frame = ttk.LabelFrame(left_frame, text=self.T("t1_legend_title"))
        info_frame.pack(fill="x", pady=10)
        
        self.lbl_weight = ttk.Label(info_frame, text=self.T("t1_lbl_weight_ph"))
        self.lbl_weight.pack(anchor="w", padx=5)
        self.lbl_normal = ttk.Label(info_frame, text=self.T("t1_lbl_normal_ph"))
        self.lbl_normal.pack(anchor="w", padx=5)
        self.lbl_fric_force = ttk.Label(info_frame, text=self.T("t1_lbl_fric_ph"))
        self.lbl_fric_force.pack(anchor="w", padx=5)
        self.lbl_net_force = ttk.Label(info_frame, text=self.T("t1_lbl_net_ph"))
        self.lbl_net_force.pack(anchor="w", padx=5)
        self.lbl_accel = ttk.Label(info_frame, text=self.T("t1_lbl_acc_ph"), font=("Arial", 10, "bold"))
        self.lbl_accel.pack(anchor="w", padx=5, pady=5)

        # --- VISUALIZATION SETUP ---
        self.fig_gerak = Figure(figsize=(6, 5), dpi=100)
        self.ax_gerak = self.fig_gerak.add_subplot(111)
        self.ax_gerak.set_aspect('equal')
        
        self.canvas_gerak = FigureCanvasTkAgg(self.fig_gerak, master=right_frame)
        self.canvas_gerak.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.reset_simulasi_gerak()

    def reset_simulasi_gerak(self):
        self.ax_gerak.clear()
        
        # Ground
        self.ax_gerak.add_patch(patches.Rectangle((-2, -1), 14, 1, color="#7f8c8d"))
        
        # Block (Initial position)
        self.block_patch = patches.Rectangle((0, 0), 2, 1, facecolor="#e74c3c", edgecolor="black")
        self.ax_gerak.add_patch(self.block_patch)
        self.ax_gerak.text(1, 0.5, "Massa", ha="center", va="center", color="white", weight="bold")
        
        self.ax_gerak.set_xlim(-1, 10)
        self.ax_gerak.set_ylim(-2, 3)
        self.ax_gerak.set_title(self.T("t1_graph_title"))
        self.ax_gerak.grid(True, linestyle="--", alpha=0.5)
        self.canvas_gerak.draw()

        # Reset labels
        self.lbl_weight.config(text=self.T("t1_lbl_weight_ph"))
        self.lbl_normal.config(text=self.T("t1_lbl_normal_ph"))
        self.lbl_fric_force.config(text=self.T("t1_lbl_fric_ph"))
        self.lbl_net_force.config(text=self.T("t1_lbl_net_ph"))
        self.lbl_accel.config(text=self.T("t1_lbl_acc_ph"))

    def run_simulation_gerak(self):
        try:
            m = self.var_mass.get()
            F_app = self.var_force.get()
            mu = self.var_friction.get()
            g = self.var_gravity.get()
        except tk.TclError:
            messagebox.showerror(self.T("msg_error"), self.T("msg_invalid"))
            return

        # Physics Calculations
        W = m * g
        N = W
        f_max = mu * N
        
        f_kinetic = f_max
        if F_app > 0:
            F_net = F_app - f_kinetic
        else:
            F_net = 0 
        
        if F_net < 0: 
            F_net = 0
            f_actual = F_app
        else:
            f_actual = f_kinetic

        a = F_net / m
        
        # Update Info
        self.lbl_weight.config(text=self.T("t1_res_weight").format(W))
        self.lbl_normal.config(text=self.T("t1_res_normal").format(N))
        self.lbl_fric_force.config(text=self.T("t1_res_friction").format(f_actual))
        self.lbl_net_force.config(text=self.T("t1_res_net").format(F_net))
        self.lbl_accel.config(text=self.T("t1_res_acc").format(a))

        # Animation Setup
        self.ani_frames = 100
        t_max = 2.0 # seconds
        dt = t_max / self.ani_frames
        
        positions = []
        velocities = []
        x = 0
        v = 0
        for i in range(self.ani_frames):
            v += a * dt
            x += v * dt
            positions.append(x)
            velocities.append(v)

        def update(frame):
            self.ax_gerak.clear()
            
            # Static Environment
            self.ax_gerak.add_patch(patches.Rectangle((-2, -1), 500, 1, color="#7f8c8d"))
            
            current_x = positions[frame]
            
            # Moving Block
            block = patches.Rectangle((current_x, 0), 2, 1, facecolor="#e74c3c", edgecolor="black")
            self.ax_gerak.add_patch(block)
            self.ax_gerak.text(current_x + 1, 0.5, "m", ha="center", va="center", color="white", weight="bold")
            
            # Application Force
            if F_app > 0:
                self.ax_gerak.annotate("", xy=(current_x + 2 + (F_app/100)*2, 0.5), xytext=(current_x + 2, 0.5),
                                     arrowprops=dict(arrowstyle="->", color="blue", lw=2))
                self.ax_gerak.text(current_x + 2.5, 0.6, f"F={F_app}N", color="blue")
            
            # Friction
            if f_actual > 0:
                self.ax_gerak.annotate("", xy=(current_x - (f_actual/100)*2, 0.1), xytext=(current_x, 0.1),
                                     arrowprops=dict(arrowstyle="->", color="red", lw=2))
                self.ax_gerak.text(current_x - 1, 0.2, f"f={f_actual:.1f}N", color="red")

            # Normal & Weight
            self.ax_gerak.annotate("", xy=(current_x + 1, 1.5), xytext=(current_x + 1, 1),
                                 arrowprops=dict(arrowstyle="->", color="green", lw=1))
            self.ax_gerak.text(current_x + 1.1, 1.6, "N", color="green", fontsize=8)
            
            self.ax_gerak.annotate("", xy=(current_x + 1, -0.5), xytext=(current_x + 1, 0),
                                 arrowprops=dict(arrowstyle="->", color="green", lw=1))
            self.ax_gerak.text(current_x + 1.1, -0.6, "W", color="green", fontsize=8)

            # Camera
            view_x = current_x - 2 if current_x > 5 else -1
            self.ax_gerak.set_xlim(view_x, view_x + 12)
            self.ax_gerak.set_ylim(-2, 3)
            
            self.ax_gerak.set_title(self.T("t1_graph_title_sim").format(frame*dt, velocities[frame], current_x))
            self.ax_gerak.grid(True, linestyle="--", alpha=0.5)

        self.ani = FuncAnimation(self.fig_gerak, update, frames=self.ani_frames, interval=30, repeat=False)
        self.canvas_gerak.draw()

    # =========================================
    # TAB 2: SIMULASI HUKUM NEWTON III
    # =========================================
    def setup_aksi_reaksi(self):
        pane = tk.PanedWindow(self.tab2, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(pane, padding=10)
        pane.add(left_frame, stretch="always")
        right_frame = ttk.Frame(pane, padding=10)
        pane.add(right_frame, stretch="always")

        ttk.Label(left_frame, text=self.T("t2_title"), font=("Arial", 12, "bold")).pack(anchor="w", pady=10)
        ttk.Label(left_frame, text=self.T("t2_desc")).pack(anchor="w", pady=5)

        form_frame = ttk.Frame(left_frame)
        form_frame.pack(fill="x", pady=10)

        ttk.Label(form_frame, text=self.T("t2_m1")).grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(form_frame, textvariable=self.var_m1).grid(row=0, column=1)

        ttk.Label(form_frame, text=self.T("t2_m2")).grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(form_frame, textvariable=self.var_m2).grid(row=1, column=1)
        
        ttk.Label(form_frame, text=self.T("t2_f12")).grid(row=2, column=0, sticky="w", pady=5)
        ttk.Entry(form_frame, textvariable=self.var_force_explode).grid(row=2, column=1)

        ttk.Button(left_frame, text=self.T("t2_btn_push"), command=self.run_recoil).pack(pady=20)
        self.lbl_result_iii = ttk.Label(left_frame, text=self.T("t2_res_wait"), font=("Arial", 10))
        self.lbl_result_iii.pack(pady=10)

        # Area analisis data
        analysis_frame = ttk.LabelFrame(right_frame, text=self.T("t2_ana_frame"))
        analysis_frame.pack(fill="x", pady=5)
        self.analysis_text = tk.Text(analysis_frame, height=12, bg="#ecf0f1", font=("Consolas", 11))
        self.analysis_text.pack(fill="both", expand=True)

        # Plot setup
        self.fig_recoil = Figure(figsize=(7, 6), dpi=100)
        self.ax_anim = self.fig_recoil.add_subplot(211)
        self.ax_p = self.fig_recoil.add_subplot(212)
        self.canvas_recoil = FigureCanvasTkAgg(self.fig_recoil, master=right_frame)
        self.canvas_recoil.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.reset_recoil_view()

    def reset_recoil_view(self):
        self.ax_anim.clear()
        self.ax_p.clear()
        self.ax_anim.set_xlim(-10, 10)
        self.ax_anim.set_ylim(-2, 2)
        # Benda A
        a_patch = patches.Rectangle((-2.1, 0), 2, 1, facecolor="#3498db")
        self.ax_anim.add_patch(a_patch)
        self.ax_anim.text(-1.1, 0.5, "A", color="white", ha="center", va="center", weight="bold")
        # Benda B
        b_patch = patches.Rectangle((0.1, 0), 2, 1, facecolor="#e67e22")
        self.ax_anim.add_patch(b_patch)
        self.ax_anim.text(1.1, 0.5, "B", color="white", ha="center", va="center", weight="bold")
        self.ax_anim.axhline(0, color='black', lw=1)
        self.ax_anim.set_title(self.T("t2_graph_title"))
        self.ax_p.set_title("")
        self.canvas_recoil.draw()

    def run_recoil(self):
        try:
            m1 = self.var_m1.get()
            m2 = self.var_m2.get()
            F = self.var_force_explode.get()
        except:
            return
        dt = 0.05
        duration = 2.0
        steps = int(duration / dt)
        push_duration = 0.2
        push_steps = int(push_duration / dt)
        a1_push = -F / m1
        a2_push = F / m2
        t_data = []
        x1_data = []
        x2_data = []
        v1_data = []
        v2_data = []
        p1_data = []
        p2_data = []
        v1, v2 = 0, 0
        x1, x2 = -1.1, 1.1
        for i in range(steps):
            if i < push_steps:
                a1 = a1_push
                a2 = a2_push
            else:
                a1 = 0
                a2 = 0
            v1 += a1 * dt
            v2 += a2 * dt
            x1 += v1 * dt
            x2 += v2 * dt
            t_data.append(i*dt)
            x1_data.append(x1)
            x2_data.append(x2)
            v1_data.append(v1)
            v2_data.append(v2)
            p1_data.append(m1*v1)
            p2_data.append(m2*v2)
        
        self.lbl_result_iii.config(text=self.T("t2_res_fmt").format(F, -F, a1_push, a2_push))
        
        # Analisis Data Tumbukan
        output = self.T("t2_ana_header")
        output += self.T("t2_line1").format(F, -F)
        output += self.T("t2_table_head").format("t(s)", "xA", "vA", "pA", "xB", "vB", "pB")
        output += f"{'-'*62}\n"
        for i in range(0, steps, max(1, steps//20)):
            output += f"{t_data[i]:<6.2f}{x1_data[i]:>8.2f}{v1_data[i]:>10.2f}{p1_data[i]:>10.2f}{x2_data[i]:>8.2f}{v2_data[i]:>10.2f}{p2_data[i]:>10.2f}\n"
        output += self.T("t2_total_init")
        output += self.T("t2_total_final").format(p1_data[-1]+p2_data[-1])
        
        cons = self.T("t2_conserved_yes") if abs(p1_data[-1]+p2_data[-1])<1e-2 else self.T("t2_conserved_no")
        output += self.T("t2_conserved").format(cons)
        
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, output)
        
        # Plot
        self.ax_anim.clear()
        self.ax_p.clear()
        self.ax_anim.set_xlim(-10, 10)
        self.ax_anim.set_ylim(-2, 2)
        self.ax_anim.axhline(0, color='black', lw=1)
        self.ax_anim.set_title(self.T("t2_graph_title"))
        
        self.anim_x1_data = x1_data
        self.anim_x2_data = x2_data
        
        def update_anim(frame):
            self.ax_anim.clear()
            self.ax_anim.set_xlim(-10, 10)
            self.ax_anim.set_ylim(-2, 2)
            self.ax_anim.axhline(0, color='black', lw=1)
            # Benda A
            rect_a = patches.Rectangle((self.anim_x1_data[frame] - 1, 0), 2, 1, facecolor="#3498db")
            self.ax_anim.add_patch(rect_a)
            self.ax_anim.text(self.anim_x1_data[frame], 0.5, "A", color="white", ha="center")
            # Benda B
            rect_b = patches.Rectangle((self.anim_x2_data[frame] - 1, 0), 2, 1, facecolor="#e67e22")
            self.ax_anim.add_patch(rect_b)
            self.ax_anim.text(self.anim_x2_data[frame], 0.5, "B", color="white", ha="center")
            # Vectors during push
            if frame < push_steps:
                self.ax_anim.annotate("", xy=(self.anim_x2_data[frame], 0.5), xytext=(self.anim_x2_data[frame] - 1.5, 0.5),
                                        arrowprops=dict(arrowstyle="->", color="black", lw=2))
                self.ax_anim.annotate("", xy=(self.anim_x1_data[frame], 0.5), xytext=(self.anim_x1_data[frame] + 1.5, 0.5),
                                        arrowprops=dict(arrowstyle="->", color="black", lw=2))
        self.ani_recoil = FuncAnimation(self.fig_recoil, update_anim, frames=len(t_data), interval=30, repeat=False)
        
        # Grafik momentum total
        self.ax_p.plot(t_data, np.array(p1_data)+np.array(p2_data), label=self.T("t2_g_mom_legend"), color='black', linestyle='-')
        self.ax_p.set_title(self.T("t2_g_mom_title"))
        self.ax_p.set_xlabel(self.T("t2_g_mom_x"))
        self.ax_p.set_ylabel(self.T("t2_g_mom_y"))
        self.ax_p.legend()
        self.fig_recoil.tight_layout()
        self.canvas_recoil.draw()

    # =========================================
    # TAB 3: ANALISIS DATA PENGUKURAN
    # =========================================
    def setup_analisis_data(self):
        pane = tk.PanedWindow(self.tab3, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(pane, padding=10)
        pane.add(left_frame, stretch="always") # Input & List
        
        right_frame = ttk.Frame(pane, padding=10)
        pane.add(right_frame, stretch="always") # Stats & Graph

        # --- DATA INPUT ---
        ttk.Label(left_frame, text=self.T("t3_input_title"), font=("Arial", 12, "bold")).pack(anchor="w", pady=10)
        ttk.Label(left_frame, text=self.T("t3_input_desc")).pack(anchor="w")

        input_frame = ttk.Frame(left_frame)
        input_frame.pack(fill="x", pady=10)

        self.entry_data = ttk.Entry(input_frame, textvariable=self.var_data_input)
        self.entry_data.pack(side="left", padx=5)
        self.entry_data.bind('<Return>', lambda e: self.add_data_point())

        ttk.Button(input_frame, text=self.T("t3_btn_add"), command=self.add_data_point).pack(side="left", padx=5)
        ttk.Button(input_frame, text=self.T("t3_btn_clear"), command=self.clear_data).pack(side="left", padx=5)

        # Data List
        columns = ("col1", "col2", "col3", "col4")
        self.tree_data = ttk.Treeview(left_frame, columns=columns, show="headings", height=15)
        
        self.tree_data.heading("col1", text=self.T("t3_col_no"))
        self.tree_data.heading("col2", text=self.T("t3_col_val"))
        self.tree_data.heading("col3", text=self.T("t3_col_dev"))
        self.tree_data.heading("col4", text=self.T("t3_col_sq"))
        
        for col in columns:
            self.tree_data.column(col, width=100, anchor="center")
        
        self.tree_data.pack(fill="both", expand=True, pady=10)
        
        # --- STATISTICS RESULT ---
        ttk.Label(right_frame, text=self.T("t3_stats_title"), font=("Arial", 12, "bold")).pack(anchor="w", pady=10)
        
        self.stats_frame = ttk.LabelFrame(right_frame, text=self.T("t3_stats_frame"))
        self.stats_frame.pack(fill="x", pady=10)
        
        self.lbl_n_data = ttk.Label(self.stats_frame, text=self.T("t3_lbl_N").format(0))
        self.lbl_n_data.pack(anchor="w", padx=10, pady=2)
        
        self.lbl_mean = ttk.Label(self.stats_frame, text=self.T("t3_lbl_mean").format(0.0))
        self.lbl_mean.pack(anchor="w", padx=10, pady=2)
        
        self.lbl_std_dev = ttk.Label(self.stats_frame, text=self.T("t3_lbl_std").format(0.0))
        self.lbl_std_dev.pack(anchor="w", padx=10, pady=2)
        
        self.lbl_uncertainty = ttk.Label(self.stats_frame, text=self.T("t3_lbl_unc").format(0.0))
        self.lbl_uncertainty.pack(anchor="w", padx=10, pady=2)
        
        self.lbl_relative_error = ttk.Label(self.stats_frame, text=self.T("t3_lbl_ralat").format(0.0))
        self.lbl_relative_error.pack(anchor="w", padx=10, pady=2)
        
        self.lbl_final_result = ttk.Label(right_frame, text=self.T("t3_res_ph"), 
                                          font=("Arial", 14, "bold"), foreground="#e74c3c")
        self.lbl_final_result.pack(pady=20)

        # --- GRAPH ---
        self.fig_stats = Figure(figsize=(5, 4), dpi=100)
        self.ax_stats = self.fig_stats.add_subplot(111)
        self.canvas_stats = FigureCanvasTkAgg(self.fig_stats, master=right_frame)
        self.canvas_stats.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def add_data_point(self):
        try:
            val = self.var_data_input.get()
            self.data_values.append(val)
            self.update_analysis_table()
            self.entry_data.delete(0, tk.END) 
        except tk.TclError:
            messagebox.showerror(self.T("msg_error"), self.T("msg_num_only"))

    def clear_data(self):
        self.data_values = []
        self.update_analysis_table()

    def update_analysis_table(self):
        for item in self.tree_data.get_children():
            self.tree_data.delete(item)
            
        N = len(self.data_values)
        if N == 0:
            self.lbl_n_data.config(text=self.T("t3_lbl_N").format(0))
            self.ax_stats.clear()
            self.canvas_stats.draw()
            return

        mean_val = np.mean(self.data_values)
        
        sum_sq_diff = 0
        for i, x in enumerate(self.data_values):
            diff = x - mean_val
            sq_diff = diff ** 2
            sum_sq_diff += sq_diff
            self.tree_data.insert("", "end", values=(i+1, f"{x:.4f}", f"{diff:.4f}", f"{sq_diff:.6f}"))

        if N > 1:
            std_dev = np.sqrt(sum_sq_diff / (N - 1))
            uncertainty = std_dev / np.sqrt(N)
            rel_error = (uncertainty / mean_val) * 100 if mean_val != 0 else 0
        else:
            std_dev = 0
            uncertainty = 0
            rel_error = 0

        self.lbl_n_data.config(text=self.T("t3_lbl_N").format(N))
        self.lbl_mean.config(text=self.T("t3_lbl_mean").format(mean_val))
        self.lbl_std_dev.config(text=self.T("t3_lbl_std").format(std_dev))
        self.lbl_uncertainty.config(text=self.T("t3_lbl_unc").format(uncertainty))
        self.lbl_relative_error.config(text=self.T("t3_lbl_ralat").format(rel_error))
        
        self.lbl_final_result.config(text=self.T("t3_res_report").format(f"{mean_val:.3f}", f"{uncertainty:.3f}"))

        self.ax_stats.clear()
        self.ax_stats.hist(self.data_values, bins='auto', color='#3498db', alpha=0.7, rwidth=0.85)
        self.ax_stats.axvline(mean_val, color='red', linestyle='dashed', linewidth=1, label=self.T("t3_hist_legend").format(mean_val))
        self.ax_stats.set_title(self.T("t3_hist_title"))
        self.ax_stats.set_xlabel(self.T("t3_hist_x"))
        self.ax_stats.set_ylabel(self.T("t3_hist_y"))
        self.ax_stats.legend()
        self.canvas_stats.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabHukumNewton(root)
    root.mainloop()
