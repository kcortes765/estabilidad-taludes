from utils.config import load_config, validate_config


def test_load_and_validate_config():
    cfg = load_config()
    validate_config(cfg)
    assert "circle_constraints" in cfg
