#!/usr/bin/env python2

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

"""
This program creates a monospace font from a variable-width font, using fontforge.
"""

# $ fc-list | grep -i symbola
# /usr/share/fonts/truetype/ttf-ancient-scripts/Symbola605.ttf: Symbola:style=Regular

try:
    import fontforge
except ImportError:
    print("This program requires FontForge's python bindings:")
    print("  hub checkout fontforge/fontforge")
    print("  cd fontforge")
    print("  ./bootstrap")
    print("  ./configure --enable-pyextension")
    print("  make -j8")
    print("  sudo make install")
    raise

import math
from collections import Counter

class GlyphScaler(object): # pylint: disable=too-few-public-methods
    def __init__(self, cell_width):
        self.cell_width = cell_width

    @staticmethod
    def set_width(glyph, width):
        delta = width - glyph.width
        glyph.left_side_bearing += delta / 2
        glyph.right_side_bearing += delta - glyph.left_side_bearing
        glyph.width = width

class BasicGlyphScaler(GlyphScaler): # pylint: disable=too-few-public-methods
    def __init__(self, cell_width):
        GlyphScaler.__init__(self, cell_width)

    def scale(self, glyph):
        GlyphScaler.set_width(glyph, self.cell_width)

class AllowWideCharsGlyphScaler(GlyphScaler): # pylint: disable=too-few-public-methods
    def __init__(self, cell_width, avg_width):
        """Construct a scaler that allocates multiple cells for wide glyphs."""
        GlyphScaler.__init__(self, cell_width)
        self.avg_width = avg_width

    def scale(self, glyph):
        new_width_in_cells = int(math.ceil(0.75 * float(glyph.width) / self.avg_width))
        if new_width_in_cells > 1:
            print("{} is {} cells wide ({} -> {})".format(glyph.glyphname, new_width_in_cells, self.cell_width, glyph.width))
        GlyphScaler.set_width(glyph, new_width_in_cells * self.cell_width)

class FontScaler(object):
    def __init__(self, path):
        self.font = fontforge.open(path) # Prints a few warnings

    @staticmethod
    def average_width(font):
        """
        Compute the average character width in FONT.
        Useful to compare a character to others in a font.
        """
        return int(1 + sum(g.width for g in font.glyphs()) / sum(1 for _ in font.glyphs()))

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
        print("> Setting width to {}".format(scaler.cell_width))

        counter = Counter()
        for glyph in self.font.glyphs():
            scaler.scale(glyph)
            counter[glyph.width] += 1

        print("> Final width distribution: {}".format(",".join(map(str, sorted(counter.items())))))

    @staticmethod
    def rename(font, newname):
        oldname = font.fontname
        font.fontname = newname
        font.fullname = newname
        font.familyname = newname
        font.sfnt_names = [(lng, key, (val if newname in val
                                       else val.replace(oldname, newname)))
                           for (lng, key, val) in font.sfnt_names]
        # print("\n".join("{}: {}".format(attr, getattr(font,attr)) for attr in dir(font)))

    def write(self, file_name):
        """
        Rename and save the font to FILE_NAME.
        """
        FontScaler.rename(self.font, self.font.fontname + "Monospace")
        self.font.generate(file_name)

def main():
    fscaler = FontScaler("symbola.ttf")
    reference = fontforge.open("consolas.ttf")

    gscaler = BasicGlyphScaler(FontScaler.most_common_width(reference))
    # gscaler = AllowWideCharsGlyphScaler(FontScaler.most_common_width(reference), FontScaler.average_width(fscaler.font))

    fscaler.scale_glyphs(gscaler)
    fscaler.write("symbola-monospace-2.ttf")

def plot_widths(glyphs):
    # Putting imports in this order prevents a circular import
    import matplotlib
    import matplotlib.cbook
    from matplotlib import pyplot

    widths = [glyph.width for glyph in glyphs]
    pyplot.hist(widths, bins=400)
    pyplot.show()

if __name__ == '__main__':
    main()

# Local Variables:
# python-shell-interpreter: "python2"
# End:
