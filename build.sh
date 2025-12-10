#!/bin/bash
set -e
for FILE in *.ipynb; do
    echo "Processing $FILE file...";
    filename=$(basename -- "$FILE")
    extension="${filename##*.}"
    filename="${filename%.*}"
    jupyter nbconvert --clear-output --inplace "$FILE"
    jupyter nbconvert --execute --to notebook --inplace "$FILE"
done
