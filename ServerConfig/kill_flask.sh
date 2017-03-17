#!/bin/bash
kill $(ps aux | awk '!/awk/ && /flask/ { print $2 }')
kill $(netstat -tulpn | grep ":5000" | cut -d / -f 1)
