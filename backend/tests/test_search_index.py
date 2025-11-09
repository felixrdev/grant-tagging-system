from src.models import Grant
from src.search_index import SearchIndex


def test_search_index_add_grants():
    index = SearchIndex()
    grants = [
        Grant(
            grant_name="Test Grant 1",
            grant_description="Description 1",
            tags=["agriculture", "education"],
        ),
        Grant(
            grant_name="Test Grant 2",
            grant_description="Description 2",
            tags=["education", "youth"],
        ),
    ]

    index.add_grants(grants)

    assert len(index.grant_id_to_grant) == 2
    assert len(index.tag_to_grant_ids["agriculture"]) == 1
    assert len(index.tag_to_grant_ids["education"]) == 2
    assert len(index.tag_to_grant_ids["youth"]) == 1


def test_search_index_search_all_mode():
    index = SearchIndex()
    grants = [
        Grant(
            grant_name="Grant 1",
            grant_description="Desc 1",
            tags=["agriculture", "education", "soil"],
        ),
        Grant(
            grant_name="Grant 2",
            grant_description="Desc 2",
            tags=["education", "youth"],
        ),
        Grant(
            grant_name="Grant 3",
            grant_description="Desc 3",
            tags=["agriculture", "soil"],
        ),
    ]

    index.add_grants(grants)

    results = index.search_by_tags(["agriculture", "soil"], mode="all")
    assert len(results) == 2
    assert results[0].grant_name in ["Grant 1", "Grant 3"]
    assert results[1].grant_name in ["Grant 1", "Grant 3"]


def test_search_index_search_any_mode():
    index = SearchIndex()
    grants = [
        Grant(
            grant_name="Grant 1",
            grant_description="Desc 1",
            tags=["agriculture", "education"],
        ),
        Grant(
            grant_name="Grant 2",
            grant_description="Desc 2",
            tags=["education", "youth"],
        ),
        Grant(grant_name="Grant 3", grant_description="Desc 3", tags=["soil"]),
    ]

    index.add_grants(grants)

    results = index.search_by_tags(["agriculture", "youth"], mode="any")
    assert len(results) == 2


def test_search_index_rebuild():
    index = SearchIndex()
    grants1 = [
        Grant(grant_name="Grant 1", grant_description="Desc 1", tags=["agriculture"])
    ]

    index.add_grants(grants1)
    assert len(index.grant_id_to_grant) == 1

    grants2 = [
        Grant(grant_name="Grant 2", grant_description="Desc 2", tags=["education"]),
        Grant(grant_name="Grant 3", grant_description="Desc 3", tags=["youth"]),
    ]

    index.rebuild(grants2)
    assert len(index.grant_id_to_grant) == 2
    assert len(index.tag_to_grant_ids["agriculture"]) == 0
    assert len(index.tag_to_grant_ids["education"]) == 1


def test_search_index_empty_tags():
    index = SearchIndex()
    grants = [
        Grant(grant_name="Grant 1", grant_description="Desc 1", tags=["agriculture"])
    ]

    index.add_grants(grants)

    results = index.search_by_tags([], mode="all")
    assert len(results) == 0


def test_search_index_case_insensitive():
    index = SearchIndex()
    grants = [
        Grant(
            grant_name="Grant 1",
            grant_description="Desc 1",
            tags=["Agriculture", "Education"],
        )
    ]

    index.add_grants(grants)

    results = index.search_by_tags(["agriculture"], mode="all")
    assert len(results) == 1

    results = index.search_by_tags(["EDUCATION"], mode="all")
    assert len(results) == 1


def test_search_index_no_matches():
    index = SearchIndex()
    grants = [
        Grant(grant_name="Grant 1", grant_description="Desc 1", tags=["agriculture"])
    ]

    index.add_grants(grants)

    results = index.search_by_tags(["nonexistent"], mode="all")
    assert len(results) == 0
