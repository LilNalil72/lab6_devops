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

@app.route("/schedules", methods=["GET"])
def get_schedules():
    doctor_id = request.args.get("doctor_id")
    with get_db_connection() as conn, conn.cursor() as cur:
        if doctor_id:
            cur.execute("SELECT * FROM schedules WHERE doctor_id = %s;", (doctor_id,))
        else:
            cur.execute("SELECT * FROM schedules;")
        return jsonify(cur.fetchall())

@app.route("/schedules", methods=["POST"])
def create_schedule():
    data = request.json
    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO schedules (doctor_id, work_date, start_time, end_time)
            VALUES (%s, %s, %s, %s);
            """,
            (data["doctor_id"], data["work_date"], data["start_time"], data["end_time"]),
        )
        conn.commit()
    return jsonify(status="created"), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
