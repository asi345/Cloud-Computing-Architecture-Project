import docker
import json
import psutil
import subprocess
import time

from init_config import cores, images, threads, MAX_MEMORY
from scheduler_logger import Job, SchedulerLogger

class DockerContainerHandler:
    def __init__(self, logger: SchedulerLogger):
        """Initialize a Docker client and a logger."""
        self.client = docker.from_env()
        self.logger = logger
        self.containers = {}

    def create_container(self, name: str, cpu_period: int = 100000, cpu_quota: int = 10000) -> docker.models.containers.Container:
        """Create a Docker container with the specified name and configuration."""
        config = {
            "auto_remove": False,
            "command": f"./run -a run -S {'splash2x' if name == 'radix' else 'parsec'} -p {name} -i native -n {threads[name]}",
            "cpu_quota": cpu_quota,
            "cpu_period": cpu_period,
            "cpuset_cpus": cores[name],
            "detach": True,
            "image": images[name],
            "name": name,
        }
        container = self.client.containers.run(**config)
        self.logger.job_start(Job(container.name), initial_cores=cores[name].split(","), initial_threads=threads[name])
        container.reload()
        self.containers[container.name] = container
        return container

    def get_all_containers_resource_usage(self) -> dict:
        """Return the resource usage of all running Docker containers."""
        output = subprocess.getoutput('docker stats --no-stream')
        result = {}
        for line in output.splitlines()[1:]:
            line = line.split()
            result[line[1]] = {}
            result[line[1]]["CPU"] = float(line[2][:-1])
            result[line[1]]["MEM"] = line[3]
        return result

    def is_finished(self) -> bool:
        for container in list(self.containers.values()):
            container.reload()
            if container.status == "exited":
                self.remove_container(container)

        if not self.containers:
            self.logger.end()
            return True
        return False

    def pause_container(self, container: docker.models.containers.Container) -> bool:
        """Pause the given container if it is running."""
        if container == None:
            return False

        container.reload()
        if container.status in ["created", "running"]:
            container.pause()
            self.logger.job_pause(Job(container.name))
            return True

        return False

    def remove_container(self, container: docker.models.containers.Container) -> bool:
        """Removes the given container."""
        if container == None:
            return False

        container.reload()
        try:
            with open(f"logs/{container.name}.txt", "wb") as f:
                    f.write(container.logs())
            self.logger.job_end(Job(container.name))
            del self.containers[container.name]
            container.remove()
            return True
        except:
            with open(f"logs/{container.name}.txt", "wb") as f:
                    f.write(container.logs())
            self.logger.job_end(Job(container.name))
            del self.containers[container.name]
            container.remove(force=True)
            return True

    def remove_if_exited(self, container: docker.models.containers.Container) -> bool:
        """Removes the given container if it exited."""
        if container == None:
            return False

        container.reload()
        if container.status == "exited":
            try:
                with open(f"logs/{container.name}.txt", "wb") as f:
                    f.write(container.logs())
                self.logger.job_end(Job(container.name))
                del self.containers[container.name]
                container.remove()
                return True
            except:
                with open(f"logs/{container.name}.txt", "wb") as f:
                    f.write(container.logs())
                self.logger.job_end(Job(container.name))
                del self.containers[container.name]
                container.remove(force=True)
                return True

        return False

    def remove_all_exited(self):
        """Removes all exited containers."""
        for container in self.containers.values():
            self.remove_if_exited(container)
        return

    def remove_all(self):
        """Removes all containers."""
        for container in self.containers.values():
            self.remove_container(container)
        return

    def unpause_container(self, container: docker.models.containers.Container) -> bool:
        """Unpauses or starts the given container."""
        if container == None:
            return False

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

    def update_cpu_shares(self, container: docker.models.containers.Container, shares: float) -> docker.models.containers.Container:
        """Updates the allowed cpu shares of the given container. Valid share values are between 0 - #cores"""
        if container == None:
            return None

        container.reload()
        container.update(cpu_period = 100000, cpu_quota = int(shares * 100000))
        self.logger.custom_event(Job(container.name), f"cpu shares updated to {shares}")
        return container

    def update_cores(self, container: docker.models.containers.Container, cores: str) -> docker.models.containers.Container:
        """Updates the cpu affinity of the given container."""
        if container == None:
            return None

        container.reload()
        container.update(cpuset_cpus = cores)
        self.logger.update_cores(Job(container.name), cores.split(","))
        return container

    def update_memory_limit(self, container: docker.models.containers.Container, fraction: float) -> docker.models.containers.Container:
        """Updates memory usage limit of the given container."""
        output = subprocess.getoutput(['docker', 'stats', '--no-stream'])
        container.update(memswap_limit=-1, mem_limit=str(int(fraction * MAX_MEMORY * 1024)) + "m")
        return container


class MemcachedHandler:
    def __init__(self, logger: SchedulerLogger):
        self.pid = self.get_memcached_pid()
        self.process = psutil.Process(self.pid)
        self.logger = logger

    def get_memcached_pid(self):
        """Returns the memcached process."""
        while not subprocess.getoutput("pidof memcached"):
            time.sleep(0.05)
            print("Waiting for memcached to run.")

        self.logger.job_start(Job("memcached"))
        return int(subprocess.getoutput("pidof memcached"))

    def update_memcached_cores(self, cores):
        cmd = f"sudo taskset -acp {cores} {self.pid}"
        subprocess.run(cmd.split(" "), stderr=subprocess.STDOUT, stdout=subprocess.STDOUT)
        self.logger.update_cores(Job("memcached"))
        return

    def get_core_usage(self):
        """Returns cpu usage of the memcached process."""
        return self.process.cpu_percent()



if __name__ == "__main__":
    handler = DockerContainerHandler(SchedulerLogger())
    handler.create_container("dedup")
    handler.create_container("radix")
    handler.create_container("ferret")
    handler.create_container("freqmine")
    handler.create_container("canneal")
    handler.create_container("vips")
    handler.create_container("blackscholes")
    while not handler.is_finished():
        time.sleep(0.5)
        print(handler.get_all_containers_resource_usage())
