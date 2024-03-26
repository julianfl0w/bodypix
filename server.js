process.env['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true';

const express = require('express');
const tf = require('@tensorflow/tfjs-node-gpu'); // Ensure tfjs-node-gpu is installed and CUDA is properly set up
const bodyPix = require('@tensorflow-models/body-pix');
const multer = require('multer');

const app = express();
const port = 5000;

const upload = multer({ storage: multer.memoryStorage() });

let net;

async function loadModel() {
  try {
    net = await bodyPix.load({
      architecture: 'ResNet50',
      outputStride: 4,
      multiplier: 1.0,
      quantBytes: 2
    });
    console.log('BodyPix model loaded');
  } catch (error) {
    console.error('Failed to load the BodyPix model:', error);
  }
}

loadModel();

app.post('/detect_faces', upload.single('image'), async (req, res) => {
  if (!req.file) {
    return res.status(400).send('No image file uploaded.');
  }

  try {
    const imgTensor = tf.node.decodeImage(req.file.buffer);
    const segmentation = await net.segmentPersonParts(imgTensor, {
      flipHorizontal: false,
      internalResolution: 'full',
      segmentationThreshold: 0.5
    });
    
    // Create a tensor from the entire segmentation data array
    const segmentationTensor = tf.tensor2d(segmentation.data, [segmentation.height, segmentation.width], 'int32');
    const segmentation3D = segmentationTensor.expandDims(-1);
    
    // Convert the full segmentation tensor to a PNG buffer
    const pngBuffer = await tf.node.encodePng(segmentation3D);
    
    // Send the PNG buffer as a response
    res.writeHead(200, {
      'Content-Type': 'image/png',
      'Content-Disposition': 'attachment; filename=segmentation.png'
    });
    res.end(Buffer.from(pngBuffer), 'binary');
    
    // Dispose of tensors to free up memory
    tf.dispose([imgTensor, segmentationTensor, segmentation3D]);
  
  } catch (error) {
    console.error(error);
    if (!res.headersSent) {
      res.status(500).send('Error processing image');
    }
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
