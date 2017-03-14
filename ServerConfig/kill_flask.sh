#!/bin/bash
kill $(ps aux | awk '!/awk/ && /flask/ { print $2 }')
