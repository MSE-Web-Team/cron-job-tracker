from flask import Flask
from models import db
from routes import job_routes, log_message_routes
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////root/db/db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy extension with the Flask app
db.init_app(app)

# Register blueprints
app.register_blueprint(job_routes)
app.register_blueprint(log_message_routes)

if __name__ == '__main__':
    # Create the database tables before running the app
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
