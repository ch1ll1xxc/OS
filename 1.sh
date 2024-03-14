#!/bin/bash

file="$1"
c_date=`(date +"%Y-%m-%d")`
c_time=`(date +"%H:%M:%S")`
uptime=`(uptime)`
users=`(grep -v "^#" /etc/passwd | cut -d: -f1)`

echo "Date: $c_date"
echo "Time: $c_time"
echo -e "\nUptime:\n$uptime"
echo -e "\nUsers:\n$users"

echo "Date: $c_date">"$file"
echo "Time: $c_time">>"$file"
echo -e "\nUptime:\n$uptime">>"$file"
echo -e "\nUsers:\n$users">>"$file"
