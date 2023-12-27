import imageio
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--in-dir', type=str, help='Input folder (where the png files are)')
    parser.add_argument('-o', '--out-name', type=str, help='Output file name (with .gif extension)')
    parser.add_argument('--fps', type=float, default=10, help='Output frame rate')
    args = parser.parse_args()
    print(args)
    return args

args = parse_args()

def png_to_gif(png_dir, output_file, fps):
    images = []
    png_files = sorted((os.path.join(png_dir, f) for f in os.listdir(png_dir) if f.endswith('.png')))
    for filename in png_files:
        images.append(imageio.imread(filename))
    imageio.mimsave(output_file, images, fps=fps)  # adjust duration as needed

# usage
png_to_gif(args.in_dir, args.out_name, args.fps)