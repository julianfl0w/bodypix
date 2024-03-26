import cv2
import requests
import numpy as np
from io import BytesIO
import util

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame vertically
    # frame_flipped = cv2.flip(frame, 1)
    #frame_flipped = frame
    # Flip the frame horizontally
    frame_flipped = cv2.flip(frame, 1)

    segmented_image = util.get_bodypix_image(frame_flipped)
 
    # Apply the color map to the segmented image
    color_segmented_image = util.colorize_segmented_image(segmented_image)

    # Display the color-coded segmented image
    cv2.imshow('Segmented Image', color_segmented_image)

    # Display the original flipped frame
    cv2.imshow('Webcam Feed', frame_flipped)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
