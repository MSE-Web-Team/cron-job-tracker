from flask import Blueprint, jsonify, request
from models import db, Job, LogMessage
from datetime import datetime

job_routes = Blueprint('job_routes', __name__)
log_message_routes = Blueprint('log_message_routes', __name__)

@job_routes.route('/api/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
    job_list = [{'id': job.id, 'process_name': job.process_name, 'description': job.description,
                 'ongoing': job.ongoing, 'start_time': job.start_time.isoformat(),
                 'end_time': job.end_time.isoformat() if job.end_time else None,
                 'status': job.status} for job in jobs]
    return jsonify({'jobs': job_list})

@job_routes.route('/api/jobs', methods=['POST'])
def create_job():
    data = request.json
    new_job = Job(
        process_name=data['process_name'],
        description=data['description'],
        ongoing=data.get('ongoing', True),
        start_time=data.get('start_time', datetime.utcnow()),
        end_time=data.get('end_time'),
        status=data.get('status', 'LOG')
    )

    db.session.add(new_job)
    db.session.commit()
    return jsonify({'message': 'Job created successfully!', 'job_id': new_job.id})

@job_routes.route('/update_job/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    job = Job.query.get_or_404(job_id)
    data = request.json

    # Update job status, end time, etc.
    job.status = data.get('status', job.status)
    job.end_time = data.get('end_time', job.end_time)
    # Update other fields as needed

    db.session.commit()

    return jsonify({'message': 'Job updated successfully'}), 200


# Define routes for LogMessage model
@log_message_routes.route('/api/log_messages', methods=['GET'])
def get_log_messages():
    log_messages = LogMessage.query.all()
    log_message_list = [{'id': log_message.id, 'process_name': log_message.process_name,
                         'timestamp': log_message.timestamp.isoformat(), 'message': log_message.message,
                         'level': log_message.level} for log_message in log_messages]
    return jsonify({'log_messages': log_message_list})

@log_message_routes.route('/api/log_messages', methods=['POST'])
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
