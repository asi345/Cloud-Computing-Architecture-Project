sudo apt update
sudo apt install -y memcached libmemcached-tools
sudo systemctl status memcached
source memcached_int_ip.txt
sudo sed -i -e "s/-m 64/-m 1024/" /etc/memcached.conf
sudo sed -i -e "s/-l 127.0.0.1/-l $MEMCACHED_INT_IP/" /etc/memcached.conf
sudo sed -i -e "s/-p 11211/-p 11211 -t 1/" /etc/memcached.conf
sudo systemctl restart memcached
sleep 10
sudo taskset -acp 0 $(pgrep memcached)
sleep 10
sudo systemctl status memcached
mkdir logs

sudo apt --yes --force-yes install python3-pip
pip3 install psutil
python3 cpu_usage.py > usage.txt &