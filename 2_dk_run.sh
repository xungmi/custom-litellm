docker run -d -it --gpus all \
  --name litellm_effiaiv1 \
  -v $PWD:/app \
  --entrypoint /bin/bash \
  litellm_effiai:v1