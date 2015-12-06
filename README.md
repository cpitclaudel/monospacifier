# monospacifier.py

A great way to increase the Unicode coverage of your favorite programming font.

![default vs monospacified](demo/symbola-loop.gif)

## Details

`monospacifier.py` adjusts every character of your favourite variable-pitch font to match the width of a reference monospace font. The result is an good fallback font to use for characters not covered by the reference font. The final combination (original monospace font + monospacified font as fallback) has good Unicode coverage, and does not break indentation.

`monospacifier.py` includes multiple scaling algorithms. They are all pretty basic; this approach won't work well for anything but a fallback font. The most advanced one (demoed) sets the bounding box of each glyph appropriately, and slightly compresses wide characters to not spill too much from that bounding box. This preserves ratios (so ↦ and ⟼ are still distinguishable), while ensuring that each character occupies one "screen cell". Of course, two consecutive wide symbols will overlap.

## Pre-monospacified fonts (monospace fonts with good Unicode coverage)

Instead of running this program, you can use one of the *pre-generated* monospace fonts listed below (to be use *as a fallback*, for symbols not covered by your favorite font).

### Download a fallback font

Choose from this list (Symbola is a great choice), based on your main programming font:

| Programming font     | Monospacified fallback fonts                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|:---------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Consolas**         | [Asana Math](./fonts/Asana_monospacified_for_Consolas.ttf), [FreeSerif](./fonts/FreeSerif_monospacified_for_Consolas.ttf), [Latin Modern Math](./fonts/LatinModernMath_monospacified_for_Consolas.ttf), [STIX Math](./fonts/STIXMath_monospacified_for_Consolas.ttf), [Symbola](./fonts/Symbola_monospacified_for_Consolas.ttf), [TeX Gyre Schola Math](./fonts/TeXGyreScholaMath_monospacified_for_Consolas.ttf), [XITS Math](./fonts/XITSMath_monospacified_for_Consolas.ttf)                                                                   |
| **DejaVu Sans Mono** | [Asana Math](./fonts/Asana_monospacified_for_DejaVuSansMono.ttf),  [FreeSerif](./fonts/FreeSerif_monospacified_for_DejaVuSansMono.ttf), [Latin Modern Math](./fonts/LatinModernMath_monospacified_for_DejaVuSansMono.ttf), [STIX Math](./fonts/STIXMath_monospacified_for_DejaVuSansMono.ttf), [Symbola](./fonts/Symbola_monospacified_for_DejaVuSansMono.ttf), [TeX Gyre Schola Math](./fonts/TeXGyreScholaMath_monospacified_for_DejaVuSansMono.ttf), [XITS Math](./fonts/XITSMath_monospacified_for_DejaVuSansMono.ttf) |

If your favorite combination is not available, please let me know.

### Install it

* On Windows put the font in `C:\Windows\Font`.
* On Debian-inspired systems put the font in `~/.fonts` and run `fc-cache`.

### Configure fallback

#### Emacs

Add the following snippet to your `.emacs` (replacing font names as appropriate), then restart:

``` elisp
(set-fontset-font t 'unicode (font-spec :name "<variable-width font> monospacified for <monospace font>") nil 'append)
```

Here are two examples:

``` elisp
(set-fontset-font t 'unicode (font-spec :name "Symbola monospacified for Consolas") nil 'append)
(set-fontset-font t 'unicode (font-spec :name "Asana Math monospacified for DejaVu Sans Mono") nil 'append)
```

#### Other editors

Please submit recipes for other editors or operating systems!

## Demo

![inconsistent fallbacks](demo/original.png) ![consistent fallback](demo/symbola.png) ![monospacified fallback](demo/symbola-monospacified.png)

Monospace font + default fallbacks — Monospace font + original Symbola — Monospace font + Monospacified Symbola
