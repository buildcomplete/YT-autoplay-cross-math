#!/bin/bash
shopt -s nullglob  # Set nullglob to avoid expanding to non-existing files
for file in /shared/new/*.jpg /shared/new/*.png
do
    # replace space
    if [[ "$file" == *" "* ]]; then
        new_file=$(echo "$file" | tr ' ' '_')
        mv "$file" "$new_file"        
    fi
done

for file in /shared/new/*.jpg /shared/new/*.png
do
    filename=$(basename -- "$file")
    extension="${filename##*.}"
    filename="${filename%.*}"
    octave --quiet go_bin.m $file /shared/results/$filename.txt 0
    mv $file /shared/processed/$filename.jpg
done
shopt -u nullglob  # Unset nullglob
