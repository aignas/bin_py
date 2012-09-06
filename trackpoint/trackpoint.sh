# !/bin/bash

DIR=/sys/devices/platform/i8042/serio1

# Press to select
echo $1 > ${DIR}/press_to_select
shift

# Inertia
echo $1 > ${DIR}/inertia
shift

# Sensitivity
echo $1 > ${DIR}/sensitivity
shift

# Speed
echo $1 > ${DIR}/speed
shift

echo "Done"
