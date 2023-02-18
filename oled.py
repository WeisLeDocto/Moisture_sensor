# coding: utf-8

from machine import I2C
from binary_ascii import bin_tuple

# The startup instructions for the setting up the display
init_cmds = (0xAE,  # Switch off display
             0x20,  0x00,  # Set addressing mode to horizontal
             0x40,  # Set the first addressing line to line 0
             0xA1,  # Column 127 mapped to SEG0
             0xA8, 31,  # Set the number of lines to 32
             0x22, 0x00, 0x03,  # Cropping the display to 32 lines
             0xC8,  # Set the scan direction to inverted
             0xD3, 0x00,  # Set the vertical offset to 0
             0xDA, 0x02,  # Sequential COM pin configuration
             0xD5, 0x80,  # Set default clock frequency and divider
             0xD9, 0x22,  # Set the pre-charge period
             0xDB, 0x20,  # Set COM deselect level
             0x81, 0xFF,  # Set contrast to the maximum
             0xA4,  # Display follows RAM content
             0xA6,  # Display pixels are not inverted
             0x8D, 0x14,  # Enable charge pump
             0xAF  # Switch display on
             )


class Oled:
  """Class for controlling Adafruit's 0.91" monochrome 128x32 Oled display over
  I2C.

  Its main purpose it to correctly initialize the display and to update the
  displayed text.
  Information on the display can be found at:
  https://www.adafruit.com/product/4440
  """

  def __init__(self, i2c: I2C) -> None:
    """Initializes the display over the provided i2c connection object."""

    self._i2c = i2c
    self._addr = 0x3C
    self._rows = 32
    self._cols = 128
    self._buf = bytearray(self._cols // 8 * self._rows)

    for cmd in init_cmds:
      self._send_cmd(cmd)

  def __str__(self) -> str:
    """Returns an overview of what the display should look like given the
    current data buffer.

    Might be too heavy for the memory of basic microcontrollers.
    """

    return '\n'.join(' '.join('*' if self._get_pix(i, j) else ' '
                              for j in range(self._cols))
                     for i in range(self._rows))

  def power(self, on: bool) -> None:
    """Powers the screen on or off, but preserves the settings and the data
    buffer."""

    self._send_cmd(0xAE | int(on))

  def reset(self) -> None:
    """Resets the display to black pixels only."""

    self._reset_buf()
    self._send_buf()

  def display(self,
              text: str,
              pad_x: int = 4,
              pad_y: int = 4,
              space_y: int = 4) -> None:
    """Updates the buffer according to the given message to display, and sends
    the updated buffer.

    Args:
      text: The text to display, with each line separated by a line return
        character.
      pad_x: The number of pixels to leave black between the text and the
        borders of the screen in the x direction.
      pad_y: The number of pixels to leave black between the text and the
        borders of the screen in the y direction.
      space_y: The number of pixels to leave black between two lines.
    """

    self._write_buf(text=text,
                    pad_x=pad_x,
                    pad_y=pad_y,
                    space_y=space_y)

    self._send_buf()

  def _reset_buf(self) -> None:
    """Resets the data buffer to only zeros."""

    for i in range(self._rows):
      for j in range(self._cols):
        self._set_pix(i, j, False)

  def _write_buf(self,
                 text: str,
                 pad_x: int = 4,
                 pad_y: int = 4,
                 space_y: int = 4) -> None:
    """Checks whether the given text fits on the screen for the given settings,
    and if it does updates the data buffer accordingly.

    Args:
      text: The text to display, with each line separated by a line return
        character.
      pad_x: The number of pixels to leave black between the text and the
        borders of the screen in the x direction.
      pad_y: The number of pixels to leave black between the text and the
        borders of the screen in the y direction.
      space_y: The number of pixels to leave black between two lines.
    """

    lines = text.split('\n')

    if 8 * len(lines) + space_y * (len(lines) - 1) + 2 * pad_y > self._rows:
      raise ValueError("Too many lines to display !")
    if any(len(line) + 2 * pad_x > self._cols for line in lines):
      raise ValueError("Line too long to display !")

    self._reset_buf()

    for i, line in enumerate(lines):
      for j, char in enumerate(line):
        for k, byte in enumerate(bin_tuple[ord(char) - 32]):
          for m, val in enumerate(byte >> n & 0b1 for n in range(7, -1, -1)):
            self._set_pix(pad_y + (8 + space_y) * i + k,
                          pad_x + 8 * j + m, bool(val))

  def _send_buf(self) -> None:
    """Sends the data buffer to the display."""

    self._i2c.writevto(self._addr, [b'\x40', self._buf])

  def _send_cmd(self, cmd: int):
    """Sends a single command to the display, for setting parameters."""

    self._i2c.writeto(self._addr, bytearray([0x80, cmd]))

  def _get_pix(self, row: int, col: int) -> int:
    """Returns the value of the pixel at position row, col in the data
    buffer."""

    return self._buf[col + (row // 8) * self._cols] >> (row % 8) & 0b1

  def _set_pix(self, row: int, col: int, val: bool) -> None:
    """Sets the value of the pixel at position row, col in the data buffer to
    val."""

    prev = self._buf[col + (row // 8) * self._cols]

    if val:
      prev |= 1 << (row % 8)
    else:
      prev &= 0xFF - (1 << (row % 8))

    self._buf[col + (row // 8) * self._cols] = prev
