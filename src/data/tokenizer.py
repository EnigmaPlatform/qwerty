import numpy as np
import re
from collections import Counter, defaultdict


class SimpleTokenizer:
    """
    A simple tokenizer for converting text to tokens and vice versa.
    """
    def __init__(self):
        self.vocab = {}
        self.reverse_vocab = {}
        self.vocab_size = 0
        self.pad_token_id = 0
        self.unk_token_id = 1
        self.bos_token_id = 2
        self.eos_token_id = 3
        
    def build_vocab(self, texts, min_freq=1):
        """
        Build vocabulary from a list of texts.
        """
        # Initialize special tokens
        self.vocab = {
            '<PAD>': self.pad_token_id,
            '<UNK>': self.unk_token_id,
            '<BOS>': self.bos_token_id,
            '<EOS>': self.eos_token_id
        }
        
        # Count word frequencies
        word_counts = Counter()
        for text in texts:
            # Simple tokenization by whitespace and punctuation
            tokens = re.findall(r'\b\w+\b|[^\w\s]', text.lower())
            word_counts.update(tokens)
        
        # Add words that meet minimum frequency
        for word, count in word_counts.items():
            if count >= min_freq:
                self.vocab[word] = len(self.vocab)
        
        # Create reverse vocabulary
        self.reverse_vocab = {v: k for k, v in self.vocab.items()}
        self.vocab_size = len(self.vocab)
        
        print(f"Vocabulary built with {self.vocab_size} tokens")
    
    def encode(self, text, add_special_tokens=True):
        """
        Convert text to token IDs.
        """
        # Simple tokenization by whitespace and punctuation
        tokens = re.findall(r'\b\w+\b|[^\w\s]', text.lower())
        
        # Convert tokens to IDs
        token_ids = []
        if add_special_tokens:
            token_ids.append(self.bos_token_id)
        
        for token in tokens:
            token_ids.append(self.vocab.get(token, self.unk_token_id))
        
        if add_special_tokens:
            token_ids.append(self.eos_token_id)
        
        return np.array(token_ids, dtype=np.int32)
    
    def decode(self, token_ids):
        """
        Convert token IDs back to text.
        """
        tokens = []
        for token_id in token_ids:
            if token_id in self.reverse_vocab:
                token = self.reverse_vocab[token_id]
                if token not in ['<PAD>', '<BOS>', '<EOS>', '<UNK>']:
                    tokens.append(token)
            else:
                tokens.append('<UNK>')
        
        # Join tokens, adding spaces except for punctuation
        text = ""
        for i, token in enumerate(tokens):
            if re.match(r'[^\w\s]', token) and i > 0:  # Punctuation
                text += token
            else:  # Words
                if text:
                    text += " " + token
                else:
                    text += token
        
        return text
    
    def encode_batch(self, texts, max_length=None, padding='post'):
        """
        Encode a batch of texts to token IDs with padding.
        """
        encoded_batch = [self.encode(text) for text in texts]
        
        if max_length is None:
            max_length = max(len(ids) for ids in encoded_batch)
        
        # Pad sequences
        padded_batch = []
        for ids in encoded_batch:
            if len(ids) >= max_length:
                padded_ids = ids[:max_length]
            else:
                if padding == 'post':
                    padded_ids = np.pad(ids, (0, max_length - len(ids)), 
                                      mode='constant', constant_values=self.pad_token_id)
                else:  # pre
                    padded_ids = np.pad(ids, (max_length - len(ids), 0), 
                                      mode='constant', constant_values=self.pad_token_id)
            padded_batch.append(padded_ids)
        
        return np.array(padded_batch)


class CharacterTokenizer:
    """
    A character-level tokenizer for more fine-grained tokenization.
    """
    def __init__(self):
        self.char_to_idx = {}
        self.idx_to_char = {}
        self.vocab_size = 0
        self.pad_token_id = 0
        self.unk_token_id = 1
        self.bos_token_id = 2
        self.eos_token_id = 3
        
    def build_vocab(self, texts):
        """
        Build vocabulary from unique characters in texts.
        """
        # Initialize special tokens
        self.char_to_idx = {
            '<PAD>': self.pad_token_id,
            '<UNK>': self.unk_token_id,
            '<BOS>': self.bos_token_id,
            '<EOS>': self.eos_token_id
        }
        
        # Collect all unique characters
        all_chars = set()
        for text in texts:
            all_chars.update(text)
        
        # Add characters to vocabulary
        for char in sorted(all_chars):
            if char not in self.char_to_idx:
                self.char_to_idx[char] = len(self.char_to_idx)
        
        # Create reverse mapping
        self.idx_to_char = {v: k for k, v in self.char_to_idx.items()}
        self.vocab_size = len(self.char_to_idx)
        
        print(f"Character vocabulary built with {self.vocab_size} tokens")
    
    def encode(self, text, add_special_tokens=True):
        """
        Convert text to character token IDs.
        """
        token_ids = []
        if add_special_tokens:
            token_ids.append(self.bos_token_id)
        
        for char in text:
            token_ids.append(self.char_to_idx.get(char, self.unk_token_id))
        
        if add_special_tokens:
            token_ids.append(self.eos_token_id)
        
        return np.array(token_ids, dtype=np.int32)
    
    def decode(self, token_ids):
        """
        Convert character token IDs back to text.
        """
        chars = []
        for token_id in token_ids:
            if token_id in self.idx_to_char:
                char = self.idx_to_char[token_id]
                if char not in ['<PAD>', '<BOS>', '<EOS>', '<UNK>']:
                    chars.append(char)
            else:
                chars.append('<UNK>')
        
        return ''.join(chars)