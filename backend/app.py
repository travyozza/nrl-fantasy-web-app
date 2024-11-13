from flask import Flask, jsonify, request
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
url = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(url)

app = Flask(__name__)

@app.get("/")
def home():
    return "Flask App Running!"