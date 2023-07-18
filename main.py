'''
TODO:
- open app by process id
'''

import time
import cv2
import numpy as np
import pyautogui
import pytesseract

SLEEP_TIME_SECONDS = 30

TEXT_TO_FIND = []
TEXT_INDEX = 0


def detect_text():
    # Get screen resolution
    screen_width, screen_height = pyautogui.size()

    # Create screenshot of the screen
    screenshot = pyautogui.screenshot()

    # Convert screenshot to OpenCV format
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Recognize text in the image
    data = pytesseract.image_to_data(gray_image, output_type='dict')

    boxNum = len(data['level'])

    #!! image_marked = image.copy()
    click_position = (screen_width, screen_height)
    is_found = False
    for i in range(boxNum):
        if TEXT_TO_FIND[TEXT_INDEX] in data['text'][i]:
            (x, y, w, h) = (data['left'][i], data['top']
                            [i], data['width'][i], data['height'][i])

            start = (x, y)
            #!! end = (x + w, y + h)

            #!! # Draw box
            #!! cv2.rectangle(image_marked, start, end, (0, 255, 0), 2)

            if x < click_position[0]:
                click_position = start

            is_found = True

    # Click on the text
    if is_found:
        pyautogui.click(x=click_position[0], y=click_position[1])

    # Next text
    TEXT_INDEX = (TEXT_INDEX+1) % len(TEXT_TO_FIND)

    #!! # Save images
    #!! cv2.imwrite('desktop.png', image)
    #!! cv2.imwrite('desktop_gray.png', gray_image)
    #!! cv2.imwrite('desktop_marked.png', image_marked)

    #!! # Display images
    #!! cv2.imshow("desktop", image)
    #!! cv2.imshow("desktop_gray", gray_image)
    #!! cv2.imshow("desktop_marked", image_marked)

    #!! # Close images
    #!! cv2.waitKey(0)
    #!! cv2.destroyAllWindows()


def is_integer(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def main():
    global TEXT_TO_FIND, TEXT_INDEX, SLEEP_TIME_SECONDS

    # Specify text
    # if len(sys.argv) > 1:
    #     if is_integer(sys.argv[1]):
    #         SLEEP_TIME_SECONDS = int(sys.argv[1])
    #         if len(sys.argv[2:]) > 0:
    #             TEXT_TO_FIND = sys.argv[2:]
    #     else:
    #         TEXT_TO_FIND = sys.argv[1:]
    # else:
    #     print("No text provided!")
    #     # exit()

    with open("text.txt", "r") as f:
        line = f.readline().rstrip()

        if is_integer(line):
            sleep_time = int(line)
            if sleep_time > 0:
                SLEEP_TIME_SECONDS = sleep_time
            line = f.readline().rstrip()

        while line:
            if len(line) > 0:
                TEXT_TO_FIND.append(line)

            line = f.readline().rstrip()

    if len(TEXT_TO_FIND) == 0:
        print("No text provided!")
        return

    while True:
        detect_text()
        time.sleep(SLEEP_TIME_SECONDS)  # Sleep for X seconds


if __name__ == "__main__":
    main()
