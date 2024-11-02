import typer
import re

re_img = r'<img\s+[^>]*src="([^"]+)"'


class SearchMethods:
    def __init__(self, requested_searches: list, files_to_search: list):
        self.files_to_search = files_to_search
        self.detected_paths = []

        supported_searches = [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("__")]
        for req in requested_searches:
          if req in supported_searches:
              try:
                  self.detected_paths += getattr(self, req)()
              except TypeError as e:
                  typer.echo(f"{req} is not a valid search type. Skipping.")
          else:
              typer.echo(f"Search type {req} not supported. Skipping.")


    def regex(self) -> list:
        typer.echo("Searching for images paths using regex")
        detected_paths = []
        for file in self.files_to_search:
            with open(file, "r") as f:
                content = f.read()
                matches = re.findall(re_img, content)
                for match in matches:
                    detected_paths.append(match)
        return detected_paths