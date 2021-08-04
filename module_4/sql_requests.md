Задание 4.1

SELECT DISTINCT a.city,
                count(a.airport_name)
FROM dst_project.airports a
GROUP BY 1
HAVING count(a.airport_name) >= 2

/*
Moscow
3
Ulyanovsk
2
*/

Задание 4.2.1

SELECT count(DISTINCT status)
FROM dst_project.flights

/*
6
*/

Задание 4.2.2

SELECT count(aircraft_code)
FROM dst_project.flights
WHERE status = 'Departed'

/*
58
*/

Задание 4.2.3

SELECT count(seat_no)
FROM dst_project.seats
WHERE aircraft_code = '773'

/*
402
*/

Задание 4.2.4

SELECT count(flight_id)
FROM dst_project.flights
WHERE status = 'Arrived'
  AND actual_arrival BETWEEN '2017-04-01' AND '2017-09-01'

/*
74227
*/

Задание 4.3.1

SELECT count(flight_id)
FROM dst_project.flights
WHERE status = 'Cancelled'

/*
437
*/

Задание 4.3.2

SELECT 'Boeing' aircraft,
                count(*)
FROM dst_project.aircrafts a
WHERE a.model like 'Boeing%'
UNION ALL
SELECT 'Sukhoi Superjet' aircraft,
                        count(*)
FROM dst_project.aircrafts a
WHERE a.model like 'Sukhoi%'
UNION ALL
SELECT 'Airbus' aircraft,
                count(*)
FROM dst_project.aircrafts a
WHERE a.model like 'Airbus%'

/*
Boeing
3
Sukhoi Superjet
1
Airbus
3
*/

Задание 4.3.3

SELECT 'Asia' world_part,
              count(*)
FROM dst_project.airports ap
WHERE ap.timezone like 'Asia%'
UNION ALL
SELECT 'Europe' world_part,
                count(*)
FROM dst_project.airports ap
WHERE ap.timezone like 'Europe%'
UNION ALL
SELECT 'Australia' world_part,
                   count(*)
FROM dst_project.airports ap
WHERE ap.timezone like 'Australia%'
ORDER BY 2 DESC

/*
Asia
52
Europe
52
Australia
0
*/

Задание 4.3.4

SELECT f.flight_id,
       f.actual_arrival - f.scheduled_arrival delay
FROM dst_project.flights f
WHERE f.actual_arrival IS NOT NULL
ORDER BY delay DESC
LIMIT 1

/*
157,571
0 years 0 mons 0 days 5 hours 7 mins 0.00 secs
*/

Задание 4.4.1

SELECT f.scheduled_departure
FROM dst_project.flights f
ORDER BY 1
LIMIT 1

/*
август 14, 2016, 11:45 вечера
*/

Задание 4.4.2

SELECT EXTRACT(EPOCH
               FROM MAX(f.scheduled_arrival - f.scheduled_departure))/ 60
FROM dst_project.flights f

/*
530
*/

Задание 4.4.3

SELECT f.departure_airport,
       f.arrival_airport,
       f.scheduled_arrival - f.scheduled_departure
FROM dst_project.flights f
ORDER BY 3 DESC
LIMIT 1

/*
DME
UUS
0 years 0 mons 0 days 8 hours 50 mins 0.00 secs
*/

Задание 4.4.4

SELECT TRUNC (EXTRACT(EPOCH
                      FROM AVG(f.actual_arrival - f.actual_departure))/ 60)
FROM dst_project.flights f

/*
128
*/

Задание 4.5.1

SELECT fare_conditions,
       count(*)
FROM dst_project.seats
WHERE aircraft_code = 'SU9'
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1

/*
Economy
85
*/

Задание 4.5.2

SELECT MIN(total_amount)
FROM dst_project.bookings

/*
3400
*/

Задание 4.5.3

SELECT bp.seat_no
FROM dst_project.boarding_passes bp
JOIN dst_project.tickets t ON t.ticket_no = bp.ticket_no
WHERE t.passenger_id = '4313 788533'

/*
2A
*/

Задание 5.1.1

SELECT count(f.flight_id)
FROM dst_project.airports a
JOIN dst_project.flights f ON a.airport_code = f.arrival_airport
WHERE a.city = 'Anapa'
  AND f.actual_arrival BETWEEN '2017-01-01' AND '2017-12-31'

/*
456
*/

Задание 5.1.2

SELECT count(f.flight_id)
FROM dst_project.airports a
JOIN dst_project.flights f ON a.airport_code = f.departure_airport
WHERE a.city = 'Anapa'
  AND (date_trunc('month', f.actual_departure) in ('2017-01-01',
                                                 '2017-02-01',
                                                 '2017-12-01'))
  AND f.status not in ('Cancelled')

/*
127
*/

Задание 5.1.3

SELECT count(f.flight_id)
FROM dst_project.airports a
JOIN dst_project.flights f ON a.airport_code = f.departure_airport
WHERE a.city = 'Anapa'
  AND f.status in ('Cancelled')

/*
1
*/

Задание 5.1.4

SELECT count(f.flight_id)
FROM dst_project.airports a
JOIN dst_project.flights f ON a.airport_code = f.arrival_airport
WHERE a.city not in ('Moscow')
  AND f.departure_airport in ('AAQ')

/*
453
*/

Задание 5.1.5

SELECT ac.model,
       count(s.seat_no)
FROM dst_project.airports a
JOIN dst_project.flights f ON a.airport_code = f.arrival_airport
JOIN dst_project.aircrafts ac ON f.aircraft_code = ac.aircraft_code
JOIN dst_project.seats s ON s.aircraft_code = ac.aircraft_code
WHERE a.city = 'Anapa'
GROUP BY 1
LIMIT 1

/*
Boeing 737-300
58,890
*/

Финальный запрос!

SELECT f.flight_id,
       f.actual_departure,
       f.scheduled_departure,
       f.actual_arrival,
       f.scheduled_arrival,
       EXTRACT(EPOCH
               FROM (f.actual_arrival - f.actual_departure))/ 60 actual_flight_time,
       a7.city departure_city,
       f.departure_airport,
       ca.arrival_city,
       f.arrival_airport,
       a.model,
       a.range,
       a1.seats,
       a2.passengers,
       a3.economy_seats,
       a4.economy_passengers,
       a5.business_seats,
       a6.business_passengers,
       a2.profit
FROM dst_project.flights f
LEFT JOIN dst_project.aircrafts a ON f.aircraft_code = a.aircraft_code
LEFT JOIN dst_project.airports a7 ON f.departure_airport = a7.airport_code
LEFT JOIN
  (SELECT f.flight_id,
          ai.city arrival_city
   FROM dst_project.flights f
   LEFT JOIN dst_project.airports ai ON f.arrival_airport = ai.airport_code
   WHERE f.departure_airport = 'AAQ') ca ON f.flight_id = ca.flight_id
LEFT JOIN
  (SELECT s.aircraft_code,
          count(s.seat_no) seats
   FROM dst_project.seats s
   GROUP BY s.aircraft_code) a1 ON a1.aircraft_code = f.aircraft_code
LEFT JOIN
  (SELECT tf.flight_id,
          sum(tf.amount) profit,
          count(tf.ticket_no) passengers
   FROM dst_project.ticket_flights tf
   GROUP BY tf.flight_id) a2 ON f.flight_id = a2.flight_id
LEFT JOIN
  (SELECT s1.aircraft_code,
          count(s1.fare_conditions) economy_seats
   FROM dst_project.seats s1
   WHERE s1.fare_conditions = 'Economy'
   GROUP BY s1.aircraft_code) a3 ON f.aircraft_code = a3.aircraft_code
LEFT JOIN
  (SELECT tf1.flight_id,
          count(tf1.fare_conditions) economy_passengers
   FROM dst_project.ticket_flights tf1
   WHERE tf1.fare_conditions = 'Economy'
   GROUP BY tf1.flight_id) a4 ON f.flight_id = a4.flight_id
LEFT JOIN
  (SELECT s2.aircraft_code,
          count(s2.fare_conditions) business_seats
   FROM dst_project.seats s2
   WHERE s2.fare_conditions = 'Business'
   GROUP BY s2.aircraft_code) a5 ON f.aircraft_code = a5.aircraft_code
LEFT JOIN
  (SELECT tf2.flight_id,
          count(tf2.fare_conditions) business_passengers
   FROM dst_project.ticket_flights tf2
   WHERE tf2.fare_conditions = 'Business'
   GROUP BY tf2.flight_id) a6 ON f.flight_id = a6.flight_id
WHERE f.departure_airport = 'AAQ'
  AND (date_trunc('month', f.scheduled_departure) in ('2017-01-01',
                                                      '2017-02-01',
                                                      '2017-12-01'))
  AND f.status not in ('Cancelled')


