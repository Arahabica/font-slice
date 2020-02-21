from fontslice import (
    _chunk_list,
    _get_unicode_range_hash,
    get_120_unicode_ranges,
    convert_unicode_range,
    generate_css,
    get_unicode_ranges_from_text,
)


def test_chunk_list():
    assert _chunk_list([1, 2, 3, 4, 5, 6, 7, 8, 9], 3) == [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    assert _chunk_list([1, 2, 3, 4, 5, 6, 7, 8], 3) == [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8],
    ]
    assert _chunk_list([], 3) == []


def test_get_unicode_range_hash():
    assert _get_unicode_range_hash("U+768c-768e") == "17295b9f59962c7a845e0381a181aa15"


def test_get_120_unicode_ranges():
    ranges = get_120_unicode_ranges()
    assert len(ranges) == 120
    assert ranges[0][:7] == "U+25e56"


def test_convert_unicode_range():
    assert convert_unicode_range([]) == ""
    assert convert_unicode_range([(0, 255)]) == "U+0-ff"
    assert convert_unicode_range([(0, 255), (500, 600)]) == "U+0-ff,U+1f4-258"
    assert (
        convert_unicode_range([(0, 240), (255, 255), (300, 400)])
        == "U+0-f0,U+ff,U+12c-190"
    )


def test_generate_css():
    assert generate_css("@font-face", {"a": "x", "b": "y"}) == "@font-face {a: x;b: y;}"


def test_get_unicode_ranges_from_text():
    assert get_unicode_ranges_from_text("あいうえお") == [
        "U+3042,U+3044,U+3046,U+3048,U+304a",
        "U+1-3041",
        "U+3043",
        "U+3045",
        "U+3047",
        "U+3049",
        "U+304b-3ffff",
    ]
    assert get_unicode_ranges_from_text("abcdefghijklmn") == [
        "U+61-6e",
        "U+1-60",
        "U+6f-3ffff",
    ]
