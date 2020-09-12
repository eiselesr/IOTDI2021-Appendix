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

Setup Kubernetes cluster:

* Video source file: https://vanderbilt.app.box.com/file/217581007445?s=l9onxj3r7acb9zx7ig9ts3ztytvc83rl
* if /usr/bin/python fails: https://www.toptechskills.com/ansible-tutorials-courses/how-to-fix-usr-bin-python-not-found-error-tutorial/

* Follow this video https://www.youtube.com/watch?v=CJ5G4GpqDy0&t=635s tutorial to set up kubernetes cluster.
* Its easiest if the username on all the machines is the same, I used `ubuntu`.
* I used openstack with floating external ips, in `admin.conf` the value of `server` needs to be changed to the ip of the floating ip of the first node. I think technically it can be any node with the master role, but I'm not sure. 
* Additionally the `~/<>/kubespray/inventory/mycluster/hosts.yaml` needed to have the `ip` values updated to the corresponding floating ips. 

* kubectl was installed using snap and I couldn't figure out where to copy the admin.conf file so that it would read it. So instead add add `export KUBECONFIG=/home/ubuntu/.kube/admin.conf` to your `~/.bashrc` so that running `kubectl get nodes` will be successful. 

* Modifying the cluster: https://github.com/kubernetes-sigs/kubespray/blob/master/docs/nodes.md
```
ansible-playbook -i inventory/mycluster/hosts.yaml --become --become-user=root cluster.yml
ansible-playbook -e node=node4 -i inventory/mycluster/hosts.yaml --become --become-user=root remove-node.ym
ansible-playbook  -i inventory/mycluster/hosts.yaml --become --become-user=root facts.yml
ansible-playbook --limit=node4 -i inventory/mycluster/hosts.yaml --become --become-user=root scale.yml
```

* docker container had no internet: https://development.robinwinslow.uk/2016/06/23/fix-docker-networking-dns/

* test setup (specifically the network): https://github.com/kubernetes-sigs/kubespray/blob/master/docs/setting-up-your-first-cluster.md

Getting Dashboard to work
* `wget https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0/aio/deploy/recommended.yaml`. Then replace 'namespace: dashboard-kubernetes` with 'namespace: kube-system' because it needs to be in the same namespace to see the nodes. (This may be wrong, and only the token needs to be in the right namespace)
* replace namespace again: https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md
* use kubectl port forwarding https://github.com/kubernetes/dashboard/tree/master/docs/user/accessing-dashboard#kubectl-port-forward
* TODO https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/#deploying-containerized-applications


Note from Mike: Remove all docker containers and images 
```bash
# Delete every Docker containers
# Must be run first because images are attached to containers
docker rm -f $(docker ps -a -q)

# Delete every Docker image
docker rmi -f $(docker images -q)
```