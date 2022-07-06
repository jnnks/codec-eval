#!/bin/bash -e


for input_file in $(ls tmp); do
    filename="${input_file%.*}"

    for codec_lib in libvpx-vp9 libx265 libx264 libaom-av1; do
        ffmpeg -i out/${filename}_${codec_lib}.mkv -i tmp/$input_file -lavfi psnr=stats_file=logs/${filename}_${codec_lib}_psnr.log -f null -
    done
    echo $filename
done

