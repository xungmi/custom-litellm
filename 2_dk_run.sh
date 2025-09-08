  docker run -d -it -p 4000:4000 \
  --name litellm_effiaiv1 \
  -v $PWD:/app \
  --entrypoint /bin/bash \
  litellm_effiai:v1
