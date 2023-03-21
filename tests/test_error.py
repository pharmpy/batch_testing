from pharmpy.modeling import set_additive_error_model, set_combined_error_model, set_proportional_error_model, remove_error_model


def test_remove(model):
    remove_error_model(model)


def test_additive(model):
    set_additive_error_model(model)


def test_proportional(model):
    set_proportional_error_model(model)


def test_combined(model):
    set_combined_error_model(model)
