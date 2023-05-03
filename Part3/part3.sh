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
sudo sh schedule_memcached.sh -n node-c-8core -t 2

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
sudo sh schedule_parsec.sh -j blackscholes -n node-c-8core -t 6 -c 1,2,3,4,5,6,7 &
sudo sh schedule_parsec.sh -j canneal -n node-c-8core -t 4 -c 1,2,3,4,5,6,7 &
sudo sh schedule_parsec.sh -j radix -n node-c-8core -t 4 -c 1,2,3,4,5,6,7 &
sudo sh schedule_parsec.sh -j dedup -n node-a-2core -t 4 &
sudo sh schedule_parsec.sh -j ferret -n node-a-2core -t 4 &
sudo sh schedule_parsec.sh -j vips -n node-b-4core -t 4 &
sudo sh schedule_parsec.sh -j freqmine -n node-b-4core -t 4 &

sleep 300

gcloud compute scp ubuntu@$MEASURE_NAME:~/memcache-perf-dynamic/memcached_output.txt ./memcached_output.txt --zone europe-west3-a --ssh-key-file ~/.ssh/cloud-computing

kubectl get jobs > job_names.txt
python3 jobs.py
source job_vars.txt
kubectl logs $(kubectl get pods --selector=job-name=$BLACKSCHOLES_NAME --output=jsonpath='{.items[*].metadata.name}') > blackscholes_logs.txt
kubectl logs $(kubectl get pods --selector=job-name=$CANNEAL_NAME --output=jsonpath='{.items[*].metadata.name}') > canneal_logs.txt
kubectl logs $(kubectl get pods --selector=job-name=$DEDUP_NAME --output=jsonpath='{.items[*].metadata.name}') > dedup_logs.txt
kubectl logs $(kubectl get pods --selector=job-name=$FERRET_NAME --output=jsonpath='{.items[*].metadata.name}') > ferret_logs.txt
kubectl logs $(kubectl get pods --selector=job-name=$FREQMINE_NAME --output=jsonpath='{.items[*].metadata.name}') > freqmine_logs.txt
kubectl logs $(kubectl get pods --selector=job-name=$RADIX_NAME --output=jsonpath='{.items[*].metadata.name}') > radix_logs.txt
kubectl logs $(kubectl get pods --selector=job-name=$VIPS_NAME --output=jsonpath='{.items[*].metadata.name}') > vips_logs.txt

kubectl get pods -o json > results.json
python3 get_time.py results.json > outputs.txt
#kops delete cluster --name part3.k8s.local --yes 