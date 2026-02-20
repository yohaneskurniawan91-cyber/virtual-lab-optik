import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from virtual_lab_data_manager import DataManager

# --- KONFIGURASI TAMPILAN AWAL ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class LoginDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Login Praktikan - Virtual Lab Optik")
        self.geometry("400x450")
        self.resizable(False, False)
        
        # Center window
        self.update_idletasks()
        width = 400
        height = 450
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")
        
        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.attributes("-topmost", True)
        
        # UI Elements
        ctk.CTkLabel(self, text="Selamat Datang", font=("Arial", 24, "bold")).pack(pady=(30, 10))
        ctk.CTkLabel(self, text="Silakan login untuk memulai praktikum", text_color="gray").pack(pady=(0, 20))
        
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        ctk.CTkLabel(self.frame, text="Nama Lengkap:", anchor="w").pack(fill="x", padx=20, pady=(10, 5))
        self.entry_nama = ctk.CTkEntry(self.frame, placeholder_text="Masukkan Nama Anda")
        self.entry_nama.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(self.frame, text="NIM / No. Identitas:", anchor="w").pack(fill="x", padx=20, pady=(5, 5))
        self.entry_nim = ctk.CTkEntry(self.frame, placeholder_text="Masukkan NIM")
        self.entry_nim.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(self.frame, text="Kelas / Kelompok:", anchor="w").pack(fill="x", padx=20, pady=(5, 5))
        self.entry_kelas = ctk.CTkEntry(self.frame, placeholder_text="Contoh: Fisika A - Kelompok 3")
        self.entry_kelas.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(self.frame, text="MASUK (LOGIN)", font=("Arial", 14, "bold"), height=40,
                      command=self.login).pack(fill="x", padx=20, pady=20)
                      
        ctk.CTkLabel(self, text="*Data Anda akan direkam untuk laporan otomatis", 
                     font=("Arial", 10), text_color="gray").pack(pady=10)

        # Autofill
        profile = DataManager.get_profile()
        if profile:
            self.entry_nama.insert(0, profile.get("nama", ""))
            self.entry_nim.insert(0, profile.get("nim", ""))
            self.entry_kelas.insert(0, profile.get("kelas", ""))
            
    def login(self):
        nama = self.entry_nama.get().strip()
        nim = self.entry_nim.get().strip()
        kelas = self.entry_kelas.get().strip()
        
        if not nama or not nim:
            messagebox.showerror("Login Error", "Nama dan NIM wajib diisi!")
            return
            
        if DataManager.save_profile(nama, nim, kelas):
            self.parent.deiconify() # Show main app
            self.destroy()
        else:
            messagebox.showerror("Error", "Gagal menyimpan profil.")

    def on_close(self):
        self.parent.destroy()

class VirtualLabOptikApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Hide initially for login
        self.withdraw()
        
        # Show Login
        self.after(100, self.show_login)

        # Konfigurasi Window Utama
        self.title("Virtual Lab Optik Pro - Physics Engine v2.0")
        self.geometry("1400x900")

        # Layout Grid (1x2) - Sidebar di kiri, Konten di kanan
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR (NAVIGASI) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        # Grid layout for sidebar
        self.sidebar_frame.grid_rowconfigure(8, weight=1) # Spacer at bottom

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="V-LAB OPTIK\nPRO EDITION", 
                                       font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 20))

        # Tombol Menu
        self.btn_profile = self.create_nav_btn("  👨‍💻  Profil Pengembang", self.show_profile_frame, 1)
        self.btn_geometri = self.create_nav_btn("  🔍  Optik Geometri", self.show_geometri_frame, 2)
        self.btn_snellius = self.create_nav_btn("  📐  Hukum Snellius", self.show_snellius_frame, 3)
        self.btn_interferensi = self.create_nav_btn("  🌊  Interferensi & Difraksi", self.show_interferensi_frame, 4)
        self.btn_polarisasi = self.create_nav_btn("  🕶️  Polarisasi Cahaya", self.show_polarisasi_frame, 5)
        self.btn_dispersi = self.create_nav_btn("  🌈  Dispersi Prisma", self.show_dispersi_frame, 6)
        self.btn_kisi = self.create_nav_btn("  🔬  Kisi Difraksi", self.show_kisi_frame, 7)

        # Footer Sidebar
        self.label_mode = ctk.CTkLabel(self.sidebar_frame, text="Mode Tampilan:", anchor="w")
        self.label_mode.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.option_mode = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                             command=ctk.set_appearance_mode)
        self.option_mode.grid(row=10, column=0, padx=20, pady=(5, 20))
        self.option_mode.set("Dark")

        # --- AREA KONTEN UTAMA ---
        self.current_frame = None
        self.show_profile_frame()

    def show_login(self):
        """Show login dialog"""
        LoginDialog(self)

    def create_nav_btn(self, text, command, row):
        btn = ctk.CTkButton(self.sidebar_frame, text=text, command=command, 
                            height=45, font=ctk.CTkFont(size=14, weight="bold"),
                            anchor="w", fg_color="transparent", text_color=("gray10", "#DCE4EE"),
                            hover_color=("gray70", "#3B8ED0"), border_spacing=10, corner_radius=8)
        btn.grid(row=row, column=0, sticky="ew", padx=15, pady=5)
        return btn

    def show_profile_frame(self):
        self.switch_frame(DeveloperProfileFrame)

    def show_geometri_frame(self):
        self.switch_frame(OptikGeometriFrame)

    def show_snellius_frame(self):
        self.switch_frame(SnelliusFrame)

    def show_interferensi_frame(self):
        self.switch_frame(InterferensiFrame)

    def show_polarisasi_frame(self):
        self.switch_frame(PolarisasiFrame)

    def show_dispersi_frame(self):
        self.switch_frame(DispersiFrame)
        
    def show_kisi_frame(self):
        self.switch_frame(KisiDifraksiFrame)

    def switch_frame(self, frame_class):
        if self.current_frame: self.current_frame.destroy()
        self.current_frame = frame_class(self)
        self.current_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)


# ==========================================
# BASE CLASS UNTUK MODUL
# ==========================================
class BaseModuleFrame(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header Module
        self.header = ctk.CTkFrame(self, height=50, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        ctk.CTkLabel(self.header, text=title, font=ctk.CTkFont(size=24, weight="bold")).pack(side="left")

        # Tabview (Simulasi vs Panduan)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.tab_sim = self.tabview.add("Laboratorium Virtual")
        self.tab_guide = self.tabview.add("Panduan & Teori")
        
        # Setup Grid Tab Simulasi
        self.tab_sim.grid_columnconfigure(1, weight=1)
        self.tab_sim.grid_rowconfigure(0, weight=1)
        
        # Data Recording
        self.recorded_data = []

    def wavelength_to_rgb(self, wavelength):
        """Konversi panjang gelombang (nm) ke RGB Tuple (0-255)"""
        gamma = 0.8
        intensity_max = 255
        try:
            if 380 <= wavelength <= 440:
                attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
                R = (-(wavelength - 440) / (440 - 380)) * attenuation ** gamma
                G = 0.0
                B = (1.0) * attenuation ** gamma
            elif 440 <= wavelength <= 490:
                R = 0.0
                G = ((wavelength - 440) / (490 - 440)) ** gamma
                B = 1.0
            elif 490 <= wavelength <= 510:
                R = 0.0
                G = 1.0
                B = (-(wavelength - 510) / (510 - 490)) ** gamma
            elif 510 <= wavelength <= 580:
                R = ((wavelength - 510) / (580 - 510)) ** gamma
                G = 1.0
                B = 0.0
            elif 580 <= wavelength <= 645:
                R = 1.0
                G = (-(wavelength - 645) / (645 - 580)) ** gamma
                B = 0.0
            elif 645 <= wavelength <= 750:
                attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
                R = (1.0) * attenuation ** gamma
                G = 0.0
                B = 0.0
            else:
                R = 0.0; G = 0.0; B = 0.0
            
            return (int(R * intensity_max), int(G * intensity_max), int(B * intensity_max))
        except:
            return (255, 255, 255)

    def setup_data_recording(self, parent_frame, get_data_callback):
        """Standard Data Recording Panel"""
        # Save frame to pack into
        frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(frame, text="Rekam & Simpan Data Eksperimen", 
                     font=("Arial", 12, "bold"), text_color="#00d2ff").pack(anchor="w")
        
        btn_record = ctk.CTkButton(frame, text="📸 Rekam Data (Snapshot)", 
                                   fg_color="#e1b12c", text_color="black",
                                   command=lambda: self.record_data(get_data_callback))
        btn_record.pack(fill="x", pady=5)
        
        btn_save = ctk.CTkButton(frame, text="💾 Simpan ke Excel/Database", 
                                 fg_color="#44bd32",
                                 command=self.save_recorded_data)
        btn_save.pack(fill="x", pady=5)
        
        self.lbl_count = ctk.CTkLabel(frame, text="Data tersimpan: 0 baris", font=("Arial", 10))
        self.lbl_count.pack()
        
    def record_data(self, callback):
        data = callback()
        if data:
            self.recorded_data.append(data)
            count = len(self.recorded_data)
            self.lbl_count.configure(text=f"Data tersimpan: {count} baris")
            # Blink effect or toast
            
    def save_recorded_data(self):
        if not self.recorded_data:
            messagebox.showwarning("Peringatan", "Belum ada data yang direkam!")
            return
            
        success, msg = DataManager.save_data_unified(self.recorded_data, getattr(self, "module_name", "Optik Experiment"))
        if success:
            messagebox.showinfo("Berhasil", msg)
            self.recorded_data = [] # Clear after save? Or keep? Usually keep until reset or new session.
            # self.lbl_count.configure(text="Data tersimpan: 0 baris") 
        else:
            messagebox.showerror("Gagal", msg)

    def add_plot_area(self):
        frame = ctk.CTkFrame(self.tab_sim)
        frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        return frame

    def add_control_panel(self):
        scroll = ctk.CTkScrollableFrame(self.tab_sim, width=320, label_text="Panel Kontrol Eksperimen")
        scroll.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        return scroll

    def setup_matplotlib(self, parent_frame, figsize=(6,5)):
        fig, ax = plt.subplots(figsize=figsize)
        # Styling Dark Mode
        fig.patch.set_facecolor('#2b2b2b')
        ax.set_facecolor('#1e1e1e')
        ax.tick_params(colors='white', which='both')
        for spine in ax.spines.values(): spine.set_color('white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        return fig, ax, canvas

    def set_guide_content(self, steps_list, tools_list, theory_text):
        # Frame Konten
        scroll = ctk.CTkScrollableFrame(self.tab_guide)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Judul Teori
        ctk.CTkLabel(scroll, text="A. Dasar Teori Fisika", font=ctk.CTkFont(size=18, weight="bold"), anchor="w").pack(fill="x", pady=(0,10))
        # Use Textbox for Theory so it can be longer and formatted better
        theory_box = ctk.CTkTextbox(scroll, height=200, fg_color="transparent", text_color="#dddddd", font=("Arial", 14))
        theory_box.pack(fill="x", padx=10, pady=(0,20))
        theory_box.insert("0.0", theory_text)
        theory_box.configure(state="disabled")

        # Alat & Bahan (Susunan Alat)
        ctk.CTkLabel(scroll, text="B. Susunan Alat (Equipment)", font=ctk.CTkFont(size=18, weight="bold"), anchor="w").pack(fill="x", pady=(0,10))
        
        # Container for tools grid
        tools_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        tools_frame.pack(fill="x", padx=20)
        
        for idx, item in enumerate(tools_list):
            # item could be a tuple (name, description) or just name
            if isinstance(item, tuple):
                name, desc = item
                text_display = f"📦 {name}\n    └ {desc}"
            else:
                text_display = f"📦 {item}"
                
            tool_lbl = ctk.CTkLabel(tools_frame, text=text_display, anchor="w", justify="left", text_color="#aaaaaa")
            tool_lbl.grid(row=idx // 2, column=idx % 2, sticky="w", padx=10, pady=5)

        # Langkah Kerja
        ctk.CTkLabel(scroll, text="\nC. Langkah Praktikum", font=ctk.CTkFont(size=18, weight="bold"), anchor="w").pack(fill="x", pady=(10,10))
        
        step_frame = ctk.CTkFrame(scroll, fg_color="#2b2b2b", corner_radius=10)
        step_frame.pack(fill="x", padx=10, pady=5)
        
        for i, step in enumerate(steps_list, 1):
            row = ctk.CTkFrame(step_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(row, text=f"{i}.", font=("Arial", 14, "bold"), width=30).pack(side="left", anchor="n")
            ctk.CTkLabel(row, text=step, font=("Arial", 14), justify="left", wraplength=700).pack(side="left", fill="x")


# ==========================================
# HALAMAN PROFIL PENGEMBANG
# ==========================================
class DeveloperProfileFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        # Center Content
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0)
        
        # Profile Icon
        profile_icon = ctk.CTkLabel(container, text="👨‍💻", font=("Arial", 100))
        profile_icon.pack(pady=(0, 20))
        
        # Name
        name_label = ctk.CTkLabel(container, text="Yohanes Kurniawan", font=ctk.CTkFont(size=32, weight="bold"))
        name_label.pack(pady=5)
        
        # Education & Background (From Fisika Modern Module)
        info_text = (
            "S3 Teknologi Pembelajaran Universitas Negeri Malang\n"
            "S2 Pendidikan Fisika Universitas Negeri Yogyakarta\n"
            "S1 Pendidikan Fisika Universitas Nusa Cendana\n"
            "Asal Lembata - Nusa Tenggara Timur\n"
            "Dosen Unika Santu Paulus Ruteng"
        )
        
        info_label = ctk.CTkLabel(container, text=info_text, font=ctk.CTkFont(size=16), 
                                  justify="center", text_color="#aab7b8")
        info_label.pack(pady=10)
        
        # Specs Box
        specs_frame = ctk.CTkFrame(container, fg_color="#2b2b2b", corner_radius=10)
        specs_frame.pack(pady=20, padx=20, fill="x")
        
        specs = [
            ("Framework UI", "CustomTkinter v5.2"),
            ("Physics Engine", "NumPy & Matplotlib"),
            ("License", "Educational Use Only"),
            ("Version", "2.0 Pro Edition")
        ]
        
        for key, val in specs:
            row = ctk.CTkFrame(specs_frame, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=5)
            ctk.CTkLabel(row, text=key, font=ctk.CTkFont(weight="bold")).pack(side="left")
            ctk.CTkLabel(row, text=val, text_color="#00d2ff").pack(side="right")


# ==========================================
# MODUL 1: OPTIK GEOMETRI (Advanced)
# ==========================================
class OptikGeometriFrame(BaseModuleFrame):
    def __init__(self, master):
        super().__init__(master, "Modul 1: Optik Geometri & Alat Optik")
        
        # 1. Setup Kontrol
        self.panel = self.add_control_panel()
        
        self.var_jenis = ctk.StringVar(value="Lensa Cembung (Konvergen)")
        ctk.CTkLabel(self.panel, text="Komponen Optik:").pack(anchor="w")
        ctk.CTkOptionMenu(self.panel, variable=self.var_jenis, 
                         values=["Lensa Cembung (Konvergen)", "Lensa Cekung (Divergen)", 
                                 "Cermin Cekung (Konvergen)", "Cermin Cembung (Divergen)", "Cermin Datar"],
                         command=self.update).pack(fill="x", pady=5)

        self.sl_f = self.add_slider("Jarak Fokus (f) [cm]", 5, 50, 15)
        self.sl_s = self.add_slider("Jarak Benda (s) [cm]", 0, 80, 20)
        self.sl_h = self.add_slider("Tinggi Benda (h) [cm]", 1, 10, 3)

        ctk.CTkLabel(self.panel, text="Opsi Visualisasi:").pack(anchor="w", pady=(15,5))
        self.check_ray1 = ctk.CTkCheckBox(self.panel, text="Sinar Istimewa 1 (Sejajar -> Fokus)", command=self.update)
        self.check_ray1.pack(anchor="w"); self.check_ray1.select()
        self.check_ray2 = ctk.CTkCheckBox(self.panel, text="Sinar Istimewa 2 (Pusat Optik)", command=self.update)
        self.check_ray2.pack(anchor="w"); self.check_ray2.select()
        self.check_ray3 = ctk.CTkCheckBox(self.panel, text="Sinar Istimewa 3 (Fokus -> Sejajar)", command=self.update)
        self.check_ray3.pack(anchor="w"); self.check_ray3.select()

        # Output Data
        self.res_frame = ctk.CTkFrame(self.panel)
        self.res_frame.pack(fill="x", pady=20)
        self.lbl_s_img = ctk.CTkLabel(self.res_frame, text="s' = - cm")
        self.lbl_s_img.pack()
        self.lbl_m = ctk.CTkLabel(self.res_frame, text="Perbesaran (M) = -")
        self.lbl_m.pack()
        self.lbl_sifat = ctk.CTkLabel(self.res_frame, text="Sifat: -", text_color="yellow")
        self.lbl_sifat.pack()

        # 2. Setup Plot
        self.plot_container = self.add_plot_area()
        self.fig, self.ax, self.canvas = self.setup_matplotlib(self.plot_container)
        
        # 3. Setup Panduan
        theory = (
            "HUKUM PEMANTULAN & PEMBIASAN (OPTIK GEOMETRI)\n\n"
            "1. Hukum Gauss (Lensa & Cermin Tipis):\n"
            "   1/f = 1/s + 1/s'\n"
            "   f  = Jarak fokus (cm)\n"
            "   s  = Jarak benda ke pusat optik (cm)\n"
            "   s' = Jarak bayangan ke pusat optik (cm)\n\n"
            "2. Perbesaran Linear (Magnification):\n"
            "   M = h'/h = -s'/s\n"
            "   Jika |M| > 1 : Diperbesar\n"
            "   Jika |M| < 1 : Diperkecil\n\n"
            "3. Konvensi Tanda (Sign Convention):\n"
            "   • Benda Nyata (s > 0): Benda di depan lensa/cermin.\n"
            "   • Bayangan Nyata (s' > 0): Dapat ditangkap layar (terbalik).\n"
            "   • Bayangan Maya (s' < 0): Tidak dapat ditangkap layar (tegak).\n"
            "   • Fokus Konvergen (f > 0): Lensa Cembung / Cermin Cekung.\n"
            "   • Fokus Divergen (f < 0): Lensa Cekung / Cermin Cembung."
        )
        
        tools = [
            ("Bangku Optik / Rel Presisi", "Landasan logam berskala cm untuk meletakkan komponen."),
            ("Sumber Cahaya", "Lampu pijar atau Lilin sebagai benda optik."),
            ("Lensa Cembung (+)", "Kekuatan +10D atau f=+10cm."),
            ("Lensa Cekung (-)", "Kekuatan -10D atau f=-10cm."),
            ("Cermin Cekung & Cembung", "Cermin lengkung dengan fokus tertentu."),
            ("Layar Putih", "Media penangkap bayangan nyata."),
            ("Pemegang Lensa/Cermin", "Klem geser yang dapat diatur tingginya.")
        ]
        
        steps = [
            "Susun alat pada Bangku Optik secara berurutan: Sumber Cahaya (Benda) - Lensa/Cermin - Layar.",
            "Pastikan poros utama semua komponen sejajar (tinggi sama).",
            "Pilih Lensa Cembung pada menu simulasi.",
            "Atur jarak benda (s) lebih besar dari 2f. Geser layar hingga terbentuk bayangan tajam.",
            "Catat jarak benda (s) dan jarak bayangan (s'). Hitung fokus (f) dan bandingkan dengan nilai asli.",
            "Ulangi dengan memindahkan benda ke posisi antara f dan 2f.",
            "Ganti dengan Lensa Cekung. Amati bahwa bayangan tidak pernah terbentuk di layar (Maya).",
            "Analisis sifat bayangan: Nyata/Maya, Tegak/Terbalik, Diperbesar/Diperkecil."
        ]

        self.set_guide_content(steps, tools, theory)

        # Setup Data Recording
        self.module_name = "Optik Geometri"
        self.setup_data_recording(self.panel, self.get_data)

        self.update()

    def get_data(self):
        f = self.sl_f.get()
        s = self.sl_s.get()
        h = self.sl_h.get()
        jenis = self.var_jenis.get()
        
        # Recalculate Logic to get derived values
        f_active = f
        if "Cekung (Divergen)" in jenis or "Cembung (Divergen)" in jenis:
            f_active = -f
        elif "Datar" in jenis:
            f_active = float('inf')
            
        if "Datar" in jenis:
            s_img = -s
            m = 1
            sifat = "Maya"
        elif abs(s - f_active) < 0.1: # At Focus
            s_img = float('inf')
            m = float('inf')
            sifat = "Tak Terdefinisi"
        else:
            s_img = (s * f_active) / (s - f_active)
            m = -s_img / s if s != 0 else 0
            # S image + means real (behind lens or in front of mirror?)
            # Wait, standard convention:
            # Lens: s' > 0 (Real, behind), s' < 0 (Virtual, front)
            # Mirror: s' > 0 (Real, front), s' < 0 (Virtual, behind)
            # But the formula 1/f = 1/s + 1/s' gives s' sign consistent with Real/Virtual
            sifat = "Nyata" if s_img > 0 else "Maya"
        
        return {
            "Jenis Optik": jenis,
            "Fokus (f)": f_active if f_active != float('inf') else "Inf",
            "Jarak Benda (s)": round(s, 2),
            "Tinggi Benda (h)": round(h, 2),
            "Jarak Bayangan (s')": round(s_img, 2) if s_img != float('inf') else "Inf",
            "Perbesaran (M)": round(m, 2) if m != float('inf') else "Inf",
            "Sifat": sifat
        }

    def add_slider(self, label, vmin, vmax, vdef):
        ctk.CTkLabel(self.panel, text=label).pack(anchor="w")
        slider = ctk.CTkSlider(self.panel, from_=vmin, to=vmax, number_of_steps=100, command=self.update)
        slider.set(vdef)
        slider.pack(fill="x", pady=5)
        return slider

    def update(self, _=None):
        self.ax.clear()
        
        # Params
        jenis = self.var_jenis.get()
        f_val = self.sl_f.get()
        s_val = self.sl_s.get()
        h_obj = self.sl_h.get()

        # Physics Logic Convention
        # s selalu positif (benda riil di depan optik)
        # Lensa Cembung / Cermin Cekung : f positif
        # Lensa Cekung / Cermin Cembung : f negatif
        
        is_mirror = "Cermin" in jenis
        is_flat = "Datar" in jenis
        
        if "Cekung (Konvergen)" in jenis or "Cembung (Konvergen)" in jenis:
            f = f_val
        elif "Konvergen" in jenis: # fallback
            f = f_val
        elif "Divergen" in jenis:
            f = -f_val
        else:
            f = float('inf') # Datar

        # Calculate Image
        text_info = ""
        if is_flat:
            s_img = -s_val
            m = 1
            h_img = h_obj
            real = False
            x_img = -s_img # s' negative, so x_img positive (Right)
        else:
            if abs(s_val - f) < 0.1: # At Focus
                s_img = float('inf')
                m = float('inf')
                h_img = float('inf')
                real = False
                x_img = float('inf')
            else:
                s_img = (s_val * f) / (s_val - f)
                m = -s_img / s_val
                h_img = m * h_obj
                
                # Determine Real/Virtual and X position
                if is_mirror:
                    # Mirror: Real is same side (-x), Virtual is behind (+x)
                    real = s_img > 0
                    x_img = -s_img 
                else:
                    # Lens: Real is opposite side (+x), Virtual is same side (-x)
                    real = s_img > 0
                    x_img = s_img

        # --- DRAWING ---
        self.ax.axhline(0, color='white', linewidth=1)
        self.ax.axvline(0, color='#00d2ff', linewidth=3, alpha=0.4) # Optic Axis
        
        # Draw Focus Points & Optic Shape
        if not is_flat:
            # Draw specific shape for Lens/Mirror
            y_curve = np.linspace(-15, 15, 100)
            if "Cembung" in jenis: # Convex
                curve = - (y_curve**2) / 100 if "Lensa" in jenis else (y_curve**2) / 100
            else: # Concave
                curve = (y_curve**2) / 100 if "Lensa" in jenis else - (y_curve**2) / 100
            
            # Simplified lens/mirror drawing 
            if "Lensa" in jenis:
                self.ax.add_patch(patches.Ellipse((0,0), width=2, height=30, color='skyblue', alpha=0.3))
                # Focal points
                self.ax.scatter([f, -f], [0, 0], color='#ff4757', zorder=5)
                self.ax.text(f, -2, 'F2', color='#ff4757', ha='center')
                self.ax.text(-f, -2, "F1", color='#ff4757', ha='center')
            else:
                # Mirror - Draw arc
                x_arc = curve
                self.ax.plot(x_arc, y_curve, color='cyan', linewidth=2)
                # Hatching for non-reflective side
                if "Cekung (Konvergen)" in jenis: # Cermin Cekung (Fokus didepan/kiri, R didepan/kiri)
                    # Real focus is at s > 0 side (Left for object?? No, usually left is incident)
                    # Convention here: Object at -s (Left).
                    # Concave Mirror: Focus is on the Left (-f).
                    # Note on f value: We set f positive for "Konvergen".
                    # But geometrically, if object is at -s, focus is at -f.
                    real_f = -abs(f) 
                else: # Cermin Cembung
                    # Virtual focus is on the Right (+f).
                    real_f = abs(f)

                self.ax.scatter([real_f], [0], color='#ff4757', zorder=5)
                self.ax.text(real_f, -2, 'F', color='#ff4757', ha='center')
                # Center of curvature
                self.ax.scatter([2*real_f], [0], color='white', marker='x')

        # Draw Object (Arrow) - Position at -s (Left side convention)
        x_obj = -s_val 
        self.draw_arrow(x_obj, 0, 0, h_obj, color='#2ed573', label="Benda")

        # Draw Image
        sifat_txt = []
        if s_img == float('inf'):
            sifat_txt = ["Bayangan di Tak Hingga"]
        else:
            # Coordinate mapping
            if is_mirror:
                # Mirror Formula: 1/s + 1/s' = 1/f
                # If s' is positive (Real), it is on the SAME side as object (Left).
                # If s' is negative (Virtual), it is on the BEHIND side (Right).
                # Our X-axis: Object is at negative X.
                # So "Same side" means negative X.
                # "Behind" means positive X.
                # Logic: If s_img > 0 (Real), draw at -s_img.
                # If s_img < 0 (Virtual), draw at -s_img (which becomes positive).
                # Wait, if s_img is calculated using standard formula where s, s' are coordinates?
                # Formula used: 1/f = 1/s + 1/s'. 
                # If s=20, f=10 -> s' = 20. Real. Position is at x = -20.
                # If s=5, f=10 -> s' = -10. Virtual. Position is at x = +10.
                
                # So for Mirror: x_img = -s_img
                x_img = -s_img
                real = s_img > 0
            else:
                # Lense:
                # s' > 0 (Real) -> Opposite side (Right -> +x)
                # s' < 0 (Virtual) -> Same side (Left -> -x)
                # So for Lens: x_img = s_img.
                x_img = s_img
                real = s_img > 0

            self.draw_arrow(x_img, 0, 0, h_img, color='#eccc68' if real else '#a29bfe', label="Bayangan")
            
            # Sinar Istimewa Drawing
            if self.check_ray1.get(): # Sejajar -> Fokus
                self.ax.plot([x_obj, 0], [h_obj, h_obj], 'w--', alpha=0.3)
                if not is_flat:
                    # After interface
                    if is_mirror: target_x = -f if real else f # Pantul
                    else: target_x = f # Bias ke F seberang
                    
                    # Extrapolate ray
                    slope = (0 - h_obj) / (target_x - 0) if target_x != 0 else 0
                    y_end = h_obj + slope * (x_img - 0)
                    self.ax.plot([0, x_img], [h_obj, y_end], 'w--', alpha=0.3)

            if self.check_ray2.get(): # Lewat Pusat
                if not is_flat:
                    # Lensa: lurus, Cermin: pantul simetris
                    if is_mirror:
                         self.ax.plot([x_obj, 0], [h_obj, 0], 'c--', alpha=0.3)
                         self.ax.plot([0, x_obj], [0, -h_obj], 'c--', alpha=0.3)
                    else:
                         self.ax.plot([x_obj, x_img], [h_obj, h_img], 'c--', alpha=0.3)

            # Sifat Data
            sifat_txt.append("Nyata" if real else "Maya")
            sifat_txt.append("Tegak" if m > 0 else "Terbalik")
            sifat_txt.append(f"M = {abs(m):.2f}x")

        # Styling Limits
        limit = max(abs(x_obj), 60)
        self.ax.set_xlim(-limit, limit)
        self.ax.set_ylim(-20, 20)
        self.ax.legend(facecolor='#2b2b2b', labelcolor='white')
        self.ax.set_title(f"Simulasi: {jenis}", color='white')
        
        # Update Labels
        if s_img == float('inf'):
            self.lbl_s_img.configure(text="s' = ∞")
            self.lbl_m.configure(text="M = ∞")
        else:
            self.lbl_s_img.configure(text=f"s' = {s_img:.1f} cm")
            self.lbl_m.configure(text=f"M = {m:.2f}x")
        
        self.lbl_sifat.configure(text=" | ".join(sifat_txt))
        self.canvas.draw()

    def draw_arrow(self, x, y, dx, dy, color, label):
        self.ax.arrow(x, y, dx, dy, head_width=1.5, head_length=1.5, fc=color, ec=color, width=0.4, label=label)


# ==========================================
# MODUL 2: HUKUM SNELLIUS (Pro)
# ==========================================
class SnelliusFrame(BaseModuleFrame):
    def __init__(self, master):
        super().__init__(master, "Modul 2: Pembiasan Cahaya (Refraction)")
        
        panel = self.add_control_panel()
        
        self.var_mat1 = ctk.StringVar(value="Udara (n=1.0)")
        self.var_mat2 = ctk.StringVar(value="Kaca (n=1.5)")
        
        materials = ["Vakum (n=1.0)", "Udara (n=1.0003)", "Air (n=1.33)", "Kaca (n=1.5)", "Intan (n=2.42)"]
        
        ctk.CTkLabel(panel, text="Medium 1 (Atas):").pack(anchor="w")
        ctk.CTkOptionMenu(panel, variable=self.var_mat1, values=materials, command=self.update).pack(fill="x", pady=5)
        
        ctk.CTkLabel(panel, text="Medium 2 (Bawah):").pack(anchor="w", pady=(10,0))
        ctk.CTkOptionMenu(panel, variable=self.var_mat2, values=materials, command=self.update).pack(fill="x", pady=5)
        
        self.sl_angle = ctk.CTkSlider(panel, from_=0, to=90, number_of_steps=90, command=self.update)
        self.sl_angle.set(45)
        ctk.CTkLabel(panel, text="Sudut Datang (Incident Angle)").pack(anchor="w", pady=(15,0))
        self.sl_angle.pack(fill="x")
        
        # Output Info
        self.info_box = ctk.CTkTextbox(panel, height=120, text_color="#00fa9a")
        self.info_box.pack(fill="x", pady=20)

        # Plot
        self.plot_container = self.add_plot_area()
        self.fig, self.ax, self.canvas = self.setup_matplotlib(self.plot_container)
        
        # Panduan
        theory = (
            "HUKUM PEMBIASAN CAHAYA (SNELLIUS)\n\n"
            "1. Pembiasan (Refraction):\n"
            "   Peristiwa pembelokan arah cahaya saat melewati batas\n"
            "   dua medium berbeda kerapatan (n1 berbeda dengan n2).\n\n"
            "2. Hukum Snellius:\n"
            "   n1 . sin(i) = n2 . sin(r)\n"
            "   n1 = Indeks bias medium datang\n"
            "   n2 = Indeks bias medium tuju\n"
            "   i  = Sudut datang (terhadap garis normal)\n"
            "   r  = Sudut bias (terhadap garis normal)\n\n"
            "3. Indeks Bias (n):\n"
            "   n = c / v\n"
            "   c = Kecepatan cahaya vakum (3x10^8 m/s)\n"
            "   v = Kecepatan cahaya dalam medium\n\n"
            "4. Pemantulan Sempurna (Total Internal Reflection):\n"
            "   Terjadi jika cahaya dari medium rapat (n1 besar) ke renggang\n"
            "   (n2 kecil) dengan sudut i > sudut kritis (ic).\n"
            "   sin(ic) = n2 / n1."
        )

        tools = [
            ("Sumber Cahaya Laser", "Menghasilkan berkas cahaya tunggal (monokromatik)."),
            ("Meja Optik (Hartl)", "Piringan berskala sudut 0-360 derajat."),
            ("Kaca Setengah Lingkaran", "Benda bening untuk diamati pembiasannya (n ≈ 1.5)."),
            ("Prisma Segitiga", "Opsional, untuk mendemonstrasikan dispersi."),
            ("Mistar & Busur Derajat", "Alat ukur sudut manual.")
        ]

        steps = [
            "Letakkan Kaca Setengah Lingkaran tepat di tengah Meja Optik.",
            "Arahkan sinar Laser tegak lurus (0 derajat) terhadap bidang lengkung kaca.",
            "Putar meja optik untuk mengubah sudut datang (i) dari 10 derajat hingga 80 derajat.",
            "Catat sudut bias (r) yang terjadi pada setiap perubahan sudut i.",
            "Pastikan sinar datang dari Udara ke Kaca (Medium Renggang ke Rapat). Sinar akan dibiaskan MENDEKATI Garis Normal.",
            "Balik posisi: Sinar datang dari Kaca ke Udara (Rapat ke Renggang). Sinar akan dibiaskan MENJAUHI Garis Normal.",
            "Cari Sudut Kritis: Terus perbesar sudut datang dari kaca hingga sinar bias sejajar permukaan (r = 90 derajat).",
            "Amati fenomena Pemantulan Sempurna jika sudut datang > sudut kritis."
        ]

        self.set_guide_content(steps, tools, theory)
        
        # Setup Data Recording
        self.module_name = "Hukum Snellius"
        self.setup_data_recording(panel, self.get_data)
        
        self.update()

    def get_data(self):
        n1 = self.get_n(self.var_mat1.get())
        n2 = self.get_n(self.var_mat2.get())
        i = self.sl_angle.get()
        
        # Calculate r (Physics)
        try:
            rad1 = np.radians(i)
            sin_r = (n1/n2) * np.sin(rad1)
            if abs(sin_r) > 1.0:
                r_val = "Pantulan Sempurna (Total Internal Reflection)"
            else:
                r_val = round(np.degrees(np.arcsin(sin_r)), 2)
        except:
             r_val = "Error"
             
        return {
            "Medium 1": self.var_mat1.get(),
            "Medium 2": self.var_mat2.get(),
            "Indeks Bias 1 (n1)": n1,
            "Indeks Bias 2 (n2)": n2,
            "Sudut Datang (i)": i,
            "Sudut Bias (r)": r_val
        }

    def get_n(self, text):
        return float(text.split('=')[1].replace(')', ''))

    def update(self, _=None):
        n1 = self.get_n(self.var_mat1.get())
        n2 = self.get_n(self.var_mat2.get())
        deg1 = self.sl_angle.get()
        rad1 = np.radians(deg1)
        
        # Snellius Calc
        try:
            sin_deg2 = (n1 / n2) * np.sin(rad1)
            tir = False
            if abs(sin_deg2) > 1.0:
                tir = True
                deg2 = deg1 # Refleksi
                rad2 = -np.radians(deg1) # Arah berlawanan visual
            else:
                rad2 = np.arcsin(sin_deg2)
                deg2 = np.degrees(rad2)
        except:
            deg2 = 0; rad2 = 0; tir = False

        # Visuals
        self.ax.clear()
        
        # Draw Mediums
        self.ax.fill_between([-10, 10], 0, 10, color='skyblue' if n1 < 1.1 else '#0097e6', alpha=0.3)
        self.ax.fill_between([-10, 10], -10, 0, color='skyblue' if n2 < 1.1 else '#0097e6', alpha=0.5)
        self.ax.axhline(0, color='white', linewidth=2) # Interface
        self.ax.axvline(0, color='gray', linestyle='--') # Normal
        
        # Draw Protractor (Busur)
        busur = patches.Arc((0,0), 6, 6, angle=0, theta1=0, theta2=180, edgecolor='white', linestyle=':', alpha=0.5)
        self.ax.add_patch(busur)
        busur2 = patches.Arc((0,0), 6, 6, angle=0, theta1=180, theta2=360, edgecolor='white', linestyle=':', alpha=0.5)
        self.ax.add_patch(busur2)

        # Rays
        len_ray = 8
        # Incident Ray (Top-Left quadrant coming down)
        # origin (0,0). Source is at (-x, +y).
        x1 = -len_ray * np.sin(rad1)
        y1 = len_ray * np.cos(rad1)
        self.ax.plot([x1, 0], [y1, 0], color='#ff5252', linewidth=3, label='Sinar Datang')
        
        # Result Ray
        if tir:
            # Reflection (Top-Right quadrant going up)
            # Angle is equal to i
            x2 = len_ray * np.sin(np.radians(deg2)) 
            y2 = len_ray * np.cos(np.radians(deg2)) 
            self.ax.plot([0, x2], [0, y2], color='#ff5252', linewidth=3, linestyle='--', label='Pantulan Sempurna')
            res_text = f"TOTAL INTERNAL REFLECTION!\nSudut Pantul = {deg2:.1f}°"
        else:
            # Refraction (Bottom-Right quadrant going down)
            # Angle r is measured from Normal (Negative Y-axis)
            # So x is positive, y is negative.
            x2 = len_ray * np.sin(rad2)
            y2 = -len_ray * np.cos(rad2)
            self.ax.plot([0, x2], [0, y2], color='#7bed9f', linewidth=3, label='Sinar Bias')
            res_text = f"Sudut Bias (θ2) = {deg2:.1f}°"
            
            # Partial Reflection (Weak) - Real Physics!
            # Always exists.
            x3 = len_ray * np.sin(rad1)
            y3 = len_ray * np.cos(rad1)
            self.ax.plot([0, x3], [0, y3], color='#ff5252', linewidth=1, alpha=0.3, linestyle=':', label='Pantulan Parsial')

        self.ax.set_xlim(-8, 8); self.ax.set_ylim(-8, 8)
        self.ax.set_aspect('equal')
        self.ax.legend(loc='upper right', facecolor='#2b2b2b', labelcolor='white')
        
        # Calculations Text
        crit_txt = ""
        if n1 > n2:
            theta_c = np.degrees(np.arcsin(n2/n1))
            crit_txt = f"\nSudut Kritis = {theta_c:.1f}°"
        
        self.info_box.configure(state="normal")
        self.info_box.delete("0.0", "end")
        self.info_box.insert("0.0", f"Analisis Fisika:\n----------------\nn1 = {n1}, n2 = {n2}\nSudut Datang (θ1) = {deg1:.1f}°\n{res_text}{crit_txt}")
        self.info_box.configure(state="disabled")
        self.canvas.draw()


# ==========================================
# MODUL 3: INTERFERENSI & DIFRAKSI (Pro)
# ==========================================
class InterferensiFrame(BaseModuleFrame):
    def __init__(self, master):
        super().__init__(master, "Modul 3: Gelombang Cahaya (Interferensi)")
        
        panel = self.add_control_panel()
        
        # Tabs untuk Sub-Modul
        self.mode_tab = ctk.CTkTabview(panel, height=100)
        self.mode_tab.pack(fill="x", pady=5)
        self.mode_tab.add("Celah Ganda (Young)")
        self.mode_tab.add("Difraksi Celah Tunggal")
        self.mode_tab.set("Celah Ganda (Young)")
        
        # Shared Controls in Panel
        ctk.CTkLabel(panel, text="Warna Laser (λ):").pack(anchor="w")
        self.sl_wave = ctk.CTkSlider(panel, from_=380, to=750, number_of_steps=370, command=self.update)
        self.sl_wave.set(632) # HeNe Red
        self.sl_wave.pack(fill="x"); self.lbl_wave = ctk.CTkLabel(panel, text="632 nm (Merah)")
        self.lbl_wave.pack()

        ctk.CTkLabel(panel, text="Lebar/Jarak Celah (a/d):").pack(anchor="w", pady=10)
        self.sl_d = ctk.CTkSlider(panel, from_=0.05, to=0.5, number_of_steps=90, command=self.update) # type: ignore
        self.sl_d.set(0.1)
        self.sl_d.pack(fill="x"); self.lbl_d = ctk.CTkLabel(panel, text="0.10 mm")
        self.lbl_d.pack()

        ctk.CTkLabel(panel, text="Jarak Layar (L):").pack(anchor="w", pady=10)
        self.sl_L = ctk.CTkSlider(panel, from_=0.5, to=2.0, number_of_steps=30, command=self.update) # type: ignore
        self.sl_L.set(1.0)
        self.sl_L.pack(fill="x"); self.lbl_L = ctk.CTkLabel(panel, text="1.0 m")
        self.lbl_L.pack()

        # Connect tab change to update
        self.mode_tab._command = self.update

        # Plot
        self.plot_container = self.add_plot_area()
        self.fig, (self.ax1, self.ax2), self.canvas = self.setup_matplotlib_multi(self.plot_container)
        
        # Panduan
        theory = (
            "GELOMBANG CAHAYA (INTERFERENSI & DIFRAKSI)\n\n"
            "1. Sifat Gelombang Cahaya:\n"
            "   Cahaya bersifat sebagai gelombang elektromagnetik transversal.\n"
            "   Mengalami superposisi (penjumlahan amplitudo).\n\n"
            "2. Interferensi Celah Ganda (Young):\n"
            "   Terbentuk pola garis Terang-Gelap akibat perbedaan lintasan (Δ).\n"
            "   Pola Terang (Konstruktif):\n"
            "   d sin θ = n . λ  (n = 0, 1, 2...)\n"
            "   Pola Gelap (Destruktif):\n"
            "   d sin θ = (n - 1/2) . λ\n\n"
            "3. Difraksi Celah Tunggal (Fraunhofer):\n"
            "   Pola Gelap (Minimum):\n"
            "   a sin θ = n . λ  (n = 1, 2, 3...)\n\n"
            "4. Variabel:\n"
            "   d = Jarak antar celah (mm)\n"
            "   a = Lebar celah tunggal (mm)\n"
            "   L = Jarak celah ke layar (m)\n"
            "   y = Jarak pola ke terang pusat (m)\n"
            "   Untuk sudut kecil (θ < 10 derajat), sin θ ≈ tan θ = y / L."
        )

        tools = [
            ("Laser Monokromatik", "Sumber koheren (Wajib). Merah=632nm, Hijau=532nm."),
            ("Piringan Celah (Slit Plate)", "Piringan berisi celah ganda (d=0.1mm) dan celah tunggal."),
            ("Bangku Optik (Rel)", "Landasan rel besi untuk menjaga kesejajaran."),
            ("Layar Putih", "Media penangkap pola gelap-terang."),
            ("Mistar Panjang / Rollmeter", "Untuk mengukur jarak Layar (L)."),
            ("Jangka Sorong digital", "Mengukur jarak pola Terang-Pusat (y).")
        ]

        steps = [
            "Hidupkan Laser (Hati-hati, jangan menatap langsung sumber sinar!).",
            "Pasang Celah Ganda pada pemegang di rel optik.",
            "Letakkan Layar sejauh 1-2 meter dari celah. Lebih jauh lebih baik agar pola renggang.",
            "Pastikan sinar Laser tepat mengenai tengah celah.",
            "Amati pola garis-garis terang dan gelap yang muncul di Layar.",
            "Ukur jarak antar 2 garis terang yang berdekatan (y) menggunakan jangka sorong/penggaris milimeter.",
            "Hitung panjang gelombang (λ) menggunakan rumus: λ = (y . d) / (n . L).",
            "Bandingkan hasil hitungan dengan label pada Laser (misal: 632 nm).",
            "Ulangi percobaan dengan Celah Tunggal (Difraksi). Amati perbedaan pola intensitasnya."
        ]

        self.set_guide_content(steps, tools, theory)
        
        # Setup Data Recording
        self.module_name = "Interferensi & Difraksi"
        self.setup_data_recording(panel, self.get_data)
        
        self.update()
        
    def get_data(self):
        return {
            "Mode": self.mode_tab.get(),
            "Warna Laser (λ) [nm]": int(self.sl_wave.get()),
            "Lebar Celah (d) [mm]": round(self.sl_d.get(), 2),
            "Jarak Layar (L) [m]": round(self.sl_L.get(), 2)
        }

    def setup_matplotlib_multi(self, parent):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6), gridspec_kw={'height_ratios': [1, 2]})
        fig.patch.set_facecolor('#2b2b2b')
        for ax in [ax1, ax2]:
            ax.set_facecolor('#1e1e1e')
            ax.tick_params(colors='white')
            for spine in ax.spines.values(): spine.set_color('white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        return fig, (ax1, ax2), canvas

    def update(self, _=None):
        mode = self.mode_tab.get()
        lam_nm = self.sl_wave.get()
        d_mm = self.sl_d.get()
        L_m = self.sl_L.get()
        
        # Update Labels
        self.lbl_wave.configure(text=f"{int(lam_nm)} nm")
        self.lbl_d.configure(text=f"{d_mm:.2f} mm")
        self.lbl_L.configure(text=f"{L_m:.1f} m")
        
        # Physic constants
        lam = lam_nm * 1e-9
        d = d_mm * 1e-3
        L = L_m
        k = 2 * np.pi / lam

        # Screen coordinates Y (mm)
        Y = np.linspace(-30, 30, 1000) # -3cm to 3cm
        y_m = Y * 1e-3
        theta = np.arctan(y_m / L) 
        
        # Calculate Intensity (Relative)
        # Convert lambda to meters for wave calc
        lam_m = lam
        d_m = d
        a_m = d / 5  # Asumsi lebar celah a = 1/5 dari d (standar umum)

        # Beta for diffraction Envelope: beta = (pi * a * sin(theta)) / lambda
        # Alpha/Delta for interference: delta = (2*pi * d * sin(theta)) / lambda
        # Note: numpy.sinc(x) is sin(pi*x)/(pi*x). So we pass (a sin theta / lambda)
        
        sin_theta = np.sin(theta)
        
        if mode == "Celah Ganda (Young)":
            # I = I0 * cos^2(delta/2) * sinc^2(beta)
            # delta/2 = (pi * d * sin(theta)) / lambda
            val_inter = (d_m * sin_theta) / lam_m
            val_diff = (a_m * sin_theta) / lam_m
            
            # Interference term
            term_inter = np.cos(np.pi * val_inter)**2
            
            # Diffraction envelope term
            term_diff = np.sinc(val_diff)**2
            
            intensity = term_inter * term_diff
            title = f"Interferensi Celah Ganda (d={d_mm:.2f}mm, a={d_mm/5:.2f}mm)"
        else: # Tunggal
            # I = I0 * sinc^2(beta)
            # Here 'd' slider acts as slit width 'a'
            width = d_m 
            val_diff = (width * sin_theta) / lam_m
            intensity = np.sinc(val_diff)**2 
            title = f"Difraksi Celah Tunggal (a={d_mm:.2f}mm)"

        # --- PLOT 1: Simulated Screen ---
        self.ax1.clear()
        # Get RGB
        rgb = self.wavelength_to_rgb(lam_nm) # Use Base Method
        color_norm = [c/255 for c in rgb]

        # Efficient drawing for Screen
        # Create an image array (1, N) where logic is applied to alpha
        img_arr = np.zeros((1, len(Y), 4))
        img_arr[:, :, 0] = color_norm[0]
        img_arr[:, :, 1] = color_norm[1]
        img_arr[:, :, 2] = color_norm[2]
        img_arr[:, :, 3] = intensity # Alpha mapped to intensity
        
        self.ax1.imshow(img_arr, aspect='auto', extent=[Y[0], Y[-1], 0, 1])
        self.ax1.set_yticks([])
        self.ax1.set_xlabel("Posisi Layar (mm)", color='white', fontsize=8)
        self.ax1.set_title("Visualisasi Pola Terang-Gelap", fontsize=10, color='white')

        # --- PLOT 2: Intensity Graph ---
        self.ax2.clear()
        self.ax2.plot(Y, intensity, color=color_norm, linewidth=2)
        self.ax2.fill_between(Y, intensity, color=color_norm, alpha=0.3)
        self.ax2.set_xlabel("Posisi y (mm)")
        self.ax2.set_ylabel("Intensitas (I/I₀)")
        self.ax2.set_xlim(-30, 30)
        self.ax2.set_ylim(0, 1.1)
        self.ax2.grid(True, linestyle=':', alpha=0.3)
        self.ax2.set_title(title, fontsize=10, color='white')

        self.canvas.draw()

    # Removed Duplicate wavelength_to_rgb


# ==========================================
# MODUL 4: POLARISASI CAHAYA (Hukum Malus)
# ==========================================
class PolarisasiFrame(BaseModuleFrame):
    def __init__(self, master):
        super().__init__(master, "Modul 4: Polarisasi Cahaya (Hukum Malus)")
        
        panel = self.add_control_panel()
        
        ctk.CTkLabel(panel, text="Intensitas Awal (I₀) [W/m²]:").pack(anchor="w")
        self.sl_I0 = ctk.CTkSlider(panel, from_=0, to=100, number_of_steps=100, command=self.update)
        self.sl_I0.set(100)
        self.sl_I0.pack(fill="x"); self.lbl_I0 = ctk.CTkLabel(panel, text="100 W/m²")
        self.lbl_I0.pack()

        ctk.CTkLabel(panel, text="Sudut Analisator (θ) [Derajat]:").pack(anchor="w", pady=10)
        self.sl_theta = ctk.CTkSlider(panel, from_=0, to=360, number_of_steps=360, command=self.update)
        self.sl_theta.set(0)
        self.sl_theta.pack(fill="x"); self.lbl_theta = ctk.CTkLabel(panel, text="0°")
        self.lbl_theta.pack()

        # Output Info
        self.res_frame = ctk.CTkFrame(panel)
        self.res_frame.pack(fill="x", pady=20)
        self.lbl_res_I = ctk.CTkLabel(self.res_frame, text="Intensitas Akhir (I) = 100.0 W/m²", font=("Arial", 14, "bold"))
        self.lbl_res_I.pack(pady=10)
        
        # Plot
        self.plot_container = self.add_plot_area()
        self.fig, self.ax, self.canvas = self.setup_matplotlib(self.plot_container)
        
        # Panduan
        theory = (
            "POLARISASI CAHAYA (HUKUM MALUS)\n\n"
            "1. Konsep Dasar:\n"
            "   Cahaya adalah gelombang transversal yang memiliki arah getar medan listrik.\n"
            "   Cahaya Alami (tak terpolarisasi) memiliki arah getar ke segala arah acak.\n\n"
            "2. Polarisator & Analisator:\n"
            "   • Polarisator: Filter pertama yang mengubah cahaya alami menjadi terpolarisasi linier.\n"
            "     Intensitas setelah polarisator (I₁) = 1/2 I₀ (untuk cahaya alami).\n"
            "   • Analisator: Filter kedua yang dapat diputar sudutnya (θ) terhadap sumbu transmisi polarisator.\n\n"
            "3. Hukum Malus:\n"
            "   Intensitas cahaya yang diteruskan oleh analisator (I₂) bergantung pada sudut θ:\n"
            "   I₂ = I₁ cos²θ\n"
            "   Jika I₁ adalah intensitas cahaya terpolarisasi yang masuk ke analisator.\n\n"
            "4. Hasil Eksperimen:\n"
            "   • Maksimum (I₂ = I₁) saat θ = 0° atau 180° (Sejajar).\n"
            "   • Minimum (I₂ = 0) saat θ = 90° atau 270° (Tegak lurus/Crossed Polarizers)."
        )

        tools = [
            ("Sumber Cahaya", "Lampu pijar atau Laser (sumber I₀)."),
            ("Filter Polarisator (P)", "Terpasang tetap (sudut 0°)."),
            ("Filter Analisator (A)", "Dapat diputar 0-360°."),
            ("Luxmeter / Sensor Cahaya", "Mengukur intensitas cahaya (W/m² atau Lux)."),
            ("Rel Optik", "Tempat meletakkan komponen sejajar.")
        ]

        steps = [
            "Nyalakan sumber cahaya dengan intensitas tertentu (I₀).",
            "Pasang Polarisator di depan sumber cahaya. Intensitas menjadi I₁.",
            "Pasang Analisator di belakang Polarisator.",
            "Putar Analisator (θ) mulai dari 0° hingga 360° dengan interval 10°.",
            "Amati perubahan terang-gelap cahaya pada layar atau sensor.",
            "Catat nilai intensitas (I) pada setiap sudut θ.",
            "Buat grafik hubungan I vs cos²θ. Seharusnya berupa garis lurus."
        ]
        
        self.set_guide_content(steps, tools, theory)
        
        # Setup Data Recording
        self.module_name = "Polarisasi Cahaya"
        self.setup_data_recording(panel, self.get_data)
        
        self.update()

    def get_data(self):
        I0 = self.sl_I0.get()
        theta = self.sl_theta.get()
        I = I0 * (np.cos(np.radians(theta))**2)
        return {
            "Intensitas Awal (I0)": I0,
            "Sudut Analisator (θ)": theta,
            "Intensitas Akhir (I)": round(I, 2),
            "cos^2(θ)": round(np.cos(np.radians(theta))**2, 3)
        }

    def update(self, _=None):
        I0 = self.sl_I0.get()
        theta_deg = self.sl_theta.get()
        theta_rad = np.radians(theta_deg)
        
        # Recalculate I
        I = I0 * (np.cos(theta_rad)**2)
        
        self.lbl_I0.configure(text=f"{int(I0)} W/m²")
        self.lbl_theta.configure(text=f"{int(theta_deg)}°")
        self.lbl_res_I.configure(text=f"Intensitas Akhir (I) = {I:.1f} W/m²")
        
        # Graphing
        self.ax.clear()
        
        # Plot Theoretical Curve
        angles = np.linspace(0, 360, 360)
        intensities = I0 * (np.cos(np.radians(angles))**2)
        self.ax.plot(angles, intensities, color='#00d2ff', linewidth=2, label='Teori Hukum Malus')
        
        # Plot Current Point
        self.ax.scatter([theta_deg], [I], color='red', s=100, zorder=5, label='Posisi Saat Ini')
        
        # Visualizing the Filters (Schematic)
        # Draw vector arrow representing polarization direction
        arrow_len = 20
        # P1 (Fixed Vertical)
        self.ax.arrow(50, 50, 0, arrow_len, head_width=5, color='white', alpha=0.5)
        self.ax.arrow(50, 50, 0, -arrow_len, head_width=5, color='white', alpha=0.5)
        self.ax.text(50, 20, "Polarisator\n(0°)", color='white', ha='center', fontsize=8)
        
        # P2 (Rotated)
        dx = arrow_len * np.sin(theta_rad)
        dy = arrow_len * np.cos(theta_rad)
        self.ax.arrow(150, 50, dx, dy, head_width=5, color='yellow', alpha=0.8)
        self.ax.arrow(150, 50, -dx, -dy, head_width=5, color='yellow', alpha=0.8)
        self.ax.text(150, 20, f"Analisator\n({int(theta_deg)}°)", color='yellow', ha='center', fontsize=8)

        # Settings
        self.ax.set_title(f"Grafik Intensitas vs Sudut Pemutar (I = I₀ cos²θ)", color='white')
        self.ax.set_xlabel("Sudut Analisator (θ)", color='white')
        self.ax.set_ylabel("Intensitas (I)", color='white')
        self.ax.set_xlim(0, 360)
        self.ax.set_ylim(-10, I0 + 20) # A bit of padding
        self.ax.grid(True, linestyle=':', alpha=0.3)
        self.ax.legend(facecolor='#2b2b2b', labelcolor='white')
        
        # Can we draw the actual visual brightness?
        # Maybe a rect with alpha
        brightness = I / 100 if I0 > 0 else 0
        rect = patches.Rectangle((250, 30), 50, 50, linewidth=1, edgecolor='white', facecolor='white', alpha=brightness)
        self.ax.add_patch(rect)
        self.ax.text(275, 20, "Output", color='white', ha='center')

        self.canvas.draw()


# ==========================================
# MODUL 5: DISPERSI PRISMA
# ==========================================
class DispersiFrame(BaseModuleFrame):
    def __init__(self, master):
        super().__init__(master, "Modul 5: Dispersi Cahaya pada Prisma")
        
        panel = self.add_control_panel()
        
        ctk.CTkLabel(panel, text="Sudut Pembias Prisma (β) [°]:").pack(anchor="w")
        self.sl_beta = ctk.CTkSlider(panel, from_=10, to=60, number_of_steps=50, command=self.update)
        self.sl_beta.set(45)
        self.sl_beta.pack(fill="x"); self.lbl_beta = ctk.CTkLabel(panel, text="45°")
        self.lbl_beta.pack()

        ctk.CTkLabel(panel, text="Sudut Datang (i) [°]:").pack(anchor="w", pady=10)
        self.sl_i = ctk.CTkSlider(panel, from_=0, to=90, number_of_steps=90, command=self.update)
        self.sl_i.set(45)
        self.sl_i.pack(fill="x"); self.lbl_i = ctk.CTkLabel(panel, text="45°")
        self.lbl_i.pack()
        
        ctk.CTkLabel(panel, text="Indeks Bias Kaca (n_avg):").pack(anchor="w", pady=10)
        self.sl_n = ctk.CTkSlider(panel, from_=1.4, to=1.8, number_of_steps=40, command=self.update) # type: ignore
        self.sl_n.set(1.5)
        self.sl_n.pack(fill="x"); self.lbl_n = ctk.CTkLabel(panel, text="1.50")
        self.lbl_n.pack()

        # Checkbox Dispersi
        self.check_dispersi = ctk.CTkCheckBox(panel, text="Tampilkan Spectrum (Dispersi)", command=self.update)
        self.check_dispersi.pack(pady=20, anchor="w")
        self.check_dispersi.select()

        # Output Info
        self.res_frame = ctk.CTkFrame(panel)
        self.res_frame.pack(fill="x", pady=10)
        self.lbl_dev = ctk.CTkLabel(self.res_frame, text="Sudut Deviasi (δ) = -°", font=("Arial", 12))
        self.lbl_dev.pack(pady=5)

        # Plot
        self.plot_container = self.add_plot_area()
        self.fig, self.ax, self.canvas = self.setup_matplotlib(self.plot_container)
        
        # Panduan
        theory = (
            "DISPERSI CAHAYA PADA PRISMA\n\n"
            "1. Pembiasan Prisma:\n"
            "   Cahaya putih terdiri dari berbagai panjang gelombang (polikromatik).\n"
            "   Indeks bias bahan (n) bergantung pada panjang gelombang (λ).\n"
            "   n_ungu > n_merah, sehingga sinar ungu dibelokkan lebih kuat daripada merah.\n\n"
            "2. Sudut Deviasi (δ):\n"
            "   Adalah sudut antara perpanjangan sinar datang mula-mula dengan sinar bias akhir.\n"
            "   δ = i₁ + r₂ - β\n"
            "   Dimana β adalah sudut pembias prisma.\n\n"
            "3. Deviasi Minimum (δ_min):\n"
            "   Terjadi saat i₁ = r₂, sehingga lintasan sinar simetris.\n"
            "   n = sin((δ_min + β)/2) / sin(β/2)\n\n"
            "4. Sudut Dispersi (φ):\n"
            "   Selisih sudut deviasi antara sinar Ungu dan Merah.\n"
            "   φ = δ_ungu - δ_merah = (n_ungu - n_merah) β (untuk sudut kecil)."
        )
        
        tools = [
            ("Prisma Segitiga Siku-siku / Sama Sisi", "Bahan kaca atau akrilik."),
            ("Sumber Cahaya Putih (Ray Box)", "Menghasilkan berkas sinar sejajar."),
            ("Kertas HVS Putih", "Sebagai layar atau alas jejak sinar."),
            ("Busur Derajat", "Mengukur sudut datang dan sudut deviasi.")
        ]
        
        steps = [
            "Letakkan prisma di atas kertas putih. Gambar kontur segitiga prisma.",
            "Nyalakan Ray Box, arahkan sinar putih ke salah satu sisi prisma dengan sudut datang (i).",
            "Amati sinar yang keluar dari sisi lain prisma. Apakah terjadi pelangi (dispersi)?",
            "Tandai jejak sinar datang dan sinar keluar dengan titik-titik.",
            "Tarik garis untuk menemukan sudut deviasi (δ).",
            "Ubah sudut datang (i) secara perlahan. Cari posisi di mana sudut deviasi paling kecil (Minimum).",
            "Hitung indeks bias prisma menggunakan rumus Deviasi Minimum."
        ]
        
        self.set_guide_content(steps, tools, theory)
        self.module_name = "Dispersi Prisma"
        self.setup_data_recording(panel, self.get_data)
        self.update()

    def get_data(self):
        return {
            "Sudut Prisma (β)": self.sl_beta.get(),
            "Sudut Datang (i)": self.sl_i.get(),
            "Indeks Bias (n)": round(self.sl_n.get(), 3),
            "Deviasi (δ)": self.current_dev
        }
        
    def solve_prism(self, n, beta_deg, i_deg):
        # Calculation for single ray through prism
        # 1. Air to Glass
        # sin(i) = n * sin(r1) -> r1 = arcsin(sin(i)/n)
        try:
            i_rad = np.radians(i_deg)
            beta_rad = np.radians(beta_deg)
            r1 = np.arcsin(np.sin(i_rad) / n)
            
            # Geometry inside: r1 + r2 = beta -> r2 = beta - r1
            r2 = beta_rad - r1
            
            # 2. Glass to Air
            # n * sin(r2) = sin(e) -> e = arcsin(n * sin(r2))
            val = n * np.sin(r2)
            if abs(val) > 1: return None, None # Total internal
            e = np.arcsin(val)
            
            # Deviation delta = i + e - beta
            delta = i_rad + e - beta_rad
            return np.degrees(delta), np.degrees(e)
            
        except:
            return None, None

    def update(self, _=None):
        beta = self.sl_beta.get()
        i_deg = self.sl_i.get()
        n_base = self.sl_n.get()
        
        self.lbl_beta.configure(text=f"{int(beta)}°")
        self.lbl_i.configure(text=f"{int(i_deg)}°")
        self.lbl_n.configure(text=f"{n_base:.2f}")
        
        self.ax.clear()

        # --- GEOMETRI PRISMA ---
        # Height of prism visualization
        H = 4 
        # Half angle
        beta_rad = np.radians(beta)
        # Width of base: tan(beta/2) = (W/2) / H => W = 2*H*tan(beta/2)
        # But usually Prism is equilateral-ish or Isosceles.
        # Let's fix the Apex at (0, 2).
        top_y = 2
        
        # Calculate vertices based on Beta
        # Left side angle from vertical is beta/2.
        # Slope of Left Face: dy/dx = tan(90 - beta/2) ?
        # No, normal to left face makes angle (180 - beta/2 + 90) = 270 - beta/2
        # Let's define vector for Left Face direction:
        # Down-Left vector: (-sin(beta/2), -cos(beta/2))
        
        side_len = 6
        dx = side_len * np.sin(beta_rad/2)
        dy = side_len * np.cos(beta_rad/2)
        
        A = np.array([0, top_y])
        B = np.array([-dx, top_y - dy])
        C = np.array([dx, top_y - dy])
        
        prism_poly = patches.Polygon([A, B, C], closed=True, color='cyan', alpha=0.15, edgecolor='white')
        self.ax.add_patch(prism_poly)
        
        # --- RAY TRACING ---
        # 1. Incident Ray
        # Target Point: Middle of Left Face AB
        P_in = (A + B) / 2
        
        # Normal vector at P_in (Left Face)
        # Face vector B-A = (-dx, -dy)
        # Normal is perpendicular (-dy, dx) -> pointing Left-Up?
        # Let's verify: Face slope is positive or negative?
        # A is (0,2), B is negative X, negative Y relative to A.
        # Vector AB is (-x, -y). Normal (-y, x) involves 90 deg rotation.
        # Wait, simple geometry: Normal angle relative to horizontal X-axis.
        # Left face angle with horizontal = (90 + beta/2).
        # Normal angle = (90 + beta/2) + 90 = 180 + beta/2. Or - (180 - (90+beta/2))?
        # Angle of Normal of Left Face = 180 - (90 - beta/2) = 90 + beta/2.
        theta_normal_1 = 180 - (90 - beta/2) # Pointing Left-Up
        theta_normal_1_rad = np.radians(theta_normal_1)
        
        # Draw Normal at P_in
        norm_len = 2
        # Normal for Left Face: points Left-Up
        # Face vector (-dx, -dy). Perpendicular is (-dy, dx).
        # We need normalized vector direction
        norm_v = np.array([-dy, dx])
        theta_norm_rad = np.arctan2(norm_v[1], norm_v[0])
        
        nx = norm_len * np.cos(theta_norm_rad)
        ny = norm_len * np.sin(theta_norm_rad)
        self.ax.plot([P_in[0], P_in[0]+nx], [P_in[1], P_in[1]+ny], 'w--', alpha=0.3, linewidth=1)
        
        # Incident Ray Angle
        # Ray direction = Norm_Angle - 180 + i
        ray_in_angle_rad = theta_norm_rad - np.pi + np.radians(i_deg)
        
        # Start point of ray (backwards 5 units)
        start_pt = P_in - 5 * np.array([np.cos(ray_in_angle_rad), np.sin(ray_in_angle_rad)])
        self.ax.plot([start_pt[0], P_in[0]], [start_pt[1], P_in[1]], 'r-', linewidth=2, label='Sinar Datang')
        
        # --- REFRACTION LOGIC ---
        
        def trace_ray(wave_color, n_val):
            try:
                # 1. Refraction at Face 1
                # Snell: sin(i) = n sin(r1)
                sin_r1 = np.sin(np.radians(i_deg)) / n_val
                if abs(sin_r1) > 1: return None # Impossible (n < 1?)
                r1_rad = np.arcsin(sin_r1)
                
                # Ray 2 Angle
                # Ray bends TOWARDS normal (entering glass).
                # New Angle relative to Normal is (180 - r1)? No.
                # Standard conversion: Ray 2 Angle = Ray 1 Angle - Deviation1 (i - r1)
                # Why minus? Ray 1 is flatter, Ray 2 is steeper (closer to normal).
                theta_ray_2 = ray_in_angle_rad - (np.radians(i_deg) - r1_rad)
                
                # Intersection with Face 2 (AC)
                # Face 2: Point A(0, top_y), C(dx, top_y - dy).
                m_ray = np.tan(theta_ray_2)
                
                # Face 2 Line Eq
                if abs(dx) < 1e-6: # Vertical face (unlikely here)
                     ix = 0; iy = m_ray*(0-P_in[0]) + P_in[1]
                else: 
                     slope_face = (C[1] - A[1]) / (C[0] - A[0])
                     # Intersect Lines
                     # y - P_in_y = m_ray(x - P_in_x)
                     # y - A_y = slope_face(x - A_x)
                     ix = (m_ray*P_in[0] - P_in[1] - slope_face*A[0] + A[1]) / (m_ray - slope_face)
                     iy = m_ray*(ix - P_in[0]) + P_in[1]
                
                P_out = np.array([ix, iy])
                
                # Draw Ray Inside
                self.ax.plot([P_in[0], P_out[0]], [P_in[1], P_out[1]], color=wave_color, alpha=0.8)
                
                # 2. Refraction at Face 2
                # Calculate internal incidence angle r2
                # Geometry: r2 = beta - r1
                r2_rad = np.radians(beta) - r1_rad
                
                # Snell 2: n sin(r2) = sin(e)
                sin_e = n_val * np.sin(r2_rad)
                
                if abs(sin_e) >= 1.0:
                    # TIR - Reflect inside
                    self.ax.plot([P_out[0]], [P_out[1]], 'rx') # Mark TIR
                    return None
                
                e_rad = np.arcsin(sin_e)
                
                # Ray 3 Angle
                # Deviation delta = i + e - beta
                delta_rad = np.radians(i_deg) + e_rad - np.radians(beta)
                theta_ray_3 = ray_in_angle_rad - delta_rad
                
                # Draw Ray 3
                end_pt = P_out + 5 * np.array([np.cos(theta_ray_3), np.sin(theta_ray_3)])
                self.ax.plot([P_out[0], end_pt[0]], [P_out[1], end_pt[1]], color=wave_color, alpha=0.8)
                
                return np.degrees(delta_rad)
                
            except Exception as ex:
                return None

        # Execute Ray Traces
        dev_val = 0
        if self.check_dispersi.get():
            # Red, Green, Blue
            trace_ray('red', n_base - 0.03)
            trace_ray('blue', n_base + 0.03)
            dev_val = trace_ray('green', n_base) # Use Green as avg
        else:
            dev_val = trace_ray('yellow', n_base)

        if dev_val:
            self.lbl_dev.configure(text=f"Sudut Deviasi (δ) ≈ {dev_val:.2f}°")
            self.current_dev = round(dev_val, 2)
        else:
             self.lbl_dev.configure(text="Total Internal Reflection!")
             self.current_dev = "TIR"

        self.ax.set_aspect('equal')
        self.ax.set_xlim(-6, 6)
        self.ax.set_ylim(-4, 4)
        self.ax.axis('off')
        self.canvas.draw()


# ==========================================
# MODUL 6: KISI DIFRAKSI
# ==========================================
class KisiDifraksiFrame(BaseModuleFrame):
    def __init__(self, master):
        super().__init__(master, "Modul 6: Kisi Difraksi (Spectroscopy)")
        
        panel = self.add_control_panel()
        
        ctk.CTkLabel(panel, text="Konstanta Kisi (N) [Garis/mm]:").pack(anchor="w")
        self.sl_N = ctk.CTkSlider(panel, from_=100, to=1000, number_of_steps=90, command=self.update)
        self.sl_N.set(300)
        self.sl_N.pack(fill="x"); self.lbl_N = ctk.CTkLabel(panel, text="300 garis/mm")
        self.lbl_N.pack()

        ctk.CTkLabel(panel, text="Orde Difraksi (m) Target:").pack(anchor="w", pady=10)
        self.sl_m = ctk.CTkSlider(panel, from_=1, to=3, number_of_steps=2, command=self.update)
        self.sl_m.set(1)
        self.sl_m.pack(fill="x"); self.lbl_m = ctk.CTkLabel(panel, text="Orde 1")
        self.lbl_m.pack()
        
        ctk.CTkLabel(panel, text="Panjang Gelombang (λ):").pack(anchor="w", pady=10)
        self.sl_wave = ctk.CTkSlider(panel, from_=380, to=750, command=self.update)
        self.sl_wave.set(532) # Green
        self.sl_wave.pack(fill="x"); self.lbl_wave = ctk.CTkLabel(panel, text="532 nm")
        self.lbl_wave.pack()

        # Output Info
        self.res_frame = ctk.CTkFrame(panel)
        self.res_frame.pack(fill="x", pady=20)
        self.lbl_angle = ctk.CTkLabel(self.res_frame, text="Sudut Deviasi (θ) = -°", font=("Arial", 12, "bold"))
        self.lbl_angle.pack(pady=5)
        self.lbl_d = ctk.CTkLabel(self.res_frame, text="d = - nm")
        self.lbl_d.pack()

        # Plot
        self.plot_container = self.add_plot_area()
        self.fig, self.ax, self.canvas = self.setup_matplotlib(self.plot_container)
        
        # Panduan
        theory = (
            "DIFRAKSI PADA KISI (DIFFRACTION GRATING)\n\n"
            "1. Definisi:\n"
            "   Kisi difraksi terdiri dari ribuan celah sempit yang sejajar.\n"
            "   Berfungsi memisahkan cahaya menjadi spektrum warna dengan resolusi tinggi.\n\n"
            "2. Rumus Kisi:\n"
            "   d sin θ = m λ\n"
            "   d = Lebar antar celah (1/N)\n"
            "   N = Konstanta kisi (garis/mm)\n"
            "   θ = Sudut deviasi orde ke-m\n"
            "   m = Orde difraksi (0, 1, 2, ...)\n"
            "   λ = Panjang gelombang cahaya\n\n"
            "3. Manfaat:\n"
            "   Digunakan dalam spektrometer untuk menentukan panjang gelombang sumber cahaya unknown."
        )
        
        tools = [
            ("Kisi Difraksi (100, 300, 600 garis/mm)", "Komponen utama."),
            ("Spectrometer Table", "Meja putar dengan skala sudut presisi."),
            ("Teleskop Pengamat", "Untuk melihat garis spektrum."),
            ("Lampu Spektral (Hg, Na, He)", "Sumber cahaya gas untuk dianalisis.")
        ]
        
        steps = [
            "Pasang kisi tegak lurus pada meja spektrometer.",
            "Arahkan teleskop ke posisi tegak lurus (Orde 0, putih/terang pusat).",
            "Putar teleskop ke kanan/kiri hingga menemukan garis warna terang pertama (Orde 1).",
            "Baca sudut θ pada skala nonius meja spektrometer.",
            "Gunakan rumus d sin θ = m λ untuk menghitung panjang gelombang.",
            "Ulangi untuk orde ke-2 jika masih terlihat."
        ]
        
        self.set_guide_content(steps, tools, theory)
        self.module_name = "Kisi Difraksi"
        self.setup_data_recording(panel, self.get_data)
        self.update()

    def get_data(self):
        N = self.sl_N.get()
        lam_nm = self.sl_wave.get()
        m = int(self.sl_m.get())
        d_nm = (1 / N) * 1e6 # mm to nm
        
        # Calculate theta
        try:
             # d sin theta = m lambda -> sin theta = m lambda / d
             val = (m * lam_nm) / d_nm
             if val <= 1:
                 theta = np.degrees(np.arcsin(val))
                 status = "Valid"
             else:
                 theta = 0
                 status = "Tidak Teramati (NA)"
        except:
             theta = 0
             status = "Error"
             
        return {
            "Konstanta Kisi (N)": int(N),
            "Panjang Gelombang (λ)": int(lam_nm),
            "Orde (m)": m,
            "Jarak Celah (d) [nm]": round(d_nm, 2),
            "Sudut (θ)": round(theta, 2) if isinstance(theta, float) else status
        }

    def update(self, _=None):
        N = self.sl_N.get()
        lam = self.sl_wave.get()
        m_target = int(self.sl_m.get())
        
        self.lbl_N.configure(text=f"{int(N)} garis/mm")
        self.lbl_wave.configure(text=f"{int(lam)} nm")
        self.lbl_m.configure(text=f"Orde {m_target}")
        
        # Physics
        d_mm = 1/N
        d_nm = d_mm * 1e6
        self.lbl_d.configure(text=f"Jarak celah (d) = {d_nm:.1f} nm")
        
        # Calculate Angles for m=0, 1, 2, 3
        valid_orders = []
        intensities = []
        angles = []
        
        # Sweep angles -90 to 90
        theta_range = np.linspace(-90, 90, 1000)
        # Intensity function approx for grating: I = I0 * (sin(N*gamma)/sin(gamma))^2
        # where gamma = (pi * d * sin(theta)) / lambda
        # Let's keep it simple: Just draw lines at calculated angles
        
        self.ax.clear()
        
        # Screen representation (Semi-circle or flat screen)
        # Let's draw radial lines from origin
        
        # Central Max
        self.ax.plot([0, 0], [0, 5], color='white', linewidth=3, alpha=0.9, label='Orde 0')
        
        found_target = False
        
        for m in range(1, 4):
            # sin theta = m * lambda / d
            val = (m * lam) / d_nm
            if abs(val) <= 1:
                deg = np.degrees(np.arcsin(val))
                
                # Get Color
                rgb = self.wavelength_to_rgb(lam)
                color_hex = f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
                
                # Draw Lines +m and -m
                len_line = 5
                
                # + side
                x = len_line * np.sin(np.radians(deg))
                y = len_line * np.cos(np.radians(deg))
                self.ax.plot([0, x], [0, y], color=color_hex, linewidth=2, label=f'Orde {m}')
                
                # - side
                self.ax.plot([0, -x], [0, y], color=color_hex, linewidth=2)
                
                if m == m_target:
                    found_target = True
                    self.lbl_angle.configure(text=f"Sudut Deviasi (θ_{m}) = {deg:.2f}°")
                    # Highlight arc
                    arc = patches.Arc((0,0), 3, 3, theta1=90-deg, theta2=90, color='yellow')
                    self.ax.add_patch(arc)
            else:
                if m == m_target:
                    self.lbl_angle.configure(text=f"Sudut Deviasi (θ_{m}) = Tidak Terlihat")

        # Draw Grating
        self.ax.hlines(0, -2, 2, color='gray', linewidth=5)
        self.ax.text(0, -0.5, "KISI DIFRAKSI", ha='center', color='gray')
        
        self.ax.set_xlim(-6, 6)
        self.ax.set_ylim(-1, 6)
        self.ax.set_aspect('equal')
        self.canvas.draw()
    
    def wavelength_to_rgb(self, wavelength):
        # ...reuse existing or simplify...
        return (255, 255, 0) # Fallback handled in logic above if method exist in app scope?
        # Actually wavelength_to_rgb is method of each class or App? 
        # It was defined in InterferensiFrame. Let's copy it to avoid error or make static.
        # Better: copy the helper method here.
        
        gamma = 0.8
        intensity_max = 255
        try:
            if 380 <= wavelength <= 440:
                attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
                R = (-(wavelength - 440) / (440 - 380)) * attenuation ** gamma; G = 0.0; B = (1.0) * attenuation ** gamma
            elif 440 <= wavelength <= 490:
                R = 0.0; G = ((wavelength - 440) / (490 - 440)) ** gamma; B = 1.0
            elif 490 <= wavelength <= 510:
                R = 0.0; G = 1.0; B = (-(wavelength - 510) / (510 - 490)) ** gamma
            elif 510 <= wavelength <= 580:
                R = ((wavelength - 510) / (580 - 510)) ** gamma; G = 1.0; B = 0.0
            elif 580 <= wavelength <= 645:
                R = 1.0; G = (-(wavelength - 645) / (645 - 580)) ** gamma; B = 0.0
            elif 645 <= wavelength <= 750:
                attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
                R = (1.0) * attenuation ** gamma; G = 0.0; B = 0.0
            else:
                R = 0.0; G = 0.0; B = 0.0
            R = int(R * intensity_max); G = int(G * intensity_max); B = int(B * intensity_max)
            return (R, G, B)
        except:
             return (255, 255, 255)


if __name__ == "__main__":
    app = VirtualLabOptikApp()
    app.mainloop()
