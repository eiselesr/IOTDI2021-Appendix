# MODiCuM outsourcing online computation to surplus resources

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
