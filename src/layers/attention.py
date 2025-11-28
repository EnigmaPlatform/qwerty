import numpy as np
from .linear import LinearLayer
from .activation import ReLULayer


class MultiHeadAttention:
    """
    Multi-head attention mechanism as used in transformers.
    """
    def __init__(self, embed_dim, num_heads):
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        
        assert self.head_dim * num_heads == embed_dim, "Embedding dimension must be divisible by number of heads"
        
        # Initialize weight matrices for Q, K, V projections and output projection
        self.W_q = np.random.randn(embed_dim, embed_dim) * 0.01
        self.W_k = np.random.randn(embed_dim, embed_dim) * 0.01
        self.W_v = np.random.randn(embed_dim, embed_dim) * 0.01
        self.W_o = np.random.randn(embed_dim, embed_dim) * 0.01
        
        # Store intermediate values for backpropagation
        self.inputs = None
        self.queries = None
        self.keys = None
        self.values = None
        self.attention_scores = None
        self.attention_weights = None
        self.attention_output = None
        
    def forward(self, inputs):
        """
        Forward pass of multi-head attention
        """
        batch_size, seq_len, _ = inputs.shape
        self.inputs = inputs
        
        # Project inputs to Q, K, V
        queries = np.dot(inputs, self.W_q)  # (batch_size, seq_len, embed_dim)
        keys = np.dot(inputs, self.W_k)     # (batch_size, seq_len, embed_dim)
        values = np.dot(inputs, self.W_v)   # (batch_size, seq_len, embed_dim)
        
        # Reshape for multi-head attention
        queries = queries.reshape(batch_size, seq_len, self.num_heads, self.head_dim)
        keys = keys.reshape(batch_size, seq_len, self.num_heads, self.head_dim)
        values = values.reshape(batch_size, seq_len, self.num_heads, self.head_dim)
        
        # Transpose to (batch_size, num_heads, seq_len, head_dim)
        queries = queries.transpose(0, 2, 1, 3)
        keys = keys.transpose(0, 2, 1, 3)
        values = values.transpose(0, 2, 1, 3)
        
        self.queries = queries
        self.keys = keys
        self.values = values
        
        # Compute attention scores
        attention_scores = np.matmul(queries, keys.transpose(0, 1, 3, 2))  # (batch_size, num_heads, seq_len, seq_len)
        attention_scores = attention_scores / np.sqrt(self.head_dim)  # Scale by sqrt(head_dim)
        
        # Apply softmax to get attention weights
        # For numerical stability, subtract max value before softmax
        shifted_scores = attention_scores - np.max(attention_scores, axis=-1, keepdims=True)
        exp_scores = np.exp(shifted_scores)
        attention_weights = exp_scores / np.sum(exp_scores, axis=-1, keepdims=True)
        
        self.attention_scores = attention_scores
        self.attention_weights = attention_weights
        
        # Apply attention weights to values
        attention_output = np.matmul(attention_weights, values)  # (batch_size, num_heads, seq_len, head_dim)
        
        # Transpose back to (batch_size, seq_len, num_heads, head_dim)
        attention_output = attention_output.transpose(0, 2, 1, 3)
        
        # Reshape to (batch_size, seq_len, embed_dim)
        attention_output = attention_output.reshape(batch_size, seq_len, self.embed_dim)
        
        self.attention_output = attention_output
        
        # Final projection
        output = np.dot(attention_output, self.W_o)
        
        return output
    
    def backward(self, grad_output):
        """
        Backward pass of multi-head attention
        """
        batch_size, seq_len, _ = grad_output.shape
        
        # Gradient with respect to final projection
        # grad_output: (batch_size, seq_len, embed_dim)
        # self.attention_output: (batch_size, seq_len, embed_dim)
        # grad_Wo should be: (embed_dim, embed_dim)
        grad_Wo = np.matmul(self.attention_output.reshape(-1, self.embed_dim).T, 
                           grad_output.reshape(-1, self.embed_dim))
        grad_attention_output = np.dot(grad_output, self.W_o.T)
        
        # Reshape for multi-head processing
        grad_attention_output = grad_attention_output.reshape(batch_size, seq_len, self.num_heads, self.head_dim)
        grad_attention_output = grad_attention_output.transpose(0, 2, 1, 3)  # (batch_size, num_heads, seq_len, head_dim)
        
        # Gradient with respect to values
        grad_values = np.matmul(self.attention_weights.transpose(0, 1, 3, 2), grad_attention_output)
        
        # Gradient with respect to attention weights
        grad_attention_weights = np.matmul(grad_attention_output, self.values.transpose(0, 1, 3, 2))
        
        # Gradient of softmax (simplified)
        grad_attention_scores = grad_attention_weights * self.attention_weights
        sum_grad = np.sum(grad_attention_scores, axis=-1, keepdims=True) * self.attention_weights
        grad_attention_scores = grad_attention_scores - sum_grad
        
        # Gradient with respect to Q*K^T computation
        grad_QK = grad_attention_scores / np.sqrt(self.head_dim)
        
        # Gradients with respect to queries and keys
        grad_queries = np.matmul(grad_QK, self.keys)
        grad_keys = np.matmul(grad_QK.transpose(0, 1, 3, 2), self.queries)
        
        # Transpose back to (batch_size, seq_len, num_heads, head_dim)
        grad_queries = grad_queries.transpose(0, 2, 1, 3).reshape(batch_size, seq_len, self.embed_dim)
        grad_keys = grad_keys.transpose(0, 2, 1, 3).reshape(batch_size, seq_len, self.embed_dim)
        grad_values = grad_values.transpose(0, 2, 1, 3).reshape(batch_size, seq_len, self.embed_dim)
        
        # Gradients with respect to input projections
        grad_input_queries = np.dot(grad_queries, self.W_q.T)
        grad_input_keys = np.dot(grad_keys, self.W_k.T)
        grad_input_values = np.dot(grad_values, self.W_v.T)
        
        # Combine gradients
        grad_inputs = grad_input_queries + grad_input_keys + grad_input_values
        
        # Compute gradients for weight matrices
        inputs_reshaped = self.inputs.reshape(-1, self.embed_dim)
        grad_queries_reshaped = grad_queries.reshape(-1, self.embed_dim)
        grad_keys_reshaped = grad_keys.reshape(-1, self.embed_dim)
        grad_values_reshaped = grad_values.reshape(-1, self.embed_dim)
        
        self.grad_Wq = np.dot(inputs_reshaped.T, grad_queries_reshaped)
        self.grad_Wk = np.dot(inputs_reshaped.T, grad_keys_reshaped)
        self.grad_Wv = np.dot(inputs_reshaped.T, grad_values_reshaped)
        self.grad_Wo = grad_Wo  # Already computed correctly above
        
        return grad_inputs
    
    def update_parameters(self, learning_rate):
        """
        Update weight matrices using computed gradients
        """
        self.W_q -= learning_rate * self.grad_Wq
        self.W_k -= learning_rate * self.grad_Wk
        self.W_v -= learning_rate * self.grad_Wv
        self.W_o -= learning_rate * self.grad_Wo


class PositionWiseFeedForward:
    """
    Position-wise feed-forward network used in transformers.
    """
    def __init__(self, embed_dim, ff_dim):
        self.linear1 = LinearLayer(embed_dim, ff_dim)
        self.relu = ReLULayer()
        self.linear2 = LinearLayer(ff_dim, embed_dim)
    
    def forward(self, inputs):
        x = self.linear1.forward(inputs)
        x = self.relu.forward(x)
        output = self.linear2.forward(x)
        return output
    
    def backward(self, grad_output):
        grad_x = self.linear2.backward(grad_output)
        grad_x = self.relu.backward(grad_x)
        grad_x = self.linear1.backward(grad_x)
        return grad_x
    
    def update_parameters(self, learning_rate):
        self.linear1.update_parameters(learning_rate)
        self.linear2.update_parameters(learning_rate)