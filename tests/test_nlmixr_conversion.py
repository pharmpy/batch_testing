from pharmpy.plugins.nlmixr import verification

def test_nlmixr_conversion(model):
    assert verification(model, f'batch_verification/{model.name}')