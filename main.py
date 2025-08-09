import cv2
from numpy import array
from datetime import timedelta
from keyboard import is_pressed
from multiprocessing import Process
from time import sleep, perf_counter
from pyautogui import screenshot, click
from pytesseract import image_to_string, pytesseract

pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def capture_text(region):
    image_hsv = cv2.cvtColor(array(screenshot(region=region)), cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(image_hsv, array([0,0,200]), array([0,0,255]))
    text = image_to_string(mask, config ="--psm 10")

    return text

def time_to_timedelta(time_str):
    seconds, milliseconds = map(int, time_str.split(':'))
    return timedelta(seconds=seconds, milliseconds=milliseconds)

def compare_times(inp_time, ref_time):
    inp_delta = time_to_timedelta(inp_time)
    ref_delta = time_to_timedelta(ref_time)
    
    return inp_delta <= ref_delta

def keep_page_alive():
    while True:
        sleep(15)
        click(1500, 300)

def main():
    avg_run_time_total = 0
    avg_run_counter = 0

    process = Process(target=keep_page_alive)
    process.start()

    while True:
        start_time = perf_counter()

        if is_pressed('esc'):
            print(f"Average Run Time (MS): {avg_run_time_total / avg_run_counter * 1000:.3f}")
            process.terminate()
            exit()

        screen_text = capture_text((800, 285, 270, 70))

        try:
            # print(screen_text)
            result = compare_times(screen_text, "53:50")

            if result:
                print("Click Now")
                click(940,500)
        except ValueError:
            continue
        finally:
            avg_run_counter += 1
            avg_run_time_total += perf_counter() - start_time

if __name__ == "__main__":
    main()
