import json
import datetime

class Account:
    def __init__(
        self,
        account_login: str = '',
        user_type: int = 0,
        phone_number: str = '',
        account_email: str = ''
        ):
            self.account_login = account_login
            self.user_type = user_type
            self.phone_number = phone_number
            self.account_email = account_email

class Passenger:
    def __init__(
        self,
        passport_seria: int = 0,
        passport_number: int = 0,
        account_login: str = '',
        full_name: str = '',
        sex: str = '',
        citizenship: str = ''
    ):
        self.passport_seria = passport_seria
        self.passport_number = passport_number
        self.account_login = account_login
        self.full_name = full_name
        self.sex = sex
        self.citizenship = citizenship

    def from_json(p):
        passenger = Passenger(
            p['passport_seria'],
            p['passport_number'],
            p['account_login'],
            p['full_name'],
            p['sex'],
            p['citizenship']
        )

        return passenger

    def to_json(self):
        dict_pass = {
            'passport_seria': self.passport_seria,
            'passport_number': self.passport_number,
            'account_login': self.account_login,
            'full_name': self.full_name,
            'sex': self.sex,
            'citizenship': self.citizenship
        }

        return json.dumps(dict_pass)

class Flight:
    def __init__(
        self,
        flight_number: int = 0,
        dep_date: str = '2000-01-01',
        arr_date: str = '2000-01-01',
        local_dep_time: str = '00:00:00',
        local_arr_time: str = '00:00:00',
        dep_airport: str = '',
        arr_airport: str = '',
        iata_type_code: str = '',
        pack_code: int = 0
    ):
        self.flight_number = flight_number
        self.dep_date = dep_date
        self.arr_date = arr_date
        self.local_dep_time = local_dep_time
        self.local_arr_time = local_arr_time
        self.dep_airport = dep_airport
        self.arr_airport = arr_airport
        self.iata_type_code = iata_type_code
        self.pack_code = pack_code

class Airport:
    def __init__(
        self,
        airport_code: str = '',
        airport_name: str = '',
        country: str = '',
        city: str = '',
        timezone_hours: int = 0,
        timezone_minutes: int = 0,
    ):
        self.airport_code = airport_code
        self.airport_name = airport_name
        self.country = country
        self.city = city
        self.timezone_hours = timezone_hours
        self.timezone_minutes = timezone_minutes

class Aircraft:
    def __init__(
        self,
        iata_type_code: str = '',
        model_name: str = ''
    ):
        self.iata_type_code = iata_type_code
        self.model_name = model_name

class AircraftPack:
    def __init__(
        self,
        iata_type_code: str = '',
        pack_code: int = 0,
        economy_seats: int = 0,
        business_seats: int = 0,
        first_seats: int = 0,
        aircrafts_count: int = 0 
    ):
        self.iata_type_code = iata_type_code
        self.pack_code = pack_code
        self.economy_seats = economy_seats
        self.business_seats = business_seats
        self.first_seats = first_seats
        self.aircrafts_count = aircrafts_count

class FareBasis:
    def __init__(
        self,
        flight_number: int = 0,
        fare_basis_code: str = '',
        basis_cost: float = 0
    ):
        self.flight_number = flight_number
        self.fare_basisc_code = fare_basis_code
        self.basis_cost = basis_cost

class BoardingPass:
    def __init__(
        self,
        boarding_pass_id: int = 0,
        seat: str = '',
        gate: str = '',
        ticket_number: int = 0
    ):
        self.boarding_pass_id = boarding_pass_id
        self.seat = seat
        self.gate = gate
        self.ticket_number = ticket_number

class Ticket:
    def __init__(
        self,
        ticket_number: int = 0,
        dep_date: str = '2000-01-01',
        ticket_class: str = '',
        status: str = '',
        fare_basis_code: str = '',
        nvb: str = '2000-01-01',
        nva: str = '2000-01-01',
        baggage: bool = False,
        flight_number: int = 0,
        passport_seria: int = 0,
        passport_number: int = 0,
        account_login: str = '',
        pnr: str = ''
    ):
        self.ticket_number = ticket_number
        self.dep_date = dep_date
        self.ticket_class = ticket_class
        self.status = status
        self.fare_basis_code = fare_basis_code
        self.nvb = nvb
        self.nva = nva
        self.baggage = baggage
        self.flight_number = flight_number
        self.passport_seria = passport_seria
        self.passport_number = passport_number
        self.account_login = account_login
        self.pnr = pnr

class Booking:
    def __init__(
        self,
        pnr: str = '',
        fare: float = 0
    ):
        self.pnr = pnr
        self.fare = fare

class BookingService:
    def __int__(
        self,
        pnr: str = '',
        service_id: int = 0
    ):
        self.pnr = pnr
        self.service_id = service_id

class ExtraService:
    def __init__(
        self,
        service_id: int = 0,
        service_name: str = '',
        service_cost: float = 0
    ):
        self.service_id = service_id
        self.service_name = service_name
        self.service_cost = service_cost

class FlightsView:
    def __init__(
        self,
        flight_number: int = 0,
        dep_code: str = '',
        dep_name: str = '',
        dep_country: str = '',
        dep_city: str = '',
        arr_code: str = '',
        arr_name: str = '',
        arr_country: str = '',
        arr_city: str = '',
        dep_date: str = '2000-01-01',
        arr_date: str = '2000-01-01',
        local_dep_time: str = '00:00:00',
        local_arr_time: str = '00:00:00',
        fare_basis: str = '',
        cost: float = 0
    ):
        self.flight_number = flight_number
        self.dep_code = dep_code
        self.dep_name = dep_name
        self.dep_country = dep_country
        self.dep_city = dep_city
        self.arr_code = arr_code
        self.arr_name = arr_name
        self.arr_country = arr_country
        self.arr_city = arr_city
        self.dep_date = dep_date
        self.arr_date = arr_date
        self.local_dep_time = local_dep_time
        self.local_arr_time = local_arr_time
        self.fare_basis = 'Business' if fare_basis == 'C' else 'Economy'
        self.cost = cost


    def from_json(f):
        flight = FlightsView(
            f['flight_number'],
            f['dep_code'],
            f['dep_name'],
            f['dep_country'],
            f['dep_city'],
            f['arr_code'],
            f['arr_name'],
            f['arr_country'],
            f['arr_city'],
            f['dep_date'],
            f['arr_date'],
            f['local_dep_time'],
            f['local_arr_time'],
            f['fare_basis'],
            float(f['cost'])
        )

        return flight

    def to_json(self):
        dict_view = {
            'flight_number': self.flight_number,
            'dep_code': self.dep_code,
            'dep_name': self.dep_name,
            'dep_country': self.dep_country,
            'dep_city': self.dep_city,
            'arr_code': self.arr_code,
            'arr_name': self.arr_name,
            'arr_country': self.arr_country,
            'arr_city': self.arr_city,
            'dep_date': self.dep_date,
            'arr_date': self.arr_date,
            'local_dep_time': self.local_dep_time,
            'local_arr_time': self.local_arr_time,
            'fare_basis': self.fare_basis,
            'cost': str(self.cost),
        }
        return json.dumps(dict_view, default=json_converter)


class TicketsView:
    def __init__(
        self,
        ticket_number: int = 0,
        pnr: str = '',
        dep_code = '',
        dep_city = '',
        dep_country = '',
        arr_code = '',
        arr_city = '',
        arr_country = '',
        dep_date: str = '2000-01-01',
        dep_time: str = '00:00:00',
        arr_date: str = '2000-01-01',
        arr_time: str = '00:00:00',
        ticket_class: str = '',
        status: str = '',
        fare_basis_code: str = '',
        nvb: str = '2000-01-01',
        nva: str = '2000-01-01',
        baggage: bool = False,
        flight_number: int = 0,
        passenger_name: str = ''
    ):
        self.ticket_number = ticket_number
        self.pnr = pnr
        self.dep_code = dep_code
        self.dep_city = dep_city
        self.dep_country = dep_country
        self.arr_code = arr_code
        self.arr_city = arr_city
        self.arr_country = arr_country
        self.dep_date = dep_date
        self.dep_time = dep_time
        self.arr_date = arr_date
        self.arr_time = arr_time
        self.ticket_class = 'Business' if ticket_class == 'C' else 'Economy'
        self.status = status
        self.fare_basis_code = fare_basis_code
        self.nvb = nvb
        self.nva = nva
        self.baggage = baggage
        self.flight_number = flight_number
        self.passenger_name = passenger_name


def json_converter(o):
    if isinstance(o, datetime.date) or isinstance(o, datetime.time) or isinstance(o, float):
        return o.__str__()