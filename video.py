import cv2
import numpy as np
import util
import sys

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
        segmented_image = util.get_bodypix_image(frame)
        if segmented_image is not None:
            # Colorize the segmented image
            color_segmented_image = util.colorize_segmented_image(segmented_image)

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
