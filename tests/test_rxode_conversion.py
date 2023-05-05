from pharmpy.plugins.rxode import verification

def test_rxode_conversion(model):
    assert verification(model, f'batch_verification/{model.name}')