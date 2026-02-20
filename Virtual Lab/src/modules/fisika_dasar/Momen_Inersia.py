import tkinter as tk
from virtual_lab_data_manager import DataManager, ScrollableFrame

class LabMomenInersia:
    def __init__(self, parent):
        self.container = ScrollableFrame(parent, bg="#f5f6fa")
        self.container.pack(fill="both", expand=True)
        self.root = self.container.scrollable_frame
        self.setup_ui()

    def setup_ui(self):
        # UI setup code goes here
        pass

    def save_data(self):
        # Data collection logic goes here
        data = [{"moment_of_inertia": 5, "mass": 10, "radius": 2}, ...]
        success, msg = DataManager.save_data_unified(data, module_name="Momen Inersia")
        tk.messagebox.askokcancel("Result", msg)  # Show result to user