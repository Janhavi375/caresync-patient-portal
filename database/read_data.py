# read_data.py
# CareSync Database Reader

import mysql.connector
from datetime import date

# DATABASE CONNECTION
connection = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    password='Janhavi@566',
    database='caresync',
    auth_plugin='caching_sha2_password'
)

cursor = connection.cursor(dictionary=True)

print('Connected to CareSync database.')
print('=' * 60)

# QUERY 1: How many doctors in each specialisation?
print()
print('QUERY 1: Doctor Count by Specialisation')
print('-' * 45)

cursor.execute(
    '''
    SELECT
        specialisation,
        COUNT(*) AS total_doctors
    FROM doctor
    WHERE is_active = 1
    GROUP BY specialisation
    ORDER BY total_doctors DESC
    '''
)

rows = cursor.fetchall()

for row in rows:
    print(f" {row['specialisation']:<25} {row['total_doctors']} doctors")

print()

# QUERY 2: Total revenue by billing status
print('QUERY 2: Revenue Summary by Bill Status')
print('-' * 45)

cursor.execute(
    '''
    SELECT
        status,
        COUNT(*) AS total_bills,
        ROUND(SUM(total_amount), 2) AS total_billed,
        ROUND(SUM(amount_paid), 2) AS total_paid
    FROM billing
    GROUP BY status
    ORDER BY total_billed DESC
    '''
)

rows = cursor.fetchall()

for row in rows:
    print(
        f" {row['status']:<20} "
        f"Bills: {row['total_bills']:<5} "
        f"Billed: ₹{row['total_billed']:<12} "
        f"Paid: ₹{row['total_paid']}"
    )

print()

# QUERY 3: Recent appointments
print('QUERY 3: Recent Appointments')
print('-' * 45)

cursor.execute(
    '''
    SELECT
        a.appointment_id,
        p.full_name AS patient_name,
        d.full_name AS doctor_name,
        a.appointment_date,
        a.status
    FROM appointment a
    JOIN patient p ON a.patient_id = p.patient_id
    JOIN doctor d ON a.doctor_id = d.doctor_id
    ORDER BY a.appointment_date DESC
    LIMIT 10
    '''
)

rows = cursor.fetchall()

for row in rows:
    print(
        f" Appointment {row['appointment_id']}: "
        f"{row['patient_name']} | "
        f"{row['doctor_name']} | "
        f"{row['appointment_date']} | "
        f"{row['status']}"
    )

print()

cursor.close()
connection.close()

print('Done. Database connection closed.')