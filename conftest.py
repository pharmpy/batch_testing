from pathlib import Path
import tomllib

from pharmpy.modeling import read_model


def pytest_addoption(parser):
    parser.addoption('--testdefs')


def pytest_generate_tests(metafunc):
    testdefs = Path(metafunc.config.getoption('testdefs'))
    with open(testdefs, "rb") as f:
        defs = tomllib.load(f)

    model_dir = testdefs.parent / Path(defs['main']['path'])
    if model_dir:
        model_paths = list(Path(model_dir).glob('*.mod'))
    else:
        model_paths = []

    testname = metafunc.function.__name__[5:]
    keep = []
    for model_path in model_paths:
        model_name = model_path.with_suffix('').name
        if model_name in defs:
            model_defs = defs[model_name]
            if testname in model_defs:
                test_defs = model_defs[testname]
                if test_defs.get('skip', False):
                    continue
        keep.append(model_path)

    if 'model_path' in metafunc.fixturenames:
       metafunc.parametrize('model_path', keep)
    elif 'model' in metafunc.fixturenames:
        models = [read_model(model) for model in keep]
        metafunc.parametrize('model', models)
