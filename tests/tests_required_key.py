import pytest
import requests
from api import auth_key, create_booking, base_url


@pytest.mark.xfail
@pytest.mark.required_key
@pytest.mark.parametrize(
    "auth_key, create_booking, content_type, expected_status",
    [(auth_key(), create_booking(auth_key), "application/json", 201),
     ("asd324sda", create_booking(auth_key), "application/json", 403),
     (auth_key(), "-1", "application/json", 405),
     (auth_key(), create_booking(auth_key), "text/plain", 415)])

def test_delete_booking(auth_key, create_booking, content_type, expected_status):

    url = f"{base_url} + /booking/{create_booking}"
    headers = {
        "Content-Type": f"{content_type}",
        "Cookie": f"key = {auth_key}"
    }
    res = requests.delete(url, headers=headers)
    if res.status_code == 201:
        assert res.status_code == expected_status,\
        f"Delete booking request failed with status code {res.status_code}"
        assert res.text == "Created", \
        "Delete booking response should contain 'Created'"
    elif res.status_code == 403:
        assert res.status_code == expected_status, \
        f"Delete booking request failed with status code {res.status_code}"
        assert res.text == "Forbidden", \
        "Delete booking response should contain 'Created'"
    elif res.status_code == 405:
        assert res.status_code == expected_status, \
        f"Delete booking request failed with status code {res.status_code}"
        assert res.text == "Method Not Allowed", \
        "Delete booking response should contain 'Created'"
    elif res.status_code == 415:
        assert res.status_code == expected_status, \
        f"Delete booking request failed with status code {res.status_code}"
        assert res.text == "Unsupported Media Type", \
        "Delete booking response should contain 'Created'"