from tkinter import *
import tkinter.messagebox as tsmg
from PIL import ImageTk,Image
import speech_recognition as sr
import pyttsx3
import pyaudio
import pygame
import wikipedia
import webbrowser
from textwrap import fill
pygame.init()
pygame.mixer.init()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def render_textrect(string, font, rect, text_color, background_color,justification=0):
        """Returns a surface containing the passed text string, reformatted
        to fit within the given rect, word-wrapping as necessary. The text
        will be anti-aliased.
    
        Takes the following arguments:
    
        string - the text you wish to render. \n begins a new line.
        font - a Font object
        rect - a rectstyle giving the size of the surface requested.
        text_color - a three-byte tuple of the rgb value of the
                     text color. ex (0, 0, 0) = BLACK
        background_color - a three-byte tuple of the rgb value of the surface.
        justification - 0 (default) left-justified
                        1 horizontally centered
                        2 right-justified
    
        Returns the following values:
    
        Success - a surface object with the text rendered onto it.
        Failure - raises a TextRectException if the text won't fit onto the surface.
        """
    
        
        
        
        final_lines = []
    
        requested_lines = string.splitlines()
    
        # Create a series of lines that will fit on the provided
        # rectangle.
    
        for requested_line in requested_lines:
            if font.size(requested_line)[0] > rect.width:
                words = requested_line.split(' ')
                # if any of our words are too long to fit, return.
                for word in words:
                    if font.size(word)[0] >= rect.width:
                        print("Error")
                # Start a new line
                accumulated_line = ""
                for word in words:
                    test_line = accumulated_line + word + " "
                    # Build the line while the words fit.    
                    if font.size(test_line)[0] < rect.width:
                        accumulated_line = test_line
                    else:
                        final_lines.append(accumulated_line)
                        accumulated_line = word + " "
                final_lines.append(accumulated_line)
            else:
                final_lines.append(requested_line)
    
        # Let's try to write the text out on the surface.
    
        surface = pygame.Surface(rect.size)
        surface.fill(background_color)
    
        accumulated_height = 0
        for line in final_lines:
            if accumulated_height + font.size(line)[1] >= rect.height:
                print("Error")
            if line != "":
                tempsurface = font.render(line, 1, text_color)
                if justification == 0:
                    surface.blit(tempsurface, (0, accumulated_height))
                elif justification == 1:
                    surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
                elif justification == 2:
                    surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
                else:
                    print("Error")
            accumulated_height += font.size(line)[1]
    
        return surface
    

def takeCommand():
    r =sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.energy_threshold = 300
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing....")
        query = r.recognize_google(audio,language ='en-in')
        print("User said : \n",query)
    except Exception as e:
        return "None"
    
    return query

engine = pyttsx3.init("sapi5")
voices =engine.getProperty("voices")
voice = engine.setProperty("voice",voices[0].id)
engine.setProperty("rate",120)

exit_game=False


gamewindow = pygame.display.set_mode((900,400))

img = pygame.image.load("./cyber.jpg")
img =pygame.transform.scale(img,(900,400)).convert_alpha()
clock =pygame.time.Clock() 
font = pygame.font.SysFont(None,20,bold=1,italic=1)
while not exit_game:
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            quit()
    gamewindow.blit(img,[0,0])
    rect = pygame.draw.rect(gamewindow,(250,250,250),[0,340,900,60])
    pygame.draw.rect(gamewindow,(250,250,250),[0,340,900,60])    
    
    speak("Hey dear Sarthak!!")
    pygame.display.update()
    reply = takeCommand().lower()
    if "wikipedia" in reply:
        reply.replace("wikipedia"," ")
        result = wikipedia.summary(reply,sentences=2)
        speak("According to Wikipedia...")
        
        fonts = render_textrect(result, font, rect, (0,0,0),(216,216,216), justification=0)
        
        gamewindow.blit(fonts,[rect.left,rect.top])
        pygame.display.update()
        speak(result)
        
        
        
    if "google" in reply:
        webbrowser.open("www.google.com")
    if "bye" in reply:
        speak("Lets have a chat some other time")
        quit()

    
    clock.tick(90)