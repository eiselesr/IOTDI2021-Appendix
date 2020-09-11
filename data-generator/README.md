How to run this application

```bash
NAME=${PWD##*/}
docker run -it --rm --name docker-client-1 "$NAME:1.0"

#docker run -it --rm --name docker-client docker-client:1.0
```