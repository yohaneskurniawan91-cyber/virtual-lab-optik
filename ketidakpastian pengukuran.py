import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import statistics
import math
import random

class VirtualLabKetidakpastian:
    def __init__(self, parent):
        self.parent = parent
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        # Notebook (Tabs)
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Tab 1: Pengukuran Tunggal (Mistar/Jangka Sorong/Mikrometer)
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="1. Simulasi Alat Ukur")
        self.setup_tab1()

        # Tab 2: Pengukuran Berulang
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="2. Pengukuran Berulang")
        self.setup_tab2()
        
        # Tab 3: Perambatan Kesalahan
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="3. Perambatan Kesalahan")
        self.setup_tab3()

    # ===========================
    # TAB 1: PENGUKURAN TUNGGAL & SIMULASI ALAT
    # ===========================
    def setup_tab1(self):
        # Layout: Kiri (Kontrol), Kanan (Visualisasi)
        pane = tk.PanedWindow(self.tab1, orient=tk.HORIZONTAL)
        pane.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(pane, width=300, relief=tk.SUNKEN)
        self.right_frame = ttk.Frame(pane, relief=tk.SUNKEN)
        pane.add(left_frame)
        pane.add(self.right_frame)

        # --- Bagian Kontrol (Kiri) ---
        tk.Label(left_frame, text="PENGATURAN PENGUKURAN", font=("Arial", 12, "bold")).pack(pady=10)
        
        # 1. Pilih Alat
        ttk.Label(left_frame, text="Pilih Alat Ukur:").pack(anchor="w", padx=10)
        self.alat_var = tk.StringVar(value="Mistar")
        alat_combo = ttk.Combobox(left_frame, textvariable=self.alat_var, 
                                values=["Mistar", "Jangka Sorong", "Mikrometer Sekrup"])
        alat_combo.pack(fill="x", padx=10, pady=(0, 10))
        alat_combo.bind("<<ComboboxSelected>>", self.update_simulasi_ui)

        # 2. Pilih Benda
        ttk.Label(left_frame, text="Pilih Objek:").pack(anchor="w", padx=10)
        self.benda_var = tk.StringVar(value="Balok Kayu")
        benda_combo = ttk.Combobox(left_frame, textvariable=self.benda_var, 
                                 values=["Balok Kayu (Panjang)", "Apel Malang (Diameter)", "Kelereng (Diameter)", "Koin (Tebal)"])
        benda_combo.pack(fill="x", padx=10, pady=(0, 10))
        benda_combo.bind("<<ComboboxSelected>>", self.update_object_value)

        # 3. Slider Nilai (Simulasi Pengukuran)
        ttk.Label(left_frame, text="Geser untuk Mengukur (Nilai Sebenarnya):").pack(anchor="w", padx=10)
        self.slider_val = tk.DoubleVar(value=5.0)
        self.scale_slider = ttk.Scale(left_frame, from_=0, to=20, variable=self.slider_val, command=self.on_slider_change)
        self.scale_slider.pack(fill="x", padx=10, pady=(0, 5))
        
        self.label_reading = ttk.Label(left_frame, text="Posisi: 5.00 cm", font=("Consolas", 10))
        self.label_reading.pack(anchor="e", padx=10)

        # Informasi Alat
        self.info_text = tk.Text(left_frame, height=8, bg="#ecf0f1", wrap=tk.WORD)
        self.info_text.pack(fill="x", padx=10, pady=10)
        self.info_text.insert(tk.END, "Info alat akan muncul di sini.")

        # Tombol Hitung

        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Hitung Ketidakpastian", command=self.calculate_uncertainty).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="Reset", command=self.reset_tab1).pack(side="left")

        # Hasil Perhitungan
        self.result_text1 = tk.Text(left_frame, height=10, bg="#ecf0f1")
        self.result_text1.pack(fill="both", expand=True, padx=10, pady=5)

        # --- Bagian Visualisasi (Kanan) ---
        self.fig_sim = Figure(figsize=(7, 6), dpi=100)
        self.ax_sim = self.fig_sim.add_subplot(111)
        self.canvas_sim = FigureCanvasTkAgg(self.fig_sim, master=self.right_frame)
        self.canvas_sim.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # Inisialisasi awal
        self.update_simulasi_ui()
    def reset_tab1(self):
        self.alat_var.set("Mistar")
        self.benda_var.set("Balok Kayu (Panjang)")
        self.slider_val.set(5.0)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, "Info alat akan muncul di sini.")
        self.result_text1.delete(1.0, tk.END)
        self.update_simulasi_ui()

    def update_simulasi_ui(self, event=None):
        alat = self.alat_var.get()
        
        if alat == "Mistar":
            self.scale_slider.config(from_=0, to=30)
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, "Mistar (Penggaris)\nNST: 0.1 cm\nKetidakpastian: 0.05 cm\nCocok untuk: Panjang balok, tali, buku.")
        elif alat == "Jangka Sorong":
            self.scale_slider.config(from_=0, to=15)
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, "Jangka Sorong (Vernier Caliper)\nNST: 0.01 cm (Umum)\nKetidakpastian: 0.005 cm\nCocok untuk: Diameter apel, kelereng, diameter dalam pipa.")
        elif alat == "Mikrometer Sekrup":
            self.scale_slider.config(from_=0, to=25) # mm
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, "Mikrometer Sekrup\nNST: 0.01 mm\nKetidakpastian: 0.005 mm\nCocok untuk: Tebal koin, kertas, kawat halus.\n(Satuan otomatis berubah ke mm)")

        self.update_object_value() # Reset value based on object logic
        self.draw_simulation()

    def update_object_value(self, event=None):
        obj = self.benda_var.get()
        alat = self.alat_var.get()
        
        # Logika "Random" Ukuran Benda (Simulasi variasi alami)
        base_val = 5.0
        if "Balok" in obj: base_val = 12.5 # cm
        elif "Apel" in obj: base_val = random.uniform(6.5, 8.5) # cm
        elif "Kelereng" in obj: base_val = 1.55 # cm
        elif "Koin" in obj: base_val = 2.3 # mm/cm tergantung alat later
        
        # Konversi jika Mikrometer (karena mm)
        if alat == "Mikrometer Sekrup":
            if "Balok" in obj or "Apel" in obj:
                messagebox.showinfo("Info", "Objek terlalu besar untuk Mikrometer Sekrup! Mengganti ke Koin.")
                self.benda_var.set("Koin (Tebal)")
                base_val = 2.35 # mm
            elif "Kelereng" in obj:
                base_val = 15.5 # mm
            elif "Koin" in obj:
                base_val = 2.35 # mm
        else:
             # Mistar/Jangka Sorong (cm)
             if "Koin" in obj: base_val = 0.235 # cm

        self.slider_val.set(base_val)
        self.on_slider_change()

    def on_slider_change(self, event=None):
        val = self.slider_val.get()
        unit = "mm" if self.alat_var.get() == "Mikrometer Sekrup" else "cm"
        self.label_reading.config(text=f"Posisi: {val:.3f} {unit}")
        self.draw_simulation()

    def calculate_uncertainty(self):
        val = self.slider_val.get()
        alat = self.alat_var.get()
        
        nst = 0.1
        unit = "cm"
        
        if alat == "Mistar":
            nst = 0.1
        elif alat == "Jangka Sorong":
            nst = 0.01
        elif alat == "Mikrometer Sekrup":
            nst = 0.01
            unit = "mm"

        uncertainty = 0.5 * nst
        rel_error = (uncertainty / val) * 100 if val > 0 else 0
        ketelitian = 100 - rel_error

        res = f"--- HASIL PENGUKURAN ---\n"
        res += f"Alat: {alat}\n"
        res += f"Objek: {self.benda_var.get()}\n"
        res += f"Nilai Terbaca (x): {val:.3f} {unit}\n"
        res += f"NST Alat: {nst} {unit}\n"
        res += f"Ketidakpastian (Δx): {uncertainty} {unit}\n"
        res += f"Pelaporan: ({val:.3f} ± {uncertainty}) {unit}\n"
        res += f"Ketelitian: {ketelitian:.2f}%"
        
        self.result_text1.delete(1.0, tk.END)
        self.result_text1.insert(tk.END, res)

    def draw_simulation(self):
        self.ax_sim.clear()
        alat = self.alat_var.get()
        val = self.slider_val.get()
        
        self.ax_sim.set_axis_off()
        # Background Grid halus untuk kesan teknis
        self.ax_sim.grid(True, linestyle=':', alpha=0.3)
        
        if alat == "Mistar":
            self.draw_mistar(val)
        elif alat == "Jangka Sorong":
            self.draw_jangka_sorong(val)
        elif alat == "Mikrometer Sekrup":
            self.draw_mikrometer(val)

        # Gambar Label Objek dengan style badge
        self.ax_sim.text(0.5, 0.05, f"Benda: {self.benda_var.get()}", 
                         transform=self.ax_sim.transAxes, ha='center', fontsize=10, 
                         color='white', weight='bold',
                         bbox=dict(boxstyle="round,pad=0.4", fc='#2c3e50', ec='#34495e', alpha=0.9))
        self.canvas_sim.draw()

    def draw_mistar(self, val):
        # Setup view: Lebih luas sedikit
        self.ax_sim.set_xlim(-2, val + 5)
        self.ax_sim.set_ylim(-1.5, 3.5)
        self.ax_sim.set_title(f"Mistar (Penggaris) - Bacaan: {val:.2f} cm", fontsize=12, pad=10)
        
        # 1. Gambar Benda (Object) dengan gradien simulasi (fill)
        # Kita pakai solid color dulu tapi stroke jelas
        rect = plt.Rectangle((0, 0), val, 1.2, facecolor='#3498db', edgecolor='#2980b9', linewidth=2, alpha=0.9, label='Benda')
        self.ax_sim.add_patch(rect)
        self.ax_sim.text(val/2, 0.6, "Benda Uji", color='white', ha='center', va='center', weight='bold')

        # 2. Gambar Body Mistar (Kuning Kayu / Plastik)
        # Posisi mistar sedikit di atas benda
        ruler_y_bottom = 1.3
        ruler_height = 1.2
        ruler_bg = plt.Rectangle((-1, ruler_y_bottom), val + 6, ruler_height, facecolor='#f1c40f', edgecolor='#f39c12', linewidth=2)
        self.ax_sim.add_patch(ruler_bg)

        # 3. Ticks & Angka
        # Garis batas nol mistar
        zero_x = 0
        
        limit_ruler = int(val) + 5
        for i in range(-1, limit_ruler):
            # Garis Utama (cm)
            x_line = i
            if x_line >= -1: 
                # CM Mark
                self.ax_sim.plot([x_line, x_line], [ruler_y_bottom, ruler_y_bottom + 0.6], color='black', linewidth=1.2)
                self.ax_sim.text(x_line, ruler_y_bottom + 0.8, str(i), ha='center', fontsize=9, color='black')
                
                # MM Marks
                for j in range(1, 10):
                    mm_x = x_line + j/10.0
                    if j == 5:
                        # Setengah cm
                        self.ax_sim.plot([mm_x, mm_x], [ruler_y_bottom, ruler_y_bottom + 0.4], color='black', linewidth=0.8)
                    else:
                        # mm biasa
                        self.ax_sim.plot([mm_x, mm_x], [ruler_y_bottom, ruler_y_bottom + 0.25], color='black', linewidth=0.5)

        # 4. Indikator Pembacaan (Garis Putus-putus Merah) yang lebih cantik
        self.ax_sim.axvline(x=val, ymin=0, ymax=1, color='#e74c3c', linestyle='--', linewidth=2, alpha=0.8)
        
        # Arrow pointer
        self.ax_sim.annotate(f"{val:.2f} cm", xy=(val, ruler_y_bottom), xytext=(val, ruler_y_bottom + 1.5),
                             arrowprops=dict(facecolor='#e74c3c', shrink=0.05),
                             bbox=dict(boxstyle="round", fc='#ecf0f1', ec='#e74c3c'),
                             ha='center', color='#c0392b', weight='bold')

    def draw_jangka_sorong(self, val):
        # View Setup
        self.ax_sim.set_xlim(val - 3, val + 8)
        self.ax_sim.set_ylim(-3.5, 3.5)
        self.ax_sim.set_title(f"Jangka Sorong (Vernier Caliper) - Bacaan: {val:.3f} cm", fontsize=12, pad=10)

        # Warna Metalik
        color_fixed = '#bdc3c7'
        color_slide = '#95a5a6'
        color_stroke = '#7f8c8d'

        # --- 1. BENDA (Object) ---
        radius = val / 2
        # Gambar Benda di antara rahang bawah (posisi y < 0)
        # Rahang bawah menyentuh di x=0 dan x=val
        # Pusat benda di x=val/2.
        
        if "Apel" in self.benda_var.get():
             circle = plt.Circle((val/2, -1.0), radius, facecolor='#e74c3c', edgecolor='#c0392b', alpha=0.9)
             self.ax_sim.add_patch(circle)
             self.ax_sim.text(val/2, -1.0, "Benda", color='white', fontsize=8, ha='center', va='center')
        else:
             # Default Box agar pas dijepit rahang
             rect_benda = plt.Rectangle((0, -2.0), val, 2.0, facecolor='#3498db', edgecolor='#2980b9', alpha=0.8)
             self.ax_sim.add_patch(rect_benda)
             self.ax_sim.text(val/2, -1.0, "Benda", color='white', fontsize=8, ha='center', va='center')

        # --- 2. MAIN SCALE (FIXED PART) ---
        # Batang Utama (Horizontal)
        main_bar = plt.Rectangle((-2, 0), 25, 1.5, facecolor=color_fixed, edgecolor=color_stroke, linewidth=1)
        self.ax_sim.add_patch(main_bar)
        
        # Rahang Tetap Bawah (Fixed Jaw) - x=0
        jaw_fixed_poly = plt.Polygon([[0, 0], [0, -2.5], [-0.5, -2.5], [-0.5, 1.5]], closed=True, facecolor=color_fixed, edgecolor=color_stroke)
        self.ax_sim.add_patch(jaw_fixed_poly)
        
        # Rahang Tetap Atas (Inner Jaw) - x=0
        jaw_fixed_upper = plt.Polygon([[0, 1.5], [0, 2.5], [-0.5, 2.5], [-0.5, 1.5]], closed=True, facecolor=color_fixed, edgecolor=color_stroke)
        self.ax_sim.add_patch(jaw_fixed_upper)

        # Ticks Main Scale (cm dan mm) di bagian bawah batang utama
        start_tick = -1
        end_tick = int(val) + 10
        for i in range(start_tick, end_tick):
            x_cm = i
            # CM Mark
            self.ax_sim.plot([x_cm, x_cm], [0, 0.5], color='black', linewidth=1)
            self.ax_sim.text(x_cm, 0.6, str(i), fontsize=8, ha='center')
            
            # MM Marks
            for j in range(1, 10):
                x_mm = x_cm + j/10.0
                h_mm = 0.3 if j == 5 else 0.2
                self.ax_sim.plot([x_mm, x_mm], [0, h_mm], color='black', linewidth=0.5)

        # --- 3. VERNIER SCALE (SLIDING PART) ---
        # Bergerak sesuai `val`
        # Body Vernier
        vernier_x = val
        vernier_width = 3.5 # Cukup untuk 10 skala (0.9 cm x something)
        vernier_body = plt.Rectangle((vernier_x, -0.8), vernier_width, 2.3, facecolor=color_slide, edgecolor=color_stroke, alpha=0.9)
        self.ax_sim.add_patch(vernier_body)
        
        # Rahang Geser Bawah
        jaw_slide_poly = plt.Polygon([[vernier_x, 0], [vernier_x, -2.5], [vernier_x+0.5, -2.5], [vernier_x+0.5, 0]], closed=True, facecolor=color_slide, edgecolor=color_stroke)
        self.ax_sim.add_patch(jaw_slide_poly)
        
        # Rahang Geser Atas
        jaw_slide_upper = plt.Polygon([[vernier_x, 1.5], [vernier_x, 2.5], [vernier_x+0.5, 2.5], [vernier_x+0.5, 1.5]], closed=True, facecolor=color_slide, edgecolor=color_stroke)
        self.ax_sim.add_patch(jaw_slide_upper)
        
        # Ticks Vernier Scale
        # Prinsip: 10 skala nonius = 0.9 cm skala utama (umumnya 0.05mm or 0.1mm caliper)
        # Kita pakai n=10, ketelitian 0.1 mm -> jarak antar tick = 0.9 mm
        
        vernier_spacing = 0.09
        y_vernier_base = 0 # Nempel sama main scale ticks
        
        self.ax_sim.text(vernier_x + 1.5, 1.0, "Vernier Scale", fontsize=7, color='white', style='italic')

        for i in range(11):
            vx = vernier_x + (i * vernier_spacing)
            # Garis tick nonius (dari bawah ke atas, nempel main scale)
            self.ax_sim.plot([vx, vx], [y_vernier_base, y_vernier_base - 0.4], color='black', linewidth=1)
            
            # Angka Nonius (0, 5, 10)
            if i % 5 == 0:
                self.ax_sim.text(vx, y_vernier_base - 0.6, str(i), fontsize=7, ha='center', weight='bold')
            elif i == 0 or i == 10:
                pass # Already handled by modulo

        # Highlight Arrow
        self.ax_sim.annotate(f"Nol Nonius", xy=(vernier_x, 0), xytext=(vernier_x, -1.5),
                             arrowprops=dict(arrowstyle="->", color='#c0392b'),
                             fontsize=8, color='#c0392b', ha='center')

    def draw_mikrometer(self, val_mm):
        # View Setup
        self.ax_sim.set_xlim(val_mm - 5, val_mm + 25)
        self.ax_sim.set_ylim(-5, 5)
        self.ax_sim.set_title(f"Mikrometer Sekrup - Bacaan: {val_mm:.2f} mm", fontsize=12, pad=10)

        # Warna
        color_frame = '#34495e'
        color_sleeve = '#ecf0f1'
        color_thimble = '#bdc3c7'
        color_stroke = '#7f8c8d'
        
        # --- 1. BENDA (OBJECT) ---
        rect_benda = plt.Rectangle((0, -1.0), val_mm, 2.0, facecolor='#f1c40f', edgecolor='#f39c12', alpha=0.9)
        self.ax_sim.add_patch(rect_benda)
        self.ax_sim.text(val_mm/2, 0, "Benda", ha='center', va='center', fontsize=8, weight='bold', color='black')

        # --- 2. FRAME & ANVIL (KIRI) ---
        # Anvil Block
        self.ax_sim.add_patch(plt.Rectangle((-2, -1), 2, 2, facecolor='#95a5a6', edgecolor='black'))
        
        # Frame U (Curve)
        t = np.linspace(np.pi/2, 3*np.pi/2, 50)
        frame_x = -2 + 12*np.cos(t)
        frame_y = 10*np.sin(t) - 4
        self.ax_sim.plot(frame_x, frame_y, color=color_frame, linewidth=12, solid_capstyle='round')

        # --- 3. SLEEVE (MAIN SCALE - FIXED) ---
        # Kita mulai Sleeve dari posisi referensi tetap relatif terhadap Anvil?
        # Di mikrometer, Sleeve diam. Thimble mundur.
        # Kita set offset Sleeve mulai dari X = val_mm + (gap).
        # Tapi yang benar: 
        # Anvil di 0. Spindle bergerak. Sleeve/Body Statis di kanan.
        # Jika val=0 (rapat), Spindle nutup.
        # Kita visualkan Sleeve mulai dari X = gap_visual (misal 5 mm dari benda terbesar)
        # Agar rapi, kita buat Sleeve mulai dari X = val_mm + 2. (Spindle terlihat panjang)
        
        # Posisi bibir Thimble = Sleeve Start + val_mm ?
        # Tidak. Posisi 0 Sleeve adalah referensi.
        # Misal Titik 0 Sleeve diletakkan di X = 0 (tertutup benda). Ini membingungkan visual.
        
        # Pendekatan Visual Terbaik:
        # Benda di kiri (Width = val).
        # Spindle (Batang) = dari val sampai ??
        # Sleeve (Body) = Diam di posisi X = 25 (misal).
        # Thimble = Mundur dari Sleeve.
        # Ini ribet karena mikrometer memanjang.
        
        # Pendekatan "Relative":
        # Anggap Sleeve diam di posisi X = val_mm (seolah-olah kita geser pandangan).
        # Tepi Thimble ada di X = val_mm + val_mm?
        
        # Paling logis untuk simulasi:
        # Tepi kiri Thimble merepresentasikan nilai bacaan.
        # Kita gambar Sleeve (Skala Utama) panjang dari kiri ke kanan.
        # Thimble menutupi sleeve sampai posisi val_mm.
        # Jadi Titik 0 Sleeve ada di kiri.
        # Masalah: Benda dimana?
        # Kita gambar terpisah saja. Benda di kiri. Mikrometer di kanan.
        
        # Sesuai request "visual menarik":
        # Kita gambar gabung.
        # Start Sleeve (Titik 0) = Visual Offset dari benda.
        sleeve_zero_x = val_mm + 2
        
        # Gambar Batang Spindle (dari benda ke sleeve)
        self.ax_sim.add_patch(plt.Rectangle((val_mm, -0.8), (sleeve_zero_x - val_mm) + 25, 1.6, facecolor='#bdc3c7', edgecolor='black')) 
        # (Itu batang dalam spindle yang panjang)
        
        # Gambar SLEEVE (Tabung Luar Diam)
        # Titik 0 ada di sleeve_zero_x.
        self.ax_sim.add_patch(plt.Rectangle((sleeve_zero_x, -1.2), 30, 2.4, facecolor=color_sleeve, edgecolor=color_stroke))
        self.ax_sim.plot([sleeve_zero_x, sleeve_zero_x+30], [0, 0], color='black', linewidth=1)
        
        # Ticks Main Scale
        for i in range(30):
            tick_x = sleeve_zero_x + i
            # 1mm marks (Atas)
            self.ax_sim.plot([tick_x, tick_x], [0, 0.8], color='black', linewidth=1)
            if i % 5 == 0:
                self.ax_sim.text(tick_x, 0.9, str(i), ha='center', fontsize=8)
            # 0.5mm marks (Bawah)
            self.ax_sim.plot([tick_x+0.5, tick_x+0.5], [0, -0.8], color='black', linewidth=1)

        # --- 4. THIMBLE (ROTATING SCALE) ---
        # Tepi Thimble ada di posisi (sleeve_zero_x + val_mm)
        thimble_edge = sleeve_zero_x + val_mm
        
        # Gambar Thimble (Tabung Penutup) menutupi sisi kanan
        # Bentuk Bevel
        poly_thimble = plt.Polygon([
            [thimble_edge, -1.5], 
            [thimble_edge + 12, -1.5], [thimble_edge + 12, 1.5], 
            [thimble_edge, 1.5], 
            [thimble_edge - 1.5, 1.0], [thimble_edge - 1.5, -1.0] # Bevel nose
        ], closed=True, facecolor=color_thimble, edgecolor='black')
        self.ax_sim.add_patch(poly_thimble)
        
        # Skala Putar (Nonius) Vertical
        frac = val_mm - int(val_mm)
        center_tick = int(round(frac * 100)) % 50
        
        for i in range(-4, 5):
            val_tick = (center_tick + i) % 50
            y_pos = i * 0.3
            
            # Garis Tick di Bevel
            tx = thimble_edge - 0.5
            self.ax_sim.plot([tx, tx+1], [y_pos, y_pos], color='black', linewidth=1)
            
            # Angka
            if val_tick % 5 == 0:
                self.ax_sim.text(tx + 1.5, y_pos, str(val_tick), va='center', fontsize=7)

        # Highlight Reading line
        self.ax_sim.plot([thimble_edge - 2, thimble_edge], [0, 0], color='#e74c3c', linewidth=1.5)
        self.ax_sim.add_patch(plt.Rectangle((offset, -1), 20, 2, color='#ecf0f1', zorder=0)) # Tabung Sleeve putih
        self.ax_sim.plot([offset, offset+20], [0, 0], color='black', linewidth=1) # Garis tengah
        
        # Ticks Sleeve
        for i in range(25):
            x_pos = offset + i
            # Jika x_pos < bibir thimble, gambar.
            bibir_thimble = offset + val_mm
            
            if x_pos < bibir_thimble:
                # 1 mm (Atas)
                self.ax_sim.plot([x_pos, x_pos], [0, 0.5], color='black', linewidth=1)
                if i % 5 == 0:
                    self.ax_sim.text(x_pos, 0.8, str(i), ha='center', fontsize=8)
                
                # 0.5 mm (Bawah)
                if x_pos + 0.5 < bibir_thimble:
                    self.ax_sim.plot([x_pos+0.5, x_pos+0.5], [0, -0.5], color='black', linewidth=1)

        # THIMBLE (BERGERAK/MUNDUR)
        # Ujung kiri thimble ada di bibir_thimble
        thimble_len = 8
        self.ax_sim.add_patch(plt.Rectangle((bibir_thimble, -1.2), thimble_len, 2.4, color='#95a5a6', zorder=5))
        
        # Skala pada Thimble (Vertikal)
        # Kita harus mensimulasikan nilai desimal. 
        # desimal = val_mm % 0.5 (karena satu putaran thimble = 0.5 mm)
        # Tapi ada 50 strip. Jadi nilai terbaca val_mm sisa 0.5 mm dikali 100.
        
        fraction = (val_mm % 0.5) * 100 # skalar 0 .. 49.99
        # Misal fraction = 30. Berarti angka 30 di thimble pas di garis tengah.
        
        # Gambar garis-garis thimble secara "pseudo 3D" (vertikal lines)
        # Center line is 'fraction'. Above is fraction+1, Below is fraction-1.
        
        center_val = int(fraction)
        
        for k in range(-3, 4): # Gambar 7 garis sekitar center
            val_show = (center_val + k) % 50
            y_pos = k * 0.3 # Jarak antar garis vertikal
            
            # Garis strip
            self.ax_sim.plot([bibir_thimble, bibir_thimble+1.5], [y_pos, y_pos], color='black', linewidth=1, zorder=6)
            
            # Angka
            if val_show % 5 == 0:
                self.ax_sim.text(bibir_thimble + 2, y_pos, str(val_show), va='center', fontsize=8, zorder=6)
                
        # Garis batas thimble
        self.ax_sim.plot([bibir_thimble, bibir_thimble], [-1.2, 1.2], color='black', linewidth=2, zorder=7)

    # ===========================
    # TAB 1: PENGUKURAN TUNGGAL (OLD CODE - RETAINED OR MOVED?)
    # ===========================
    # ... (Bagian ini digantikan/di-merge ke setup_tab1 yang baru) ...
    # Agar clean, kita hapus metode setup_tab1 dan process_tunggal yang lama 
    # di pikiran kita, tapi di kode ini saya sudah menimpa setup_tab1.

    # ... Sisa Tab 2 dan 3 tetap sama ...
    # TAB 2: PENGUKURAN BERULANG
    def setup_tab2(self):
        # Frame Input
        input_frame = ttk.LabelFrame(self.tab2, text="B. Input Data Sampel")
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Data (pisahkan koma):").pack(side="top", anchor="w", padx=5)
        self.entry_data_berulang = ttk.Entry(input_frame, width=80)
        self.entry_data_berulang.insert(0, "10.0, 10.2, 10.1, 10.0, 10.0, 9.9, 10.1, 9.8, 9.9, 10.0")
        self.entry_data_berulang.pack(side="top", padx=5, pady=5, fill="x")

        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(side="top", fill="x", padx=5, pady=5)
        ttk.Button(btn_frame, text="Analisis Data", command=self.process_berulang).pack(side="left")
        ttk.Button(btn_frame, text="Generate Data Acak", command=self.generate_random_data).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Reset", command=self.reset_tab2).pack(side="left", padx=10)

        # Area analisis lengkap (statistik)
        stats_frame = ttk.Frame(self.tab2)
        stats_frame.pack(fill="both", expand=False, padx=10, pady=(0, 5))
        self.stats_text = tk.Text(stats_frame, height=18, bg="#ecf0f1", font=("Consolas", 12))
        self.stats_text.pack(fill="both", expand=True)

        # Visualisasi sebaran data di bawahnya
        vis_frame = ttk.Frame(self.tab2)
        vis_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.fig_berulang = Figure(figsize=(7, 4), dpi=100)
        self.ax_berulang = self.fig_berulang.add_subplot(111)
        self.canvas_berulang = FigureCanvasTkAgg(self.fig_berulang, master=vis_frame)
        self.canvas_berulang.get_tk_widget().pack(fill="both", expand=True)

    def hitung_ketidakpastian_berulang(self):
        try:
            raw_data = self.entry_data_berulang.get()
            data = [float(x.strip()) for x in raw_data.split(',')]
            n = len(data)
            if n < 2:
                raise ValueError("Data harus lebih dari 1.")
            mean = statistics.mean(data)
            stdev = statistics.stdev(data)
            delta_x = stdev / math.sqrt(n)
            ralat_nisbih = delta_x / mean if mean != 0 else 0
            persentase_ketelitian = 100 - (ralat_nisbih * 100)
            res = f"--- KETIDAKPASTIAN PENGUKURAN BERULANG ---\n"
            res += f"Rata-rata (x̄)           : {mean:.4f}\n"
            res += f"Ketidakpastian (Δx)      : {delta_x:.4f}\n"
            res += f"Ralat Nisbih             : {ralat_nisbih:.4f}\n"
            res += f"Persentase Ketelitian    : {persentase_ketelitian:.2f}%\n"
            res += f"Pelaporan: ({mean:.3f} ± {delta_x:.3f})"
            self.result_text_berulang.delete(1.0, tk.END)
            self.result_text_berulang.insert(tk.END, res)
        except Exception:
            self.result_text_berulang.delete(1.0, tk.END)
            self.result_text_berulang.insert(tk.END, "Format data tidak valid atau kurang dari 2 data.")
    def reset_tab2(self):
        self.entry_data_berulang.delete(0, tk.END)
        self.entry_data_berulang.insert(0, "10.0, 10.2, 10.1, 10.0, 10.0, 9.9, 10.1, 9.8, 9.9, 10.0")
        self.stats_text.delete(1.0, tk.END)
        self.ax_berulang.clear()
        self.ax_berulang.set_title("Distribusi Data Pengukuran Berulang")
        self.canvas_berulang.draw()

        # Tidak membuat ulang frame dan widget, cukup reset konten

    def generate_random_data(self):
        # Buat data dummy random normal
        data = np.random.normal(loc=10.0, scale=0.1, size=20)
        data_str = ", ".join([f"{x:.2f}" for x in data])
        self.entry_data_berulang.delete(0, tk.END)
        self.entry_data_berulang.insert(0, data_str)

    def process_berulang(self):
        try:
            raw_data = self.entry_data_berulang.get()
            data = [float(x.strip()) for x in raw_data.split(',')]
            n = len(data)
            if n < 2:
                raise ValueError("Data harus lebih dari 1.")

            # Perhitungan Statistik
            mean = statistics.mean(data)
            stdev = statistics.stdev(data)
            minimum = min(data)
            maximum = max(data)
            q1 = np.percentile(data, 25)
            q3 = np.percentile(data, 75)
            median = np.median(data)
            delta_x = stdev / math.sqrt(n)


            # Analisis tambahan: ralat nisbih dan persentase ketelitian
            ralat_nisbih = delta_x / mean if mean != 0 else 0
            persentase_ketelitian = 100 - (ralat_nisbih * 100)


            output = f"--- STATISTIK & PERHITUNGAN LENGKAP ---\n"
            output += f"Jumlah Data (n)         : {n}\n"
            output += f"Rata-rata (x̄)           : {mean:.4f}\n"
            output += f"Median                  : {median:.4f}\n"
            output += f"Q1 (25%)                : {q1:.4f}\n"
            output += f"Q3 (75%)                : {q3:.4f}\n"
            output += f"Minimum                 : {minimum:.4f}\n"
            output += f"Maksimum                : {maximum:.4f}\n"
            output += f"Std. Deviasi (s)        : {stdev:.4f}\n"
            output += f"\n--- ANALISIS DATA ---\n"
            output += f"Ketidakpastian (Δx)     : {delta_x:.4f}\n"
            output += f"Ralat Nisbih            : {ralat_nisbih:.4f}\n"
            output += f"Persentase Ketelitian   : {persentase_ketelitian:.2f}%\n"
            output += f"Pelaporan: ({mean:.3f} ± {delta_x:.3f})\n"

            # Tabel ralat nisbih tiap data
            output += f"\nTabel Ralat Nisbih Tiap Data:\n"
            output += f"{'No.':<4}{'xᵢ':>10}{'Ralat Nisbih':>18}\n"
            output += f"{'-'*32}\n"
            for i, xi in enumerate(data, 1):
                ralat_i = abs(xi - mean) / mean if mean != 0 else 0
                output += f"{i:<4}{xi:>10.4f}{ralat_i:>18.4f}\n"


            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(tk.END, output)


            # Visualisasi Histogram, Boxplot, dan Sebaran Data
            self.ax_berulang.clear()
            self.ax_berulang.set_title("Sebaran & Analisis Data Pengukuran Berulang")

            # Histogram
            count, bins, ignored = self.ax_berulang.hist(data, bins='auto', alpha=0.5, color='blue', density=True, label='Histogram')

            # Kurva Gauss (Normal Distribution)
            xmin, xmax = self.ax_berulang.get_xlim()
            x = np.linspace(xmin, xmax, 100)
            p = (1 / (stdev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / stdev) ** 2)
            self.ax_berulang.plot(x, p, 'k', linewidth=2, label='Distribusi Normal')

            # Garis Rata-rata dan Median
            self.ax_berulang.axvline(mean, color='red', linestyle='dashed', linewidth=1.5, label=f'Rata-rata: {mean:.2f}')
            self.ax_berulang.axvline(median, color='green', linestyle='dotted', linewidth=1.5, label=f'Median: {median:.2f}')

            # Boxplot di bawah histogram
            box = self.ax_berulang.boxplot(data, vert=False, positions=[-0.15], widths=0.1, patch_artist=True,
                                           boxprops=dict(facecolor='#f1c40f', color='#e67e22'),
                                           medianprops=dict(color='green'),
                                           whiskerprops=dict(color='#e67e22'),
                                           capprops=dict(color='#e67e22'),
                                           flierprops=dict(markerfacecolor='red', marker="o", markersize=5, linestyle='none'))

            # Visualisasi sebaran data (strip plot)
            y_strip = np.full_like(data, -0.25)
            self.ax_berulang.plot(data, y_strip, 'o', color='#e74c3c', alpha=0.7, label='Sebaran Data')

            self.ax_berulang.legend(loc='upper right')
            self.ax_berulang.set_xlabel("Nilai Pengukuran")
            self.ax_berulang.set_ylabel("Kepadatan Probabilitas")
            self.canvas_berulang.draw()

        except ValueError:
            messagebox.showerror("Error", "Cek format data. Gunakan angka dan tanda koma.")

    # ===========================
    # TAB 3: PERAMBATAN KESALAHAN
    # ===========================
    def setup_tab3(self):
        frame = ttk.Frame(self.tab3)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text="Menghitung Volume Balok (p x l x t)").grid(row=0, column=0, columnspan=2, pady=10)

        # Input p, l, t
        entries = {}
        labels = ['Panjang (p)', 'Lebar (l)', 'Tinggi (t)']
        vars = ['p', 'l', 't']
        
        for i, (lbl, var) in enumerate(zip(labels, vars)):
            ttk.Label(frame, text=lbl + ":").grid(row=i+1, column=0, sticky='e')
            entries[var] = ttk.Entry(frame)
            entries[var].grid(row=i+1, column=1, pady=5)
            
            ttk.Label(frame, text="± Δ" + var + ":").grid(row=i+1, column=2, sticky='e')
            entries['d'+var] = ttk.Entry(frame, width=10)
            entries['d'+var].grid(row=i+1, column=3, pady=5)

        # Default values
        entries['p'].insert(0, "10.0"); entries['dp'].insert(0, "0.1")
        entries['l'].insert(0, "5.0"); entries['dl'].insert(0, "0.1")
        entries['t'].insert(0, "4.0"); entries['dt'].insert(0, "0.1")

        self.entries_tab3 = entries
        

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=4, pady=20)
        ttk.Button(btn_frame, text="Hitung Perambatan", command=self.process_propagasi).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="Reset", command=self.reset_tab3).pack(side="left")
        
        self.result_label_propagasi = ttk.Label(frame, text="Hasil akan muncul di sini", font=("Consolas", 12), justify="left")
        self.result_label_propagasi.grid(row=5, column=0, columnspan=4)

    def reset_tab3(self):
        self.entries_tab3['p'].delete(0, tk.END)
        self.entries_tab3['p'].insert(0, "10.0")
        self.entries_tab3['dp'].delete(0, tk.END)
        self.entries_tab3['dp'].insert(0, "0.1")
        self.entries_tab3['l'].delete(0, tk.END)
        self.entries_tab3['l'].insert(0, "5.0")
        self.entries_tab3['dl'].delete(0, tk.END)
        self.entries_tab3['dl'].insert(0, "0.1")
        self.entries_tab3['t'].delete(0, tk.END)
        self.entries_tab3['t'].insert(0, "4.0")
        self.entries_tab3['dt'].delete(0, tk.END)
        self.entries_tab3['dt'].insert(0, "0.1")
        self.result_label_propagasi.config(text="Hasil akan muncul di sini")
        
    def process_propagasi(self):
        try:
            p = float(self.entries_tab3['p'].get())
            l = float(self.entries_tab3['l'].get())
            t = float(self.entries_tab3['t'].get())
            
            dp = float(self.entries_tab3['dp'].get())
            dl = float(self.entries_tab3['dl'].get())
            dt = float(self.entries_tab3['dt'].get())
            
            # Volume Base
            V = p * l * t
            
            # Propagasi (Rumus Turunan Parsial / Relatif)
            # Ketidakpastian relatif dV/V = sqrt( (dp/p)^2 + (dl/l)^2 + (dt/t)^2 )
            rel_p = dp/p
            rel_l = dl/l
            rel_t = dt/t
            
            rel_error_v = math.sqrt(rel_p**2 + rel_l**2 + rel_t**2)
            dV = V * rel_error_v
            
            # Format Output
            res = f"Volume (V) = {V:.2f}\n"
            res += f"Ketidakpastian Mutlak (ΔV) = {dV:.2f}\n"
            res += f"Ketidakpastian Relatif = {rel_error_v*100:.2f}%\n"
            res += f"\nHasil Akhir: V = ({V:.2f} ± {dV:.2f})"
            
            self.result_label_propagasi.config(text=res)
            
        except ValueError:
            self.result_label_propagasi.config(text="Input tidak valid")

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabKetidakpastian(root)
    root.mainloop()

