
from flask import Flask
from flask_cors import CORS
from app.routes import register_routes
from app.models import db


app = Flask(__name__)
CORS(app)


register_routes(app)


if __name__ == '__main__':
    print("=" * 50)
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)