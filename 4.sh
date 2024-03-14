#!/bin/bash

for it in *; do
    if [-f "$it" ]; then
        echo "$it is file"
    elif [ -d "$it" ]; then
        echo "$it is directory"
    fi
done