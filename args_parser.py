import numpy as np
import argparse


parser = argparse.ArgumentParser(description='Photo / video convert to ASCII')
parser.add_argument('type',
                    type=str,
                    choices=['photo', 'video'],
                    help='type of input media (photo or video)')

parser.add_argument('indir',
                    type=str,
                    help='input dir for media')

parser.add_argument('outdir',
                    type=str,
                    help='output dir for media')

parser.add_argument('-c',
                    '--compression',
                    type=float,
                    default=4.0,
                    help='compresses the image by the value specified (default: 4.0)')

parser.add_argument('-di',
                    '--dimming_intensity',
                    type=float,
                    choices=0.1 * np.arange(4.5 / 0.1, 255.0 / 0.1),
                    default=9.8,
                    help='adjusts the darkness of the image to the level specified (4.5 - 255.0, default: 9.8)')
