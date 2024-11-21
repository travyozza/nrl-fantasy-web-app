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

team_ids = {'Sharks': 500028, 'Storm': 500021, 'Panthers': 500014, 'Broncos': 500011, 'Sea Eagles': 500002, 'Warriors': 500032, 'Knights': 500003, 'Cowboys': 500012, 'Bulldogs': 500010, 'Rabbitohs': 500005, 'Roosters': 500001, 'Tigers': 500023, 'Dragons': 500022, 'Titans': 500004, 'Raiders': 500013, 'Eels': 500031, 'Dolphins': 500723}

app = Flask(__name__)

@app.get("/")
def home():
    return "Flask App Running!"

@app.route("/api/data/playerinfo/<id>", methods=["GET"])
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

@app.route("/api/data/playerinfo/<first_name>-<last_name>", methods=["GET"])
def playerInfo_byName(first_name, last_name):
    conn = connectDB()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("SELECT * FROM main WHERE first_name ILIKE %s and last_name ILIKE %s", (first_name, last_name))
        row = cursor.fetchall()
        
        if row is None:
            return jsonify({"error": "Row not found"}), 404

        return jsonify(row), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

@app.route("/api/data/team/<team_name>", methods=["GET"])
def getTeams(team_name):
    team_name = team_name.capitalize()
    conn = connectDB()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute("SELECT * FROM main WHERE squad_id = %s", (team_ids[team_name],))
        rows = cursor.fetchall()

        if rows is None:
            return jsonify({"error": "Team not found"}), 404

        return jsonify(rows), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()