# ASCII Converter

This program converts photos and videos to ASCII art.

## How to use

### Command line arguments

- `type`: Type of input media (photo or video).
- `indir`: Input directory for media (must be a file for photos).
- `outdir`: Output directory for media.
- `-c`, `--compression`: Compresses the image by the value specified (default: 4.0).
- `-di`, `--dimming_intensity`: Adjusts the darkness of the image to the level specified (4.5 - 255.0, default: 9.8).

### Examples

```
python ascii_converter.py photo input/photo.jpg output -c 3.0 -di 8.0
```

Converts `input/photo.jpg` to ASCII art, compressing the image by a factor of 3 and dimming the intensity to 8.0. Saves the output to `output/ascii_image.jpg`.

```
python ascii_converter.py video input/video.mp4 output -c 2.0 -di 8.0
```

Converts `input/video.mp4` to ASCII art, compressing the image by a factor of 2 and dimming the intensity to 8.0. Saves the output to `output/out_video.mp4`.
