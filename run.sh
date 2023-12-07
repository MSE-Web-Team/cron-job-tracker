#!/bin/sh

# Start SQLite in the background
sqlite3 mydatabase.db &

# Keep the container running
tail -f /dev/null
