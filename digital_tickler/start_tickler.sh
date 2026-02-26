#!/usr/bin/env bash
set -euo pipefail

# small delay so the GNOME session is fully up
sleep 2

gnome-terminal --title="Digital Tickler" -- bash -lc '
python3 /home/gerit/repos/digital-tickler/digital_tickler/digital_tickler.py
exec bash
'
