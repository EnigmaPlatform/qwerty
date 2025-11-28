import numpy as np


class EmbeddingLayer:
    """
    Embedding layer to convert discrete tokens/indices to dense vectors.
    """
    def __init__(self, vocab_size, embedding_dim):
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        
        # Initialize embedding matrix with small random values
        self.embeddings = np.random.randn(vocab_size, embedding_dim) * 0.01
        
        # Store inputs and embedding lookups for backpropagation
        self.input_indices = None
        self.output_embeddings = None
        
    def forward(self, input_indices):
        """
        Forward pass: lookup embeddings for input indices
        Input: array of token indices
        Output: corresponding embedding vectors
        """
        self.input_indices = input_indices
        self.output_embeddings = self.embeddings[input_indices]
        return self.output_embeddings
    
    def backward(self, grad_output):
        """
        Backward pass: compute gradients with respect to embeddings
        grad_output shape: (batch_size, seq_len, embedding_dim)
        """
        # Initialize gradient matrix for embeddings
        grad_embeddings = np.zeros_like(self.embeddings)
        
        # Accumulate gradients for each index
        # grad_output shape: (batch_size, seq_len, embedding_dim)
        # self.input_indices shape: (batch_size, seq_len)
        batch_size, seq_len = self.input_indices.shape
        
        for i in range(batch_size):
            for j in range(seq_len):
                idx = self.input_indices[i, j]
                grad_embeddings[idx] += grad_output[i, j]
        
        # Store gradients for parameter updates
        self.grad_embeddings = grad_embeddings
        
        # Return zeros with same shape as input_indices since gradients w.r.t. indices are not meaningful
        return np.zeros_like(self.input_indices, dtype=np.float32)
    
    def update_parameters(self, learning_rate):
        """
        Update embedding matrix using computed gradients
        """
        self.embeddings -= learning_rate * self.grad_embeddings