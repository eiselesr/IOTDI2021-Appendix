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
tar -xzvf apache-pulsar-2.6.1-bin.tar.gz
cd apache-pulsar-2.6.1

# start pulsar 
rm -rf data
bin/pulsar-daemon start standalone

# to shutdown pulsar
bin/pulsar-daemon stop standalone

# Start Presto
bin/pulsar sql-worker start

# to shutdown Presto
bin/pulsar sql-worker stop
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


