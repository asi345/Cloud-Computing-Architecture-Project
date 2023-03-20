out = open('some_memcached_ip.txt', 'w')
with open('memcached_data.txt') as f:
    f.readline()
    line = f.readline().split()
    out.write('SOME_MAMCACHED_NAME="' + line[0] + '"\n')
    out.write('SOME_MEMCACHED_IP="' + line[5] + '"\n')
out.close()