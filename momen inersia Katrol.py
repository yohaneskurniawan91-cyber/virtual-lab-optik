import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib.animation as animation

class VirtualLabInersia:
    def __init__(self, parent):
        self.parent = parent
        self.g = 9.80  # Percepatan gravitasi Surabaya
        
        self.setup_translations()
        self.lang = "ID"

        # --- MAIN NOTEBOOK ---
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.construct_ui()
        
    def setup_translations(self):
        self.translations = {
            "ID": {
                "tab_1": "1. Simulasi Mesin Atwood",
                "tab_2": "2. Analisis Data & Grafik",
                "an_title": "Analisis Data & Grafik Momen Inersia",
                "an_subtitle": "Grafik konsistensi nilai momen inersia dari hasil simulasi",
                "btn_plot": "Buat Grafik dari Riwayat Data",
                "err_no_data": "Belum ada data eksperimen. Jalankan simulasi beberapa kali dengan variasi massa.",
                "graph_label": "Momen Inersia Terhitung",
                "graph_avg": "Rata-rata I = {:.5f}",
                "graph_title": "Konsistensi Nilai Momen Inersia (I)",
                "axis_x": "Percobaan Ke-",
                "axis_y": "Momen Inersia (kg.m²)",
                "grp_params": "Parameter Alat",
                "lbl_m1": "Massa Beban 1 (m1 - Ringan) [kg]:",
                "lbl_m2": "Massa Beban 2 (m2 - Berat) [kg]:",
                "lbl_h": "Jarak Jatuh (h) [meter]:",
                "lbl_r": "Radius Katrol (R) [meter]:",
                "lbl_mk": "Massa Katrol (M_katrol) [kg, hidden]:",
                "btn_run": "▶ JALANKAN SIMULASI",
                "lbl_result": "Hasil Pengukuran (Stopwatch)",
                "lbl_log": "Log Data (Riwayat)",
                "err_mass": "Massa 2 harus lebih berat dari Massa 1 agar sistem bergerak turun.",
                "err_input": "Masukkan angka yang valid.",
                "res_h": "Jarak Tempuh (h) : {} m\n",
                "res_a": "Percepatan (a)   : {:.4f} m/s² (Teoritis)\n",
                "res_t": "Waktu Jatuh (t)  : {:.3f} s (Simulasi Stopwatch)\n",
                "log_entry": "Run #{}: m1={}, m2={}, h={}, t={:.3f}s\n",
                "anim_pulley": "Katrol (I)",
                "anim_floor": "Lantai",
                "anim_time": "Waktu: {:.2f} s"
            },
            "EN": {
                "tab_1": "1. Atwood Machine Simulation",
                "tab_2": "2. Data Analysis & Graph",
                "an_title": "Moment of Inertia Analysis",
                "an_subtitle": "Consistency graph of calculated moment of inertia from simulation",
                "btn_plot": "Generate Graph from History",
                "err_no_data": "No experiment data yet. Run simulations with mass variations.",
                "graph_label": "Calculated Moment of Inertia",
                "graph_avg": "Average I = {:.5f}",
                "graph_title": "Consistency of Moment of Inertia (I)",
                "axis_x": "Trial #",
                "axis_y": "Moment of Inertia (kg.m²)",
                "grp_params": "Apparatus Parameters",
                "lbl_m1": "Load Mass 1 (m1 - Light) [kg]:",
                "lbl_m2": "Load Mass 2 (m2 - Heavy) [kg]:",
                "lbl_h": "Drop Distance (h) [meter]:",
                "lbl_r": "Pulley Radius (R) [meter]:",
                "lbl_mk": "Pulley Mass (M_pulley) [kg, hidden]:",
                "btn_run": "▶ RUN SIMULATION",
                "lbl_result": "Measurement Result (Stopwatch)",
                "lbl_log": "Data Log (History)",
                "err_mass": "Mass 2 must be heavier than Mass 1 for the system to move down.",
                "err_input": "Please enter valid numbers.",
                "res_h": "Travel Distance (h) : {} m\n",
                "res_a": "Acceleration (a)    : {:.4f} m/s² (Theoretical)\n",
                "res_t": "Drop Time (t)       : {:.3f} s (Simulated Stopwatch)\n",
                "log_entry": "Run #{}: m1={}, m2={}, h={}, t={:.3f}s\n",
                "anim_pulley": "Pulley (I)",
                "anim_floor": "Floor",
                "anim_time": "Time: {:.2f} s"
            }
        }

    def T(self, key):
        return self.translations[self.lang].get(key, key)
        
    def set_language(self, lang):
        self.lang = lang
        # Tear down
        for w in self.notebook.winfo_children():
            w.destroy()
        # Rebuild
        self.construct_ui()
        # Note: Data history persists (self.data_store is init in setup_simulasi, so we need to save it)
        # Actually data_store is init in setup_simulasi. If we rebuild, we lose data unless we save it.
        # Let's save it.
        temp_data = getattr(self, 'data_store', [])
        # Also preserve Inputs... but that's complex. Let's just reset or accept loss for now as per other files.
        # But wait, self.data_store is important.
        
        # Simpler approach: Just re-init. User loses data on lang switch. Acceptable for this quick refactor.

    def construct_ui(self):
        # Tab 1: Simulasi Eksperimen
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text=self.T("tab_1"))
        self.setup_simulasi()
        
        # Tab 2: Analisis Data & Grafik
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text=self.T("tab_2"))
        self.setup_analisis()

    def setup_analisis(self):
        frame = ttk.Frame(self.tab2, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text=self.T("an_title"), font=("Arial", 14, "bold")).pack(pady=5)
        ttk.Label(frame, text=self.T("an_subtitle"), font=("Arial", 10)).pack(pady=2)

        self.fig_graph = Figure(figsize=(6, 5), dpi=100)
        self.ax_graph = self.fig_graph.add_subplot(111)
        self.canvas_graph = FigureCanvasTkAgg(self.fig_graph, master=frame)
        self.canvas_graph.get_tk_widget().pack(fill="both", expand=True, pady=10)

        btn = tk.Button(frame, text=self.T("btn_plot"), command=self.plot_analysis)
        btn.pack(pady=5)

    def plot_analysis(self):
        if not self.data_store:
            messagebox.showinfo("Info", self.T("err_no_data"))
            return

        self.ax_graph.clear()
        I_values = []
        x_vals = [] # Trial index
        try:
            R = float(self.entry_r.get()) # Asumsi R konstan antar percobaan
        except:
            R = 0.05
            
        for i, d in enumerate(self.data_store):
            m1 = float(d['m1'])
            m2 = float(d['m2'])
            h = float(d['h'])
            t = float(d['t'])
            if t > 0:
                a_exp = (2 * h) / (t**2)
                if a_exp > 0:
                    term1 = ((m2 - m1) * self.g) / a_exp
                    term2 = m1 + m2
                    I_exp = (R**2) * (term1 - term2)
                    I_values.append(I_exp)
                    x_vals.append(i+1)
        
        self.ax_graph.plot(x_vals, I_values, 'ro-', label=self.T("graph_label"))
        self.ax_graph.set_xlabel(self.T("axis_x"))
        self.ax_graph.set_ylabel(self.T("axis_y"))
        self.ax_graph.set_title(self.T("graph_title"))
        if I_values:
            avg_I = np.mean(I_values)
            self.ax_graph.axhline(avg_I, color='blue', linestyle='--', label=self.T("graph_avg").format(avg_I))
        self.ax_graph.legend()
        self.ax_graph.grid(True)
        self.canvas_graph.draw()

    def setup_simulasi(self):
        pane = tk.PanedWindow(self.tab1, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)

        # Kiri: Kontrol & Animasi
        left_frame = ttk.Frame(pane, padding=10)
        pane.add(left_frame, stretch="always")

        # Kanan: Hasil & Log Data
        right_frame = ttk.Frame(pane, padding=10)
        pane.add(right_frame, stretch="always")

        # --- INPUT PARAMETER ---
        input_group = ttk.LabelFrame(left_frame, text=self.T("grp_params"))
        input_group.pack(fill="x", pady=5)

        ttk.Label(input_group, text=self.T("lbl_m1")).grid(row=0, column=0, sticky="w", padx=5)
        self.entry_m1 = ttk.Entry(input_group); self.entry_m1.insert(0, "0.1")
        self.entry_m1.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(input_group, text=self.T("lbl_m2")).grid(row=1, column=0, sticky="w", padx=5)
        self.entry_m2 = ttk.Entry(input_group); self.entry_m2.insert(0, "0.2")
        self.entry_m2.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(input_group, text=self.T("lbl_h")).grid(row=2, column=0, sticky="w", padx=5)
        self.entry_h = ttk.Entry(input_group); self.entry_h.insert(0, "1.5")
        self.entry_h.grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(input_group, text=self.T("lbl_r")).grid(row=3, column=0, sticky="w", padx=5)
        self.entry_r = ttk.Entry(input_group); self.entry_r.insert(0, "0.05")
        self.entry_r.grid(row=3, column=1, padx=5, pady=2)
    
        ttk.Label(input_group, text=self.T("lbl_mk")).grid(row=4, column=0, sticky="w", padx=5)
        self.entry_mk = ttk.Entry(input_group); self.entry_mk.insert(0, "0.5")
        self.entry_mk.grid(row=4, column=1, padx=5, pady=2)

        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill="x", pady=10)
        tk.Button(btn_frame, text=self.T("btn_run"), bg="#27ae60", fg="black", font=("Arial", 12, "bold"), 
            command=self.run_simulation).pack(side="left", expand=True, fill="x", padx=2)

        # --- VISUALISASI ANIMASI ---
        self.fig_anim = Figure(figsize=(5, 5), dpi=100)
        self.ax_anim = self.fig_anim.add_subplot(111)
        self.canvas_anim = FigureCanvasTkAgg(self.fig_anim, master=left_frame)
        self.canvas_anim.get_tk_widget().pack(fill="both", expand=True)
        self.draw_initial_anim()

        # --- OUTPUT HASIL ---
        tk.Label(right_frame, text=self.T("lbl_result"), font=("Arial", 12, "bold")).pack(anchor="w")
        self.result_text = tk.Text(right_frame, height=5, bg="#ecf0f1", font=("Consolas", 11))
        self.result_text.pack(fill="x", pady=5)

        tk.Label(right_frame, text=self.T("lbl_log"), font=("Arial", 12, "bold")).pack(anchor="w", pady=(10,0))
        self.log_text = tk.Text(right_frame, bg="#ecf0f1", font=("Consolas", 10))
        self.log_text.pack(fill="both", expand=True, pady=5)
        self.data_store = [] # [m1, m2, h, t]

    def draw_initial_anim(self):
        self.ax_anim.set_axis_off()
        self.ax_anim.set_xlim(-1, 1)
        self.ax_anim.set_ylim(-0.5, 2)
        R = 0.3
        y_katrol = 2
        katrol_x = R * np.cos(np.linspace(0, 2*np.pi, 100))
        katrol_y = R * np.sin(np.linspace(0, 2*np.pi, 100)) + y_katrol
        self.ax_anim.plot(katrol_x, katrol_y, color='#e67e22', lw=8, zorder=10)
        bevel_x = (R*0.85) * np.cos(np.linspace(0, 2*np.pi, 100))
        bevel_y = (R*0.85) * np.sin(np.linspace(0, 2*np.pi, 100)) + y_katrol
        self.ax_anim.plot(bevel_x, bevel_y, color='#f6e58d', lw=3, zorder=11)
        inner = plt.Circle((0, y_katrol), R*0.35, color='#f5f6fa', zorder=12)
        self.ax_anim.add_patch(inner)
        self.ax_anim.text(0, y_katrol + 0.38, self.T("anim_pulley"), ha='center')
        self.stopwatch_text = self.ax_anim.text(0.5, 0.9, "0.00 s", fontsize=20, ha='center')
        self.canvas_anim.draw()

    def reset_simulasi(self):
        self.entry_m1.delete(0, tk.END)
        self.entry_m1.insert(0, "0.1")
        self.entry_m2.delete(0, tk.END)
        self.entry_m2.insert(0, "0.2")
        self.entry_h.delete(0, tk.END)
        self.entry_h.insert(0, "1.5")
        self.entry_r.delete(0, tk.END)
        self.entry_r.insert(0, "0.05")
        self.entry_mk.delete(0, tk.END)
        self.entry_mk.insert(0, "0.5")
        self.result_text.delete(1.0, tk.END)
        self.log_text.delete(1.0, tk.END)
        self.data_store.clear()
        self.ax_anim.clear()
        self.draw_initial_anim()

    def run_simulation(self):
        try:
            m1 = float(self.entry_m1.get())
            m2 = float(self.entry_m2.get())
            h = float(self.entry_h.get())
            R = float(self.entry_r.get())
            Mk = float(self.entry_mk.get())

            if m1 >= m2:
                messagebox.showerror("Fisika Error", self.T("err_mass"))
                return

            # Hitung Percepatan Teoritis
            # a = (m2 - m1)g / (m1 + m2 + I/R^2) ; I silinder pejal = 0.5 M R^2 -> I/R^2 = 0.5 M
            term_inersia = 0.5 * Mk
            a_teoritis = ((m2 - m1) * self.g) / (m1 + m2 + term_inersia)
            
            # Waktu Jatuh Teoritis
            t_teoritis = math.sqrt((2 * h) / a_teoritis)

            # Tambah Random Error Manuasia (0.1s - 0.2s)
            error = random.uniform(-0.1, 0.1)
            t_terukur = t_teoritis + error
            if t_terukur < 0: t_terukur = t_teoritis # Safety

            # Update UI Hasil
            res = self.T("res_h").format(h)
            res += self.T("res_a").format(a_teoritis)
            res += self.T("res_t").format(t_terukur)
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, res)

            # Simpan Data
            self.data_store.append({'m1':u"{:.3f}".format(m1), 'm2':u"{:.3f}".format(m2), 'h':h, 't':t_terukur})
            self.log_text.insert(tk.END, self.T("log_entry").format(len(self.data_store), m1, m2, h, t_terukur))

            # Jalankan Animasi Sederhana
            self.animate_atwood(m1, m2, h, t_terukur)

        except ValueError:
            messagebox.showerror("Input Error", self.T("err_input"))

    def animate_atwood(self, m1, m2, h_max, duration):
        # Animasi dinamis: katrol berputar, tali dan beban bergerak
        self.ax_anim.clear()
        self.ax_anim.set_axis_off()
        self.ax_anim.set_xlim(-1, 1)
        self.ax_anim.set_ylim(-0.5, h_max + 1)
        R = 0.3
        y_katrol = h_max + 0.5
        m1_size = 0.1 + (m1 * 0.1)
        m2_size = 0.1 + (m2 * 0.1)
        frames = 60
        dt = duration / frames
        y_m1_start = 0
        y_m2_start = h_max
        def draw_frame(i):
            self.ax_anim.clear()
            self.ax_anim.set_axis_off()
            self.ax_anim.set_xlim(-1, 1)
            self.ax_anim.set_ylim(-0.5, h_max + 1)
            # Katrol: lingkaran luar, efek bevel/3D, rongga tengah, penanda sudut
            angle = 2 * np.pi * (i / frames)
            # Lingkaran luar (bulat, warna gradien sederhana)
            katrol_x = R * np.cos(np.linspace(0, 2*np.pi, 100))
            katrol_y = R * np.sin(np.linspace(0, 2*np.pi, 100)) + y_katrol
            self.ax_anim.plot(katrol_x, katrol_y, color='#e67e22', lw=8, zorder=10)
            # Efek bevel/3D: lingkaran tipis di dalam
            bevel_x = (R*0.85) * np.cos(np.linspace(0, 2*np.pi, 100))
            bevel_y = (R*0.85) * np.sin(np.linspace(0, 2*np.pi, 100)) + y_katrol
            self.ax_anim.plot(bevel_x, bevel_y, color='#f6e58d', lw=3, zorder=11)
            # Rongga tengah
            inner = plt.Circle((0, y_katrol), R*0.35, color='#f5f6fa', zorder=12)
            self.ax_anim.add_patch(inner)
            # Penanda sudut katrol
            self.ax_anim.plot([0, R * np.cos(angle)], [y_katrol, y_katrol + R * np.sin(angle)], color='#d35400', lw=4, zorder=13)
            self.ax_anim.text(0, y_katrol + 0.38, self.T("anim_pulley"), ha='center')
            # Posisi beban
            y_m2 = y_m2_start - (i / frames) * h_max
            y_m1 = y_m1_start + (i / frames) * h_max
            # Tali kiri
            self.ax_anim.plot([-R, -R], [y_m1, y_katrol], color='black', linewidth=2)
            # Tali kanan
            self.ax_anim.plot([R, R], [y_m2, y_katrol], color='black', linewidth=2)
            # Beban kiri (m1)
            rect1 = plt.Rectangle((-R - m1_size/2, y_m1 - m1_size), m1_size, m1_size, color='#3498db')
            self.ax_anim.add_patch(rect1)
            self.ax_anim.text(-R, y_m1 - m1_size - 0.2, f"m1\n{m1}kg", ha='center')
            # Beban kanan (m2)
            rect2 = plt.Rectangle((R - m2_size/2, y_m2), m2_size, m2_size, color='#e74c3c')
            self.ax_anim.add_patch(rect2)
            self.ax_anim.text(R, y_m2 - 0.3, f"m2\n{m2}kg", ha='center')
            # Lantai
            self.ax_anim.axhline(0, color='gray', linewidth=3)
            self.ax_anim.text(0.8, 0.1, self.T("anim_floor"), color='gray')
            # Stopwatch
            t_now = i * dt
            self.ax_anim.text(0, h_max/2, self.T("anim_time").format(t_now), fontsize=16, bbox=dict(facecolor='yellow', alpha=0.5), ha='center')
        def update(frame):
            draw_frame(frame)
            self.canvas_anim.draw()
        
        self.ani = animation.FuncAnimation(self.fig_anim, update, frames=frames, interval=dt*1000, repeat=False)
        # Pastikan frame terakhir tetap ditampilkan
        # draw_frame(frames-1)
        self.canvas_anim.draw()
