import tkinter as tk
from virtual_lab_data_manager import DataManager, ScrollableFrame
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class VirtualLabGerakHarmonikSederhana:
    def __init__(self, parent):
        self.container = ScrollableFrame(parent, bg="#f5f6fa")
        self.container.pack(fill="both", expand=True)
        self.root = self.container.scrollable_frame
        
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("Gerak Harmonik Sederhana")
        
        self.amplitude_label = tk.Label(self.root, text="Amplitude (m):")
        self.amplitude_label.pack()
        self.amplitude_entry = tk.Entry(self.root)
        self.amplitude_entry.pack()
        
        self.frequency_label = tk.Label(self.root, text="Frequency (Hz):")
        self.frequency_label.pack()
        self.frequency_entry = tk.Entry(self.root)
        self.frequency_entry.pack()
        
        self.start_button = tk.Button(self.root, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack()
        
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def start_simulation(self):
        amplitude = float(self.amplitude_entry.get())
        frequency = float(self.frequency_entry.get())
        
        self.simulate(amplitude, frequency)
        
    def simulate(self, amplitude, frequency):
        t = np.linspace(0, 2 * np.pi, 100)
        y = amplitude * np.sin(frequency * t)
        
        self.ax.clear()
        self.ax.plot(t, y)
        self.ax.set_title("Gerak Harmonik Sederhana")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Displacement (m)")
        
        self.canvas.draw()
        
    def save_data(self):
        data = [{"amplitude": self.amplitude_entry.get(), "frequency": self.frequency_entry.get()}]
        success, msg = DataManager.save_data_unified(data, module_name="Gerak Harmonik Sederhana")
        tk.messagebox.askokcancel("Result", msg)