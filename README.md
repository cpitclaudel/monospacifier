# monospacifier.py

*A great way to increase the Unicode coverage of your favorite programming font.*

`monospacifier.py` adjusts every character of your favorite variable-width font to match a reference monospace font. The result is a good fallback font for characters not covered by the reference: the result is a font setup with good Unicode coverage, without breaking indentation.

![default vs monospacified](demo/symbola-loop.gif)

## Pre-monospacified fonts (monospace fonts with good Unicode coverage)

Instead of running this program, you can use one of the *pre-generated* monospace fonts listed below (to be use *as a fallback*, for symbols not covered by your favorite font).

### Download a fallback font

Choose from this list, based on your main programming font.  Note that some fonts needed to be renamed to comply with their licenses (Asana → Asanb, STIX → STIY).

| Programming font                  | Monospacified fallback fonts                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|:----------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **DejaVu Sans Mono**              | [Asana Math](./fonts/Asanb_monospacified_for_DejaVuSansMono.ttf?raw=true), [FreeSerif](./fonts/FreeSerif_monospacified_for_DejaVuSansMono.ttf?raw=true), [Latin Modern Math](./fonts/LatinModernMath_monospacified_for_DejaVuSansMono.ttf?raw=true), [STIX Math](./fonts/STIYMath_monospacified_for_DejaVuSansMono.ttf?raw=true), [Symbola](./fonts/Symbola_monospacified_for_DejaVuSansMono.ttf?raw=true), [TeX Gyre Schola Math](./fonts/TeXGyreScholaMath_monospacified_for_DejaVuSansMono.ttf?raw=true), [XITS Math](./fonts/XITSMath-Bold_monospacified_for_DejaVuSansMono.ttf?raw=true), [XITS Math](./fonts/XITSMath_monospacified_for_DejaVuSansMono.ttf?raw=true)                                                                                                 |
| **Inconsolata LGC for Powerline** | [Asana Math](./fonts/Asanb_monospacified_for_InconsolataLGCForPowerline.ttf?raw=true), [FreeSerif](./fonts/FreeSerif_monospacified_for_InconsolataLGCForPowerline.ttf?raw=true), [Latin Modern Math](./fonts/LatinModernMath_monospacified_for_InconsolataLGCForPowerline.ttf?raw=true), [STIX Math](./fonts/STIYMath_monospacified_for_InconsolataLGCForPowerline.ttf?raw=true), [Symbola](./fonts/Symbola_monospacified_for_InconsolataLGCForPowerline.ttf?raw=true), [TeX Gyre Schola Math](./fonts/TeXGyreScholaMath_monospacified_for_InconsolataLGCForPowerline.ttf?raw=true), [XITS Math](./fonts/XITSMath-Bold_monospacified_for_InconsolataLGCForPowerline.ttf?raw=true), [XITS Math](./fonts/XITSMath_monospacified_for_InconsolataLGCForPowerline.ttf?raw=true) |
| **Inconsolata**                   | [Asana Math](./fonts/Asanb_monospacified_for_Inconsolata.ttf?raw=true), [FreeSerif](./fonts/FreeSerif_monospacified_for_Inconsolata.ttf?raw=true), [Latin Modern Math](./fonts/LatinModernMath_monospacified_for_Inconsolata.ttf?raw=true), [STIX Math](./fonts/STIYMath_monospacified_for_Inconsolata.ttf?raw=true), [Symbola](./fonts/Symbola_monospacified_for_Inconsolata.ttf?raw=true), [TeX Gyre Schola Math](./fonts/TeXGyreScholaMath_monospacified_for_Inconsolata.ttf?raw=true), [XITS Math](./fonts/XITSMath-Bold_monospacified_for_Inconsolata.ttf?raw=true), [XITS Math](./fonts/XITSMath_monospacified_for_Inconsolata.ttf?raw=true)                                                                                                                         |
| **Liberation Mono**               | [Asana Math](./fonts/Asanb_monospacified_for_LiberationMono.ttf?raw=true), [FreeSerif](./fonts/FreeSerif_monospacified_for_LiberationMono.ttf?raw=true), [Latin Modern Math](./fonts/LatinModernMath_monospacified_for_LiberationMono.ttf?raw=true), [STIX Math](./fonts/STIYMath_monospacified_for_LiberationMono.ttf?raw=true), [Symbola](./fonts/Symbola_monospacified_for_LiberationMono.ttf?raw=true), [TeX Gyre Schola Math](./fonts/TeXGyreScholaMath_monospacified_for_LiberationMono.ttf?raw=true), [XITS Math](./fonts/XITSMath-Bold_monospacified_for_LiberationMono.ttf?raw=true), [XITS Math](./fonts/XITSMath_monospacified_for_LiberationMono.ttf?raw=true)                                                                                                 |
| **Terminus (TTF)**                | [Asana Math](./fonts/Asanb_monospacified_for_TerminusTTF.ttf?raw=true), [FreeSerif](./fonts/FreeSerif_monospacified_for_TerminusTTF.ttf?raw=true), [Latin Modern Math](./fonts/LatinModernMath_monospacified_for_TerminusTTF.ttf?raw=true), [STIX Math](./fonts/STIYMath_monospacified_for_TerminusTTF.ttf?raw=true), [Symbola](./fonts/Symbola_monospacified_for_TerminusTTF.ttf?raw=true), [TeX Gyre Schola Math](./fonts/TeXGyreScholaMath_monospacified_for_TerminusTTF.ttf?raw=true), [XITS Math](./fonts/XITSMath-Bold_monospacified_for_TerminusTTF.ttf?raw=true), [XITS Math](./fonts/XITSMath_monospacified_for_TerminusTTF.ttf?raw=true)                                                                                                                         |
| **Ubuntu Mono**                   | [Asana Math](./fonts/Asanb_monospacified_for_UbuntuMono.ttf?raw=true), [FreeSerif](./fonts/FreeSerif_monospacified_for_UbuntuMono.ttf?raw=true), [Latin Modern Math](./fonts/LatinModernMath_monospacified_for_UbuntuMono.ttf?raw=true), [STIX Math](./fonts/STIYMath_monospacified_for_UbuntuMono.ttf?raw=true), [Symbola](./fonts/Symbola_monospacified_for_UbuntuMono.ttf?raw=true), [TeX Gyre Schola Math](./fonts/TeXGyreScholaMath_monospacified_for_UbuntuMono.ttf?raw=true), [XITS Math](./fonts/XITSMath-Bold_monospacified_for_UbuntuMono.ttf?raw=true), [XITS Math](./fonts/XITSMath_monospacified_for_UbuntuMono.ttf?raw=true)                                                                                                                                 |
| **mononoki**                      | [Asana Math](./fonts/Asanb_monospacified_for_mononoki.ttf?raw=true), [FreeSerif](./fonts/FreeSerif_monospacified_for_mononoki.ttf?raw=true), [Latin Modern Math](./fonts/LatinModernMath_monospacified_for_mononoki.ttf?raw=true), [STIX Math](./fonts/STIYMath_monospacified_for_mononoki.ttf?raw=true), [Symbola](./fonts/Symbola_monospacified_for_mononoki.ttf?raw=true), [TeX Gyre Schola Math](./fonts/TeXGyreScholaMath_monospacified_for_mononoki.ttf?raw=true), [XITS Math](./fonts/XITSMath-Bold_monospacified_for_mononoki.ttf?raw=true), [XITS Math](./fonts/XITSMath_monospacified_for_mononoki.ttf?raw=true)                                                                                                                                                 |

If your favorite combination is not available, please let me know.

### Install it

* On Windows put the font in `C:\Windows\Font`.
* On Debian-inspired systems put the font in `~/.fonts` and run `fc-cache`.

### Configure fallback

#### Emacs

Add the following snippet to your `.emacs` (replacing font names as appropriate), then restart:

``` elisp
(dolist (ft (fontset-list))
  (set-fontset-font ft 'unicode (font-spec :name "<monospace font>"))
  (set-fontset-font ft 'unicode (font-spec :name "<variable-width font> monospacified for <monospace font>") nil 'append))
```

Here are two examples:

``` elisp
(dolist (ft (fontset-list))
  (set-fontset-font ft 'unicode (font-spec :name "Consolas"))
  (set-fontset-font ft 'unicode (font-spec :name "Symbola monospacified for Consolas") nil 'append))
```

```elisp
(dolist (ft (fontset-list))
  (set-fontset-font ft 'unicode (font-spec :name "DejaVu Sans Mono"))
  (set-fontset-font ft 'unicode (font-spec :name "Asanb Math monospacified for DejaVu Sans Mono") nil 'append))
```

#### urxvt

Fallback fonts can be used with `urxvt` using comma-separated values to the `-fn` switch:

```bash
urxvt -fn 'xft:Consolas,xft:Symbola monospacified for Consolas'
```

This can also be set in the `.Xresources` file: 

```
URxvt.font: xft:Consolas,xft:Symbola monospacified for Consolas
```

Source it by running `xrdb -merge .Xresources`. 

#### Other editors

Please submit recipes for other editors or operating systems!

## Demo

![inconsistent fallbacks](demo/original.png) ![consistent fallback](demo/symbola.png) ![monospacified fallback](demo/symbola-monospacified.png)

Monospace font + default fallbacks — Monospace font + original Symbola — Monospace font + Monospacified Symbola

## Usage

## Details

* For help, run `./monospacifier.py -h`
* For examples of use, see the Makefile (I use it to generate the files listed here)

`monospacifier.py` includes multiple scaling algorithms (only one is exposed on the CLI). They are all rather basic, so don't expect this program to create anything except a decent fallback font.

The most advanced algorithm (demoed) sets the bounding box of each glyph appropriately (to match the most common width in the monospace font), and slightly compresses wide characters to reduce bleeding (wide glyphs will overlap with neighboring characters), while preserving distinctions between long and short glyphs (so ↦ and ⟼ are still distinguishable). Then (conditional on the `--copy-metrics` flag), `monospacifier.py` adjusts the metrics of the newly created font to match those of the reference (this fixes a number of issues that I don't understand well, in particular with `hhea_descent` and `os2_typodescent` metrics; if you have a clue about this, please do get in touch by opening an issue).
