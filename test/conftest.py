import pytest
from icat.query import Query


@pytest.fixture()
def icat_query(icat_client):
    return Query(icat_client, "Investigation")


@pytest.fixture()
def bad_credentials_header():
    return {"Authorization": "Bearer Invalid"}


@pytest.fixture()
def invalid_credentials_header():
    return {"Authorization": "Test"}


@pytest.fixture()
def test_config_data():
    return {
        "api": {
            "title": "Datagateway API",
            "description": "This is the API for the Datagateway",
            "url_prefix": "",
            "reload": False,
            "host": "127.0.0.1",
            "port": 5000,
            "allowed_cors_headers": ["*"],
            "allowed_cors_origins": ["*"],
            "allowed_cors_methods": ["*"],
        },
        "datagateway_api": {
            "extension": "/datagateway-api",
            "client_cache_size": 5,
            "client_pool_init_size": 2,
            "client_pool_max_size": 5,
            "icat_url": "https://localhost:8181",
            "icat_check_cert": False,
        },
        "search_api": {
            "extension": "/search-api",
            "icat_url": "https://localhost.testdomain:8181",
            "icat_check_cert": True,
            "mechanism": "anon",
            "username": "",
            "password": "",
            "search_scoring": {
                "enabled": False,
                "api_url": "http://localhost:9000/score",
                "api_request_timeout": 5,
                "group": "documents",
                "limit": 1000,
            },
        },
    }
