import re
import typer
import os
from .SearchMethods import SearchMethods

class ImageFinder:
    files_to_search = []

    def __init__(self, descriptor: dict):
        self.descriptor = descriptor

    def validate(self) -> int:
        files_to_search = self.populate_paths()
        print(files_to_search)
        typer.echo(f"Found {len(files_to_search)} files to look inside.")


        requestedSearches = self.descriptor["searchTypes"]
        typer.echo(f"Trying to search with {len(requestedSearches)} search types")

        searchEngine = SearchMethods(requestedSearches, files_to_search)
      
        print(f"Detected {len(searchEngine.detected_image_paths)} image paths")

        img_dir_base = self.descriptor["imgBasePath"]
        if not img_dir_base.endswith("/"):
            img_dir_base += "/"

        detected_image_paths = [img_dir_base + path[1::] for path in searchEngine.detected_image_paths]

        invalid_paths = self.validate_image_paths(detected_image_paths)
        if invalid_paths:
            typer.echo("The following image paths are invalid:")
            for path in invalid_paths:
                typer.echo(path)
            return 0
        
        typer.echo("All image paths are valid!")
        return 1

        


    def validate_image_paths(self, paths) -> list:
        typer.echo("Validating image paths")
        invalid_paths = []
        for path in paths:
            if not os.path.exists(path):
                invalid_paths.append(path)
        return invalid_paths



    def populate_paths(self) -> list:
        active_dirs = self.descriptor["directories"]
        files_to_search = []

        for dir in active_dirs:
            target_dir = dir["dir"]
            file_types = dir.pop("fileTypes", ["*"])
            files_to_search += self.dir_walk(target_dir, file_types)
        return files_to_search


    def dir_walk(self, dir: str, file_types: list) -> list:
        print("Looking in", dir)
        print("File types", file_types)
        curr_dir = os.listdir(dir)
        files = []

        for file in curr_dir:
            file_path = dir + "/" + file
            if os.path.isdir(file_path):
                files += self.dir_walk(file_path, file_types)
            elif "*" in file_types:
                files.append(file_path)
            else:
                if not "." in file:
                    continue
                this_type = file.split(".")[-1]
                if this_type in file_types:
                    files.append(file_path)
        return files



