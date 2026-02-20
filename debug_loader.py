import importlib.util
import sys
import os
import inspect

# Mock tkinter for headless env if needed, though we seem to have display
import tkinter as tk

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

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.getcwd()

root = tk.Tk()

for filename, title in LAB_MODULES:
    print(f"--- Checking {filename} ---")
    module_path = os.path.join(base_path, filename)
    modulename = filename.replace(".py", "").replace(" ", "_").replace("-", "_")
    
    try:
        spec = importlib.util.spec_from_file_location(modulename, module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[modulename] = module
        spec.loader.exec_module(module)

        found = False
        main_class = None
        for attr in dir(module):
            val = getattr(module, attr)
            if isinstance(val, type) and ("Lab" in attr or "Virtual" in attr):
                main_class = val
                found = True
                print(f"  FOUND Class: {attr}")
                break
        
        if not found:
            print("  FAIL: No class found!")
        else:
            try:
                # Instantiate
                tab = tk.Frame(root)
                instance = main_class(tab)
                print(f"  SUCCESS: Instantiated")
            except Exception as e:
                print(f"  ERROR Init: {e}")
                import traceback
                traceback.print_exc()

    except Exception as e:
        print(f"  ERROR Load: {e}")

root.destroy()

