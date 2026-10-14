# Contract-Driven, AI-Enhanced Development for _Schelling's Model of Segregation_

## Summary

This project contains the source files for a simple exercise in the use of LLMs&mdash;ideally (but not necessarily) via coding agents&mdash;in completing the technical specification and implementation of a simulation running [Schelling's model of segregation](https://en.wikipedia.org/wiki/Schelling%27s_model_of_segregation).

## Files and exercise flow

- [`schelling_model_base.py`](schelling_model_base.py)

    This is an _abstract base class_ (_ABC_) defining the behavioral contract for an implementation of Schelling's model of segregation. In this context, "contract" should be assumed to mean: "A definition of an abstract object type (`SchellingModelBase`, in this case), with declarations spelling out the return type and parameter types and names of each method (including some decorated with `@abstractmethod`), and with docstrings describing the responsibility and behavior of each."

    This abstract class is intended as the primary artifact around which a conversation with an AI coding agent (or web-based LLM interface) will take place. We suggest that the learner, through a series of one or more prompt-response interactions (see ["Prompts](prompts.md) for some suggestions), resolves any ambiguity or inconsistency that the agent notes in the contract, before proceeding to generate any additional code.

    Note that the above _does not_ mean that the learner should accept the agent's feedback uncritically. Instead, the learner should first read the comments and declarations in `schelling_model_base.py` thoroughly, to be in condition to have a productive conversation with the agent&mdash;which may include modifying the docstring comments or providing clarifications in subsequent prompts, based on the agent's feedback&mdash;or even pushing back to disagree with the agent's analyses or recommendations.

    In any event, any changes to the `SchellingModelBase` class should be limited to the docstring comments, and only to clarify the documented behavior&mdash;not to alter that behavior. Changes to constructor or method declarations or implementations have a significant potential to cause problems in other files in the project; these must be avoided.

    We also recommend that any changes to this file are made by the learner, rather than a coding agent; this helps the learner maintain ownership of the outcome, rather than simply turning the whole thing over to the agent, thus running the risk of ending up with something that the learner doesn't understand.  

- [`schelling_model.py`](schelling_model.py)

    This file includes an (incomplete) definition of the `SchellingModel` class, which extends `SchellingModelBase`. We strongly suggest that this should be the only file that the learner allows an agent to modify directly.

    The `SchellingModel` class is tested by the assertions in `test_schelling_model.py`, and used by the UI code in `gui.py`. A coding agent should be instructed to examine those two files before making any changes to `schelling_model.py`, to avoid inadvertently introducing breaking changes.

    The aims of any changes to `schelling_model.py` are to complete the implementation of the contract documented in `schelling_model_base.py`, so that all tests in `test_schelling_model.py` run successfully, and so that the UI defined in `gui.py` is able to use `SchellingModel` to execute the model logic, so that the simulation can be displayed by the UI.

- [`test_schelling_model.py`](test_schelling_model.py)

    This file defines a number of functions that create an object of the `SchellingModel` type, and invoke methods on the resulting object, verifying that the results match the expectations (according to the contract). In other words, the tests already embody interpretations of the contract spelled out in `SchellingModelBase`; this, this test class should also be examined by the coding agent, in identifying any ambiguities, inconsistencies, or other deficiencies in the contract.

    Any changes to this file (whether by the learner or a coding agent) should only be made for the purpose of closing any gaps in the tests' coverage of the contract.

- [`gui.py`](gui.py)

    This file includes a definition of the `SchellingGUI` class, which manages a simple user interface to control the simulation of the segregation model. The correct operation of this class depends on an implementation of `SchellingModel` that conforms to the contract specified in `SchellingModelBase`. Given this, the learner may wish to direct a coding agent to examine this file as part of examining the contract; however, we strongly recommend that the agent not be permitted to make changes to this file.

See ["Prompts"](prompts.md) for some suggested prompts for use with a coding agent or (with the necessary context provided through upload or copy & paste) a web-facing interface to an LLM model. 

## Credits, copyrights, and license information

The starter code and documentation for this exercise is &copy; 2026 Nicholas Bennett.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

<http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.