from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager

# Initialize Flask app
app = Flask(__name__)
app.config.from_object("config.Config")

# Enable CORS
CORS(app)

# Initialize database
db = SQLAlchemy(app)

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Import and register routes
from routes import setup_routes
setup_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
