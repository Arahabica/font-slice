import os
import math
import hashlib
from pathlib import Path
from argparse import ArgumentParser
from fontTools.subset import Subsetter, Options, parse_unicodes, load_font, save_font

FONT_DIR = "font-subsets"

FONT_FACE_TEMPLATE = """
@font-face {
  font-family: '%s';
  font-display: swap;
  src: url("%s.woff2") format('woff2'), url("%s.woff") format('woff');
  unicode-range: %s;
}
"""

ANOTHER_SLICE_COUNT = 10


def _chunk_list(li, num):
    return [li[i : i + num] for i in range(0, len(li), num)]


def _get_unicode_range_hash(unicode_range):
    return hashlib.sha256(unicode_range.encode()).hexdigest()[:32]


def get_120_unicode_ranges():
    with open(os.path.join(os.path.dirname(__file__), "unicode_ranges_120.txt")) as f:
        lines = f.readlines()
    return [str.strip(line) for line in lines]


def convert_unicode_range(char_num_ranges):
    ranges = []
    for (f, t) in char_num_ranges:
        if f == t:
            ranges.append("U+%x" % f)
        else:
            ranges.append("U+%x-%x" % (f, t))
    return ",".join(ranges)


def get_unicode_ranges_from_text(text):
    chars = list(text)
    char_num_list = [ord(char) for char in chars]
    char_num_list = list(set(char_num_list))
    char_num_list.sort()
    char_num_ranges = []
    cursor = char_num_list[0]
    for i, num in enumerate(char_num_list):
        if i > 0:
            if num > char_num_list[i - 1] + 1:
                char_num_ranges.append((cursor, char_num_list[i - 1]))
                cursor = num
    char_num_ranges.append((cursor, char_num_list[-1]))

    main_unicode_range = convert_unicode_range(char_num_ranges)

    another_ranges = []
    cursor = 1
    for num in char_num_list:
        if num > cursor:
            another_ranges.append((cursor, num - 1))
        cursor = num + 1
    another_ranges.append((cursor, 0x3ffff))

    chunk_size = math.floor(len(another_ranges) / ANOTHER_SLICE_COUNT)
    chunked_another_ranges = _chunk_list(another_ranges, chunk_size)

    unicode_ranges = [main_unicode_range]
    for chunk in chunked_another_ranges:
        unicode_ranges.append(convert_unicode_range(chunk))

    return unicode_ranges


def generate_subset(unicode_range, flavor, font_file, output_dir):
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
    args = ["--layout-features='*'", "--flavor=%s" % flavor]
    options = Options()
    options.parse_opts(args)
    subsetter = Subsetter(options)
    font = load_font(font_file, options)

    subsetter.populate(unicodes=parse_unicodes(unicode_range))
    subsetter.subset(font)

    font_path = Path(font_file)
    name = font_path.stem
    unicode_range_hash = _get_unicode_range_hash(unicode_range)
    outfile = "%s/%s/%s-subset-%s.%s" % (
        output_dir,
        FONT_DIR,
        name,
        unicode_range_hash,
        flavor,
    )
    save_font(font, outfile, options)
    font.close()


def generate_font_css(unicode_ranges, name, output_dir):
    css_text = ""
    for unicode_range in unicode_ranges:
        unicode_range_hash = _get_unicode_range_hash(unicode_range)
        base_path = "%s/%s-subset-%s" % (FONT_DIR, name, unicode_range_hash)
        css_text += (
            FONT_FACE_TEMPLATE % (name, base_path, base_path, unicode_range) + "\n"
        )

    with open("./%s/%s.css" % (output_dir, name), "w") as f:
        f.write(css_text)


def _main(font, output_dir, text, text_files):
    if text is None:
        text = ""
    if text_files is None:
        text_files = []
    for text_file in text_files:
        with open(text_file) as f:
            text += f.read()

    font_path = Path(font)
    if not font_path.exists():
        raise "%s is not found." % font
    name = font_path.stem
    os.makedirs("%s/%s" % (output_dir, FONT_DIR), exist_ok=True)
    if text:
        unicode_ranges = get_unicode_ranges_from_text(text)
    else:
        unicode_ranges = get_120_unicode_ranges()
    for i, unicode_range in enumerate(unicode_ranges):
        generate_subset(unicode_range, "woff", font, output_dir)
        generate_subset(unicode_range, "woff2", font, output_dir)
    generate_font_css(unicode_ranges, name, output_dir)


def main():
    parser = ArgumentParser(
        description="""
fontslice -- OpenType font subsetter and css generator

fontslice is an OpenType font subsetter and css generator, based on fontTools
    """
    )

    parser.add_argument("font", help="The input font file.")
    parser.add_argument(
        "-o",
        "--output-dir",
        default=".",
        metavar="<path>",
        help="The output directory. If not specified, the subsetted fonts and stylesheet will be saved in current directory.",
    )
    parser.add_argument(
        "--text",
        default="",
        metavar="<text>",
        help="Specify characters to include in the subset, as UTF-8 string.",
    )
    parser.add_argument(
        "--text-file",
        nargs="*",
        metavar="<path>",
        help="Like --text but reads from a file. Newline character are not added to the subset.",
    )

    args = parser.parse_args()
    _main(args.font, args.output_dir, args.text, args.text_file)
