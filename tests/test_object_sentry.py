from object_sentry import ObjectSentry, ObjectDetectionModel

def test_get_available_models():
    object_sentry = ObjectSentry()
    available_models = object_sentry.get_available_models()
    assert available_models == ["Model1", "Model2"]

def test_select_model():
    object_sentry = ObjectSentry()
    model = object_sentry.select_model("Model1")
    assert model.name == "Model1"
    assert model.config == {"param1": 1, "param2": 2}

def test_select_model_not_found():
    object_sentry = ObjectSentry()
    try:
        object_sentry.select_model("Model3")
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == "Model not found"

def test_configure_model():
    object_sentry = ObjectSentry()
    model = object_sentry.configure_model("Model1", {"new_param": 1})
    assert model.name == "Model1"
    assert model.config == {"new_param": 1}

def test_configure_model_invalid_config():
    object_sentry = ObjectSentry()
    try:
        object_sentry.configure_model("Model1", "invalid_config")
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == "Invalid config"

def test_validate_model_config():
    object_sentry = ObjectSentry()
    is_valid = object_sentry.validate_model_config("Model1", {"valid_config": 1})
    assert is_valid

def test_validate_model_config_invalid():
    object_sentry = ObjectSentry()
    try:
        object_sentry.validate_model_config("Model1", "invalid_config")
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == "Invalid config"
