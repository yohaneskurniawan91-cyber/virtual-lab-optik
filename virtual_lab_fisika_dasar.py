import tkinter as tk
from tkinter import ttk
import importlib
import importlib.util
import sys
import os
from functools import partial
from tkinter import messagebox
from virtual_lab_data_manager import DataManager

# Daftar modul dan judul tab
LAB_MODULES = [
    ("ketidakpastian pengukuran.py", "Ketidakpastian Pengukuran"),
    ("hukum newton.py", "Hukum Newton"),
    ("gaya gesekan.py", "Gaya Gesek"),
    ("momen inersia Katrol.py", "Momen Inersia"),
    ("sistem katrol.py", "Katrol"),
    ("bandul Matematis.py", "Bandul Matematis"),
    ("konstanta Pegas.py", "Konstanta Pegas"),
    ("Resonansi Gelombang Bunyi.py", "Resonansi Bunyi"),
    ("Praktikum massa jenis.py", "Massa Jenis"),
    ("penerapan termometer.py", "Termometer"),
    ("kapasitas kalorimeter.py", "Kapasitas Kalorimeter"),
    ("Usaha Energi.py", "Usaha & Energi"),
    ("Momentum & Tumbukan.py", "Momentum & Tumbukan"),
    ("Gerak Menggelinding.py", "Gerak Menggelinding")
]

class VirtualLabFisikaDasar:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Lab Fisika Dasar (Mekanika)")
        self.root.geometry("1400x900")
        self.bg_color = "#273c75"
        self.header_color = "#192a56"
        self.text_color = "#f5f6fa"
        self.accent_color = "#e1b12c"
        self.footer_color = "#353b48"
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.create_header()
        
        # Navigation Container
        self.nav_frame = tk.Frame(root, bg="#2c3e50")
        self.nav_frame.pack(side="top", fill="x")
        
        # Content Container (Scrollable)
        self.create_scrollable_container()
        
        self.frames = {} 
        self.buttons = {}
        
        self.create_home_tab() # Now creates a frame in content_frame
        self.load_labs()
        self.create_navigation_buttons()
        self.create_db_controls()
        self.create_footer()
        
        self.check_student_identity()
        
        # Show home by default
        self.show_frame("Beranda")

    def create_scrollable_container(self):
        # Container for Canvas + Scrollbar
        self.main_container = tk.Frame(self.root, bg="#f5f6fa")
        self.main_container.pack(side="top", fill="both", expand=True)
        
        self.canvas = tk.Canvas(self.main_container, bg="#f5f6fa", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # The Frame inside Canvas
        self.content_frame = tk.Frame(self.canvas, bg="#f5f6fa")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        
        self.content_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Enable MouseWheel scrolling
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
        # Ensure Grid expansion
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.check_scrollbar_visibility()

    def on_canvas_configure(self, event):
        # Force content frame width to match canvas (Proportional / Fit Width)
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        self.check_scrollbar_visibility()

    def check_scrollbar_visibility(self):
        # Show scrollbar only if content > canvas height (Auto Hide/Show)
        req_h = self.content_frame.winfo_reqheight()
        cv_h = self.canvas.winfo_height()
        
        if req_h > cv_h and cv_h > 10:
            self.scrollbar.pack(side="right", fill="y", before=self.canvas)
        else:
            self.scrollbar.pack_forget()

    def on_mousewheel(self, event):
        # Only scroll if scrollbar is active (visible)
        if self.scrollbar.winfo_ismapped():
            self.canvas.yview_scroll(int(-1*(event.delta)), "units")

    def check_student_identity(self):
        # Startup Identity Check with Explicit Login UI
        self.root.withdraw() # Hide Main App
        self.ask_identity_dialog()
            
    def ask_identity_dialog(self):
        # Dedicated Login Window
        dialog = tk.Toplevel(self.root)
        dialog.title("Login Praktikan - Fisika Dasar")
        dialog.geometry("450x400")
        dialog.configure(bg="#2d3436")
        
        # Handle Closure
        def on_close():
            self.root.destroy()
            sys.exit()
        dialog.protocol("WM_DELETE_WINDOW", on_close)
        
        # Header
        tk.Label(dialog, text="VIRTUAL LAB FISIKA DASAR", font=("Arial", 16, "bold"), bg="#2d3436", fg="#dfe6e9").pack(pady=(20,5))
        tk.Label(dialog, text="Masukkan Identitas untuk Memulai", font=("Arial", 10), bg="#2d3436", fg="#b2bec3").pack(pady=(0,15))
        
        # Form Container
        frm = tk.Frame(dialog, padx=30, pady=20, bg="#636e72", relief="flat")
        frm.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Style helper
        lbl_style = {"bg":"#636e72", "fg":"white", "font":("Arial", 10, "bold")}
        entry_bg = "#dfe6e9"
        
        tk.Label(frm, text="Nama Lengkap:", **lbl_style).pack(anchor="w", pady=(5,0))
        e_nama = tk.Entry(frm, width=40, font=("Arial", 11), bg=entry_bg)
        e_nama.pack(pady=5)
        
        tk.Label(frm, text="NIM / NIS:", **lbl_style).pack(anchor="w", pady=(10,0))
        e_nim = tk.Entry(frm, width=40, font=("Arial", 11), bg=entry_bg)
        e_nim.pack(pady=5)
        
        tk.Label(frm, text="Kelas / Shift:", **lbl_style).pack(anchor="w", pady=(10,0))
        e_kelas = tk.Entry(frm, width=40, font=("Arial", 11), bg=entry_bg)
        e_kelas.pack(pady=5)
        
        # Autofill
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
                messagebox.showerror("Login Error", "Nama dan NIM wajib diisi!", parent=dialog)
                return
                
            DataManager.save_profile(nama, nim, kelas)
            dialog.destroy()
            self.root.deiconify() # Reveal Main App
            
        tk.Button(dialog, text="MASUK / LOGIN", bg="#0984e3", fg="black", font=("Arial", 11, "bold"), 
                  width=30, pady=10, command=login).pack(pady=20)
        
        # Wait window
        self.root.wait_window(dialog)

    def create_header(self):
        frame = tk.Frame(self.root, bg=self.header_color, pady=18)
        frame.pack(side="top", fill="x")
        icon = "\U0001F52C"  # emoji mikroskop
        
        tk.Label(frame, text=f"{icon}  VIRTUAL LAB FISIKA DASAR (MEKANIKA)", 
                 font=("Arial", 24, "bold"), fg=self.text_color, bg=self.header_color,
                 wraplength=1200, justify="center").pack(pady=(0, 5))
                 
        tk.Label(frame, text="Eksperimen Interaktif | Pengembang: Yohanes Kurniawan", 
                 font=("Arial", 13), fg="#dff9fb", bg=self.header_color).pack()
                 
        tk.Label(frame, text="Virtual Lab dikembangkan untuk mendukung penerapan model Experiential Worked-Example Berbasis Seamless Learning", 
                 font=("Arial", 11, "italic"), fg="#f6e58d", bg=self.header_color,
                 wraplength=1000, justify="center").pack(pady=(2, 0))

    def create_footer(self):
        frame = tk.Frame(self.root, bg=self.footer_color, pady=8)
        frame.pack(side="bottom", fill="x")
        tk.Label(frame, text="© 2026 Yohanes Kurniawan | Virtual Lab Fisika Dasar", font=("Arial", 11), fg="#dcdde1", bg=self.footer_color).pack()

    def create_navigation_buttons(self):
        # Organize buttons into 2 rows as requested
        # Row 1 Items
        row1 = ["Beranda", "Ketidakpastian Pengukuran", "Hukum Newton", "Momen Inersia", "Katrol", "Bandul Matematis", "Konstanta Pegas"]
        # Row 2 Items (Rest of items)
        row2 = ["Massa Jenis", "Termometer", "Kapasitas Kalorimeter", "Usaha & Energi", "Momentum & Tumbukan", "Gerak Menggelinding", "Resonansi Bunyi"]
        
        # Helper to style buttons
        def create_btn(parent, text, r, c):
             # highlightbackground needed for macOS button coloring
             btn = tk.Button(parent, text=text, font=("Arial", 12, "bold"), 
                             bg="white", fg="black", highlightbackground="white",
                             activebackground=self.accent_color, activeforeground="black",
                             relief="flat", padx=10, pady=5,
                             command=partial(self.show_frame, text))
             btn.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)
             self.buttons[text] = btn
             return btn

        # Configure columns to be equal width
        for i in range(max(len(row1), len(row2))):
             self.nav_frame.grid_columnconfigure(i, weight=1)

        for i, name in enumerate(row1):
             create_btn(self.nav_frame, name, 0, i)
             
        for i, name in enumerate(row2):
             create_btn(self.nav_frame, name, 1, i)

    def create_db_controls(self):
        # Frame for Data Controls
        control_frame = tk.Frame(self.nav_frame, bg="#2c3e50", pady=5)
        # Assuming nav_frame uses grid, we can't pack mixed with grid if not careful.
        # Wait, nav_frame is used with grid in create_navigation_buttons? 
        # create_navigation_buttons uses: 
        # btn.grid(row=r, column=c...) 
        # So I cannot .pack() inside nav_frame if it has grid children.
        # I should use .grid() for control_frame too, e.g. row 2.
        control_frame.grid(row=2, column=0, columnspan=10, sticky="ew", pady=5)
        
        container = tk.Frame(control_frame, bg="#2c3e50")
        container.pack(anchor="center")
        
        # Updated style for better readability on macOS (White button with black text)
        style = {"font":("Arial", 10, "bold"), "bg":"#ffffff", "fg":"#2c3e50", 
                 "highlightbackground":"#ffffff", "activeforeground":"#2c3e50",
                 "relief":"flat", "padx":15, "pady":5, "activebackground":"#e1b12c"}
        
        tk.Button(container, text="🔗 Konfigurasi Database", command=self.open_db_settings, **style).pack(side="left", padx=5)
        tk.Button(container, text="⚡ Test Koneksi", command=self.test_db_connection, **style).pack(side="left", padx=5)
        tk.Button(container, text="💾 Unduh File Excel", command=self.handle_dl_excel, **style).pack(side="left", padx=5)
        # Save buttons moved to experiment analysis tabs

    def open_db_settings(self):
        top = tk.Toplevel(self.root)
        top.title("Konfigurasi Database")
        top.geometry("600x250")
        top.configure(bg="#2c3e50")
        
        tk.Label(top, text="Link Database / API Endpoint:", font=("Arial", 12, "bold"), fg="white", bg="#2c3e50").pack(pady=(20,5))
        tk.Label(top, text="(Contoh: https://script.google.com/... atau API Endpoint)", font=("Arial", 9), fg="#bdc3c7", bg="#2c3e50").pack(pady=(0,5))
        
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
            
        tk.Button(top, text="Simpan Konfigurasi", command=save, bg="#e1b12c", fg="black", font=("Arial", 10, "bold"), padx=10, pady=5).pack(pady=15)

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
        if instance and hasattr(instance, 'get_data'):
            return instance.get_data()
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
        # Hide all frames first to ensure content frame resizes correctly
        for name, frame in self.frames.items():
            frame.grid_remove()
            
        if page_name in self.frames:
            self.frames[page_name].grid(row=0, column=0, sticky="nsew")
            self.current_page = page_name
            
            # Reset scroll to top
            self.canvas.yview_moveto(0)
            
            # Update scrollbar visibility
            self.content_frame.update_idletasks()
            self.check_scrollbar_visibility()
            
        # Update button styles (Active state)
        for name, btn in self.buttons.items():
            # Standard Reset
            btn.config(bg="white", highlightbackground="white", fg="black")
            
        if page_name in self.buttons:
             # Active State: Accent Color + Black Text
             self.buttons[page_name].config(bg=self.accent_color, highlightbackground=self.accent_color, fg="black")

    def create_home_tab(self):
        # Create a Frame instead of adding to notebook
        home = ttk.Frame(self.content_frame)
        home.grid(row=0, column=0, sticky="nsew")
        self.frames["Beranda"] = home
        
        icon = "\U0001F393"
        # Judul utama
        tk.Label(home, text=f"{icon} Selamat Datang di Virtual Lab Fisika Dasar (Mekanika)", 
                 font=("Arial", 22, "bold"), fg=self.header_color,
                 wraplength=1000, justify="center").pack(pady=(30,10))
                 
        # Blok info pengembang
        info_frame = tk.Frame(home, bg="#f6e58d", bd=2, relief="groove")
        info_frame.pack(pady=(0,18), padx=30, fill="x")
        
        tk.Label(info_frame, text="Pengembang Virtual Lab :", font=("Arial", 13, "bold"), fg="#222", bg="#f6e58d").pack(anchor="w", padx=16, pady=(10,0))
        tk.Label(info_frame, text="Yohanes Kurniawan", font=("Arial", 14, "bold"), fg="#222", bg="#f6e58d").pack(anchor="w", padx=32)
        tk.Label(info_frame, text="S3 Teknologi Pembelajaran Universitas Negeri Malang", font=("Arial", 12), fg="#222", bg="#f6e58d").pack(anchor="w", padx=32)
        tk.Label(info_frame, text="S2 Pendidikan Fisika Universitas Negeri Yogyakarta", font=("Arial", 12), fg="#222", bg="#f6e58d").pack(anchor="w", padx=32)
        tk.Label(info_frame, text="S1 Pendidikan Fisika Universitas Nusa Cendana", font=("Arial", 12), fg="#222", bg="#f6e58d").pack(anchor="w", padx=32)
        tk.Label(info_frame, text="Asal Lembata - Nusa Tenggara Timur", font=("Arial", 12), fg="#222", bg="#f6e58d").pack(anchor="w", padx=32)
        tk.Label(info_frame, text="Dosen Unika Santu Paulus Ruteng", font=("Arial", 12), fg="#222", bg="#f6e58d").pack(anchor="w", padx=32, pady=(0,10))
        
        # Highlight tujuan aplikasi
        highlight = tk.Label(home, text="Virtual Lab ini dikembangkan untuk mendukung penerapan model Experiential Worked-Example Berbasis Seamless Learning.", font=("Arial", 12, "italic"), fg="#fff", bg="#e17055", wraplength=900, justify="center")
        highlight.pack(pady=(0,18), padx=30, fill="x")
        
        # Instruksi penggunaan
        instruksi_frame = tk.Frame(home, bg="#dff9fb", bd=1, relief="solid")
        instruksi_frame.pack(pady=(0,18), padx=30, fill="x")
        tk.Label(instruksi_frame, text="Petunjuk Penggunaan:", font=("Arial", 13, "bold"), fg=self.header_color, bg="#dff9fb").pack(anchor="w", padx=16, pady=(10,0))
        tk.Label(instruksi_frame, text="Pilih salah satu tab di atas untuk memulai eksperimen fisika secara interaktif. Setiap praktikum dapat dijalankan secara mandiri.", font=("Arial", 12), fg="#222", bg="#dff9fb", wraplength=900, justify="left").pack(anchor="w", padx=32, pady=(0,10))

    def load_labs(self):
        for filename, tab_title in LAB_MODULES:
            # Create Frame in content_frame instead of Notebook tab
            tab = ttk.Frame(self.content_frame)
            tab.grid(row=0, column=0, sticky="nsew") # Stack on top of each other
            self.frames[tab_title] = tab
            
            modulename = filename.replace(".py", "").replace(" ", "_").replace("-", "_")
            
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            module_path = os.path.join(base_path, filename)

            spec = importlib.util.spec_from_file_location(modulename, module_path)
            if spec is None:
                label = tk.Label(tab, text=f"Gagal memuat modul: {filename}", fg="red", font=("Arial", 13, "bold"))
                label.pack(padx=20, pady=20)
                continue
            module = importlib.util.module_from_spec(spec)
            sys.modules[modulename] = module
            try:
                spec.loader.exec_module(module)
            except Exception as e:
                label = tk.Label(tab, text=f"Error pada modul {filename}:\n{e}", fg="red", font=("Arial", 13, "bold"))
                label.pack(padx=20, pady=20)
                continue
            main_class = None
            for attr in dir(module):
                if ("Lab" in attr or "Virtual" in attr) and isinstance(getattr(module, attr), type):
                    main_class = getattr(module, attr)
                    break
            if main_class is None:
                label = tk.Label(tab, text=f"Tidak ditemukan kelas utama pada {filename}", fg="red", font=("Arial", 13, "bold"))
                label.pack(padx=20, pady=20)
                continue
            try:
                # Pastikan inisialisasi dengan parent=tab
                # We don't need to store lab_instances in a dict strictly if we don't access them, but kept for consistency
                main_class(tab)
            except Exception as e:
                label = tk.Label(tab, text=f"Gagal inisialisasi {main_class.__name__}:\n{e}", fg="red", font=("Arial", 13, "bold"))
                label.pack(padx=20, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabFisikaDasar(root)
    root.mainloop()
