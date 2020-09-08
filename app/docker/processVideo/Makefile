build:
	sudo docker build \
	--network host \
	-t process_video .

run:
	sudo docker run -it \
        --network host \
        --mount type=bind,source="/home/ubuntu/projects/MODiCuM-Streaming/app/video",target=/input \
        process_video