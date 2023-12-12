# MSE Cron Tab system

This system was built to keep track of all MSE processes. For this we made a replacement for Crontab that will spend API requests to a database. This is a daemon and will run indefinitely, but inorder to setup, you will have to make a system file on the linux server where the msecrontab backend server is running.

```bash msecrontab.service
[Unit]
Description=MSE Crontab Service
After=network.target

[Service]
ExecStart=/path/to/python3 /path/to/daemon_runner.py start
Restart=always

[Install]
WantedBy=multi-user.target
```

## How does it work?

This works like linux's default crontab except using a Queue and cron job tracking. It makes POST, UPDATE, and GET requests to a backend API and displays the processing linux jobs on the screen. 

## Commands:
- msecrontab -e (Opens up the crontab file)
- msecrontab -r (Resets the crontab file)


## Format of a cron
<minute> <hour> <day-of-month> <month> <day-of-week> "<job-name>" <command>

### Example:
* * * * * "This is MAS job" curl https://google.com
