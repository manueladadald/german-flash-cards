import random
import time
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
try:
    data = pandas.read_csv("data/words_to_learn.csv")
    to_learn = data.to_dict(orient="records")
except FileNotFoundError:
    data = pandas.read_csv("data/german_words.csv")
    to_learn = data.to_dict(orient="records")
finally:
    current_card = {}


# ---------------------------- GET RANDOM WORD ------------------------------- #
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    german_word = current_card["German"].lower()
    canvas.itemconfig(bg_image, image=card_front_img)
    canvas.itemconfig(language, fill="black", text="German")
    canvas.itemconfig(card_word, fill="black", text=german_word)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    english_word = current_card["English"].lower()
    canvas.itemconfig(bg_image, image=card_back_img)
    canvas.itemconfig(language, fill="white", text="English")
    canvas.itemconfig(card_word, fill="white", text=english_word)


# ---------------------------- SAVE PROGRESS ------------------------------- #
def save_progress():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)

card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
bg_image = canvas.create_image(400, 263, image=card_front_img)
language = canvas.create_text(400, 150, fill="black", font=("Courier", 30, "italic"))
card_word = canvas.create_text(400, 263, fill="black", font=("Courier", 50, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

right = PhotoImage(file="images/right.png")
right_button = Button(image=right, highlightthickness=0, bg=BACKGROUND_COLOR, command=save_progress)
right_button.grid(column=1, row=1)

wrong = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong, highlightthickness=0, bg=BACKGROUND_COLOR, command=next_card)
wrong_button.grid(column=0, row=1)

next_card()

window.mainloop()
