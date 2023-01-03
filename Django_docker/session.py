import psycopg2 as pg
import os
from models import *

HOST = os.getenv('DATABASE_URL')
PORT = os.getenv('DATABASE_PORT')
DBNAME = os.getenv('DATABASE_NAME')


class DBSession:
    def __init__(
        self,
        username,
        passwd
    ):
        self.sess = pg.connect(
            host=HOST,
            port=PORT,
            dbname=DBNAME,
            user=username,
            password=passwd
        )
        self.username = username
        self.cur = self.sess.cursor()

        query = 'SELECT user_type FROM account WHERE account_login = %s'
        self.cur.execute(query, (username,))

        self.user_type = self.cur.fetchall()[0][0]


    def get_flights(self, dep_place: str, arr_place: str) -> list[FlightsView]:
        dep_place = '%' + dep_place.lower() + '%'
        arr_place = '%' + arr_place.lower() + '%'
        flights = []

        query = 'SELECT * FROM all_flights WHERE (LOWER(dep_code) LIKE %s OR LOWER(dep_city) LIKE %s) AND (LOWER(arr_code) LIKE %s OR LOWER(arr_city) LIKE %s)'
        self.cur.execute(query, (dep_place, dep_place, arr_place, arr_place))
        result = self.cur.fetchall()

        for r in result:
            flight = FlightsView(
                r[0],
                r[1],
                r[2],
                r[3],
                r[4],
                r[5],
                r[6],
                r[7],
                r[8],
                r[9],
                r[10],
                r[11],
                r[12],
                r[13],
                r[14]
            )

            flights.append(flight)

        return flights

    
    def get_flights_with_date(self, dep_place: str, arr_place: str, dep_date: str) -> list[FlightsView]:
        dep_place = '%' + dep_place.lower() + '%'
        arr_place = '%' + arr_place.lower() + '%'
        flights = []

        query = 'SELECT * FROM all_flights WHERE dep_date = %s AND (LOWER(dep_code) LIKE %s OR LOWER(dep_city) LIKE %s) AND (LOWER(arr_code) LIKE %s OR LOWER(arr_city) LIKE %s)'
        self.cur.execute(query, (dep_date, dep_place, dep_place, arr_place, arr_place))
        result = self.cur.fetchall()

        for r in result:
            flight = FlightsView(
                r[0],
                r[1],
                r[2],
                r[3],
                r[4],
                r[5],
                r[6],
                r[7],
                r[8],
                r[9],
                r[10],
                r[11],
                r[12],
                r[13],
                r[14]
            )

            flights.append(flight)

        return flights


    def edit_passenger(self, p: Passenger, p_old: Passenger):
        query = '''UPDATE passenger SET passport_seria = %s , passport_number = %s, account_login = %s
        full_name = %s, sex = %s, citizenship = %s WHERE passport_seria = %s AND passport_number = %s'''
        
        self.cur.execute(query, 
            (p.passport_seria, p.passport_number, p.account_login, p.full_name,
                p.sex, p.citizenship, p_old.passport_seria, p_old.passport_number))
        self.sess.commit()


    def add_airport(self, a: Airport):
        query = 'INSERT INTO airport(airport_code, airport_name, country, city, timezone_hours, timezone_minutes) VALUES (%s, %s, %s, %s, %s, %s)'
        self.cur.execute(query, (a.airport_code, a.airport_name, a.country, a.city, a.timezone_hours, a.timezone_minutes))
        self.sess.commit()


    def get_airport(self, code: str) -> Airport:
        query = 'SELECT * FROM airport WHERE airport_code = %s'
        self.cur.execute(query, (code,))
        result = self.cur.fetchall()

        if len(result) == 0:
            print('not found')
            return None

        a = result[0]
        airport = Airport(
            a[0],
            a[1],
            a[2],
            a[3],
            a[4],
            a[5]
        )

        print('returned')
        return airport


    def edit_airport(self, a: Airport, a_old: Airport):
        query = 'UPDATE airport SET airport_code = %s, airport_name = %s, country = %s, city = %s, timezone_hours = %s, timezone_minutes = %s WHERE airport_code = %s'
        self.cur.execute(query, (a.airport_code, a.airport_name, a.country, a.city, a.timezone_hours, a.timezone_minutes, a_old.airport_code))
        self.sess.commit()


    def add_flight(self, f: Flight, fare_b: list[str], costs: list[str]):
        query = 'INSERT INTO flight(flight_number, dep_date, arr_date, local_dep_time, local_arr_time, dep_airport, arr_airport, iata_type_code, pack_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        self.cur.execute(query, (f.flight_number, f.dep_date, f.arr_date, f.local_dep_time, f.local_arr_time, f.dep_airport, f.arr_airport, f.iata_type_code, f.pack_code))
        for i in range(len(fare_b)):
            query = 'INSERT INTO fare_basis(flight_number, fare_basis_code, dep_date, basis_cost) VALUES (%s, %s, %s, %s)'
            self.cur.execute(query, (f.flight_number, fare_b[i], f.dep_date, costs[i]))
        self.sess.commit()


    def edit_flight_schedule(self, flight_number: int, prev_date: str, dep_date: str, dep_time: str, arr_date: str, arr_time: str):
        query = 'UPDATE flight SET dep_date = %s, arr_date = %s, local_dep_time = %s, local_arr_time = %s WHERE flight_number = %s AND dep_date = %s'
        self.cur.execute(query, (dep_date, arr_date, dep_time, arr_time, flight_number, prev_date))
        query = 'UPDATE fare_basis SET dep_date = %s WHERE flight_number = %s AND dep_date = %s'
        self.cur.execute(query, (dep_date, flight_number, prev_date))

        self.sess.commit()


    def get_flight(self, flight_number: int, dep_date: str):
        flight_number = int(flight_number)
        query = 'SELECT * from all_flights WHERE flight_number = %s AND dep_date = %s'
        self.cur.execute(query, (flight_number, dep_date))

        result = self.cur.fetchall()

        if len(result) == 0:
            return None

        f = result[0]
        flight = FlightsView(
            f[0],
            f[1],
            f[2],
            f[3],
            f[4],
            f[5],
            f[6],
            f[7],
            f[8],
            f[9],
            f[10],
            f[11],
            f[12],
            f[13],
            f[14]
        )

        return flight


    def get_my_passengers(self) -> list[Passenger]:
        query = 'SELECT * FROM passenger'
        self.cur.execute(query)
        result = self.cur.fetchall()

        passengers = []

        for r in result:
            p = Passenger(
                r[0],
                r[1],
                r[2],
                r[3],
                r[4],
                r[5]
            )

            passengers.append(p)

        return passengers


    def get_passenger(self, seria, number, login) -> Passenger:
        seria = int(seria)
        number = int(number)

        query = 'SELECT * FROM passenger WHERE passport_seria = %s AND passport_number = %s AND account_login = %s'
        self.cur.execute(query, (seria, number, login))
        result = self.cur.fetchall()

        if len(result) == 0:
            return Passenger()

        r = result[0]
        passenger = Passenger(
            r[0],
            r[1],
            r[2],
            r[3],
            r[4],
            r[5]
        )

        return passenger

    def make_booking(self, flight: FlightsView, passengers: list[Passenger]):
        query = 'SELECT generate_pnr()'
        self.cur.execute(query)
        pnr = self.cur.fetchall()[0][0]

        query = 'INSERT INTO booking(pnr, fare) VALUES (%s, %s)'
        self.cur.execute(query, (pnr, flight.cost))

        query = '''INSERT INTO ticket(ticket_number, dep_date, ticket_class, status, fare_basis_code, baggage,
                   flight_number,
                   passport_seria, passport_number, account_login, pnr) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        for p in passengers:
            query_passenger = 'CALL add_passenger_if_not_exists(%s, %s, %s, %s, %s, %s)'
            self.cur.execute(query_passenger, (p.passport_seria, p.passport_number, p.account_login, p.full_name, p.sex, p.citizenship))

            query_ticket = 'SELECT generate_ticket_number()'
            self.cur.execute(query_ticket)
            ticket_number = self.cur.fetchall()[0][0]

            ticket = Ticket(
                ticket_number,
                flight.dep_date,
                'Y' if flight.fare_basis == 'Economy' else 'C',
                'OK',
                'Y' if flight.fare_basis == 'Economy' else 'C',
                '',
                '',
                False,
                flight.flight_number,
                p.passport_seria,
                p.passport_number,
                p.account_login,
                pnr
            )

            params = (
                ticket.ticket_number,
                ticket.dep_date,
                ticket.ticket_class,
                ticket.status,
                ticket.fare_basis_code,
                ticket.baggage,
                ticket.flight_number,
                ticket.passport_seria,
                ticket.passport_number,
                ticket.account_login,
                ticket.pnr
            )
            self.cur.execute(query, params)

        self.sess.commit()

        return pnr


    def get_booking_tickets(self, pnr: str) -> list[TicketsView]:
        query = 'SELECT * FROM all_tickets WHERE pnr = %s'
        self.cur.execute(query, (pnr,))
        response = self.cur.fetchall()

        if len(response) == 0:
            return None

        tickets: list[TicketsView] = []

        for t in response:
            ticket = TicketsView(
                t[0],
                t[1],
                t[2],
                t[3],
                t[4],
                t[5],
                t[6],
                t[7],
                t[8],
                t[9],
                t[10],
                t[11],
                t[12],
                t[13],
                t[14],
                t[15],
                t[16],
                t[17],
                t[18],
                t[19]
            )

            tickets.append(ticket)

        return tickets

    def add_account(self, a: Account, password: str):
        query = 'CALL add_client(%s, %s, %s, %s, %s)'
        self.cur.execute(query, (a.account_login, password, a.user_type, a.phone_number, a.account_email))
        self.sess.commit()