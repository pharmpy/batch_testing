from pathlib import Path

import pytest

from pharmpy import Model
from pharmpy.plugins.utils import PluginError
from pharmpy.modeling import explicit_odes

model_dir = Path(__file__).parent / 'models'
ddmore_dir = Path(__file__).parent / 'ddmore'

models = []
if model_dir.exists():
    models += list(model_dir.iterdir())
if ddmore_dir.exists():
    models += list(ddmore_dir.iterdir())


@pytest.mark.parametrize('path', models)
def test_models(path):
    f = path
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

    # Test explicit_odes transformation
    explicit_odes(model)
