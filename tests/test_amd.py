import pytest
import shutil

from pharmpy.tools import run_amd

@pytest.mark.tools
def test_amd(proj, tmpdir, test_name, dataset_path, kwargs):
    run_dir = tmpdir(proj.path)
    ref = run_dir.name

    try:
        name = f'amd_{test_name}'
        run_amd(input=dataset_path, project=proj, ref=ref, name=name, **kwargs)
    except Exception:
        raise
    else:
        shutil.rmtree(run_dir / name)

