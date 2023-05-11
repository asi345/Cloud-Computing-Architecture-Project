sudo sed -i -e "s/-p 11211 -t 1/-p 11211 -t 1/" /etc/memcached.conf
sudo systemctl restart memcached
sleep 10
sudo taskset -acp 1 $(pgrep memcached)
sleep 10
sudo systemctl status memcached