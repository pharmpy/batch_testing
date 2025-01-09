import pytest
import re

from pharmpy.modeling import add_covariate_effect


#def test_covariate_effect(model):
#    print(model.source.path)
#    cov = str(model.dataset.select_dtypes(include=['float64']).columns[-2])
#    param = model.statements[3].symbol.name
#    print(param)
#    print(cov)
#    try:
#        add_covariate_effect(model, param, cov, 'exp')
#    except ValueError:
#        add_covariate_effect(model, param, cov, 'cat')
#    model.update_source()
#    assert re.search(f'{param}{cov}', str(model))

