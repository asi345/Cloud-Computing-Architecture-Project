sudo apt update
sudo apt install -y memcached libmemcached-tools
sudo systemctl status memcached
source memcached_int_ip.txt
sudo sed -i -e "s/-m 64/-m 1024/" /etc/memcached.conf
sudo sed -i -e "s/-l 127.0.0.1/-l $MEMCACHED_INT_IP/" /etc/memcached.conf
sudo sed -i -e "s/-p 11211/-p 11211 -t 2/" /etc/memcached.conf
sudo systemctl restart memcached
sleep 10
sudo taskset -acp 0,1 $(pgrep memcached)
sleep 10
sudo systemctl status memcached
mkdir logs

sudo apt --yes install python3-pip
pip3 install psutil docker

sudo usermod -aG docker ubuntu

sudo docker pull anakli/cca:parsec_blackscholes
sudo docker pull anakli/cca:parsec_canneal
sudo docker pull anakli/cca:parsec_dedup
sudo docker pull anakli/cca:parsec_ferret
sudo docker pull anakli/cca:parsec_freqmine
sudo docker pull anakli/cca:splash2x_radix
sudo docker pull anakli/cca:parsec_vips