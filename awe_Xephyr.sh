#! /bin/bash

export DISPLAY=1.0
RESOLUTION="1152x720"

Xephyr :1 -ac -br -noreset -screen ${RESOLUTION} &
awesome -c ${HOME}/.config/awesome/rc.lua
