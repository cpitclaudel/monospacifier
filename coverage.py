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

"""Find if a glyph is covered by a given font.
Example use: ./coverage.py --glyphs ω --fonts `find ~/.fonts -name '*.*tf'`"""

import argparse
from itertools import izip, repeat
import multiprocessing
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

def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--glyphs', required="True", nargs='+',
                        help="Glyphs to look for.")
    parser.add_argument('--fonts', required="True", nargs='+',
                        help="Fonts to check.")
    return parser.parse_args()

class FontInfo(object):
    def __init__(self, path, glyphs):
        """Check for unicode GLYPHS in font at PATH"""
        font = fontforge.open(os.path.abspath(path))
        self.path = path
        self.glyphs = glyphs
        self.fontname = font.fontname
        supported = set(glyph for glyph in glyphs if ord(glyph) in font)
        self.supported =   [glyph for glyph in glyphs if glyph in supported]
        self.unsupported = [glyph for glyph in glyphs if glyph not in supported]
        font.close()

    @property
    def score(self):
        return u"[✓]" if self.full_coverage else u"[{:d}/{:d}]".format(len(self.supported), len(self.glyphs))

    @property
    def full_coverage(self):
        return len(self.supported) == len(self.glyphs)

    @property
    def unsupported_s(self):
        return (u" [ " + u"  ".join(self.unsupported) + " ]") if self.unsupported else ""

def collect_font_info(glyphs, fnt):
    try:
        return FontInfo(fnt, glyphs)
    except EnvironmentError:
        return None

def imap_helper(glyphs_fnt):
    try:
        return collect_font_info(*glyphs_fnt)
    except Exception as e:
        print("ERROR:", e)
        return None

def collect_fonts_info(glyphs, fonts):
    pool = multiprocessing.Pool()
    for idx, info in enumerate(pool.imap_unordered(imap_helper, izip(repeat(glyphs), fonts))):
        print(">>> {} <<<".format(idx))
        if info:
            yield info

def main():
    args = parse_arguments()
    args.glyphs = [g.decode("utf-8") for g in args.glyphs]

    infos = list(collect_fonts_info(args.glyphs, args.fonts))
    infos.sort(key=lambda info: len(info.supported))

    for info in infos:
        print(u":: {}{} ({}) {}".format(info.score, info.unsupported_s, info.fontname, info.path))

if __name__ == '__main__':
    main()

# Local Variables:
# python-shell-interpreter: "python2"
# End:
