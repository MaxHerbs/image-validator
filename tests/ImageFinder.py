import pytest 
from image_validator.ImageFinder import ImageFinder

def test_dir_walk():
    store_files = ['tests/ImageFinder.py', 
                   'tests/__init__.py',
                    'tests/store/mydoc.md', 
                    'tests/store/test.png', 
                    'tests/ConfigManager.py'
                ]
    
    finder = ImageFinder({})
    found_files = finder.dir_walk("tests", ["*"])
    print(found_files)
    for file in store_files:
        assert file in found_files

def test_dir_walk_specifics():
    store_files = ['tests/store/mydoc.md']
    finder = ImageFinder({})
    found_files = finder.dir_walk("tests", ["md"])
    print(found_files)
    for file in store_files:
        assert file in found_files