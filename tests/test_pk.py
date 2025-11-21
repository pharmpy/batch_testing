import re

import pytest

from pharmpy.modeling import read_model, has_first_order_absorption, has_linear_odes, has_odes, has_linear_odes_with_real_eigenvalues, has_first_order_elimination


def find_in_code(model, regex):
    m = re.search(regex, model.code, re.MULTILINE)
    return bool(m)


def find_advan(model):
    m = re.search(r'ADVAN(\d+)', model.code, re.MULTILINE)
    if m is None:
        return m
    else:
        return int(m.group(1))


def has_pk(model):
    pk = find_in_code(model, r"^\s*\$PK")
    return pk


def test_has_first_order_absorption(model_path):
    model = read_model(model_path)
    has_advan1 = find_in_code(model, r"ADVAN1\D")
    has_advan2 = find_in_code(model, r"ADVAN2\D")
    has_advan3 = find_in_code(model, r"ADVAN3\D")
    has_advan4 = find_in_code(model, r"ADVAN4\D")
    has_advan11 = find_in_code(model, r"ADVAN11\D")
    has_advan12 = find_in_code(model, r"ADVAN12\D")
    # validate: has_first_order_absorption does not raise
    fo_abs = has_first_order_absorption(model)
    # validate: has_first_order_absorption always returns either True or False
    assert fo_abs is True or fo_abs is False
    # validate: has_first_order_absorption detects no first order absorption for ADVAN1 models
    assert has_advan1 and not fo_abs or not has_advan1
    # validate: has_first_order_absorption detects first order absorption for ADVAN2 models
    assert has_advan2 and fo_abs or not has_advan2
    # validate: has_first_order_absorption detects no first order absorption for ADVAN3 models
    assert has_advan3 and not fo_abs or not has_advan3
    # validate: has_first_order_absorption detects first order absorption for ADVAN4 models
    assert has_advan4 and fo_abs or not has_advan4
    # validate: has_first_order_absorption detects no first order absorption for ADVAN11 models
    assert has_advan11 and not fo_abs or not has_advan11
    # validate: has_first_order_absorption detects first order absorption for ADVAN12 models
    assert has_advan12 and fo_abs or not has_advan12
    # validate: has_first_order_absorption gives False for non-PK models
    assert (not has_pk(model) and not fo_abs) or has_pk(model)


def test_has_first_order_elimination(model_path):
    model = read_model(model_path)
    has_advan1 = find_in_code(model, r"ADVAN1\D")
    has_advan2 = find_in_code(model, r"ADVAN2\D")
    has_advan3 = find_in_code(model, r"ADVAN3\D")
    has_advan4 = find_in_code(model, r"ADVAN4\D")
    has_advan11 = find_in_code(model, r"ADVAN11\D")
    has_advan12 = find_in_code(model, r"ADVAN12\D")
    # validate: has_first_order_elimination does not raise
    fo_elim = has_first_order_elimination(model)
    # validate: has_first_order_elimination always returns either True or False
    assert fo_elim is True or fo_elim is False
    # validate: has_first_order_elimination detects first order elimination for ADVAN1 models
    assert has_advan1 and fo_elim or not has_advan1
    # validate: has_first_order_elimination detects first order elimination for ADVAN2 models
    assert has_advan2 and fo_elim or not has_advan2
    # validate: has_first_order_elimination detects first order elimination for ADVAN3 models
    assert has_advan3 and fo_elim or not has_advan3
    # validate: has_first_order_elimination detects first order elimination for ADVAN4 models
    assert has_advan4 and fo_elim or not has_advan4
    # validate: has_first_order_elimination detects first order elimination for ADVAN11 models
    assert has_advan11 and fo_elim or not has_advan11
    # validate: has_first_order_elimination detects first order elimination for ADVAN12 models
    assert has_advan12 and fo_elim or not has_advan12
    # validate: has_first_order_elimination gives False for non-PK models
    assert (not has_pk(model) and not fo_elim) or has_pk(model)


def test_has_linear_odes(model_path):
    model = read_model(model_path)
    advan = find_advan(model)
    linear_odes = has_linear_odes(model)
    linear_advans = (1, 2, 3, 4, 5, 7, 11, 12)
    # validate: has_linear_odes Gives True for all linear advans (1, 2, 3, 4, 5, 6, 11 and 12)
    assert advan in linear_advans and linear_odes is True or advan not in linear_advans
    # validate: has_linear_odes Gives False if model has no ode system
    assert advan is None and linear_odes is False or advan is not None


def test_has_odes(model_path):
    model = read_model(model_path)
    pk = find_in_code(model, r"^\s*\$PK")
    odes = has_odes(model)
    # validate: has_odes Gives True if model has $PK and False otherwise
    assert pk and odes is True or not pk and odes is False


@pytest.mark.timeout(10)
def test_has_linear_odes_with_real_eigenvalues(model_path):
    model = read_model(model_path)
    advan = find_advan(model)
    # validate: has_linear_odes_with_real_eigenvalues does not take longer than 10s to terminate
    real = has_linear_odes_with_real_eigenvalues(model)
    trivial_advans = (1, 2, 3, 4, 11, 12)
    # validate: has_linear_odes_with_real_eigenvalues gives True for advans 1, 2, 3, 4, 11 and 12
    assert advan in trivial_advans and real is True or advan not in trivial_advans
