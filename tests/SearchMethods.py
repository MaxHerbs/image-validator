from image_validator.SearchMethods import SearchMethods

def test_search_regex():
    paths = SearchMethods.search_regex(SearchMethods, ["tests/store/mydoc.md"])
    assert ["/tests/store/test.png"] == paths