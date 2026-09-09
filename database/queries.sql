CREATE OR REPLACE VIEW vw_doctor_appointment_summary AS
SELECT
    d.doctor_id,
    d.full_name AS doctor_name,
    COUNT(a.appointment_id) AS total_appointments
FROM doctor d
LEFT JOIN appointment a
    ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id, d.full_name;