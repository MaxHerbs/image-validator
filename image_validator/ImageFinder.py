import re
import typer
import os
from .SearchMethods import SearchMethods

class ImageFinder:
    files_to_search = []
    detected_image_paths = []
    invalid_image_paths = []


    def __init__(self, descriptor: dict):
        self.descriptor = descriptor

    def validate(self) -> int:
        self.populate_paths()
        print(self.files_to_search)
        typer.echo(f"Found {len(self.files_to_search)} files to look inside.")


        requestedSearches = self.descriptor["searchTypes"]
        typer.echo(f"Trying to search with {len(requestedSearches)} search types")

        searchEngine = SearchMethods(requestedSearches, self.files_to_search)
      
        print(f"Detected {len(searchEngine.detected_image_paths)} image paths")

        img_dir_base = self.descriptor["imgbasePath"]
        if not img_dir_base.endswith("/"):
            img_dir_base += "/"

        self.detected_image_paths = [img_dir_base + path[1::] for path in searchEngine.detected_image_paths]

        self.validate_image_paths()
        if self.invalid_image_paths:
            typer.echo("The following image paths are invalid:")
            for path in self.invalid_image_paths:
                typer.echo(path)
            return 0
        
        typer.echo("All image paths are valid!")
        return 1

        


    def validate_image_paths(self) -> None:
        typer.echo("Validating image paths")
        for path in self.detected_image_paths:
            if not os.path.exists(path):
                self.invalid_image_paths.append(path)



    def populate_paths(self) -> None:
        active_dirs = self.descriptor["directories"]

        for dir in active_dirs:
            self.dir_walk(dir["dir"], dir.pop("fileTypes", ["*"]))


    def dir_walk(self, dir: str, file_types: list) -> None:
        print("Looking in", dir)
        print("File types", file_types)
        curr_dir = os.listdir(dir)
        for file in curr_dir:
            file_path = dir + "/" + file
            if os.path.isdir(file_path):
                self.dir_walk(file_path, file_types)
            elif "*" in file_types:
                self.files_to_search.append(file_path)
            else:
                if not "." in file:
                    continue
                this_type = file.split(".")[-1]
                if this_type in file_types:
                    self.files_to_search.append(file_path)



