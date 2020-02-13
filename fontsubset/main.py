import os
from pathlib import Path
from argparse import ArgumentParser
from fontTools.subset import Subsetter, Options, parse_unicodes, load_font, save_font

FONT_DIR = "font-subsets"

FONT_FACE_TEMPLATE = """
@font-face {
  font-family: '%s';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url("%s/%s-subset-%d.woff") format('woff');
  unicode-range: %s;
}
"""


def get_120_unicode_ranges():
    with open(os.path.join(os.path.dirname(__file__), 'unicode_ranges_120.txt')) as f:
        lines = f.readlines()
    return [str.strip(line) for line in lines]


def get_unicode_ranges_from_text(text):
    chars = list(text)
    char_num_list = [ord(char) for char in chars]
    char_num_list = list(set(char_num_list))
    char_num_list.sort()
    main_unicode_range = ','.join(['U+%x' % num for num in char_num_list])

    another_list = []
    cursor = 1
    for num in char_num_list:
        if num > cursor:
            another_list.append((cursor, num - 1))
        cursor = num + 1
    another_ranges = []
    for (f, t) in another_list:
        if f == t:
            another_ranges.append('U+%x' % f)
        else:
            another_ranges.append('U+%x-%x' % (f, t))
    another_unicode_range = ','.join(another_ranges)
    return [main_unicode_range, another_unicode_range]


def generate_subset(unicode_range, index, font_file, output_dir):
    """
    Generate font subset.
    You can do the same with the following command.
    $ pyftsubset YOUR_FONT.otf \
    --unicodes=U+943a-943b \
    --layout-features='*' \
    --flavor=woff \
    --name-IDs='*' \
    --output-file=style/font-subsets/YOUR_FONT-subset-1.woff
    """
    args = [
        "--layout-features='*'",
        "--flavor=woff"
    ]
    options = Options()
    options.parse_opts(args)
    subsetter = Subsetter(options)
    font = load_font(font_file, options)

    subsetter.populate(unicodes=parse_unicodes(unicode_range))
    subsetter.subset(font)

    font_path = Path(font_file)
    name = font_path.stem
    outfile = '%s/%s/%s-subset-%d.woff' % (output_dir, FONT_DIR, name, index)
    save_font(font, outfile, options)
    font.close()


def generate_font_css(unicode_ranges, name, output_dir):
    css_text = ''
    for i, unicode_range in enumerate(unicode_ranges):
        css_text += FONT_FACE_TEMPLATE % (name, FONT_DIR, name, i, unicode_range) + "\n"

    with open('./%s/%s.css' % (output_dir, name), 'w') as f:
        f.write(css_text)


def _main(font, output_dir, text, text_files):
    if text is None:
        text = ''
    if text_files is None:
        text_files = []
    for text_file in text_files:
        with open(text_file) as f:
            text += f.read()

    font_path = Path(font)
    if not font_path.exists():
        raise '%s is not found.' % font
    name = font_path.stem
    os.makedirs('%s/%s' % (output_dir, FONT_DIR), exist_ok=True)
    if text:
        unicode_ranges = get_unicode_ranges_from_text(text)
    else:
        unicode_ranges = get_120_unicode_ranges()
    for i, unicode_range in enumerate(unicode_ranges):
        generate_subset(unicode_range, i, font, output_dir)
    generate_font_css(unicode_ranges, name, output_dir)


def main():
    parser = ArgumentParser(
        description="""
pyftsubset -- OpenType font subsetter and optimizer

pyftsubset is an OpenType font subsetter and optimizer, based on fontTools.
It accepts any TT- or CFF-flavored OpenType (.otf or .ttf) or WOFF (.woff)
font file. The subsetted glyph set is based on the specified glyphs
or characters, and specified OpenType layout features.
    """)

    parser.add_argument(
        'font',
        metavar='<path>',
        help='The input font file.'
    )
    parser.add_argument(
        '-o', '--output-file',
        default='style',
        metavar='<path>',
        help="The output directory. If not specified, the subsetted fonts and stylesheet will be saved in ./style/ directory."
    )
    parser.add_argument(
        '--text',
        default='',
        metavar='<text>',
        help='Specify characters to include in the subset, as UTF-8 string.'
    )
    parser.add_argument(
        '--text-file',
        nargs='*',
        metavar='<path>',
        help='Like --text but reads from a file. Newline character are not added to the subset.'
    )

    args = parser.parse_args()
    _main(args.font, args.output_file, args.text, args.text_file)
