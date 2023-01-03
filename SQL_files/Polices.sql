CREATE POLICY show_user_passengers ON passenger
    FOR SELECT TO client
    USING (account_login::text = CURRENT_USER);

CREATE POLICY add_passenger ON passenger
    FOR INSERT TO client
    WITH CHECK(account_login::text = CURRENT_USER);

ALTER TABLE passenger
    ENABLE ROW LEVEL SECURITY;

INSERT INTO passenger(passport_seria, passport_number, account_login, full_name, sex, citizenship)
VALUES (4016, 789304, 'apasovas', 'Ленин Владимир Ильич', 'M', 'Russia')