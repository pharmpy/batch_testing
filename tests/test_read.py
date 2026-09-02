import re
from pathlib import Path

import pytest

from pharmpy.model import EstimationStep, SimulationStep
from pharmpy.modeling import get_model_code, get_omegas, get_sigmas, get_thetas, read_model, set_name, set_description


def find_in_code(model, regex):
    m = re.search(regex, model.code, re.MULTILINE)
    return m


def count_in_code(model, regex):
    m = re.findall(regex, model.code, re.MULTILINE)
    return len(m)


def get_record(model, name):
    m = re.search(fr"^\s*\${name}(.*)$", model.code, re.MULTILINE)
    content = m.group(1).strip()
    return content


def test_models(model_path):
    # validate: read_model Does not crash
    model = read_model(model_path)

    # validate: read_model Model has its name attribute set to the file name without extension
    assert model_path.stem == model.name

    # validate: read_model Model.description is taken from $PROBLEM
    assert model.description == get_record(model, "(?:PROBLEM|PROB)")

    # Test round-trip
    with open(model_path, 'r', encoding='latin-1') as fh:
        content = fh.read()
    # validate: read_model can parse a NONMEM control stream so that the model code is not altered
    assert content == model.code
    # validate: get_model_code returns the model code
    assert get_model_code(model) == content


    have_error = find_in_code(model, r'^\$ERROR')
    # validate: read_model A NONMEM model with $ERROR will have statements in model.statements.after_odes
    # validate: read_model A NONMEM model without $ERROR will not have statements in model.statements.after_odes
    assert have_error and len(model.statements.after_odes) > 0 or not have_error and len(model.statements.after_odes) == 0

    # validate: read_model A NONMEM model with $ERROR will have statements in model.statements.error
    # validate: read_model A NONMEM model without $ERROR will have all statements also in model.statements.error
    assert have_error and len(model.statements.error) > 0 or not have_error and model.statements.error == model.statements

    have_pk = find_in_code(model, r'^\s*\$PK')
    # validate: read_model A NONMEM model with $PK have an ode system
    # validate: read_model A NONMEM model without $PK have no ode system
    assert have_pk and model.statements.ode_system is not None or not have_pk and model.statements.ode_system is None

    have_theta = find_in_code(model, r'^\$THETA')
    nthetas = len(get_thetas(model))
    # validate: read_model A NONMEM model having THETAs will have thetas
    # validate: read_model A NONMEM model without THETAs will have no thetas
    assert have_theta and nthetas > 0 or not have_theta and nthetas == 0

    # validate: read_model All NONMEM models have at least one omega
    assert len(get_omegas(model)) > 0

    # validate: read_model All NONMEM models have at least one sigma
    assert len(get_sigmas(model)) > 0

    # validate: read_model All NONMEM models have at least one eta
    assert len(model.random_variables.etas) > 0

    # validate: read_model All NONMEM models have at least one epsilon
    assert len(model.random_variables.epsilons) > 0

    # validate: read_model All $ESTIMATION are parsed
    nests_nonmem = count_in_code(model, r'^\$EST')
    nests_pharmpy = len([step for step in model.execution_steps if isinstance(step, EstimationStep)])
    assert nests_nonmem == nests_pharmpy

    # validate: read_model All $SIMULATION are parsed
    nsims_nonmem = count_in_code(model, r'^\$SIM;')
    nsims_pharmpy = len([step for step in model.execution_steps if isinstance(step, SimulationStep)])
    assert nsims_nonmem == nsims_pharmpy

    # validate: read_model $COV is parsed
    have_cov = find_in_code(model, r'^\$COV')
    param_uncert = model.execution_steps[-1].parameter_uncertainty_method
    assert bool(have_cov) == (param_uncert is not None)

    # validate: read_model A model compares equal to itself
    assert model == model

    # validate: set_name Creates a model with the new name
    new_name = "My new name"
    old_name = model.name
    model2 = set_name(model, new_name)
    assert model2.name == new_name

    # validate: set_name Original model keeps its name
    assert model.name == old_name

    # validate: set_description Creates a model with the new description
    new_description = "This is my model"
    old_description = model.description
    model2 = set_description(model, new_description)
    assert model2.description == new_description

    # validate: set_description Original model keeps its description
    assert model.description == old_description
