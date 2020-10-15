# MV2 Source Code

## 1. Running Pulsar

For simulations we require Pulsar as well as the Presto SQL server (part of Pulsar). We can run these
two ways, either we can download pulsar and run standalone or we can run in docker. Note that 
there are some bugs with Presto SQL with docker Pulsar that is currently being addressed by
the pulsar team.

### 1.1: Pulsar Standalone 
```bash
cd <MODiCuM-Streaming>
wget https://archive.apache.org/dist/pulsar/pulsar-2.6.1/apache-pulsar-2.6.1-bin.tar.gz
cd apache-pulsar-2.6.1

# start pulsar standalone
bin/pulsar-daemon start standalone

# start Presto SQL worker
bin/pulsar sql-worker start
```

### 1.2: Pulsar Docker
```bash
# run pulsar
docker run -it \
  --name pulsar_standalone \
  -p 6650:6650 \
  -p 8080:8080 \
  -p 8081:8081 \
  --mount source=pulsardata,target=/pulsar/data \
  --mount source=pulsarconf,target=/pulsar/conf \
  apachepulsar/pulsar-all:2.6.1 \
  bin/pulsar-daemon start standalone

# start Presto SQL worker
docker exec -d name bash bin/pulsar sql-worker start
```

## 2. Run Simulation/Test

The simulation test script is in <MODiCuM-Streaming>/src/tests/test.py. To change the number of 
suppliers and consumers change the NUM_SUPPLIERS and NUM_CUSTOMERS parameters at the top of the script.
SIMNUM is a parameter that will automatically change tenant names so that you don't need to restart
pulsar each time you run a similation, just make sure you use a new SIMNUM for a fresh simulation.

```bash
cd <MODiCuM-Streaming>/src
python tests/test.py
```

## 3. Get Simulation Results

There are two ways to get simulation results. For the log use the print-consumer to print to screen.
Make sure that the "topic" parameter in the following command matches "logger_topic" in MV2/cfg.py.

Log:
```bash
cd <MODiCuM-Streaming>/sandbox/print-consumer
python app.py \
    --pulsar_url "pulsar://localhost:6650" \
    --tenant "public" \
    --namespace "default" \
    --topic "logger" \
    --timeout "none"
```

The second way to get results is to use the jupyter notebook in <MODiCuM-Streaming>/notebooks/pulsar_sql.ipynb
to query topics to see all messages on that topic.


## 4. Game

Constraints
* b x lam > all costs
* pi_s * lam > pi_se * lam + pi_a

Input params
* b: benefit to customer - distribution
* lam: number of inputs in a job - distribution
* pi_s: payout to supplier - distribution 

Dependent params (function)
* pi_se: cost to process a service input - pi_s * pi_se_sf
* pi_mi: payout to mediator for mediating - pi_s * pi_mi_sf
* pi_sd: security deposit for supplier - (01 - 03) * scaling_factor
* pi_cd: security deposit for customer - pi_cg * scaling factor

Static params
* pi_se_sf: scaling factor 
* pi_mi_sf: scaling factor
* pi_cg: cost to customer for generating n inputs
* pi_cc: cost to customer for commiting n inputs to bc
* pi_a: payout to allocator
* pi_m: payout to mediator
* pi_sc: cost to supplier for sending n inputs to bc
* pr: penalty rate

Questions:

* Do we have to keep track of mediator in the game?
* Single allocator ok?

