from pharmpy.modeling import read_model

import re

def find_in_code(model, regex):
    m = re.search(regex, model.code, re.MULTILINE)
    return m


def test_repr(model_path):
    model = read_model(model_path)

    have_pk = find_in_code(model, r'^\s*\$PK')
    if have_pk:
        print(model.name)
        # validate: repr for ODE system does not crash
        assert repr(model.statements.ode_system)
