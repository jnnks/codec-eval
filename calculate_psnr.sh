#!/bin/bash -e


for input_file in $(ls tmp); do
    filename="${input_file%.*}"

    for codec_lib in libvpx-vp9 libx265 libx264 libaom-av1; do
        ffmpeg -i out/${filename}_${codec_lib}.mkv -i tmp/$input_file -lavfi psnr=stats_file=logs/${filename}_${codec_lib}_psnr.log -f null -
    done
    ffmpeg -i out/${filename}_rav1e.ivf -i tmp/$input_file -lavfi psnr=stats_file=logs/${filename}_rav1e_psnr.log -f null -
    echo $filename
done

