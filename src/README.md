
## Test 1: run test.py from separate container
```bash
cd <MODiCuM-Streaming>/src
docker-compose build
docker-compose up

# pulsar container: docker_pulsar_1, network: src_default
# MV2 image name: mv

# run the MV2 container
docker run -it --network src_default mv
# inside that container you can run the test script
cd /code/MV2
python3 test.py
```


## Test Executables
```bash
# setup everything
cd <MODiCuM-Streaming>/src
docker-compose build
docker-compose up


```