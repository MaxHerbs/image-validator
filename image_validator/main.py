import typer 
from typing import Optional
from typing_extensions import Annotated
import os
import subprocess

from .ConfigManager import ConfigManager
from .ImageFinder import ImageFinder

app = typer.Typer()

@app.command()
def print_dir():
    """
    Prints the current directory
    """
    dir = subprocess.run(["pwd"], capture_output=True, text=True).stdout
    typer.echo(dir)



@app.command()
def validate(
    config_path: Annotated[
        Optional[str], 
        typer.Option("-p", "--path", help="Path to a custom config file describing the validation process.")
    ] = ""
) -> bool:
    """
    Validate the images in the current directory
    """
    if not config_path:
        config_path = os.path.join(os.path.dirname(__file__), "internals/config.yaml")

    configManager = ConfigManager(config_path)
    typer.echo(f"Found config file at {config_path}")
    typer.echo("Validating images...")
    imageFinder = ImageFinder(configManager.config)
    success = imageFinder.validate()
    return success