#!/usr/bin/env python3

import sys
import requests
from datetime import datetime

"""
    This will be used for the cron jobs, so that you can create and update at will. You can make this a linux command by:
    
    chmod +x job.py
    # This will make it executable from anywhere
    sudo cp ./job.py /usr/bin
    
"""

def create_job(process_name, api_url):
    data = {
        "process_name": process_name,
        "description": "Created on Education Server",
        "status": "RUNNING"
    }

    response = requests.post(api_url, json=data, verify=False)

    if response.status_code == 200:
        job_id = response.json().get('job_id')
        print(f"Job created successfully with ID: {job_id}")
        return job_id
    else:
        print(f"Failed to create job. Response: {response.text}")
        return None

def update_job_to_success(process_name, api_url):
    job_id = get_most_recent_job_id(process_name, api_url)

    if not job_id:
        print(f"No job found for process name: {process_name}")
        return

    update_url = f"{api_url}/{job_id}"
    response = requests.put(update_url, json={"status": "SUCCESS"}, verify=False)

    if response.status_code == 200:
        print(f"Job with ID {job_id} updated to SUCCESS")
    else:
        print(f"Failed to update job. Response: {response.text}")

def get_most_recent_job_id(process_name, api_url):
    response = requests.get(api_url, verify=False)
    jobs = response.json().get('jobs', [])

    # Filter jobs by process name and find the most recent one
    matching_jobs = [job for job in jobs if job['process_name'] == process_name]
    most_recent_job = max(matching_jobs, key=lambda x: datetime.strptime(x['start_time'], "%Y-%m-%dT%H:%M:%S.%f"))

    return most_recent_job['id'] if most_recent_job else None

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: job.py <process_name> <create/update>")
        sys.exit(1)

    process_name = sys.argv[1]
    operation = sys.argv[2].lower()
    api_url = "https://msedev7.byu.edu/api/jobs"  # Update with your actual API URL

    if operation == "create":
        create_job(process_name, api_url)
    elif operation == "update":
        update_job_to_success(process_name, api_url)
    else:
        print("Invalid operation. Specify 'create' or 'update'.")
        sys.exit(1)
