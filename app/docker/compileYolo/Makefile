build:
	sudo docker build \
	--network host \
	-t yolo .

run:
	sudo docker run -it \
        --network host \
        --mount type=bind,source="/home/ubuntu/projects/MODiCuM-Streaming/app/docker/compileYolo/output",target=/output \
        yolo