from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

@app.route("/patients", methods=["POST"])
def create_patient():
    data = request.json
    conn = get_conn(); cur = conn.cursor()
    cur.execute(
        "INSERT INTO patients (name, birth_date, phone) VALUES (%s,%s,%s) RETURNING id",
        (data["name"], data["birth_date"], data["phone"])
    )
    pid = cur.fetchone()[0]
    conn.commit(); cur.close(); conn.close()
    return jsonify({"id": pid}), 201

@app.route("/appointments", methods=["POST"])
def create_appointment():
    data = request.json
    conn = get_conn(); cur = conn.cursor()
    cur.execute(
        "INSERT INTO appointments (patient_id, date_time) VALUES (%s,%s) RETURNING id",
        (data["patient_id"], data["date_time"])
    )
    aid = cur.fetchone()[0]
    conn.commit(); cur.close(); conn.close()
    return jsonify({"id": aid}), 201

@app.route("/patients", methods=["GET"])
def list_patients():
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT id, name, birth_date, phone FROM patients")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return jsonify([{"id": r[0],"name": r[1],"birth_date": str(r[2]),"phone": r[3]} for r in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0")
