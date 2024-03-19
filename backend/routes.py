from flask import Blueprint, jsonify, request
from models import db, Job, LogMessage
from datetime import datetime, timedelta
from pytz import timezone

job_routes = Blueprint('job_routes', __name__)
log_message_routes = Blueprint('log_message_routes', __name__)
utah = timezone('US/Mountain')

# TODO: Make this run on a schedule
@job_routes.route('/api/update_running_jobs', methods=['GET'])
def update_running_jobs():
    """
    Update the status of running jobs that have been running for more than 24 hours.

    Request Type: GET

    Parameters: None

    Response:
    {
      "message": "Running jobs updated"
    }
    """
    try:
        running_jobs = Job.query.filter_by(status='RUNNING').all()
        current_time = datetime.now()

        for job in running_jobs:
            start_time = job.start_time

            if start_time is not None:
                time_difference = current_time - start_time

                if time_difference > timedelta(hours=24):
                    job.description = 'This job was running for 24 hours and hasn\'t been updated.'
                    job.status = 'ERROR'
                    db.session.commit()

        return jsonify({'message': 'Running jobs updated'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.close()

@job_routes.route('/api/clear_jobs', methods=['POST'])
def remove_jobs():
    """
    Clear all jobs from the database.

    Request Type: POST

    Parameters: None

    Response:
    {
      "message": "Jobs successfully cleared"
    }
    """
    try:
        jobs = Job.query.all()

        for job in jobs:
            db.session.delete(job)

        db.session.commit()

        return jsonify({'message': 'Jobs successfully cleared'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.close()

@job_routes.route('/api/jobs', methods=['GET'])
def get_jobs():
    """
    Get a list of all jobs.

    Request Type: GET

    Parameters: None

    Response:
    {
      "jobs": [
        {
          "id": 1,
          "process_name": "example_process",
          "description": "Example job",
          "ongoing": true,
          "start_time": "2023-01-01T12:00:00",
          "end_time": "2023-01-02T12:00:00",
          "status": "SUCCESS"
        },
        // ... additional job objects
      ]
    }
    """
    try:
        unique = request.args.get('unique')
        unique = unique is not None and (unique == '1' or unique.lower() == 'true')

        age = request.args.get('age')
        age = int(age) if age is not None and age.isdigit() else None


        if unique:
            jobs = db.session.execute(db.select())
        else:
            jobs = Job.query.all()

        job_list = [{'id': job.id, 'process_name': job.process_name, 'description': job.description,
                     'ongoing': job.ongoing, 'start_time': job.start_time.isoformat(),
                     'end_time': job.end_time.isoformat() if job.end_time else None,
                     'status': job.status} for job in jobs]

        return jsonify({'jobs': job_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@job_routes.route('/api/jobs', methods=['POST'])
def create_job():
    """
    Create a new job.

    Request Type: POST

    Parameters:
    - `process_name` (string, required): The name of the process.
    - `description` (string, required): A description of the job.
    - `ongoing` (boolean, optional): Whether the job is ongoing. Defaults to `True`.
    - `start_time` (string, optional): The start time of the job in ISO format. Defaults to the current time.
    - `end_time` (string, optional): The end time of the job in ISO format.
    - `status` (string, optional): The status of the job. Defaults to "LOG".

    Response:
    {
      "message": "Job created successfully!",
      "job_id": 1
    }
    """
    try:
        data = request.json

        valid_statuses = {'EMERGENCY', 'SUCCESS', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'LOG', 'RUNNING'}
        if 'status' in data and data['status'] not in valid_statuses:
            return jsonify({'error': f"Invalid 'status' value. Allowed values: {', '.join(map(str, valid_statuses))}"}), 400

        new_job = Job(
            process_name=data['process_name'],
            description=data['description'],
            ongoing=data.get('ongoing', True),
            start_time=data.get('start_time', datetime.now()),
            end_time=data.get('end_time'),
            status=data.get('status', 'LOG')
        )

        db.session.add(new_job)
        db.session.commit()

        return jsonify({'message': 'Job created successfully!', 'job_id': new_job.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.close()

@job_routes.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    """
    Update an existing job.

    Request Type: PUT

    Parameters:
    - `status` (string, optional): The new status of the job.
    - `end_time` (string, optional): The new end time of the job in ISO format.

    Response:
    {
      "message": "Job updated successfully"
    }
    """
    try:
        job = Job.query.get_or_404(job_id)
        data = request.json

        valid_statuses = {'EMERGENCY', 'SUCCESS', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'LOG', 'RUNNING'}
        if 'status' in data and data['status'] not in valid_statuses:
            return jsonify({'error': f"Invalid 'status' value. Allowed values: {', '.join(map(str, valid_statuses))}"}), 400

        job.status = data.get('status', job.status)

        if 'end_time' in data:
            end_time_str = data.get('end_time', job.end_time)
            date_format = "%Y-%m-%d %H:%M:%S"

            try:
                end_time = datetime.strptime(end_time_str, date_format)
                job.end_time = end_time
            except ValueError:
                print("Error: Invalid end_time format. Please provide the time in the format: YYYY-MM-DD HH:MM:SS")
                return jsonify({'error': 'Invalid end_time format. Please provide the time in the format: YYYY-MM-DD HH:MM:SS'}), 400

        db.session.commit()

        return jsonify({'message': 'Job updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.close()

# Define routes for LogMessage model
@log_message_routes.route('/api/log_messages', methods=['GET'])
def get_log_messages():
    """
    Get a list of all log messages.

    Request Type: GET

    Parameters: None

    Response:
    {
      "log_messages": [
        {
          "id": 1,
          "process_name": "example_process",
          "timestamp": "2023-01-01T12:00:00",
          "message": "Example log message",
          "level": "INFO"
        },
        // ... additional log message objects
      ]
    }
    """
    try:
        log_messages = LogMessage.query.all()
        log_message_list = [{'id': log_message.id, 'process_name': log_message.process_name,
                             'timestamp': log_message.timestamp.isoformat(), 'message': log_message.message,
                             'level': log_message.level} for log_message in log_messages]

        return jsonify({'log_messages': log_message_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@log_message_routes.route('/api/log_messages', methods=['POST'])
def create_log_message():
    """
    Create a new log message.

    Request Type: POST

    Parameters:
    - `process_name` (string, required): The name of the process.
    - `timestamp` (string, optional): The timestamp of the log message in ISO format. Defaults to the current time.
    - `message` (string, required): The log message content.
    - `level` (string, optional): The level of the log message. Defaults to "INFO".

    Response:
    {
      "message": "Log message created successfully!",
      "log_message_id": 1
    }
    """
    try:
        data = request.json

        valid_levels = {'EMERGENCY', 'SUCCESS', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'LOG'}
        if 'level' in data and data['level'] not in valid_levels:
            return jsonify({'error': f"Invalid 'level' value. Allowed values: {', '.join(map(str, valid_levels))}"}), 400

        new_log_message = LogMessage(
            process_name=data['process_name'],
            timestamp=data.get('timestamp', datetime.now()),
            message=data['message'],
            level=data.get('level', 'INFO')
        )

        db.session.add(new_log_message)
        db.session.commit()

        return jsonify({'message': 'Log message created successfully!', 'log_message_id': new_log_message.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.close()

@log_message_routes.route('/api/clear_logs', methods=['POST'])
def remove_logs():
    """
    Clear all log messages from the database.

    Request Type: POST

    Parameters: None

    Response:
    {
      "message": "Logs successfully cleared"
    }
    """
    try:
        logs = LogMessage.query.all()

        for log in logs:
            db.session.delete(log)

        db.session.commit()

        return jsonify({'message': 'Logs successfully cleared'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.close()