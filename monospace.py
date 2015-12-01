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

def average_width(font):
    return (int)(1 + sum(g.width for g in font.glyphs()) / sum(1 for _ in font.glyphs()))

def most_common_width(font):
    width, _ = Counter(g.width for g in font.glyphs()).most_common(1)[0]
    return width

def set_width(glyph, avg_width, target_width, allow_wide_chars):
    if allow_wide_chars:
        new_width_in_cells = int(math.ceil(0.75 * float(glyph.width) / avg_width))
        new_width = new_width_in_cells * target_width
        if new_width_in_cells > 1:
            print("{} is {} cells wide ({} -> {})".format(glyph.glyphname, new_width_in_cells, target_width, glyph.width))
    else:
        new_width = target_width
    delta = new_width - glyph.width
    glyph.left_side_bearing += delta / 2
    glyph.right_side_bearing += delta - glyph.left_side_bearing
    glyph.width = new_width

def set_widths(font, target_width, allow_wide_chars = True):
    """
    Adjust width of glyphs in FONT to match TARGET_WIDTH.
    If ALLOW_WIDE_CHARS, let wide characters occupy more than one cell.
    """
    print("Setting width to {}".format(target_width))

    counter = Counter()
    avg_width = average_width(font)
    for idx, glyph in enumerate(font.glyphs()):
        if idx % 1000 == 0:
            print(idx)
        set_width(glyph, avg_width, target_width, allow_wide_chars)
        counter[glyph.width] += 1

    print(sorted(counter.items()))

def load_font(path):
    return fontforge.open(path) # Prints a few warnings

def rename(font, oldname, newname):
    font.fontname = newname
    font.fullname = newname
    font.familyname = newname
    font.sfnt_names = [(lng, key, (val if newname in val
                                   else val.replace(oldname, newname)))
                       for (lng, key, val) in font.sfnt_names]
    # print("\n".join("{}: {}".format(attr, getattr(font,attr)) for attr in dir(font)))

def main():
    font = load_font("symbola.ttf")
    reference = load_font("consolas.ttf")

    set_widths(font, most_common_width(reference), False)
    rename(font, "Symbola", "SymbolaMonospace")

    font.generate("symbola-monospace.ttf")
    print("Done")

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
