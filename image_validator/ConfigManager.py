import yaml
import os
import typer

class ConfigManager:
    def __init__(self, config_path):
        if not os.path.exists(config_path):
            typer.echo(f"Config file not found at {config_path}")
            exit()
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)