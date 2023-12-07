from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# SQLite database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    process_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    ongoing = db.Column(db.Boolean(), default=False)  # Defaulting to ongoing
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Enum('ERROR', 'SUCCESS', 'UNDEFINED', 'INFO'), default='SUCCESS')

    def __repr__(self):
        return f'<Job {self.id}, {self.process_name}, Status: {self.status}>'

class LogMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    process_name = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    message = db.Column(db.String(255), nullable=False)
    level = db.Column(db.Enum('ERROR', 'WARNING', 'INFO', 'DEBUG'), default='INFO')

    def __repr__(self):
        return f'<LogMessage {self.timestamp}, Level: {self.level}, Message: {self.message}>'

    

# Create the database tables before running the app
with app.app_context():
    db.create_all()
@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
    job_list = [{'id': job.id, 'process_name': job.process_name, 'description': job.description,
                 'ongoing': job.ongoing, 'start_time': job.start_time.isoformat(),
                 'end_time': job.end_time.isoformat() if job.end_time else None,
                 'status': job.status} for job in jobs]
    return jsonify({'jobs': job_list})

@app.route('/api/jobs', methods=['POST'])
def create_job():
    data = request.json
    new_job = Job(
        process_name=data['process_name'],
        description=data['description'],
        ongoing=data.get('ongoing', True),
        start_time=data.get('start_time', datetime.utcnow()),
        end_time=data.get('end_time'),
        status=data.get('status', 'SUCCESS')
    )
    db.session.add(new_job)
    db.session.commit()
    return jsonify({'message': 'Job created successfully!', 'job_id': new_job.id})


# Define routes for LogMessage model

@app.route('/api/log_messages', methods=['GET'])
def get_log_messages():
    log_messages = LogMessage.query.all()
    log_message_list = [{'id': log_message.id, 'process_name': log_message.process_name,
                         'timestamp': log_message.timestamp.isoformat(), 'message': log_message.message,
                         'level': log_message.level} for log_message in log_messages]
    return jsonify({'log_messages': log_message_list})

@app.route('/api/log_messages', methods=['POST'])
def create_log_message():
    data = request.json
    new_log_message = LogMessage(
        process_name=data['process_name'],
        timestamp=data.get('timestamp', datetime.utcnow()),
        message=data['message'],
        level=data.get('level', 'INFO')
    )
    db.session.add(new_log_message)
    db.session.commit()
    return jsonify({'message': 'Log message created successfully!', 'log_message_id': new_log_message.id})



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
