font-slice
=================================

font-slice is a tool for splitting font. font-slice generate 120 font subsets and a css file.

Requirements
------------

-  Python >= 3.6

Installation
------------

.. code:: sh

    pip install font-slice

Usage
------------

.. code:: sh

    fontsubsetcss /path/to/font.otf
    fontsubsetcss /path/to/font.otf  --output-dir style
    fontsubsetcss /path/to/font.otf  --text-file /path/to/text.txt
    fontsubsetcss /path/to/font.otf  --text 'ABCD'

Test
------------

.. code:: sh

    pip install tox
    tox
