build:
	sudo docker build \
	--network host \
	-t detect .

run:
	sudo docker run -it \
        --network host \
        --mount type=bind,source="/home/ubuntu/projects/MODiCuM-Streaming/app/video/output",target=/input \
        detect