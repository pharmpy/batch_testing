from pathlib import Path

import pytest

from pharmpy.modeling import read_model


def test_models(model_path):
    # validate: read_model does not crash
    model = read_model(model_path)

    # Test round-trip
    with open(model_path, 'r', encoding='latin-1') as fh:
        content = fh.read()
    assert content == model.code
    # validate: read_model can parse a NONMEM control stream so that the model code is not altered
