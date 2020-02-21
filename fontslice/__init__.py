import sys
from .main import (
    _chunk_list,
    _get_unicode_range_hash,
    convert_unicode_range,
    get_120_unicode_ranges,
    get_unicode_ranges_from_text,
    generate_css,
    main,
)

__all__ = [
    "_chunk_list",
    "_get_unicode_range_hash",
    "convert_unicode_range",
    "get_120_unicode_ranges",
    "get_unicode_ranges_from_text",
    "generate_css",
    "main",
]


if __name__ == "__main__":
    sys.exit(main())
