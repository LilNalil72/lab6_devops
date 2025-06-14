from flask import Flask, jsonify, request
import psycopg2, os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "hospital")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "securepass")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )

@app.route("/appointments", methods=["GET"])
def get_appointments():
    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM appointments;")
        return jsonify(cur.fetchall())

@app.route("/appointments", methods=["POST"])
def create_appointment():
    data = request.json
    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO appointments (doctor_id, patient_id, appointment_time, status)
            VALUES (%s, %s, %s, %s);
            """,
            (data["doctor_id"], data["patient_id"], data["appointment_time"], "planned"),
        )
        conn.commit()
    return jsonify(status="created"), 201

@app.route("/health")
def health():
    return jsonify(status="healthy", version="2.0.0")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
