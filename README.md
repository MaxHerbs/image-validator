# Image Validator
Finds image paths within a directory and validates the images exist.

# Supported Search Types
1. Regex

# Using the Script
A sample config script can be found in `image_validator/internals/config.yaml`

Use it as template. The YAML is configured as follows.

- **imgBasePath:** The base of the directory to search. Leave it as `.` to search from you current dir.

- **searchTypes:** A list of the desired search types. `*` will use all searches. The list of supportedd search types can be found in this `README`.

- **directories:** A list of the directories to look in
    - **dir:** The directory. The CLI will search recursively within all subdirectories
    - **fileTypes:** The file endings of the  files you want to search. Either ommit this key, or use `*` to search all files.

