import pytest
from sympy import Piecewise

from pharmpy.modeling import add_etas


def test_add_etas(model):
    print(model.source.path)
    mod_ori = str(model)
    first_symbol = model.statements[0].symbol.name
    add_etas(model, first_symbol, 'exp')
    model.update_source()
    assert str(model) != mod_ori

