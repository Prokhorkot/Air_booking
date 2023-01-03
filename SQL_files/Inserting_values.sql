
INSERT INTO aircraft_pack(iata_type_code, pack_code, economy_seats, business_seats, first_seats, aircrafts_count)
VALUES ('320', 1, 120, 20, 0, 10),
       ('320', 2, 150, 8, 0, 10),
       ('32N', 1, 144, 12, 0, 5),
       ('321', 1, 142, 28, 0, 7),
       ('321', 2, 167, 16, 0, 7),
       ('32Q', 1, 184, 12, 0, 10),
       ('77W', 1, 372, 30, 0, 10),
       ('77W', 2, 399, 28, 0, 10),
       ('738', 1, 138, 20, 0, 15)
;

INSERT INTO flight(flight_number, dep_date, arr_date, local_dep_time, local_arr_time, dep_airport, arr_airport,
                   iata_type_code, pack_code)
VALUES (1002, '2023-01-21', '2023-01-21', '06:05', '10:30', 'DME', 'BAX', '77W', 1),
       (17789, '2023-01-26', '2023-01-26', '12:00', '16:00', 'DME', 'DIA', '77W', 2),
       (88192, '2023-03-08', '2023-03-09', '20:00', '00:50', 'DME', 'LHR', '77W', 2)
;

INSERT INTO fare_basis(flight_number, dep_date, fare_basis_code, basis_cost)
VALUES (1002, '2023-01-21', 'Y', 25000.00),
       (1002, '2023-01-21', 'C', 100000.00),
       (17789, '2023-01-26', 'Y', 25000.00),
       (17789, '2023-01-26', 'C', 102000.00),
       (88192, '2023-03-08', 'Y', 6017.00),
       (88192, '2023-03-08', 'C', 40000.00)
;


CALL add_client('prokhorkot', 'Pk23072002', 0, '+7 (931) 255-49-10', 'prokhorusa@gmail.com');
CALL add_client('apasovas', 'Av11072002', 0, '+7 (915) 677-81-53', 'apasovas@yandex.ru');
CALL add_client('gorokhov', 'Dg17042002', 1, '+7 (915) 674-91-52', 'gorokgov@gmail.com');
INSERT INTO account VALUES ('kotprokhor', crypt('Pk23072002', gen_salt('md5')), 2, '+7 (926) 563-41-46', 'kotprokhor@gmail.com');


INSERT INTO passenger(passport_seria, passport_number, account_login, full_name, sex, citizenship)
VALUES (4018, 792042, 'prokhorkot', 'Зубенко Михаил Петрович', 'M', 'Russia'),
       (4128, 929821, 'prokhorkot', 'Морская Наталья Пехота', 'F', 'Russia'),
       (4278, 671234, 'prokhorkot', 'Федоров Мирон Янович', 'M', 'United Kingdom')
;

INSERT INTO extra_service(service_id, service_name, service_cost)
VALUES (10, 'Extra space', 500.00),
       (12, 'Fixed seat class 1', 300.00),
       (14, 'Fixed seat class 2', 400.00),
       (16, 'Insurance', 600.00)
;

INSERT INTO booking(pnr, fare)
VALUES ('JSU67S', 12034.00),
       ('HDO923', 102000.00),
       ('456GHJ', 25000.00),
       ('AIU8KK', 25900.00)
;

INSERT INTO booking_service(pnr, service_id, amount)
VALUES ('JSU67S', 10, 2),
       ('456GHJ', 12, 1),
       ('AIU8KK', 14, 1),
       ('AIU8KK', 10, 1)
;


INSERT INTO ticket(ticket_number, dep_date, ticket_class, status, fare_basis_code, baggage,
                   flight_number,
                   passport_seria, passport_number, account_login, pnr)
VALUES (4252412255043, '2023-01-21', 'Y', 'OK', 'Y', false, 1002, 4018, 792042, 'prokhorkot', 'AIU8KK'),
       (9152962245043, '2023-01-26', 'C', 'OK', 'C', true, 17789, 4128, 929821, 'prokhorkot', 'HDO923'),
       (8237539546032, '2023-03-08', 'Y', 'OK', 'Y', true, 88192, 4278, 671234, 'prokhorkot', 'JSU67S'),
       (7459682239450, '2023-03-08', 'Y', 'OK', 'Y', false, 88192, 4278, 671234, 'prokhorkot', 'JSU67S')
;

INSERT INTO boarding_pass(boarding_pass_id, seat, gate, ticket_number)
VALUES (537383, '25A', 'C10', 4252412255043),
       (348986, '2A', 'D3', 9152962245043),
       (567812, '18C', 'D10', 8237539546032),
       (838495, '18B', 'D10', 7459682239450)
;