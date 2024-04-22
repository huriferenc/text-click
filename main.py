"""
TODO:
- 
"""

import sys
import tkinter as tk

import cv2
import numpy as np
import pyautogui
import pytesseract

CONFIG_FNAME = "config.txt"

SLEEP_TIME_SECONDS: int
TEXT_TO_FIND: list
TEXT_INDEX: int

root: tk.Tk

play_button: tk.Button
stop_button: tk.Button

is_playing = False


def main():
    global root, is_playing, play_button, stop_button

    try:
        init()

        root = tk.Tk()

        window_width = 400
        window_height = 250

        ###
        # Centering GUI
        ###
        # Gets the coordinates of the center of the screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        # Coordinates of the upper left corner of the window to make the window appear in the center
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        root.title("Text Clicker")

        play_button = tk.Button(root, text="Play", command=play, width=50, height=3)
        play_button.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        stop_button = tk.Button(root, text="Stop", command=stop, width=50, height=3)
        stop_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        # Detect texts on the screen
        root.after(SLEEP_TIME_SECONDS, detect_texts)

        root.mainloop()
    except Exception as e:
        print(e)
        sys.exit(1)


def init():
    global CONFIG_FNAME, SLEEP_TIME_SECONDS, TEXT_TO_FIND, TEXT_INDEX

    SLEEP_TIME_SECONDS = 30000  # 30 seconds

    TEXT_TO_FIND = []
    TEXT_INDEX = 0

    with open(CONFIG_FNAME, "r") as f:
        line = f.readline().rstrip()

        if is_integer(line):
            sleep_time = int(line)
            if sleep_time > 0:
                SLEEP_TIME_SECONDS = sleep_time * 1000
            line = f.readline().rstrip()

        while line:
            if len(line) > 0:
                TEXT_TO_FIND.append(line)

            line = f.readline().rstrip()

    if len(TEXT_TO_FIND) == 0:
        raise Exception("No config provided!")


def play():
    global is_playing, play_button

    print("Play")

    is_playing = True

    play_button.configure(text="Pause", command=pause)


def pause():
    global is_playing, play_button

    print("Pause")

    is_playing = False

    play_button.configure(text="Play", command=play)


def stop():
    print("Stop")

    sys.exit(0)


def detect_texts():
    global root, is_playing, SLEEP_TIME_SECONDS

    if is_playing:  # Only do this if the Stop button has not been clicked
        detect_text()

    # After SLEEP_TIME_SECONDS seconds, call detect_texts again (create a recursive loop)
    root.after(SLEEP_TIME_SECONDS, detect_texts)


def detect_text():
    global TEXT_TO_FIND, TEXT_INDEX

    # Get screen resolution
    screen_width, screen_height = pyautogui.size()

    # Create screenshot of the screen
    screenshot = pyautogui.screenshot()

    # Convert screenshot to OpenCV format
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Recognize text in the image
    data = pytesseract.image_to_data(gray_image, output_type="dict")

    box_num = len(data["level"])

    #!! image_marked = image.copy()
    click_position = (screen_width, screen_height)
    is_found = False
    for i in range(box_num):
        if TEXT_TO_FIND[TEXT_INDEX] in data["text"][i]:
            (x, y, w, h) = (
                data["left"][i],
                data["top"][i],
                data["width"][i],
                data["height"][i],
            )

            start = (x, y)

            if x < click_position[0]:
                click_position = start

            is_found = True

    # Click on the text
    if is_found:
        pyautogui.click(x=click_position[0], y=click_position[1])

    # Next text
    TEXT_INDEX = (TEXT_INDEX + 1) % len(TEXT_TO_FIND)


def is_integer(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    main()
