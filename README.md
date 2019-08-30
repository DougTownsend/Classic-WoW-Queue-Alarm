# Classic WoW Queue Alarm

This takes a screenshot every 15 seconds and uses OCR to read the queue position. When you get to the end of the queue it sounds an alarm. It also logs the position in a csv file which can be used to see the pattern of players logging off.

The screenshot function seems to only capture the primary monitor, so make sure that is where the game is. The alarm sounds use winbeep, which I assume is only for windows. Mac users might need to swap this out for something else.

# Requirements

Python 3.7 with the following packages installed:  
OpenCV  
pyautogui  
pytesseract

You also have to have Tesseract OCR installed on your computer which can be found here:  
https://github.com/tesseract-ocr/

