from pharmpy.modeling import read_model


def test_repr(model_path):
    model = read_model(model_path)

    # validate: repr for model.statements produces something
    assert repr(model.statements)
