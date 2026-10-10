"""
gui.py
Pre-built Tkinter visualization harness.
Expects `model_impl.py` with `SchellingModel` in the same directory.
"""

import tkinter as tk
from tkinter import ttk

from model_impl import SchellingModel

from model_base import EMPTY, GROUP_A, GROUP_B

COLOR_MAP = {
  EMPTY: "#FFFFFF",
  GROUP_A: "#E74C3C",  # Coral Red
  GROUP_B: "#3498DB"   # Sky Blue
}

GRID_SIZE = 40
CELL_PX = 12


class SchellingGUI:
  def __init__(self, root: tk.Tk):
    self.root = root
    self.root.title("Schelling Segregation Explorer")
    self.running = False

    self.model = SchellingModel(
        width=GRID_SIZE,
        height=GRID_SIZE,
        density=0.85,
        tolerance=0.35
    )
    self.model.reset()

    self._build_widgets()
    self.draw_grid()

  def _build_widgets(self):
    control_panel = ttk.Frame(self.root, padding=10)
    control_panel.pack(side=tk.LEFT, fill=tk.Y)

    # Sliders
    ttk.Label(control_panel, text="Population Density").pack(anchor=tk.W)
    self.density_slider = ttk.Scale(control_panel, from_=0.1, to=0.98, value=0.85)
    self.density_slider.pack(fill=tk.X, pady=(0, 10))

    ttk.Label(control_panel, text="Tolerance Threshold (T)").pack(anchor=tk.W)
    self.tolerance_slider = ttk.Scale(control_panel, from_=0.0, to=1.0, value=0.35)
    self.tolerance_slider.pack(fill=tk.X, pady=(0, 10))

    # Status Labels
    self.status_var = tk.StringVar(value="Satisfaction: 0.0% | Moves: 0")
    ttk.Label(control_panel, textvariable=self.status_var).pack(pady=10)

    # Control Buttons
    ttk.Button(control_panel, text="Reset Grid", command=self.handle_reset).pack(fill=tk.X, pady=2)
    ttk.Button(control_panel, text="Step Once", command=self.handle_step).pack(fill=tk.X, pady=2)
    self.run_btn = ttk.Button(control_panel, text="Run Simulation", command=self.toggle_run)
    self.run_btn.pack(fill=tk.X, pady=2)

    # Canvas
    canvas_px = GRID_SIZE * CELL_PX
    self.canvas = tk.Canvas(self.root, width=canvas_px, height=canvas_px, bg="white")
    self.canvas.pack(side=tk.RIGHT, padx=10, pady=10)

  def draw_grid(self):
    self.canvas.delete("all")
    grid = self.model.get_grid()
    for r in range(GRID_SIZE):
      for c in range(GRID_SIZE):
        val = grid[r][c]
        color = COLOR_MAP.get(val, "#000000")
        x0, y0 = c * CELL_PX, r * CELL_PX
        x1, y1 = x0 + CELL_PX, y0 + CELL_PX
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#F0F0F0")

    sat = self.model.get_satisfaction_rate() * 100
    self.status_var.set(f"Satisfaction: {sat:.1f}%")

  def handle_reset(self):
    self.running = False
    self.run_btn.config(text="Run Simulation")
    self.model.density = float(self.density_slider.get())
    self.model.tolerance = float(self.tolerance_slider.get())
    self.model.reset()
    self.draw_grid()

  def handle_step(self):
    self.model.tolerance = float(self.tolerance_slider.get())
    moves = self.model.step()
    self.draw_grid()
    sat = self.model.get_satisfaction_rate() * 100
    self.status_var.set(f"Satisfaction: {sat:.1f}% | Last Moves: {moves}")
    return moves

  def toggle_run(self):
    self.running = not self.running
    self.run_btn.config(text="Pause" if self.running else "Run Simulation")
    if self.running:
      self._loop()

  def _loop(self):
    if not self.running:
      return
    moves = self.handle_step()
    if moves == 0:
      self.running = False
      self.run_btn.config(text="Run Simulation")
      return
    self.root.after(50, self._loop)


if __name__ == "__main__":
  app_root = tk.Tk()
  app = SchellingGUI(app_root)
  app_root.mainloop()
