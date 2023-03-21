from pathlib import Path

import pytest

from pharmpy.model import Model
from pharmpy.plugins.utils import PluginError


def test_models(model_path):
    model = Model.create_model(model_path)

    # Test round-trip
    with open(model_path, 'r', encoding='latin-1') as fh:
        content = fh.read()
    assert content == model.model_code
