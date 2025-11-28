import numpy as np
from ..layers.linear import LinearLayer
from ..layers.activation import SoftmaxLayer
from ..layers.embedding import EmbeddingLayer
from ..layers.attention import MultiHeadAttention, PositionWiseFeedForward


class TransformerBlock:
    """
    A single transformer block with multi-head attention and feed-forward network.
    """
    def __init__(self, embed_dim, num_heads, ff_dim):
        self.attention = MultiHeadAttention(embed_dim, num_heads)
        self.norm1 = LayerNormalization(embed_dim)
        self.norm2 = LayerNormalization(embed_dim)
        self.feed_forward = PositionWiseFeedForward(embed_dim, ff_dim)
    
    def forward(self, x):
        # Multi-head attention with residual connection
        attn_output = self.attention.forward(x)
        x = x + attn_output  # Residual connection
        x = self.norm1.forward(x)  # Layer normalization
        
        # Feed-forward network with residual connection
        ff_output = self.feed_forward.forward(x)
        x = x + ff_output  # Residual connection
        x = self.norm2.forward(x)  # Layer normalization
        
        return x
    
    def backward(self, grad_output):
        # Backward through layer norm 2
        grad_output = self.norm2.backward(grad_output)
        
        # Backward through residual connection and feed-forward
        grad_ff = grad_output
        grad_ff = self.feed_forward.backward(grad_ff)
        grad_output = grad_output + grad_ff  # Add residual gradient
        
        # Backward through layer norm 1
        grad_output = self.norm1.backward(grad_output)
        
        # Backward through residual connection and attention
        grad_attn = grad_output
        grad_attn = self.attention.backward(grad_attn)
        grad_output = grad_output + grad_attn  # Add residual gradient
        
        return grad_output
    
    def update_parameters(self, learning_rate):
        self.attention.update_parameters(learning_rate)
        self.feed_forward.update_parameters(learning_rate)
        # Note: LayerNormalization parameters would also be updated here if trainable


class LayerNormalization:
    """
    Layer normalization to normalize across the feature dimension.
    """
    def __init__(self, normalized_shape, eps=1e-5):
        self.normalized_shape = normalized_shape
        self.eps = eps
        # Learnable parameters
        self.gamma = np.ones(normalized_shape)
        self.beta = np.zeros(normalized_shape)
        
        # For backpropagation
        self.inputs = None
        self.mean = None
        self.var = None
        self.x_norm = None
    
    def forward(self, inputs):
        self.inputs = inputs
        
        # Calculate mean and variance along the last axis (feature dimension)
        self.mean = np.mean(inputs, axis=-1, keepdims=True)
        self.var = np.var(inputs, axis=-1, keepdims=True)
        
        # Normalize
        self.x_norm = (inputs - self.mean) / np.sqrt(self.var + self.eps)
        
        # Scale and shift
        output = self.gamma * self.x_norm + self.beta
        
        return output
    
    def backward(self, grad_output):
        N = grad_output.shape[-1]
        
        # Gradients w.r.t. gamma and beta
        self.grad_gamma = np.sum(grad_output * self.x_norm, axis=-2, keepdims=True)
        self.grad_beta = np.sum(grad_output, axis=-2, keepdims=True)
        
        # Gradient w.r.t. normalized inputs
        grad_x_norm = grad_output * self.gamma
        
        # Gradient w.r.t. inputs
        grad_input = (1.0 / N) * (1.0 / np.sqrt(self.var + self.eps)) * (
            N * grad_x_norm 
            - np.sum(grad_x_norm, axis=-1, keepdims=True) 
            - self.x_norm * np.sum(grad_x_norm * self.x_norm, axis=-1, keepdims=True)
        )
        
        return grad_input
    
    def update_parameters(self, learning_rate):
        self.gamma -= learning_rate * self.grad_gamma
        self.beta -= learning_rate * self.grad_beta


class TransformerModel:
    """
    A complete transformer model for generative tasks.
    """
    def __init__(self, vocab_size, embed_dim, num_heads, ff_dim, num_layers, max_seq_len):
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.num_layers = num_layers
        self.max_seq_len = max_seq_len
        
        # Token embedding layer
        self.token_embedding = EmbeddingLayer(vocab_size, embed_dim)
        
        # Positional encoding
        self.positional_encoding = self._create_positional_encoding(max_seq_len, embed_dim)
        
        # Transformer blocks
        self.transformer_blocks = []
        for _ in range(num_layers):
            self.transformer_blocks.append(
                TransformerBlock(embed_dim, num_heads, ff_dim)
            )
        
        # Final layer normalization
        self.final_norm = LayerNormalization(embed_dim)
        
        # Output projection to vocabulary size
        self.output_projection = LinearLayer(embed_dim, vocab_size)
        
        # Activation for output probabilities
        self.softmax = SoftmaxLayer()
    
    def _create_positional_encoding(self, max_len, embed_dim):
        """
        Create positional encoding matrix.
        """
        pos_enc = np.zeros((max_len, embed_dim))
        position = np.arange(0, max_len, dtype=np.float32).reshape(-1, 1)
        div_term = np.exp(np.arange(0, embed_dim, 2, dtype=np.float32) * -(np.log(10000.0) / embed_dim))
        
        pos_enc[:, 0::2] = np.sin(position * div_term)  # Even indices
        pos_enc[:, 1::2] = np.cos(position * div_term)  # Odd indices
        
        return pos_enc
    
    def forward(self, input_ids):
        """
        Forward pass through the transformer model.
        """
        batch_size, seq_len = input_ids.shape
        
        # Token embedding
        x = self.token_embedding.forward(input_ids)
        
        # Add positional encoding (only for the sequence length)
        pos_encoding = self.positional_encoding[:seq_len, :]
        x = x + pos_encoding
        
        # Pass through transformer blocks
        for block in self.transformer_blocks:
            x = block.forward(x)
        
        # Final layer norm
        x = self.final_norm.forward(x)
        
        # Output projection
        logits = self.output_projection.forward(x)
        
        # Apply softmax to get probabilities
        output_probs = self.softmax.forward(logits)
        
        return output_probs
    
    def backward(self, grad_output):
        """
        Backward pass through the transformer model.
        """
        # Backward through softmax (in practice, this is often combined with loss)
        grad_output = self.softmax.backward(grad_output)
        
        # Backward through output projection
        grad_output = self.output_projection.backward(grad_output)
        
        # Backward through final layer norm
        grad_output = self.final_norm.backward(grad_output)
        
        # Backward through transformer blocks (in reverse order)
        for block in reversed(self.transformer_blocks):
            grad_output = block.backward(grad_output)
        
        # Backward through embedding layer
        # We only need to return gradients for the embeddings, not the positional encoding
        grad_embedding = self.token_embedding.backward(grad_output)
        
        return grad_embedding
    
    def update_parameters(self, learning_rate):
        """
        Update all model parameters using computed gradients.
        """
        self.token_embedding.update_parameters(learning_rate)
        for block in self.transformer_blocks:
            block.update_parameters(learning_rate)
        self.final_norm.update_parameters(learning_rate)
        self.output_projection.update_parameters(learning_rate)
    
    def generate(self, start_tokens, max_length=50, temperature=1.0):
        """
        Generate text using the trained model.
        """
        self.eval()  # Set to evaluation mode
        
        # Start with the provided tokens
        generated = start_tokens.copy()
        
        for _ in range(max_length):
            # Get the last sequence that fits in max_seq_len
            current_input = generated[-self.max_seq_len:].reshape(1, -1)
            
            # Forward pass to get next token probabilities
            output_probs = self.forward(current_input)
            
            # Get probabilities for the last token
            last_token_probs = output_probs[0, -1, :] / temperature
            
            # Apply softmax again after temperature scaling
            shifted_probs = last_token_probs - np.max(last_token_probs)
            exp_probs = np.exp(shifted_probs)
            probs = exp_probs / np.sum(exp_probs)
            
            # Sample next token
            next_token = np.random.choice(len(probs), p=probs)
            
            # Add to generated sequence
            generated = np.append(generated, next_token)
            
            # Stop if we generated an end-of-sequence token (assuming 0 is EOS)
            if next_token == 0:
                break
        
        return generated
    
    def train_mode(self):
        """Set model to training mode."""
        self._train_mode = True
    
    def eval(self):
        """Set model to evaluation mode."""
        self._train_mode = False