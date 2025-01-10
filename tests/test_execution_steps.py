import re

from pharmpy.modeling import read_model, remove_parameter_uncertainty_step


def find_in_code(model, regex):
    m = re.search(regex, model.code, re.MULTILINE)
    return m


def test_remove_parameter_uncertainty_step(model_path):
    model = read_model(model_path)

    have_cov = find_in_code(model, r'^\$COV')
    m2 = remove_parameter_uncertainty_step(model)
    have_cov2 = find_in_code(m2, r'^\$COV')
    # validate: remove_parameter_uncertainty_step does not change the model if it didn't have $COV
    # validate: remove_parameter_uncertainty_step removes $COV
    assert not have_cov and m2.code == model.code or have_cov and not have_cov2
