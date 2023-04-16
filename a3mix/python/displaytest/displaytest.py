#!/usr/bin/python
# -*- coding: utf-8 -*-

import TCA9548A
import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106, ssd1306
from PIL import ImageFont, ImageDraw, Image

# 5 Oled Displays (SSD1306 or SH1106) connected to an i2c Multiplexer TCA9548A
# I2C Display Addresses:
SSD1306_I2C_ADDRESS_2 = 0x3d 
SSD1306_I2C_ADDRESS_3 = 0x3d
SSD1306_I2C_ADDRESS_4 = 0x3d
SSD1306_I2C_ADDRESS_5 = 0x3c
SSD1306_I2C_ADDRESS_6 = 0x3c

# set specific multiplexer to a specific channel
# TCA9548A.I2C_setup( multiplexer_addr , multiplexer_channel )
#TCA9548A.I2C_setup(0x70,2)

# try to use a display

oled_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)

def disp_1():
  TCA9548A.I2C_setup(0x70,2)
  serial_dev_1 = i2c(port=1, address=0x3d)
  device_dev_1 = ssd1306(serial_dev_1, rotate=2)
  with canvas(device_dev_1) as draw:
    draw.rectangle(device_dev_1.bounding_box, outline = "white", fill = "black")
    draw.text((15, 5), "ST: 1", font = oled_font, fill = "white")

def disp_2():
  TCA9548A.I2C_setup(0x70,3)
  serial_dev_2 = i2c(port=1, address=0x3d)
  device_dev_2 = ssd1306(serial_dev_2, rotate=2)
  with canvas(device_dev_2) as draw:
    draw.rectangle(device_dev_2.bounding_box, outline = "white", fill = "black")
    draw.text((15, 5), "ST: 2", font = oled_font, fill = "white")

def disp_3():
  TCA9548A.I2C_setup(0x70,4)
  serial_dev_3 = i2c(port=1, address=0x3d)
  device_dev_3 = ssd1306(serial_dev_3, rotate=2)
  with canvas(device_dev_3) as draw:
    draw.rectangle(device_dev_3.bounding_box, outline = "white", fill = "black")
    draw.text((15, 5), "ST: 3", font = oled_font, fill = "white")

def disp_4():
  TCA9548A.I2C_setup(0x70,5)
  serial_dev_4 = i2c(port=1, address=0x3c)
  device_dev_4 = ssd1306(serial_dev_4, rotate=2)
  with canvas(device_dev_4) as draw:
    draw.rectangle(device_dev_4.bounding_box, outline = "white", fill = "black")
    draw.text((15, 5), "ST: 4", font = oled_font, fill = "white")

def disp_5():
  TCA9548A.I2C_setup(0x70,6)
  serial_dev_5 = i2c(port=1, address=0x3c)
  device_dev_5 = ssd1306(serial_dev_5)
  with canvas(device_dev_5) as draw:
    draw.rectangle(device_dev_5.bounding_box, outline = "white", fill = "black")
    draw.text((15, 5), "Discrete", font = oled_font, fill = "white")

while True:
  disp_1()
  disp_2()
  disp_3()
  disp_4()
  disp_5()
