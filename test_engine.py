"""
test_engine.py
Deterministic unit checks to verify model implementation before attaching to UI.
"""
from collections import Counter
from random import Random

# Import the student concrete class
from model_impl import SchellingModel

from model_base import EMPTY, GROUP_A, GROUP_B


def assert_raises(exception_type, callable_, *args, **kwargs):
  try:
    callable_(*args, **kwargs)
  except exception_type:
    return
  raise AssertionError(f"Expected {exception_type.__name__} to be raised.")


def test_zero_neighbor_satisfaction():
  model = SchellingModel.from_grid([
    [EMPTY, EMPTY, EMPTY],
    [EMPTY, GROUP_A, EMPTY],
    [EMPTY, EMPTY, EMPTY]
  ], tolerance=0.5, rng=Random(0))

  assert model.is_agent_satisfied(1, 1) is True, (
    "Edge case failed: Isolated agent with 0 occupied neighbors must be satisfied."
  )
  print("✓ Zero-neighbor edge case passed.")


def test_empty_cell_satisfaction_raises_value_error():
  model = SchellingModel.from_grid([
    [EMPTY]
  ], tolerance=0.5, rng=Random(0))

  assert_raises(ValueError, model.is_agent_satisfied, 0, 0)
  print("✓ Empty-cell satisfaction error passed.")


def test_satisfaction_threshold_logic():
  # Center agent surrounded by 3 like-agents and 5 opposite-agents
  # Ratio = 3 / 8 = 0.375 -> Below 0.5 threshold -> Discontent
  model = SchellingModel.from_grid([
    [GROUP_B, GROUP_B, GROUP_B],
    [GROUP_A, GROUP_A, GROUP_B],
    [GROUP_A, GROUP_A, GROUP_B]
  ], tolerance=0.5, rng=Random(0))

  assert model.is_agent_satisfied(1, 1) is False, (
    "Center agent should be discontent (3/8 < 0.5)."
  )

  # Change tolerance to 0.3
  model.tolerance = 0.3
  assert model.is_agent_satisfied(1, 1) is True, (
    "Center agent should be satisfied under relaxed tolerance (3/8 >= 0.3)."
  )
  print("✓ Neighborhood threshold logic passed.")


def test_exact_satisfaction_threshold_is_inclusive():
  model = SchellingModel.from_grid([
    [GROUP_A, GROUP_A, GROUP_B]
  ], tolerance=0.5, rng=Random(0))

  assert model.is_agent_satisfied(0, 1) is True, (
    "An agent whose same-group neighbor ratio equals tolerance must be satisfied."
  )
  print("✓ Inclusive satisfaction threshold passed.")


def test_bounded_edges_do_not_wrap():
  model = SchellingModel.from_grid([
    [GROUP_A, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, GROUP_B]
  ], tolerance=1.0, rng=Random(0))

  assert model.is_agent_satisfied(0, 0) is True, (
    "The upper-left agent must not treat the opposite corner as a neighbor."
  )
  assert model.is_agent_satisfied(2, 2) is True, (
    "The lower-right agent must not treat the opposite corner as a neighbor."
  )
  print("✓ Bounded non-toroidal edges passed.")


def test_empty_grid_satisfaction_rate():
  model = SchellingModel(width=2, height=2, tolerance=0.5, rng=Random(0))

  assert model.get_satisfaction_rate() == 1.0, (
    "A grid containing no agents must have satisfaction rate 1.0."
  )
  print("✓ Empty-grid satisfaction rate passed.")


def test_known_mixed_grid_satisfaction_rate():
  model = SchellingModel.from_grid([
    [GROUP_A, GROUP_A, GROUP_B, EMPTY]
  ], tolerance=0.5, rng=Random(0))

  assert model.get_satisfaction_rate() == 2 / 3, (
    "Exactly two of the three agents should be satisfied."
  )
  print("✓ Known mixed-grid satisfaction rate passed.")


def test_relocation_count():
  model = SchellingModel.from_grid([
    [GROUP_A, GROUP_B, EMPTY]
  ], tolerance=1.0, rng=Random(0))
  before = Counter(cell for row in model.get_grid() for cell in row)

  moves = model.step()
  after = Counter(cell for row in model.get_grid() for cell in row)

  assert moves == 2, (
    "Both initially discontented agents must move when a vacated cell can be "
    "reused during the step."
  )
  assert after == before, "Relocation must preserve all cell-state counts."
  print("✓ Step relocation count and population invariants passed.")


def test_stable_and_blocked_step_results():
  stable = SchellingModel.from_grid([
    [GROUP_A, GROUP_A, EMPTY]
  ], tolerance=1.0, rng=Random(0))
  blocked = SchellingModel.from_grid([
    [GROUP_A, GROUP_B]
  ], tolerance=1.0, rng=Random(0))

  assert stable.step() == 0, "A fully satisfied grid must report no moves."
  assert blocked.step() == -1, (
    "A grid with discontented agents and no empty cells must report -1."
  )
  print("✓ Stable and blocked step results passed.")


def test_full_satisfied_grid_returns_zero_moves():
  model = SchellingModel.from_grid([
    [GROUP_A, GROUP_A]
  ], tolerance=1.0, rng=Random(0))

  assert model.step() == 0, (
    "A full grid with no discontented agents must report zero moves."
  )
  print("✓ Full satisfied-grid step result passed.")


def test_seeded_steps_are_reproducible():
  grid = [
    [GROUP_A, GROUP_B, EMPTY],
    [GROUP_B, GROUP_A, EMPTY]
  ]
  first = SchellingModel.from_grid(grid, tolerance=1.0, rng=Random(7))
  second = SchellingModel.from_grid(grid, tolerance=1.0, rng=Random(7))

  first_moves = first.step()
  second_moves = second.step()

  assert first_moves == second_moves, (
    "Models using identically seeded random generators must move equal counts."
  )
  assert first.get_grid() == second.get_grid(), (
    "Models using identically seeded random generators must step identically."
  )
  print("✓ Seeded step reproducibility passed.")


def test_initial_grid_is_empty():
  model = SchellingModel(width=3, height=2, tolerance=0.5, rng=Random(0))

  assert model.get_grid() == [
    [EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY]
  ], "A newly constructed model must contain an all-EMPTY grid."
  print("✓ Initial empty-grid state passed.")


def test_constructor_and_tolerance_validation():
  for invalid_width in (0, -1, 1.5, True):
    assert_raises(
        ValueError, SchellingModel,
        width=invalid_width, height=2, tolerance=0.5
    )
  for invalid_height in (0, -1, 1.5, True):
    assert_raises(
        ValueError, SchellingModel,
        width=2, height=invalid_height, tolerance=0.5
    )
  for invalid_tolerance in (-0.01, 1.01, float("nan"), float("inf"), True):
    assert_raises(
        ValueError, SchellingModel,
        width=2, height=2, tolerance=invalid_tolerance
    )

  model = SchellingModel(width=2, height=2, tolerance=0.5)
  for invalid_tolerance in (-0.01, 1.01, float("nan"), float("inf"), True):
    assert_raises(ValueError, setattr, model, "tolerance", invalid_tolerance)
  print("✓ Constructor and tolerance validation passed.")


def test_repopulate_validation_and_endpoints():
  model = SchellingModel(width=3, height=2, tolerance=0.5, rng=Random(0))

  for invalid_density in (-0.01, 1.01, float("nan"), float("inf"), True):
    assert_raises(ValueError, model.repopulate, invalid_density)

  model.repopulate(0.0)
  assert all(cell == EMPTY for row in model.get_grid() for cell in row)
  model.repopulate(1.0)
  assert all(cell != EMPTY for row in model.get_grid() for cell in row)
  print("✓ Repopulation validation and endpoints passed.")


def test_seeded_repopulation_is_reproducible():
  first = SchellingModel(width=4, height=4, tolerance=0.5, rng=Random(7))
  second = SchellingModel(width=4, height=4, tolerance=0.5, rng=Random(7))

  first.repopulate(0.5)
  second.repopulate(0.5)

  assert first.get_grid() == second.get_grid(), (
    "Models using identically seeded random generators must repopulate identically."
  )
  print("✓ Seeded repopulation reproducibility passed.")


def test_grid_copies_are_safe():
  source = [
    [GROUP_A, EMPTY],
    [EMPTY, GROUP_B]
  ]
  model = SchellingModel.from_grid(source, tolerance=0.5, rng=Random(0))
  source[0][0] = GROUP_B

  snapshot = model.get_grid()
  snapshot[0][0] = EMPTY
  snapshot.append([GROUP_A, GROUP_A])

  assert model.get_grid() == [
    [GROUP_A, EMPTY],
    [EMPTY, GROUP_B]
  ], "Input and returned-grid mutations must not change model state."
  print("✓ Safe grid copies passed.")


def test_from_grid_validation():
  assert_raises(ValueError, SchellingModel.from_grid, [], tolerance=0.5)
  assert_raises(
      ValueError, SchellingModel.from_grid,
      [[EMPTY], [EMPTY, GROUP_A]], tolerance=0.5
  )
  assert_raises(
      ValueError, SchellingModel.from_grid,
      [[EMPTY, 99]], tolerance=0.5
  )
  print("✓ Grid factory validation passed.")


if __name__ == "__main__":
  print("Running deterministic verification suite...")
  test_zero_neighbor_satisfaction()
  test_empty_cell_satisfaction_raises_value_error()
  test_satisfaction_threshold_logic()
  test_exact_satisfaction_threshold_is_inclusive()
  test_bounded_edges_do_not_wrap()
  test_empty_grid_satisfaction_rate()
  test_known_mixed_grid_satisfaction_rate()
  test_relocation_count()
  test_stable_and_blocked_step_results()
  test_full_satisfied_grid_returns_zero_moves()
  test_seeded_steps_are_reproducible()
  test_initial_grid_is_empty()
  test_constructor_and_tolerance_validation()
  test_repopulate_validation_and_endpoints()
  test_seeded_repopulation_is_reproducible()
  test_grid_copies_are_safe()
  test_from_grid_validation()
  print("\nAll verification tests passed successfully!")
