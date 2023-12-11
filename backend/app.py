from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////root/db/db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create SQLAlchemy instance without associating it with the app
db = SQLAlchemy()

# Import and register routes
from routes import job_routes, log_message_routes

app.register_blueprint(job_routes)
app.register_blueprint(log_message_routes)

# Initialize the app context and associate the SQLAlchemy instance with the app
with app.app_context():
    db.init_app(app)

    # Create database tables
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
