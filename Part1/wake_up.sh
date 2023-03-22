#gsutil mb gs://cca-eth-2023-group-13-atinan/
export KOPS_STATE_STORE=gs://cca-eth-2023-group-13-atinan
cd ~/.ssh
ssh-keygen -t rsa -b 4096 -f cloud-computing
export PROJECT=`gcloud config get-value project`
cd ~/Documents/Homeworks/ETH\ Zurich/Cloud\ Computing\ Architecture/Project/Part1
#cd to parent folder of cloud-comp-arch-project
kops create -f cloud-comp-arch-project/part1.yaml
kops create secret --name part1.k8s.local sshpublickey admin -i ~/.ssh/cloud-computing.pub
kops update cluster --name part1.k8s.local --yes --admin
kops validate cluster --wait 10m
kubectl get nodes -o wide > nodes_data.txt
python3 node_data.py
source node_ip.txt
kubectl create -f cloud-comp-arch-project/memcache-t1-cpuset.yaml
kubectl expose pod some-memcached --name some-memcached-11211 --type LoadBalancer --port 11211 --protocol TCP
sleep 60
kubectl get service some-memcached-11211
kubectl get pods -o wide > memcached_data.txt
python3 memcache_data.py
source some_memcached_ip.txt
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$AGENT_NAME --zone europe-west3-a < ./init_vm.sh &
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$MEASURE_NAME --zone europe-west3-a < ./init_vm.sh