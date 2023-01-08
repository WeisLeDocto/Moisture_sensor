# coding: utf-8

from utime import sleep_ms
from ustruct import unpack
from machine import I2C


class Seesaw:
  """This class can read data from Adafruit's capacitive soil sensor.

  It can acquire the moisture level and/or the temperature. More information on
  the sensor can be found at: https://www.adafruit.com/product/4026
  """

  def __init__(self, i2c: I2C) -> None:
    """Initializes the sensor over the provided i2c connection object."""

    # Setting the attributes
    self._i2c = i2c
    self._addr = 0x36
    self._moisture = bytearray(2)
    self._temp = bytearray(4)

    # Resetting the sensor
    self._i2c.writeto(self._addr, bytearray([0x00, 0x7F, 0xFF]))
    sleep_ms(500)

  def read_moisture(self) -> int:
    """Reads the moisture level from the sensor and returns it as an int."""

    self._i2c.writeto(self._addr, bytearray([0x0F, 0x10]))
    sleep_ms(5)
    self._i2c.readfrom_into(self._addr, self._moisture)

    return unpack('>H', self._moisture)[0]

  def read_temperature(self) -> float:
    """Reads the temperature from the sensor and returns it as a float."""

    self._i2c.writeto(self._addr, bytearray([0x00, 0x04]))
    sleep_ms(5)
    self._i2c.readfrom_into(self._addr, self._temp)
    self._temp[0] &= 0x3F

    return 0.00001525878 * unpack('>I', self._temp)[0]
