#!/usr/bin/env bash
set -euo pipefail

# small delay so the GNOME session is fully up
sleep 2

ptyxis --title="Digital Tickler" -- bash -lc '
digital_tickler run
exec bash
'
