import json
import sys
from datetime import datetime
import pandas as pd

time_format = '%Y-%m-%dT%H:%M:%SZ'
file = open(sys.argv[1], 'r')
# get run number from filename
run_number = sys.argv[1].split('_')[-1].split('.')[0]
assert run_number is not None, "Run number must be specified"
assert run_number.isdigit(), "Run number must be an integer"

json_file = json.load(file)

start_times = []
completion_times = []
jobs = []
for item in json_file['items']:
    name = item['status']['containerStatuses'][0]['name']
    if str(name) != "memcached":
        try:
            start_time = datetime.strptime(
                item['status']['containerStatuses'][0]['state']['terminated']['startedAt'],
                time_format)
            completion_time = datetime.strptime(
                item['status']['containerStatuses'][0]['state']['terminated']['finishedAt'],
                time_format)
            node = item['spec']['nodeName']
            job_time = completion_time - start_time

        except KeyError:
            print("Job {0} has not completed....".format(name))
            sys.exit(0)
    else:
        start_time = datetime.strptime(
            item['status']['containerStatuses'][0]['state']['running']['startedAt'],
            time_format)
        # no completion time for memcached
        completion_time = start_time
    jobs.append(str(name))
    start_times.append(start_time)
    completion_times.append(completion_time)


if len(start_times) != 8 and len(completion_times) != 8:
    print("You haven't run all the PARSEC jobs. Exiting...")
    sys.exit(0)

data = {'job': jobs,
        'start_time': start_times,
        'finish_time': completion_times
        }
df = pd.DataFrame.from_dict(data)
df.to_csv(f'runtime_jobs_{str(run_number)}.csv', index=False)

print("Total time: {0}".format(max(completion_times) - min(start_times)))
file.close()
