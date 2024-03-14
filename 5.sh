#!/bin/bash

directory="$1"

if [ -d "$directory" ]; then
    d_u=`(du -sh "$directory")
    echo "disk usage of $directory is $d_u"
else
    echo "directory is not exist"
fi