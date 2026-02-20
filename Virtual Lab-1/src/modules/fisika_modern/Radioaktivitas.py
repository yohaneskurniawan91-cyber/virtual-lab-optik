import tkinter as tk
from virtual_lab_data_manager import DataManager, ScrollableFrame

class LabRadioaktivitas:
    def __init__(self, parent):
        self.container = ScrollableFrame(parent, bg="#2d3436")
        self.container.pack(fill="both", expand=True)
        self.root = self.container.scrollable_frame
        
        self.setup_ui()

    def setup_ui(self):
        title_label = tk.Label(self.root, text="Simulasi Radioaktivitas", font=("Helvetica", 16), bg="#2d3436", fg="#00cec9")
        title_label.pack(pady=10)

        # Additional UI components for the radioactivity simulation
        # Example: Entry fields, buttons, and plots can be added here

        save_button = tk.Button(self.root, text="Simpan Data", command=self.save_data)
        save_button.pack(pady=20)

    def save_data(self):
        data = [{"time": 0, "activity": 100}, {"time": 1, "activity": 90}]  # Example data
        success, msg = DataManager.save_data_unified(data, module_name="Radioaktivitas")
        tk.messagebox.askokcancel("Result", msg)  # Show result to user

    # Additional methods for running the simulation can be added here