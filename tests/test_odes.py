import pytest

from pharmpy import Model
from pharmpy.modeling import explicit_odes, zero_order_absorption

def test_explicit_odes(model):
    explicit_odes(model)

def test_zero_order_absorption(model):
    zero_order_absorption(model)

