import os
import pygame as pg
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import pygame.camera
from tokenize import Number
from numpy import testing
from pygame import image
import sys
from pygame.locals import *
import numpy as np
import keras
from keras.models import load_model # type: ignore
 # we are using load_model to load the model.keras file 
import cv2  # this is used to read the image
from tensorflow.python.keras.backend import constant

windowSizeX = 800
windowSizeY = 600

BOUNDRYINC = 5
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

MODEL = load_model("model.keras") 

#take a dictionary
labels = {0:'zero', 1:'one', 2:'two', 3:'three', 4:'four', 5:'five', 6:'six', 7:'seven', 8:'eight', 9:'nine'}

# # set the font file path and font size
font_path = 'arial.ttf'
font_size = 16


pg.init()  # initialize all pg module
pg.mixer.init() #initialize sound 

#creating window
SCREEN = pg.display.set_mode((windowSizeX, windowSizeY))
pg.display.set_caption('click')
pg.display.set_caption('Digit Board')
ICON = pg.image.load('icon.png')
pg.display.set_icon(ICON)



numXcord, numYcord = [], []

PREDICT = True


sound = pg.mixer.Sound(os.path.join('mixkit-modern-technology-select-3124.wav'))


font = pygame.font.SysFont("Arial", 26)
txtsurf = font.render("Clear", True, BLACK)
SCREEN.blit(txtsurf,(370, 548))
fontObj = pg.font.Font(font_path, font_size)  # create the font object
drawing = False
run = True

# # Button setup
# quit_button = pg.Rect(windowSizeX - 150, windowSizeY - 50, 100, 40)
# clear_button = pg.Rect(windowSizeX - 300, windowSizeY - 50, 100, 40)

# def draw_buttons():
#     pg.draw.rect(SCREEN, (100,100,100), quit_button)
#     pg.draw.rect(SCREEN, (100,100,100), clear_button)
    
#     quit_text = fontObj.render('Quit', True, WHITE)
#     clear_text = fontObj.render('Clear', True, WHITE)
    
#     SCREEN.blit(quit_text, (quit_button.x + 25, quit_button.y + 10))
#     SCREEN.blit(clear_text, (clear_button.x + 20, clear_button.y + 10))
    
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == MOUSEMOTION and drawing:
            xcord, ycord = pg.mouse.get_pos()
            numXcord.append(xcord)
            numYcord.append(ycord)
            pg.draw.circle(SCREEN, WHITE, pg.mouse.get_pos(), 7)
            print()
            
        if event.type == pg.MOUSEBUTTONDOWN:
            drawing = True
            # if quit_button.collidepoint(event.pos):
            #     run = False
            # if clear_button.collidepoint(event.pos):
            #     SCREEN.fill(BLACK)
                
        
        if event.type == pg.MOUSEBUTTONUP:
            drawing = False
            if numXcord and numYcord:  # Check if lists are not empty
                numXcord = sorted(numXcord)
                numYcord = sorted(numYcord)
            
            rect_min_x, rect_max_x = max(numXcord[0]-BOUNDRYINC, 0), min(windowSizeX,numXcord[-1]+BOUNDRYINC)
            rect_min_y, rect_max_y = max(numYcord[0]-BOUNDRYINC, 0), min(numYcord[-1]+BOUNDRYINC, windowSizeY)

            numXcord, numYcord = [], []       
           
            img_arr = np.array(pg.PixelArray(SCREEN))[rect_min_x:rect_max_x, rect_min_y:rect_max_y].T.astype(np.float32)
            
            if PREDICT:
                image = cv2.resize(img_arr,(28,28)) #resize img 
                image = np.pad(image, (10,10), 'constant', constant_values=0) #add padding
                image = np.array(image) 
                image = cv2.resize(image, (28,28))/255 # resize between [0, 1]
                reshaped_image = image.reshape(1,28,28,1) 
                prediction = MODEL.predict(reshaped_image)
                label = str(labels[np.argmax(prediction)])
                
               # Rendering the Predicted Label
                textSurfaceObj = fontObj.render(label, True, RED, WHITE)
                textRectObj = textSurfaceObj.get_rect()

                textRectObj.left, textRectObj.bottom = rect_min_x , rect_max_y + 30   #where to show the digit no.

                SCREEN.blit(textSurfaceObj, textRectObj)
                
            IMAGESAVE = True
    
        if event.type == KEYDOWN:
            if event.unicode == ' ':
                    pg.mixer.Sound.play(sound)
                    SCREEN.fill(BLACK)
        
        
        clear_text = fontObj.render('click \'space\' to clear the screen', True, WHITE)
        SCREEN.blit(clear_text, (windowSizeX//3, windowSizeY-30))
        pg.display.update()
        

          
pg.quit()




