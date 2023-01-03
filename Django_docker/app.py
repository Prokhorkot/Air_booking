from flask import Flask, session, redirect, render_template, url_for, request
import os
from session import DBSession
from dotenv import load_dotenv
from models import *
import json
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
URL = os.getenv('DATABASE_URL')
sessions = {}


def requires_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'uname' not in session or session['uname'] not in sessions.keys():
            return redirect(url_for('login'))

        sess: DBSession = sessions[session['uname']]
        if not sess.user_type == 2:
            return redirect(url_for('main_menu', invalid="You don't have privileges for this action"))

        return f(*args, **kwargs)
    return decorated_function


def requires_manager(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'uname' not in session or session['uname'] not in sessions.keys():
            return redirect(url_for('login'))

        sess: DBSession = sessions[session['uname']]
        if sess.user_type == 0:
            return redirect(url_for('main_menu', invalid="You don't have privileges for this action"))

        return f(*args, **kwargs)
    return decorated_function


def requires_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'uname' not in session or session['uname'] not in sessions.keys():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.get('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        uname = request.form['uname']
        passwd = request.form['psw']
        try:
            sess = DBSession(uname, passwd)
            session['uname'] = uname
            sessions[uname] = sess

            return redirect(url_for('main_menu'))
        except Exception as e:
            return render_template('login.html', invalid='Incorrect login or password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register_client.html')

    if request.method == 'POST':
        try:
            login = request.form['uname']
            password = request.form['psw']
            phone_number = request.form['ph_number']
            email = request.form['email']

            account = Account(login, 0, phone_number, email)

            sess = DBSession('kotprokhor', 'Pk23072002')
            sess.add_account(account, password)

            return redirect(url_for('login'))
        except:
            return render_template('register_client.html', invalid='Incorrect input')



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    sessions.pop(session['uname'], None)
    session.clear()
    return redirect(url_for('login'))


@app.route('/main_menu', methods=['GET'])
@requires_auth
def main_menu():
    sess: DBSession = sessions[session['uname']]
    if sess.user_type == 2:
        return render_template('admin_main_menu.html', invalid=request.args.get('invalid', None, type=str))
    elif sess.user_type == 1:
        return render_template('manager_main_menu.html', invalid=request.args.get('invalid', None, type=str))
    else:
        return render_template('client_main_menu.html', invalid=request.args.get('invalid', None, type=str))


@app.route('/search_flights', methods=['GET'])
@requires_manager
def search_flights():
    try:
        args = request.args
        sess: DBSession = sessions[session['uname']]

        if 'dep' in args.keys() and 'arr' in args.keys():
            dep = args.get('dep')
            arr = args.get('arr')

            flights = sess.get_flights(dep, arr)
            
            if len(flights) != 0:
                return render_template('search_flights.html', flights=flights)

            return render_template('search_flights.html', invalid='No flights found')

        return render_template('search_flights.html')
    except:
        return render_template('search_flights.html', invalid='Incorrect input')


@app.route('/edit_passenger', methods=['GET', 'POST'])
@requires_auth
def edit_passenger():
    try:
        args = request.args
        sess: DBSession = sessions[session['uname']]

        if request.method == 'GET':
            if 'passport' in args.keys():
                if sess.user_type == 0:
                    seria, number = args.get('passport').split(' ')

                    passenger = sess.get_passenger(seria, number, session['uname'])
                    if passenger == Passenger():
                        return render_template('edit_passenger.html', invalid='Passenger not found')

                    session['seria'] = passenger.passport_seria
                    session['number'] = passenger.passport_number
                    return render_template('edit_passenger.html', passenger=passenger)

                if 'login' in args.keys():
                    seria, number = args.get('passport').split(' ')
                    uname = args.get('login')

                    passenger = sess.get_passenger(seria, number, uname)
                    if passenger == Passenger():
                        return render_template('edit_passenger.html', login=True, invalid='Passenger not found')

                    session['seria'] = seria
                    session['number'] = number
                    session['login_to_look'] = uname
                    return render_template('edit_passenger.html', login=True, passenger=passenger)

            if sess.user_type != 0:
                return render_template('edit_passenger.html', login=True)
            return render_template('edit_passenger.html')

        if request.method == 'POST':
            uname = session['uname'] if sess.user_type == 0 else session['login_to_look']

            editing_passenger = Passenger(
                session['seria'],
                session['number'],
                uname
            )

            passenger = Passenger(
                request.form['seria'],
                request.form['number'],
                uname,
                request.form['name'],
                request.form['sex'],
                request.form['citizenship']
            )

            sess.edit_passenger(passenger, editing_passenger)
            del session['seria']
            del session['number']
            return redirect(url_for('main_menu'))
    except:
        if sess.user_type == 0:
            return render_template('edit_passenger.html', invalid='Incorrect input')
        return render_template('edit_passenger.html', login=True, invalid='Incorrect input')


@app.route('/add_airport', methods=['GET', 'POST'])
@requires_admin
def add_airport():
    sess: DBSession = sessions[session['uname']]

    if request.method == 'GET':
        return render_template('add_airport.html')

    if request.method == 'POST':
        try:
            airport = Airport(
                request.form['code'],
                request.form['name'],
                request.form['country'],
                request.form['city'],
                request.form['hours'],
                request.form['minutes']
            )

            sess.add_airport(airport)

            return redirect(url_for('main_menu'))
        except Exception as e:
            e.with_traceback()
            return render_template('add_airport.html', invalid='Incorrect input')
    

@app.route('/edit_airport', methods=['GET', 'POST'])
@requires_admin
def edit_airport():
    args = request.args
    sess: DBSession = sessions[session['uname']]
    
    if request.method == 'GET':
        try:
            if 'code' not in args.keys():
                return render_template('edit_airport_info.html')

            code = args.get('code')

            airport = sess.get_airport(code)
            if airport is None:
                return render_template('edit_airport_info.html', invalid='Airport not found')

            session['IATA'] = code
            return render_template('edit_airport_info.html', airport=airport)
        except:
            return render_template('edit_airport_info.html', invalid='Incorrect input')

    if request.method == 'POST':
        try:
            old_airport = Airport(session['IATA'])
            airport = Airport(
                request.form['code'],
                request.form['name'],
                request.form['country'],
                request.form['city'],
                request.form['hours'],
                request.form['minutes'],
            )
            sess.edit_airport(airport, old_airport)
            del session['IATA']

            return redirect(url_for('main_menu'))
        except:
            return render_template('edit_airport_info.html', invalid='Incorrect input')


@app.route('/add_flight', methods=['GET', 'POST'])
@requires_admin
def add_flight():
    sess: DBSession = sessions[session['uname']]

    if request.method == 'GET':
        return render_template('add_flight.html')

    if request.method == 'POST':
        try:
            flight = Flight(
                request.form['number'],
                request.form['dep_date'],
                request.form['arr_date'],
                request.form['dep_time'],
                request.form['arr_time'],
                request.form['dep_code'],
                request.form['arr_code'],
                request.form['iata_code'],
                request.form['package'],
            )

            fare_basises = ['Y']
            costs = [request.form['economy']]

            if request.form['business'] != '-':
                fare_basises.append('C')
                costs.append(request.form['business'])

            sess.add_flight(flight, fare_basises, costs)

            return redirect(url_for('main_menu'))
        except Exception as e:
            e.with_traceback()
            return render_template('add_flight.html', invalid='Incorrect input')


@app.route('/edit_flight', methods=['GET', 'POST'])
@requires_manager
def edit_flight():
    sess: DBSession = sessions[session['uname']]

    if request.method == 'GET':
        try:
            flight_number = request.args.get('flight_number')
            dep_date = request.args.get('dep_date')

            flight = sess.get_flight(flight_number, dep_date)

            return render_template('edit_flight.html', flight=flight)
        except:
            return redirect(url_for('main_menu'))

    if request.method == 'POST':
        try:
            flight_number = request.args.get('flight_number')
            prev_date = request.args.get('dep_date')
            dep_date, dep_time = request.form['dep_datetime'].split('T')
            arr_date, arr_time = request.form['arr_datetime'].split('T')

            sess.edit_flight_schedule(flight_number, prev_date, dep_date, dep_time, arr_date, arr_time)

            return redirect(url_for('main_menu'))
        except:
            return render_template('edit_flight.html', invalid='Incorrect input')


@app.route('/client/search_flights', methods=['GET'])
@requires_auth
def client_search_flights():
    sess: DBSession = sessions[session['uname']]
    args = request.args

    if 'dep' in args.keys() and 'arr' in args.keys() and 'dep_date' in args.keys():
        try:
            dep = args.get('dep')
            arr = args.get('arr')
            passengers = int(args.get('passengers'))
            dep_date = args.get('dep_date')

            flights = sess.get_flights_with_date(dep, arr, dep_date)

            if len(flights) == 0:
                return render_template('client_search_flights.html', invalid='No flights found')

            for f in flights:
                f.cost *= passengers
            
            return render_template('client_search_flights.html', flights=flights, dep_date=dep_date, dep_code=dep, arr_code=arr, passengers=passengers)
        except:
            return render_template('client_search_flights.html', invalid='Incorrect input')
    return render_template('client_search_flights.html')


@app.route('/client/book_flights', methods=['GET', 'POST'])
@requires_auth
def client_book_flights():
    sess: DBSession = sessions[session['uname']]
    args = request.args

    if request.method == 'GET':
        try:
            flight = json.loads(args.get('flight'))
            session['flight'] = args.get('flight')
            passengers = int(args.get('passengers'))

            flight = FlightsView.from_json(flight)

            client_pass = sess.get_my_passengers()

            return render_template(
                'client_book_tickets.html',
                flight=flight,
                passengers=passengers,
                client_pass=client_pass)
        except:
            return redirect(url_for('client_search_flights'))

    if request.method == 'POST':
        p = request.args.get('passengers')
        passengers = []

        for i in range(1, int(p) + 1):
            passengers.append(
                Passenger(
                    request.form[f'passport_{i}'].split(' ')[0],
                    request.form[f'passport_{i}'].split(' ')[1],
                    session['uname'],
                    request.form[f'full_name_{i}'],
                    request.form[f'sex_{i}'],
                    request.form[f'citizenship_{i}']
                )
            )

        session['passengers'] = [p.to_json() for p in passengers]

        return redirect(url_for('purchase'))



@app.get('/get_passenger')
@requires_auth
def get_passenger():
    sess: DBSession = sessions[session['uname']]
    args = request.args

    try:
        seria, number = args.get('passport').split(' ')
        passenger = sess.get_passenger(seria, number, session['uname'])

        return json.dumps(passenger.__dict__)
    except:
        return json.dumps(Passenger().__dict__)

@app.route('/purchase', methods=['GET', 'POST'])
@requires_auth
def purchase():
    sess: DBSession = sessions[session['uname']]
    args = request.args

    if request.method == 'GET':
        try:
            flight = json.loads(session['flight'])
            passengers = [json.loads(p) for p in session['passengers']]

            flight = FlightsView.from_json(flight)
            passengers = [Passenger.from_json(p) for p in passengers]

            return render_template('purchase.html', flight=flight, passengers=passengers)
        except:
            return redirect(url_for('client_search_flights'))

    if request.method == 'POST':
        try:
            flight = json.loads(session['flight'])
            passengers = [json.loads(p) for p in session['passengers']]

            flight = FlightsView.from_json(flight)
            passengers = [Passenger.from_json(p) for p in passengers]

            pnr = sess.make_booking(flight, passengers)

            del session['flight']
            del session['passengers']

            session['pnr'] = pnr

            return redirect(url_for('purchase_completed'))
        except Exception as e:
            e.with_traceback()
            return redirect(url_for('client_search_flights', invalid='Something went wrong'))


@app.route('/purchase_completed', methods=['GET', 'POST'])
@requires_auth
def purchase_completed():
    if request.method == 'GET':
        return render_template('purchase_completed.html')

    if request.method == 'POST':
        try:
            return redirect(url_for('your_booking', pnr=session['pnr']))
        except:
            return redirect(url_for('main_menu'))


@app.route('/your_booking', methods=['GET'])
@requires_auth
def your_booking():
    try:
        session.pop('pnr', None)
        return render_template('your_booking.html', pnr=request.args.get('pnr'))
    except:
        return render_template('your_booking.html', invalid='Something went wrong')

@app.route('/booking_info', methods=['GET'])
@requires_auth
def booking_info():
    if 'uname' not in session or session['uname'] not in sessions.keys():
        return redirect(url_for('login'))

    sess: DBSession = sessions[session['uname']]
    args = request.args

    if 'pnr' in args.keys():
        try:
            pnr = args.get('pnr')
            tickets = sess.get_booking_tickets(pnr)

            if tickets is None:
                return render_template('booking_info.html', pnr=pnr, invalid='No bookings found')

            return render_template('booking_info.html', tickets=tickets, pnr=pnr)
        except Exception as e:
            e.with_traceback()
            return render_template('booking_info.html', invalid='Incorrect input')

    return render_template('booking_info.html')