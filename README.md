# monospacifier.py

A great way to increase the unicode coverage of your favourite programming font. Live demo:

![default vs monospacified](demo/symbola-loop.gif)

## Concept

`monospacifier.py` adjusts every character of your favourite variable-pitch font to match the width of a reference monospace font. The result is an good fallback font to use for characters not covered by the reference font. The final combination (original monospace font + monospacified font as fallback) has good unicode coverage, and does not break indentation.

## Examples

![inconsistent fallbacks](demo/original.png) ![consistent fallback](demo/symbola.png) ![monospacified fallback](demo/symbola-monospacified.png)

Monospace font + default fallbacks — Monospace font + Symbola — Monospace font + Monospacified Symbola
