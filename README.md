# Sin Network Node - Generative AI with Blockchain Integration

## Overview

Sin Network Node is a comprehensive system that combines a generative AI model with a blockchain network (Sin/SIN). The system allows users to run a node that participates in both blockchain mining and AI training, earning rewards for both activities.

## Features

### Blockchain Features
- **Sin (SIN) Blockchain**: A Bitcoin-like blockchain with 2x the supply (42 million coins)
- **Wallet System**: Bitcoin-style wallet addresses with ECDSA cryptography
- **Transaction System**: Signed transactions with balance verification
- **Mining**: Proof-of-Work mining with adjustable difficulty
- **Halving**: Block rewards halve every 210,000 blocks (like Bitcoin)
- **P2P Network**: Node-to-node communication for transaction and block propagation

### AI Features
- **Transformer Model**: Full implementation of transformer architecture with attention mechanisms
- **Training System**: AI training with performance evaluation
- **Reward System**: Earn SIN tokens for training high-quality models (10% of block reward)

### Resource Management
- **System Monitoring**: Automatic detection of CPU, GPU, RAM, and disk resources
- **Resource Allocation**: Set limits from 10% to 80% for each resource type
- **Reward Scaling**: Higher resource allocation leads to higher potential rewards

## Architecture

The system consists of several interconnected components:

1. **sin_blockchain.py**: Core blockchain implementation with wallet and transaction functionality
2. **ai_model.py**: Transformer neural network implementation
3. **node_manager.py**: System resource management and monitoring
4. **mining_core.py**: Mining algorithm and block creation
5. **ai_training.py**: AI training and evaluation system
6. **distributed_storage.py**: Distributed storage across nodes
7. **main.py**: Main node application with user interface

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Running a Node

```bash
python main.py
```

This will start the node with an interactive menu that allows you to:

1. View wallet address
2. Create new wallet
3. Send transactions
4. Check balance
5. Start/stop mining
6. Train AI model
7. Check blockchain stats
8. Check network stats
9. Connect to other nodes

### Wallet Management

- **Automatic Wallet Creation**: A wallet is automatically created when the node starts
- **New Wallet**: Option to generate a new wallet and replace the current one
- **Transaction Signing**: All transactions are automatically signed with the current wallet

### Mining Configuration

When starting mining, you'll be prompted to set resource limits:
- CPU limit (10% to 80%)
- GPU limit (10% to 80%) 
- RAM limit (10% to 80%)
- Disk limit (10% to 80%)

Higher resource allocation leads to higher potential rewards.

### AI Training

The system includes a full transformer model that can be trained on text data. Training rewards are issued when model quality meets certain thresholds.

## Technical Details

### Blockchain Specifications
- **Ticker**: SIN
- **Total Supply**: 42,000,000 coins (2x Bitcoin)
- **Block Reward**: Starts at 50 SIN, halves every 210,000 blocks
- **Difficulty Adjustment**: Automatic based on network hashrate
- **Transaction Fees**: Minimal fees for transaction processing

### AI Model Specifications
- **Architecture**: Transformer with multi-head attention
- **Components**: Encoder/decoder layers, feed-forward networks, positional encoding
- **Training**: Full training pipeline with evaluation metrics

### Security Features
- **ECDSA Signatures**: All transactions are signed with ECDSA
- **Balance Verification**: Double-spend protection
- **Blockchain Validation**: Full chain validation
- **Wallet Security**: Private key encryption

## Reward System

### Mining Rewards
- Standard Proof-of-Work rewards
- Adjustable based on resource allocation (10% to 80%)
- Maximum 100 SIN per block

### AI Training Rewards
- 10% of block reward when training quality is positive
- Quality evaluated based on accuracy and perplexity metrics

## Network Features

- **P2P Communication**: Nodes can connect to form a decentralized network
- **Transaction Propagation**: Transactions broadcast to connected nodes
- **Distributed Storage**: Network storage across participating nodes
- **Network Statistics**: Real-time monitoring of network health

## File Structure

```
/workspace/
├── sin_blockchain.py      # Core blockchain implementation
├── ai_model.py           # AI model and tokenizer
├── node_manager.py       # Resource management
├── mining_core.py        # Mining functionality
├── ai_training.py        # AI training and evaluation
├── distributed_storage.py # Distributed storage
├── main.py              # Main application
├── test_system.py       # Test script
└── requirements.txt     # Dependencies
```

## Requirements

- Python 3.8+
- PyTorch (CPU or CUDA)
- ecdsa for cryptographic operations
- GPUtil for GPU monitoring
- psutil for system monitoring

## Testing

Run the test suite to verify all components:

```bash
python test_system.py
```

This will test all major components and verify the system is working correctly.