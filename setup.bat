@echo off
title python setup
color 0a

echo installing libraries...
py -3 -m pip install -U pip
py -3 -m pip install -U discord.py
py -3 -m pip install -U pystyle

echo.
echo finished installing setup
pause
