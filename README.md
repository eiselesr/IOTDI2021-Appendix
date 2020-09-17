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

* Follow this video tutorial https://www.youtube.com/watch?v=CJ5G4GpqDy0&t=635s or this guide https://github.com/kubernetes-sigs/kubespray/blob/master/docs/setting-up-your-first-cluster.md to set up kubernetes cluster.




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

```cat <<EOF | kubectl apply -f -
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

Note from Mike: Remove all docker containers and images 
Note from Scott: Don't do this on nodes managed by kubernetes
```bash
# Delete every Docker containers
# Must be run first because images are attached to containers
docker rm -f $(docker ps -a -q)

# Delete every Docker image
docker rmi -f $(docker images -q)
```
