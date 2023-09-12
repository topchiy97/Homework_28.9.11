from pydantic import BaseModel, Field

class BookingDates(BaseModel):
    checkin: str = Field(...)
    checkout: str = Field(...)

class BookingResponseModel(BaseModel):
    firstname: str = Field(...)
    lastname: str = Field(...)
    totalprice: int = Field(...)
    depositpaid: bool = Field(...)
    bookingdates: dict = Field(...)
    additionalneeds: str = Field(...)

    class Config:
        allow_population_by_field_name = True

class CreateBookingRequest(BaseModel):
    firstname: str = Field(...)
    lastname: str = Field(...)
    totalprice: int = Field(...)
    depositpaid: bool = Field(...)
    bookingdates: BookingDates = Field(...)
    additionalneeds: str = Field(...)

class BookingResponse(BaseModel):
    bookingid: int
    booking: CreateBookingRequest

class Booking(BaseModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: str

class CreateBookingResponse(BaseModel):
    bookingid: int