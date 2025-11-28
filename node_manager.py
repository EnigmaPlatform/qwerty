import psutil
import GPUtil
import os
import shutil
from typing import Dict, Tuple
import threading
import time

class NodeResourceManager:
    def __init__(self):
        self.cpu_usage = 0
        self.gpu_usage = 0
        self.ram_usage = 0
        self.disk_usage = 0
        self.cpu_limit = 0.5  # Default 50%
        self.gpu_limit = 0.5  # Default 50%
        self.ram_limit = 0.5  # Default 50%
        self.disk_limit = 0.5  # Default 50%
        self.lock = threading.Lock()
    
    def scan_resources(self) -> Dict:
        """Scan and return available system resources"""
        # CPU info
        cpu_count = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()
        
        # GPU info
        gpus = GPUtil.getGPUs()
        gpu_info = []
        for gpu in gpus:
            gpu_info.append({
                "id": gpu.id,
                "name": gpu.name,
                "memory_total": gpu.memoryTotal,
                "memory_used": gpu.memoryUsed,
                "memory_free": gpu.memoryFree,
                "driver": gpu.driver,
                "gpu_load": gpu.load,
                "memory_util": gpu.memoryUtil
            })
        
        # RAM info
        ram = psutil.virtual_memory()
        
        # Disk info
        disk = shutil.disk_usage("/")
        
        resources = {
            "cpu": {
                "count": cpu_count,
                "freq": cpu_freq._asdict() if cpu_freq else None,
                "usage": psutil.cpu_percent(interval=1)
            },
            "gpu": gpu_info,
            "ram": {
                "total": ram.total,
                "available": ram.available,
                "used": ram.used,
                "percent": ram.percent
            },
            "disk": {
                "total": disk.total,
                "free": disk.free,
                "used": disk.used
            }
        }
        
        return resources
    
    def set_resource_limits(self, cpu_percent: float, gpu_percent: float, 
                           ram_percent: float, disk_percent: float):
        """Set resource limits as percentages (0.1 to 0.8)"""
        if not 0.1 <= cpu_percent <= 0.8:
            raise ValueError("CPU percent must be between 0.1 and 0.8")
        if not 0.1 <= gpu_percent <= 0.8:
            raise ValueError("GPU percent must be between 0.1 and 0.8")
        if not 0.1 <= ram_percent <= 0.8:
            raise ValueError("RAM percent must be between 0.1 and 0.8")
        if not 0.1 <= disk_percent <= 0.8:
            raise ValueError("Disk percent must be between 0.1 and 0.8")
        
        with self.lock:
            self.cpu_limit = cpu_percent
            self.gpu_limit = gpu_percent
            self.ram_limit = ram_percent
            self.disk_limit = disk_percent
    
    def get_resource_usage(self) -> Dict:
        """Get current resource usage based on limits"""
        resources = self.scan_resources()
        
        # Calculate usage based on limits
        cpu_usage = resources["cpu"]["usage"] * self.cpu_limit
        ram_usage = resources["ram"]["percent"] * self.ram_limit
        
        # Calculate GPU usage if available
        gpu_usage = 0
        if resources["gpu"]:
            gpu_usage = sum([gpu["gpu_load"] for gpu in resources["gpu"]]) / len(resources["gpu"]) * self.gpu_limit
        
        # Calculate disk usage
        disk_usage = (resources["disk"]["used"] / resources["disk"]["total"]) * 100 * self.disk_limit
        
        return {
            "cpu_usage": cpu_usage,
            "gpu_usage": gpu_usage,
            "ram_usage": ram_usage,
            "disk_usage": disk_usage
        }
    
    def get_hashrate_contribution(self) -> float:
        """Calculate hashrate contribution based on allocated resources"""
        usage = self.get_resource_usage()
        
        # Base hashrate is proportional to resource allocation
        # Higher allocation = higher hashrate = higher reward potential
        base_hashrate = 100  # Base hashrate in MH/s
        resource_factor = (
            (usage["cpu_usage"] / 100) * 0.4 +  # CPU contributes 40%
            (usage["gpu_usage"] / 100) * 0.4 +  # GPU contributes 40%
            (usage["ram_usage"] / 100) * 0.1 +  # RAM contributes 10%
            (usage["disk_usage"] / 100) * 0.1   # Disk contributes 10%
        )
        
        return base_hashrate * resource_factor
    
    def get_reward_multiplier(self) -> float:
        """Calculate reward multiplier based on resource allocation"""
        usage = self.get_resource_usage()
        
        # Reward multiplier based on resource allocation
        resource_factor = (
            (usage["cpu_usage"] / 100) * 0.4 +  # CPU contributes 40%
            (usage["gpu_usage"] / 100) * 0.4 +  # GPU contributes 40%
            (usage["ram_usage"] / 100) * 0.1 +  # RAM contributes 10%
            (usage["disk_usage"] / 100) * 0.1   # Disk contributes 10%
        )
        
        # Ensure multiplier is between 0.1 and 1.0
        return max(0.1, min(1.0, resource_factor))
    
    def monitor_resources(self, interval: int = 10):
        """Continuously monitor resources"""
        while True:
            usage = self.get_resource_usage()
            self.cpu_usage = usage["cpu_usage"]
            self.gpu_usage = usage["gpu_usage"]
            self.ram_usage = usage["ram_usage"]
            self.disk_usage = usage["disk_usage"]
            time.sleep(interval)