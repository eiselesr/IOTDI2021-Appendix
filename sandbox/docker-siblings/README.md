
# build and run "parent" 
```bash
# build
cd <sandbox/docker-siblings>
bash build.sh 
# now the parent image is built and is called docker-siblings

# run the container
NAME=${PWD##*/}
docker run -it --rm --name docker-sibling-master-1 -v /var/run/docker.sock:/var/run/docker.sock "$NAME:1.0"

# now we are in the docker-sibling-master-1 container
# run the hellow-world container (this will be the example sibling container)
docker run hello-world
```

# open a second terminal on HOST machine
```bash
docker ps -a
# you should see the hello-world image used in a container, this proves we 
# can create a sibling container
```