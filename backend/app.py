from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()
url = os.environ.get("DATABASE_URL")

def connectDB():
    conn = psycopg2.connect(url)
    return conn

app = Flask(__name__)

@app.get("/")
def home():
    return "Flask App Running!"

@app.route("/api/playerinfo/<id>", methods=["GET"])
def playerinfo(id):
    conn = connectDB()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Query to get the row based on id
        cursor.execute("SELECT * FROM main WHERE id = %s", (id,))
        row = cursor.fetchone()
        
        if row is None:
            return jsonify({"error": "Row not found"}), 404

        return jsonify(row), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()
    