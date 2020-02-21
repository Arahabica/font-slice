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

    fontslice /path/to/font.otf
    fontslice /path/to/font.otf --output-dir style
    fontslice /path/to/font.otf --text-file /path/to/text.txt
    fontslice /path/to/font.otf --text 'ABCD'
    fontslice /path/to/font.otf --weight bold

Test
------------

.. code:: sh

    pip install tox
    tox
