sudo sed -i -e "s/-p 11211 -t 2/-p 11211 -t 2/" /etc/memcached.conf
sudo systemctl restart memcached
sleep 10
sudo taskset -acp 0,1 $(pgrep memcached)
sleep 10
sudo systemctl status memcached
python3 cpu_usage.py > usage.txt &