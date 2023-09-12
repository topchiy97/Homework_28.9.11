from pydantic import BaseModel
import pytest
import requests

class AccessKeyRequest(BaseModel):
    access_key: str

class User(BaseModel):
    id: int
    first_name: str
    last_name: str

def test_access_key_required():
    request = {
        "access_key": "token123"
    }
    AccessKeyRequest(**request)

def test_users_get_response():
    res = [
        {"id": 367, "first_name": "Any", "last_name": "Dammer"},
        {"id": 763, "first_name": "James", "last_name": "Dammer"}
    ]
    users = [User(**user) for user in res]

def test_access_key_required():
    request = {}
    with pytest.raises(ValueError):
        AccessKeyRequest(**request)

def test_access_key_format():
    request = {
        "access_token": "invalid_token_format"
    }
    with pytest.raises(ValueError):
        AccessKeyRequest(**request)

def test_users_get_success():
    res = [
        {"id": 367, "first_name": "Any", "last_name": "Dammer"},
        {"id": 763, "first_name": "James", "last_name": "Dammer"}
    ]
    users = [User(**user) for user in res]
    assert len(users) == 2
    assert users[0].id == 123
    assert users[0].first_name == "Any"
    assert users[0].last_name == "Dammer"

def test_users_get_no_users():
    res = []
    users = [User(**user) for user in res]
    assert len(users) == 0

def test_user_format():
    user = {
        "id": "invalid_id_format",
        "first_name": "Any",
        "last_name": "Dammer"
    }
    with pytest.raises(ValueError):
        User(**user)

def test_user_name_format():
    user = {
        "id": 123,
        "first_name": "Any367",
        "last_name": "Dammer"
    }
    with pytest.raises(ValueError):
        User(**user)

def test_user_lastname_format():
    user = {
        "id": 123,
        "first_name": "John",
        "last_name": "Doe123"
    }
    with pytest.raises(ValueError):
        User(**user)

def test_users_get_one_user():
    response = [{"id": 123, "first_name": "John", "last_name": "Doe"}]
    users = [User(**user) for user in response]
    assert len(users) == 1
    assert users[0].id == 123
    assert users[0].first_name == "John"
    assert users[0].last_name == "Doe"

def test_users_get_max_users():
    res = [{"id": i, "first_name": "User", "last_name": str(i)} for i in range(1000)
]
    users = [User(**user) for user in res]
    assert len(users) == 1000
    assert users[-1].id == 999
    assert users[-1].first_name == "User"
    assert users[-1].last_name == "999"

def test_users_get_invalid_response():
    response = [{"invalid_attr": "value"}]
    with pytest.raises(ValueError):
        users = [User(**user) for user in response]