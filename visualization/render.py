"""Build a portrait animation of the exact p=10 worked slice and its offline ZIP."""

import argparse
from fractions import Fraction
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from PIL import Image, ImageDraw, ImageFont

SIZE = (704, 830)
PAPER, INK, SUBTLE = '#f4f7fa', '#182840', '#415a74'
POS, NEG, FAIL = '#cbece4', '#f7ddb7', '#ffdedb'
FONT = '/System/Library/Fonts/Supplemental/Arial{}.ttf'


def title(draw, text, xy, size, *, bold=False, color=INK, anchor=None):
    font = ImageFont.truetype(FONT.format(' Bold' if bold else ''), size)
    box = draw.textbbox(xy, text, font=font, anchor=anchor)
    assert box[0] >= 0 and box[1] >= 0 and box[2] < SIZE[0] and box[3] < SIZE[1], (text, box)
    draw.text(xy, text, font=font, fill=color, anchor=anchor)


def display(value):
    return str(value.numerator) if value.denominator == 1 else str(value.numerator) + '/' + str(value.denominator)


def frame(noise, highlight=None):
    image = Image.new('RGB', SIZE, PAPER)
    draw = ImageDraw.Draw(image)
    title(draw, 'Two signals, one covariance', (38, 32), 42, bold=True)
    title(draw, '10 observed variables and 6 factors', (40, 87), 29, color=SUBTLE)
    draw.rounded_rectangle((36, 142, 667, 544), radius=20, fill='white', outline='#ccd9e7', width=2)
    title(draw, 'B − A', (353, 165), 35, bold=True, anchor='mt')
    title(draw, 'Only the diagonal changes', (353, 209), 29, color=SUBTLE, anchor='mt')
    start_x, start_y, cell = 204, 245, 28
    for i in range(10):
        for j in range(10):
            x, y = start_x + j * cell, start_y + i * cell
            fill = '#edf3f9' if i != j else (POS if i < 6 else NEG)
            draw.rectangle((x, y, x + cell - 2, y + cell - 2), fill=fill)
            if i == j:
                if highlight == i:
                    draw.rectangle((x, y, x + cell - 2, y + cell - 2), outline='#003b60', width=3)
                title(draw, '+' if i < 6 else '−', (x + cell // 2 - 1, y + 4), 23,
                      bold=True, anchor='mt')
    title(draw, 'Each diagonal step is +1 or −1.', (40, 573), 33, bold=True)
    title(draw, f'Noise level s = {display(noise)}', (41, 620), 31, bold=True)
    for x, signal, detail, valid, fill in [
            (40, 'Signal A', f'All ten: {display(noise)}', True, POS),
            (366, 'Signal B', f'Six: {display(noise - 1)}   Four: {display(noise + 1)}', noise > 1, NEG)]:
        draw.rounded_rectangle((x, 674, x + 296, 797), radius=17, fill=fill if valid else FAIL)
        title(draw, signal, (x + 15, 691), 27, bold=True)
        title(draw, detail, (x + 15, 728), 25)
        title(draw, 'All variances positive' if valid else 'Fails positive noise',
              (x + 15, 765), 23, bold=True, color=INK if valid else '#8d2824')
    return image.quantize(colors=96, method=Image.Quantize.MEDIANCUT)


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=here)
    destination = parser.parse_args().output
    destination.mkdir(parents=True, exist_ok=True)
    slides = [(Fraction(2), None, 2100)]
    slides += [(Fraction(2), cell, 160) for cell in range(10)]
    slides += [(Fraction(1), None, 2000), (Fraction(1, 2), None, 2600), (Fraction(3, 2), None, 1200)]
    frames = [frame(step, marker) for step, marker, _ in slides]
    frames[0].save(destination / 'variance-tradeoff.gif', save_all=True, append_images=frames[1:],
                   duration=[duration for _, _, duration in slides], loop=0, optimize=True)
    entry = ZipInfo('index.html', (1980, 1, 1, 0, 0, 0))
    entry.external_attr = 0o100644 << 16
    with ZipFile(destination / 'variance-tradeoff-explorer.zip', 'w') as archive:
        archive.writestr(entry, (here / 'index.html').read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=9)


if __name__ == '__main__':
    main()
