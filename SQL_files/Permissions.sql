/*Creating roles*/

DROP ROLE IF EXISTS client;
CREATE ROLE client;
DROP ROLE IF EXISTS manager;
CREATE ROLE manager;

/*Granting and revoking permissions*/

GRANT SELECT ON TABLE airport to client, manager;
GRANT SELECT ON TABLE aircraft to client, manager;
GRANT SELECT ON TABLE aircraft_pack to client, manager;
GRANT SELECT ON TABLE extra_service to client, manager;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE passenger to client, manager;

GRANT SELECT, INSERT ON TABLE booking_service to client;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE booking_service TO manager;

GRANT SELECT ON TABLE flight to client;
GRANT SELECT, UPDATE, INSERT, DELETE ON TABLE flight to manager;

GRANT SELECT ON TABLE fare_basis to client;
GRANT SELECT, INSERT, UPDATE ON TABLE fare_basis to manager;

GRANT SELECT, INSERT ON TABLE booking to client;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE booking to manager;

GRANT SELECT, INSERT, UPDATE ON TABLE ticket to client;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE ticket to manager;

GRANT SELECT, INSERT, UPDATE ON TABLE account to client;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE account to manager;

GRANT SELECT ON TABLE boarding_pass to client;
GRANT SELECT, INSERT, UPDATE ON TABLE boarding_pass to manager;

