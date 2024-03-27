const express = require('express');
const tf = require('@tensorflow/tfjs-node-gpu'); // Ensure tfjs-node-gpu is installed and CUDA is properly set up
const bodyPix = require('@tensorflow-models/body-pix');
const multer = require('multer');

// Set TF_FORCE_GPU_ALLOW_GROWTH to true
process.env['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true';

const app = express();
const port = process.env.PORT || 5000; // Use PORT environment variable if available, else default to 5000

const upload = multer({ storage: multer.memoryStorage() });

let net;

async function loadModel() {
  try {
    const architecture = process.env.BODYPIX_ARCHITECTURE || 'MobileNetV1';
    const outputStride = process.env.BODYPIX_OUTPUT_STRIDE ? parseInt(process.env.BODYPIX_OUTPUT_STRIDE, 10) : 16;
    const multiplier = process.env.BODYPIX_MULTIPLIER ? parseFloat(process.env.BODYPIX_MULTIPLIER) : 1.0;
    const quantBytes = process.env.BODYPIX_QUANT_BYTES ? parseInt(process.env.BODYPIX_QUANT_BYTES, 10) : 2;

    net = await bodyPix.load({
      architecture: architecture,
      outputStride: outputStride,
      multiplier: multiplier,
      quantBytes: quantBytes
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
    
    const segmentationTensor = tf.tensor2d(segmentation.data, [segmentation.height, segmentation.width], 'int32');
    const segmentation3D = segmentationTensor.expandDims(-1);
    
    const pngBuffer = await tf.node.encodePng(segmentation3D);
    
    res.writeHead(200, {
      'Content-Type': 'image/png',
      'Content-Disposition': 'attachment; filename=segmentation.png'
    });
    res.end(Buffer.from(pngBuffer), 'binary');
    
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
