import cv2
import numpy as np
import util
import pyvirtualcam

def run(cam):

    curr_y = 300
    curr_x = 300
    inertia = 0.65
    zoom = 1/7.0
    # Initialize the webcam
    cap = cv2.VideoCapture(0)


    while True: 
        ret, frame = cap.read()
        if not ret:
            break

        #frame_flipped = cv2.flip(frame, 1)
        frame_flipped = frame
        outsize = (300, 600)
        outaspect = outsize[1] / outsize[0]
        

        # get the body map
        segmented_image = util.get_bodypix_image(frame_flipped)

        # find the center and std of the head
        # Assume the head pixels are labeled as 0 or 1 in the segmented image
        y_coords, x_coords = np.where((segmented_image == 1) | (segmented_image == 0))
        if len(x_coords) < 1000:
            center_x = frame.shape[1]/2
            center_y = frame.shape[0]/2
            std_dev_x = frame.shape[1]/2
            head_height = frame.shape[0]/2
        else:
            center_x = int(np.mean(x_coords))
            center_y = int(np.mean(y_coords))

            # Calculate standard deviation for x and y coordinates
            std_dev_x = np.std(x_coords)
            head_height = np.std(y_coords)

        curr_x = inertia*curr_x + (1-inertia)*center_x
        curr_y = inertia*curr_y + (1-inertia)*center_y
        aspect_ratio = outsize[0] / outsize[1]  # Calculate the target aspect ratio from outsize

        # Calculate the height of the crop based on head_height
        crop_height = head_height /zoom  # total height = 1 head above + 3 heads below


        # Determine top, bottom, left, right to maintain the aspect ratio
        top = int(max(curr_y - 2*crop_height, 0))
        bottom = int(min(curr_y + 3 * crop_height, frame.shape[0]))
        crop_width = int((bottom-top) * aspect_ratio)
        left = int(max(curr_x - crop_width // 2, 0))
        right = int(min(curr_x + crop_width // 2, frame.shape[1]))

        # Crop the frame
        cropped_frame = frame[top:bottom, left:right]
        cropped_frame = cv2.resize(cropped_frame, outsize)
        #cropped_frame = frame
        #cv2.circle(cropped_frame, (int(curr_x), int(curr_y)), radius=10, color=(0, 255, 0), thickness=2)

        # Display the cropped frame
        cv2.imshow('Cropped Head Frame', cropped_frame)
        
        # Send frame to virtual camera
        cam.send(cropped_frame)
        cam.sleep_until_next_frame()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    
    with pyvirtualcam.Camera(width=300, height=600, fps=20) as cam:
        run(cam)