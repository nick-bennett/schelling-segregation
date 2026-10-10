"""
test_engine.py
Deterministic unit checks to verify model implementation before attaching to UI.
"""
from random import Random

# Import the student concrete class
from model_impl import SchellingModel

from model_base import EMPTY, GROUP_A, GROUP_B


def test_zero_neighbor_satisfaction():
  model = SchellingModel(width=3, height=3, tolerance=0.5, rng = Random(0))
  # Clear grid
  model.grid = [[EMPTY] * 3 for _ in range(3)]
  # Place a single agent in the center
  model.grid[1][1] = GROUP_A

  assert model.is_agent_satisfied(1, 1) is True, (
    "Edge case failed: Isolated agent with 0 occupied neighbors must be satisfied."
  )
  print("✓ Zero-neighbor edge case passed.")


def test_satisfaction_threshold_logic():
  model = SchellingModel(width=3, height=3, density=1.0, tolerance=0.5)
  # Center agent surrounded by 3 like-agents and 5 opposite-agents
  # Ratio = 3 / 8 = 0.375 -> Below 0.5 threshold -> Discontent
  model.grid = [
    [GROUP_B, GROUP_B, GROUP_B],
    [GROUP_A, GROUP_A, GROUP_B],
    [GROUP_A, GROUP_A, GROUP_B]
  ]

  assert model.is_agent_satisfied(1, 1) is False, (
    "Center agent should be discontent (3/8 < 0.5)."
  )

  # Change tolerance to 0.3
  model.tolerance = 0.3
  assert model.is_agent_satisfied(1, 1) is True, (
    "Center agent should be satisfied under relaxed tolerance (3/8 >= 0.3)."
  )
  print("✓ Neighborhood threshold logic passed.")


def test_relocation_count():
  model = SchellingModel(width=3, height=3, tolerance=0.8)
  model.repopulate(0.5)
  moves = model.step()
  assert isinstance(moves, int), "step() must return an integer move count."
  print("✓ Step relocation return type passed.")


if __name__ == "__main__":
  print("Running deterministic verification suite...")
  test_zero_neighbor_satisfaction()
  test_satisfaction_threshold_logic()
  test_relocation_count()
  print("\nAll verification tests passed successfully!")
