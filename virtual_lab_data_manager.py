import json
import os
import sys
import requests
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

CONFIG_FILE = "db_config.json"

class DataManager:
    # --- Profile Management ---
    PROFILE_FILE = "student_profile.json"

    @staticmethod
    def save_profile(nama, nim, kelas):
        try:
            with open(DataManager.PROFILE_FILE, 'w') as f:
                json.dump({"nama": nama, "nim": nim, "kelas": kelas}, f)
            return True
        except:
            return False

    @staticmethod
    def get_profile():
        if os.path.exists(DataManager.PROFILE_FILE):
            try:
                with open(DataManager.PROFILE_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    # --------------------------

    @staticmethod
    def load_config():
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {"db_link": ""}
        return {"db_link": ""}

    @staticmethod
    def save_config(link):
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump({"db_link": link}, f)
            return True, "Konfigurasi berhasil disimpan."
        except Exception as e:
            return False, f"Gagal menyimpan konfigurasi: {str(e)}"

    @staticmethod
    def test_connection(link):
        if not link:
            return False, "Link database kosong!"
            
        if not link.endswith("/exec"):
             return False, "Link harus berakhiran '/exec'.\nPastikan Anda menggunakan URL 'Web App', bukan URL editor."

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Content-Type': 'application/json'
        }

        if link.startswith("http"):
            try:
                # Try a GET request first with headers
                response = requests.get(link, headers=headers, timeout=10, allow_redirects=True)
                
                if response.status_code == 200:
                    # Check if we got a Google Login page (indication that permissions are wrong)
                    if "accounts.google.com" in response.url or "Sign in" in response.text:
                         return False, "Terdeteksi Halaman Login.\nWeb App harus disetting: 'Who has access: Anyone'."
                    return True, "Koneksi ke endpoint berhasil!"
                elif response.status_code == 405:
                    return True, "Endpoint terdeteksi (Method POST needed)."
                elif response.status_code == 403:
                    return False, "Akses ditolak (403). Pastikan Web App disetting 'Who has access: Anyone'."
                else:
                    return False, f"Respon server: {response.status_code}"
            except Exception as e:
                return False, f"Gagal terkoneksi: {str(e)}"
        else:
            return False, "Format link tidak didukung (Gunakan HTTP/HTTPS)"

    @staticmethod
    def export_excel(data_list):
        if not data_list:
            return False, "Tidak ada data eksperimen untuk diekspor."
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Simpan Hasil Praktikum"
        )
        
        if not filename:
            return False, "Penyimpanan dibatalkan."

        try:
            df = pd.DataFrame(data_list)
            df.to_excel(filename, index=False)
            return True, f"Data berhasil disimpan ke:\n{filename}"
        except Exception as e:
            return False, f"Gagal membuat file Excel: {str(e)}"

    @staticmethod
    def send_to_database(data_list, link, module_name="Experiment"):
        if not data_list:
            return False, "Tidak ada data untuk dikirim."
        if not link:
            return False, "Link database belum diatur."
            
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        if link.startswith("http"):
            try:
                # Load Profile for Identity
                profile = DataManager.get_profile()
                nama = profile.get("nama", "Anonim")
                nim = profile.get("nim", "-")
                kelas = profile.get("kelas", "-")

                # Wrap data in a standard format
                payload = {
                    "experiment_data": data_list,
                    "timestamp": pd.Timestamp.now().isoformat(),
                    # Additional Identity Fields
                    "nama": nama,
                    "nim": nim,
                    "kelas": kelas,
                    "module": module_name
                }
                
                # Send Data
                response = requests.post(link, json=payload, headers=headers, timeout=10)

                if "accounts.google.com" in response.url or "Sign in" in response.text:
                    return False, "Gagal: Server meminta Login. Set permissions Web App ke 'Anyone'."
                         
                try:
                    res_json = response.json()
                    if res_json.get("status") == "success":
                        return True, f"Sukses! {res_json.get('rows')} baris data tersimpan."
                    elif res_json.get("status") == "error":
                        return False, f"Server Script Error: {res_json.get('message')}"
                except:
                    pass
                    
                # Robust Text Check
                resp_text = response.text.lower()
                if "success" in resp_text or "sukses" in resp_text:
                     return True, "Data tersimpan (Respon Text OK)."
                
                if response.status_code == 200:
                    # If 200 but no recognizable success message, return warning but count as success?
                    # Better to return Success but note the ambiguity
                     return True, f"Terkirim (Status 200). Cek Spreadsheet Anda."
                elif response.status_code == 201:
                    return True, "Data Created (201)."
                elif response.status_code == 302:
                    return True, "Data dikirim (Redirected)."
                else:
                    return False, f"Gagal mengirim data. Kode: {response.status_code}\nRespon: {response.text[:100]}"
            except Exception as e:
                return False, f"Error koneksi: {str(e)}"
        else:
            return False, "Saat ini hanya mendukung koneksi API (HTTP/HTTPS)."

    @staticmethod
    def save_excel_auto(data_list, prefix="Data"):
        folder = "Hasil_Praktikum"
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except:
                return False, "Gagal membuat folder penyimpanan."
        
        timestamp = pd.Timestamp.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Sanitize prefix
        clean_prefix = "".join(x for x in prefix if x.isalnum() or x in " -_")
        filename = os.path.join(folder, f"{clean_prefix}_{timestamp}.xlsx")
        
        try:
            df = pd.DataFrame(data_list)
            df.to_excel(filename, index=False)
            return True, f"Tersimpan di folder {folder}"
        except Exception as e:
            return False, f"Gagal auto-save Excel: {str(e)}"

    @staticmethod
    def save_data_unified(data_list, module_name="Experiment"):
        if not data_list:
            return False, "Tidak ada data untuk disimpan."
            
        # 1. Load Config for DB
        conf = DataManager.load_config()
        link = conf.get("db_link", "")
        
        # 2. Excel Export (Offline - Silent/Auto)
        excel_success, excel_msg = DataManager.save_excel_auto(data_list, module_name)
        
        # 3. Database Export (Online)
        db_success = False
        db_msg = "Link database belum disetting"
        
        if link:
            db_success, db_msg = DataManager.send_to_database(data_list, link, module_name)
            
        # 4. Construct Final Message
        if excel_success and db_success:
            return True, "Sukses menyimpan data online dan offline."
        elif excel_success and not db_success:
            return True, f"Sukses menyimpan offline.\nGagal online: {db_msg}"
        elif not excel_success and db_success:
            return True, f"Sukses menyimpan online.\nGagal offline: {excel_msg}"
        else:
            return False, f"Gagal menyimpan data.\nExcel: {excel_msg}\nOnline: {db_msg}"

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        bg_color = kwargs.get("bg", "#f5f6fa") 
        super().__init__(container, *args, **kwargs)
        self.configure(bg=bg_color)
        
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, bg=bg_color)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg_color)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Set scrolling increment to 1 pixel for smooth scrolling
        self.canvas.configure(yscrollincrement=1)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind("<Enter>", self._bound_to_mousewheel)
        self.canvas.bind("<Leave>", self._unbound_to_mousewheel)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        if event.delta:
            if sys.platform == "darwin":
                # macOS: event.delta is pixel-like. Use directly with yscrollincrement=1
                # Multiply by a speed factor (e.g. 2 or 3) if too slow, or keeping 1 for precision.
                # Inverting sign is required for standard wheel behavior vs canvas.
                self.canvas.yview_scroll(int(-1 * event.delta), "units")
            else:
                # Windows: event.delta is ±120.
                # -1 * (delta/120) * speed_factor
                self.canvas.yview_scroll(int(-1 * (event.delta / 120) * 30), "units")


