# coding: utf-8

"""This script takes the image containing the ascii characters, isolates each
character, converts it to a numpy array, and then to a tuple of bytearrays.
The characters are sorted according to their ascii code. For some reason, the
space character isn't placed correctly.
"""

from PIL import Image
import numpy as np

if __name__ == '__main__':

  # Opening the image
  img = Image.open('font.png')
  img = np.array(img)[::4, ::4, 0]

  # Creating a numpy array for each character, sorted by ascii codes
  bitmap_dict = {chr(i): img[8 * ((i - 1) // 16): 8 * ((i - 1) // 16) + 8,
                             8 * ((i - 1) % 16): 8 * ((i - 1) % 16) + 8]
                 for i in range(33, 96)}
  bitmap_dict.update({chr(32): np.zeros((8, 8)).astype('uint8')})
  bitmap_dict.update({chr(i - 1):
                      img[8 * ((i - 1) // 16): 8 * ((i - 1) // 16) + 8,
                          8 * ((i - 1) % 16): 8 * ((i - 1) % 16) + 8]
                      for i in range(97, 128)})

  # Converting the numpy arrays to bytearrays
  bin_arr = 2 ** (7 - np.arange(8))
  bin_dict = {key: bytearray(int(np.sum(bin_arr * line / 255)) for line in val)
              for key, val in bitmap_dict.items()}

  # Converting the dict to a tuple, as the order of the elements is known
  bin_tuple = tuple(val for _, val in sorted(bin_dict.items(),
                                             key=lambda item: ord(item[0])))
