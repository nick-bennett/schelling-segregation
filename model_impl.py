"""
model_impl.py
Concrete implementation scaffold for the Schelling Segregation Model.
"""

from typing import List

from model_base import SchellingModelBase


class SchellingModel(SchellingModelBase):
  """
  Concrete Schelling model implementation scaffold.
  """

  def repopulate(self, density: float) -> None:
    raise NotImplementedError

  def is_agent_satisfied(self, row: int, col: int) -> bool:
    raise NotImplementedError

  def step(self) -> int:
    raise NotImplementedError

  def get_grid(self) -> List[List[int]]:
    raise NotImplementedError

  def get_satisfaction_rate(self) -> float:
    raise NotImplementedError
