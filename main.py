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
display_on = not bool(pin_in.value())


def power_callback(pin) -> None:
  """Callback called when the polarity of the pin checking whether the
  sprinkler is connected changes.

  When the sprinkler is connected, the display is shut off and the DAC is
  enabled, and vice-versa when the sprinkler is disconnected.
  """

  global display
  connected = bool(pin.value())
  display.power(not connected)
  global display_on
  display_on = not connected
  global dac
  dac.write(0)


# Affecting the callback to the pin
pin_in.irq(power_callback,
           trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING)


while True:

  # Disabling callback as we don't want it to trigger while sending data
  machine.disable_irq()
  # Reading the moisture and temperature
  moisture = sensor.read_moisture()
  temperature = round(sensor.read_temperature(), 1)

  # Either displaying the information or sending it to the sprinkler
  if display_on:
    display.display("Humidite: {}\nTemp: {} C".format(int(moisture),
                                                      int(temperature)))
  else:
    dac.write(min(1023, moisture))
  # Re-enabling callback
  machine.enable_irq()

  # No need to loop to fast
  sleep_ms(1000)
