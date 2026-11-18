def assert_listing_matches(actual, expected, listing_id, owner_id):
    assert actual["id"] == listing_id
    assert actual["owner"] == owner_id
    assert {field: actual[field] for field in expected} == expected
