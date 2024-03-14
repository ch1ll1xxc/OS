#!/bin/bash

directory="$1"
if [ -d "$directory" ]; then
	ls -l "$directory"
else
	echo "directory is not exist"
fi
