from pharmpy.tools import read_modelfit_results


def test_models(model_path):
    ext_path =  model_path.with_suffix('.ext')
    if ext_path.is_file():

        # validate: read_modelfit_results does not crash
        res = read_modelfit_results(model_path)

        with open(ext_path, 'r') as fh:
            lines = fh.readlines()

        for line in lines:
            if line.startswith("  -1000000000"):
                ofv = float(line.split()[-1])
                # validate: read_modelfit_results retrieves ofv correctly
                assert res.ofv == ofv
                break
