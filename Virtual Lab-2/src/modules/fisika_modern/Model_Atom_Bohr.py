import tkinter as tk
from virtual_lab_data_manager import DataManager, ScrollableFrame

class VirtualLabModelAtomBohr:
    def __init__(self, parent):
        self.container = ScrollableFrame(parent, bg="#2d3436")
        self.container.pack(fill="both", expand=True)
        self.root = self.container.scrollable_frame
        
        self.setup_ui()

    def setup_ui(self):
        # UI setup code for the Bohr model simulation
        title_label = tk.Label(self.root, text="Model Atom Bohr", font=("Helvetica", 16), bg="#2d3436", fg="#00cec9")
        title_label.pack(pady=10)

        # Additional UI components for the simulation
        # ...

        save_button = tk.Button(self.root, text="Simpan Data", command=self.save_data)
        save_button.pack(pady=20)

    def save_data(self):
        data = [{"n": 1, "energy": -13.6, "radius": 0.529}, ...]  # Example data structure
        success, msg = DataManager.save_data_unified(data, module_name="Model Atom Bohr")
        tk.messagebox.askokcancel("Result", msg)  # Show result to user

    # Additional methods for the simulation logic
    # ...