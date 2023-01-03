CREATE FUNCTION recalulate_total_fare() returns trigger AS
$add_booking_service$
BEGIN
    UPDATE booking
    SET fare = fare + (SELECT service_cost FROM extra_service WHERE extra_service.service_id = NEW.service_id)
    WHERE pnr = NEW.pnr;
    RETURN NEW;
end ;
$add_booking_service$ LANGUAGE plpgsql;


CREATE TRIGGER add_booking_service
    AFTER INSERT OR UPDATE
    ON booking_service
    FOR EACH STATEMENT
EXECUTE PROCEDURE recalulate_total_fare();


CREATE EXTENSION IF NOT EXISTS pgcrypto;


CREATE PROCEDURE add_client(c_login text, c_password text, usertype int, c_phone text, c_email text) AS
$$
BEGIN
    IF EXISTS(SELECT FROM account WHERE account_login = c_login) THEN
        RAISE EXCEPTION 'User with such login already exists';
    end if;

    INSERT INTO account(account_login, account_password, user_type, phone_number, account_email)
    VALUES (format('%s', c_login),
            crypt(format('%s', c_password), gen_salt('md5')),
            usertype,
            format('%s', c_phone),
            format('%s', c_email));

    EXECUTE format('CREATE USER %s WITH PASSWORD %L', $1, $2);

    IF ($3 = 1) THEN
        EXECUTE format('GRANT manager TO %s', $1);
    ELSE
        EXECUTE format('GRANT client TO %s', $1);
    end if;
    COMMIT;
end;
$$ LANGUAGE plpgsql;


CREATE INDEX ind_airport_iata ON airport (airport_code);
CREATE INDEX ind_airport_city ON airport (city);
CREATE INDEX ind_booking_pnr ON booking (pnr);
CREATE INDEX ind_passenger_name ON passenger (full_name);
CREATE INDEX ind_flight_number ON flight (flight_number);
CREATE INDEX ind_login ON account (account_login);


CREATE OR REPLACE VIEW all_flights AS
SELECT f.flight_number,
       a.airport_code     AS dep_code,
       a.airport_name     AS dep_name,
       a.country          AS dep_country,
       a.city             AS dep_city,
       b.airport_code     AS arr_code,
       b.airport_name     AS arr_name,
       b.country          AS arr_country,
       b.city             AS arr_city,
       f.dep_date         AS dep_date,
       f.arr_date         AS arr_date,
       local_dep_time,
       local_arr_time,
       fb.fare_basis_code AS fare_basis,
       fb.basis_cost      AS cost
FROM flight f
         RIGHT JOIN fare_basis fb on f.flight_number = fb.flight_number
         JOIN airport a ON f.dep_airport = a.airport_code
         JOIN airport b ON f.arr_airport = b.airport_code;


GRANT SELECT ON TABLE all_flights to client, manager;

CREATE OR REPLACE VIEW all_tickets AS
SELECT ticket_number,
       pnr,
       d.airport_code   AS dep_code,
       d.city           AS dep_city,
       d.country        AS dep_country,
       a.airport_code   AS arr_code,
       a.city           AS arr_city,
       a.country        AS arr_country,
       f.dep_date       AS dep_date,
       f.local_dep_time AS dep_time,
       f.arr_date       AS arr_date,
       f.local_arr_time AS arr_time,
       ticket_class,
       status,
       fare_basis_code,
       nvb,
       nva,
       baggage,
       t.flight_number  AS flight_number,
       p.full_name      AS passenger_name
FROM ticket t
         JOIN passenger p on p.passport_seria = t.passport_seria and p.passport_number = t.passport_number
         JOIN flight f on t.flight_number = f.flight_number
         JOIN airport a on f.arr_airport = a.airport_code
         JOIN airport d on f.dep_airport = d.airport_code;


GRANT SELECT ON TABLE all_tickets to client, manager;


CREATE OR REPLACE FUNCTION get_booking_tickets(booking_number text) RETURNS SETOF all_tickets
    LANGUAGE plpgsql
AS
$$
DECLARE
    r all_tickets%rowtype;
BEGIN
    FOR r IN (SELECT *
              FROM all_tickets
              WHERE pnr = $1)
        LOOP
            RETURN NEXT r;
        end loop;
end;
$$;


CREATE PROCEDURE add_passenger(p_seria int, p_number int, a_login text, p_name text, p_sex text, p_citizenship text)
    LANGUAGE plpgsql
AS
$$
BEGIN
    IF NOT EXISTS(SELECT FROM passenger WHERE passport_seria = $1 AND passport_number = $2 AND account_login = $3) THEN
        INSERT INTO passenger(passport_seria, passport_number, account_login, full_name, sex, citizenship) VALUES ($1, $2, $3, $4, $5, $6);
    end if;
end;
$$;


CREATE OR REPLACE FUNCTION generate_pnr() RETURNS text AS
$$
DECLARE
    chars  text[]  := '{0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z}';
    result text    := '';
    i      integer := 0;
BEGIN
    FOR i IN 1..6
        LOOP
            result := result || chars[1 + random() * (array_length(chars, 1) - 1)];
        end loop;
    IF EXISTS(SELECT FROM booking WHERE pnr = result) THEN
        result := generate_pnr();
    end if;

    RETURN result;
end;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION generate_ticket_number() RETURNS bigint AS
$$
DECLARE
    result bigint;
BEGIN
    result := floor(random() * 100000000000000);
    IF EXISTS(SELECT FROM ticket WHERE ticket_number = result) THEN
        result := generate_ticket_number();
    end if;

    RETURN result;
end;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE add_passenger_if_not_exists(seria int, number int, login text, full_name text, p_sex char(1),
                                             p_citizenship text) AS
$$
BEGIN
    IF NOT EXISTS(SELECT
                  FROM passenger
                  WHERE passport_seria = $1
                    AND passport_number = $2
                    AND account_login = $3) THEN
        INSERT INTO passenger(passport_seria, passport_number, account_login, full_name, sex, citizenship)
        VALUES ($1, $2, $3, $4, $5, $6);
    end if;
end;
$$ LANGUAGE plpgsql;
