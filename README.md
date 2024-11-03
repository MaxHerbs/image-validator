![Tests](https://github.com/maxherbs/image-validator/actions/workflows/tests.yml/badge.svg)

# Image Validator
Finds image paths within a directory and validates the images exist. Designed for Jekyll sites

# Supported Search Types
1. Regex
2. Frontmatter

# Using the Script
The module can be installed by running 
```bash
$ pip install https://github.com/MaxHerbs/image-validator
```

A sample config script can be found in `image_validator/internals/config.yaml`

Use it as template. The YAML is configured as follows.

- **imgBasePath:** The base of the directory to search. Leave it as `.` to search from you current dir.

- **searchTypes:** A list of the desired search types. `*` will use all searches. The list of supportedd search types can be found in this `README`.

- **directories:** A list of the directories to look in
    - **dir:** The directory. The CLI will search recursively within all subdirectories
    - **fileTypes:** The file endings of the  files you want to search. Either ommit this key, or use `*` to search all files.

Run the script with:

```bash
$ image-validator validate -p path/to/your/config
```

# TODO:
1. Add more search methods.