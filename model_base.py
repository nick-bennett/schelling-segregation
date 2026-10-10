"""
model_base.py
Abstract base class contract for the Schelling Segregation Model.
"""

from abc import ABC, abstractmethod
from random import Random
from typing import List

# Cell States
EMPTY = 0
GROUP_A = 1
GROUP_B = 2


class SchellingModelBase(ABC):
  """
  Abstract interface for a 2D Schelling Segregation simulation engine.
  """

  def __init__(self, width: int, height: int, tolerance: float,
      rng: Random | None = None):
    """
    Initialize the simulation grid. Parameter values outside allowed ranges
    result in ValueError.

    :param width: Number of columns in the grid; must be positive.
    :param height: Number of rows in the grid; must be positive.
    :param tolerance: Minimum fraction of similar neighbors required
                      for an agent to be content; must be in [0.0, 1.0].
    :param rng: Source of randomness used for all random sampling/generation
                operations. If not provided, a new instance of Random is created.
    """
    if (width <= 0 or height <= 0
        or tolerance < 0 or tolerance > 1):
      raise ValueError()
    self._width = width
    self._height = height
    self._tolerance = tolerance
    self._rng = rng or Random()

  @abstractmethod
  def repopulate(self, density: float) -> None:
    """
    Randomly populate each cell of the grid in turn, from three possibilities:
    GROUP_A, GROUP_B, and EMPTY. Use roulette-wheel sampling, independenly for
    each sell, with probabilities of (density * 0.5) for GROUP_A,
    (density * 0.5) for GROUP_B, and (1 - density) for EMPTY.

    :param density target density, reflected (approximately) in the resulting
                   grid population; must be in [0.0, 1.0], or ValueError is
                   raised.
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
    Boundary condition: Bounded edges (non-toroidal; cells on borders have fewer neighbors).

    Rule:
    - If an agent has zero occupied neighbors:
        - it is defined as satisfied (ratio = 1.0).
      Otherwise:
        - Ratio = (count of same-group neighbors) / (count of all non-empty neighbors).
        - An agent is satisfied if ratio >= self.tolerance.

    :raises ValueError: If (row, col) is EMPTY.
    """
    pass

  @abstractmethod
  def step(self) -> int:
    """
    Execute one complete simulation step:
    1. Identify all discontented agents, according to the current tolerance.
    2. Identify all empty cell locations.
    3. If there are discontented agents and empty cell locations:
        a. Shuffle the discontented agents.
        b. For each discontented agent in turn, in shuffled order:
            i. Select a destination at random from the empty cell locations --
               without regard to whether the destination would be satisfactory
               to the agent.
           ii. Relocate the discontented agent to the destination.
          iii. Mark the destination unavailable for further relocations in this
               step, and update the cell content to GROUP_A or GROUP_B,
               according to the relocated agent.
           iv. Make the vacated location available for further relocations in
               this step, updating the cell content to EMPTY. (This deviates
               from some versions of Schelling's segregation model, in which
               newly vacated spaces are not available as destinatins in the same
               step.)

    Use steps 3.b.iii–iv to preserve the invariant condition that the total
    counts of GROUP_A, GROUP_B, and EMPTY cells remain constant.

    :return: Number of agents that were relocated during this step, or -1 if
             there are discontented agents, but no empty cell locations.
    """
    pass

  @abstractmethod
  def get_grid(self) -> List[List[int]]:
    """
    Return a safe copy of the current state of the grid as a 2D list of integers
    where values correspond to EMPTY (0), GROUP_A (1), and GROUP_B (2).
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

  @property
  def tolerance(self):
    return self._tolerance

  @tolerance.setter
  def tolerance(self, value: float):
    if value < 0 or value > 1:
      raise ValueError
    self._tolerance = value
