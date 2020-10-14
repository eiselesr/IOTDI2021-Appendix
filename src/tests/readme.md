1a. start pulsar - docker:
```bash
cd <MODiCuM-Streaming>/src
docker rm -f $(docker ps -a -q)
docker volume rm $(docker volume ls -q)

docker build --tag "pulsar_standalone_image" -f Dockerfile .
docker run -it \
  --name pulsar_standalone \
  -p 6650:6650 \
  -p 8080:8080 \
  -p 8081:8081 \
  --mount source=pulsardata,target=/pulsar/data \
  --mount source=pulsarconf,target=/pulsar/conf \
  pulsar_standalone_image \
  bin/pulsar standalone
```

1b. start pulsar - standalone
```bash
cd <pulsar>
bin/pulsar-daemon start standalone
bin/pulsar sql-worker start

# to stop
bin/pulsar sql-worker stop
bin/pulsar-daemon stop standalone
```


shell 2: run logger consumer
```bash
cd <MODiCuM-Streaming>/sandbox/print-consumer
python app.py \
    --pulsar_url "pulsar://localhost:6650" \
    --tenant "public" \
    --namespace "default" \
    --topic "logger2" \
    --timeout "none"
```

shell 3: run allocator
```bash
cd <MODiCuM-Streaming>/src
python bin/app_allocator.py
```

shell 4: run verifier
```bash
cd <MODiCuM-Streaming>/src
python bin/app_verifier.py --tenant "v1"
```

shell 5: run supplier 1
```bash
cd <MODiCuM-Streaming>/src
python bin/app_supplier.py \
    --tenant "s1" \
    --behavior "correct" 
```

shell 6: run supplier 2
```bash
cd <MODiCuM-Streaming>/src
python bin/app_supplier.py \
    --tenant "s2" \
    --behavior "correct" 
```

shell 7: run customer 1
```bash
cd <MODiCuM-Streaming>/src
python bin/app_customer.py \
    --tenant "c1" \
    --replicas "2" \
    --service_name "rand_nums" 
```
