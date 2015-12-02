# monospacifier.py

A great way to increase the unicode coverage of your favourite programming font. Live demo: (using a variable-width fallback font *vs.* using the same fallback font after monospacification)

![default vs monospacified](demo/symbola-loop.gif)

## Pre-monospacified fonts (monospace font with good unicode coverage)

Instead of running this program, you can download a pre-generated fallback font. I use [Symbola](http://users.teilar.gr/~g1951d/), which is "free for any use". Unfortunately, since the widths of the monospace and fallback fonts must match, the results won't be perfect unless you use one of the monospace fonts below:

* [SymbolaMonospace](fonts/SymbolaMonospace-Consolas.ttf) for **Consolas** (width: 1126)

If your favorite monospace font is not in this list, please let me know.

### Usage

#### Emacs

Add the following snippet to your `.emacs`:

``` elisp
(set-fontset-font t 'unicode (font-spec :name "SymbolaMonospace") nil 'append)
```

#### Others

Please submit recipes for other editors or operating systems!

## Details

`monospacifier.py` adjusts every character of your favourite variable-pitch font to match the width of a reference monospace font. The result is an good fallback font to use for characters not covered by the reference font. The final combination (original monospace font + monospacified font as fallback) has good unicode coverage, and does not break indentation.

`monospacifier.py` includes multiple scaling algorithms. They are all pretty basic; this approach won't work well for anything but a fallback font. The most advanced one (demoed) sets the bounding box of each glyph appropriately, and slightly compresses wide characters to not spill too much from that bounding box. This preserves ratios (so ↦ and ⟼ are still distinguishable), while ensuring that each character occupies one "screen cell". Of course, two consecutive wide symbols will overlap.

## Examples

![inconsistent fallbacks](demo/original.png) ![consistent fallback](demo/symbola.png) ![monospacified fallback](demo/symbola-monospacified.png)

Monospace font + default fallbacks — Monospace font + Symbola — Monospace font + Monospacified Symbola
