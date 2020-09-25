
## 1. Install Google Cloud Command Line
This  actually was really easy. I just followed this tutorial https://cloud.google.com/sdk/docs/quickstart

## 2. Create a Kubernetes cluster on Google Cloud

docs: https://github.com/streamnative/charts

```bash
cd <MODiCuM-Streaming>/gke-pulsar-deploy
git clone https://github.com/streamnative/charts.git
cd charts
PROJECT=modicum scripts/pulsar/gke_bootstrap_script.sh up
```

## 3. Install Pulsar on the Cluster

docs: https://github.com/streamnative/charts

```bash
cd <MODiCuM-Streaming>/gke-pulsar-deploy
helm repo add streamnative https://charts.streamnative.io
./scripts/pulsar/prepare_helm_release.sh -n pulsar -k pulsar -c
helm install --set initialize=true pulsar streamnative/pulsar
```

## 4. Get IP info, use proxy to connect to cluster
```bash
kubectl get service -n pulsar
```

## Other
```bash
PROJECT=modicum scripts/pulsar/gke_bootstrap_script.sh down
kubectl get namespace
```