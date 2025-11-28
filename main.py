import time
import threading
import socket
import json
from sin_blockchain import SinBlockchain, Transaction, Wallet
from ai_model import Transformer, Tokenizer
from node_manager import NodeResourceManager
from mining_core import MiningCore
from ai_training import AITrainingSystem
from distributed_storage import DistributedStorage
import random

class SinNetworkNode:
    def __init__(self):
        self.blockchain = SinBlockchain()
        self.node_manager = NodeResourceManager()
        self.mining_core = None
        self.ai_training = None
        self.distributed_storage = DistributedStorage()
        self.wallet = Wallet()  # Generate initial wallet
        self.nodes = set()  # Connected nodes
        self.server_socket = None
        self.running = False
        
        # Initialize other components
        self.tokenizer = Tokenizer()
        self.model = Transformer(
            src_vocab_size=10000,
            tgt_vocab_size=10000,
            d_model=512,
            num_heads=8,
            num_layers=6,
            d_ff=2048,
            max_seq_length=100
        )
        self.ai_training = AITrainingSystem(self.model, self.tokenizer, self.blockchain)
        self.mining_core = MiningCore(self.blockchain, self.node_manager)
        
        # Register this node
        resources = self.node_manager.scan_resources()
        node_id = f"node_{self.wallet.address[:8]}"  # Use part of wallet address as node ID
        self.distributed_storage.register_node(node_id, resources)
        
        print(f"Node initialized with wallet address: {self.wallet.address}")
    
    def create_new_wallet(self):
        """Create a new wallet and replace the current one"""
        old_address = self.wallet.address
        self.wallet = Wallet()
        print(f"Wallet changed from {old_address} to {self.wallet.address}")
        return self.wallet.address
    
    def send_transaction(self, recipient: str, amount: float, data: dict = None):
        """Send a transaction to the network"""
        transaction = Transaction(
            sender=self.wallet.address,
            recipient=recipient,
            amount=amount,
            data=data or {}
        )
        transaction.sign_transaction(self.wallet)
        
        if self.blockchain.add_transaction(transaction):
            print(f"Transaction sent: {amount} SIN to {recipient}")
            # Broadcast transaction to other nodes
            self.broadcast_transaction(transaction)
            return True
        else:
            print("Failed to send transaction")
            return False
    
    def broadcast_transaction(self, transaction: Transaction):
        """Broadcast transaction to connected nodes"""
        # In a real implementation, this would send the transaction to other nodes
        print(f"Broadcasting transaction: {transaction.transaction_id}")
    
    def start_server(self, port=5000):
        """Start the node server to accept connections"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('0.0.0.0', port))
        self.server_socket.listen(5)
        self.running = True
        
        print(f"Node server started on port {port}")
        
        def accept_connections():
            while self.running:
                try:
                    client_socket, addr = self.server_socket.accept()
                    print(f"Connection from {addr}")
                    # Handle client in a separate thread
                    threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
                except:
                    if self.running:
                        print("Error accepting connections")
        
        threading.Thread(target=accept_connections, daemon=True).start()
    
    def handle_client(self, client_socket):
        """Handle a client connection"""
        try:
            data = client_socket.recv(4096).decode()
            if data:
                message = json.loads(data)
                self.process_message(message, client_socket)
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()
    
    def process_message(self, message, client_socket):
        """Process incoming messages from other nodes"""
        msg_type = message.get("type")
        
        if msg_type == "transaction":
            # Process incoming transaction
            tx_data = message.get("transaction")
            transaction = Transaction(
                sender=tx_data["sender"],
                recipient=tx_data["recipient"],
                amount=tx_data["amount"],
                data=tx_data.get("data", {}),
                signature=tx_data.get("signature")
            )
            transaction.transaction_id = tx_data.get("transaction_id")
            self.blockchain.add_transaction(transaction)
        
        elif msg_type == "block":
            # Process incoming block (for synchronization)
            print("Received block from another node")
            # In a real implementation, we would validate and add the block if it's valid
        
        elif msg_type == "get_balance":
            # Return balance for a specific address
            address = message.get("address")
            balance = self.blockchain.get_balance_of_address(address)
            response = {"type": "balance", "address": address, "balance": balance}
            client_socket.send(json.dumps(response).encode())
    
    def connect_to_node(self, host, port):
        """Connect to another node"""
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            self.nodes.add((host, port))
            print(f"Connected to node {host}:{port}")
            
            # Send a simple handshake
            handshake = {"type": "handshake", "node_id": self.wallet.address[:16]}
            client_socket.send(json.dumps(handshake).encode())
            client_socket.close()
        except Exception as e:
            print(f"Failed to connect to {host}:{port} - {e}")
    
    def get_balance(self, address: str = None):
        """Get balance for an address (current wallet if none specified)"""
        if address is None:
            address = self.wallet.address
        return self.blockchain.get_balance_of_address(address)
    
    def start_mining(self):
        """Start mining with current wallet as reward address"""
        self.mining_core.start_mining(self.wallet.address)
    
    def stop_mining(self):
        """Stop mining"""
        self.mining_core.stop_mining()
    
    def main_loop(self):
        """Main loop for the node"""
        while True:
            print("\n--- Sin Network Node ---")
            print(f"Current wallet: {self.wallet.address}")
            print(f"Balance: {self.get_balance():.4f} SIN")
            print("1. View wallet address")
            print("2. Create new wallet")
            print("3. Send transaction")
            print("4. Check balance")
            print("5. Start mining")
            print("6. Stop mining")
            print("7. Train AI model")
            print("8. Evaluate AI model")
            print("9. Check blockchain stats")
            print("10. Check network stats")
            print("11. Connect to another node")
            print("12. Exit")
            
            choice = input("Select option: ")
            
            if choice == "1":
                print(f"Current wallet address: {self.wallet.address}")
                
            elif choice == "2":
                new_address = self.create_new_wallet()
                print(f"New wallet created: {new_address}")
                
            elif choice == "3":
                recipient = input("Enter recipient address: ")
                try:
                    amount = float(input("Enter amount: "))
                    data_input = input("Enter optional data (or press Enter): ")
                    data = json.loads(data_input) if data_input else {}
                    
                    success = self.send_transaction(recipient, amount, data)
                    if success:
                        print("Transaction sent successfully")
                    else:
                        print("Failed to send transaction")
                except ValueError:
                    print("Invalid amount")
                    
            elif choice == "4":
                address = input("Enter address to check (or press Enter for current): ").strip()
                if not address:
                    address = self.wallet.address
                balance = self.get_balance(address)
                print(f"Balance for {address}: {balance:.4f} SIN")
                
            elif choice == "5":
                # Set resource limits
                print("\nSetting resource limits (choose values between 0.1 and 0.8):")
                try:
                    cpu_limit = float(input("CPU limit (0.1-0.8, default 0.5): ") or "0.5")
                    gpu_limit = float(input("GPU limit (0.1-0.8, default 0.5): ") or "0.5")
                    ram_limit = float(input("RAM limit (0.1-0.8, default 0.5): ") or "0.5")
                    disk_limit = float(input("Disk limit (0.1-0.8, default 0.5): ") or "0.5")
                    
                    self.node_manager.set_resource_limits(cpu_limit, gpu_limit, ram_limit, disk_limit)
                    print(f"Resource limits set: CPU={cpu_limit}, GPU={gpu_limit}, RAM={ram_limit}, Disk={disk_limit}")
                    
                    self.start_mining()
                except ValueError:
                    print("Invalid input for resource limits")
                
            elif choice == "6":
                self.stop_mining()
                
            elif choice == "7":
                print("Training AI model...")
                # Add some sample training data
                sample_data = [
                    ("The quick brown fox", "jumps over the lazy dog"),
                    ("Machine learning is", "a subset of artificial intelligence"),
                    ("Blockchain technology", "enables decentralized systems"),
                    ("Neural networks", "mimic human brain functions"),
                    ("Artificial intelligence", "is transforming industries"),
                    ("Cryptocurrency mining", "requires computational power"),
                    ("Distributed systems", "enable peer-to-peer networks"),
                    ("Natural language", "processing involves AI models")
                ]
                self.ai_training.add_training_data(sample_data)
                
                epochs = int(input("Enter number of training epochs (default 5): ") or "5")
                metrics = self.ai_training.train_model(epochs=epochs)
                print(f"Training completed. Metrics: {metrics}")
                
                # Evaluate and reward if quality is positive
                reward_address = input("Enter SIN address for training rewards (or press Enter for current): ").strip()
                if not reward_address:
                    reward_address = self.wallet.address
                self.ai_training.evaluate_and_reward(reward_address)
                
            elif choice == "8":
                metrics = self.ai_training.get_model_metrics()
                print(f"Current model metrics: {metrics}")
                
            elif choice == "9":
                stats = self.blockchain.get_network_stats()
                mining_stats = self.mining_core.get_mining_stats()
                resource_usage = self.node_manager.get_resource_usage()
                
                print(f"\nBlockchain Stats:")
                print(f"  Block count: {stats['block_count']}")
                print(f"  Difficulty: {stats['difficulty']}")
                print(f"  Total supply: {stats['total_supply']:.2f} SIN")
                print(f"  Current block reward: {stats['current_block_reward']:.2f} SIN")
                print(f"  Pending transactions: {stats['pending_transactions']}")
                
                print(f"\nMining Stats:")
                print(f"  Hashrate: {mining_stats['hashrate']:.2f} H/s")
                print(f"  Blocks mined: {mining_stats['blocks_mined']}")
                print(f"  Mining status: {'Active' if mining_stats['is_mining'] else 'Inactive'}")
                
                print(f"\nResource Usage:")
                for resource, usage in resource_usage.items():
                    print(f"  {resource}: {usage:.2f}%")
                    
            elif choice == "10":
                net_stats = self.distributed_storage.get_network_statistics()
                node_dist = self.distributed_storage.get_node_data_distribution()
                
                print(f"\nNetwork Statistics:")
                print(f"  Total nodes: {net_stats['total_nodes']}")
                print(f"  Active nodes: {net_stats['active_nodes']}")
                print(f"  Total capacity: {net_stats['total_capacity'] / (1024**3):.2f} GB")
                print(f"  Used storage: {net_stats['used_storage'] / (1024**2):.2f} MB")
                
                print(f"\nNode Data Distribution:")
                for node_id, info in node_dist.items():
                    print(f"  {node_id}: {info['shards_stored']} shards, {info['storage_used'] / (1024**2):.2f} MB")
                    
            elif choice == "11":
                host = input("Enter host IP: ")
                port = int(input("Enter port: "))
                self.connect_to_node(host, port)
                
            elif choice == "12":
                print("Stopping node...")
                self.running = False
                if self.server_socket:
                    self.server_socket.close()
                self.stop_mining()
                break
                
            else:
                print("Invalid option")

def main():
    print("Starting Sin Network Node...")
    
    node = SinNetworkNode()
    
    # Start the server in a separate thread
    threading.Thread(target=node.start_server, daemon=True).start()
    
    # Run the main loop
    node.main_loop()

if __name__ == "__main__":
    main()