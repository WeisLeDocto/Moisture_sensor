# U2F Files

The two .u2f files in this folder are meant to be copy-pasted in the filesystem
of the microcontroller. To do so, the microcontroller should first be connected 
to a PC. Then, it should be put in the correct mode by double-clicking on the
reset switch. The filesystem of the microcontroller should then open on the PC, 
allowing to drag and drop the files. The bootloader should be uploaded first, 
and then the other file containing MicroPython.