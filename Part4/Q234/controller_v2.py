import docker
import json
import psutil
import subprocess
import time
import signal
import sys
import functools

from handlers import DockerContainerHandler, MemcachedHandler
from init_config import cores, images, threads, weights
from scheduler_logger import SchedulerLogger, Job

ORDER = ["radix", "ferret", "freqmine", "canneal", "vips", "blackscholes", "dedup"]

class Scheduler:
    def __init__(self):
        self.logger = SchedulerLogger()
        self.parsec_handler = DockerContainerHandler(self.logger)
        self.memcached_handler = MemcachedHandler(self.logger)
        self.current_job = 0
        self.parsec_handler.create_container(ORDER[0])
        self.allow_second_core = False

    def schedule_next_job(self):
        if self.parsec_handler.containers[ORDER[self.current_job]].status == "exited":
            self.parsec_handler.remove_container(self.parsec_handler.containers[ORDER[self.current_job]])
            self.current_job += 1
            if not self.is_finished():
                cont = self.parsec_handler.create_container(ORDER[self.current_job])
                if self.allow_second_core:
                    self.parsec_handler.update_cores(cont, "1,2,3")
        return
    
    def update_state(self):
        if not self.allow_second_core:
            util = sum(list(psutil.cpu_percent(interval=None, percpu=True))[:2])
            if util < 100.0:
                self.memcached_handler.update_memcached_cores("0")
                self.allow_second_core = True
                cont = self.parsec_handler.containers[ORDER[self.current_job]]
                self.parsec_handler.update_cores(cont, "1,2,3")
        elif self.allow_second_core:
            util = sum(list(psutil.cpu_percent(interval=None, percpu=True))[:1])
            if util > 80.0:
                self.memcached_handler.update_memcached_cores("0,1")
                self.allow_second_core = False
                cont = self.parsec_handler.containers[ORDER[self.current_job]]
                self.parsec_handler.update_cores(cont, "2,3")
    
    def is_finished(self):
        if self.current_job == 7:
            self.logger.end()
            return True 
        
        return False 



if __name__ == "__main__":
    scheduler = Scheduler()

    while not scheduler.is_finished():
        scheduler.schedule_next_job()
        scheduler.update_state()
        #print(f"Currently running {ORDER[scheduler.current_job]}")
        time.sleep(0.2)
        
    print("Finished")
