#!/usr/bin/env python3
"""
Test script to demonstrate the Sin Network Node functionality
"""

from sin_blockchain import Wallet, Transaction
from ai_model import Transformer, Tokenizer
from node_manager import NodeResourceManager
from mining_core import MiningCore
from ai_training import AITrainingSystem
import time

def test_wallet_functionality():
    print("=== Testing Wallet Functionality ===")
    
    # Create wallets
    wallet1 = Wallet()
    wallet2 = Wallet()
    
    print(f"Wallet 1 address: {wallet1.address}")
    print(f"Wallet 2 address: {wallet2.address}")
    
    # Test transaction creation
    transaction = Transaction(
        sender=wallet1.address,
        recipient=wallet2.address,
        amount=10.5,
        data={"message": "Test transaction"}
    )
    transaction.sign_transaction(wallet1)
    
    print(f"Transaction ID: {transaction.transaction_id}")
    print(f"Transaction signature: {transaction.signature[:20]}..." if transaction.signature else "No signature")
    print(f"Transaction valid: {transaction.verify_signature()}")
    
    print()

def test_blockchain():
    print("=== Testing Blockchain ===")
    
    from sin_blockchain import SinBlockchain
    
    blockchain = SinBlockchain()
    
    print(f"Genesis block: {blockchain.chain[0].hash}")
    print(f"Initial block reward: {blockchain.get_block_reward()}")
    print(f"Network stats: {blockchain.get_network_stats()}")
    
    # Create wallets for testing
    sender_wallet = Wallet()
    recipient_wallet = Wallet()
    
    # Create and add a transaction
    test_transaction = Transaction(
        sender=sender_wallet.address,
        recipient=recipient_wallet.address,
        amount=5.0,
        data={"type": "test"}
    )
    test_transaction.sign_transaction(sender_wallet)
    
    success = blockchain.add_transaction(test_transaction)
    print(f"Transaction added: {success}")
    
    # Mine a block with the transaction
    mining_success = blockchain.mine_pending_transactions(recipient_wallet.address)
    print(f"Block mined: {mining_success}")
    
    print(f"Updated network stats: {blockchain.get_network_stats()}")
    print(f"Recipient balance: {blockchain.get_balance_of_address(recipient_wallet.address)}")
    
    print()

def test_ai_model():
    print("=== Testing AI Model ===")
    
    # Initialize model and tokenizer
    tokenizer = Tokenizer()
    model = Transformer(
        src_vocab_size=1000,
        tgt_vocab_size=1000,
        d_model=128,
        num_heads=4,
        num_layers=2,
        d_ff=512,
        max_seq_length=50
    )
    
    print("Model initialized successfully")
    
    # Build vocabulary with some sample text
    sample_texts = [
        "The quick brown fox jumps over the lazy dog",
        "Machine learning is a subset of artificial intelligence",
        "Blockchain technology enables decentralized systems"
    ]
    for text in sample_texts:
        tokenizer.build_vocab([text])
    
    print(f"Vocabulary size: {len(tokenizer.vocab)}")
    
    # Test encoding/decoding
    test_text = "The quick brown fox"
    encoded = tokenizer.encode(test_text)
    decoded = tokenizer.decode(encoded)
    
    print(f"Original: {test_text}")
    print(f"Encoded: {encoded}")
    print(f"Decoded: {decoded}")
    
    print()

def test_node_resource_manager():
    print("=== Testing Node Resource Manager ===")
    
    node_manager = NodeResourceManager()
    
    # Scan resources
    resources = node_manager.scan_resources()
    print(f"Detected CPU cores: {resources['cpu']['count']}")
    print(f"Total RAM: {resources['ram']['total'] / (1024**3):.2f} GB")
    print(f"Total disk: {resources['disk']['total'] / (1024**3):.2f} GB")
    print(f"GPU count: {len(resources['gpu'])}")
    
    # Set resource limits
    node_manager.set_resource_limits(0.3, 0.2, 0.4, 0.3)  # 30% CPU, 20% GPU, 40% RAM, 30% disk
    
    usage = node_manager.get_resource_usage()
    print(f"Resource usage after limits: {usage}")
    
    hashrate = node_manager.get_hashrate_contribution()
    print(f"Estimated hashrate contribution: {hashrate:.2f} H/s")
    
    reward_mult = node_manager.get_reward_multiplier()
    print(f"Reward multiplier: {reward_mult:.2f}")
    
    print()

def test_ai_training():
    print("=== Testing AI Training System ===")
    
    # Import SinBlockchain
    from sin_blockchain import SinBlockchain
    
    # Initialize blockchain for rewards
    blockchain = SinBlockchain()
    wallet = Wallet()
    
    # Initialize model and tokenizer
    tokenizer = Tokenizer()
    model = Transformer(
        src_vocab_size=1000,
        tgt_vocab_size=1000,
        d_model=128,
        num_heads=4,
        num_layers=2,
        d_ff=512,
        max_seq_length=50
    )
    
    # Initialize training system
    training_system = AITrainingSystem(model, tokenizer, blockchain)
    
    # Add sample training data
    sample_data = [
        ("The quick brown fox", "jumps over the lazy dog"),
        ("Machine learning is", "a subset of AI"),
        ("Blockchain technology", "enables decentralization")
    ]
    training_system.add_training_data(sample_data)
    print(f"Added {len(sample_data)} training samples")
    
    # Perform a quick training evaluation (without full training to save time)
    metrics = training_system.evaluator.evaluate_model_performance(model, sample_data, tokenizer)
    print(f"Initial model metrics: {metrics}")
    
    print()

def main():
    print("Testing Sin Network Node Components\n")
    
    test_wallet_functionality()
    test_blockchain()
    test_ai_model()
    test_node_resource_manager()
    test_ai_training()
    
    print("All tests completed successfully!")
    print("\nTo run the full node, execute: python main.py")

if __name__ == "__main__":
    main()