from pharmpy.tools import read_modelfit_results


def test_models(model_path):
    if model_path.with_suffix('.lst').is_file():

        # validate: read_modelfit_results does not crash
        model = read_modelfit_results(model_path)
