./bin/pulsar-admin topics delete sh2/traffic_detection/output
./bin/pulsar-admin topics delete sh3/traffic_detection/output

./bin/pulsar-admin namespaces delete sh2/traffic_detection
./bin/pulsar-admin namespaces delete sh3/traffic_detection

./bin/pulsar-admin tenants delete sh2
./bin/pulsar-admin tenants delete sh3



./bin/pulsar-admin topics delete public/default/allocation_topic
./bin/pulsar-admin topics delete public/default/customer_offers
./bin/pulsar-admin topics delete public/default/supply_offers


