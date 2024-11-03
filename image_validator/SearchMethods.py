import typer
import re
import yaml

re_img = r'<img\s+[^>]*src="([^"]+)"'


class SearchMethods:
    def __init__(self, requested_searches: list, files_to_search: list):
        self.files_to_search = files_to_search
        self.detected_paths = []

        supported_searches = [func for func in dir(self) if callable(getattr(self, func)) and func.startswith("search")]
        for req in requested_searches:
          req = "search_" + req
          if req in supported_searches:
              try:
                  self.detected_paths += getattr(self, req)(files_to_search)
              except TypeError as e:
                  typer.echo(f"{req} is not a valid search type. Skipping.")
                  typer.echo(e)
          else:
              typer.echo(f"Search type {req} not supported. Skipping.")


    def search_regex(self, file_paths) -> list:
        typer.echo("Searching for images paths using regex")
        detected_paths = []
        for file in file_paths:
            with open(file, "r") as f:
                content = f.read()
                matches = re.findall(re_img, content)
                for match in matches:
                    detected_paths.append(match)
        return detected_paths
    
    def search_frontmatter(self, file_paths) -> list:
        typer.echo("Searching for images paths in frontmatter")
        detected_paths = []
        for file in file_paths:
            with open(file, "r") as f:
                print("File: " + file)
                frontMatter = ""
                f.readline()
                while True:
                    thisLine = f.readline().strip()
                    print(thisLine)
                    if thisLine == "---":
                        break
                    frontMatter += thisLine + "\n"
                serialisedFrontmatter = yaml.safe_load(frontMatter)
                
                if "background" in serialisedFrontmatter:
                    detected_paths.append(serialisedFrontmatter["background"])

        return detected_paths