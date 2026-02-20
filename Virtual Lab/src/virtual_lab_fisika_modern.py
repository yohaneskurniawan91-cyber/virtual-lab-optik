import tkinter as tk
from tkinter import ttk
import os
from virtual_lab_data_manager import DataManager, ScrollableFrame

class VirtualLabModern:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Lab Fisika Modern")
        self.root.geometry("800x600")
        
        self.container = ScrollableFrame(self.root, bg="#2d3436")
        self.container.pack(fill="both", expand=True)
        self.main_frame = self.container.scrollable_frame
        
        self.create_widgets()
        self.load_modules()

    def create_widgets(self):
        self.title_label = ttk.Label(self.main_frame, text="Virtual Lab Fisika Modern", font=("Helvetica", 16), background="#2d3436", foreground="#00cec9")
        self.title_label.pack(pady=10)

        self.module_listbox = tk.Listbox(self.main_frame, width=50, height=15)
        self.module_listbox.pack(pady=10)

        self.load_button = ttk.Button(self.main_frame, text="Load Module", command=self.load_selected_module)
        self.load_button.pack(pady=5)

    def load_modules(self):
        self.modules = [
            ("Efek_Fotolistrik.py", "Photoelectric Effect"),
            ("Efek_Compton.py", "Compton Scattering"),
            ("Model_Atom_Bohr.py", "Bohr Model of Atom"),
            ("Radioaktivitas.py", "Radioactivity"),
            ("Difraksi_Elektron.py", "Electron Diffraction"),
        ]
        
        for module in self.modules:
            self.module_listbox.insert(tk.END, module[1])

    def load_selected_module(self):
        selected_index = self.module_listbox.curselection()
        if selected_index:
            module_name = self.modules[selected_index[0]][0]
            module_path = os.path.join("modules", "fisika_modern", module_name)
            self.run_module(module_path)

    def run_module(self, module_path):
        module = __import__(module_path[:-3])  # Import the module dynamically
        lab_class = getattr(module, "VirtualLab" + module_path.split('.')[0])  # Get the class
        lab_instance = lab_class(self.main_frame)  # Create an instance of the class

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualLabModern(root)
    root.mainloop()