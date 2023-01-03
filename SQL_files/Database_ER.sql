/* Create Tables */
BEGIN;

CREATE SEQUENCE seq_tickets START 1001;

CREATE TABLE account
(
    account_login    varchar(20) NOT NULL,
    account_password varchar(50) NOT NULL,
    user_type        smallint    NOT NULL,
    phone_number     varchar(20) NOT NULL,
    account_email    varchar(30) NOT NULL,
    PRIMARY KEY (account_login)
) WITHOUT OIDS;


CREATE TABLE aircraft
(
    iata_type_code char(3)      NOT NULL,
    model_name     varchar(100) NOT NULL,
    PRIMARY KEY (iata_type_code)
) WITHOUT OIDS;


CREATE TABLE aircraft_pack
(
    iata_type_code  char(3) NOT NULL,
    pack_code       int     NOT NULL,
    economy_seats   int     NOT NULL,
    business_seats  int     NOT NULL,
    first_seats     int     NOT NULL,
    aircrafts_count int     NOT NULL,
    PRIMARY KEY (iata_type_code, pack_code)
) WITHOUT OIDS;


CREATE TABLE airport
(
    airport_code     char(3)      NOT NULL,
    airport_name     varchar(100) NOT NULL,
    country          varchar(100) NOT NULL,
    city             varchar(100) NOT NULL,
    timezone_hours   int          NOT NULL,
    timezone_minutes int          NOT NULL,
    PRIMARY KEY (airport_code)
) WITHOUT OIDS;


CREATE TABLE boarding_pass
(
    boarding_pass_id bigint     NOT NULL,
    seat             varchar(3) NOT NULL,
    gate             varchar(4) NOT NULL,
    ticket_number    bigint     NOT NULL,
    PRIMARY KEY (boarding_pass_id)
) WITHOUT OIDS;


CREATE TABLE booking
(
    PNR  char(6)         NOT NULL,
    fare decimal(100, 2) NOT NULL,
    PRIMARY KEY (PNR)
) WITHOUT OIDS;


CREATE TABLE booking_service
(
    PNR        char(6) NOT NULL,
    service_id int     NOT NULL,
    amount     int     NOT NULL,
    PRIMARY KEY (PNR, service_id)
) WITHOUT OIDS;


CREATE TABLE extra_service
(
    service_id   int             NOT NULL,
    service_name varchar(40)     NOT NULL,
    service_cost decimal(100, 2) NOT NULL,
    PRIMARY KEY (service_id)
) WITHOUT OIDS;


CREATE TABLE flight
(
    flight_number  int     NOT NULL,
    dep_date       date    NOT NULL,
    arr_date       date    NOT NULL,
    local_dep_time time    NOT NULL,
    local_arr_time time    NOT NULL,
    dep_airport    char(3) NOT NULL,
    arr_airport    char(3) NOT NULL,
    iata_type_code char(3) NOT NULL,
    pack_code      int     NOT NULL,
    PRIMARY KEY (flight_number, dep_date)
) WITHOUT OIDS;


CREATE TABLE fare_basis
(
    flight_number   int             NOT NULL,
    fare_basis_code varchar(5)      NOT NULL,
    dep_date        date            NOT NULL,
    basis_cost      decimal(100, 2) NOT NULL,
    PRIMARY KEY (flight_number, fare_basis_code, dep_date)
) WITHOUT OIDS;


CREATE TABLE passenger
(
    passport_seria  int          NOT NULL,
    passport_number int          NOT NULL,
    account_login   varchar(20)  NOT NULL,
    full_name       varchar(100) NOT NULL,
    sex             char(1)      NOT NULL,
    citizenship     varchar(30)  NOT NULL,
    PRIMARY KEY (passport_seria, passport_number, account_login)
) WITHOUT OIDS;


CREATE TABLE ticket
(
    ticket_number   bigint      NOT NULL,
    dep_date        date        NOT NULL,
    ticket_class    char(1)     NOT NULL,
    status          char(2)     NOT NULL,
    fare_basis_code varchar(5)  NOT NULL,
    NVB             date,
    NVA             date,
    baggage         boolean     NOT NULL,
    flight_number   int         NOT NULL,
    passport_seria  int         NOT NULL,
    passport_number int         NOT NULL,
    account_login   varchar(20) NOT NULL,
    PNR             char(6)     NOT NULL,
    PRIMARY KEY (ticket_number)
) WITHOUT OIDS;

CREATE SEQUENCE seq_ticket_number

/* Create Foreign Keys */

ALTER TABLE passenger
    ADD FOREIGN KEY (account_login)
        REFERENCES account (account_login)
        ON UPDATE CASCADE
        ON DELETE CASCADE
;


ALTER TABLE aircraft_pack
    ADD FOREIGN KEY (iata_type_code)
        REFERENCES aircraft (iata_type_code)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
;


ALTER TABLE flight
    ADD FOREIGN KEY (iata_type_code, pack_code)
        REFERENCES aircraft_pack (iata_type_code, pack_code)
        ON UPDATE CASCADE
        ON DELETE CASCADE
;


ALTER TABLE flight
    ADD FOREIGN KEY (dep_airport)
        REFERENCES airport (airport_code)
        ON UPDATE CASCADE
        ON DELETE CASCADE
;


ALTER TABLE flight
    ADD FOREIGN KEY (arr_airport)
        REFERENCES airport (airport_code)
        ON UPDATE CASCADE
        ON DELETE CASCADE
;


ALTER TABLE fare_basis
    ADD FOREIGN KEY (flight_number, dep_date)
        REFERENCES flight (flight_number, dep_date)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
;


ALTER TABLE booking_service
    ADD FOREIGN KEY (PNR)
        REFERENCES booking (PNR)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
;


ALTER TABLE ticket
    ADD FOREIGN KEY (PNR)
        REFERENCES booking (PNR)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
;



ALTER TABLE booking_service
    ADD FOREIGN KEY (service_id)
        REFERENCES extra_service (service_id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
;


ALTER TABLE ticket
    ADD FOREIGN KEY (flight_number, dep_date)
        REFERENCES flight (flight_number, dep_date)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
;


ALTER TABLE ticket
    ADD FOREIGN KEY (passport_seria, passport_number, account_login)
        REFERENCES passenger (passport_seria, passport_number, account_login)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
;


ALTER TABLE ticket
    ADD FOREIGN KEY (flight_number, dep_date, fare_basis_code)
        REFERENCES fare_basis (flight_number, dep_date, fare_basis_code)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
;


ALTER TABLE boarding_pass
    ADD FOREIGN KEY (ticket_number)
        REFERENCES ticket (ticket_number)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
;

COMMIT;







