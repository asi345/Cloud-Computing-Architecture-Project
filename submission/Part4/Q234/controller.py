import docker
import json
import psutil
import subprocess
import time
import signal
import sys

from handlers import DockerContainerHandler, MemcachedHandler
from init_config import cores, images, threads, weights
from scheduler_logger import SchedulerLogger, Job
class Scheduler:
    def __init__(self):
        self.logger = SchedulerLogger()
        self.running_containers = 7
        self.parsec_handler = DockerContainerHandler(self.logger)
        self.memcached_handler = MemcachedHandler(self.logger)
        self.start_jobs()
        self.weights = weights
        self.parsec_shares = 2.0
        self.memcached = 1.8
        self.set_parsec_shares(2.0)

    def start_jobs(self):
        for name in images.keys():
            self.parsec_handler.create_container(name)

    def compute_next_shares(self):
        memcached_util = self.memcached_handler.get_core_usage()
        total_util = psutil.cpu_percent(interval = None)

    def set_parsec_shares(self, shares):
        total_weight = sum([self.weights[key] for key in self.parsec_handler.containers.keys()])
        self.current_parsec_shares = shares
        for container in self.parsec_handler.containers.values():
            container.reload()
            self.parsec_handler.update_cpu_shares(container, shares * self.weights[container.name] / total_weight)
        return

if __name__ == "__main__":
    scheduler = Scheduler()
    def signal_handler(signum, frame):
        for container in scheduler.parsec_handler.containers:
            scheduler.parsec_handler.remove_container(container)
        sys.exit(0)

    while not scheduler.parsec_handler.is_finished():
        scheduler.set_parsec_shares(2.0)
        time.sleep(0.25)
    print("Finished")
