import os
import pickle
import json
import time
from typing import Any, Dict, List
from sin_blockchain import Transaction

class DistributedStorage:
    def __init__(self, storage_path: str = "./distributed_storage"):
        self.storage_path = storage_path
        self.nodes = {}  # Node ID -> Node info
        self.data_shards = {}  # Data ID -> List of shard locations
        self.node_capacities = {}  # Node ID -> Capacity info
        self.network_stats = {
            "total_nodes": 0,
            "active_nodes": 0,
            "total_storage": 0,
            "used_storage": 0
        }
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_path, exist_ok=True)
    
    def register_node(self, node_id: str, capacity_info: Dict):
        """Register a new node in the network"""
        self.nodes[node_id] = {
            "id": node_id,
            "capacity": capacity_info,
            "last_seen": time.time(),
            "status": "active"
        }
        self.node_capacities[node_id] = capacity_info
        self.network_stats["total_nodes"] += 1
        self.network_stats["active_nodes"] += 1
    
    def store_data_shard(self, data_id: str, shard_data: Any, storing_node: str):
        """Store a data shard on a specific node"""
        # Serialize data
        shard_file = os.path.join(self.storage_path, f"{data_id}_{storing_node}.dat")
        with open(shard_file, 'wb') as f:
            pickle.dump(shard_data, f)
        
        # Update shard locations
        if data_id not in self.data_shards:
            self.data_shards[data_id] = []
        self.data_shards[data_id].append({
            "node_id": storing_node,
            "shard_path": shard_file,
            "stored_at": time.time()
        })
        
        # Update network stats
        self.network_stats["used_storage"] += len(pickle.dumps(shard_data))
    
    def retrieve_data_shard(self, data_id: str, node_id: str) -> Any:
        """Retrieve a data shard from a specific node"""
        for shard_info in self.data_shards.get(data_id, []):
            if shard_info["node_id"] == node_id:
                shard_file = shard_info["shard_path"]
                if os.path.exists(shard_file):
                    with open(shard_file, 'rb') as f:
                        return pickle.load(f)
        return None
    
    def get_network_statistics(self) -> Dict:
        """Get network statistics"""
        total_capacity = sum(
            node_info["capacity"]["disk"]["total"] 
            for node_info in self.nodes.values()
        )
        
        self.network_stats.update({
            "total_capacity": total_capacity,
            "active_nodes": sum(1 for node in self.nodes.values() if node["status"] == "active")
        })
        
        return self.network_stats
    
    def get_node_data_distribution(self) -> Dict:
        """Get data distribution across nodes"""
        distribution = {}
        for node_id in self.nodes:
            distribution[node_id] = {
                "shards_stored": len([shard for shards in self.data_shards.values() 
                                    for shard in shards if shard["node_id"] == node_id]),
                "storage_used": sum(
                    os.path.getsize(shard["shard_path"]) 
                    for shards in self.data_shards.values() 
                    for shard in shards 
                    if shard["node_id"] == node_id and os.path.exists(shard["shard_path"])
                )
            }
        return distribution