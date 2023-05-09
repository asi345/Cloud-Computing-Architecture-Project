sudo apt update
sudo apt install -y memcached libmemcached-tools
sudo systemctl status memcached
source memcached_int_ip.txt
sudo sed -i -e "s/-m 64/-m 1024/" /etc/memcached.conf
sudo sed -i -e "s/-l 127.0.0.1/-l $MEMCACHED_INT_IP/" /etc/memcached.conf
sudo systemctl restart memcached
sleep 10
sudo systemctl status memcached
#rewrite the changes to go back to original
sudo sed -i -e "s/-m 1024/-m 64/" /etc/memcached.conf
sudo sed -i -e "s/-l $MEMCACHED_INT_IP/-l 127.0.0.1/" /etc/memcached.conf