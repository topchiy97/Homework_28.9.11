import pytest
import requests
from pydantic import ValidationError
from dumpers.booking_model import BookingResponseModel, CreateBookingRequest, BookingResponse
from api import base_url


@pytest.mark.without_token
@pytest.mark.parametrize('booking_id, expected_status, headers', [
    (1, 200, {"Accept": "application/json"}),
    (0, 404, {"Accept": "application/json"}),
    (-1, 404, {"Accept": "application/json"}),
    ("a", 404, {"Accept": "application/json"}),
    (1, 418, {"Accept": ""}),
    (1, 200, None)])

def test_get_booking(booking_id, expected_status, headers):
    url = f"{base_url} + booking/{booking_id}"

    res = requests.get(url, headers=headers)

    assert res.status_code == expected_status, \
    f"Request failed with status code {res.status_code}"

    if expected_status == 200:
        try:
            data = res.json()
            booking = BookingResponseModel(**data)
        except (ValidationError, TypeError) as e:
            pytest.fail(f"Failed to validate booking response data: {e}")

        assert booking.firstname != '', "Firstname is missing"
        assert booking.lastname != '', "Lastname is missing"
        assert booking.totalprice >= 0, "Total price must be non-negative"
        assert isinstance(booking.depositpaid, bool), "Depositpaid must be a boolean"
        assert isinstance(booking.bookingdates, dict), "Bookingdates must be a dictionary"
        assert "checkin" in booking.bookingdates \
        and isinstance(booking.bookingdates["checkin"], str), \
            "Checkin date is missing or invalid"
        assert "checkout" in booking.bookingdates \
        and isinstance(booking.bookingdates["checkout"], str), \
            "Checkout date is missing or invalid"


@pytest.mark.xfail
@pytest.mark.without_key
@pytest.mark.parametrize("headers, request_body, expected_status", [
    ({"Content-Type": "application/json", "Accept": "application/json"},
     {"firstname": "Jim", "lastname": "Brown", "totalprice": 111, "depositpaid": True,
        "bookingdates": {"checkin": "2018-01-01", "checkout": "2019-01-01"},
        "additionalneeds": "Breakfast"}, 200),
    ({"Content-Type": "text/plain", "Accept": "text/plain"},
     {"firstname": "Jim", "lastname": "Brown", "totalprice": 111, "depositpaid": True,
      "bookingdates": {"checkin": "2018-01-01", "checkout": "2019-01-01"},
        "additionalneeds": "Breakfast"}, 415),
    (None, {"firstname": "Jim", "lastname": "Brown", "totalprice": 111, "depositpaid": True,
        "bookingdates": {"checkin": "2018-01-01", "checkout": "2019-01-01"},
        "additionalneeds": "Breakfast"}, 200)])

def test_create_booking(headers, request_body, expected_status):

    try:
        request_data = CreateBookingRequest(**request_body)
    except ValidationError as e:
        pytest.fail(f"Failed to validate request data: {e}")

    res = requests.post(base_url + "booking", headers=headers, json=request_data.dict())

    assert res.status_code == expected_status, \
    f"Request failed with status code {res.status_code}"

    if expected_status == 200:
        try:
            response_data = res.json()
            booking_response = BookingResponse(**response_data)
        except (ValidationError, TypeError) as e:
            pytest.fail(f"Failed to validate booking response data: {e}")

        assert booking_response.bookingid is not None and isinstance(booking_response.bookingid, int), \
            "Booking ID is missing or invalid"
        assert isinstance(booking_response.booking, CreateBookingRequest), \
            "Booking data is missing or invalid"
        booking = booking_response.booking
        assert booking.firstname == request_data.firstname, \
            "Invalid firstname in the response"
        assert booking.lastname == request_data.lastname, \
            "Invalid lastname in the response"
        assert booking.totalprice == request_data.totalprice, \
            "Invalid totalprice in the response"
        assert booking.depositpaid == request_data.depositpaid, \
            "Invalid depositpaid in the response"
        assert booking.bookingdates.dict() == request_data.bookingdates.dict(), \
            "Invalid bookingdates in the response"
        assert booking.additionalneeds == request_data.additionalneeds, \
            "Invalid additionalneeds in the response"