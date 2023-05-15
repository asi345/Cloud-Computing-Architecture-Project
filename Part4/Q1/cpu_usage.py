import psutil

for _ in range(40):
    print(psutil.cpu_percent(interval=5, percpu=True))