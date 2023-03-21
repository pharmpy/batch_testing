from pathlib import Path

from pharmpy.model import Model


def pytest_addoption(parser):
    parser.addoption('--model_dir')


def pytest_generate_tests(metafunc):
    model_dir = metafunc.config.getoption('model_dir')
    if model_dir:
        model_paths = list(Path(model_dir).glob('*.mod'))
    else:
        model_paths = []

    if 'model_path' in metafunc.fixturenames:
       metafunc.parametrize('model_path', model_paths)
    elif 'model' in metafunc.fixturenames:
        models = [Model.create_model(model) for model in model_paths]
        metafunc.parametrize('model', models)
