-- Step 1: Query the the description field of the "crime_scene_reports" table.
SELECT
  description
FROM
  crime_scene_reports
WHERE
  year = 2021
  AND month = 7
  AND day = 28
  AND street = "Humphrey Street";

-- Results
-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
-- Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.
----------------------------------------------------
-- Step 2: Query the keyword within the transcript field of the "interviews" table.

SELECT
  transcript
FROM
  interviews
WHERE
  transcript LIKE "%bakery%";

-- Results
-- Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
-- If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.

-- I don't know the thief's name, but it was someone I recognized.
-- Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

-- As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
-- In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
-- The thief then asked the person on the other end of the phone to purchase the flight ticket.
----------------------------------------------------
-- Step 3: Find the the city the thief ESCAPED TO
SELECT
  *
FROM
  flights
WHERE
  year = 2021
  AND month = 7
  AND day = 29
ORDER BY
  hour
LIMIT
  1;

-- Step 3.1 Get the city name by query the airports table
SELECT
  city
FROM
  airports
WHERE
  id == 4;

-- The city the thief ESCAPED TO: New York City
----------------------------------------------------
-- Step 4: Find the suspects by flight ID = 36

SELECT
  people.name,
  people.phone_number,
  people.passport_number,
  people.license_plate
FROM
  passengers
  JOIN people ON people.passport_number = passengers.passport_number
WHERE
  flight_id == 36;


-- The suspects are
-- --+--------+----------------+-----------------+---------------+
-- |  name  |  phone_number  | passport_number | license_plate |
-- +--------+----------------+-----------------+---------------+
-- | Doris  | (066) 555-9701 | 7214083635      | M51FA04       |
-- | Sofia  | (130) 555-0289 | 1695452385      | G412CB7       |
-- | Bruce  | (367) 555-5533 | 5773159633      | 94KL13X       |
-- | Edward | (328) 555-1152 | 1540955065      | 130LD9Z       |
-- | Kelsey | (499) 555-9472 | 8294398571      | 0NTHK55       |
-- | Taylor | (286) 555-6063 | 1988161715      | 1106N58       |
-- | Kenny  | (826) 555-1652 | 9878712108      | 30G67EN       |
-- | Luca   | (389) 555-5198 | 8496433585      | 4328GD8       |
-- +--------+----------------+-----------------+---------------+

----------------------------------------------------
-- Step 5: Find the insight in "bakery_security_logs" table
SELECT
  *
FROM
  bakery_security_logs
  JOIN people ON people.license_plate == bakery_security_logs.license_plate
WHERE
  year == 2021
  AND month == 7
  AND day == 28
  AND hour == 10
  AND minute BETWEEN 15
  AND 30
  AND bakery_security_logs.activity == "exit"
  AND bakery_security_logs.license_plate IN (
    'M51FA04', 'G412CB7', '94KL13X', '130LD9Z',
    '0NTHK55', '1106N58', '30G67EN',
    '4328GD8'
  );

-- +-----+------+-------+-----+------+--------+----------+---------------+--------+--------+----------------+-----------------+---------------+
-- | id  | year | month | day | hour | minute | activity | license_plate |   id   |  name  |  phone_number  | passport_number | license_plate |
-- +-----+------+-------+-----+------+--------+----------+---------------+--------+--------+----------------+-----------------+---------------+
-- | 261 | 2021 | 7     | 28  | 10   | 18     | exit     | 94KL13X       | 686048 | Bruce  | (367) 555-5533 | 5773159633      | 94KL13X       |
-- | 263 | 2021 | 7     | 28  | 10   | 19     | exit     | 4328GD8       | 467400 | Luca   | (389) 555-5198 | 8496433585      | 4328GD8       |
-- | 264 | 2021 | 7     | 28  | 10   | 20     | exit     | G412CB7       | 398010 | Sofia  | (130) 555-0289 | 1695452385      | G412CB7       |
-- | 267 | 2021 | 7     | 28  | 10   | 23     | exit     | 0NTHK55       | 560886 | Kelsey | (499) 555-9472 | 8294398571      | 0NTHK55       |
-- +-----+------+-------+-----+------+--------+----------+---------------+--------+--------+----------------+-----------------+---------------+

----------------------------------------------------
-- Step 6: Find the suspects more precisely

SELECT
  phone_calls.caller,
  people.name,
  people.license_plate,
  people.passport_number
FROM
  phone_calls
  JOIN people ON people.phone_number = phone_calls.caller
  JOIN passengers ON passengers.passport_number == people.passport_number
WHERE
  year == 2021
  AND month == 7
  AND day == 28
  AND duration < 60
  AND license_plate IN (
    '94KL13X', '4328GD8', 'G412CB7', '0NTHK55'
  )
  AND passengers.flight_id == 36;


-- +----------------+--------+---------------+-----------------+
-- |     caller     |  name  | license_plate | passport_number |
-- +----------------+--------+---------------+-----------------+
-- | (130) 555-0289 | Sofia  | G412CB7       | 1695452385      |
-- | (499) 555-9472 | Kelsey | 0NTHK55       | 8294398571      |
-- | (367) 555-5533 | Bruce  | 94KL13X       | 5773159633      |
-- | (499) 555-9472 | Kelsey | 0NTHK55       | 8294398571      |
-- +----------------+--------+---------------+-----------------+
-- The suspects are Sofia, Kelsey and Bruce

----------------------------------------------------
-- Step 7. Find the bank_accounts for Sofia, Kelsey and Bruce
SELECT
  *
FROM
  bank_accounts
  JOIN people ON people.id == bank_accounts.person_id
WHERE
  people.name IN ("Sofia", "Kelsey", "Bruce");

-- +----------------+-----------+---------------+--------+-------+----------------+-----------------+---------------+
-- | account_number | person_id | creation_year |   id   | name  |  phone_number  | passport_number | license_plate |
-- +----------------+-----------+---------------+--------+-------+----------------+-----------------+---------------+
-- | 49610011       | 686048    | 2010          | 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
-- +----------------+-----------+---------------+--------+-------+----------------+-----------------+---------------+

-- The THIEF is: Bruce
----------------------------------------------------
-- Step 8: Find ACCOMPLICE
SELECT
  *
FROM
  phone_calls
  JOIN people ON people.phone_number = phone_calls.caller
WHERE
  year == 2021
  AND month == 7
  AND day == 28
  AND duration < 60
  AND caller == "(367) 555-5533";

-- The receiver is (375) 555-8161

SELECT
  *
FROM
  people
WHERE
  phone_number == "(375) 555-8161";


-- +--------+-------+----------------+-----------------+---------------+
-- |   id   | name  |  phone_number  | passport_number | license_plate |
-- +--------+-------+----------------+-----------------+---------------+
-- | 864400 | Robin | (375) 555-8161 | NULL            | 4V16VO0       |
-- +--------+-------+----------------+-----------------+---------------+

-- The ACCOMPLICE is: Robin