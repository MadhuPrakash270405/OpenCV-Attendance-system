import os
import cv2
from screeninfo import get_monitors
from icecream import ic
from datetime import datetime

# Get the current time in 12-hour format
current_time = datetime.now().strftime("%I:%M:%S %p")
ic.configureOutput(prefix=f"[{current_time}]", includeContext=True)


def get_screen_resolution():
    monitor = get_monitors()[0]
    ic(f"Screen resolution: {monitor.width}x{monitor.height}")
    return monitor.width, monitor.height


screen_width, screen_height = get_screen_resolution()


# Move the window to the calculated coordinates
def move_window_to_center(window_title, image):
    # Get the width and height of the image window
    window_width = image.shape[1]
    window_height = image.shape[0]
    # Calculate the top-left corner coordinates to center the window
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    cv2.moveWindow(window_title, x, y)


def show_image(image_title, image):
    cv2.imshow(image_title, image)
    # Move the window to the calculated coordinates
    move_window_to_center(image_title, image)
    cv2.waitKey(0)  # Wait until a key is pressed
    cv2.destroyAllWindows()  # Close all OpenCV windows


def read_image(filename):
    # Read an image
    image = cv2.imread(filename)
    # Display the image in a window
    show_image("Image", image)
    return image


def write_image(filename):
    # Read an image
    image = read_image(filename)
    # Save the image
    cv2.imwrite(f"output_{filename}.jpg", image)


def resize_image(filename):
    image = cv2.imread(filename)
    screen_width, screen_height = get_screen_resolution()
    # Resize the image to fit the screen
    aspect_ratio = image.shape[1] / float(image.shape[0])
    if (aspect_ratio * screen_height) > screen_width:
        # Fit to width
        new_width = screen_width
        new_height = int(screen_width / aspect_ratio)
    else:
        # Fit to height
        new_height = screen_height
        new_width = int(screen_height * aspect_ratio)
    resized_image = cv2.resize(image, (new_width, new_height))
    show_image("Resized Image", resized_image)
    return resized_image


def grayscale_image(filename):
    resized_image = resize_image(filename)
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    show_image("Grayscale Image", gray_image)


def gaussian_blurring(filename):
    resized_image = resize_image(filename)
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    show_image("Grayscale Image", gray_image)


if __name__ == "__main__":
    filename = os.path.join("./resources/images/01.jpg")
    grayscale_image(filename)
