import pyautogui
import time

def print_coordinates():
    try:
        while True:
            x, y = pyautogui.position()
            print(f"X: {x}, Y: {y}")
            time.sleep(1)  # Adjust the sleep duration as needed
    except KeyboardInterrupt:
        print("Exiting program.")

if __name__ == "__main__":
    print("Press Ctrl+C to stop the program.")
    print_coordinates()
