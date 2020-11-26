#!/usr/bin/env python3
import subprocess

def take_picture(filename):
    test = subprocess.Popen([
    "gphoto2",
    "--capture-image-and-download",
    "--filename", "/home/pi/Desktop/DSLR-photos/"+filename],
    stdout=subprocess.PIPE)

#https://www.youtube.com/watch?v=88oD1o6R6gE