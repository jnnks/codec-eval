from os import walk, stat
from os.path import splitext, join, exists
import subprocess

INPUT_DIR = "in"
OUTPUT_DIR = "out"
TEMP_DIR = "tmp"

ENCODERS = ["libvpx-vp9", "libx265", "libx264", "libaom-av1" ]

NORM_FPS = 4
NORM_RES = "256x144"

TARGET_BITRATE = 20

def run_ffmpeg(args):
    """run ffmpeg with default arguments"""
    subprocess.run(
        "ffmpeg -y -loglevel panic -hide_banner " + args,
        shell=True, check=True)

def get_kbits(file_path):
    """calculate kbits per seconds of a video file"""
    file_size = stat(file_path).st_size
    proc = subprocess.run(
        f'ffprobe -i {file_path} -show_entries format=duration -v quiet -of csv="p=0"',
        shell=True, capture_output=True, check=True)
    video_len = float(proc.stdout.decode('ascii')[:-1])
    return int((file_size / video_len) * 8)

# collect input files
[(root, _, files)] = list(walk(INPUT_DIR))
input_files = [(root, file) for file in files if file.endswith(".mp4")]
print(f"found {len(input_files)} files")


# main loop
for (root, file_name) in input_files:
    print()

    # decompress and resize input video to standardized format
    normalized_file = join(TEMP_DIR, f"{splitext(file_name)[0]}.y4m")
    if not exists(normalized_file):
        print(f"{file_name}: normalizing")
        run_ffmpeg(f"-i {join(root, file_name)} -r {str(NORM_FPS)} -s {NORM_RES} -pix_fmt yuv420p {normalized_file}")

    print(f"{file_name}: encoding")
    for encoder in ENCODERS:
        print(f"  {encoder}")

        # encoding loop
        #   keep adjusting ffmpeg bitrate until actual bitrage matches to 5% 
        current_bitrate = TARGET_BITRATE
        while True:
            out_file = f"{OUTPUT_DIR}/{splitext(file_name)[0]}_{encoder}.mkv"
            print(f"    {out_file} with {current_bitrate}kbps")

            run_ffmpeg(f"-i {normalized_file} -strict -2 -c:v {encoder} -b:v {str(current_bitrate)}K -maxrate {str(current_bitrate)}K -bufsize {str(current_bitrate)}K -an {out_file}")
            kbits = get_kbits(out_file) / 1000
            print(f"      got {str(kbits)}kbps")
            
            rel_diff = TARGET_BITRATE / kbits
            if abs(1 - rel_diff) <= 0.05:
                # actual bitrate within 5% of target bitrate
                break
            
            # adjust ffmpeg input bitrate
            current_bitrate = int(current_bitrate * rel_diff)
