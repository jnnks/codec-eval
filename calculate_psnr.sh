
for input_file in $(ls in); do
    filename="${input_file%.*}"

    for codec_lib in libvpx-vp9 libx265 libx264 libaom-av1; do
        ffmpeg -i out/${filename}_${codec_lib}.mkv -i in/$input_file -lavfi psnr=logs/${filename}_${codec_lib}_psnr.log -f null -
    done
    echo $filename
done

