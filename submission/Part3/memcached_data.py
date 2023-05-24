out = open('memcached_ip.txt', 'w')
with open('memcached_data.txt') as f:
    f.readline()
    line = f.readline().split()
    out.write('MEMCACHED_IP="' + line[5] + '"\n')
out.close()