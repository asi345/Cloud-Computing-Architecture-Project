cd ~/Documents/Homeworks/ETH\ Zurich/Cloud\ Computing\ Architecture/Project/Part4/Q1
export KOPS_STATE_STORE=gs://cca-eth-2023-group-13-atinan
export PROJECT='gcloud config get-value project'
kops create -f ../../cloud-comp-arch-project/part4.yaml
kops update cluster --name part4.k8s.local --yes --admin
kops validate cluster --wait 10m
kubectl get nodes -o wide > nodes_data.txt
python3 nodes_data.py
source node_vars.txt

echo MEMCACHED_INT_IP=\"$MEMCACHED_INT_IP\" > memcached_int_ip.txt
gcloud compute scp ./memcached_int_ip.txt ubuntu@$MEMCACHED_NAME:~/ --zone europe-west3-a --ssh-key-file ~/.ssh/cloud-computing
#send scheduler files to memcached server
#gcloud compute scp ./ ubuntu@$MEMCACHED_NAME:~/ --zone europe-west3-a --ssh-key-file ~/.ssh/cloud-computing
gcloud compute scp ./node_vars.txt ubuntu@$MEASURE_NAME:~/ --zone europe-west3-a --ssh-key-file ~/.ssh/cloud-computing

gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$AGENT_NAME --zone europe-west3-a < ./init_memcached.sh &
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$MEASURE_NAME --zone europe-west3-a < ./init_memcached.sh
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$MEMCACHED_NAME --zone europe-west3-a < ./install_memcached.sh

gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$AGENT_NAME --zone europe-west3-a < ./run_agent.sh &
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$MEASURE_NAME --zone europe-west3-a < ./run_measure.sh