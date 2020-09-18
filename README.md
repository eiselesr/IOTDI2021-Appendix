# MODiCuM outsourcing online computation to surplus resources

Prerequisites

Docker: https://docs.docker.com/engine/install/ubuntu/#installation-methods
```
sudo apt-get update

sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
    
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo apt-key fingerprint 0EBFCD88

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

```

Download repository
```
sudo apt-get install -y git-lfs
git lfs install
git clone https://github.com/scope-lab-vu/MODiCuM-Streaming.git
```

App

* Video source file: https://vanderbilt.app.box.com/file/217581007445?s=l9onxj3r7acb9zx7ig9ts3ztytvc83rl
* docker container had no internet, : added `--network host` to docker commands

Tips for setting up Kubernetes cluster:

* Its easiest if the username on all the machines is the same, I used `ubuntu`.
* if /usr/bin/python fails: https://www.toptechskills.com/ansible-tutorials-courses/how-to-fix-usr-bin-python-not-found-error-tutorial/
* I used openstack with floating external ips, in `admin.conf` the value of `server` needs to be changed to the ip of the floating ip of the first node. I think technically it can be any node with the master role, but I'm not sure. 
    * Additionally the `~/<>/kubespray/inventory/mycluster/hosts.yaml` needed to have the `ip` values updated to the corresponding floating ips. 
* I installed kubectl using snap and I couldn't figure out where to copy the admin.conf file so that it would read it. So instead add `export KUBECONFIG=/home/ubuntu/.kube/admin.conf` to your `~/.bashrc` so that running `kubectl get nodes` will be successful. 


Setting up Kubernetes cluster:

* Follow this video tutorial https://www.youtube.com/watch?v=CJ5G4GpqDy0&t=635s or this guide https://github.com/kubernetes-sigs/kubespray/blob/master/docs/setting-up-your-first-cluster.md or this one https://kubespray.io/#/ to set up kubernetes cluster.

1. copy public key to `~/.ssh/authoized_keys` on remote nodes; `ssh-copy-id -i [identity file] [user]@ip
1. modify `/etc/sudoers` file on targets to add line `ubuntu ALL=(ALL:ALL) NOPASSWD: ALL` so we don't need sudo access
1. `cp -rfp inventory/sample inventory/mycluster`
1. save target ips to environment variable `declare -a IPS=(192.168.222.111 192.168.222.101 192.168.222.102 192.168.222.103 192.168.222.104)`
1. create `[kubespray]/inventory/mycluster/hosts.yaml `CONFIG_FILE=inventory/mycluster/hosts.yaml python3 contrib/inventory_builder/inventory.py ${IPS[@]}`
1. modify each instance of "node1, node2, etc" in `[kubespray]/inventory/mycluster/hosts.yaml` to match hostname of target machines, or else it will rename the hosts to node1, node2, etc.
1. `[kubespray]/inventory/mycluster/group_vars/k8s-cluster/addons.yml` uncomment `metrics_server_enabled: true`
1. `[kubespray]/inventory/mycluster/group_vars/k8s-cluster/k8s-cluster.yml` uncomment and set to true `kubeconfig_localhost: true`
1. `ansible-playbook -i inventory/mycluster/hosts.yaml -u $USERNAME -b --become --become-user=root -v --private-key=~/.ssh/id_rsa cluster.yml`
1. `ansible-playbook -i inventory/mycluster/hosts.yaml  --private-key=~/.ssh/isislab -u ubuntu  --become --become-user=root cluster.yml`
1. edit `~/.bashrc` to add `export KUBECONFIG=/home/ubuntu/.kube/admin.conf`
1. `cp [kubespray]/inventory/isislab/mycluster/admin.conf ~/.kube/`
1. `kubectl get nodes` (might have to open new shell session... or reboot(?) for .`bashrc` to take efftect.
1. `kubectl -n kube-system  get services`
1. `kubectl top nodes` check that metric collection is working
1. `kubectl get namespaces` doesn't modity anything just for satisfying curiosity

For dashboard try these:
1. `kubectl port-forward -n kube-system  service/kubernetes-dashboard 8080:443`
1. `http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#!/login`
1. create a sample user https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md
    1. replace every occurance of `kubernetes-dashboard` with `kube-system`
1. paste token into login




* Modifying the cluster: https://github.com/kubernetes-sigs/kubespray/blob/master/docs/nodes.md
```
ansible-playbook -i inventory/mycluster/hosts.yaml --become --become-user=root cluster.yml
ansible-playbook -e node=node4 -i inventory/mycluster/hosts.yaml --become --become-user=root remove-node.ym
ansible-playbook  -i inventory/mycluster/hosts.yaml --become --become-user=root facts.yml
ansible-playbook --limit=node4 -i inventory/mycluster/hosts.yaml --become --become-user=root scale.yml
```





Getting Dashboard to work
* `wget https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0/aio/deploy/recommended.yaml`. Then replace 'namespace: dashboard-kubernetes` with 'namespace: kube-system' because it needs to be in the same namespace to see the nodes. (This may be wrong, and only the token needs to be in the right namespace)
* replace namespace again: https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md
* use kubectl port forwarding https://github.com/kubernetes/dashboard/tree/master/docs/user/accessing-dashboard#kubectl-port-forward
    * `kubectl port-forward -n kube-system  service/kubernetes-dashboard 8080:443`
* TODO https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/#deploying-containerized-applications


Create token for accessing dashboard. 

```
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kube-system
EOF

cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kube-system
EOF
```
`kubectl -n kube-system describe secret $(kubectl -n kube-system  get secret | grep admin-user | awk '{print $1}')`

Note from Mike: Remove all docker containers and images 

Note from Scott: Don't do this on nodes managed by kubernetes
```bash
# Delete every Docker containers
# Must be run first because images are attached to containers
docker rm -f $(docker ps -a -q)

# Delete every Docker image
docker rmi -f $(docker images -q)
```


ERRORS
```
fatal: [isislab21 -> 129.59.234.231]: FAILED! => {"attempts": 4, "changed": true, "cmd": ["/usr/bin/docker", "pull", "docker.io/calico/node:v3.15.2"], "delta": "0:00:00.366135", "end": "2020-09-17 20:46:03.241613", "msg": "non-zero return code", "rc": 1, "start": "2020-09-17 20:46:02.875478", "stderr": "Error response from daemon: Get https://registry-1.docker.io/v2/calico/node/manifests/v3.15.2: unauthorized: incorrect username or password", "stderr_lines": ["Error response from daemon: Get https://registry-1.docker.io/v2/calico/node/manifests/v3.15.2: unauthorized: incorrect username or password"], "stdout": "", "stdout_lines": []}
```
