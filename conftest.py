import os
import pytest
import tomllib
from pathlib import Path
from tempfile import mkdtemp

from pharmpy.internals.fs.path import path_absolute
from pharmpy.modeling import read_model
from pharmpy.tools import open_project


def pytest_addoption(parser):
    parser.addoption('--testdefs')


def pytest_generate_tests(metafunc):
    testdefs = Path(metafunc.config.getoption('testdefs'))
    with open(testdefs, "rb") as f:
        defs = tomllib.load(f)

    test_markers = [m.name for m in metafunc.definition.iter_markers()]
    mark_expr = metafunc.config.option.markexpr
    if mark_expr and 'tools' == mark_expr:
        if 'tools' in test_markers:
            generate_tool_tests(defs, metafunc)
        else:
            return
    else:
        if mark_expr and 'not tools' in mark_expr or not mark_expr:
            generate_model_tests(testdefs, defs, metafunc)
        else:
            return


def generate_model_tests(testdefs, defs, metafunc):
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


def generate_tool_tests(defs, metafunc):
    project_name = defs['main']['project_name']
    project_ref = defs['main']['project_ref']
    proj = open_project(project_name, ref=project_ref)

    test_names, dataset_paths, kwargs = [], [], []
    for key, value in defs.items():
        if key == 'main':
            continue

        test_names.append(key)

        dataset_path = path_absolute(Path(defs['main']['path']) / value['dataset_path'])
        dataset_paths.append(dataset_path)

        kwargs_item = value.copy()
        del kwargs_item['dataset_path']
        kwargs.append(kwargs_item)

    options = list(zip([proj]*len(test_names),test_names,dataset_paths,kwargs))
    metafunc.parametrize('proj,test_name,dataset_path,kwargs', options)

@pytest.fixture(scope="session")
def tmpdir(request):
    state = {"instance": None}

    def _get_or_create_instance(path=None):
        if state["instance"] is None:
            assert path is not None
            dir_name = mkdtemp(dir=path)
            state["instance"] = Path(dir_name)
        return state["instance"]

    def teardown():
        path = state["instance"]
        if path is not None and not any(path.iterdir()):
            if request.session.testsfailed == 0:
                os.rmdir(path)

    request.addfinalizer(teardown)
    return _get_or_create_instance
