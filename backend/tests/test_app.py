import json

import pytest

from app import app
from src.search_index import get_search_index
from src.store import GrantStore


@pytest.fixture
def client():
    app.config["TESTING"] = True

    store = GrantStore()
    store.clear_grants()

    search_index = get_search_index()
    search_index.clear()

    with app.test_client() as client:
        yield client

    store.clear_grants()
    search_index.clear()


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Grant Tagging API"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_get_tags(client):
    response = client.get("/api/tags")
    assert response.status_code == 200
    tags = response.get_json()
    assert isinstance(tags, list)
    assert len(tags) > 0
    assert "agriculture" in tags


def test_batch_tag_grants(client):
    grants_input = [
        {
            "grant_name": "Sustainable Agriculture Research Grant",
            "grant_description": (
                "Funding for projects that promote organic farming practices "
                "and soil conservation."
            ),
        },
        {
            "grant_name": "STEM Education Initiative",
            "grant_description": (
                "Support for programs that encourage high school students to pursue "
                "careers in science, technology, engineering, and mathematics."
            ),
        },
    ]

    response = client.post(
        "/api/grants/batch",
        data=json.dumps(grants_input),
        content_type="application/json",
    )

    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2

    grant1 = data[0]
    assert grant1["grant_name"] == "Sustainable Agriculture Research Grant"
    assert "tags" in grant1
    assert isinstance(grant1["tags"], list)
    assert len(grant1["tags"]) > 0

    grant2 = data[1]
    assert grant2["grant_name"] == "STEM Education Initiative"
    assert "tags" in grant2


def test_get_grants(client):
    grants_input = [
        {
            "grant_name": "Test Grant",
            "grant_description": "This is a test grant for education and research.",
        }
    ]

    client.post(
        "/api/grants/batch",
        data=json.dumps(grants_input),
        content_type="application/json",
    )

    response = client.get("/api/grants")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 1
    assert data[0]["grant_name"] == "Test Grant"


def test_search_grants(client):
    grants_input = [
        {
            "grant_name": "Agriculture Grant",
            "grant_description": "Farming and soil conservation.",
        },
        {
            "grant_name": "Education Grant",
            "grant_description": "School programs and training.",
        },
    ]

    client.post(
        "/api/grants/batch",
        data=json.dumps(grants_input),
        content_type="application/json",
    )

    response = client.get("/api/search?tags=agriculture,soil")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 1
    assert "Agriculture Grant" in [g["grant_name"] for g in data]


def test_batch_invalid_input(client):
    response = client.post(
        "/api/grants/batch",
        data=json.dumps({"invalid": "data"}),
        content_type="application/json",
    )

    assert response.status_code == 400


def test_batch_missing_fields(client):
    grants_input = [{"grant_name": "Test"}]

    response = client.post(
        "/api/grants/batch",
        data=json.dumps(grants_input),
        content_type="application/json",
    )

    assert response.status_code == 400


def test_advanced_search_with_query(client):
    grants_input = [
        {
            "grant_name": "Agriculture Education Program",
            "grant_description": "Teaching students about farming and soil health.",
        },
        {
            "grant_name": "Urban Farming Initiative",
            "grant_description": "Supporting local food production in cities.",
        },
    ]

    client.post(
        "/api/grants/batch",
        data=json.dumps(grants_input),
        content_type="application/json",
    )

    response = client.get("/api/search/advanced?q=learning")
    assert response.status_code == 200
    data = response.get_json()

    assert "resolved_tags" in data
    assert "education" in data["resolved_tags"]
    assert "grants" in data
    assert len(data["grants"]) >= 1


def test_advanced_search_with_tags_param(client):
    grants_input = [
        {
            "grant_name": "Soil Conservation Grant",
            "grant_description": "Improving soil health through conservation practices.",
        }
    ]

    client.post(
        "/api/grants/batch",
        data=json.dumps(grants_input),
        content_type="application/json",
    )

    response = client.get("/api/search/advanced?tags=soil,agriculture")
    assert response.status_code == 200
    data = response.get_json()

    assert "soil" in data["resolved_tags"]
    assert "agriculture" in data["resolved_tags"]


def test_advanced_search_mode_any(client):
    grants_input = [
        {
            "grant_name": "Farm Grant",
            "grant_description": "Supporting agricultural producers.",
        },
        {
            "grant_name": "School Grant",
            "grant_description": "Educational programs for students.",
        },
    ]

    client.post(
        "/api/grants/batch",
        data=json.dumps(grants_input),
        content_type="application/json",
    )

    response = client.get("/api/search/advanced?tags=agriculture,education&mode=any")
    assert response.status_code == 200
    data = response.get_json()

    assert len(data["grants"]) == 2


def test_advanced_search_mode_all(client):
    grants_input = [
        {
            "grant_name": "Farm Education Grant",
            "grant_description": "Teaching students about agriculture and soil.",
        },
        {
            "grant_name": "Farm Grant",
            "grant_description": "Supporting agricultural producers.",
        },
    ]

    client.post(
        "/api/grants/batch",
        data=json.dumps(grants_input),
        content_type="application/json",
    )

    response = client.get("/api/search/advanced?tags=agriculture,education&mode=all")
    assert response.status_code == 200
    data = response.get_json()

    assert len(data["grants"]) == 1


def test_advanced_search_synonym_resolution(client):
    grants_input = [
        {
            "grant_name": "Irrigation System Grant",
            "grant_description": "Installing water systems for farms.",
        }
    ]

    client.post(
        "/api/grants/batch",
        data=json.dumps(grants_input),
        content_type="application/json",
    )

    response = client.get("/api/search/advanced?q=irrigation")
    assert response.status_code == 200
    data = response.get_json()

    assert "water" in data["resolved_tags"]
    assert len(data["grants"]) >= 1


def test_advanced_search_empty_query(client):
    response = client.get("/api/search/advanced")
    assert response.status_code == 200
    data = response.get_json()

    assert data["resolved_tags"] == []
    assert data["grants"] == []


def test_advanced_search_invalid_mode(client):
    response = client.get("/api/search/advanced?q=test&mode=invalid")
    assert response.status_code == 400
