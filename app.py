# app.py - GLAVNA DATOTEKA ZA POKRETANJE
from flask import Flask
from flask_cors import CORS
from app.routes import register_routes
from app.models import db

# === 1. KREIRAMO FLASK APLIKACIJU ===
app = Flask(__name__)
CORS(app)

# === 2. REGISTRIRAMO SVE RUTE ===
register_routes(app)

# === 3. POKREĆEMO APLIKACIJU ===
if __name__ == '__main__':
    print("=" * 50)
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)