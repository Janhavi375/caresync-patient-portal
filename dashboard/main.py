# main.py
# CareSync Dashboard Backend

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

# Create the FastAPI application
app = FastAPI(title='CareSync Dashboard API')

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['GET'],
    allow_headers=['*'],
)

# Database connection helper
def get_db():
    return mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='Janhavi@566',
        database='caresync',
        auth_plugin='caching_sha2_password'
    )

# ENDPOINT 1: Summary numbers
@app.get('/summary')
def get_summary():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        'SELECT COUNT(*) AS total FROM patient WHERE is_deleted = 0'
    )
    patients = cursor.fetchone()['total']

    cursor.execute(
        'SELECT COUNT(*) AS total FROM doctor WHERE is_active = 1'
    )
    doctors = cursor.fetchone()['total']

    cursor.execute(
        'SELECT COUNT(*) AS total FROM appointment'
    )
    appointments = cursor.fetchone()['total']

    cursor.execute(
        'SELECT COUNT(*) AS total FROM billing'
    )
    bills = cursor.fetchone()['total']

    cursor.execute(
        "SELECT COUNT(*) AS total FROM billing WHERE status = 'Rejected'"
    )
    rejected = cursor.fetchone()['total']

    rejection_rate = round(
        (rejected / bills * 100), 1
    ) if bills > 0 else 0

    cursor.execute(
        'SELECT ROUND(SUM(amount_paid), 2) AS total FROM billing'
    )
    revenue = cursor.fetchone()['total'] or 0

    cursor.close()
    db.close()

    return {
        'total_patients': patients,
        'total_doctors': doctors,
        'total_appointments': appointments,
        'total_bills': bills,
        'rejection_rate': rejection_rate,
        'total_revenue': float(revenue),
    }


# ENDPOINT 2: Patient list
@app.get('/patients')
def get_patients():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        '''
        SELECT
        patient_id,
        full_name,
        gender,
        blood_group,
        DATE_FORMAT(date_of_birth, '%d %b %Y') AS date_of_birth,
        DATE_FORMAT(created_at, '%d %b %Y') AS registered_on
        FROM patient
        WHERE is_deleted = 0
        ORDER BY created_at DESC
        LIMIT 50
        '''
    )

    patients = cursor.fetchall()

    cursor.close()
    db.close()

    return {'patients': patients}


# ENDPOINT 3: Billing summary
@app.get('/billing')
def get_billing():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        '''
        SELECT
        b.bill_id,
        p.full_name AS patient_name,
        b.total_amount,
        b.amount_paid,
        b.status,
        DATE_FORMAT(b.bill_date, '%d %b %Y') AS bill_date
        FROM billing b
        JOIN patient p ON p.patient_id = b.patient_id
        ORDER BY b.created_at DESC
        LIMIT 50
        '''
    )

    bills = cursor.fetchall()

    for bill in bills:
        bill['total_amount'] = float(bill['total_amount'])
        bill['amount_paid'] = float(bill['amount_paid'])

    cursor.close()
    db.close()

    return {'bills': bills}


# ENDPOINT 4: Doctor list
@app.get('/doctors')
def get_doctors():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        '''
        SELECT
        d.doctor_id,
        d.full_name,
        d.specialisation,
        COUNT(a.appointment_id) AS total_appointments
        FROM doctor d
        LEFT JOIN appointment a ON a.doctor_id = d.doctor_id
        AND a.status = 'Completed'
        WHERE d.is_active = 1
        GROUP BY d.doctor_id, d.full_name, d.specialisation
        ORDER BY total_appointments DESC
        '''
    )

    doctors = cursor.fetchall()

    cursor.close()
    db.close()

    return {'doctors': doctors}

from fastapi import HTTPException

@app.get("/patients/{patient_id}")
def get_patient_by_id(patient_id: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM patient WHERE patient_id = %s",
        (patient_id,)
    )

    patient = cursor.fetchone()

    cursor.close()
    db.close()

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient

@app.get("/patients/{patient_id}/appointments")
def get_patient_appointments(patient_id: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT a.*
        FROM appointment a
        JOIN patient p ON a.patient_id = p.patient_id
        WHERE p.patient_id = %s
        """,
        (patient_id,)
    )

    appointments = cursor.fetchall()

    cursor.close()
    db.close()

    return appointments

# ENDPOINT: Doctor Analytics
@app.get("/analytics/doctors")
def get_doctor_analytics():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            doctor_name,
            total_appointments
        FROM vw_doctor_appointment_summary
        ORDER BY total_appointments DESC
    """)

    doctors = cursor.fetchall()

    cursor.close()
    db.close()

    return doctors