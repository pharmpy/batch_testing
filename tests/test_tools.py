import pytest
import shutil

from pharmpy.tools import run_tool

@pytest.mark.tools
def test_tool(proj, tmpdir, test_name, tool_name, kwargs):
    run_dir = tmpdir(proj.path)
    ref = run_dir.name

    try:
        name = f'{tool_name}_{test_name}'
        run_tool(tool_name, project=proj, ref=ref, name=name, seed=12345, **kwargs)
    except Exception:
        raise
    else:
        shutil.rmtree(run_dir / name)

