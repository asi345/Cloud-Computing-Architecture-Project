out = open('job_vars.txt', 'w')
with open('jobs.txt') as f:
    f.readline()
    line = f.readline().split()
    out.write('JOB_NAME="' + line[0] + '"\n')
out.close()