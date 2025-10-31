
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector as mysql
import os

app = Flask(__name__)
CORS(app)

def get_db():
    return mysql.connect(
        host=os.getenv("DB_HOST","127.0.0.1"),
        user=os.getenv("DB_USER","root"),
        password=os.getenv("DB_PASS",""),
        database=os.getenv("DB_NAME","virtual_study_groups"),
        port=int(os.getenv("DB_PORT","3306"))
    )

@app.get("/health")
def health(): return {"status":"ok"}

@app.post("/api/auth/login")
def login():
    data = request.get_json() or {}
    email = data.get("email"); password = data.get("password")
    if not email or not password:
        return jsonify({"error":"email and password required"}), 400
    return jsonify({"token":"demo-token","user":{"email":email}})

@app.get("/api/groups")
def groups():
    try:
        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT id, name, description FROM study_groups ORDER BY id DESC")
        out = cur.fetchall()
        cur.close(); db.close()
        return jsonify(out)
    except Exception as e:
        return jsonify({"error":str(e)}), 500

@app.post("/api/groups")
def create_group():
    d = request.get_json() or {}
    name = d.get("name"); desc = d.get("description","")
    if not name: return jsonify({"error":"name required"}), 400
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO study_groups (name, description, owner_id) VALUES (%s,%s,%s)", (name, desc, 1))
        db.commit()
        gid = cur.lastrowid
        cur.close(); db.close()
        return jsonify({"id":gid,"name":name,"description":desc}), 201
    except Exception as e:
        return jsonify({"error":str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
