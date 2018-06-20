#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Find all glyphs covered by a given font.
Example use: ./allchars.py test.ttf`"""

import sys
import os

try:
    import fontforge
    import psMat
except ImportError:
    print("This program requires FontForge's python bindings:")
    print("  git clone https://github.com/fontforge/fontforge")
    print("  cd fontforge")
    print("  ./bootstrap")
    print("  ./configure")
    print("  make -j8")
    print("  sudo make install")
    raise

def supported_chars(path):
    ft = fontforge.open(path)
    try:
        for glyph in ft.glyphs():
            if glyph.unicode >= 0:
                yield unichr(glyph.unicode)
    finally:
        ft.close()

def charmap(chars, width=80):
    buf = []
    for char in chars:
        buf.append(char)
        if len(buf) == width:
            yield u"".join(buf)
            buf = []
    if len(buf) > 0:
        yield u"".join(buf)

def compare(f1, f2):
    gl1, gl2 = set(supported_chars(f1)), set(supported_chars(f2))
    only1, only2 = (sorted(gl1 - gl2), sorted(gl2 - gl1))
    # print("{} has {} glyphs".format(f1, len(gl1)))
    # print("{} has {} glyphs".format(f2, len(gl2)))
    print("\n# Only in {}:".format(f1))
    print("\n".join(charmap(only1)))
    print("\n# Only in {}:".format(f2))
    print("\n".join(charmap(only2)))

def main():
    if len(sys.argv) == 2:
        print("\n".join(charmap(supported_chars(sys.argv[1]))))
    elif len(sys.argv) == 3:
        compare(sys.argv[1], sys.argv[2])
    else:
        print("Needs 1-2 arguments (paths to font files)")

if __name__ == '__main__':
    main()

# Local Variables:
# python-shell-interpreter: "python2"
# End:
