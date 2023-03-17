from moviepy.editor import AudioFileClip, VideoFileClip
from PIL import Image, ImageDraw, ImageFont
from progress.bar import IncrementalBar
from args_parser import parser
from itertools import repeat
import multiprocessing
from time import time
import numpy as np
import argparse
import cv2
import os


def make_ascii_frame(image: np.ndarray, size: tuple, dimming_intensity: float) -> np.ndarray:
    font = ImageFont.truetype('lucidaconsole.ttf', 8)
    ascii_img = Image.new('RGB', (size[0] * 6, size[1] * 6), color='white')
    drawing = ImageDraw.Draw(ascii_img)

    ascii_symbols = 'Ñ@#W9876543210!abc;:+=-,._                               '
    for row, h in zip(range(size[1]), range(0, size[1] * 6, 6)):
        for col, w in zip(range(size[0]), range(0, size[0] * 6, 6)):
            r, g, b = image[row, col]
            brightness = 0.299 * r + 0.587 * g + 0.114 * b
            symbol = ascii_symbols[int(brightness / dimming_intensity)]
            drawing.text((w, h), symbol, font=font, fill='black')

    return np.asarray(ascii_img)


def make_ascii_photo(in_path: str, out_path: str, compression: int, dimming_intensity: float):
    print('Converting photo...')
    img = cv2.imread(in_path)
    height, width, _ = img.shape
    dsize = (int(width) // compression, int(height) // compression)
    resized_img = cv2.resize(img, dsize)
    ascii_img = make_ascii_frame(resized_img, dsize, dimming_intensity)
    cv2.imwrite(f'{out_path}/ascii_image.jpg', ascii_img)


def make_ascii_video(in_path: str, out_path: str, compression: int, dimming_intensity: float):
    print('Converting video...')
    cpu = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(cpu)

    video = cv2.VideoCapture(in_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    dsize = (int(width) // compression, int(height) // compression)

    frames = []
    without_audio = 'temp.avi'
    codec = cv2.VideoWriter_fourcc(*'DIVX')
    frames_bar = IncrementalBar('Frames', max=total_frames)
    temp = cv2.VideoWriter(without_audio, codec, fps, (dsize[0] * 6, dsize[1] * 6))
    for _ in range(total_frames):
        _, frame = video.read()
        resized = cv2.resize(frame, dsize)
        frames.append(resized)
        if len(frames) == cpu:
            ascii_frames = pool.starmap(make_ascii_frame, zip(frames, repeat(dsize), repeat(dimming_intensity)))
            for f in ascii_frames:
                temp.write(f)
            frames = []
        frames_bar.next()
    ascii_frames = pool.starmap(make_ascii_frame, zip(frames, repeat(dsize), repeat(dimming_intensity)))
    for f in ascii_frames:
        frames_bar.next()
        temp.write(f)
    temp.release()
    frames_bar.finish()

    print('Adding audio...')
    audio = AudioFileClip(in_path)
    out_video = VideoFileClip(without_audio)
    out_video.audio = audio
    out_video.write_videofile(f'{out_path}/out_video.mp4', codec='libx264', logger=None)
    audio.close()
    out_video.close()

    os.remove(without_audio)


def validation(args: argparse.Namespace):
    if args.type != 'video' and args.type != 'photo':
        print('Invalid type of media.')
        return 0
    else:
        if not os.path.exists(args.outdir):
            print('Invalid out path.')
            return 0
        else:
            if not (os.path.exists(args.indir) and os.path.isfile(args.indir)):
                print('Invalid in path.')
                return 0
            else:
                if args.compression < 4.5 or args.compression > 255.0:
                    print('Invalid compression.')
                    return 0
                else:
                    return 1


def main():
    args = parser.parse_args()
    
    if validation(args):
        if args.type == 'photo':
            make_ascii_photo(args.indir, args.outdir, args.compression, args.dimming_intensity)
        elif args.type == 'video':
            make_ascii_video(args.indir, args.outdir, args.compression, args.dimming_intensity)

        return 1
    else:
        return 0


if __name__ == "__main__":
    start = time()
    successful = main()
    if successful:
        print(f'Finished in {round(time() - start, 2)} s')
