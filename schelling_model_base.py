"""
schelling_model_base.py
Abstract base class contract for an implementation of Schelling's model of
segregation (https://en.wikipedia.org/wiki/Schelling%27s_model_of_segregation).
"""

from abc import ABC, abstractmethod
from math import isfinite
from numbers import Real
from random import Random
from typing import List

# Cell States
EMPTY = 0
GROUP_A = 1
GROUP_B = 2


class SchellingModelBase(ABC):
  """
  Abstract interface for a 2D Schelling segregation model simulation engine. The
  implemented functionality includes:
  - Initialize a grid of a specified size, with an initial tolerance value, and
    a source of randomness.
  - Populate the grid with agents, to a specified density. (The process is
    stochastic, so the actual density is not guaranteed to match the specified
    value exactly.)
  -

  On initialization by the constructor,
  A
  grid is populated (to a specified density) by agents, each of whom belongs to
  one
  of two groups, GROUP_A and GROUP_B; the population is approximately equally
  divided between the two groups. Group membership is the only distinguishing
  feature of an agent; thus, each cell of the grid holds just its agent's group
  identifier (if occupied) or EMPTY (if unoccupied).
  """

  def __init__(self, width: int, height: int, tolerance: float,
      rng: Random | None = None):
    """
    Initialize the simulation grid without any agents. Parameter values outside
    allowed ranges result in ValueError.

    :param width: Number of columns in the grid; must be positive.
    :param height: Number of rows in the grid; must be positive.
    :param tolerance: Minimum fraction of similar neighbors required
                      for an agent to be content; must be in [0.0, 1.0].
    :param rng: Source of randomness used for all random sampling/generation. If
                not provided, a new instance of Random is created.
    """
    if not isinstance(width, int) or isinstance(width, bool) or width <= 0:
      raise ValueError("width must be a positive integer")
    if not isinstance(height, int) or isinstance(height, bool) or height <= 0:
      raise ValueError("height must be a positive integer")
    self._validate_proportion(tolerance, "tolerance")
    self._width = width
    self._height = height
    self._tolerance = float(tolerance)
    self._rng = Random() if rng is None else rng
    self._grid = [[EMPTY] * width for _ in range(height)]

  @classmethod
  def from_grid(cls, grid: List[List[int]], tolerance: float,
      rng: Random | None = None):
    """
    Create a model containing a safe copy of a specified grid.

    :param grid: Non-empty rectangular grid containing only EMPTY, GROUP_A,
                 and GROUP_B values.
    :param tolerance: Minimum fraction of similar neighbors required for an
                      agent to be content; must be in [0.0, 1.0].
    :param rng: Source of randomness used for all random operations.
    :return: New model initialized with the specified grid contents.
    :raises ValueError: If the grid is empty, ragged, or contains an invalid
                        cell value.
    """
    if not grid or not grid[0]:
      raise ValueError("grid must contain at least one row and one column")
    width = len(grid[0])
    valid_states = {EMPTY, GROUP_A, GROUP_B}
    for row in grid:
      if len(row) != width:
        raise ValueError("grid rows must all have the same length")
      if any(type(cell) is not int or cell not in valid_states for cell in row):
        raise ValueError("grid cells must be EMPTY, GROUP_A, or GROUP_B")
    model = cls(width=width, height=len(grid), tolerance=tolerance, rng=rng)
    model._grid = [row.copy() for row in grid]
    return model

  @abstractmethod
  def populate(self, density: float) -> None:
    """
    Randomly populate each cell of the grid in turn, from three possibilities:
    GROUP_A, GROUP_B, and EMPTY. Use roulette-wheel sampling, independently for
    each cell, with probabilities of (density / 2) for GROUP_A,
    (density / 2) for GROUP_B, and (1 - density) for EMPTY.

    :param density: Target density, reflected approximately in the resulting
                    grid population; must be a finite number in [0.0, 1.0].
    :raises ValueError: If density is outside the valid range.
    """
    pass

  @abstractmethod
  def step(self) -> int:
    """
    Execute one complete simulation step:
    1. Identify the locations of all discontented agents, according to the
       current tolerance.
    2. Identify all empty cell locations.
    3. If there are discontented agent locations and empty cell locations:
        a. Shuffle the discontented agent locations.
        b. For each discontented agent location in turn, in shuffled order:
            i. Select a destination at random from the empty cell locations --
               without regard to whether the destination would be satisfactory
               to the agent.
           ii. Swap the cell contents of the discontented agent location and the
               destination location. Effectively, this moves the discontented
               agent to the destination, and makes that agent's previous
               location empty. This preserves the invariant that the counts of
               GROUP_A, GROUP_B, and EMPTY cells remain constant.

    :return: Number of agents that were relocated during this step, or -1 if
             there are discontented agents, but no empty cell locations. A
             return value of zero (0) indicates that there are no discontented
             agents.
    """
    pass

  @abstractmethod
  def is_agent_satisfied(self, row: int, col: int) -> bool:
    """
    Determine if the agent at (row, col) is satisfied based on its neighbors.

    Assumption: row and col are within the bounds of the grid. It is the
                caller's responsibility to ensure that this is the case;
                behavior outside the bounds is not defined.
    Neighbor convention: Moore neighborhood (8 surrounding cells).
    Boundary condition: Bounded edges (non-toroidal; cells on borders have fewer
    neighbors).

    Rule:
    - If an agent has zero occupied neighbors:
        - it is satisfied by definition.
      Otherwise:
        - Ratio = (count of same-group neighbors) /
          (count of all non-empty neighbors).
        - An agent is satisfied if ratio >= self.tolerance.

    :raises ValueError: If (row, col) is EMPTY.
    """
    pass

  @abstractmethod
  def get_satisfaction_rate(self) -> float:
    """
    If there are any agents, compute the fraction of all active agents
    currently satisfied.
    :return: Value between 0.0 and 1.0. If no agents exist, returns 1.0.
    """
    pass

  @abstractmethod
  def get_grid(self) -> List[List[int]]:
    """
    Return a safe copy of the current state of the grid as a 2D list of integers
    where values correspond to EMPTY (0), GROUP_A (1), and GROUP_B (2).
    """
    pass

  @property
  def tolerance(self) -> float:
    return self._tolerance

  @tolerance.setter
  def tolerance(self, value: float) -> None:
    self._validate_proportion(value, "tolerance")
    self._tolerance = float(value)

  @staticmethod
  def _validate_proportion(value: float, name: str) -> None:
    if (not isinstance(value, Real) or isinstance(value, bool)
        or not isfinite(value) or value < 0 or value > 1):
      raise ValueError(f"{name} must be a finite number between 0.0 and 1.0")
