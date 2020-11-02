#import argparse
from pathlib import Path

import pytest

from pharmpy import Model
from pharmpy.plugins.utils import PluginError
from pharmpy.modeling import explicit_odes


def test_models(model_path):
    f = model_path
    try:
        model = Model(f)
    except PluginError:
        return
    print(model.name)

    # Test round-trip
    with open(f, 'r', encoding='latin-1') as fh:
        content = fh.read()
    assert content == str(model)

    # Parse parameters
    params = model.parameters

    # Parse PK/PRED/ERROR
    try:
        statements = model.statements
    except Exception as e:
        print(e)


def test_explicit_odes(model):
    explicit_odes(model)
