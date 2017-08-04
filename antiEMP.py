"""
Python code that reads 8 bits of laser data with a camera, rather quickly. It uses a Computer Vision library (opencv) and does image analysis (histogram).
Not that DRY.

"""
import pygame
import pygame.camera
from pygame.locals import *
from termcolor import colored

import Image
from pygame.locals import *
import sys
from PIL import Image
import ImageChops
import math, operator
import itertools
import binascii

#import opencv
#this is important for capturing/displaying images
#from opencv import highgui 

from ctypes import *
import sys
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, EncoderPositionChangeEventArgs, InputChangeEventArgs
from Phidgets.Devices.LED import LED, LEDCurrentLimit, LEDVoltage
from Phidgets.Devices.Encoder import Encoder
from time import sleep
import time

#Create an LED object
try:
    led = LED()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (led.isAttached(), led.getDeviceName(), led.getSerialNum(), led.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")

#Event Handler Callback Functions
def ledAttached(e):
    attached = e.device
    print("LED %i Attached!" % (attached.getSerialNum()))

def ledDetached(e):
    detached = e.device
    print("LED %i Detached!" % (detached.getSerialNum()))

def ledError(e):
    source = e.device
    print("LED %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))

#Main Program Code
try:
    led.setOnAttachHandler(ledAttached)
    led.setOnDetachHandler(ledDetached)
    led.setOnErrorhandler(ledError)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    exit(1)

try:
    led.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    exit(1)
print("Waiting for attach....")

try:
    led.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        led.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        exit(1)
    exit(1)
else:
    displayDeviceInfo()

print("Setting the output current limit and voltage levels to the default values....")
print("This is only supported on the 1031 - LED Advanced")

#try to set these values, if we get an exception, it means most likely we are using an old 1030 LED board instead of a 1031 LED Advanced board
try:
    led.setCurrentLimit(LEDCurrentLimit.CURRENT_LIMIT_80mA)
    led.setVoltage(LEDVoltage.VOLTAGE_5_0V)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))

#camera = highgui.cvCreateCameraCapture(0)
def get_image():
    im = highgui.cvQueryFrame(camera)
    # Add the line below if you need it (Ubuntu 8.04+)
    im = opencv.cvGetMat(im)
    #convert Ipl image to PIL image
    return opencv.adaptors.Ipl2PIL(im) 

def rmsdiff_2011(im1, im2):
    "Calculate the root-mean-square difference between two images"
    diff = ImageChops.difference(im1, im2)
    h = diff.histogram()
    sq = (value*(idx**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
    return rms

def ncycle(iterable, n):
    for item in itertools.cycle(iterable):
      for i in range(n):
        yield item

fps = 30.0
#pygame.init()
pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(640,480))
cam.start()
#window = pygame.display.set_mode((640,480))
#pygame.display.set_caption("WebCam Demo")
#screen = pygame.display.get_surface()

img1_b = Image.open('laser1_blank.jpg')
img2_b = Image.open('laser2_blank.jpg')
img3_b = Image.open('laser3_blank.jpg')
img4_b = Image.open('laser4_blank.jpg')
img5_b = Image.open('laser5_blank.jpg')
img6_b = Image.open('laser6_blank.jpg')
img7_b = Image.open('laser7_blank.jpg')
img8_b = Image.open('laser8_blank.jpg')

img1_b= img1_b.convert('L')
img2_b= img2_b.convert('L')
img3_b= img3_b.convert('L')
img4_b= img4_b.convert('L')
img5_b= img5_b.convert('L')
img6_b= img6_b.convert('L')
img7_b= img7_b.convert('L')
img8_b= img8_b.convert('L')
s="Kometkameratene, vi vil laere, vi vil teste"
l=list(s)
a=ncycle(l,1)

while True:
     e=a.next()
     c=map(int,list(bin(ord(e))[2:].zfill(8)))
     d=[0,0,0,0,0,0,0,0] 
#     c=[1,1,1,1,1,1,1,1]
#     c=[0,0,0,0,0,0,0,0]
#     print c
#     sleep(.5)
     b=77*c[0]
     led.setDiscreteLED(0,b)
     led.setDiscreteLED(0,b)
     led.setDiscreteLED(0,b)
#     sleep(.1)
     b=77*c[1]
     led.setDiscreteLED(1,b)
     led.setDiscreteLED(1,b)
     led.setDiscreteLED(1,b)
#     sleep(.1)
     b=77*c[2]
     led.setDiscreteLED(2,b)
     led.setDiscreteLED(2,b)
     led.setDiscreteLED(2,b)
#     sleep(.1)
     b=77*c[3]
     led.setDiscreteLED(3,b)
     led.setDiscreteLED(3,b)
     led.setDiscreteLED(3,b)
#     sleep(.1)
     b=77*c[4]
     led.setDiscreteLED(4,b)
     led.setDiscreteLED(4,b)
     led.setDiscreteLED(4,b)
#     sleep(.1)
     b=77*c[5]
     led.setDiscreteLED(5,b)
     led.setDiscreteLED(5,b)
     led.setDiscreteLED(5,b)
#     sleep(.1)
     b=77*c[6]
     led.setDiscreteLED(6,b)
     led.setDiscreteLED(6,b)
     led.setDiscreteLED(6,b)
#     sleep(.1)
     b=77*c[7]
     led.setDiscreteLED(7,b)
     led.setDiscreteLED(7,b)
     led.setDiscreteLED(7,b)

#    events = pygame.event.get()
#    for event in events:
#        if event.type == QUIT or event.type == KEYDOWN:
#            sys.exit(0)
#     sleep(.5)
#     print camera.query_image()
#     im = get_image()
#     image = cam.get_image()
     image = cam.get_image()
     image = cam.get_image()
#     pygame.image.save(im,"filename.jpg")
#     img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
#pygame.image.save(img,"filename1.jpg")
     pil_string_image = pygame.image.tostring(image, "RGBA",False)
     img = Image.fromstring("RGBA",(640,480),pil_string_image)
#     img = Image.fromstring("RGBA",(640,480),image)
#     img=im 
#    screen.blit(pg_img, (0,0))
#    pygame.display.flip()
#     pygame.time.delay(int(1000 * 1.0/fps))
     img= img.convert('L')
#     img.save('filename1.jpg',"JPEG")

     left = 28
     top = 354
     width = 25
     height = 40
     box = (left, top, left+width, top+height)
     area1 = img.crop(box)
#     area1.save('laser1.jpg', 'jpeg')
     left=87
     top=354
     box = (left, top, left+width, top+height)
     area2 = img.crop(box)
#     area2.save('laser2.jpg', 'jpeg')
     left=194
     top=354
     box = (left, top, left+width, top+height)
     area3 = img.crop(box)
#     area3.save('laser3.jpg', 'jpeg')
     left=260
     top=354
     box = (left, top, left+width, top+height)
     area4 = img.crop(box)
#     area4.save('laser4.jpg', 'jpeg')
     left=371
     top=354
     box = (left, top, left+width, top+height)
     area5 = img.crop(box)
#     area5.save('laser5.jpg', 'jpeg')
     left=435
     top=354
     box = (left, top, left+width, top+height)
     area6 = img.crop(box)
#     area6.save('laser6.jpg', 'jpeg')
     left=545
     top=354
     box = (left, top, left+width, top+height)
     area7 = img.crop(box)
#     area7.save('laser7.jpg', 'jpeg')
     left=603
     top=354
     box = (left, top, left+width, top+height)
     area8 = img.crop(box)
#     area8.save('laser8.jpg', 'jpeg')
     del img
#area1= area1.convert('L')
#area2= area2.convert('L')
#area3= area3.convert('L')
#area4= area4.convert('L')
#area5= area5.convert('L')
#area6= area6.convert('L')
#area7= area7.convert('L')
#area8= area8.convert('L')

     d[0]=1 if rmsdiff_2011(img1_b,area1) > 35 else 0
     d[1]=1 if rmsdiff_2011(img2_b,area2) > 35 else 0
     d[2]=1 if rmsdiff_2011(img3_b,area3) > 35 else 0
     d[3]=1 if rmsdiff_2011(img4_b,area4) > 35 else 0
     d[4]=1 if rmsdiff_2011(img5_b,area5) > 35 else 0
     d[5]=1 if rmsdiff_2011(img6_b,area6) > 35 else 0
     d[6]=1 if rmsdiff_2011(img7_b,area7) > 30 else 0
     d[7]=1 if rmsdiff_2011(img8_b,area8) > 24 else 0
          
#     print rmsdiff_2011(img1_b,area1)
#     print rmsdiff_2011(img2_b,area2)
#     print rmsdiff_2011(img3_b,area3)
#     print rmsdiff_2011(img4_b,area4)
#     print rmsdiff_2011(img5_b,area5)
#     print rmsdiff_2011(img6_b,area6)
#     print rmsdiff_2011(img7_b,area7)
#     print rmsdiff_2011(img8_b,area8)
#     print e, " ", c, " ", d, " ", binascii.unhexlify('%0.8x' % int('0b' + ''.join(map(str, d)), 2))
     f = binascii.unhexlify('%0.8x' % int('0b' + ''.join(map(str, d)), 2))
     if c == d:
         print colored(f, 'green')
     else:
         print colored(f, 'red')
		


     area1=img1_b
     area2=img2_b
     area3=img3_b
     area4=img4_b
     area5=img5_b
     area6=img6_b
     area7=img7_b
     area8=img8_b
