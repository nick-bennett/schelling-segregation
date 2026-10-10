"""
schelling_model.py
Concrete implementation of the Schelling Segregation Model.
"""

from typing import List

from schelling_model_base import EMPTY, GROUP_A, GROUP_B, SchellingModelBase


class SchellingModel(SchellingModelBase):
  """
  Concrete Schelling segregation simulation engine.
  """

  def repopulate(self, density: float) -> None:
    self._validate_proportion(density, "density")
    density = float(density)
    group_probability = density * 0.5
    self._grid = []
    for _ in range(self._height):
      row = []
      for _ in range(self._width):
        sample = self._rng.random()
        if sample < group_probability:
          row.append(GROUP_A)
        elif sample < density:
          row.append(GROUP_B)
        else:
          row.append(EMPTY)
      self._grid.append(row)

  def is_agent_satisfied(self, row: int, col: int) -> bool:
    agent = self._grid[row][col]
    if agent == EMPTY:
      raise ValueError("cannot determine satisfaction for an empty cell")

    occupied_neighbors = 0
    same_group_neighbors = 0
    for row_offset in (-1, 0, 1):
      neighbor_row = row + row_offset
      if neighbor_row < 0 or neighbor_row >= self._height:
        continue
      for col_offset in (-1, 0, 1):
        if row_offset == 0 and col_offset == 0:
          continue
        neighbor_col = col + col_offset
        if neighbor_col < 0 or neighbor_col >= self._width:
          continue
        neighbor = self._grid[neighbor_row][neighbor_col]
        if neighbor != EMPTY:
          occupied_neighbors += 1
          if neighbor == agent:
            same_group_neighbors += 1

    if occupied_neighbors == 0:
      return True
    return same_group_neighbors / occupied_neighbors >= self._tolerance

  def step(self) -> int:
    discontented_agents = []
    empty_locations = []
    for row in range(self._height):
      for col in range(self._width):
        if self._grid[row][col] == EMPTY:
          empty_locations.append((row, col))
        elif not self.is_agent_satisfied(row, col):
          discontented_agents.append((row, col))

    if not discontented_agents:
      return 0
    if not empty_locations:
      return -1

    self._rng.shuffle(discontented_agents)
    for source_row, source_col in discontented_agents:
      destination = self._rng.choice(empty_locations)
      empty_locations.remove(destination)
      destination_row, destination_col = destination

      self._grid[destination_row][destination_col] = self._grid[source_row][source_col]
      self._grid[source_row][source_col] = EMPTY
      empty_locations.append((source_row, source_col))

    return len(discontented_agents)

  def get_grid(self) -> List[List[int]]:
    return [row.copy() for row in self._grid]

  def get_satisfaction_rate(self) -> float:
    agent_count = 0
    satisfied_count = 0
    for row in range(self._height):
      for col in range(self._width):
        if self._grid[row][col] != EMPTY:
          agent_count += 1
          if self.is_agent_satisfied(row, col):
            satisfied_count += 1

    if agent_count == 0:
      return 1.0
    return satisfied_count / agent_count
