#!/bin/bash
kill $(ps aux | awk '!/awk/ && /flask/ { print $2 }')
kill $(netstat -tulpn | awk '/:5000/ {print $7}' | cut -d / -f 1)
