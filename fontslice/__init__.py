import sys
from .main import get_120_unicode_ranges, _main, main

__all__ = ["get_120_unicode_ranges", "_main", "main"]


if __name__ == "__main__":
    sys.exit(main())
