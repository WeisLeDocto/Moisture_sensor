# coding: utf-8

import machine
from utime import sleep_ms
from oled import Oled
from seesaw import Seesaw

# Switching off the central led
spi = machine.SPI(1, baudrate=100000, sck=machine.Pin("PA01"),
                  mosi=machine.Pin("PA00"))
spi.write(bytearray(b'\x00\x00\x00\x00\xff\x00\x00\x00\xff'))
spi.deinit()

# Initializing the I2C devices
i2c = machine.I2C(0, sda=machine.Pin("PA08"), scl=machine.Pin("PA09"))
display = Oled(i2c)
sensor = Seesaw(i2c)

# DAC for communication with the sprinkler
dac = machine.DAC(0)
dac.write(0)

# Pins for checking whether the sprinkler is connected
pin_in = machine.Pin("PA06", machine.Pin.IN, machine.Pin.PULL_DOWN)
display_on = bool(pin_in.value())
prev = display_on

# The main loop, executed once every second
while True:

  # Checking whether the sprinkler is connected
  display_on = bool(pin_in.value())

  # Reading the moisture and temperature
  moisture = sensor.read_moisture()
  temperature = round(sensor.read_temperature(), 1)

  # Either displaying the information or sending it to the sprinkler
  if display_on:
    # If the display was not previously on, switching it on
    # Also disabling the sprinkler
    if not prev:
      display.power(True)
      dac.write(0)
    # Updating the displayed value
    display.display("Humidite: {}\nTemp: {} C".format(int(moisture),
                                                      int(temperature)))
  else:
    # Making sure the display remains off
    display.power(False)
    dac.write(min(1023, moisture))

  # Storing the value of display_on for the next loop
  prev = display_on

  # No need to loop to fast
  sleep_ms(1000)
