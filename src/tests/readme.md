shell 1: run pulsar
```bash
cd <MODiCuM-Streaming>/src
docker rm -f $(docker ps -a -q)
docker volume rm $(docker volume ls -q)
docker-compose up
```

shell 2: run logger consumer
```bash
cd <MODiCuM-Streaming>/sandbox/print-consumer
python app.py \
    --pulsar_url "pulsar://localhost:6650" \
    --tenant "public" \
    --namespace "default" \
    --topic "logger" \
    --timeout "none"

persistent://s1/rand_nums/27032e0e-5232-4b59-beb9-994e4e304b35

python app.py \
    --pulsar_url "pulsar://localhost:6650" \
    --tenant "s1" \
    --namespace "rand_nums" \
    --topic "27032e0e-5232-4b59-beb9-994e4e304b35" \
    --timeout "none" \
    --subscription_name "test3"
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
    --service_name "rand_nums" \
    --num_windows "3" \
    --num_messages "15"
```
