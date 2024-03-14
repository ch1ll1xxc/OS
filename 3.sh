#!/bin/bash

file="$1"

if [-f "$file"]; then
    while IFS=read -r line; do
        echo "$line"
    done < "$line"
else
    echo "file is not exist"
fi