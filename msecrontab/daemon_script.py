import schedule
import requests
import json
import subprocess
from datetime import datetime
import argparse
import time


# Define the MSE Cron Tab API endpoint
MSE_CRON_API_URL = "http://0.0.0.0/api/"
# Path to the cron file
CRON_FILE_PATH = "./msecrontab.txt"

def parse_cron_text():
    with open(CRON_FILE_PATH,'r') as file:
        ...


def job_scheduler():
    while True:
        ...

def edit_cron_tab():
    # Open the cron file in the default editor (replace "editor" with your preferred text editor)
    subprocess.run(["nano", CRON_FILE_PATH])

def reset_cron_tab():
    # clear the data in the info file
    with open(CRON_FILE_PATH,'w') as file:
        file.write("# Example MSE Cron Tab file\n")
        file.write("# Format: <minute> <hour> <day-of-month> <month> <day-of-week> \"<job-name>\" <command>\n")
        file.write("# 30 17 * * * 'MAS UPDATE SCRIPT' /path/to/script.sh\n")
        pass

def main():
    parser = argparse.ArgumentParser(description="MSE Cron Tab System")
    parser.add_argument("-e", action="store_true", help="Edit the cron tab")
    parser.add_argument("-r", action="store_true", help="Reset the cron tab")
    args = parser.parse_args()

    if args.e:
        edit_cron_tab()
    elif args.r:
        reset_cron_tab()
    else:
        job_scheduler()

if __name__ == "__main__":
    main()
