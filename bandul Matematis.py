import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from virtual_lab_data_manager import DataManager

class VirtualLabBandul:
    def __init__(self, parent):
        self.parent = parent
        self.bg_color = "#2c3e50"
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.setup_translations()
        self.lang = "ID"
        
        self.init_vars()
        self.setup_ui()
        
    def setup_translations(self):
        self.translations = {
            "ID": {
                "tab1_title": "1. Simulasi Gerak Harmonik Sederhana",
                "tab2_title": "2. Analisis Data & Grafik (T² vs L)",
                "param_sys": "PARAMETER SISTEM",
                "len_str": "Panjang Tali (L) [m]:",
                "grav": "Gravitasi (g) [m/s²]:",
                "angle": "Sudut Awal (θ) [°]:",
                "mass": "Massa Beban (m) [kg]:",
                "btn_start": "▶ Mulai Osilasi",
                "btn_stop": "⏹ Stop / Reset",
                "btn_record_auto": "Catat Data (Auto)",
                "theo_val": "Besaran Teoretis",
                "period": "Periode (T): {:.3f} s",
                "freq": "Frekuensi (f): {:.3f} Hz",
                "period_ph": "Periode (T): - s",
                "freq_ph": "Frekuensi (f): - Hz",
                "graph_sim_title": "Visualisasi Bandul",
                "tab2_obs_table": "TABEL PENGAMATAN",
                "box_add_data": "Tambah Data",
                "lbl_entry_L": "Panjang Tali (L) [m]:",
                "lbl_entry_T": "Periode (T) [s]:",
                "btn_save_entry": "Simpan Data",
                "col_L": "L (m)",
                "col_T": "T (s)",
                "col_T2": "T² (s²)",
                "btn_clear_all": "Hapus Semua Data",
                "btn_save_db": "☁️ Simpan Database (Unified)",
                "res_g_title": "Hasil Perhitungan Gravitasi (g): -",
                "res_g_val": "Gravitasi (g) = {:.3f} m/s²",
                "graph_ana_title": "Grafik T² vs Panjang Tali (L)",
                "axis_L": "Panjang Tali L (m)",
                "axis_T2": "Kuadrat Periode T² (s²)",
                "legend_data": "Data Percobaan",
                "legend_fit": "Fit: y={:.2f}x + {:.2f}",
                "msg_success": "Sukses",
                "msg_data_recorded": "Data L={:.2f}m, T={:.3f}s berhasil dicatat!",
                "msg_saved": "Status Penyimpanan",
                "msg_input_error": "Input harus angka!",
                "msg_error": "Error"
            },
            "EN": {
                "tab1_title": "1. Simple Harmonic Motion Simulation",
                "tab2_title": "2. Data Analysis & Graph (T² vs L)",
                "param_sys": "SYSTEM PARAMETERS",
                "len_str": "String Length (L) [m]:",
                "grav": "Gravity (g) [m/s²]:",
                "angle": "Initial Angle (θ) [°]:",
                "mass": "Bob Mass (m) [kg]:",
                "btn_start": "▶ Start Oscillation",
                "btn_stop": "⏹ Stop / Reset",
                "btn_record_auto": "Record Data (Auto)",
                "theo_val": "Theoretical Values",
                "period": "Period (T): {:.3f} s",
                "freq": "Frequency (f): {:.3f} Hz",
                "period_ph": "Period (T): - s",
                "freq_ph": "Frequency (f): - Hz",
                "graph_sim_title": "Pendulum Visualization",
                "tab2_obs_table": "OBSERVATION TABLE",
                "box_add_data": "Add Data",
                "lbl_entry_L": "String Length (L) [m]:",
                "lbl_entry_T": "Period (T) [s]:",
                "btn_save_entry": "Add Entry",
                "col_L": "L (m)",
                "col_T": "T (s)",
                "col_T2": "T² (s²)",
                "btn_clear_all": "Clear All Data",
                "btn_save_db": "☁️ Save Database (Unified)",
                "res_g_title": "Calculated Gravity (g): -",
                "res_g_val": "Gravity (g) = {:.3f} m/s²",
                "graph_ana_title": "Graph T² vs String Length (L)",
                "axis_L": "String Length L (m)",
                "axis_T2": "Period Squared T² (s²)",
                "legend_data": "Exp Data",
                "legend_fit": "Fit: y={:.2f}x + {:.2f}",
                "msg_success": "Success",
                "msg_data_recorded": "Data L={:.2f}m, T={:.3f}s recorded!",
                "msg_saved": "Save Status",
                "msg_input_error": "Input must be numbers!",
                "msg_error": "Error"
            }
        }
        
    def T(self, key):
        return self.translations[self.lang].get(key, key)
        
    def init_vars(self):
        # Variables
        self.var_length = tk.DoubleVar(value=1.0) # meter
        self.var_gravity = tk.DoubleVar(value=9.8) # m/s^2
        self.var_mass = tk.DoubleVar(value=0.5) # kg
        self.var_angle = tk.DoubleVar(value=10.0) # degrees
        self.var_damping = tk.DoubleVar(value=0.0) # damping coef
        
        self.data_points = [] # List of tuples (L, T)
        self.ani = None
        
    def setup_ui(self):
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text=self.T("tab1_title"))
        self.setup_simulasi()
        
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text=self.T("tab2_title"))
        self.setup_analisis()
        
    def set_language(self, lang):
        self.lang = lang
        if self.ani and self.ani.event_source:
             self.ani.event_source.stop()
             self.ani = None
        
        self.notebook.destroy()
        self.setup_ui()
        if hasattr(self, 'data_points') and self.data_points:
            self.restore_table_view()

    def restore_table_view(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for l, t in self.data_points:
            t_sq = t**2
            self.tree.insert("", "end", values=(f"{l:.2f}", f"{t:.3f}", f"{t_sq:.3f}"))
        self.update_regression()

    def create_header(self):
        pass
    def create_footer(self):
        pass

    # =========================================
    # TAB 1: SIMULASI
    # =========================================
    def setup_simulasi(self):
        pane = tk.PanedWindow(self.tab1, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(pane, padding=10)
        pane.add(left_frame, stretch="always")
        right_frame = ttk.Frame(pane, padding=10)
        pane.add(right_frame, stretch="always")

        # --- CONTROLS ---
        ttk.Label(left_frame, text=self.T("param_sys"), font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))

        form = ttk.Frame(left_frame)
        form.pack(fill="x", pady=5)

        # Panels
        ttk.Label(form, text=self.T("len_str")).grid(row=0, column=0, sticky="w", pady=5)
        self.scale_l = tk.Scale(form, from_=0.1, to=2.5, resolution=0.1, orient="horizontal", variable=self.var_length, length=200, command=self.update_preview)
        self.scale_l.grid(row=0, column=1)

        ttk.Label(form, text=self.T("grav")).grid(row=1, column=0, sticky="w", pady=5)
        self.scale_g = tk.Scale(form, from_=1.6, to=20.0, resolution=0.1, orient="horizontal", variable=self.var_gravity, length=200, command=self.update_preview)
        self.scale_g.grid(row=1, column=1)

        ttk.Label(form, text=self.T("angle")).grid(row=2, column=0, sticky="w", pady=5)
        self.scale_theta = tk.Scale(form, from_=5, to=45, resolution=1, orient="horizontal", variable=self.var_angle, length=200, command=self.update_preview)
        self.scale_theta.grid(row=2, column=1)

        ttk.Label(form, text=self.T("mass")).grid(row=3, column=0, sticky="w", pady=5)
        self.scale_m = tk.Scale(form, from_=0.1, to=5.0, resolution=0.1, orient="horizontal", variable=self.var_mass, length=200)
        self.scale_m.grid(row=3, column=1)

        # Buttons
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill="x", pady=20)
        ttk.Button(btn_frame, text=self.T("btn_start"), command=self.run_animation).pack(side="left", padx=5)
        ttk.Button(btn_frame, text=self.T("btn_stop"), command=self.stop_animation).pack(side="left", padx=5)
        
        ttk.Button(btn_frame, text=self.T("btn_record_auto"), command=self.record_current_sim_data).pack(side="left", padx=5)

        # Info Box
        self.info_frame = ttk.LabelFrame(left_frame, text=self.T("theo_val"))
        self.info_frame.pack(fill="x", pady=10)
        
        self.lbl_T = ttk.Label(self.info_frame, text=self.T("period_ph"))
        self.lbl_T.pack(anchor="w", padx=10)
        self.lbl_f = ttk.Label(self.info_frame, text=self.T("freq_ph"))
        self.lbl_f.pack(anchor="w", padx=10)
        self.lbl_formula = ttk.Label(self.info_frame, text="T = 2π√(L/g)", font=("Arial", 10, "italic"))
        self.lbl_formula.pack(anchor="w", padx=10, pady=5)

        # --- VISUALIZATION ---
        self.fig_sim = Figure(figsize=(5, 5), dpi=100)
        self.ax_sim = self.fig_sim.add_subplot(111)
        self.ax_sim.set_aspect('equal')
        self.canvas_sim = FigureCanvasTkAgg(self.fig_sim, master=right_frame)
        self.canvas_sim.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.ani = None
        self.update_preview()

    def calculate_period(self):
        L = self.var_length.get()
        g = self.var_gravity.get()
        if g > 0:
            T = 2 * math.pi * math.sqrt(L/g)
            f = 1/T
            self.lbl_T.config(text=self.T("period").format(T))
            self.lbl_f.config(text=self.T("freq").format(f))
            return T
        return 0

    def draw_pendulum(self, theta, L):
        self.ax_sim.clear()
        
        self.ax_sim.add_patch(patches.Rectangle((-1, 0), 2, 0.1, color="#7f8c8d"))
        
        x = L * math.sin(theta)
        y = -L * math.cos(theta)

        self.ax_sim.plot([0, x], [0, y], 'k-', lw=2)
        
        bob_radius = 0.1 + (self.var_mass.get() * 0.02)
        bob = patches.Circle((x, y), bob_radius, facecolor="#e74c3c", edgecolor="black")
        self.ax_sim.add_patch(bob)
        
        self.ax_sim.plot([0, 0], [0, -L-0.5], 'b--', alpha=0.3)
        
        if self.ani is None:
             arc = patches.Arc((0,0), L, L, angle=-90, theta1=0, theta2=math.degrees(theta), color='green')
             self.ax_sim.add_patch(arc)

        self.ax_sim.set_xlim(-2, 2)
        self.ax_sim.set_ylim(-3, 0.5)
        self.ax_sim.set_title(self.T("graph_sim_title"))
        self.ax_sim.grid(False)
        self.canvas_sim.draw()

    def update_preview(self, event=None):
        if self.ani is None:
            L = self.var_length.get()
            theta_deg = self.var_angle.get()
            self.calculate_period()
            self.draw_pendulum(math.radians(theta_deg), L)

    def run_animation(self):
        if self.ani is not None:
            self.stop_animation()

        L = self.var_length.get()
        g = self.var_gravity.get()
        theta0 = math.radians(self.var_angle.get())
        omega = math.sqrt(g/L)
        
        self.calculate_period()

        start_time = 0
        dt = 0.05
        
        def update(frame):
            t = frame * dt
            theta_t = theta0 * math.cos(omega * t)
            self.draw_pendulum(theta_t, L)
            self.ax_sim.set_title(f"t = {t:.2f} s")

        self.ani = FuncAnimation(self.fig_sim, update, interval=50, frames=200) 
        self.canvas_sim.draw()

    def stop_animation(self):
        if self.ani is not None:
            self.ani.event_source.stop()
            self.ani = None
        self.update_preview()

    def record_current_sim_data(self):
        L = self.var_length.get()
        T = self.calculate_period()
        
        self.notebook.select(self.tab2)
        
        t_sq = T**2
        self.data_points.append((L, T))
        self.tree.insert("", "end", values=(f"{L:.2f}", f"{T:.3f}", f"{t_sq:.3f}"))
        
        self.update_regression()
        messagebox.showinfo(self.T("msg_success"), self.T("msg_data_recorded").format(L, T), parent=self.parent)

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

        # --- INPUT ---
        ttk.Label(left_frame, text=self.T("tab2_obs_table"), font=("Arial", 12, "bold")).pack(anchor="w", pady=10)
        
        input_box = ttk.LabelFrame(left_frame, text=self.T("box_add_data"))
        input_box.pack(fill="x", pady=5)
        
        ttk.Label(input_box, text=self.T("lbl_entry_L")).grid(row=0, column=0, padx=5, pady=2)
        self.entry_L = ttk.Entry(input_box, width=10)
        self.entry_L.grid(row=0, column=1)
        
        ttk.Label(input_box, text=self.T("lbl_entry_T")).grid(row=1, column=0, padx=5, pady=2)
        self.entry_T = ttk.Entry(input_box, width=10)
        self.entry_T.grid(row=1, column=1)
        
        btn_add = ttk.Button(input_box, text=self.T("btn_save_entry"), command=self.add_data)
        btn_add.grid(row=2, column=0, columnspan=2, pady=5)

        # Treeview
        cols = ("col1", "col2", "col3")
        self.tree = ttk.Treeview(left_frame, columns=cols, show="headings", height=10)
        self.tree.heading("col1", text=self.T("col_L"))
        self.tree.heading("col2", text=self.T("col_T"))
        self.tree.heading("col3", text=self.T("col_T2"))
        
        self.tree.column("col1", width=80, anchor="center")
        self.tree.column("col2", width=80, anchor="center")
        self.tree.column("col3", width=80, anchor="center")
        
        self.tree.pack(fill="both", expand=True, pady=10)
        
        btn_action_frame = ttk.Frame(left_frame)
        btn_action_frame.pack(fill="x", pady=5)

        ttk.Button(btn_action_frame, text=self.T("btn_clear_all"), command=self.clear_data).pack(side="left", padx=5)
        ttk.Button(btn_action_frame, text=self.T("btn_save_db"), command=self.save_data_unified).pack(side="left", padx=5)


        # --- GRAPH & RESULT ---
        self.fig_graph = Figure(figsize=(5, 4), dpi=100)
        self.ax_graph = self.fig_graph.add_subplot(111)
        self.canvas_graph = FigureCanvasTkAgg(self.fig_graph, master=right_frame)
        self.canvas_graph.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas_graph, right_frame)
        toolbar.update()
        toolbar.pack(side="bottom", fill="x")

        self.lbl_result_g = ttk.Label(right_frame, text=self.T("res_g_title"), 
                                      font=("Arial", 12, "bold"), foreground="#2980b9")
        self.lbl_result_g.pack(pady=10)

    def get_data(self):
        export_data = []
        for l, t in self.data_points:
            t_sq = t**2
            g_calc = (4 * (math.pi**2) * l) / t_sq if t_sq != 0 else 0
            
            export_data.append({
                "Modul": "Bandul Matematis",
                "Panjang Tali L (m)": float(l),
                "Periode T (s)": float(t),
                "T Kuadrat (s^2)": float(t_sq),
                "Gravitasi Terhitung (m/s^2)": float(g_calc)
            })
        return export_data

    def save_data_unified(self):
        data = self.get_data()
        success, msg = DataManager.save_data_unified(data, "BandulMatematis")
        if success:
            messagebox.showinfo(self.T("msg_saved"), msg, parent=self.parent)
        else:
            messagebox.showwarning(self.T("msg_saved"), msg, parent=self.parent)

    def add_data(self):
        try:
            l = float(self.entry_L.get())
            t = float(self.entry_T.get())
            t_sq = t**2
            
            self.data_points.append((l, t))
            self.tree.insert("", "end", values=(f"{l:.2f}", f"{t:.3f}", f"{t_sq:.3f}"))
            
            self.entry_L.delete(0, tk.END)
            self.entry_T.delete(0, tk.END)
            
            self.update_regression()
        except ValueError:
            messagebox.showerror(self.T("msg_error"), self.T("msg_input_error"))

    def clear_data(self):
        self.data_points = []
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.ax_graph.clear()
        self.canvas_graph.draw()
        self.lbl_result_g.config(text=self.T("res_g_title"))

    def update_regression(self):
        if len(self.data_points) < 2:
            return

        L_vals = np.array([p[0] for p in self.data_points])
        T_vals = np.array([p[1] for p in self.data_points])
        T2_vals = T_vals ** 2

        coef = np.polyfit(L_vals, T2_vals, 1)
        gradien = coef[0]
        intercept = coef[1]
        
        g_calc = (4 * (math.pi**2)) / gradien
        
        self.ax_graph.clear()
        self.ax_graph.scatter(L_vals, T2_vals, color='red', label=self.T("legend_data"))
        
        x_line = np.linspace(0, max(L_vals)*1.1, 50)
        y_line = gradien * x_line + intercept
        self.ax_graph.plot(x_line, y_line, 'b--', label=self.T("legend_fit").format(gradien, intercept))
        
        self.ax_graph.set_title(self.T("graph_ana_title"))
        self.ax_graph.set_xlabel(self.T("axis_L"))
        self.ax_graph.set_ylabel(self.T("axis_T2"))
        self.ax_graph.legend()
        self.ax_graph.grid(True)
        self.canvas_graph.draw()
        
        self.lbl_result_g.config(text=self.T("res_g_val").format(g_calc))

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabBandul(root)
    root.mainloop()
