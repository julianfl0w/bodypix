import cv2
import requests
import numpy as np
from io import BytesIO

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
import numpy as np
import cv2

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

def process_video(input_video_filename, output_video_filename):
    # Open the input video
    cap = cv2.VideoCapture(input_video_filename)
    if not cap.isOpened():
        print(f"Error: Unable to open video file {input_video_filename}")
        return

    # Get input video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    downscale = 1
    # Define the codec and create VideoWriter object for the output
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_filename, fourcc, fps, (int(frame_width*2*downscale), int(frame_height*downscale)))

    while cap.isOpened():
        ret, frame = cap.read()
        
        # Calculate new dimensions
        new_width = int(frame.shape[1] * downscale)
        new_height = int(frame.shape[0] * downscale)
        
        # Resize the frame
        frame = cv2.resize(frame, (new_width, new_height))
        
        if not ret:
            break

        # Get the bodypix image
        segmented_image = get_bodypix_image(frame)
        if segmented_image is not None:
            # Colorize the segmented image
            color_segmented_image = colorize_segmented_image(segmented_image)

            # Resize the color_segmented_image to match the frame's size
            color_segmented_image_resized = cv2.resize(color_segmented_image, (new_width, new_height))

            # Concatenate the frame and the color_segmented_image side by side
            combined_frame = np.hstack((frame, color_segmented_image_resized))

            # Show the combined frame
            cv2.imshow('Processed Frame', combined_frame)

            # Write the combined frame to the output file
            out.write(combined_frame)

        # Wait for a key press with a timeout set to match the frame rate
        if cv2.waitKey(int(1000/fps)) & 0xFF == ord('q'):  # Press 'q' to quit early
            break

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Processing completed. Output saved to {output_video_filename}")

# Example usage
input_video = sys.argv[1]
output_video = 'example.mp4'
process_video(input_video, output_video)
