from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pytz import timezone

db = SQLAlchemy()
utah = timezone('US/Mountain')

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    process_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    ongoing = db.Column(db.Boolean(), default=True)  # Defaulting to ongoing
    start_time = db.Column(db.DateTime, default=datetime.now())
    end_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Enum('EMERGENCY', 'SUCCESS', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'LOG', 'RUNNING'), default='SUCCESS')

    def __repr__(self):
        return f'<Job {self.id}, {self.process_name}, Status: {self.status}>'

class LogMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    process_name = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now())
    message = db.Column(db.String(255), nullable=False)
    level = db.Column(db.Enum('EMERGENCY', 'SUCCESS', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'LOG'), default='INFO')

    def __repr__(self):
        return f'<LogMessage {self.timestamp}, Level: {self.level}, Message: {self.message}>'
