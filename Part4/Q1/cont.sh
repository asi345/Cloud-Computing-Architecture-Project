cd ~/Documents/Homeworks/ETH\ Zurich/Cloud\ Computing\ Architecture/Project/Part4/Q1
export KOPS_STATE_STORE=gs://cca-eth-2023-group-13-atinan
export PROJECT='gcloud config get-value project'
source node_vars.txt

gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$AGENT_NAME --zone europe-west3-a < ./stop_agent.sh
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$MEMCACHED_NAME --zone europe-west3-a < ./cont_memcached.sh

gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$AGENT_NAME --zone europe-west3-a < ./run_agent.sh &
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$MEASURE_NAME --zone europe-west3-a < ./run_measure.sh

gcloud compute scp ubuntu@$MEASURE_NAME:~/memcache-perf-dynamic/memcached_output.txt ./memcached_output.txt --zone europe-west3-a --ssh-key-file ~/.ssh/cloud-computing