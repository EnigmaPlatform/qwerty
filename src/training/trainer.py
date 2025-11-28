import numpy as np
from ..utils.loss import CrossEntropyLoss


class Trainer:
    """
    A trainer class to handle model training with backpropagation.
    """
    def __init__(self, model, loss_fn=None, learning_rate=0.001):
        self.model = model
        self.loss_fn = loss_fn or CrossEntropyLoss()
        self.learning_rate = learning_rate
        self.step_count = 0
    
    def train_step(self, inputs, targets):
        """
        Perform a single training step: forward pass, loss computation, backward pass, parameter update.
        inputs shape: (batch_size, seq_len)
        targets shape: (batch_size, seq_len)
        model output shape: (batch_size, seq_len, vocab_size)
        """
        # Forward pass
        outputs = self.model.forward(inputs)  # Shape: (batch_size, seq_len, vocab_size)
        
        # Reshape outputs and targets for loss computation
        # outputs: (batch_size, seq_len, vocab_size) -> (batch_size*seq_len, vocab_size)
        batch_size, seq_len, vocab_size = outputs.shape
        outputs_reshaped = outputs.reshape(-1, vocab_size)
        
        # targets: (batch_size, seq_len) -> (batch_size*seq_len,)
        targets_reshaped = targets.flatten()
        
        # Compute loss
        loss = self.loss_fn.forward(outputs_reshaped, targets_reshaped)
        
        # Backward pass through loss
        grad_output_reshaped = self.loss_fn.backward()  # Shape: (batch_size*seq_len, vocab_size)
        
        # Reshape back to match model output
        grad_output = grad_output_reshaped.reshape(batch_size, seq_len, vocab_size)  # (batch_size, seq_len, vocab_size)
        
        # Backward pass through model
        _ = self.model.backward(grad_output)
        
        # Update parameters
        self.model.update_parameters(self.learning_rate)
        
        self.step_count += 1
        return loss
    
    def train_epoch(self, dataloader, verbose=True):
        """
        Train for one epoch using the provided dataloader.
        """
        total_loss = 0
        num_batches = 0
        
        for batch_inputs, batch_targets in dataloader:
            loss = self.train_step(batch_inputs, batch_targets)
            total_loss += loss
            num_batches += 1
            
            if verbose and num_batches % 10 == 0:
                print(f"Batch {num_batches}, Loss: {loss:.4f}")
        
        avg_loss = total_loss / num_batches
        return avg_loss
    
    def train(self, dataloader, epochs, verbose=True):
        """
        Train the model for the specified number of epochs.
        """
        for epoch in range(epochs):
            if verbose:
                print(f"Epoch {epoch + 1}/{epochs}")
            
            avg_loss = self.train_epoch(dataloader, verbose=verbose)
            
            if verbose:
                print(f"Epoch {epoch + 1} completed. Average Loss: {avg_loss:.4f}\n")
        
        print("Training completed!")


class SimpleDataLoader:
    """
    A simple data loader for demonstration purposes.
    """
    def __init__(self, X, y, batch_size=32, shuffle=True):
        self.X = X
        self.y = y
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.n_samples = X.shape[0]
        self.indices = np.arange(self.n_samples)
        
    def __iter__(self):
        if self.shuffle:
            np.random.shuffle(self.indices)
        
        self.current_idx = 0
        return self
    
    def __next__(self):
        if self.current_idx >= self.n_samples:
            raise StopIteration
        
        end_idx = min(self.current_idx + self.batch_size, self.n_samples)
        batch_indices = self.indices[self.current_idx:end_idx]
        
        batch_X = self.X[batch_indices]
        batch_y = self.y[batch_indices]
        
        self.current_idx = end_idx
        
        return batch_X, batch_y
    
    def __len__(self):
        return int(np.ceil(self.n_samples / self.batch_size))