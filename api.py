import requests
from dumpers.key_model import AuthResponse
from dumpers.booking_model import BookingResponse

base_url = "https://restful-booker.herokuapp.com/"

def auth_key():
    headers = {"Content-Type": "application/json"}
    data = {
        "username": "admin",
        "password": "password123"
    }
    res = requests.post(base_url + "auth", headers=headers, json=data)
    res_model = AuthResponse(**res.json())
    return res_model.key

def create_booking():
    headers = {"Content-Type": "application/json"}
    data = {
        "firstname": "Sam",
        "lastname": "Jones",
        "totalprice": 505,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2022-01-01",
            "checkout": "2023-01-01"
        },
        "additionalneeds": "Breakfast"
    }
    res = requests.post(base_url + "booking", headers=headers, json=data)
    res_model = BookingResponse(**res.json())
    return res_model.bookingidxc