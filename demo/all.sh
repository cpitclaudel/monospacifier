#!/usr/bin/env bash
./truncate.sh original.png
./truncate.sh symbola.png
./truncate.sh symbola-monospacified.png
convert -delay 100 -loop 0 symbola.png symbola-monospacified.png symbola-loop.gif
