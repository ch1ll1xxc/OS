#!/bin/bash

directory="$1"
for file in "$directory"; do
    if [ -x "$file" ]; then 
        echo "$file"
    fi
done