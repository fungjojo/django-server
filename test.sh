#!/bin/sh

touch cert-test1.json
echo "this is a new text" >> cert-test1.json

FILE=./cert-test1.json
if [ -f "$FILE" ]; then
    echo "$FILE exists."
else 
    echo "$FILE does not exist."
fi