#!/bin/bash
touch /root/db/db.sqlite3
sqlite3 /root/db/db.sqlite3 ".databases"
