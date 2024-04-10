from pathlib import Path

import pytest

from pharmpy.modeling import read_model


def test_models(model_path):
    f = model_path
    model = read_model(f)
    print(model.name)

    # Test round-trip
    #with open(f, 'r', encoding='latin-1') as fh:
    #    content = fh.read()
    #assert content == str(model)
