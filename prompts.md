# Suggested Prompts

## Validation and Contract Review

### Prompt

> Act as a senior software architect and domain modeler. Read this abstract base class and docstrings for a Schelling Segregation simulation (`schelling_model_base.py`). Identify unhandled edge cases, potential division-by-zero risks, boundary condition problems, and logical ambiguities in the specification before we write code.

### Context

- `schelling_model_base.py`

## Prompt 2: Validation & Contract Review

## Prompt 2: Verification-First Implementation

> Implement a concrete class `SchellingModel` inheriting from `SchellingModelBase` in `model_impl.py` using standard Python library data structures only (no external dependencies). Ensure you explicitly protect against zero-neighbor division by zero, use a bounded 8-cell Moore neighborhood, and implement asynchronous or synchronous relocation cleanly as documented.

## Prompt 3: Debugging Integration Failures

> My simulation fails the test harness with the following error output: [PASTE TEST ERROR / TRACEBACK]. Analyze the discrepancy between the test assertion and `model_impl.py`, identify the root cause, and provide the corrected method.
