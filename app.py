from tokenize import Number
from numpy import testing
from numpy.lib.type_check import imag
import pygame , sys
from pygame import image
from pygame.locals import *
import numpy as np
from keras.models import load_model
 # we are using load_model to load the model.h5 file 
import cv2  # this is used to read the image
from tensorflow.python.keras.backend import constant


windowSizeX = 640
windowSizeY = 480
#INITIALIZING THE Pygame

BOUNDRYINC = 5
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

IMAGESAVE = False
MODEL = load_model("model.h5") 

#take a dictionary
labels = {0:'zero', 1:'one', 2:'two', 3:'three', 4:'four', 5:'five', 6:'six', 7:'seven', 8:'eight', 9:'nine'}

pygame.init()

# set the font file path and font size
font_path = 'arial.ttf'
font_size = 16

# create the font object
fontObj = pygame.font.Font(font_path, font_size)

DISPLAYSURF = pygame.display.set_mode((windowSizeX, windowSizeY))

pygame.display.set_caption('Digit Board')

iswriting = False
numXcord = []
numYcord = []

image_cnt = 1
PREDICT = True

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == MOUSEMOTION and iswriting:
            xcord , ycord = event.pos
            pygame.draw.circle(DISPLAYSURF, WHITE, (xcord, ycord), 4,0)
            numXcord.append(xcord)
            numYcord.append(ycord)

        if event.type == MOUSEBUTTONDOWN:
            iswriting = True
        
        if event.type == MOUSEBUTTONUP:
            iswriting = False
            numXcord = sorted(numXcord)
            numYcord = sorted(numYcord)

           
            rect_min_x, rect_max_x = max(numXcord[0]-BOUNDRYINC, 0), min(windowSizeX,numXcord[-1]+BOUNDRYINC)
            rect_min_y, rect_max_y = max(numYcord[0]-BOUNDRYINC,0), min(numYcord[-1]+BOUNDRYINC, windowSizeX)

            numXcord = []
            numYcord = []
            
           

            img_arr = np.array(pygame.PixelArray(DISPLAYSURF))[rect_min_x:rect_max_x, rect_min_y:rect_max_y].T.astype(np.float32)

            if IMAGESAVE:
                cv2.imwrite("image.png")
                image_cnt += 1

            if PREDICT:
                image = cv2.resize(img_arr,(28,28))
                image = np.pad(image, (10,10), 'constant', constant_values=0)
                image = np.array(image)

                image = cv2.resize(image, (28,28))/255

                label = str(labels[np.argmax(MODEL.predict(image.reshape(1,28,28,1)))])
                
                textSurfaceObj = fontObj.render(label, True, RED, WHITE)
                textRectObj = textSurfaceObj.get_rect()
               # textsurface = FONT.render(label, True, RED, WHITE)
               # textRecObj = testing.get_rect()
                textRectObj.left, textRectObj.bottom = rect_min_x, rect_max_y

                DISPLAYSURF.blit(textSurfaceObj, textRectObj)

            if event.type == KEYDOWN:
                if event.unicode == 'n':
                     DISPLAYSURF.fill(BLACK)

        
        pygame.display.update()
