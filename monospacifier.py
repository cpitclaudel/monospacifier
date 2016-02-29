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
existing monospace font to extend its Unicode coverage."""

# Technical note: two cycles of (open, modify, save, close) cause a segfault.
# On the other hand, copying a font and reading, modifying, and overwriting
# the copy works.

from __future__ import division

import argparse
from collections import Counter
import math
import os
import re
import shutil

try:
    import fontforge
    import psMat
except ImportError:
    print("This program requires FontForge's python bindings:")
    print("  git clone https://github.com/fontforge/fontforge")
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
    METRICS = ["ascent", "descent", "hhea_ascent", "hhea_ascent_add",
               "hhea_descent", "hhea_descent_add", "hhea_linegap", "os2_capheight",
               "os2_strikeypos", "os2_strikeysize", "os2_subxoff", "os2_subxsize",
               "os2_subyoff", "os2_subysize", "os2_supxoff", "os2_supxsize", "os2_supyoff",
               "os2_supysize", "os2_typoascent", "os2_typoascent_add", "os2_typodescent",
               "os2_typodescent_add", "os2_typolinegap", "os2_width", "os2_winascent",
               "os2_winascent_add", "os2_windescent", "os2_windescent_add", "os2_xheight",
               "vhea_linegap"]

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

    def copy_metrics(self, reference):
        for metric in FontScaler.METRICS:
            if hasattr(reference, metric):
                setattr(self.font, metric, getattr(reference, metric))

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

def make_monospace(reference, fallback, gscaler, save_to, copy_metrics):
    fontname = "{}_monospacified_for_{}".format(cleanup_font_name(fallback.fontname), cleanup_font_name(reference.fontname))
    familyname = "{} monospacified for {}".format(cleanup_font_name(fallback.familyname), cleanup_font_name(reference.familyname))
    fullname = "{} monospacified for {}".format(cleanup_font_name(fallback.fullname), cleanup_font_name(reference.fullname))

    destination = os.path.join(save_to, fontname + ".ttf")
    shutil.copy(fallback.path, destination)
    fscaler = FontScaler(destination)
    fscaler.font.sfnt_names = [] # Get rid of 'Prefered Name' etc.
    fscaler.font.fontname = fontname
    fscaler.font.familyname = familyname
    fscaler.font.fullname = fullname

    fscaler.font.em = reference.em # Adjust em size (number of internal units per em)
    fscaler.scale_glyphs(gscaler)
    if copy_metrics:
        fscaler.copy_metrics(reference)
    fscaler.write(destination)

    return destination

def cleanup_font_name(name):
    return re.sub('(.monospacified.for.*|-.*)', '', name)

def merge_fonts(reference, fallback, save_to):
    fontname = "{}_extended_with_{}".format(cleanup_font_name(reference.fontname), cleanup_font_name(fallback.fontname))
    familyname = "{} extended with {}".format(cleanup_font_name(reference.familyname), cleanup_font_name(fallback.familyname))
    fullname = "{} extended with {}".format(cleanup_font_name(reference.fullname), cleanup_font_name(fallback.fullname))

    destination = os.path.join(save_to, fontname + ".ttf")
    shutil.copy(reference.path, destination)
    merged = fontforge.open(destination)
    merged.sfnt_names = []
    merged.fontname = fontname
    merged.familyname = familyname
    merged.fullname = fullname

    merged.mergeFonts(fallback.path)
    merged.generate(destination)

    return destination

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
                        help="Whether to create copies of the reference font, extended with monospacified glyphs of the inputs.")
    parser.add_argument('--copy-metrics', action='store_const', const=True, default=False,
                        help="Whether to apply the metrics of the reference font to the new font.")
    return parser.parse_args()

def process_fonts(ref_paths, fnt_paths, save_to, merge, copy_metrics):
    for ref in ref_paths:
        reference = fontforge.open(ref)
        ref_width = FontScaler.most_common_width(reference)
        print(">>> For reference font {}:".format(reference.familyname))
        for fnt in fnt_paths:
            fallback = fontforge.open(fnt)
            print(">>> - Monospacifying {}".format(fallback.familyname))
            gscaler = StretchingGlyphScaler(ref_width, FontScaler.average_width(fallback))
            path = make_monospace(reference, fallback, gscaler, save_to, copy_metrics)
            if merge:
                monospacified = fontforge.open(path)
                print(">>> - Merging with {}".format(monospacified.familyname))
                path = merge_fonts(reference, monospacified, save_to)
            yield (reference.familyname, fallback.familyname, path)

def main():
    args = parse_arguments()
    # del args.inputs[1:]
    # del args.references[1:]
    results = list(process_fonts(args.references, args.inputs, args.save_to, args.merge, args.copy_metrics))

    tabdata = {}
    for ref, fnt, ttf in results:
        tabdata.setdefault(u"**{}**".format(ref), []).append(u"[{}]({}?raw=true)".format(fnt, ttf))
    table = [(header, u", ".join(items)) for header, items in sorted(tabdata.items())]

    try:
        from tabulate import tabulate
        print(tabulate(table, headers=[u'Programming font', u'Monospacified fallback fonts'], tablefmt='pipe'))
    except ImportError:
        print("!!! tabulate package not available")

if __name__ == '__main__':
    main()

# Local Variables:
# python-shell-interpreter: "python2"
# End:
