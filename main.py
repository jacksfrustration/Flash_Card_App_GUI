import pandas as pd
import random
import time
from tkinter import *
current_card={}
BACKGROUND_COLOR = "#B1DDC6"
#try to read the to_learn csv file. if the file is not found it reads the initial french words csv file instead. this will occur the first time the program is ran
try:
    to_learn_data=pd.read_csv("./words_to_learn.csv")
except FileNotFoundError:

    original_data=pd.read_csv("./french_words.csv")
    to_learn=original_data.to_dict(orient="records")
else:
    to_learn=to_learn_data.to_dict(orient="records")

def flip_card():
    '''Flips card/changes word and title and picture in canvas'''
    canvas.itemconfig(card_title,text="English",fill="white")
    canvas.itemconfig(card_word,text=current_card["English"],fill="white")
    canvas.itemconfig(card_bg,image=card_back_img)

def next_card():
    '''generates a random choice from the list of dictionaries
    and presents the french word first. after 3 seconds
    the flip card function is called to present the word in english'''
    global current_card,flip_timer
    window.after_cancel(flip_timer)
    current_card=random.choice(to_learn)
    canvas.itemconfig(card_title,text="French",fill="black")
    canvas.itemconfig(card_word,text=current_card["French"],fill="black")
    canvas.itemconfig(card_bg,image=card_front_img)
    flip_timer=window.after(3000,func=flip_card)

def is_known():
    '''gets triggered if the user knows the word. removes that word from the
    list of dictionaries and saves the updated list into a csv file called to learn'''
    to_learn.remove(current_card)
    data=pd.DataFrame(to_learn)
    data.to_csv("words_to_learn.csv",index=False)
    next_card()

window=Tk()
window.title("Flash Card App")
window.config(padx=50,pady=50,bg=BACKGROUND_COLOR)
flip_timer=window.after(3000,func=flip_card)
canvas=Canvas(width=800,height=526)
card_front_img=PhotoImage(file="card_front.png")
card_back_img=PhotoImage(file="card_back.png")
card_bg=canvas.create_image(400,263,image=card_front_img)
card_title=canvas.create_text(400,150,text="",font=("Ariel",40,"italic"))
card_word=canvas.create_text(400,263,text="",font=("Ariel",60,"bold"))
canvas.config(bg=BACKGROUND_COLOR,highlightthickness=0)
canvas.grid(row=0,column=0,columnspan=2)
not_known_img=PhotoImage(file="wrong.png")
not_known_button=Button(image=not_known_img,highlightthickness=0,command=next_card)
not_known_button.grid(row=1,column=0)

known_image=PhotoImage(file="right.png")
known_button=Button(image=known_image,highlightthickness=0,command=is_known)
known_button.grid(row=1,column=1)

next_card()

window.mainloop()