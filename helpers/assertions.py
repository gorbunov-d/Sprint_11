def assert_listing_matches(actual, expected, owner_id):
    assert actual["owner"] == owner_id
    assert {field: actual[field] for field in expected} == expected
