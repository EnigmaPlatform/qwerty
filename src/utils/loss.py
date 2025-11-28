import numpy as np


class CrossEntropyLoss:
    """
    Cross-entropy loss function for classification tasks.
    """
    def __init__(self):
        self.predictions = None
        self.targets = None
    
    def forward(self, predictions, targets):
        """
        Forward pass: compute cross-entropy loss
        """
        self.predictions = predictions
        self.targets = targets
        
        # Add small epsilon for numerical stability
        epsilon = 1e-15
        predictions_clipped = np.clip(predictions, epsilon, 1 - epsilon)
        
        # Compute cross-entropy loss
        if targets.ndim == 1:
            # If targets are class indices
            loss = -np.log(predictions_clipped[range(len(predictions_clipped)), targets] + 1e-15)
        else:
            # If targets are one-hot encoded
            loss = -np.sum(targets * np.log(predictions_clipped + 1e-15), axis=1)
        
        return np.mean(loss)
    
    def backward(self):
        """
        Backward pass: compute gradient of cross-entropy loss
        """
        grad = self.predictions.copy()
        
        if self.targets.ndim == 1:
            # If targets are class indices
            grad[range(len(grad)), self.targets] -= 1
        else:
            # If targets are one-hot encoded
            grad -= self.targets
        
        grad /= len(grad)  # Normalize by batch size
        return grad


class MSELoss:
    """
    Mean Squared Error loss function for regression tasks.
    """
    def __init__(self):
        self.predictions = None
        self.targets = None
    
    def forward(self, predictions, targets):
        """
        Forward pass: compute mean squared error loss
        """
        self.predictions = predictions
        self.targets = targets
        loss = np.mean((predictions - targets) ** 2)
        return loss
    
    def backward(self):
        """
        Backward pass: compute gradient of MSE loss
        """
        grad = 2 * (self.predictions - self.targets) / len(self.predictions)
        return grad