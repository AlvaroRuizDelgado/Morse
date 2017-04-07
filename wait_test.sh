#!/bin/bash

stack_name="morse_stack"
test_string="po morse_stack pi pe pu CREATE_COMPLETE"

echo $(echo $test_string | awk '/'"$stack_name"'/ { print $6 }')
echo "CREATE_COMPLETE"

while [ $(echo $test_string | awk '/'"$stack_name"'/ { print $6 }') != "CREATE_COMPLETE" ]
do
    echo "nope"
    sleep 1
done
echo "Freee!"
