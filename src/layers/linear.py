import numpy as np


class LinearLayer:
    """
    A fully connected linear layer with configurable input and output dimensions.
    Can handle both 2D (batch, features) and 3D (batch, seq_len, features) inputs.
    """
    def __init__(self, input_size, output_size):
        # Initialize weights with small random values
        self.weights = np.random.randn(input_size, output_size) * 0.01
        self.biases = np.zeros((1, output_size))
        
        # Store inputs for backpropagation
        self.inputs = None
        
    def forward(self, inputs):
        """
        Forward pass: compute output = inputs @ weights + biases
        Works with 2D inputs (batch, features) or 3D inputs (batch, seq_len, features)
        """
        self.inputs = inputs
        
        if inputs.ndim == 2:
            # Standard 2D case: (batch, input_features) @ (input_features, output_features)
            output = np.dot(inputs, self.weights) + self.biases
        elif inputs.ndim == 3:
            # 3D case: apply linear transformation to last dimension
            # Reshape to 2D, apply transformation, then reshape back
            batch_size, seq_len, input_features = inputs.shape
            inputs_2d = inputs.reshape(-1, input_features)  # (batch*seq_len, input_features)
            output_2d = np.dot(inputs_2d, self.weights) + self.biases  # (batch*seq_len, output_features)
            output = output_2d.reshape(batch_size, seq_len, -1)  # (batch_size, seq_len, output_features)
        else:
            raise ValueError(f"Expected 2D or 3D input, got {inputs.ndim}D")
        
        return output
    
    def backward(self, grad_output):
        """
        Backward pass: compute gradients with respect to inputs, weights, and biases
        """
        if grad_output.ndim == 2:
            # Standard 2D case
            # Gradient with respect to inputs
            grad_inputs = np.dot(grad_output, self.weights.T)
            
            # Gradient with respect to weights
            grad_weights = np.dot(self.inputs.T, grad_output)
            
            # Gradient with respect to biases
            grad_biases = np.sum(grad_output, axis=0, keepdims=True)
        
        elif grad_output.ndim == 3:
            # 3D case
            batch_size, seq_len, output_features = grad_output.shape
            input_features = self.weights.shape[0]
            
            # Reshape grad_output for matrix operations
            grad_output_2d = grad_output.reshape(-1, output_features)  # (batch*seq_len, output_features)
            
            # Reshape inputs for matrix operations
            inputs_2d = self.inputs.reshape(-1, input_features)  # (batch*seq_len, input_features)
            
            # Gradient with respect to inputs
            grad_inputs_2d = np.dot(grad_output_2d, self.weights.T)  # (batch*seq_len, input_features)
            grad_inputs = grad_inputs_2d.reshape(batch_size, seq_len, -1)  # (batch_size, seq_len, input_features)
            
            # Gradient with respect to weights
            grad_weights = np.dot(inputs_2d.T, grad_output_2d)  # (input_features, output_features)
            
            # Gradient with respect to biases
            grad_biases = np.sum(grad_output_2d, axis=0, keepdims=True)  # (1, output_features)
        else:
            raise ValueError(f"Expected 2D or 3D grad_output, got {grad_output.ndim}D")
        
        # Store gradients for parameter updates
        self.grad_weights = grad_weights
        self.grad_biases = grad_biases
        
        return grad_inputs
    
    def update_parameters(self, learning_rate):
        """
        Update weights and biases using computed gradients
        """
        self.weights -= learning_rate * self.grad_weights
        self.biases -= learning_rate * self.grad_biases