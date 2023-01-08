#!/bin/sh

# Checking whether picocom is installed
if ! command -v picocom > /dev/null
then
    echo "picocom is not installed !"
    echo "It can be installed with sudo apt install picocom"
    exit
fi

dev=''

# Checking if there's at least one connected device
for entry in /dev/*
do
  if echo "$entry" | grep -q ttyACM; then
    dev="${dev} ${entry##"/dev/ttyACM"}"
  fi
done

dev=${dev##" "}

# Aborting if there's no connected device
if [ "$dev" = "" ]; then
  echo "No device connected, aborting !"; exit
fi

# Displaying the list of possible devices to upload files to
echo "On which USB port is the Trinket M0 connected ?"
i=1
for port in $dev; do
  echo "$i : " "/dev/ttyACM""$port"
  i=$((i+1))
done
echo "(ctrl + c to escape)"
echo ""

# Letting the user select a device
printf "Port : "
read -r port
echo ""

# Making sure the selected device is valid
while { ! echo "$port" | grep -q '^[0-9]' || [ "$port" -gt "$((i-1))" ] || [ "$port" -le 0 ]; }; do
  echo "Invalid choice !"
  echo "On which USB port is the Trinket M0 connected ?"
  i=1
  for port in $dev; do
    echo "$i : " "/dev/ttyACM""$port"
    i=$((i+1))
  done
  echo "(ctrl + c to escape)"
  echo ""
  printf "Port : "
  read -r port
  echo ""
done

# Saving the user's choice
i=1
for p in $dev; do
  if [ "$port" = $i ]; then
    port=$p
  fi
  i=$((i+1))
done

# Finally, opening the console on the selected device
picocom -b 115200 "/dev/ttyACM$port"
