from pharmpy.modeling import read_model, set_additive_error_model, set_combined_error_model, set_proportional_error_model, remove_error_model


def test_remove_error(model_path):
    model = read_model(model_path)
    # validate: remove_error_model doesn't crash
    m2 = remove_error_model(model)
    # validate: remove_error_model does not change the code before the ODE system ($PK)
    assert model.statements.ode_system is None or model.statements.before_odes == m2.statements.before_odes
    # validate: remove_error_model does not change the ODE system
    assert model.statements.ode_system == m2.statements.ode_system


#def test_additive(model_path):
    # Segfaults for some model
#    model = read_model(model_path)
#    set_additive_error_model(model)


#def test_proportional(model_path):
    # Segfaults for some model
#    model = read_model(model_path)
#    set_proportional_error_model(model)


#def test_combined(model_path):
#    model = read_model(model_path)
#    set_combined_error_model(model)
