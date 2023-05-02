cd ~/Documents/Homeworks/ETH\ Zurich/Cloud\ Computing\ Architecture/Project/Part3
export KOPS_STATE_STORE=gs://cca-eth-2023-group-13-atinan
export PROJECT=`gcloud config get-value project`
kops create -f ../cloud-comp-arch-project/part3.yaml
kops update cluster --name part3.k8s.local --yes --admin
kops validate cluster --wait 10m
kubectl get nodes -o wide > nodes_data.txt
python3 nodes_data.py
source node_vars.txt

kubectl label nodes $NODE_A2_NAME cca-project-nodetype=node-a-2core
kubectl label nodes $NODE_B4_NAME cca-project-nodetype=node-b-4core
kubectl label nodes $NODE_C8_NAME cca-project-nodetype=node-c-8core # use for nodeSelector, static assignment

#do the memcached job scheduling here
#sh schedule_memcached.sh -n -t -c

sleep 60
kubectl get service some-memcached-11211
kubectl get pods -o wide > memcached_data.txt
python3 memcached_data.py
source memcached_ip.txt

gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$AGENT_A_NAME --zone europe-west3-a < ./init_memcached.sh &
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$AGENT_B_NAME --zone europe-west3-a < ./init_memcached.sh &
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$MEASURE_NAME --zone europe-west3-a < ./init_memcached.sh

gcloud compute scp ./memcached_ip.txt ubuntu@$MEASURE_NAME:~/ --zone europe-west3-a --ssh-key-file ~/.ssh/cloud-computing
gcloud compute scp ./node_vars.txt ubuntu@$MEASURE_NAME:~/ --zone europe-west3-a --ssh-key-file ~/.ssh/cloud-computing

gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$AGENT_A_NAME --zone europe-west3-a < ./run_agent_a.sh &
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$AGENT_B_NAME --zone europe-west3-a < ./run_agent_b.sh &
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$MEASURE_NAME --zone europe-west3-a < ./run_measure.sh &

#do parsec schedulings here
#sh schedule_parsec.sh -j -n -t -c

gcloud compute scp ubuntu@$MEASURE_NAME:~/memcache-perf-dynamic/memcached_output.txt ./memcached_output.txt --zone europe-west3-a --ssh-key-file ~/.ssh/cloud-computing

kubectl get pods -o json > results.json
python3 get_time.py results.json > outputs.txt
kops delete cluster --name part3.k8s.local --yes 