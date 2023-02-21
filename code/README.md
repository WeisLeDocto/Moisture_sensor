# Code

This folder contains the code to upload to the microcontroller for driving the
moisture sensor setup. All four files must be uploaded in order for the project
to work properly. The oled.py file contains the code driving the display. The
seesaw.py file contains the code driving the moisture sensor. The binary_ascii.py
file contains binary objects encoding 8x8 ASCII characters, since MicroPython
does not natively include any font. Finally, the main.py file is the main code
that will be executed by the microcontroller and import the objects contained 
in the three other files.