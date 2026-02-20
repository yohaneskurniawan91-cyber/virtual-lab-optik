import tkinter as tk
from virtual_lab_data_manager import DataManager, ScrollableFrame

class LabEfekCompton:
    def __init__(self, parent):
        self.container = ScrollableFrame(parent, bg="#2d3436")
        self.container.pack(fill="both", expand=True)
        self.root = self.container.scrollable_frame
        
        self.setup_ui()
        
    def setup_ui(self):
        # UI setup code goes here
        title_label = tk.Label(self.root, text="Efek Compton", font=("Helvetica", 16), bg="#2d3436", fg="#00cec9")
        title_label.pack(pady=10)

        # Additional UI components for the experiment
        # ...

        save_button = tk.Button(self.root, text="Simpan Data", command=self.save_data)
        save_button.pack(pady=10)

    def save_data(self):
        # Data is a list of dicts (for DataFrame conversion)
        data = [{"photon_energy": 10, "scattering_angle": 45, "energy_after_scatter": 8.5}, ...]
        success, msg = DataManager.save_data_unified(data, module_name="Efek Compton")
        tk.messagebox.askokcancel("Result", msg)  # Show result to user

    # Additional methods for the experiment simulation
    # ...