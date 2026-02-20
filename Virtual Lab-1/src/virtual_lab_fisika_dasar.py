import tkinter as tk
from tkinter import ttk
import os
from virtual_lab_data_manager import DataManager

class VirtualLabFisikaDasar:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Lab Fisika Dasar")
        self.root.geometry("800x600")
        
        self.create_widgets()
        self.load_modules()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.frame = ttk.Frame(self.notebook)
        self.notebook.add(self.frame, text='Home')

        self.label = tk.Label(self.frame, text="Selamat datang di Virtual Lab Fisika Dasar", font=("Arial", 16))
        self.label.pack(pady=20)

        self.load_button = tk.Button(self.frame, text="Load Experiment Modules", command=self.load_modules)
        self.load_button.pack(pady=10)

    def load_modules(self):
        # Load experiment modules from the Basic Physics directory
        module_dir = os.path.join("src", "modules", "fisika_dasar")
        for module in os.listdir(module_dir):
            if module.endswith(".py"):
                module_name = module[:-3]  # Remove .py extension
                self.notebook.add(ttk.Frame(self.notebook), text=module_name)

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabFisikaDasar(root)
    root.mainloop()