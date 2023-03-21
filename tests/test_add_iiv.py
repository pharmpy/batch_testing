from pharmpy.modeling import add_iiv


def test_add_iiv(model):
    mod_ori = model.model_code
    first_symbol = model.statements[0].symbol.name
    model = add_iiv(model, first_symbol, 'exp')
    assert model.model_code != mod_ori
