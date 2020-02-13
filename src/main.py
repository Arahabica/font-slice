import os
import subprocess


FONT_DIR = "font-subsets"

CMD_TEMPLATE = """pyftsubset %s.otf \
--unicodes=%s \
--layout-features='*' \
--flavor=woff \
--name-IDs='*' \
--output-file=%s/%s/%s-subset-%d.woff
"""

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
    with open('./unicode_ranges_120.txt') as f:
        lines = f.readlines()
    return [str.strip(line) for line in lines]


def get_unicode_ranges_from_text(subset_file):
    with open(subset_file) as f:
        text = f.read()
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


def generate_subset(unicode_range, index, name, output_dir):
    cmd = CMD_TEMPLATE % (name, unicode_range, output_dir, FONT_DIR, name, index)
    subprocess.call(cmd.split())


def generate_font_css(unicode_ranges, name, output_dir):
    css_text = ''
    for i, unicode_range in enumerate(unicode_ranges):
        css_text += FONT_FACE_TEMPLATE % (name, FONT_DIR, name, i, unicode_range) + "\n"

    with open('./%s/%s.css' % (output_dir, name), 'w') as f:
        f.write(css_text)


def main(name, output_dir, text_file):
    os.makedirs('%s/%s' % (output_dir, FONT_DIR), exist_ok=True)
    # unicode_ranges = get_120_unicode_ranges()
    unicode_ranges = get_unicode_ranges_from_text(text_file)
    for i, unicode_range in enumerate(unicode_ranges):
        generate_subset(unicode_range, i, name, output_dir)
    generate_font_css(unicode_ranges, name, output_dir)


if __name__=='__main__':
    main(name="RiiT_F", output_dir="style", text_file='./subset.txt')
