from flask import Flask, jsonify, request
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

# Database connection settings
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "hospital")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "securepass")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/health")
def health():
    """Service health check endpoint"""
    return jsonify(status="healthy", version="3.0.0")

@app.route("/doctors", methods=["GET"])
def get_doctors():
    """Get list of all doctors"""
    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, full_name, specialization, phone FROM doctors;")
        doctors = []
        for row in cur.fetchall():
            doctors.append({
                "id": row[0],
                "full_name": row[1],
                "specialization": row[2],
                "phone": row[3] if len(row) > 3 else None
            })
        return jsonify(doctors)

@app.route("/doctors", methods=["POST"])
def create_doctor():
    """Create a new doctor"""
    data = request.json
    required = ['full_name', 'specialization']
    if not all(field in data for field in required):
        return jsonify(error="Missing required fields"), 400

    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO doctors (full_name, specialization, phone) VALUES (%s, %s, %s) RETURNING id;",
            (data['full_name'], data['specialization'], data.get('phone'))
        )
        doctor_id = cur.fetchone()[0]
        conn.commit()
        return jsonify(id=doctor_id), 201

@app.route("/patients", methods=["GET"])
def get_patients():
    """Get list of all patients"""
    search = request.args.get('search', '')
    
    with get_db_connection() as conn, conn.cursor() as cur:
        query = "SELECT id, full_name, policy_number, email FROM patients"
        params = []
        
        if search:
            query += " WHERE full_name ILIKE %s OR policy_number ILIKE %s"
            params.extend([f'%{search}%', f'%{search}%'])
        
        query += " ORDER BY full_name;"
        cur.execute(query, params)
        
        patients = []
        for row in cur.fetchall():
            patients.append({
                "id": row[0],
                "full_name": row[1],
                "policy_number": row[2],
                "email": row[3]
            })
        return jsonify(patients)        

@app.route("/patients", methods=["POST"])
def create_patient():
    """Register a new patient"""
    data = request.json
    required = ['full_name', 'policy_number']
    if not all(field in data for field in required):
        return jsonify(error="Missing required fields"), 400

    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO patients (full_name, policy_number, email) VALUES (%s, %s, %s) RETURNING id;",
            (data['full_name'], data['policy_number'], data.get('email'))
        )
        patient_id = cur.fetchone()[0]
        conn.commit()
        return jsonify(id=patient_id), 201

@app.route("/patients/<int:patient_id>", methods=["GET"])
def get_patient(patient_id):
    """Get patient details"""
    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT id, full_name, policy_number, email FROM patients WHERE id = %s;",
            (patient_id,)
        )
        patient = cur.fetchone()
        if not patient:
            return jsonify(error="Patient not found"), 404
            
        return jsonify({
            "id": patient[0],
            "full_name": patient[1],
            "policy_number": patient[2],
            "email": patient[3]
        })

@app.route("/appointments", methods=["POST"])
def create_appointment():
    """Create a new appointment"""
    data = request.json
    required = ['doctor_id', 'patient_id', 'appointment_time']
    if not all(field in data for field in required):
        return jsonify(error="Missing required fields"), 400

    try:
        # Validate appointment time format
        appointment_time = datetime.fromisoformat(data['appointment_time'])
        if appointment_time < datetime.now():
            return jsonify(error="Appointment time must be in the future"), 400
    except ValueError:
        return jsonify(error="Invalid time format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"), 400

    with get_db_connection() as conn, conn.cursor() as cur:
        # Check if doctor exists
        cur.execute("SELECT 1 FROM doctors WHERE id = %s;", (data['doctor_id'],))
        if not cur.fetchone():
            return jsonify(error="Doctor not found"), 404

        # Check if patient exists
        cur.execute("SELECT 1 FROM patients WHERE id = %s;", (data['patient_id'],))
        if not cur.fetchone():
            return jsonify(error="Patient not found"), 404

        # Create appointment
        cur.execute(
            """
            INSERT INTO appointments (doctor_id, patient_id, appointment_time)
            VALUES (%s, %s, %s)
            RETURNING id;
            """,
            (data['doctor_id'], data['patient_id'], data['appointment_time'])
        )
        appointment_id = cur.fetchone()[0]
        conn.commit()
        return jsonify(id=appointment_id), 201

@app.route("/appointments", methods=["GET"])
def get_appointments():
    """Get appointments with optional filters"""
    doctor_id = request.args.get('doctor_id')
    patient_id = request.args.get('patient_id')
    status = request.args.get('status', 'planned')

    query = """
        SELECT a.id, a.appointment_time, a.status,
               d.id AS doctor_id, d.full_name AS doctor_name,
               p.id AS patient_id, p.full_name AS patient_name
        FROM appointments a
        JOIN doctors d ON a.doctor_id = d.id
        JOIN patients p ON a.patient_id = p.id
        WHERE a.status = %s
    """
    params = [status]

    if doctor_id:
        query += " AND a.doctor_id = %s"
        params.append(doctor_id)
    if patient_id:
        query += " AND a.patient_id = %s"
        params.append(patient_id)

    query += " ORDER BY a.appointment_time;"

    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute(query, params)
        appointments = []
        for row in cur.fetchall():
            appointments.append({
                "id": row[0],
                "appointment_time": row[1].isoformat(),
                "status": row[2],
                "doctor": {"id": row[3], "name": row[4]},
                "patient": {"id": row[5], "name": row[6]}
            })
        return jsonify(appointments)

@app.route("/appointments/<int:appointment_id>", methods=["PUT"])
def update_appointment(appointment_id):
    """Update appointment status"""
    data = request.json
    if 'status' not in data:
        return jsonify(error="Missing status field"), 400

    valid_statuses = ['planned', 'completed', 'cancelled']
    if data['status'] not in valid_statuses:
        return jsonify(error=f"Invalid status. Valid options: {', '.join(valid_statuses)}"), 400

    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "UPDATE appointments SET status = %s WHERE id = %s;",
            (data['status'], appointment_id)
        )
        if cur.rowcount == 0:
            return jsonify(error="Appointment not found"), 404
        conn.commit()
        return jsonify(success=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)