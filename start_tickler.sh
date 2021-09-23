#!/bin/sh
gnome-terminal --geometry 80x25+100+100 -e "python3 $(dirname "$0")/digital_tickler/digital_tickler.py"
read input_variable
echo " "
