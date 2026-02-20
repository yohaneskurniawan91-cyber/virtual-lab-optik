import tkinter as tk
from tkinter import ttk, messagebox
import importlib
import importlib.util
import sys
import os
import math
import random
import time
from functools import partial
from virtual_lab_data_manager import DataManager, ScrollableFrame

# --- Internationalization / Bahasa ---
TRANSLATIONS = {
    "ID": {
        "app_title": "Virtual Laboratorium Fisika Modern",
        "header_title": "VIRTUAL LABORATORIUM FISIKA MODERN",
        "header_subtitle": "Eksperimen Interaktif Tingkat Lanjut | Pengembang: Yohanes Kurniawan",
        "home": "Beranda",
        "verify": "Verifikasi Teori",
        "footer_copy": "© 2026 Yohanes Kurniawan | Virtual Lab Fisika Modern v2.0",
        "exit": "KELUAR / EXIT",
        "exit_confirm": "Apakah Anda yakin ingin menutup aplikasi?",
        "exit_title": "Konfirmasi",
        "hero_title": "FISIKA\nMODERN",
        "hero_sub": "VIRTUAL DISCOVERY LABORATORY",
        "hero_desc": "Selamat datang di platform simulasi interaktif sains.\nVisualisasikan fenomena kuantum, atom, dan relativitas\nyang tidak kasat mata menjadi pengalaman nyata.",
        "dev_info": "Pengembang Virtual Lab :",
        "db_conf": "🔗 Konfigurasi Database",
        "db_test": "⚡ Test Koneksi",
        "dl_excel": "💾 Unduh File Excel",
        "open_sim": "Buka Simulasi  \u279C",
        "login_title": "Login Praktikan",
        "login_btn": "MASUK / LOGIN",
        "login_note": "*Data Anda akan direkam di setiap pengambilan data eksperimen.",
        "welcome": "Selamat Datang - Guest",
        "input_name": "Nama Lengkap:",
        "input_nim": "NIM / ID:",
        "input_class": "Kelas / Shift:",
        "login_subs": "Silakan Login untuk Memulai Praktikum",
        "verif_title": "Verifikasi & Validasi Model Fisika",
        "verif_sub": "Dokumentasi persamaan matematis dan metode verifikasi yang digunakan dalam simulasi.",
        "total_modules": "Total Modul",
        "var_desc": "Keterangan Variabel:",
        "method": "Metode Verifikasi",
        "const": "Konstanta",
        "lang_btn": "🌐 Bahasa: ID",
        "server_time": "Waktu Server"
    },
    "EN": {
        "app_title": "Modern Physics Virtual Laboratory",
        "header_title": "MODERN PHYSICS VIRTUAL LABORATORY",
        "header_subtitle": "Advanced Interactive Experiments | Developer: Yohanes Kurniawan",
        "home": "Home",
        "verify": "Theory Verification",
        "footer_copy": "© 2026 Yohanes Kurniawan | Modern Physics Virtual Lab v2.0",
        "exit": "EXIT APP",
        "exit_confirm": "Are you sure you want to close the application?",
        "exit_title": "Confirmation",
        "hero_title": "MODERN\nPHYSICS",
        "hero_sub": "VIRTUAL DISCOVERY LABORATORY",
        "hero_desc": "Welcome to the interactive science simulation platform.\nVisualize invisible quantum, atomic, and relativity\nphenomena into real experiences.",
        "dev_info": "Virtual Lab Developer :",
        "db_conf": "🔗 Database Config",
        "db_test": "⚡ Test Connection",
        "dl_excel": "💾 Download Excel",
        "open_sim": "Open Simulation  \u279C",
        "login_title": "Student Login",
        "login_btn": "ENTER / LOGIN",
        "login_note": "*Your data will be recorded for every experiment data collection.",
        "welcome": "Welcome - Guest",
        "input_name": "Full Name:",
        "input_nim": "Student ID:",
        "input_class": "Class / Shift:",
        "login_subs": "Please Login to Start Experiment",
        "verif_title": "Physics Model Verification & Validation",
        "verif_sub": "Documentation of mathematical equations and verification methods used in simulations.",
        "total_modules": "Total Modules",
        "var_desc": "Variable Description:",
        "method": "Verification Method",
        "const": "Constants",
        "lang_btn": "🌐 Language: EN",
        "server_time": "Server Time"
    }
}

MODULE_TRANSLATIONS = {
    "Konstanta Planck": "Planck's Constant",
    "Radiasi Benda Hitam": "Blackbody Radiation",
    "Efek Fotolistrik": "Photoelectric Effect",
    "Tetes Minyak Millikan": "Millikan Oil Drop",
    "Sifat Partikel Cahaya": "Particle Nature of Light",
    "Difraksi Celah Ganda": "Double Slit Diffraction",
    "Penyerapan Sinar-X": "X-Ray Absorption",
    "Resonansi Spin (ESR)": "Electron Spin Resonance",
    "Efek Hall (Hall Effect)": "Hall Effect",
    "Spektrum Atom": "Atomic Spectrum",
    "Kuantisasi Energi (Franck-Hertz)": "Energy Quantization"
}

# Daftar modul dan judul tab untuk Fisika Modern
LAB_MODULES = [
    ("konstanta planck.py", "Konstanta Planck"),
    ("Radiasi benda Hitam.py", "Radiasi Benda Hitam"),
    ("EFEK FOTOLISTRIK.py", "Efek Fotolistrik"),
    ("Hamburan Milikan.py", "Tetes Minyak Millikan"),
    ("Sifat cahaya.py", "Sifat Partikel Cahaya"),
    ("DIFRAKSI CELAH GANDA.py", "Difraksi Celah Ganda"),
    ("Sifat & Penyerapan Sinar-X.py", "Penyerapan Sinar-X"),
    ("RESONANSI SPIN ELEKTRON (ESR).py", "Resonansi Spin (ESR)"),
    ("Effect Hall.py", "Efek Hall (Hall Effect)"),
    ("Spektrum Atom.py", "Spektrum Atom"),
    ("Kuantisasi Energi Atom.py", "Kuantisasi Energi (Franck-Hertz)")
]

class VirtualLabFisikaModern:
    def __init__(self, root):
        self.root = root
        self.lang = "ID"  # Default Language
        self.check_student_identity()
        self.root.title(self.T("app_title"))
        
        # Responsive Layout Configuration
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Center the window
        width, height = 1366, 768
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(1024, 700)
        
        # Modern Color Palette (Darker, sleek)
        self.bg_color = "#2d3436"      # Dark Grey
        self.header_color = "#0984e3"  # Electronic Blue
        self.text_color = "#dfe6e9"    # Off-white
        self.accent_color = "#00cec9"  # Robin's Egg Blue
        self.footer_color = "#2d3436"
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure TFrame to match background
        self.style.configure("TFrame", background="#f5f6fa")
        
        # --- UI Containers ---
        self.header_frame = tk.Frame(root, bg=self.header_color)
        self.header_frame.pack(side="top", fill="x")

        self.nav_frame = tk.Frame(root, bg="#636e72")
        self.nav_frame.pack(side="top", fill="x")

        self.content_frame = tk.Frame(self.root, bg="#f5f6fa")
        self.content_frame.pack(side="top", fill="both", expand=True)
        # Ensure Grid expansion
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.footer_frame = tk.Frame(self.root, bg=self.footer_color)
        self.footer_frame.pack(side="bottom", fill="x")

        # Data & State
        self.frames = {} 
        self.buttons = {}
        self.lab_instances = {} 
        self.current_page = "Beranda"
        self.home_anim_running = True

        # Build Content
        self.create_header()
        self.create_home_tab()
        self.create_verification_tab()
        self.load_labs()
        self.create_navigation_buttons()
        # self.create_db_controls() # Moved to create_navigation_buttons
        self.create_footer()
        
        self.show_frame("Beranda")

    def T(self, key):
        """Helper for Translation"""
        return TRANSLATIONS[self.lang].get(key, key)

    def toggle_language(self):
        self.lang = "EN" if self.lang == "ID" else "ID"
        self.refresh_ui()
        # Propagate to modules
        for key, instance in self.lab_instances.items():
            if hasattr(instance, 'set_language'):
                try:
                    instance.set_language(self.lang)
                except Exception as e:
                    print(f"Error setting language for {key}: {e}")

    def refresh_ui(self):
        self.root.title(self.T("app_title"))
        self.create_header()
        self.create_footer()
        self.create_navigation_buttons()
        self.create_home_tab()
        self.create_verification_tab()
        # Refresh current page view
        self.show_frame(self.current_page)

    def create_content_container(self):
        # Deprecated: Merged into __init__ for better references
        pass

    def check_student_identity(self):
        # Startup Identity Check
        # Strategy: Always show LOGIN screen. 
        # If previous profile exists, autofill it but allow edits.
        self.root.withdraw() # Hide main app
        self.ask_identity_dialog()
            
    def ask_identity_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Login Praktikan")
        dialog.geometry("450x400")
        dialog.configure(bg="#f5f6fa")
        
        # Handle Closure (X button) to exit App
        def on_close():
            self.root.destroy()
            sys.exit()
        dialog.protocol("WM_DELETE_WINDOW", on_close)

        # Header
        tk.Label(dialog, text=self.T("header_title"), font=("Arial", 16, "bold"), bg="#f5f6fa", fg="#0984e3").pack(pady=(20,5))
        tk.Label(dialog, text=self.T("login_subs"), font=("Arial", 10), bg="#f5f6fa", fg="#636e72").pack(pady=(0,15))
        
        # Form Frame
        frm = tk.Frame(dialog, padx=30, pady=20, bg="white", relief="raised", bd=1)
        frm.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(frm, text=self.T("input_name"), bg="white", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5,0))
        e_nama = tk.Entry(frm, width=40, font=("Arial", 11), bg="#f1f2f6")
        e_nama.pack(pady=5)
        
        tk.Label(frm, text=self.T("input_nim"), bg="white", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10,0))
        e_nim = tk.Entry(frm, width=40, font=("Arial", 11), bg="#f1f2f6")
        e_nim.pack(pady=5)
        
        tk.Label(frm, text=self.T("input_class"), bg="white", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10,0))
        e_kelas = tk.Entry(frm, width=40, font=("Arial", 11), bg="#f1f2f6")
        e_kelas.pack(pady=5)
        
        # Autofill if profile exists
        profile = DataManager.get_profile()
        if profile:
            e_nama.insert(0, profile.get("nama", ""))
            e_nim.insert(0, profile.get("nim", ""))
            e_kelas.insert(0, profile.get("kelas", ""))
        
        def login():
            nama = e_nama.get().strip()
            nim = e_nim.get().strip()
            kelas = e_kelas.get().strip()
            
            if not nama or not nim:
                messagebox.showerror("Login Gagal", "Nama dan NIM wajib diisi!", parent=dialog)
                return
                
            # Save new identity (overwriting previous if any)
            saved = DataManager.save_profile(nama, nim, kelas)
            if saved:
                dialog.destroy()
                self.root.deiconify() # Enter Main App
            else:
                messagebox.showerror("Error", "Gagal menyimpan profil lokal.", parent=dialog)
            
        tk.Button(dialog, text=self.T("login_btn"), bg="#0984e3", fg="black", highlightbackground="#0984e3", font=("Arial", 11, "bold"), 
                  width=30, pady=8, command=login).pack(pady=20)
        
        tk.Label(dialog, text=self.T("login_note"), 
                 font=("Arial", 8, "italic"), bg="#f5f6fa", fg="gray").pack(side="bottom", pady=10)
        
        # Wait window
        self.root.wait_window(dialog)

    def create_header(self):
        # Clear existing
        for widget in self.header_frame.winfo_children():
            widget.destroy()
            
        frame = tk.Frame(self.header_frame, bg=self.header_color, pady=20)
        frame.pack(side="top", fill="x")
        
        # Language Toggle (Top Right) -- Professional Touch
        # Fixed: High contrast colors (White button with Blue text) for readability
        lang_btn = tk.Button(frame, text=self.T("lang_btn"), font=("Arial", 9, "bold"),
                             bg="white", fg="#0984e3", 
                             highlightbackground="white", # Critical for macOS bg color
                             activebackground="#dfe6e9", activeforeground="#0984e3",
                             relief="flat", bd=0, command=self.toggle_language)
        lang_btn.place(relx=0.98, rely=0.1, anchor="ne")

        icon = "\U0000269B"  # Atom symbol
        
        tk.Label(frame, text=f"{icon}  {self.T('header_title')}", 
                 font=("Helvetica", 24, "bold"), fg="#ffffff", bg=self.header_color,
                 wraplength=1200, justify="center").pack(pady=(0, 5))
                 
        tk.Label(frame, text=self.T("header_subtitle"), 
                 font=("Helvetica", 14), fg="#dfe6e9", bg=self.header_color).pack()

    def create_footer(self):
        # Clear existing
        for widget in self.footer_frame.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.footer_frame, bg=self.footer_color, pady=8, padx=20)
        frame.pack(side="bottom", fill="x")
        
        # Copyright
        tk.Label(frame, text=self.T("footer_copy"), 
                 font=("Arial", 9), fg="#b2bec3", bg=self.footer_color).pack(side="left")

        # Clock
        self.lbl_clock = tk.Label(frame, text="", font=("Courier New", 10, "bold"), fg="#00cec9", bg=self.footer_color)
        self.lbl_clock.pack(side="left", padx=20)
        self.update_clock()
        
        # Exit Button
        btn_exit = tk.Button(frame, text=self.T("exit"), font=("Arial", 9, "bold"),
                            bg="#d63031", fg="white", activebackground="#fab1a0",
                            relief="flat", padx=10, command=self.confirm_exit)
        btn_exit.pack(side="right")

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        if hasattr(self, 'lbl_clock') and self.lbl_clock.winfo_exists():
            self.lbl_clock.config(text=f"{self.T('server_time')}: {now}")
        self.root.after(1000, self.update_clock)

    def confirm_exit(self):
        if messagebox.askyesno(self.T("exit_title"), self.T("exit_confirm")):
            self.root.destroy()
            sys.exit()

    def create_navigation_buttons(self):
        # Clear existing
        for widget in self.nav_frame.winfo_children():
            widget.destroy()
            
        # Define Layout Groups
        row1_target = ["Beranda", "Verifikasi Teori", "Spektrum Atom", "Kuantisasi Energi (Franck-Hertz)", "Sifat Partikel Cahaya", "Efek Fotolistrik", "Radiasi Benda Hitam"]
        
        # Organize items
        all_titles = ["Beranda", "Verifikasi Teori"] + [title for _, title in LAB_MODULES]
        
        # Row 1 items (preserving target order, if available)
        row1_items = [t for t in row1_target if t in all_titles]
        
        # Row 2 items (The rest, preserving LAB_MODULES order)
        row2_items = [t for t in all_titles if t not in row1_items]
        
        # Use subframes for independent grid layouts
        frame_row1 = tk.Frame(self.nav_frame, bg="#636e72")
        frame_row1.pack(side="top", fill="x")
        
        frame_row2 = tk.Frame(self.nav_frame, bg="#636e72")
        frame_row2.pack(side="top", fill="x")
        
        self.buttons = {} # Reset buttons map

        # Helper to create buttons
        def add_btn(parent, key, col, font_size=12):
            # Resolve Display Text
            if key == "Beranda":
                display_text = self.T("home")
            elif key == "Verifikasi Teori":
                display_text = self.T("verify")
            else:
                display_text = key # Default fallback
                if self.lang == "EN" and key in MODULE_TRANSLATIONS:
                    display_text = MODULE_TRANSLATIONS[key]
            
            parent.grid_columnconfigure(col, weight=1)
            btn = tk.Button(parent, text=display_text, font=("Arial", font_size, "bold"), 
                            bg="white", fg="black", highlightbackground="white",
                            activebackground=self.accent_color, activeforeground="black",
                            relief="flat", padx=10, pady=8,
                            command=partial(self.show_frame, key))
            btn.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
            self.buttons[key] = btn # Store by Logic Key (ID)

        # Build Row 1
        for i, text in enumerate(row1_items):
            add_btn(frame_row1, text, i, 12)
            
        # Build Row 2
        for i, text in enumerate(row2_items):
            add_btn(frame_row2, text, i, 11) # Slightly smaller font for more items

        # Re-add DB controls
        self.create_db_controls()

    def create_db_controls(self):
        # Frame for Data Controls (Integrated into Nav Frame)
        control_frame = tk.Frame(self.nav_frame, bg="#2d3436", pady=5)
        control_frame.pack(side="top", fill="x")
        
        # Center container
        container = tk.Frame(control_frame, bg="#2d3436")
        container.pack(anchor="center")
        
        # Updated style for better readability on macOS (White button with black text)
        style = {"font":("Arial", 10, "bold"), "bg":"#ffffff", "fg":"#2d3436", 
                 "highlightbackground":"#ffffff", "activeforeground":"#2d3436",
                 "relief":"flat", "padx":15, "pady":5, "activebackground":"#00cec9"}
        
        btn_conf = tk.Button(container, text=self.T("db_conf"), command=self.open_db_settings, **style)
        btn_conf.pack(side="left", padx=5)
        
        btn_test = tk.Button(container, text=self.T("db_test"), command=self.test_db_connection, **style)
        btn_test.pack(side="left", padx=5)

        btn_excel = tk.Button(container, text=self.T("dl_excel"), command=self.handle_dl_excel, **style)
        btn_excel.pack(side="left", padx=5)

    def open_db_settings(self):
        top = tk.Toplevel(self.root)
        top.title(self.T("db_conf"))
        top.geometry("600x250")
        top.configure(bg="#2d3436")
        
        tk.Label(top, text="Link Database / API Endpoint:", font=("Arial", 12, "bold"), fg="white", bg="#2d3436").pack(pady=(20,5))
        tk.Label(top, text="(Contoh: https://script.google.com/... atau http://localhost:5000/api/save)", 
                 font=("Arial", 9), fg="#b2bec3", bg="#2d3436").pack(pady=(0,5))
        
        current_conf = DataManager.load_config()
        entry_link = tk.Entry(top, width=60, font=("Arial", 11))
        entry_link.insert(0, current_conf.get("db_link", ""))
        entry_link.pack(pady=5)
        
        def save():
            link = entry_link.get()
            success, msg = DataManager.save_config(link)
            if success:
                messagebox.showinfo("Info", msg)
                top.destroy()
            else:
                messagebox.showerror("Error", msg)
            
        tk.Button(top, text="Simpan Konfigurasi", command=save, bg="#00cec9", fg="black", highlightbackground="#00cec9", font=("Arial", 10, "bold"), padx=10, pady=5).pack(pady=15)

    def test_db_connection(self):
        conf = DataManager.load_config()
        link = conf.get("db_link", "")
        success, msg = DataManager.test_connection(link)
        if success:
            messagebox.showinfo("Sukses", msg)
        else:
            messagebox.showerror("Gagal", msg)

    def get_current_data(self):
        if self.current_page == "Beranda":
            return None
        
        instance = self.lab_instances.get(self.current_page)
        # Check if instance has get_data method
        if instance and hasattr(instance, 'get_data'):
            return instance.get_data()
        # Fallback: check if instance has 'data_points' attribute directly
        if instance and hasattr(instance, 'data_points'):
             return instance.data_points
        return None

    def handle_dl_excel(self):
        data = self.get_current_data()
        if not data:
            messagebox.showwarning("Peringatan", f"Modul '{self.current_page}' belum memiliki data untuk diekspor.")
            return
        
        success, msg = DataManager.export_excel(data)
        if success:
            messagebox.showinfo("Sukses", msg)
        else:
            messagebox.showerror("Error", msg)

    def handle_save_db(self):
        data = self.get_current_data()
        if not data:
            messagebox.showwarning("Peringatan", f"Modul '{self.current_page}' belum memiliki data untuk disimpan.")
            return

        conf = DataManager.load_config()
        link = conf.get("db_link", "")
        
        if not link:
            messagebox.showwarning("Peringatan", "Link database belum disetting!")
            self.open_db_settings()
            return
            
        success, msg = DataManager.send_to_database(data, link)
        if success:
            messagebox.showinfo("Sukses", msg)
        else:
            messagebox.showerror("Gagal", msg)

    def show_frame(self, page_name):
        # Update Window Title
        self.root.title(f"Virtual Lab Fisika Modern - {page_name}")
        
        # STOP Animation on previous page if applicable
        if self.current_page == "Beranda":
            self.home_anim_running = False
            
        if self.current_page in self.lab_instances:
            inst = self.lab_instances[self.current_page]
            if hasattr(inst, "stop_animation"):
                inst.stop_animation()

        # Hide all frames first to ensure content frame resizes correctly
        for name, frame in self.frames.items():
            frame.grid_remove()
            
        if page_name in self.frames:
            self.frames[page_name].grid(row=0, column=0, sticky="nsew")
            self.current_page = page_name
            
            # START Animation on new page if applicable
            if page_name == "Beranda":
                self.home_anim_running = True
                self.animate_home_atom()
                
            if page_name in self.lab_instances:
                inst = self.lab_instances[page_name]
                if hasattr(inst, "start_animation"):
                    inst.start_animation()
            
        for name, btn in self.buttons.items():
            btn.config(bg="white", highlightbackground="white", fg="black")
            
        if page_name in self.buttons:
             self.buttons[page_name].config(bg=self.accent_color, highlightbackground=self.accent_color, fg="black")

    def create_home_tab(self):
        home = self.frames.get("Beranda")
        if not home:
            home = ttk.Frame(self.content_frame)
            home.grid(row=0, column=0, sticky="nsew")
            self.frames["Beranda"] = home
        else:
            # Clear for refresh
            for w in home.winfo_children(): w.destroy()
        
        # --- Developer Info (Bottom) ---
        info_frame = tk.Frame(home, bg="#f6e58d", bd=2, relief="groove")
        info_frame.pack(side="bottom", pady=(0,18), padx=30, fill="x")
        
        dev_labels = [
            (self.T("dev_info"), 13, "bold"),
            ("Yohanes Kurniawan", 14, "bold"),
            ("S3 Teknologi Pembelajaran Universitas Negeri Malang", 12, "normal"),
            ("S2 Pendidikan Fisika Universitas Negeri Yogyakarta", 12, "normal"),
            ("S1 Pendidikan Fisika Universitas Nusa Cendana", 12, "normal"),
            ("Asal Lembata - Nusa Tenggara Timur", 12, "normal"),
            ("Dosen Unika Santu Paulus Ruteng", 12, "normal")
        ]
        
        for i, (txt, sz, wt) in enumerate(dev_labels):
            p = (10, 0) if i == 0 else (0, 10) if i == len(dev_labels)-1 else (0, 0)
            indent = 16 if i == 0 else 32
            tk.Label(info_frame, text=txt, font=("Arial", sz, wt), 
                     fg="#222", bg="#f6e58d").pack(anchor="w", padx=indent, pady=p)

        # --- Hero Section (Top - Animated) ---
        hero_frame = tk.Frame(home, bg="#2d3436") 
        hero_frame.pack(side="top", fill="both", expand=True)

        # Left: Typography & Intro
        left_hero = tk.Frame(hero_frame, bg="#2d3436", width=400)
        left_hero.pack(side="left", fill="y", padx=50, pady=50)
        
        # Fancy Title
        tk.Label(left_hero, text=self.T("hero_title"), font=("Tw Cen MT", 48, "bold"), 
                 fg="#00cec9", bg="#2d3436", justify="left").pack(anchor="w")
                 
        tk.Label(left_hero, text=self.T("hero_sub"), font=("Helvetica", 14, "bold"), 
                 fg="#74b9ff", bg="#2d3436", justify="left").pack(anchor="w", pady=(5, 20))
        
        tk.Label(left_hero, text=self.T("hero_desc"), font=("Arial", 12), fg="#dfe6e9", bg="#2d3436", justify="left").pack(anchor="w")

        # Right: Atom Animation Canvas
        self.home_canvas = tk.Canvas(hero_frame, bg="#2d3436", highlightthickness=0)
        self.home_canvas.pack(side="right", fill="both", expand=True)
        
        # Initialize Electron Particles for Animation
        self.electrons = []
        colors = ["#00cec9", "#0984e3", "#fdcb6e", "#e17055", "#6c5ce7"]
        for i in range(5):
            self.electrons.append({
                "rx": random.randint(100, 200), # X radius
                "ry": random.randint(40, 90),   # Y radius
                "speed": random.uniform(0.03, 0.08) * (1 if i%2==0 else -1),
                "angle": random.uniform(0, 6.28),
                "tilt": random.uniform(0, 3.14), # Orbital tilt
                "color": colors[i % len(colors)]
            })

        self.animate_home_atom()

    def animate_home_atom(self):
        # Stop animation if canvas is destroyed (tab switch/close)
        if not self.home_anim_running: return
        try:
            if not self.home_canvas.winfo_exists(): return
        except: return

        w = self.home_canvas.winfo_width()
        h = self.home_canvas.winfo_height()
        # Default if not packed yet
        if w < 10: w=500; h=400 
        
        cx, cy = w/2, h/2
        self.home_canvas.delete("all")
        
        # 1. Draw "Quantum Cloud" Background (Subtle noise)
        for _ in range(20):
            nx = random.randint(0, w)
            ny = random.randint(0, h)
            self.home_canvas.create_oval(nx, ny, nx+2, ny+2, fill="#636e72", outline="")

        # 2. Draw Nucleus (Pulsing Glow)
        # import time (Removed: Moved to top-level)
        t = time.time()
        pulse = math.sin(t*3) * 3
        
        # Glow
        self.home_canvas.create_oval(cx-25-pulse, cy-25-pulse, cx+25+pulse, cy+25+pulse, 
                                     fill="#d63031", outline="", stipple="gray50") # Fake transparency
        # Core
        self.home_canvas.create_oval(cx-15, cy-15, cx+15, cy+15, fill="#ff7675", outline="white", width=2)
        
        # 3. Draw Orbiting Electrons
        for e in self.electrons:
            e["angle"] += e["speed"]
            
            # 3D Orbit Logic
            # Base ellipse
            raw_x = e["rx"] * math.cos(e["angle"])
            raw_y = e["ry"] * math.sin(e["angle"])
            
            # Rotation Matrix for Tilt
            rot_x = raw_x * math.cos(e["tilt"]) - raw_y * math.sin(e["tilt"])
            rot_y = raw_x * math.sin(e["tilt"]) + raw_y * math.cos(e["tilt"])
            
            px, py = cx + rot_x, cy + rot_y
            
            # Draw Trail (Comet tail effect simply by existing line is hard, just drawing particle)
            self.home_canvas.create_oval(px-5, py-5, px+5, py+5, fill=e["color"], outline="white", width=1)
            
            # Draw Orbital Path (Static Ellipse approximation is hard with tilt, skip for clean look)
            
        self.root.after(20, self.animate_home_atom)

    def create_verification_tab(self):
        tab_frame = self.frames.get("Verifikasi Teori")
        if not tab_frame:
            # Use a container to hold the scrollable frame
            tab_frame = tk.Frame(self.content_frame, bg="#f5f6fa")
            tab_frame.grid(row=0, column=0, sticky="nsew")
            self.frames["Verifikasi Teori"] = tab_frame
        else:
            for w in tab_frame.winfo_children(): w.destroy()

        # Header Fixed
        header = tk.Frame(tab_frame, bg="#dfe6e9", pady=25, padx=30)
        header.pack(fill="x")
        
        title_frame = tk.Frame(header, bg="#dfe6e9")
        title_frame.pack(side="left")
        
        tk.Label(title_frame, text=self.T("verif_title"), 
                 font=("Helvetica", 28, "bold"), bg="#dfe6e9", fg="#2d3436").pack(anchor="w")
        tk.Label(title_frame, text=self.T("verif_sub"), 
                 font=("Arial", 12), bg="#dfe6e9", fg="#636e72").pack(anchor="w", pady=(5,0))
        
        # Legend/Stats
        stats_frame = tk.Frame(header, bg="#dfe6e9")
        stats_frame.pack(side="right")
        tk.Label(stats_frame, text=self.T("total_modules"), font=("Arial", 10, "bold"), bg="#dfe6e9", fg="gray").pack()
        tk.Label(stats_frame, text="11", font=("Helvetica", 20, "bold"), bg="#dfe6e9", fg="#0984e3").pack()

        # Content - Scrollable
        scroll_wrapper = ScrollableFrame(tab_frame, bg="#f5f6fa")
        scroll_wrapper.pack(fill="both", expand=True, padx=30, pady=20)
        content_area = scroll_wrapper.scrollable_frame

        # Define data structure with categories/themes
        # Theme Colors: Quantum=#0984e3 (Blue), Atomic=#6c5ce7 (Purple), Waves=#e17055 (Orange), EM=#00b894 (Green)
        
        verification_data = [
            {
                "category": "Kuantum",
                "color": "#0984e3",
                "modul": "Efek Fotolistrik",
                "target": "Efek Fotolistrik",
                "law": "Emisi Fotoelektron & Kuantum Cahaya",
                "eq": "Ek_max = hf - Φ",
                "desc": "Visualisasi interaksi foton-elektron pada permukaan logam. Membuktikan bahwa energi kinetik elektron bergantung pada frekuensi, bukan intensitas cahaya, sesuai postulat Einstein.",
                "vars": [
                    ("Ek_max", "Energi Kinetik Maksimum (J)"),
                    ("h", "Konstanta Planck (6.626e-34 J.s)"),
                    ("f", "Frekuensi Cahaya (Hz)"),
                    ("Φ", "Fungsi Kerja Logam (J)")
                ],
                "const": "c = 3e8 m/s, e = 1.6e-19 C, me = 9.1e-31 kg",
                "logic": "Calculated by computing stopping potential (Vs) for variable frequency.",
                "status": "Terverifikasi"
            },
            {
                "category": "Kuantum",
                "color": "#0984e3",
                "modul": "Radiasi Benda Hitam",
                "target": "Radiasi Benda Hitam",
                "law": "Hukum Radiasi Termal (Planck, Wien, Stefan-Boltzmann)",
                "eq": "λ_max T = b  ;  I(λ,T) = (2hc²/λ⁵) / (e^(hc/λkT) - 1)",
                "desc": "Simulasi spektrum radiasi elektromagnetik dari rongga benda hitam ideal sebagai fungsi temperatur. Membuktikan pergeseran puncak intensitas (Wien) dan total emisi daya (Stefan-Boltzmann).",
                "vars": [
                    ("λ_max", "Panjang gelombang puncak (m)"),
                    ("T", "Suhu Mutlak (K)"),
                    ("b", "Konstanta Wien (2.898e-3 m.K)"),
                    ("k", "Konstanta Boltzmann")
                ],
                "const": "h = 6.626e-34 Js, k = 1.38e-23 J/K",
                "logic": "Curve rendering using Planck's Distribution Formula.",
                "status": "Terverifikasi"
            },
            {
                "category": "Kuantum",
                "color": "#0984e3",
                "modul": "Konstanta Planck",
                "target": "Konstanta Planck", 
                "law": "Hukum Kuantisasi Energi (Metode LED)",
                "eq": "V_th = (h/e)f - (Φ/e)",
                "desc": "Validasi eksperimental konstanta fundamental Planck (h) menggunakan metode tegangan nyala (turn-on voltage) pada serangkaian LED monokromatik.",
                "vars": [
                    ("V_th", "Tegangan Nyala / Threshold (Volt)"),
                    ("h/e", "Gradien Grafik V vs f"),
                    ("e", "Muatan elementer (C)"),
                    ("Φ/e", "Fungsi Kerja Semikonduktor")
                ],
                "const": "e = 1.6e-19 C",
                "logic": "Linear Regression of V_th vs f (Slope Analysis).",
                "status": "Terverifikasi"
            },
            {
                "category": "Kuantum",
                "color": "#0984e3",
                "modul": "Sifat Partikel Cahaya",
                "target": "Sifat Partikel Cahaya",
                "law": "Dualisme Gelombang-Partikel",
                "eq": "p = E/c = h/λ",
                "desc": "Penelusuran sifat diskrit cahaya melalui eksperimen interferensi foton tunggal, menunjukkan transisi perilaku dari partikel ke pola gelombang statistik.",
                "vars": [
                    ("p", "Momentum Foton (kg m/s)"),
                    ("E", "Energi Foton (J)"),
                    ("c", "Kecepatan Cahaya (3e8 m/s)"),
                    ("λ", "Panjang Gelombang (m)")
                ],
                "const": "c = 3e8 m/s, h = 6.626e-34 Js",
                "logic": "Momentum conservation in photon-electron collision.",
                "status": "Terverifikasi"
            },
            {
                "category": "Atom",
                "color": "#6c5ce7",
                "modul": "Spektrum Atom & Model Bohr",
                "target": "Spektrum Atom",
                "law": "Transisi Kuantum & Deret Spektral Balmer",
                "eq": "1/λ = R_H (1/n_f² - 1/n_i²)",
                "desc": "Analisis sidik jari spektral atom Hidrogen. Mengamati garis emisi diskrit yang dihasilkan relaksasi elektron antar tingkat energi utama.",
                "vars": [
                    ("R_H", "Konstanta Rydberg (1.097e7 /m)"),
                    ("n_i, n_f", "Bilangan Kuantum Utama"),
                    ("λ", "Panjang Gelombang Emisi")
                ],
                "const": "R_H = 1.097e7 m^-1",
                "logic": "Discrete energy level transitions simulation.",
                "status": "Terverifikasi"
            },
            {
                "category": "Atom",
                "color": "#6c5ce7",
                "modul": "Kuantisasi Energi (Franck-Hertz)",
                "target": "Kuantisasi Energi (Franck-Hertz)", 
                "law": "Tumbukan Inelastis & Tingkat Energi Diskrit",
                "eq": "ΔE = E_kinetik - E_eksitasi",
                "desc": "Bukti eksperimental struktur kulit energi atom. Mengamati penurunan arus periodik akibat transfer energi kinetik elektron ke atom Merkuri pada nilai kritis.",
                "vars": [
                    ("V_acc", "Tegangan Pemercepat"),
                    ("I", "Arus Kolektor"),
                    ("E_eks", "Energi Eksitasi (~4.9 eV)")
                ],
                "const": "Hg Excitation Energy ~ 4.9 eV",
                "logic": "Periodic current drop simulation at V = n * V_exc.",
                "status": "Terverifikasi"
            },
            {
                 "category": "Atom",
                 "color": "#6c5ce7",
                 "modul": "Sifat & Penyerapan Sinar-X",
                 "target": "Penyerapan Sinar-X",
                 "law": "Hukum Beer-Lambert (Atenuasi Radiasi)",
                 "eq": "I = I₀ e^(-μx)",
                 "desc": "Studi interaksi radiasi energi tinggi dengan materi, mengukur koefisien atenuasi linear dan ketebalan paruh (HVL) berbagai material penyerap.",
                 "vars": [
                     ("I, I₀", "Intensitas Akhir & Awal"),
                     ("μ", "Koefisien Atenuasi Linear (/cm)"),
                     ("x", "Ketebalan Absorber (cm)")
                 ],
                 "const": "N/A (Material dependent)",
                 "logic": "Exponential decay calculation of intensity.",
                 "status": "Terverifikasi"
            },
            {
                 "category": "Atom",
                 "color": "#6c5ce7",
                 "modul": "Resonansi Spin Elektron (ESR)",
                 "target": "Resonansi Spin (ESR)", 
                 "law": "Efek Zeeman & Resonansi Magnetik",
                 "eq": "hν = g μ_B B_res",
                 "desc": "Spektroskopi absorpsi energi gelombang mikro yang menginduksi transisi spin elektron tak berpasangan di bawah pengaruh medan magnet eksternal.",
                 "vars": [
                     ("g", "Faktor Lande g"),
                     ("μ_B", "Magneton Bohr"),
                     ("B_res", "Medan Magnet Resonansi (Tesla)"),
                     ("ν", "Frekuensi RF (Hz)")
                 ],
                 "const": "g ~ 2.0023, μ_B = 9.274e-24 J/T",
                 "logic": "Matching RF frequency to Larmor frequency.",
                 "status": "Terverifikasi"
            },
            {
                 "category": "Elektromagnetik",
                 "color": "#00b894",
                 "modul": "Tetes Minyak Millikan",
                 "target": "Tetes Minyak Millikan",
                 "law": "Kuantisasi Muatan Listrik",
                 "eq": "q = (mg d) / V (saat diam)",
                 "desc": "Eksperimen keseimbangan gaya (listrik vs gravitasi) pada mikrosfer minyak bermuatan untuk menentukan muatan elementer elektron (e).",
                 "vars": [
                     ("q", "Muatan Tetesan (C)"),
                     ("m", "Massa Tetesan (kg)"),
                     ("V/d", "Kuat Medan Listrik E"),
                     ("v_term", "Kecepatan Terminal")
                 ],
                 "const": "g = 9.8 m/s^2, ρ_oil = 900 kg/m^3",
                 "logic": "Forces balance (Fg = Fe) and Stokes Law application.",
                 "status": "Terverifikasi"
            },
            {
                 "category": "Elektromagnetik",
                 "color": "#00b894",
                 "modul": "Efek Hall",
                 "target": "Efek Hall (Hall Effect)",
                 "law": "Gaya Lorentz pada Pembawa Muatan",
                 "eq": "V_H = (I B) / (n e d)",
                 "desc": "Pengukuran tegangan transversal pada konduktor berarus dalam medan magnet untuk menentukan densitas, mobilitas, dan tipe pembawa muatan (tipe-n/p).",
                 "vars": [
                     ("V_H", "Tegangan Hall (V)"),
                     ("n", "Konsentrasi Pembawa Muatan"),
                     ("d", "Tebal Lempeng (m)"),
                     ("R_H", "Koefisien Hall")
                 ],
                 "const": "e = 1.6e-19 C",
                 "logic": "Calculation of Hall Voltage from Lorentz Force.",
                 "status": "Terverifikasi"
            },
            {
                 "category": "Gelombang",
                 "color": "#e17055",
                 "modul": "Difraksi Celah Ganda",
                 "target": "Difraksi Celah Ganda", 
                 "law": "Interferensi & Difraksi Cahaya",
                 "eq": "d sin(θ) = nλ (Terang)",
                 "desc": "Pola gelap terang yang dihasilkan oleh superposisi gelombang cahaya yang melewati dua celah sempit.",
                 "vars": [
                     ("d", "Jarak antar celah (m)"),
                     ("θ", "Sudut deviasi"),
                     ("n", "Orde interferensi (0,1,2..)"),
                     ("λ", "Panjang Gelombang (m)")
                 ],
                 "const": "c = 3e8 m/s",
                 "logic": "Superposition principle and path difference calculation.",
                 "status": "Terverifikasi"
            }
        ]

        # Helper to render cards
        for item in verification_data:
            # Main Card container
            card = tk.Frame(content_area, bg="white", bd=0)
            card.pack(fill="x", pady=15)
            
            # Dropshadow effect (simple border)
            container = tk.Frame(card, bg="white", bd=1, relief="solid")
            container.pack(fill="x", padx=2, pady=2)
            
            # 1. Colored Header Stripe
            stripe = tk.Frame(container, bg=item["color"], height=40)
            stripe.pack(fill="x")
            stripe.pack_propagate(False)
            
            # Title inside header
            tk.Label(stripe, text=f"{item['category'].upper()}  |  {item['modul']}", 
                     font=("Arial", 14, "bold"), bg=item["color"], fg="white").pack(side="left", padx=15)
            
            # Status Badge
            tk.Label(stripe, text=f"✓ {item['status']}", 
                     font=("Arial", 10, "bold"), bg="white", fg=item["color"], padx=8, pady=2).pack(side="right", padx=15)

            # 2. Main Body (Grid Layout)
            body = tk.Frame(container, bg="white", padx=20, pady=20)
            body.pack(fill="x")
            
            # Left Column: Theory & Equation
            left_col = tk.Frame(body, bg="white")
            left_col.pack(side="left", fill="both", expand=True, padx=(0, 20))
            
            tk.Label(left_col, text=item["law"], font=("Georgia", 16, "bold"), bg="white", fg="#2d3436", anchor="w").pack(fill="x")
            
            # Description text
            tk.Label(left_col, text=item["desc"], font=("Arial", 11), bg="white", fg="#636e72", justify="left", wraplength=400, anchor="w").pack(fill="x", pady=10)
            
            # Equation Box (Math look)
            eq_box = tk.Label(left_col, text=item["eq"], font=("Times New Roman", 18, "italic"), 
                             bg="#f1f2f6", fg="#2d3436", padx=20, pady=10, relief="solid", bd=1)
            eq_box.pack(fill="x", pady=15)

            # Logic & Constants
            info_box = tk.Frame(left_col, bg="#f5f6fa", pady=5)
            info_box.pack(fill="x")
            tk.Label(info_box, text=f"{self.T('method')}: {item.get('logic','N/A')}", font=("Arial", 10, "italic"), bg="#f5f6fa", fg="gray", anchor="w").pack(fill="x", padx=10)
            tk.Label(info_box, text=f"{self.T('const')}: {item.get('const','N/A')}", font=("Arial", 10, "italic"), bg="#f5f6fa", fg="gray", anchor="w").pack(fill="x", padx=10)
            
            # Right Column: Variables
            right_col = tk.Frame(body, bg="white")
            right_col.pack(side="right", fill="both", expand=True)
            
            tk.Label(right_col, text=self.T("var_desc"), font=("Arial", 10, "bold"), bg="white", fg="#b2bec3", anchor="w").pack(fill="x", pady=(0,5))
            
            # Variable Grid
            var_grid = tk.Frame(right_col, bg="white")
            var_grid.pack(fill="x")
            
            for idx, (sym, det) in enumerate(item["vars"]):
                tk.Label(var_grid, text=f"• {sym}", font=("Times New Roman", 12, "italic", "bold"), bg="white", fg="#2d3436", width=8, anchor="w").grid(row=idx, column=0, sticky="w")
                tk.Label(var_grid, text=f": {det}", font=("Arial", 11), bg="white", fg="#636e72", anchor="w").grid(row=idx, column=1, sticky="w")
            
            # 3. Action Footer
            footer = tk.Frame(container, bg="white", height=50)
            footer.pack(fill="x")
            
            target_name = item["target"]
            # Check if target is in our list
            if target_name in [m[1] for m in LAB_MODULES]:
                 btn = tk.Button(footer, text=self.T("open_sim"), font=("Arial", 10, "bold"), 
                                fg="#2d3436", bg="white",
                                command=partial(self.show_frame, target_name))
                 btn.pack(side="right", padx=15, pady=8)
            footer = tk.Frame(container, bg="#f5f6fa", height=45)
            footer.pack(fill="x")
            footer.pack_propagate(False)
            
            # Button (Using partial for callback)
            target_name = item.get("target", "")
            if target_name:
                 # Note: On macOS, standard buttons look better than styled ones usually, but here we want color
                 # Use a simple button with text
                 btn = tk.Button(footer, text="Buka Simulasi  \u279C", font=("Arial", 10, "bold"), 
                                fg="#2d3436", bg="white",
                                command=partial(self.show_frame, target_name))
                 btn.pack(side="right", padx=15, pady=8)

    def load_labs(self):
        for filename, tab_title in LAB_MODULES:
            tab = ttk.Frame(self.content_frame)
            tab.grid(row=0, column=0, sticky="nsew")
            self.frames[tab_title] = tab
            
            modulename = filename.replace(".py", "").replace(" ", "_").replace("-", "_")
            
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            module_path = os.path.join(base_path, filename)
            
            if not os.path.exists(module_path):
                 tk.Label(tab, text=f"File Modul hilang: {filename}", fg="red").pack()
                 continue

            spec = importlib.util.spec_from_file_location(modulename, module_path)
            if spec is None:
                continue
            module = importlib.util.module_from_spec(spec)
            sys.modules[modulename] = module
            try:
                spec.loader.exec_module(module)
            except Exception as e:
                tk.Label(tab, text=f"Error loading {filename}: {e}", fg="red").pack()
                continue
            
            # Find the Lab class
            main_class = None
            for attr in dir(module):
                if ("Lab" in attr or "Virtual" in attr) and isinstance(getattr(module, attr), type):
                    main_class = getattr(module, attr)
                    break
            
            if main_class:
                # Instantiate with the tab as parent
                try:
                    app_instance = main_class(tab)
                    self.lab_instances[tab_title] = app_instance # Store instance
                    
                    # Initialize Language
                    if hasattr(app_instance, 'set_language'):
                        app_instance.set_language(self.lang)
                        
                    # If it's a Frame subclass, we might need to pack it if the class doesn't pack itself
                    if isinstance(app_instance, tk.Widget):
                        app_instance.pack(fill="both", expand=True)
                except Exception as e:
                    tk.Label(tab, text=f"Error initializing {filename}: {e}", fg="red").pack()
            else:
                tk.Label(tab, text=f"No Lab class found in {filename}", fg="red").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabFisikaModern(root)
    root.mainloop()
