import requests
from io import BytesIO
import numpy as np
import cv2


def get_bodypix_image(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    files = {'image': BytesIO(buffer)}
    response = requests.post('http://localhost:5000/detect_faces', files=files)
    if response.status_code == 200:
        segmented_image = np.frombuffer(response.content, dtype=np.uint8)
        segmented_image = cv2.imdecode(segmented_image, cv2.IMREAD_GRAYSCALE)
        return segmented_image
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def colorize_segmented_image(segmented_image):
    num_body_parts = 256
    hue_distance_factor = 13

    # Create an array for hues including an entry for the -1 index
    hues = np.zeros(num_body_parts + 1, dtype=np.uint8)
    hues[1:] = (np.arange(num_body_parts) * hue_distance_factor) % 180  # Skip the first entry

    colors_hsv = np.zeros((num_body_parts + 1, 3), dtype=np.uint8)
    colors_hsv[1:, 0] = hues[1:]  # Hue
    colors_hsv[1:, 1] = 255  # Saturation
    colors_hsv[1:, 2] = 255  # Value

    # Set the color for -1 index to black
    colors_hsv[0, :] = [0, 0, 0]  # HSV for black is 0,0,0

    colors_rgb = cv2.cvtColor(np.expand_dims(colors_hsv, 0), cv2.COLOR_HSV2BGR)[0]

    # Increment all indices in segmented_image by 1 to map -1 to 0, 0 to 1, and so on.
    color_segmented_image = np.take(colors_rgb, segmented_image + 1, axis=0)

    return color_segmented_image