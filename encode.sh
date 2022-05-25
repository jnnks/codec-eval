#!/bin/bash

for input_file in $(ls in); do
    filename="${input_file%.*}"

    for codec_lib in libvpx-vp9 libx265 libx264 libaom-av1; do
        ffmpeg -i in/$input_file -c:v $codec_lib -strict -2 -b:v 20K out/${filename}_${codec_lib}.mkv &
    done
    echo $filename
done


