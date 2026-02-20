import tkinter as tk
from virtual_lab_data_manager import DataManager, ScrollableFrame

class VirtualLabEfekFotolistrik:
    def __init__(self, parent):
        self.container = ScrollableFrame(parent, bg="#2d3436")
        self.container.pack(fill="both", expand=True)
        self.root = self.container.scrollable_frame
        
        self.setup_ui()
        
    def setup_ui(self):
        title_label = tk.Label(self.root, text="Efek Fotolistrik", font=("Helvetica", 16), bg="#2d3436", fg="#00cec9")
        title_label.pack(pady=10)

        # Additional UI components for the experiment can be added here

        save_button = tk.Button(self.root, text="Simpan Data", command=self.save_data)
        save_button.pack(pady=10)

    def save_data(self):
        data = [{"frequency": 5, "energy": 2.5}, {"frequency": 6, "energy": 3.0}]  # Example data
        success, msg = DataManager.save_data_unified(data, module_name="Efek Fotolistrik")
        tk.messagebox.askokcancel("Result", msg)  # Show result to user

    # Additional methods for running the simulation can be added here