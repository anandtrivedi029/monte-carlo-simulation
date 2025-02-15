import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class MonteCarloApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monte Carlo Simulation - Estimate π")
        
        # Parameters for simulation
        self.total_points = 0
        self.inside_circle = 0
        self.points = []
        
        # Setting up GUI layout
        self.setup_gui()
        
    def setup_gui(self):
        # Frame for controls
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Input for number of points
        tk.Label(control_frame, text="Number of Points:").pack(pady=5)
        self.num_points_entry = ttk.Entry(control_frame)
        self.num_points_entry.pack(pady=5)
        
        # Start button
        self.start_button = ttk.Button(control_frame, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack(pady=10)
        
        # Reset button
        self.reset_button = ttk.Button(control_frame, text="Reset", command=self.reset_simulation)
        self.reset_button.pack(pady=5)
        
        # Output label
        self.result_label = tk.Label(control_frame, text="Estimated π: N/A", font=("Arial", 14))
        self.result_label.pack(pady=10)
        
        # Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-1, 1)
        self.ax.set_aspect('equal')
        self.ax.add_patch(plt.Circle((0, 0), 1, color='blue', fill=False))
        
        # Embed Matplotlib figure into Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
    def start_simulation(self):
        try:
            num_points = int(self.num_points_entry.get())
        except ValueError:
            self.result_label.config(text="Please enter a valid number.")
            return
        
        self.total_points += num_points
        
        for _ in range(num_points):
            x, y = random.uniform(-1, 1), random.uniform(-1, 1)
            self.points.append((x, y))
            if x**2 + y**2 <= 1:
                self.inside_circle += 1
        
        self.update_plot()
        self.update_result()
        
    def update_plot(self):
        self.ax.clear()
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-1, 1)
        self.ax.set_aspect('equal')
        self.ax.add_patch(plt.Circle((0, 0), 1, color='blue', fill=False))
        
        # Plot points
        for x, y in self.points:
            color = 'green' if x**2 + y**2 <= 1 else 'red'
            self.ax.plot(x, y, marker='o', markersize=2, color=color)
        
        self.canvas.draw()
        
    def update_result(self):
        if self.total_points > 0:
            estimated_pi = 4 * (self.inside_circle / self.total_points)
            self.result_label.config(text=f"Estimated π: {estimated_pi:.6f}")
        
    def reset_simulation(self):
        self.total_points = 0
        self.inside_circle = 0
        self.points = []
        self.ax.clear()
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-1, 1)
        self.ax.set_aspect('equal')
        self.ax.add_patch(plt.Circle((0, 0), 1, color='blue', fill=False))
        self.result_label.config(text="Estimated π: N/A")
        self.canvas.draw()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MonteCarloApp(root)
    root.mainloop()
