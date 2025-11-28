import hashlib
import json
import time
import threading
import random
import ecdsa
from ecdsa import SigningKey, VerifyingKey, SECP256k1
from typing import List, Dict, Optional
import base64

class Block:
    def __init__(self, index: int, previous_hash: str, timestamp: float, transactions: List['Transaction'], nonce: int = 0, hash: str = None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.hash = hash or self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate the block's hash using SHA-256"""
        block_string = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int):
        """Mine the block with the given difficulty"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

class Wallet:
    def __init__(self):
        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()
        self.address = self.generate_address()
    
    def generate_address(self) -> str:
        """Generate a Bitcoin-like address from public key"""
        # Convert public key to bytes
        public_key_bytes = self.public_key.to_string()
        
        # Double SHA256 of public key
        sha256_1 = hashlib.sha256(public_key_bytes).digest()
        sha256_2 = hashlib.sha256(sha256_1).digest()
        
        # Take first 20 bytes (RIPEMD-160 equivalent)
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256_2)
        hash160 = ripemd160.digest()
        
        # Add version byte (0x00 for mainnet)
        versioned_payload = b'\x00' + hash160
        
        # Double SHA256 for checksum
        checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
        
        # Combine and encode as base58
        full_payload = versioned_payload + checksum
        address = self.base58_encode(full_payload)
        
        return address
    
    def base58_encode(self, data: bytes) -> str:
        """Encode bytes in Base58 format similar to Bitcoin"""
        alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        n = int.from_bytes(data, 'big')
        res = ""
        while n:
            n, r = divmod(n, 58)
            res = alphabet[r] + res
        # Add leading zeros (for version byte)
        for byte in data:
            if byte == 0:
                res = alphabet[0] + res
            else:
                break
        return res
    
    def sign_transaction(self, transaction_data: str) -> str:
        """Sign transaction data with private key"""
        signature = self.private_key.sign(transaction_data.encode())
        return base64.b64encode(signature).decode()
    
    def verify_signature(self, public_key: VerifyingKey, data: str, signature: str) -> bool:
        """Verify signature against public key and data"""
        try:
            signature_bytes = base64.b64decode(signature.encode())
            return public_key.verify(signature_bytes, data.encode())
        except:
            return False

class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float, data: Dict = None, signature: str = None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.data = data or {}
        self.signature = signature
        self.timestamp = time.time()
        self.transaction_id = self.calculate_transaction_id()
    
    def calculate_transaction_id(self) -> str:
        """Calculate unique transaction ID"""
        transaction_string = json.dumps({
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "data": self.data
        }, sort_keys=True)
        return hashlib.sha256(transaction_string.encode()).hexdigest()
    
    def sign_transaction(self, wallet: Wallet):
        """Sign the transaction with wallet's private key"""
        transaction_data = json.dumps({
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "data": self.data
        }, sort_keys=True)
        self.signature = wallet.sign_transaction(transaction_data)
    
    def verify_signature(self) -> bool:
        """Verify the transaction signature"""
        if not self.signature or not self.sender:
            return False
            
        # Create a temporary verifying key from the sender address
        # In a real implementation, we'd need to retrieve the public key from the address
        # For now, we'll just verify the signature structure
        try:
            signature_bytes = base64.b64decode(self.signature.encode())
            transaction_data = json.dumps({
                "sender": self.sender,
                "recipient": self.recipient,
                "amount": self.amount,
                "timestamp": self.timestamp,
                "data": self.data
            }, sort_keys=True)
            # Verification would require the original public key
            # This is a simplified version
            return len(signature_bytes) > 0
        except:
            return False
    
    def to_dict(self) -> Dict:
        """Convert transaction to dictionary for serialization"""
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "data": self.data,
            "signature": self.signature,
            "transaction_id": self.transaction_id
        }

class SinBlockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.difficulty = 4  # Initial difficulty
        self.transactions: List[Transaction] = []
        self.mining_reward = 50.0  # Initial reward in SIN
        self.halving_interval = 210000  # Same as BTC
        self.total_supply = 0.0
        self.max_supply = 42000000.0  # 2x BTC supply
        self.lock = threading.Lock()
        
        # Create genesis block
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the blockchain"""
        genesis_transaction = Transaction(
            sender="0",  # Genesis transaction has no sender
            recipient="0000000000000000000000000000000000000000000000000000000000000000",
            amount=0,
            data={"type": "genesis"}
        )
        genesis_block = Block(0, "0", time.time(), [genesis_transaction])
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Get the latest block in the chain"""
        return self.chain[-1]
    
    def add_transaction(self, transaction: Transaction) -> bool:
        """Add a transaction to the pool"""
        if not transaction.sender or not transaction.recipient:
            print("Transaction must have sender and recipient")
            return False
        
        if not self.is_valid_transaction(transaction):
            print("Transaction is invalid")
            return False
        
        with self.lock:
            self.transactions.append(transaction)
        return True
    
    def is_valid_transaction(self, transaction: Transaction) -> bool:
        """Validate a transaction"""
        # Verify signature
        if not transaction.verify_signature():
            print("Invalid transaction signature")
            return False
        
        # Check if sender has sufficient balance
        if transaction.sender != "0":  # Not a mining reward
            sender_balance = self.get_balance_of_address(transaction.sender)
            if sender_balance < transaction.amount:
                print(f"Insufficient balance for {transaction.sender}")
                return False
        
        return True
    
    def has_transaction(self, transaction_id: str) -> bool:
        """Check if a transaction already exists in the blockchain"""
        for block in self.chain:
            for tx in block.transactions:
                if tx.transaction_id == transaction_id:
                    return True
        return False
    
    def mine_pending_transactions(self, mining_reward_address: str) -> bool:
        """Mine pending transactions and reward the miner"""
        if len(self.transactions) == 0:
            return False
        
        # Calculate current block reward based on halving
        block_reward = self.get_block_reward()
        
        # Add mining reward transaction
        reward_transaction = Transaction(
            sender="0",  # System transaction
            recipient=mining_reward_address,
            amount=block_reward,
            data={"type": "mining_reward"}
        )
        
        # Include reward transaction and pending transactions
        transactions_to_mine = [reward_transaction] + [tx for tx in self.transactions if not self.has_transaction(tx.transaction_id)]
        
        if len(transactions_to_mine) <= 1:  # Only reward transaction, no user transactions
            return False
        
        # Create new block
        new_block = Block(
            index=len(self.chain),
            previous_hash=self.get_latest_block().hash,
            timestamp=time.time(),
            transactions=transactions_to_mine
        )
        
        # Mine the block
        print(f"Mining block {new_block.index} with {len(transactions_to_mine)} transactions...")
        new_block.mine_block(self.difficulty)
        
        # Add block to chain
        self.chain.append(new_block)
        
        # Update total supply
        self.total_supply += block_reward
        
        # Clear pending transactions that were included
        with self.lock:
            self.transactions = [tx for tx in self.transactions if not self.has_transaction(tx.transaction_id)]
        
        print(f"Block {new_block.index} mined successfully! Reward: {block_reward} SIN")
        return True
    
    def get_block_reward(self) -> float:
        """Calculate current block reward considering halving"""
        halvings = len(self.chain) // self.halving_interval
        reward = self.mining_reward / (2 ** halvings)
        
        # Ensure we don't go below 0.00000001 SIN
        return max(reward, 0.00000001)
    
    def is_chain_valid(self) -> bool:
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check if current block hash is valid
            if current_block.hash != current_block.calculate_hash():
                print(f"Block {i} has invalid hash")
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                print(f"Block {i} has invalid previous hash")
                return False
        
        return True
    
    def get_balance_of_address(self, address: str) -> float:
        """Get balance of an address"""
        balance = 0.0
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.recipient == address:
                    balance += transaction.amount
                if transaction.sender == address and transaction.sender != "0":  # Don't count mining rewards as spendable
                    balance -= transaction.amount
        
        return balance
    
    def get_network_stats(self) -> Dict:
        """Get network statistics"""
        return {
            "block_count": len(self.chain),
            "difficulty": self.difficulty,
            "total_supply": self.total_supply,
            "max_supply": self.max_supply,
            "current_block_reward": self.get_block_reward(),
            "pending_transactions": len(self.transactions)
        }
    
    def to_dict(self) -> Dict:
        """Convert blockchain to dictionary for serialization"""
        return {
            "chain": [block.__dict__ for block in self.chain],
            "difficulty": self.difficulty,
            "mining_reward": self.mining_reward,
            "halving_interval": self.halving_interval,
            "total_supply": self.total_supply,
            "max_supply": self.max_supply,
            "transactions": [tx.to_dict() for tx in self.transactions]
        }