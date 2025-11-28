import numpy as np


class ReLULayer:
    """
    ReLU (Rectified Linear Unit) activation function layer.
    """
    def __init__(self):
        self.inputs = None
    
    def forward(self, inputs):
        """
        Forward pass: apply ReLU activation: max(0, x)
        """
        self.inputs = inputs
        return np.maximum(0, inputs)
    
    def backward(self, grad_output):
        """
        Backward pass: compute gradient of ReLU
        """
        grad_inputs = grad_output * (self.inputs > 0)
        return grad_inputs


class SigmoidLayer:
    """
    Sigmoid activation function layer.
    """
    def __init__(self):
        self.outputs = None
    
    def forward(self, inputs):
        """
        Forward pass: apply sigmoid activation: 1 / (1 + exp(-x))
        """
        # Clip inputs to prevent overflow
        clipped_inputs = np.clip(inputs, -500, 500)
        self.outputs = 1 / (1 + np.exp(-clipped_inputs))
        return self.outputs
    
    def backward(self, grad_output):
        """
        Backward pass: compute gradient of sigmoid
        """
        grad_inputs = grad_output * self.outputs * (1 - self.outputs)
        return grad_inputs


class SoftmaxLayer:
    """
    Softmax activation function layer for multi-class classification.
    """
    def __init__(self):
        self.outputs = None
    
    def forward(self, inputs):
        """
        Forward pass: apply softmax activation
        """
        # Subtract max for numerical stability
        shifted_inputs = inputs - np.max(inputs, axis=1, keepdims=True)
        exp_values = np.exp(shifted_inputs)
        self.outputs = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        return self.outputs
    
    def backward(self, grad_output):
        """
        Backward pass: compute gradient of softmax
        This implementation assumes cross-entropy loss which simplifies the gradient
        """
        # For cross-entropy loss with softmax, the gradient simplifies to:
        # outputs - targets, but since we don't have targets here, we return the general form
        # The full softmax gradient would be more complex, involving the Jacobian matrix
        # For typical use with cross-entropy loss, this is handled in the loss function
        return grad_output  # Placeholder - in practice, combined with cross-entropy