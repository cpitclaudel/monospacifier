#!/usr/bin/env bash
# convert -crop +1+26 -crop -1-37 +repage -trim "raw/$1" "$1"
convert -crop +1+26 -crop -1-100 +repage \
        -background black \
        -gravity North -splice 0x1 -trim -chop 0x1 +repage \
        -gravity South -splice 0x1 -trim -chop 0x1 +repage \
        -gravity West -splice 1x0 -trim -chop 1x0 +repage \
        -bordercolor white -border 10 +repage \
        -chop 10x0 +repage \
        "raw/$1" "$1"
