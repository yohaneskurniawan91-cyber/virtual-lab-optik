import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class VirtualLabPegas:
    def __init__(self, parent):
        self.parent = parent
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="1. Simulasi Pegas")
        self.setup_simulasi()
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="2. Analisis Data Pegas")
        self.setup_analisis()
        # ...lanjutkan inisialisasi lain, tanpa header/footer window dan tanpa set title/geometry...

    def create_header(self):
        header_frame = tk.Frame(self.root, bg="#2c3e50", pady=15)
        header_frame.pack(side="top", fill="x")
        tk.Label(header_frame, text="VIRTUAL LAB: KONSTANTA PEGAS (HUKUM HOOKE)", font=("Arial", 22, "bold"), fg="white", bg="#2c3e50").pack()
        tk.Label(header_frame, text="Simulasi & Analisis Interaktif Percobaan Pegas", font=("Arial", 14), fg="#bdc3c7", bg="#2c3e50").pack()
        tk.Label(header_frame, text="Pengembang: Yohanes Kurniawan", font=("Arial", 13, "bold"), fg="white", bg="#2c3e50").pack(pady=(5, 0))

    def create_footer(self):
        footer_frame = tk.Frame(self.root, bg="#2c3e50", pady=8)
        footer_frame.pack(side="bottom", fill="x")
        tk.Label(footer_frame, text="VERSI APLIKASI PRO", font=("Arial", 10, "bold"), fg="#e74c3c", bg="#2c3e50").pack(side="left", padx=20)
        tk.Label(footer_frame, text="Modul Fisika Dasar: Elastisitas & Pegas", font=("Arial", 10), fg="#bdc3c7", bg="#2c3e50").pack(side="right", padx=20)

    def setup_simulasi(self):
        pane = tk.PanedWindow(self.tab1, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)
        left_frame = ttk.Frame(pane, padding=10)
        pane.add(left_frame, stretch="always")
        right_frame = ttk.Frame(pane, padding=10)
        pane.add(right_frame, stretch="always")
        ttk.Label(left_frame, text="PARAMETER SIMULASI", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))
        self.var_m = tk.DoubleVar(value=0.2)
        self.var_l0 = tk.DoubleVar(value=0.10)
        self.var_g = tk.DoubleVar(value=9.8)
        form = ttk.Frame(left_frame)
        form.pack(fill="x", pady=5)
        ttk.Label(form, text="Massa Beban (kg):").grid(row=0, column=0, sticky="w", pady=5)
        self.scale_m = tk.Scale(form, from_=0.05, to=1.0, resolution=0.01, orient="horizontal", variable=self.var_m, length=200, command=self.update_simulasi)
        self.scale_m.grid(row=0, column=1)
        ttk.Label(form, text="Panjang Pegas Awal (m):").grid(row=1, column=0, sticky="w", pady=5)
        self.scale_l0 = tk.Scale(form, from_=0.05, to=0.20, resolution=0.005, orient="horizontal", variable=self.var_l0, length=200, command=self.update_simulasi)
        self.scale_l0.grid(row=1, column=1)
        ttk.Label(form, text="Gravitasi (g) [m/s²]:").grid(row=2, column=0, sticky="w", pady=5)
        self.scale_g = tk.Scale(form, from_=8.0, to=10.0, resolution=0.01, orient="horizontal", variable=self.var_g, length=200, command=self.update_simulasi)
        self.scale_g.grid(row=2, column=1)
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill="x", pady=10)
        ttk.Button(btn_frame, text="Reset", command=self.reset_simulasi).pack(side="left", padx=5)
        self.lbl_f = ttk.Label(left_frame, text="Gaya Berat (F): - N")
        self.lbl_f.pack(anchor="w", padx=10, pady=5)
        self.lbl_l = ttk.Label(left_frame, text="Panjang Pegas Akhir (L): - m")
        self.lbl_l.pack(anchor="w", padx=10, pady=5)
        self.lbl_x = ttk.Label(left_frame, text="Pertambahan Panjang (Δx): - m")
        self.lbl_x.pack(anchor="w", padx=10, pady=5)
        self.lbl_k = ttk.Label(left_frame, text="Konstanta Pegas (k): - N/m")
        self.lbl_k.pack(anchor="w", padx=10, pady=5)
        self.fig_sim = Figure(figsize=(4, 6), dpi=100)
        self.ax_sim = self.fig_sim.add_subplot(111)
        self.canvas_sim = FigureCanvasTkAgg(self.fig_sim, master=right_frame)
        self.canvas_sim.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.update_simulasi()

    def reset_simulasi(self):
        self.var_m.set(0.2)
        self.var_l0.set(0.10)
        self.var_g.set(9.8)
        self.update_simulasi()

    def update_simulasi(self, event=None):
        m = self.var_m.get()
        l0 = self.var_l0.get()
        g = self.var_g.get()
        F = m * g
        k = 20.0 # default k (N/m)
        dx = F / k
        L = l0 + dx
        self.lbl_f.config(text=f"Gaya Berat (F): {F:.3f} N")
        self.lbl_l.config(text=f"Panjang Pegas Akhir (L): {L:.3f} m")
        self.lbl_x.config(text=f"Pertambahan Panjang (Δx): {dx:.3f} m")
        self.lbl_k.config(text=f"Konstanta Pegas (k): {k:.2f} N/m (default)")
        self.draw_pegas(l0, L)

    def draw_pegas(self, l0, L):
        self.ax_sim.clear()
        # Pegas realistik: spiral dinamis, efek 3D, bayangan, beban bulat
        n_coil = 16
        y_top = 0.92
        y_bot = 0.92 - L
        y_pegas = np.linspace(y_top, y_bot, n_coil*30)
        amp = 0.07 + 0.03 * np.sin(np.linspace(0, np.pi, n_coil*30)) # efek diameter spiral
        x_pegas = amp * np.sin(2 * np.pi * n_coil * (y_pegas - y_bot) / (y_top - y_bot))
        # Efek 3D: bayangan spiral
        self.ax_sim.plot(x_pegas-0.01, y_pegas-0.01, color='#888', lw=2, alpha=0.18, zorder=1)
        # Spiral utama
        self.ax_sim.plot(x_pegas, y_pegas, color='#2980b9', lw=3, zorder=2)
        # Gantungan atas
        self.ax_sim.plot([0, 0], [y_top+0.04, y_top], color='#555', lw=5, zorder=3)
        self.ax_sim.add_patch(plt.Circle((0, y_top+0.04), 0.025, color='#888', zorder=3))
        # Beban bulat dengan efek bayangan
        y_beban = y_bot - 0.07
        self.ax_sim.add_patch(plt.Circle((0, y_beban-0.01), 0.055, color='#222', alpha=0.18, zorder=1))
        self.ax_sim.add_patch(plt.Circle((0, y_beban), 0.055, color='#34495e', zorder=4))
        self.ax_sim.text(0, y_beban-0.08, f"m = {self.var_m.get():.2f} kg", ha='center', fontsize=10, color='black', zorder=5)
        # Label panjang
        self.ax_sim.annotate(f"L = {L:.3f} m", xy=(0.11, (y_top+y_bot)/2), xytext=(0.13, (y_top+y_bot)/2),
            arrowprops=dict(arrowstyle="->", color='#e67e22'), color='#e67e22', fontsize=10, va='center')
        self.ax_sim.set_xlim(-0.18, 0.18)
        self.ax_sim.set_ylim(0, 1)
        self.ax_sim.axis('off')
        self.ax_sim.set_title("Visualisasi Pegas & Beban (Realistik)")
        self.canvas_sim.draw()

    def setup_analisis(self):
        pane = tk.PanedWindow(self.tab2, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)
        left_frame = ttk.Frame(pane, padding=10)
        pane.add(left_frame, stretch="always")
        right_frame = ttk.Frame(pane, padding=10)
        pane.add(right_frame, stretch="always")
        ttk.Label(left_frame, text="INPUT DATA PENGAMATAN", font=("Arial", 12, "bold")).pack(anchor="w", pady=10)
        input_box = ttk.LabelFrame(left_frame, text="Input Data")
        input_box.pack(fill="x", pady=5)
        ttk.Label(input_box, text="Massa Beban (kg):").grid(row=0, column=0, padx=5, pady=5)
        self.entry_m = ttk.Entry(input_box, width=10)
        self.entry_m.grid(row=0, column=1)
        ttk.Label(input_box, text="Panjang Pegas (L) [m]:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_L = ttk.Entry(input_box, width=10)
        self.entry_L.grid(row=1, column=1)
        ttk.Button(input_box, text="Tambah Data", command=self.add_data_point).grid(row=2, column=0, columnspan=2, pady=10, sticky='ew')
        cols = ("m (kg)", "L (m)", "F (N)", "Δx (m)")
        self.tree = ttk.Treeview(left_frame, columns=cols, show="headings", height=12)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=80, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=10)
        ttk.Button(left_frame, text="Hapus Semua Data", command=self.clear_data).pack(fill='x')
        self.fig_graph = Figure(figsize=(5, 4), dpi=100)
        self.ax_graph = self.fig_graph.add_subplot(111)
        self.canvas_graph = FigureCanvasTkAgg(self.fig_graph, master=right_frame)
        self.canvas_graph.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.lbl_result_k = ttk.Label(right_frame, text="Konstanta Pegas (k): - N/m", font=("Arial", 14, "bold"), foreground="#2980b9")
        self.lbl_result_k.pack(pady=10)
        self.data_points = []
        self.l0_ref = 0.10

    def add_data_point(self):
        try:
            m = float(self.entry_m.get().replace(',', '.'))
            L = float(self.entry_L.get().replace(',', '.'))
            g = 9.8
            F = m * g
            dx = L - self.l0_ref
            self.data_points.append({'m': m, 'L': L, 'F': F, 'dx': dx})
            self.tree.insert("", "end", values=(f"{m:.2f}", f"{L:.3f}", f"{F:.2f}", f"{dx:.3f}"))
            self.update_graph()
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid")

    def clear_data(self):
        self.data_points = []
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.ax_graph.clear()
        self.canvas_graph.draw()
        self.lbl_result_k.config(text="Konstanta Pegas (k): - N/m")

    def update_graph(self):
        if len(self.data_points) < 2:
            return
        dxs = np.array([d['dx'] for d in self.data_points])
        Fs = np.array([d['F'] for d in self.data_points])
        coef = np.polyfit(dxs, Fs, 1)
        slope = coef[0]
        self.ax_graph.clear()
        self.ax_graph.scatter(dxs, Fs, color='blue', label='Data')
        x_line = np.linspace(min(dxs), max(dxs), 50)
        y_line = coef[0]*x_line + coef[1]
        self.ax_graph.plot(x_line, y_line, 'r--', label=f'Fit Slope = {slope:.2f}')
        self.ax_graph.set_title(f"Hubungan F vs Δx (k = {slope:.2f} N/m)")
        self.ax_graph.set_xlabel("Pertambahan Panjang Δx (m)")
        self.ax_graph.set_ylabel("Gaya F (N)")
        self.ax_graph.legend()
        self.ax_graph.grid(True)
        self.canvas_graph.draw()
        self.lbl_result_k.config(text=f"Konstanta Pegas (k): {slope:.2f} N/m")

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabPegas(root)
    root.mainloop()