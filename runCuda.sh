docker run --gpus all -it --rm --net=host -v $(pwd):/app -w /app nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04 /bin/bash
