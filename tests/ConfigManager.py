import pytest 
from image_validator.ConfigManager import ConfigManager

def test_config_manager():
    configManager = ConfigManager("image_validator/internals/config.yaml")
    basePath = configManager.config.pop('imgBasePath', None)

    assert basePath != None

