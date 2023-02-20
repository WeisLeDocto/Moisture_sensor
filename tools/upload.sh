#!/bin/sh

# pyboard.py available at https://github.com/micropython/micropython/blob/master/tools/pyboard.py

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

# Displaying the list of possible files to upload
i=1
echo "Which file to upload ?"
for entry in ../code/*
do
  if echo "$entry" | grep -q .py; then
    echo "$i" ': ' "$entry"
    i=$((i+1))
  fi
done
echo "(ctrl + c to escape)"
echo ""

# Letting the user select the file to upload
printf "File n°: "
read -r file_nr
echo ""

# Making sure the selected file is valid
while { ! echo "$file_nr" | grep -q '^[0-9]' || [ "$file_nr" -gt "$((i-1))" ] || [ "$file_nr" -le 0 ]; }; do
  echo "Invalid choice !"
  i=1
  echo "Which file to upload ?"
  for entry in ../code/*
  do
  if echo "$entry" | grep -q .py; then
    echo "$i" ': ' "$entry"
    i=$((i+1))
  fi
  done
  echo "(ctrl + c to escape)"
  echo ""
  printf "File n°: "
  read -r file_nr
  echo ""
done

# Displaying a message indicating which file will be uploaded to which device
i=1
for entry in ../code/*
do
  if echo "$entry" | grep -q .py; then
    if [ "$i" = "$file_nr" ]; then
      file=$entry
      echo "Uploading $file to /dev/ttyACM$port"
      echo ""
    fi
  i=$((i+1))
  fi
done

# Finally, uploading the file
python3 -m pyboard -d "/dev/ttyACM$port" -f cp "$file" :
