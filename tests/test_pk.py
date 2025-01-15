import re

from pharmpy.modeling import read_model, has_first_order_absorption


def find_in_code(model, regex):
    m = re.search(regex, model.code, re.MULTILINE)
    return bool(m)


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
