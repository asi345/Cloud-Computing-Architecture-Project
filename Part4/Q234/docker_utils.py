import docker
from scheduler_logger import SchedulerLogger, Job
import psutil
from jobs import images, threads, cores

class ContainerHandler:
    def __init__(self):
        self.client = docker.from_env()
        self.logger = SchedulerLogger()
        self.containers = []

    def create_container(self, name, cpu_period=100000, cpu_quota=100000):
        config = {
            "name": name,
            "cpuset_cpus": cores,
            "image": images[name],
            "command": f"./bin/parsecmgmt -a run -p {cores[name]} -i native -n {threads[name]}",
            "detach": True,
            "auto_remove": False
        }
        container = self.client.containers.run(**config)
        self.logger.job_start(Job(container.name), initial_cores=cores.split(","), initial_threads=num_threads)
        container.reload()
        return container

    def remove_if_exited(self, container):
        if container == None:
            return False 
        
        container.reload()
        if container.status == "exited":
            try:
                container.remove()
                self.logger.job_end(Job(container.name))
                return True
            except:
                container.remove(force=True)
                self.logger.job_end(Job(container.name))
                return True
            
        return False

    def remove(self, container):
        if container == None:
            return None
        
        container.reload()
        try:
            container.remove()
            self.logger.job_end(Job(container.name))
            return True
        except:
            container.remove(force=True)
            self.logger.job_end(Job(container.name))
            return True

        
    def pause(self, container):
        if container == None:
            return None 
        
        container.reload()
        if container.status == "running":
            container.pause()
            self.logger.job_pause(Job(container.name))
            return True 
        
        return False
    
    def unpause(self, container):
        if container == None:
            return None 
        
        container.reload()
        if container.status == "paused":
            container.unpause()
            self.logger.job_unpaused(Job(container.name))
            return True
        elif container.status == "created":
            container.start()
            self.logger.job_unpause(Job(container.name))
            return True 
        
        return False
    
    def update_cpu_shares(self, container, shares): # shares between 0-400
        if container == None:
            return None 
        
        container.reload()
        container.update(cpu_quota = shares * 100000)

    def update_cores(self, container, cores="0,1,2,3"):
        if container == None:
            return None
        
        container.reload()
        container.update(cpuset_cpus = cores)



if __name__ == "__main__":
    handler = ContainerHandler()
    cont = handler.create_container("dedup")
    while not handler.remove_if_exited(cont):
        print(psutil.cpu_percent(interval=0.1, percpu=True))
