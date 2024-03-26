# bodypix docker

## Example


## Introduction
This Docker image encapsulates the @tensorflow-models/body-pix Javascript library, running as a REST API on nodejs. 

Files included as a POST request will be returned as images representing the bodypix numbers for body parts:

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

## Run
```bash
docker run --gpus all -p 5000:5000 julianfl0w/bodypix:latest
```

then, run either webcam.py or video.py. These files make requests to the 5000 endpoint