Download and run pulsar
```bash
cd <MODiCuM-Streaming>
wget https://archive.apache.org/dist/pulsar/pulsar-2.6.1/apache-pulsar-2.6.1-bin.tar.gz
# unzip
cd apache-pulsar-2.6.1
mkdir connectors
cd connectors
curl -o "pulsar-io-data-generator-2.6.1.nar" "https://archive.apache.org/dist/pulsar/pulsar-2.6.1/connectors/pulsar-io-data-generator-2.6.1.nar"

cd ..
bin/pulsar-daemon start standalone
bin/pulsar sql-worker start
```

Generate some data
```bash
./bin/pulsar-admin sources create --name generator --destinationTopicName generator_test --source-type data-generator
```

Test it: see notebook in <MODiCuM-Streaming>/notebooks/presto_sql.ipynb