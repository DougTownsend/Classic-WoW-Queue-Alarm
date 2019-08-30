# -*- coding: utf-8 -*-
import cv2
import pyautogui
import pytesseract
import winsound
import datetime
import time
import re

#Path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

#Get start time to name the csv file
now = datetime.datetime.now()
sample_rate = datetime.timedelta(seconds=15)
last_sample_datetime = now - sample_rate

#Create a csv file to log the data
csvfilename = str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '_' + str(now.hour) + '_' + str(now.minute) + '.csv'
csvfile = open(csvfilename, 'a+')
csvfile.close()

#example beep to adjust volume
winsound.Beep(1000, 500)

while True:
    now = datetime.datetime.now()
    
    #Wait until it has been 15 seconds since last reading
    while now - last_sample_datetime < sample_rate:
        #print(str(now - last_sample_datetime))
        time.sleep(1)
        now = datetime.datetime.now()
    
    #take a screenshot and open it
    pyautogui.screenshot('screenshot.png')
    img = cv2.imread('screenshot.png')

    #remove the blue and green channels and threshold the red channel to highlight text
    b,g,r = cv2.split(img)
    ret,img = cv2.threshold(r,127,255,cv2.THRESH_BINARY)
    
    #Apply OCR to image
    string = pytesseract.image_to_string(img)
    
    #Keep last image and OCR text saved for debugging
    cv2.imwrite('last_screenshot.png', img)
    last_text = open('last_text.txt', 'w+')
    last_text.write(str(string.encode('utf-8')))
    last_text.close()
    
    #extract the queue position. Include letters that the OCR might think the numbers are
    r1 = re.findall(r'queue: ([sSlLiIoO\d]+)', string)
    
    #print(string)
    if len(r1) > 0:
        #Replace any letters with numbers
        r1[0] = re.sub(r'[sS]', r'5', r1[0])
        r1[0] = re.sub(r'[lLiI]', r'1', r1[0])
        r1[0] = re.sub(r'[oO]', r'0', r1[0])
        
        #print queue position
        print(r1[0])
        
        #log the data into the csv file
        csvfile = open(csvfilename, 'a+')
        csvfile.write(str(now.month) + '/' + str(now.day) + '/' + str(now.year) + ' ' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second) + ',' + r1[0] + '\n')
        csvfile.close()
        
        #update the time of the last sample
        last_sample_datetime = now
    else:
        '''
        If the regex is not found that means either:
            1. The queue is over
            2. You disconnected
            3. The OCR made a mistake
        
        For any of these break out of the loop and sound the alarm
            
        If it is case 3, review last_screenshot.png and last_text.txt to
        find out the problem. Keep last_screenshot.png and use it as input
        as you adjust the image threshold and regex until it is read correctly.
        
        '''
        break
    
    #Wait until it has been 15 seconds since last reading
    while now - last_sample_datetime < sample_rate:
        #print(str(now - last_sample_datetime))
        time.sleep(1)
        now = datetime.datetime.now()

#Sound the alarm
while True:
    winsound.Beep(1000, 200)
    time.sleep(0.02)
