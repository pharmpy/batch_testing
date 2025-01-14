import re

from pharmpy.model import EstimationStep
from pharmpy.modeling import read_model, remove_parameter_uncertainty_step


def find_in_code(model, regex):
    m = re.search(regex, model.code, re.MULTILINE)
    return m


def find_last_estimation_step(model):
    steps = model.execution_steps
    found = None
    for step in reversed(steps):
        if isinstance(step, EstimationStep):
            found = step
            break
    return found


def test_remove_parameter_uncertainty_step(model_path):
    model = read_model(model_path)

    have_cov = find_in_code(model, r'^\$COV')
    m2 = remove_parameter_uncertainty_step(model)
    have_cov2 = find_in_code(m2, r'^\$COV')
    eststep = find_last_estimation_step(m2)
    # validate: remove_parameter_uncertainty_step unsets parameter_uncertainty_method if execution steps exist
    # validate: remove_parameter_uncertainty_step doesn't change Model.execution_steps if model had no execution step
    assert eststep is not None and eststep.parameter_uncertainty_method is None or eststep is None and model.execution_steps == m2.execution_steps
    # validate: remove_parameter_uncertainty_step does not change the model if it didn't have $COV
    # validate: remove_parameter_uncertainty_step removes $COV
    assert not have_cov and m2.code == model.code or have_cov and not have_cov2
