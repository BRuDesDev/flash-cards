from tkinter import *
from pandas import *
from random import choice
from os import path

# ---------------  GENERATE DATAFRAME AS DICT   -------------------- #


# ---------------   CONSTANTS  -------------------- #
BACKGROUND_COLOR = "#B1DDC6"

current_card = {}
to_learn = {}


# ---------------   FUNCTIONS   -------------------- #
def check_for_data():
    global to_learn
    exists = path.exists('data/words_to_learn.csv')
    if exists:
        print("Existing Data Found")
        data = read_csv('data/words_to_learn.csv')
        to_learn = data.to_dict(orient='records')
    else:
        print("No Data Found")
        data = read_csv('data/french_words.csv')
        to_learn = data.to_dict(orient='records')

        dataframe = DataFrame(to_learn)
        dataframe.to_csv("data/words_to_learn.csv", index=False)
        print("CSV successfully created.")


def remove_card():
    data = read_csv("data/words_to_learn.csv")
    words_to_learn = data.to_dict(orient='records')
    words_to_learn.remove(current_card)
    print(f"{current_card} removed from stack! {len(words_to_learn)} left!")
    # saving data
    dataframe = DataFrame(words_to_learn)
    dataframe.to_csv('data/words_to_learn.csv', index=False)
    next_card()


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(to_learn)

    canvas.itemconfig(card_img, image=card_front_img)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=current_card["French"], fill="black")
    window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_img, image=card_back_img)


# ---------------   UI  -------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)
# ---------------   CARD CANVAS  -------------------- #
canvas = Canvas(width=800, height=526)

card_back_img = PhotoImage(file="images/card_back.png")
card_front_img = PhotoImage(file="images/card_front.png")
# Capturing the Canvas Img
card_img = canvas.create_image(400, 263, image=card_front_img)
title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

# # ---------------   BUTTONS  -------------------- #
right = PhotoImage(file="images/right.png")
right_btn = Button(image=right, highlightthickness=0, command=remove_card)
right_btn.grid(column=1, row=1)

wrong = PhotoImage(file="images/wrong.png")
wrong_btn = Button(image=wrong, highlightthickness=0, command=next_card)
wrong_btn.grid(column=0, row=1)


# ---------------  MAIN  -------------------- #

check_for_data()


next_card()

window.mainloop()