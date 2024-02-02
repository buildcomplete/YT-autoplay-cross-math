#!/bin/bash

for file in /shared/new/*.jpg
do
    # replace space
    if [[ "$file" == *" "* ]]; then
        new_file=$(echo "$file" | tr ' ' '_')
        mv "$file" "$new_file"
        $file=$new_file
        
    fi
    #echo $file

    filename=$(basename -- "$file")
    extension="${filename##*.}"
    filename="${filename%.*}"
    octave go_bin.m $file /shared/results/$filename.txt 0
    mv $file /shared/processed/$filename.jpg
done
