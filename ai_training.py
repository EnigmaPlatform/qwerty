import torch
import torch.nn as nn
import torch.optim as optim
from ai_model import Transformer, Tokenizer, AITrainingEvaluator
from sin_blockchain import Transaction, Wallet
from typing import List, Tuple, Dict
import random

class AITrainingSystem:
    def __init__(self, model: Transformer, tokenizer: Tokenizer, blockchain):
        self.model = model
        self.tokenizer = tokenizer
        self.blockchain = blockchain
        self.evaluator = AITrainingEvaluator()
        self.training_data = []
        self.optimizer = optim.Adam(model.parameters(), lr=0.0001)
        self.criterion = nn.CrossEntropyLoss(ignore_index=0)
        self.is_training = False
        self.training_thread = None
    
    def add_training_data(self, data: List[Tuple[str, str]]):
        """Add training data to the system"""
        self.training_data.extend(data)
    
    def train_epoch(self, data_batch: List[Tuple[str, str]]) -> float:
        """Train for one epoch on a batch of data"""
        self.model.train()
        total_loss = 0.0
        
        for src_text, tgt_text in data_batch:
            self.optimizer.zero_grad()
            
            src_tokens = torch.tensor([self.tokenizer.encode(src_text)])
            tgt_tokens = torch.tensor([self.tokenizer.encode(tgt_text)])
            
            # Shift target for teacher forcing
            tgt_input = tgt_tokens[:, :-1]
            tgt_output = tgt_tokens[:, 1:]
            
            output = self.model(src_tokens, tgt_input)
            loss = self.criterion(output.view(-1, output.size(-1)), tgt_output.view(-1))
            
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
        
        return total_loss / len(data_batch)
    
    def train_model(self, epochs: int = 10, batch_size: int = 4) -> Dict:
        """Train the model and return metrics"""
        if not self.training_data:
            print("No training data available")
            return {}
        
        for epoch in range(epochs):
            # Shuffle data each epoch
            random.shuffle(self.training_data)
            
            # Process in batches
            for i in range(0, len(self.training_data), batch_size):
                batch = self.training_data[i:i+batch_size]
                loss = self.train_epoch(batch)
                print(f"Epoch {epoch+1}/{epochs}, Batch loss: {loss:.4f}")
        
        # Evaluate model performance after training
        metrics = self.evaluator.evaluate_model_performance(
            self.model, 
            self.training_data[:min(100, len(self.training_data))],  # Evaluate on subset
            self.tokenizer
        )
        
        return metrics
    
    def evaluate_and_reward(self, reward_address: str) -> bool:
        """Evaluate model quality and reward if positive"""
        if not self.training_data:
            print("No training data to evaluate")
            return False
        
        # Evaluate model performance
        metrics = self.evaluator.evaluate_model_performance(
            self.model,
            self.training_data[:min(100, len(self.training_data))],  # Evaluate on subset
            self.tokenizer
        )
        
        # Check if quality is positive
        if self.evaluator.is_quality_positive(metrics):
            # Calculate reward (10% of current block reward)
            block_reward = self.blockchain.get_block_reward()
            training_reward = block_reward * 0.1
            
            # Create reward transaction
            reward_transaction = Transaction(
                sender="0",  # System transaction
                recipient=reward_address,
                amount=training_reward,
                data={
                    "type": "training_reward",
                    "metrics": metrics
                }
            )
            
            # Add to blockchain
            self.blockchain.add_transaction(reward_transaction)
            print(f"Training reward issued: {training_reward} SIN to {reward_address}")
            return True
        else:
            print(f"Model quality not positive. Accuracy: {metrics.get('accuracy', 0):.4f}, Perplexity: {metrics.get('perplexity', float('inf')):.2f}")
            return False
    
    def get_model_metrics(self) -> Dict:
        """Get current model metrics"""
        return self.evaluator.metrics