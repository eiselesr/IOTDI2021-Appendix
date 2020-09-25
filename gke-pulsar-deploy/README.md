
Install
```bash
git clone https://github.com/streamnative/charts.git
cd charts
PROJECT=modicum scripts/pulsar/gke_bootstrap_script.sh up
helm repo add streamnative https://charts.streamnative.io
./scripts/pulsar/prepare_helm_release.sh -n pulsar -k pulsar -c
helm install --set initialize=true pulsar streamnative/pulsar

# get IP info for access to the cluster
kubectl get service -n pulsar

```

Other
```bash
PROJECT=modicum scripts/pulsar/gke_bootstrap_script.sh down
kubectl get namespace
```