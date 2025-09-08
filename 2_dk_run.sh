  docker run -d -it -p 4000:4000 \
  --name xungmi/litellm:v1 \
  -v $PWD:/app \
  --entrypoint /bin/bash \
  xungmi/litellm:v1
