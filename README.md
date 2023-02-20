# Moisture sensor
This repo contains all the data of a home-made electronic moisture sensor project.

The moisture sensor is linked to a microcontroller, that reads the current
moisture and temperature value. These values are then displayed on a small
screen, also driven by the microcontroller. The entire setup is powered by
two coin cell batteries, and can be switched on and off using a switch. A Jack
outlet allows driving an automatic sprinkler, although the sprinkler project is still ongoing.

Almost all the components necessary for the project are directly available from 
Mouser, for less than $50. The casing, however, has to be 3D-printed. The PCB
connecting the electronic components together also has to be custom-made, or 
more likely ordered from a PCB manufacturer. A soldering iron and some tin is
ultimately required for soldering all the components to the PCB.

The moisture sensor is [Adafruit's STEMMA soil sensor](https://www.adafruit.com/product/4026),
the microcontroller is [Adafruit's Trinket M0](https://www.adafruit.com/product/3500),
and the display is [Adafruit's monochrome 128x32 I2C OLED display](https://www.adafruit.com/product/931).
The switch, connectors, and cables are also from Adafruit.

This repo contains :
- the bill of materials for ordering the various components from Mouser
- the .stl files for 3D-printing the casing
- the KiCad files for ordering the PCB from a PCB manufacturer
- the MicroPython code to upload to the microcontroller for driving the setup
- tools that were handful for the project
