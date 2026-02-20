import tkinter as tk
from virtual_lab_data_manager import DataManager, ScrollableFrame
import matplotlib.pyplot as plt
import numpy as np

class VirtualLabGerakParabola:
    def __init__(self, parent):
        self.container = ScrollableFrame(parent, bg="#f5f6fa")
        self.container.pack(fill="both", expand=True)
        self.root = self.container.scrollable_frame
        
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("Gerak Parabola")
        
        # Input fields for initial velocity and angle
        tk.Label(self.root, text="Kecepatan Awal (m/s):").grid(row=0, column=0)
        self.initial_velocity_entry = tk.Entry(self.root)
        self.initial_velocity_entry.grid(row=0, column=1)
        
        tk.Label(self.root, text="Sudut (derajat):").grid(row=1, column=0)
        self.angle_entry = tk.Entry(self.root)
        self.angle_entry.grid(row=1, column=1)
        
        # Button to run the simulation
        self.run_button = tk.Button(self.root, text="Jalankan Simulasi", command=self.run_simulation)
        self.run_button.grid(row=2, columnspan=2)
        
        # Canvas for plotting
        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.grid(row=3, columnspan=2)
        
    def run_simulation(self):
        try:
            v_0 = float(self.initial_velocity_entry.get())
            angle = float(self.angle_entry.get())
            self.simulate_projectile_motion(v_0, angle)
        except ValueError:
            tk.messagebox.showerror("Input Error", "Masukkan nilai yang valid untuk kecepatan dan sudut.")
    
    def simulate_projectile_motion(self, v_0, angle):
        g = 9.81  # Acceleration due to gravity (m/s^2)
        angle_rad = np.radians(angle)
        
        # Time of flight
        t_flight = (2 * v_0 * np.sin(angle_rad)) / g
        t = np.linspace(0, t_flight, num=100)
        
        # Calculate x and y coordinates
        x = v_0 * np.cos(angle_rad) * t
        y = (v_0 * np.sin(angle_rad) * t) - (0.5 * g * t**2)
        
        # Clear previous plot
        self.canvas.delete("all")
        
        # Plot the trajectory
        plt.figure(figsize=(6, 4))
        plt.plot(x, y)
        plt.title("Trajektori Gerak Parabola")
        plt.xlabel("Jarak (m)")
        plt.ylabel("Tinggi (m)")
        plt.xlim(0, max(x))
        plt.ylim(0, max(y) + 1)
        plt.grid()
        
        # Draw the plot on the Tkinter canvas
        self.draw_plot()
        
    def draw_plot(self):
        plt.savefig("temp_plot.png")
        plt.close()
        img = tk.PhotoImage(file="temp_plot.png")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.canvas.image = img  # Keep a reference to avoid garbage collection

    def save_data(self):
        data = [{"v_0": self.initial_velocity_entry.get(), "angle": self.angle_entry.get()}]
        success, msg = DataManager.save_data_unified(data, module_name="Gerak Parabola")
        tk.messagebox.askokcancel("Result", msg)  # Show result to user