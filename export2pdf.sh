#!/bin/bash
set -Eeuo pipefail

trap 'echo "Error while exporting PDFs at line $LINENO" >&2' ERR

cd _site
sudo chmod -R 777 . || true
for FILE in *.html; do 
    if [[ "$FILE" == *-bbs* ]]; then
        echo "Skipping $FILE"
        continue
    fi
    echo "Processing $PWD/$FILE file...";
    filename=$(basename -- "$FILE")
    extension="${filename##*.}"
    filename="${filename%.*}"

    # docker run -v $(pwd):/home/user astefanutti/decktape /home/user/$FILE $filename-$date.pdf
    # docker cp `docker ps -lq`:slides/$filename-$date.pdf .
    container_id=$(docker create -v "$(pwd):/home/user" ghcr.io/astefanutti/decktape /home/user/"$FILE" "$filename.pdf")
    docker start -a "$container_id"
    exit_code=$(docker inspect "$container_id" --format '{{.State.ExitCode}}')
    if [[ "$exit_code" -ne 0 ]]; then
        docker rm "$container_id" >/dev/null
        exit "$exit_code"
    fi
    docker cp "$container_id":slides/"$filename.pdf" .
    docker rm "$container_id" >/dev/null
done
