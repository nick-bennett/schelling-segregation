"""
model_base.py
Abstract base class contract for the Schelling Segregation Model.
"""

from abc import ABC, abstractmethod
from typing import List

# Cell States
EMPTY = 0
GROUP_A = 1
GROUP_B = 2


class SchellingModelBase(ABC):
  """
  Abstract interface for a 2D Schelling Segregation simulation engine.
  """

  def __init__(self, width: int, height: int, density: float, tolerance: float):
    """
    Initialize the simulation grid.

    :param width: Number of columns in the grid.
    :param height: Number of rows in the grid.
    :param density: Fraction of grid populated by agents (0.0 to 1.0).
    :param tolerance: Minimum fraction of similar neighbors required
                      for an agent to be content (0.0 to 1.0).
    """
    self.width = width
    self.height = height
    self.density = density
    self.tolerance = tolerance

  @abstractmethod
  def reset(self) -> None:
    """
    Randomly populate the grid according to self.density with an equal
    split between GROUP_A and GROUP_B. The remaining cells must be EMPTY.
    """
    pass

  @abstractmethod
  def is_agent_satisfied(self, row: int, col: int) -> bool:
    """
    Determine if the agent at (row, col) is satisfied based on its neighbors.

    Neighbor convention: Moore neighborhood (8 surrounding cells).
    Boundary condition: Bounded edges (non-toroidal; cells on borders have fewer neighbors).

    Rule:
    - Ratio = (count of same-group neighbors) / (count of all non-empty neighbors).
    - If an agent has zero occupied neighbors, it is defined as satisfied (ratio = 1.0).
    - An agent is satisfied if ratio >= self.tolerance.

    :raises ValueError: If (row, col) is EMPTY.
    """
    pass

  @abstractmethod
  def step(self) -> int:
    """
    Execute one complete simulation step:
    1. Identify all discontented agents.
    2. Identify all empty cell locations.
    3. Relocate discontented agents to randomly selected empty positions.

    :return: Number of agents that were relocated during this step.
    """
    pass

  @abstractmethod
  def get_grid(self) -> List[List[int]]:
    """
    Return the current state of the grid as a 2D list of integers
    where values correspond to EMPTY (0), GROUP_A (1), and GROUP_B (2).
    """
    pass

  @abstractmethod
  def get_satisfaction_rate(self) -> float:
    """
    Compute the percentage of all active agents currently satisfied.
    :return: Value between 0.0 and 1.0. If no agents exist, returns 1.0.
    """
    pass
