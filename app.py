import pytesseract
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image
import pyautogui as pg
import os
from autocorrect import Speller


root = Tk()
path_to_tesseract = r"C:\Users\willi\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = path_to_tesseract
spell = Speller()

# takes screenshot of entire screen, shows the image captured, then redisplays the program window
# to do: select screenshot size
def screenshot():
    img = pg.screenshot("img.png")
    img.show()
    root.deiconify()

# removes program window out of frame then runs screenshot()
def hide_window():
    root.withdraw()
    root.after(1000, screenshot)

# reads text from img.png user tesseract
# to add: remove color, blur, & thresh
# https://www.geeksforgeeks.org/reading-text-from-the-image-using-tesseract/
def getText():
    filename = filedialog.askopenfilename(initialdir = '/', title = "Select File", filetypes=(("image files", ".png"), ("image files", ".jpg"), ("image files", ".jpeg")))
    img = Image.open(filename)
    text = pytesseract.image_to_string(img)

    text = fix(text, 1) # autocorrects the entire text

    with open('text.txt', 'w') as f:
        f.write(text)
    
    os.system("notepad.exe text.txt")

# autocorrects words 
# text = the words, num = # of words to be fixed in sequence at a time
def fix(text, num):

    if text:
        arry = text.split()

        for i in range (len(arry) - num):

            words = ""

            for j in range(num):

                words += arry[i + j] + " "
            
            words = spell(words)

            arry = arry[0:i] + words.split() + arry[i + num:len(arry)]

        output = ""

        for i in arry:
            output += i + " "
        
        return output

    else:
        return text

canvas = Canvas(root, bg = "beige", width = 500, height = 400)
canvas.pack()

# button to take screenshots
# calls hide_window to remove program window from the frame first
capture = Button(canvas, font = ("Arial 12 bold"), text = "Screenshot", width = 10, bg = "lightblue", command = hide_window)
capture.place(relx = 0.35, rely = 0.3)

# button to read text from the image
scan = Button(canvas, font = ("Arial 12 bold"), text = "Scan Image", width = 10, bg = "lightblue", command = getText)
scan.place(relx = 0.35, rely = 0.5)

mainloop()


