import numpy as np
from src.models.transformer import TransformerModel
from src.data.tokenizer import SimpleTokenizer
from src.training.trainer import Trainer, SimpleDataLoader
import pickle


class GenerativeAIInterface:
    """
    A user-friendly interface for the generative AI model.
    """
    def __init__(self, vocab_size=1000, embed_dim=128, num_heads=4, ff_dim=256, num_layers=2, max_seq_len=50):
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.num_layers = num_layers
        self.max_seq_len = max_seq_len
        
        # Initialize tokenizer
        self.tokenizer = SimpleTokenizer()
        
        # Initialize model
        self.model = TransformerModel(
            vocab_size=vocab_size,
            embed_dim=embed_dim,
            num_heads=num_heads,
            ff_dim=ff_dim,
            num_layers=num_layers,
            max_seq_len=max_seq_len
        )
        
        # Initialize trainer
        self.trainer = Trainer(self.model)
        
        print("Generative AI Interface initialized!")
    
    def train_on_texts(self, texts, epochs=10, learning_rate=0.001, batch_size=8):
        """
        Train the model on provided texts.
        """
        print("Building vocabulary...")
        self.tokenizer.build_vocab(texts)
        
        # Update model vocab size if needed
        if self.tokenizer.vocab_size != self.vocab_size:
            print(f"Updating model vocabulary size from {self.vocab_size} to {self.tokenizer.vocab_size}")
            # Set vocab size to the actual vocabulary size from tokenizer
            self.vocab_size = self.tokenizer.vocab_size
            self.model = TransformerModel(
                vocab_size=self.vocab_size,
                embed_dim=self.embed_dim,
                num_heads=self.num_heads,
                ff_dim=self.ff_dim,
                num_layers=self.num_layers,
                max_seq_len=self.max_seq_len
            )
            self.trainer = Trainer(self.model, learning_rate=learning_rate)
        
        print("Preparing training data...")
        # Prepare training data - create input-target pairs from texts
        # In language modeling, we predict the next token given the previous tokens
        input_sequences = []
        target_sequences = []
        
        for text in texts:
            token_ids = self.tokenizer.encode(text, add_special_tokens=True)
            
            # Slide a window across the sequence to create input-target pairs
            # Input: [x1, x2, ..., xn] -> Target: [x2, x3, ..., xn+1]
            for i in range(len(token_ids) - 1):
                # Input sequence: from position i to end-1
                input_seq = token_ids[i:i + self.max_seq_len-1] if len(token_ids) - i > self.max_seq_len-1 else token_ids[i:]
                # Target sequence: from position i+1 to end
                target_seq = token_ids[i+1:i + self.max_seq_len] if len(token_ids) - (i+1) > self.max_seq_len-1 else token_ids[i+1:]
                
                # Pad sequences to max length
                if len(input_seq) < self.max_seq_len:
                    padded_input = np.pad(input_seq, (0, self.max_seq_len - len(input_seq)), 
                                        mode='constant', constant_values=self.tokenizer.pad_token_id)
                else:
                    padded_input = input_seq[:self.max_seq_len]
                
                if len(target_seq) < self.max_seq_len:
                    padded_target = np.pad(target_seq, (0, self.max_seq_len - len(target_seq)), 
                                         mode='constant', constant_values=self.tokenizer.pad_token_id)
                else:
                    padded_target = target_seq[:self.max_seq_len]
                
                input_sequences.append(padded_input)
                target_sequences.append(padded_target)
        
        X = np.array(input_sequences)
        y = np.array(target_sequences)
        
        print(f"Training on {len(X)} sequence pairs...")
        
        # Create data loader
        dataloader = SimpleDataLoader(X, y, batch_size=batch_size, shuffle=True)
        
        # Train the model
        self.trainer.learning_rate = learning_rate
        self.trainer.train(dataloader, epochs=epochs)
    
    def generate_text(self, prompt="", max_length=50, temperature=0.8):
        """
        Generate text based on a prompt.
        """
        if not prompt:
            # Start with BOS token if no prompt provided
            start_tokens = np.array([self.tokenizer.bos_token_id])
        else:
            # Encode the prompt
            start_tokens = self.tokenizer.encode(prompt, add_special_tokens=True)
        
        # Generate text
        generated_tokens = self.model.generate(start_tokens, max_length=max_length, temperature=temperature)
        
        # Decode the generated tokens
        generated_text = self.tokenizer.decode(generated_tokens)
        
        return generated_text
    
    def save_model(self, filepath):
        """
        Save the trained model and tokenizer to disk.
        """
        model_data = {
            'model_state': self.model,
            'tokenizer': self.tokenizer,
            'config': {
                'vocab_size': self.vocab_size,
                'embed_dim': self.embed_dim,
                'num_heads': self.num_heads,
                'ff_dim': self.ff_dim,
                'num_layers': self.num_layers,
                'max_seq_len': self.max_seq_len
            }
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """
        Load a trained model and tokenizer from disk.
        """
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model_state']
        self.tokenizer = model_data['tokenizer']
        config = model_data['config']
        
        # Update config
        self.vocab_size = config['vocab_size']
        self.embed_dim = config['embed_dim']
        self.num_heads = config['num_heads']
        self.ff_dim = config['ff_dim']
        self.num_layers = config['num_layers']
        self.max_seq_len = config['max_seq_len']
        
        # Reinitialize trainer
        self.trainer = Trainer(self.model)
        
        print(f"Model loaded from {filepath}")


def main():
    """
    Main function demonstrating the usage of the Generative AI Interface.
    """
    print("Initializing Generative AI...")
    
    # Create interface with a smaller initial vocab size to match our sample data
    ai = GenerativeAIInterface(
        vocab_size=128,  # Start with a smaller vocabulary size
        embed_dim=64,
        num_heads=4,
        ff_dim=128,
        num_layers=2,
        max_seq_len=32
    )
    
    # Sample training data
    sample_texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Machine learning is a subset of artificial intelligence.",
        "Deep learning models can learn complex patterns from data.",
        "Natural language processing enables computers to understand human language.",
        "Transformers are powerful models for sequence processing.",
        "The sun rises in the east and sets in the west.",
        "Water boils at 100 degrees Celsius at sea level.",
        "Programming requires logical thinking and problem solving skills.",
        "The internet has revolutionized how we communicate and access information.",
        "Exercise and a healthy diet are important for physical well-being."
    ]
    
    print("\nTraining the model...")
    ai.train_on_texts(sample_texts, epochs=5, learning_rate=0.001, batch_size=4)
    
    print("\nGenerating text with the trained model...")
    
    # Generate text with different prompts
    prompts = ["", "The", "Machine", "Deep"]
    
    for prompt in prompts:
        print(f"\nPrompt: '{prompt}'")
        generated = ai.generate_text(prompt, max_length=20, temperature=0.8)
        print(f"Generated: '{generated}'")
    
    print("\nTraining completed and text generation demonstrated!")


if __name__ == "__main__":
    main()