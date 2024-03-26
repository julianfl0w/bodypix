import cv2
import requests
import numpy as np
from io import BytesIO

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

    # Encode the flipped frame to JPEG format
    _, buffer = cv2.imencode('.jpg', frame_flipped)
    files = {'image': BytesIO(buffer)}  # Ensure this matches the field expected by your server

    # Send the frame to the Flask API
    response = requests.post('http://localhost:5000/detect_faces', files=files)

    # Check if the request was successful
    if response.status_code == 200:
        # The server returns a PNG buffer of the segmented image
        # Ensure segmented_image is a single-channel image with body part indices
        segmented_image = np.frombuffer(response.content, dtype=np.uint8)
        segmented_image = cv2.imdecode(segmented_image, cv2.IMREAD_GRAYSCALE)

        # Number of unique body parts expected in the segmentation
        num_body_parts = 256

        # Hue distance factor - adjust as needed
        hue_distance_factor = 13

        # Generate hues in HSV color space with controlled distance
        hues = (np.arange(num_body_parts) * hue_distance_factor) % 180

        colors_hsv = np.zeros((num_body_parts, 3), dtype=np.uint8)
        colors_hsv[:, 0] = hues  # Hue
        colors_hsv[:, 1] = 255  # Saturation
        colors_hsv[:, 2] = 255  # Value

        # Convert from HSV to RGB
        colors_rgb = cv2.cvtColor(np.expand_dims(colors_hsv, 0), cv2.COLOR_HSV2BGR)[0]

        # Apply the color map to the segmented image
        color_segmented_image = np.take(colors_rgb, segmented_image, axis=0)

        # Display the color-coded segmented image
        cv2.imshow('Segmented Image', color_segmented_image)
    else:
        print(f"Error: {response.status_code} - {response.text}")

    # Display the original flipped frame
    cv2.imshow('Webcam Feed', frame_flipped)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
