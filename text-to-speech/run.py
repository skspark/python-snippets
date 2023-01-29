import os
from gtts import gTTS
import ffmpeg
import sys
from enum import Enum
import argparse


class Theme(Enum):
    JAMMIN = "jammin"


parser = argparse.ArgumentParser(prog='Text to Speech')
parser.add_argument('--input-file',
                    dest='input_file',
                    default='input.txt',
                    type=str,
                    nargs=1,
                    help='input text file location')
parser.add_argument('--lang',
                    dest='lang',
                    default='ko',
                    type=str,
                    nargs=1,
                    help='language')
parser.add_argument('--theme',
                    dest='theme',
                    default=Theme.JAMMIN,
                    choices=list(Theme),
                    nargs=1,
                    help='theme')
parser.add_argument('--output-dir',
                    dest='output_dir',
                    default='outputs',
                    type=str,
                    nargs=1,
                    help='output directory')

args = parser.parse_args()
input_file, lang, theme, output_dir = args.input_file, args.lang, args.theme, args.output_dir

if not os.path.isfile(input_file):
    print(f"input file {input_file} not found")
    parser.print_help()
    sys.exit(1)

# create output dir if not exist
os.makedirs(output_dir, exist_ok=True)
with open(input_file, 'r') as f:
    for line in f.readlines():
        print(f"creating output audio file for {line}")
        if theme == Theme.JAMMIN:
            escaped = line.replace(" ", "_").strip()
            out_filepath = f"{output_dir}/{escaped[:min(len(escaped), 20)]}.mp3"
            temp_out_filepath = f"{output_dir}/{escaped[:min(len(escaped), 20)]}_temp.mp3"
            gTTS(line, lang=lang).save(temp_out_filepath)
            (ffmpeg.input(temp_out_filepath)
                .filter('asetrate', 44100 * 0.9)
                .filter('atempo', 0.9).output(out_filepath).run())
            os.remove(temp_out_filepath)

print("all output voice file created")
