# BodyPix Segmentation Service
This service provides an API for segmenting human bodies in images using the BodyPix model. It allows clients to upload an image, and returns a segmented version of the image with different body parts highlighted.

This Docker image encapsulates the @tensorflow-models/body-pix Javascript library, running as a REST API on nodejs. 

Files included as a POST request will be returned as images representing the bodypix numbers for body parts (below)

## Example
[output.webm](https://github.com/julianfl0w/bodypix/assets/8158655/205291a3-6148-4b7b-8654-f1af37639b14)

## Quick Start
### Standard run 
npm install
node bodypix.js

Then, if you want to do face tracking
python face_track.py
Or, to see the segmentation
python webcam.py

### Docker run (server)
```bash
docker run --gpus all -p 5000:5000 julianfl0w/bodypix:latest
```

After starting the service, use `webcam.py` or `video.py` to send requests to the server at port 5000:

- `webcam.py` processes images in real-time using your computer's webcam. It captures live video feed, segments it using the BodyPix model, and displays the results on-the-fly.
- `video.py` processes a pre-recorded video file. You need to pass the path to the video file as the first argument when running the script. It reads the video frame by frame, sends each frame for segmentation, and can optionally save or display the output.


## API Endpoints

### POST `/detect_faces`

Uploads an image for body part segmentation and returns an image highlighting different body parts.

#### Request

- **Content-Type:** `multipart/form-data`
- **Body:** A single image file under the key `image`.

#### Response

- **Content-Type:** `image/png`
- The response body contains a PNG image of the segmented body parts.

#### Example CURL Request

```bash
curl -X POST -F "image=@path_to_your_image.jpg" http://localhost:5000/detect_faces -o segmented_image.png
```

## Body Part Numbers

| Part Id | Part Name          |
|---------|--------------------|
| -1      | (no body part)     |
| 0       | leftFace           |
| 1       | rightFace          |
| 2       | rightUpperLegFront |
| 3       | rightLowerLegBack  |
| 4       | rightUpperLegBack  |
| 5       | leftLowerLegFront  |
| 6       | leftUpperLegFront  |
| 7       | leftUpperLegBack   |
| 8       | leftLowerLegBack   |
| 9       | rightFeet          |
| 10      | rightLowerLegFront |
| 11      | leftFeet           |
| 12      | torsoFront         |
| 13      | torsoBack          |
| 14      | rightUpperArmFront |
| 15      | rightUpperArmBack  |
| 16      | rightLowerArmBack  |
| 17      | leftLowerArmFront  |
| 18      | leftUpperArmFront  |
| 19      | leftUpperArmBack   |
| 20      | leftLowerArmBack   |
| 21      | rightHand          |
| 22      | rightLowerArmFront |
| 23      | leftHand           |
