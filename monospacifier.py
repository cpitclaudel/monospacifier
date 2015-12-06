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

# $ fc-list | grep -i symbola
# /usr/share/fonts/truetype/ttf-ancient-scripts/Symbola605.ttf: Symbola:style=Regular

"""Convert a variable-width font to monospace, optionally merging it with an
existing monospace font to extend its unicode coverage."""

# Techincal note: two cycles of (open, modify, save, close) cause a segfault.
# On the other hand, copying a font and reading, modifying, and overwriting
# the copy works.

from __future__ import division

import argparse
import itertools
import math
import os
import shutil
import re
from collections import Counter

try:
    import fontforge
    import psMat
except ImportError:
    print("This program requires FontForge's python bindings:")
    print("  hub checkout fontforge/fontforge")
    print("  cd fontforge")
    print("  ./bootstrap")
    print("  ./configure --enable-pyextension")
    print("  make -j8")
    print("  sudo make install")
    raise

class GlyphScaler(object):
    def __init__(self, cell_width):
        self.cell_width = cell_width

    @staticmethod
    def set_width(glyph, width):
        delta = width - glyph.width
        glyph.left_side_bearing += delta / 2
        glyph.right_side_bearing += delta - glyph.left_side_bearing
        glyph.width = width

class BasicGlyphScaler(GlyphScaler):
    """
    A GlyphScaler that adjust glyph bounding boxes so that their widths are
    all equal to the base cell width.
    """

    def __init__(self, cell_width):
        GlyphScaler.__init__(self, cell_width)

    def scale(self, glyph):
        if glyph.width > 0:
            GlyphScaler.set_width(glyph, self.cell_width)

class AllowWideCharsGlyphScaler(GlyphScaler):
    """
    A GlyphScaler that adjusts glyph bounding boxes so that their widths are
    multiples of the base cell width. Which multiple is chosen depends on the
    width of each glyph, compared to the given average width.
    """

    def __init__(self, cell_width, avg_width):
        """Construct an instance based on the target CELL_WIDTH and the source AVG_WIDTH."""
        GlyphScaler.__init__(self, cell_width)
        self.avg_width = avg_width

    def scale(self, glyph):
        if glyph.width > 0:
            new_width_in_cells = int(math.ceil(0.75 * glyph.width / self.avg_width))
            # if new_width_in_cells > 1:
            #     print("{} is {} cells wide ({} -> {})".format(
            #         glyph.glyphname, new_width_in_cells, self.cell_width, glyph.width))
            GlyphScaler.set_width(glyph, new_width_in_cells * self.cell_width)

class StretchingGlyphScaler(GlyphScaler):
    """
    A GlyphScaler that adjusts glyph bounding boxes so that their widths are all
    equal to the base cell width. Unlike the basic scaler, this one also scales
    the glyphs themselves horizontally by a small amount, in proportion of their
    distance to the average glyph width.
    """

    def __init__(self, cell_width, avg_width):
        """Construct an instance based on the target CELL_WIDTH and the source AVG_WIDTH."""
        GlyphScaler.__init__(self, cell_width)
        self.avg_width = avg_width

    def scale(self, glyph):
        if glyph.width > 0:
            source_cells_width = glyph.width / self.avg_width
            scale = 1.0 / (1.15 ** max(0, source_cells_width - 1))
            # if glyph.unicode == 10239:
            #     print("\n\n====\n" + "\n".join("{}: {}".format(attr, str(getattr(glyph, attr))) for attr in dir(glyph)))
            matrix = psMat.scale(scale, 1)
            glyph.transform(matrix)
            GlyphScaler.set_width(glyph, self.cell_width)

class FontScaler(object):
    def __init__(self, path):
        self.font = fontforge.open(path) # Prints a few warnings
        self.renamed = False

    @staticmethod
    def average_width(font):
        """
        Compute the average character width in FONT.
        Useful to compare a character to others in a font.
        """
        return int(1 + sum(g.width for g in font.glyphs()) / sum(1 for _ in font.glyphs()))

    @staticmethod
    def median_width(font):
        """
        Compute the median character width in FONT.
        Useful to compare a character to others in a font.
        """
        widths = sorted(g.width for g in font.glyphs())
        return int(widths[len(widths) // 2])

    @staticmethod
    def most_common_width(font):
        """
        Find out the most common character width in FONT.
        Useful to determine the width of a monospace font.
        """
        [(width, _)] = Counter(g.width for g in font.glyphs()).most_common(1) # pylint: disable=unbalanced-tuple-unpacking
        return width

    def scale_glyphs(self, scaler):
        """
        Adjust width of glyphs in using SCALER.
        """
        # counter = Counter()
        for glyph in self.font.glyphs():
            scaler.scale(glyph)
            # counter[glyph.width] += 1
        # print("> Final width distribution: {}".format(", ".join(map(str, counter.most_common(10)))))

    def write(self, name):
        """
        Save font to NAME.
        """
        self.font.generate(name)

def plot_widths(glyphs):
    # pylint: disable=unused-variable
    import matplotlib # Putting imports in this order prevents a circular import
    import matplotlib.cbook
    from matplotlib import pyplot

    widths = [glyph.width for glyph in glyphs]
    pyplot.hist(widths, bins=400)
    pyplot.show()

def fname(path):
    return os.path.splitext(os.path.basename(path))[0]

def make_monospace(ref, fnt, save_to):
    reference = fontforge.open(ref)
    width = FontScaler.most_common_width(reference)

    output = os.path.join(save_to, "{}-monospacified-for-{}.ttf".format(fname(fnt), fname(ref)))
    print("> * [{}]({}) monospacified for **{}** (width: {})".format(fname(fnt), output, fname(ref), width))

    shutil.copy(fnt, output)
    fscaler = FontScaler(output)

    fscaler.font.fontname = "{}-monospacified-for-{}".format(fscaler.font.fontname, reference.fontname)
    fscaler.font.familyname = "{} monospacified for {}".format(fscaler.font.familyname, reference.familyname)
    fscaler.font.fullname = "{} monospacified for {}".format(fscaler.font.fullname, reference.fullname)
    # fscaler.font.sfnt_names = [(lng, key, (val if newname in val
    #                                else val.replace(oldname, newname)))
    #                    for (lng, key, val) in font.sfnt_names]
    # print("\n".join("{}: {}".format(attr, getattr(font,attr)) for attr in dir(font)))

    gscaler = StretchingGlyphScaler(width, FontScaler.average_width(fscaler.font))
    fscaler.scale_glyphs(gscaler)
    fscaler.write(output)
    return output

def cleanup_font_name(name):
    return re.sub('.monospacified.for.*', '', name)

def merge_fonts(ref, fnt, save_to):
    output = os.path.join(save_to, "{}-extended-with-{}.ttf".format(fname(ref), cleanup_font_name(fname(fnt))))
    # print("> * [{}]({}) extended with **{}**".format(fname(ref), output, cleanup_font_name(fname(fnt))))

    shutil.copy(ref, output)
    fallback = fontforge.open(fnt)
    reference = fontforge.open(output)
    reference.fontname = "{}-extended-with-{}".format(reference.fontname, cleanup_font_name(fallback.fontname))
    reference.familyname = "{} extended with {}".format(reference.familyname, cleanup_font_name(fallback.familyname))
    reference.fullname = "{} extended with {}".format(reference.fullname, cleanup_font_name(fallback.fullname))

    reference.mergeFonts(fnt)
    reference.generate(output)
    return output

def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--references', required="True", nargs='+',
                        help="Reference monospace fonts. " +
                        "The metrics (character width, ...) of the newly created monospace fonts are inherited from these.")
    parser.add_argument('--inputs', required="True", nargs='+',
                        help="Variable-width fonts to monospacify.")
    parser.add_argument('--save-to', default=".",
                        help="Where to save the newly generated monospace fonts. Defaults to current directory.")
    parser.add_argument('--merge', action='store_const', const=True, default=False,
                        help="Whether to create a copy of the reference, including monospacified glyphs from the inputs.")
    return parser.parse_args()

def main():
    args = parse_arguments()

    for ref, fnt in itertools.product(args.references, args.inputs):
        output = make_monospace(ref, fnt, args.save_to)
        if args.merge:
            merge_fonts(ref, output, args.save_to)

if __name__ == '__main__':
    main()

# Local Variables:
# python-shell-interpreter: "python2"
# End:
