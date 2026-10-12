# Suggested Prompts

## Validation and Contract Review

### Context

- `schelling_model_base.py`

### Prompt

> Act as a senior software architect and domain modeler. Read this abstract base class and docstrings for a Schelling Segregation simulation (`schelling_model_base.py`). Identify unhandled edge cases, potential division-by-zero risks, boundary condition problems, and logical ambiguities in the specification before we write code.

## ??

### Context

- `schelling_model_base.py`
- `test_schelling_model.py`

### Prompt 

> Act as a senior quality engineer. Read this abstract base class and docstrings for a Schelling Segregation simulation (`schelling_model_base.py`). Review the behavioral and technical contract specified in the abstract base class against the tests in `test_schelling_model.py`. Identify contract elements for which there are no tests&mdash;including edge, boundary, and corner cases&mdash;as well as tests that verify behavior that is not specified in the contract.

## Verification-First Implementation

### Context

- `schelling_model_base.py`
- `schelling_model.py`
- `test_schelling_model.py`

### Prompt

> In `schelling_model.py`, complete the implementation of the `SchellingModel` concrete subclass of `SchellingModelBase` (in `schelling_model_base.py`), and verify that the implementation passes the tests defined in `test_schelling_model.py`. Use only types and functions in the Python 3.10+ language and standard library (no external dependencies). Modify _only_ `schelling_model.py`: the contract and tests (in `schelling_model_base.py` and `test_schelling_model.py`, respectively) must not be touched.

## Debugging Test Failures

If you run the tests in the `test_schelling_model.py` script, but one or more of those tests fails, and you can't figure out why, consider a prompt like the following.   

### Context 

- `schelling_model.py`
- `test_schelling_model.py`

### Prompt

> My simulation fails the test harness with the following error output: [PASTE TEST ERROR / TRACEBACK]. Analyze the discrepancy between the test assertion and `schelling_model.py`, identify the root cause, and recommend changes to correct the error.
