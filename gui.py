"""
gui.py
Pre-built Tkinter visualization harness.
Expects `schelling_model.py` with `SchellingModel` in the same directory.
"""

import tkinter as tk
from tkinter import ttk

from schelling_model import SchellingModel

from schelling_model_base import EMPTY, GROUP_A, GROUP_B

COLOR_MAP = {
  EMPTY: "#FFFFFF",
  GROUP_A: "#E74C3C",  # Coral Red
  GROUP_B: "#3498DB"   # Sky Blue
}

GRID_SIZE = 40
CELL_PX = 12
INITIAL_DENSITY = 0.85
INITIAL_TOLERANCE = 0.35


class SchellingGUI:
  def __init__(self, root: tk.Tk):
    self.root = root
    self.root.title("Schelling Segregation Explorer")
    self.running = False

    self.density_var = tk.DoubleVar(value=INITIAL_DENSITY)
    self.tolerance_var = tk.DoubleVar(value=INITIAL_TOLERANCE)
    self.density_text = tk.StringVar()
    self.tolerance_text = tk.StringVar()
    self.density_var.trace_add("write", self._update_control_values)
    self.tolerance_var.trace_add("write", self._update_control_values)
    self._update_control_values()

    self.model = SchellingModel(
        width=GRID_SIZE,
        height=GRID_SIZE,
        tolerance=INITIAL_TOLERANCE
    )
    self.model.repopulate(INITIAL_DENSITY)

    self._build_widgets()
    self.draw_grid()

  def _build_widgets(self):
    control_panel = ttk.Frame(self.root, padding=10)
    control_panel.pack(side=tk.LEFT, fill=tk.Y)

    # Sliders
    density_header = ttk.Frame(control_panel)
    density_header.pack(fill=tk.X)
    ttk.Label(density_header, text="Population Density").pack(side=tk.LEFT)
    ttk.Label(density_header, textvariable=self.density_text).pack(side=tk.RIGHT)
    self.density_slider = ttk.Scale(
        control_panel, from_=0.1, to=0.98, variable=self.density_var
    )
    self.density_slider.pack(fill=tk.X, pady=(0, 10))

    tolerance_header = ttk.Frame(control_panel)
    tolerance_header.pack(fill=tk.X)
    ttk.Label(tolerance_header, text="Tolerance Threshold (T)").pack(side=tk.LEFT)
    ttk.Label(
        tolerance_header, textvariable=self.tolerance_text
    ).pack(side=tk.RIGHT)
    self.tolerance_slider = ttk.Scale(
        control_panel, from_=0.0, to=1.0, variable=self.tolerance_var
    )
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

  def _update_control_values(self, *_):
    self.density_text.set(f"{self.density_var.get():.2f}")
    self.tolerance_text.set(f"{self.tolerance_var.get():.2f}")

  def draw_grid(self):
    self.canvas.delete("all")
    grid = self.model.get_grid()
    for r, row in enumerate(grid):
      for c, val in enumerate(row):
        color = COLOR_MAP.get(val, "#000000")
        x0, y0 = c * CELL_PX, r * CELL_PX
        x1, y1 = x0 + CELL_PX, y0 + CELL_PX
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#F0F0F0")

    sat = self.model.get_satisfaction_rate() * 100
    self.status_var.set(f"Satisfaction: {sat:.1f}%")

  def handle_reset(self):
    self.running = False
    self.run_btn.config(text="Run Simulation")
    self.model.repopulate(self.density_var.get())
    self.model.tolerance = self.tolerance_var.get()
    self.draw_grid()

  def handle_step(self):
    self.model.tolerance = self.tolerance_var.get()
    moves = self.model.step()
    self.draw_grid()
    sat = self.model.get_satisfaction_rate() * 100
    if moves == -1:
      self.status_var.set(f"Satisfaction: {sat:.1f}% | Blocked: no empty cells")
    else:
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
    if moves <= 0:
      self.running = False
      self.run_btn.config(text="Run Simulation")
      return
    self.root.after(50, self._loop)


if __name__ == "__main__":
  app_root = tk.Tk()
  app = SchellingGUI(app_root)
  app_root.mainloop()
