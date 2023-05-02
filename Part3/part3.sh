cd ~/Documents/Homeworks/ETH\ Zurich/Cloud\ Computing\ Architecture/Project/Part3
export KOPS_STATE_STORE=gs://cca-eth-2023-group-13-atinan
export PROJECT=`gcloud config get-value project`
kops create -f ../cloud-comp-arch-project/part3.yaml
kops update cluster --name part3.k8s.local --yes --admin
kops validate cluster --wait 10m
kubectl get nodes -o wide > nodes_data.txt
python3 nodes_data.py
source node_vars.txt

kubectl label nodes $NODE_A2__NAME cca-project-nodetype=node-a-2core
kubectl label nodes $NODE_B4__NAME cca-project-nodetype=node-b-4core
kubectl label nodes $NODE_C8__NAME cca-project-nodetype=node-c-8core # use for nodeSelector, static assignment

#do the job schedulings here
#sh schedule.sh -j -n -t -c

kubectl get pods -o json > results.json
python3 get_time.py results.json > outputs.txt
kops delete cluster --name part3.k8s.local --yes