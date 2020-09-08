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

Video source file: https://vanderbilt.app.box.com/file/217581007445?s=l9onxj3r7acb9zx7ig9ts3ztytvc83rl

Follow this video https://www.youtube.com/watch?v=CJ5G4GpqDy0&t=635s tutorial to set up kubernetes cluster.
Its easiest if the username on all the machines is the same, I used `ubuntu`.
I used openstack with floating external ips, in `admin.conf` the value of `server` needs to be changed to the ip of the floating ip of the first node. I think technically it can be any node with the master role, but I'm not sure. 
Additionally the `~/<>/kubespray/inventory/mycluster/hosts.yaml` needed to have the `ip` values updated to the corresponding floating ips. 

kubectl was installed using snap and I couldn't figure out where to copy the admin.conf file so that it would read it. So instead add add `export KUBECONFIG=/home/ubuntu/.kube/admin.conf` to your `~/.bashrc` so that running `kubectl get nodes` will be successful. 

Modifying the cluster: https://github.com/kubernetes-sigs/kubespray/blob/master/docs/nodes.md
```
ansible-playbook -i inventory/mycluster/hosts.yaml --become --become-user=root cluster.yml
ansible-playbook -e node=node4 -i inventory/mycluster/hosts.yaml --become --become-user=root remove-node.ym
ansible-playbook  -i inventory/mycluster/hosts.yaml --become --become-user=root facts.yml
ansible-playbook --limit=node4 -i inventory/mycluster/hosts.yaml --become --become-user=root scale.yml
```

docker container had no internet: https://development.robinwinslow.uk/2016/06/23/fix-docker-networking-dns/
