from flask import Blueprint, jsonify, request
from models import db, Job, LogMessage
from datetime import datetime, timedelta

job_routes = Blueprint('job_routes', __name__)
log_message_routes = Blueprint('log_message_routes', __name__)

# TODO: Make this run in a schedule:
@job_routes.route('/api/update_running_jobs', methods=['GET'])
def update_running_jobs():
    running_jobs = Job.query.filter_by(status='RUNNING').all()

    current_time = datetime.now()

    for job in running_jobs:
        start_time = job.start_time

        # Assuming start_time is a datetime field in your Job model
        if start_time is not None:
            time_difference = current_time - start_time

            # Check if the time difference is greater than 24 hours
            if time_difference > timedelta(hours=24):
                # Do something with the job, e.g., mark it as overdue
                job.description = 'This job was running for 24 hours and hasn\'t been updated.'
                job.status = 'ERROR'
                # You might want to commit the changes to the database
                db.session.commit()

    return jsonify({'message': 'Running jobs updated'})

@job_routes.route('/api/clear_jobs', methods=['POST'])
def remove_jobs():
    try:
        # Query all jobs
        jobs = Job.query.all()

        # Remove each job from the database
        for job in jobs:
            db.session.delete(job)

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': 'Jobs successfully cleared'}), 200

    except Exception as e:
        # Handle any exceptions that may occur during the process
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        # Close the database session
        db.session.close()


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

    # Ensure 'status' is a valid enum value
    valid_statuses = {'EMERGENCY', 'SUCCESS', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'LOG', 'RUNNING'}
    if 'status' in data and data['status'] not in valid_statuses:
        return jsonify({'error': f"Invalid 'status' value. Allowed values: {', '.join(map(str, valid_statuses))}"})


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

    # Ensure 'status' is a valid enum value
    valid_statuses = {'EMERGENCY', 'SUCCESS', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'LOG', 'RUNNING'}
    if 'status' in data and data['status'] not in valid_statuses:
        return jsonify({'error': f"Invalid 'status' value. Allowed values: {', '.join(map(str, valid_statuses))}"})



    # Update job status, end time, etc.
    job.status = data.get('status', job.status)

    # Update end time of the job if it is in there
    if 'end_time' in data:
        end_time_str = data.get('end_time', job.end_time)
        
        # Define the expected format of the end_time
        date_format = "%Y-%m-%d %H:%M:%S"
        
        try:
            # Try to parse the end_time string into a datetime object
            end_time = datetime.strptime(end_time_str, date_format)
            
            # If successful, update the job's end_time
            job.end_time = end_time
        except ValueError:
            # If parsing fails, handle the error (e.g., print a message or set a default value)
            print("Error: Invalid end_time format. Please provide the time in the format: YYYY-MM-DD HH:MM:SS")
            # Optionally, you can set a default value or raise an exception here

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

    # Ensure 'level' is a valid enum value
    valid_levels = {'EMERGENCY', 'SUCCESS', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'LOG'}
    if 'level' in data and data['level'] not in valid_levels:
        return jsonify({'error': f"Invalid 'level' value. Allowed values: {', '.join(map(str, valid_levels))}"})


    new_log_message = LogMessage(
        process_name=data['process_name'],
        timestamp=data.get('timestamp', datetime.utcnow()),
        message=data['message'],
        level=data.get('level', 'INFO')
    )

    db.session.add(new_log_message)
    db.session.commit()

    return jsonify({'message': 'Log message created successfully!', 'log_message_id': new_log_message.id})

@log_message_routes.route('/api/clear_logs', methods=['POST'])
def remove_logs():
    try:
        # Query all jobs
        logs = LogMessage.query.all()

        # Remove each job from the database
        for log in logs:
            db.session.delete(log)

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': 'Logs successfully cleared'}), 200

    except Exception as e:
        # Handle any exceptions that may occur during the process
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        # Close the database session
        db.session.close()