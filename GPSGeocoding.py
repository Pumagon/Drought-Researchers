import gpsserial as gps

serialPort = "/dev/serial0"
gpsSerialPort = gps.init(serialPort)
    
gpsData = gps.getData(gpsSerialPort)
print(gpsData)

lat = gps.getLatitude(gpsData)
lon = gps.getLongitude(gpsData)
print("Raw latitude: " + lat + ", Raw longitude: " + lon)

nsIndicator = gps.getNSIndicator(gpsData)
ewIndicator = gps.getEWIndicator(gpsData)
        
latDegree = gps.getLatitudeDegree(gpsData)
latMinute = gps.getLatitudeMinute(gpsData)
lonDegree = gps.getLongitudeDegree(gpsData)
lonMinute = gps.getLongitudeMinute(gpsData)
print("Latitude degree: " + str(latDegree) +
      ", Latitude minute: " + str(latMinute) + ", NS Indicator: " + nsIndicator)
print("Longitude degree: " + str(lonDegree) +
      ", Longitude minute: " + str(lonMinute) + ", EW Indicator: " + ewIndicator)
        
decimalLat = gps.getDecimalLatitude(gpsData)
decimalLon = gps.getDecimalLongitude(gpsData)
print("Decimal latitude: " + str(decimalLat) + ", Decimal longtitude: " + str(decimalLon))

gMapsLink = "https://www.google.com/maps?q=" + str(decimalLat) + "," + str(decimalLon)
print("Google Maps link: " + gMapsLink)
        
print("")
gpsSerialPort.close()

import geocoder
from datetime import datetime, timedelta
from nasapower import *
from usdm import *
from usstates import *
import time
import subprocess

from openweather import *

weatherApiKey = "401c88f3833d74e8bc94c60dc832a666"
    
dataToDownload = ["ALLSKY_SFC_SW_DWN", "T2M", "T2M_MAX", "TS", "TS_MAX", "PRECTOTCORR", "RH2M"]

def getPastDate(daysAgo):
    doubleDigitMonth = doubleDigitDay = "00"
    today = datetime.now()
    dt = today - timedelta(days=daysAgo)
    if dt.month // 10 == 0:
        doubleDigitMonth = "0" + str(dt.month)
    else:
        doubleDigitMonth = str(dt.month)
    if dt.day // 10 == 0:
        doubleDigitDay = "0" + str(dt.day)
    else:
        doubleDigitDay = str(dt.day)
    return str(dt.year) + doubleDigitMonth + doubleDigitDay

def ipToLatLonCityState():
    geoInfo = geocoder.ip("me")
    lat = geoInfo.lat
    lon = geoInfo.lng
    city = geoInfo.city
    state = geoInfo.state
    return (lat, lon, city, state)

lat, lon, city, stateFullName = ipToLatLonCityState()
stateCode = stateToStateCode[stateFullName]
print("Current latitude, longitude: ", lat, lon)
print("Current address: ", city, stateCode)

yesterday = getPastDate(1)
daysAgo14 = getPastDate(14)
daysAgo15 = getPastDate(15)
daysAgo28 = getPastDate(28)

import argparse
import qrcode
from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from inky.auto import auto
from PIL import Image
import inky_paste

try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")

try:
    inky_display.set_border(inky_display.WHITE)
except NotImplementedError:
    pass

scale_size = 1.0
padding = 0

if inky_display.resolution == (400, 300):
    scale_size = 2.20
    padding = 15

if inky_display.resolution == (600, 448):
    scale_size = 2.20
    padding = 30

if inky_display.resolution == (250, 122):
    scale_size = 1.30
    padding = -5
# Display the completed name badge


inky_display.show()

img = Image.new("P", inky_display.resolution)
draw = ImageDraw.Draw(img)

y_top = int(inky_display.height * (5.0 / 10.0))
y_bottom = y_top + int(inky_display.height * (4.0 / 10.0))

for y in range(y_top, inky_display.height):
    for x in range(0, inky_display.width):
        img.putpixel((x, y), inky_display.WHITE)

if inky_display.resolution == (400, 300):
    scale_size = 2.20
    padding = 15

if inky_display.resolution == (600, 448):
    scale_size = 2.20
    padding = 30

if inky_display.resolution == (250, 122):
    scale_size = 1.30
    padding = -5

# Display the completed name badge

inky_display.set_image(img)
inky_display.show()

today = datetime.now()

# PIMORONI Inky pHAT boilerplate
from inky.auto import auto
inky_display = auto()

inky_display.set_border(inky_display.WHITE)
inky_display_img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))

# --- Write your program below ---

# create
qrText = "https://www.mass.gov/info-details/drought-status"
command = "qr \"" + qrText + "\" > qrCode.png"
subprocess.run(command, shell=True)
img_path = "./qrCode.png"

severityIndex = downloadUsdmData(city, stateCode, daysAgo14, yesterday)
severityDescription = ["Abnormally Dry", "Moderate Drought",
                       "Severe Drought", "Extreme Drought", "Exceptional Drought"]


#inky_display_img = inky_paste.image(inky_display_img, img_path, 0, 0)
inky_display_img = inky_paste.image_convert(inky_display_img, img_path, -16, 0)

inky_paste.text(inky_display_img, (severityDescription[severityIndex]), inky_display.RED, 17, 95, 5)
inky_paste.text(inky_display_img, ("Address: " + city + "," + stateCode), inky_display.BLACK, 13, 95, 30)
inky_paste.text(inky_display_img, str(today), inky_display.BLACK, 16, 95, 49)
#inky_paste.text(inky_display_img, "Hello, World!", inky_display.BLACK, 13, 95, 71)
#inky_paste.text(inky_display_img, "Hello, World!", inky_display.BLACK, 22, 95, 93)


# --- Write your program above ---

# Display the image
inky_display.set_image(inky_display_img)
inky_display.show()
