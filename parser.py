from pathlib import Path

from pharmpy import Model
from pharmpy.plugins.utils import PluginError
from pharmpy.modeling import explicit_odes

model_dir = Path('/home/rikard/devel/scripts/pharmpy_testing/models')
#model_dir = Path('/home/rikard/devel/scripts/pharmpy_testing/ddmore')

n = 0
failed = 0


def test_models():
    global n, failed
    for f in model_dir.iterdir():
        n += 1
        try:
            model = Model(f)
        except PluginError:
            continue
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
            failed += 1

        # Test explicit_odes transformation
        explicit_odes(model)

print(f'{n} models tested')
print(f'{failed} models failed in statements')
