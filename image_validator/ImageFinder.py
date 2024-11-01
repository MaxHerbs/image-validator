import re
import typer
import os

re_img = r'<img\s+[^>]*src="([^"]+)"'


class ImageFinder:
    files_to_search = []
    detected_image_paths = []
    invalid_image_paths = []


    def __init__(self, descriptor: dict):
        self.descriptor = descriptor

    def validate(self) -> bool:
        self.populate_paths()
        print(self.files_to_search)
        typer.echo(f"Found {len(self.files_to_search)} files to look inside.")


        requestedSearches = self.descriptor["searchTypes"]
        supported_searches = dir(ImageFinder)  
        typer.echo(f"Trying to search with {len(requestedSearches)} search types")

        

        for req in requestedSearches:
            print(req)
            if req in supported_searches:
                try:
                    getattr(self, req)()
                except TypeError as e:
                    typer.echo(f"{req} is not a valid search type. Skipping.")
            else:
                typer.echo(f"Search type {req} not supported. Skipping.")
        print(f"Detected {len(self.detected_image_paths)} image paths")

        img_dir_base = self.descriptor["imgbasePath"]
        if not img_dir_base.endswith("/"):
            img_dir_base += "/"

        self.detected_image_paths = [img_dir_base + path[1::] for path in self.detected_image_paths]

        self.validate_image_paths()
        if self.invalid_image_paths:
            typer.echo("The following image paths are invalid:")
            for path in self.invalid_image_paths:
                typer.echo(path)
        else:
            typer.echo("All image paths are valid!")

        


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



    def regex(self) -> None:
        typer.echo("Searching for images paths using regex")

        for file in self.files_to_search:
            with open(file, "r") as f:
                content = f.read()
                matches = re.findall(re_img, content)
                for match in matches:
                    self.detected_image_paths.append(match)