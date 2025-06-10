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

@app.route("/doctors", methods=["POST"])
def create_doctor():
    data = request.json
    conn = get_conn(); cur = conn.cursor()
    cur.execute(
        "INSERT INTO doctors (name, specialty) VALUES (%s,%s) RETURNING id",
        (data["name"], data["specialty"])
    )
    did = cur.fetchone()[0]
    conn.commit(); cur.close(); conn.close()
    return jsonify({"id": did}), 201

@app.route("/shifts", methods=["POST"])
def create_shift():
    data = request.json
    conn = get_conn(); cur = conn.cursor()
    cur.execute(
        "INSERT INTO shifts (doctor_id, start_time, end_time) VALUES (%s,%s,%s) RETURNING id",
        (data["doctor_id"], data["start_time"], data["end_time"])
    )
    sid = cur.fetchone()[0]
    conn.commit(); cur.close(); conn.close()
    return jsonify({"id": sid}), 201

@app.route("/doctors", methods=["GET"])
def list_doctors():
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT id, name, specialty FROM doctors")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return jsonify([{"id": r[0],"name": r[1],"specialty": r[2]} for r in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0")
