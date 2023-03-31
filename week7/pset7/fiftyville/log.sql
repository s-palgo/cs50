-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Running this query to get information about the crime scene and any possible clues
-- that will point me to how and in which table(s) I should run my next query
-- for information.
SELECT description FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND day = 28 AND street = "Humphrey Street";

-- I ran this query because one of the results from the previous query was about the
-- robbery and mentioned that the crime happened at the bakery and three witnesses
-- were interviewed, all of whom mentioned the bakery. So, I decided to search for
-- all the transcripts of interviews from this day. I also decided to query for
-- the names of the witnesses in anticipation of the possibility that the next
-- important piece of information may be related to the witnesses.
SELECT name, transcript FROM interviews WHERE year = 2021 AND month = 7 AND day = 28;

-- The previous query showed that Ruth saw the thief leave the bakery parking lot
-- within 10 minutes of the theft (theft happened at 10:15 AM) and so she suggested looking at
-- the security footage. Information from the security footage is in the bakery_security_logs table, so
-- that's where I ran my next query. I queried for the activity column to see what
-- types of activity were logged so that I could narrow down my search to only
-- yield me exits from the parking lot. Then I also queried for license plates to
-- get an idea of how many cars were captured by the footage so I could narrow my search.
SELECT activity, license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute > 14 AND minute < 26;

-- This query takes all of the thief's potential cars (via the license plates) and
-- procures the names of the owners/drivers of those cars. This, with the information
-- about the duration of the thief's call with his/her accomplice, will help me get
-- information about the caller and receiver (e.g. thief and accomplice) from the
-- phone_calls table.
SELECT name FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute > 14 AND minute < 26);

-- We know that the thief was looking for the earliest flight from Fiftyville for the
-- day after the theft. This means that the date of the flight was July 29th. Hence,
-- I queried for all of the flight IDs on July 29th which departed from Fiftyville,
-- and sorted them by their departure time. This helped me quickly isolate the flight ID
-- of the earliest flight on July 29, which is 36. This will help me match all the passengers
-- in this flight with the names of the potential thieves based on the license plate information.
SELECT id, hour, minute FROM flights WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id IN (SELECT id FROM airports WHERE city = "Fiftyville") ORDER BY hour;

-- This query gave me the passport numbers of all the passengers on the earliest flight
-- from Fiftyville on July 29th. The passport numbers can then be used to correlate with
-- the names of the passengers using the people table.
SELECT passport_number FROM passengers WHERE flight_id = 36;

-- Running this query gave me the names of all the passengers on the flight with ID #36,
-- e.g. the flight that the thief is suspected to be on the 29th.
SELECT name FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36);

-- This query captures the names of all the people who were on flight #36 and were
-- also in the list of people who drove away in a car 10 minutes after the theft.
SELECT name FROM people WHERE name IN (SELECT name FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36)) AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute > 14 AND minute < 26);

-- I ran this query to see what types of transaction types were in the database, so that
-- I could use the transaction type corresponding to withdrawing money to filter for
-- withdrawals on Leggett Street as is prescribed by a witness.
SELECT atm_location, transaction_type FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28;

-- This query gives me all the account numbers which withdrawed money from an ATM
-- on July 28th on Leggett Street.
SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw";

-- This query gave me all of the person_ids of the people who withdrawed money from an ATM
-- on July 28th on Leggett Street. This will be used to find the names of people who
-- were on flight #36, drove a car away within 10 minutes of the theft, and also
-- withdrawed money from an ATM on July 28th on Leggett Street.
SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw");

-- This query was to find the names of people who were on flight #36, drove a car
-- away within 10 minutes of the theft, and also withdrawed money from an ATM on
-- July 28th on Leggett Street.
SELECT name FROM people WHERE id in (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw")) AND name IN (SELECT name FROM people WHERE name IN (SELECT name FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36)) AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute > 14 AND minute < 26));

-- This query selects all the phone numbers of people who made calls on July 28th,
-- 2021 which lasted for less than a minute.
SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;

-- This query gives me all the names of the people who have phone numbers which
-- made a call on July 28th, 2021 which lasted for less than a minute.
SELECT name FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60);

-- This query was to find the names of all people who had all of the following
-- characteristics of the thief as identified by the witnesses:
-- 1. were on flight #36 on July 29th
-- 2. drove a car away from the bakery within 10 minutes of the theft (which happened at 10:15 AM)
-- 3. withdrew money from an ATM on Leggett Street on July 28th
-- 4. made a call on July 28th, 2021 which lasted for less than a minute.

-- ANSWER: This query gave me Bruce as the name of the thief.
SELECT name FROM people WHERE name IN (SELECT name FROM people WHERE id in (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw")) AND name IN (SELECT name FROM people WHERE name IN (SELECT name FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36)) AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute > 14 AND minute < 26))) AND name IN (SELECT name FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60));

-- This gives me Bruce's phone number which can be used to find the name of the
-- accomplice.
SELECT phone_number FROM people WHERE name = "Bruce";

-- This query gives me the phone number of the accomplice who Bruce called after
-- the theft.

-- ANSWER: This query gave me Robin as the name of the accomplice.
SELECT receiver FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND caller IN (SELECT phone_number FROM people WHERE name = "Bruce") AND duration < 60;

-- This query gives me the ID of the destination airport of the thief, e.g. Bruce.
-- I can use this ID to what city Bruce escaped to.
SELECT destination_airport_id FROM flights WHERE id = 36;

-- This query gives me the city of Bruce's destination airport, e.g. the city
-- he escaped to.

-- ANSWER: This query gave me New York City as the city which Bruce escaped to.
SELECT city FROM airports WHERE id IN (SELECT destination_airport_id FROM flights WHERE id = 36);