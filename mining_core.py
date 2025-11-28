import hashlib
import json
import time
import threading
from typing import Dict, List
from sin_blockchain import Transaction, Block
from node_manager import NodeResourceManager

class MiningCore:
    def __init__(self, blockchain, node_manager: NodeResourceManager):
        self.blockchain = blockchain
        self.node_manager = node_manager
        self.mining = False
        self.miner_address = None
        self.mining_thread = None
        self.hashrate = 0
        self.blocks_mined = 0
        self.lock = threading.Lock()
    
    def set_miner_address(self, address: str):
        """Set the address to receive mining rewards"""
        self.miner_address = address
    
    def mine_block(self, mining_address: str) -> bool:
        """Mine a single block"""
        if not self.blockchain.transactions:
            print("No transactions to mine")
            return False
        
        if not mining_address:
            print("Miner address not set")
            return False
        
        # Get current difficulty
        difficulty = self.blockchain.difficulty
        
        # Create new block with pending transactions
        reward_transaction = Transaction(
            sender="0",  # System transaction
            recipient=mining_address,
            amount=self.blockchain.get_block_reward(),
            data={"type": "mining_reward"}
        )
        
        # Include reward transaction and pending transactions
        transactions_to_mine = [reward_transaction] + [tx for tx in self.blockchain.transactions if not self.blockchain.has_transaction(tx.transaction_id)]
        
        if len(transactions_to_mine) <= 1:  # Only reward transaction, no user transactions
            return False
        
        # Create new block
        new_block = Block(
            index=len(self.blockchain.chain),
            previous_hash=self.blockchain.get_latest_block().hash,
            timestamp=time.time(),
            transactions=transactions_to_mine
        )
        
        # Start mining
        start_time = time.time()
        target = "0" * difficulty
        nonce = 0
        
        # Use allocated resources to mine
        resource_multiplier = self.node_manager.get_reward_multiplier()
        
        while new_block.hash[:difficulty] != target:
            with self.lock:
                if not self.mining:
                    return False
            
            new_block.nonce = nonce
            new_block.hash = new_block.calculate_hash()
            nonce += 1
            
            # Adjust mining speed based on allocated resources
            time.sleep(0.001 / resource_multiplier)  # Faster with more resources
        
        end_time = time.time()
        mining_time = end_time - start_time
        self.hashrate = nonce / mining_time  # Hashes per second
        
        # Add block to chain
        self.blockchain.chain.append(new_block)
        
        # Update total supply
        self.blockchain.total_supply += self.blockchain.get_block_reward()
        
        # Clear pending transactions that were included
        with self.blockchain.lock:
            self.blockchain.transactions = [tx for tx in self.blockchain.transactions if not self.blockchain.has_transaction(tx.transaction_id)]
        
        self.blocks_mined += 1
        print(f"Block {new_block.index} mined successfully! Time: {mining_time:.2f}s, Hashrate: {self.hashrate:.2f} H/s")
        return True
    
    def start_mining(self, mining_address: str):
        """Start mining in a separate thread"""
        if self.mining:
            print("Mining is already running")
            return
        
        self.mining = True
        self.miner_address = mining_address
        
        def mining_loop():
            while self.mining:
                success = self.mine_block(mining_address)
                if not success:
                    time.sleep(1)  # Wait before trying again
        
        self.mining_thread = threading.Thread(target=mining_loop, daemon=True)
        self.mining_thread.start()
        print(f"Started mining with address: {mining_address}")
    
    def stop_mining(self):
        """Stop mining"""
        self.mining = False
        if self.mining_thread:
            self.mining_thread.join(timeout=2)
        print("Mining stopped")
    
    def get_mining_stats(self) -> Dict:
        """Get mining statistics"""
        return {
            "hashrate": self.hashrate,
            "blocks_mined": self.blocks_mined,
            "is_mining": self.mining,
            "miner_address": self.miner_address
        }