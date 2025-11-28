import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import math
from typing import List, Tuple, Optional, Dict

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model: int, num_heads: int):
        super(MultiHeadAttention, self).__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        
    def scaled_dot_product_attention(self, Q, K, V, mask=None):
        attn_scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        if mask is not None:
            attn_scores.masked_fill_(mask == 0, -1e9)
        attn_weights = torch.softmax(attn_scores, dim=-1)
        output = torch.matmul(attn_weights, V)
        return output
    
    def split_heads(self, x):
        batch_size, seq_length, d_model = x.size()
        return x.view(batch_size, seq_length, self.num_heads, self.d_k).transpose(1, 2)
    
    def combine_heads(self, x):
        batch_size, _, seq_length, d_k = x.size()
        return x.transpose(1, 2).contiguous().view(batch_size, seq_length, self.d_model)
    
    def forward(self, Q, K, V, mask=None):
        Q = self.split_heads(self.W_q(Q))
        K = self.split_heads(self.W_k(K))
        V = self.split_heads(self.W_v(V))
        
        attn_output = self.scaled_dot_product_attention(Q, K, V, mask)
        output = self.W_o(self.combine_heads(attn_output))
        return output

class PositionWiseFeedForward(nn.Module):
    def __init__(self, d_model: int, d_ff: int):
        super(PositionWiseFeedForward, self).__init__()
        self.fc1 = nn.Linear(d_model, d_ff)
        self.fc2 = nn.Linear(d_ff, d_model)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        return self.fc2(self.relu(self.fc1(x)))

class EncoderLayer(nn.Module):
    def __init__(self, d_model: int, num_heads: int, d_ff: int, dropout: float = 0.1):
        super(EncoderLayer, self).__init__()
        self.self_attn = MultiHeadAttention(d_model, num_heads)
        self.feed_forward = PositionWiseFeedForward(d_model, d_ff)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, mask=None):
        attn_output = self.self_attn(x, x, x, mask)
        x = self.norm1(x + self.dropout(attn_output))
        ff_output = self.feed_forward(x)
        x = self.norm2(x + self.dropout(ff_output))
        return x

class DecoderLayer(nn.Module):
    def __init__(self, d_model: int, num_heads: int, d_ff: int, dropout: float = 0.1):
        super(DecoderLayer, self).__init__()
        self.self_attn = MultiHeadAttention(d_model, num_heads)
        self.cross_attn = MultiHeadAttention(d_model, num_heads)
        self.feed_forward = PositionWiseFeedForward(d_model, d_ff)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.norm3 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, encoder_output, src_mask=None, tgt_mask=None):
        attn_output = self.self_attn(x, x, x, tgt_mask)
        x = self.norm1(x + self.dropout(attn_output))
        
        attn_output = self.cross_attn(x, encoder_output, encoder_output, src_mask)
        x = self.norm2(x + self.dropout(attn_output))
        
        ff_output = self.feed_forward(x)
        x = self.norm3(x + self.dropout(ff_output))
        return x

class PositionalEncoding(nn.Module):
    def __init__(self, d_model: int, max_seq_length: int):
        super(PositionalEncoding, self).__init__()
        pe = torch.zeros(max_seq_length, d_model)
        position = torch.arange(0, max_seq_length, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * 
                            (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe.unsqueeze(0))
    
    def forward(self, x):
        return x + self.pe[:, :x.size(1)]

class Transformer(nn.Module):
    def __init__(self, src_vocab_size: int, tgt_vocab_size: int, d_model: int, 
                 num_heads: int, num_layers: int, d_ff: int, max_seq_length: int, 
                 dropout: float = 0.1):
        super(Transformer, self).__init__()
        self.encoder_embedding = nn.Embedding(src_vocab_size, d_model)
        self.decoder_embedding = nn.Embedding(tgt_vocab_size, d_model)
        self.positional_encoding = PositionalEncoding(d_model, max_seq_length)
        
        self.encoder_layers = nn.ModuleList([
            EncoderLayer(d_model, num_heads, d_ff, dropout) 
            for _ in range(num_layers)
        ])
        
        self.decoder_layers = nn.ModuleList([
            DecoderLayer(d_model, num_heads, d_ff, dropout) 
            for _ in range(num_layers)
        ])
        
        self.fc_out = nn.Linear(d_model, tgt_vocab_size)
        self.dropout = nn.Dropout(dropout)
        
    def generate_mask(self, src, tgt):
        src_mask = (src != 0).unsqueeze(1).unsqueeze(2)
        tgt_mask = (tgt != 0).unsqueeze(1).unsqueeze(3)
        seq_length = tgt.size(1)
        nopeak_mask = (1 - torch.triu(torch.ones(1, seq_length, seq_length), diagonal=1)).bool()
        tgt_mask = tgt_mask & nopeak_mask
        return src_mask, tgt_mask
    
    def forward(self, src, tgt):
        src_mask, tgt_mask = self.generate_mask(src, tgt)
        
        src_embedded = self.dropout(self.positional_encoding(self.encoder_embedding(src)))
        tgt_embedded = self.dropout(self.positional_encoding(self.decoder_embedding(tgt)))
        
        enc_output = src_embedded
        for enc_layer in self.encoder_layers:
            enc_output = enc_layer(enc_output, src_mask)
        
        dec_output = tgt_embedded
        for dec_layer in self.decoder_layers:
            dec_output = dec_layer(dec_output, enc_output, src_mask, tgt_mask)
        
        output = self.fc_out(dec_output)
        return output

class Tokenizer:
    def __init__(self):
        self.vocab = {"<PAD>": 0, "<UNK>": 1, "<SOS>": 2, "<EOS>": 3}
        self.reverse_vocab = {0: "<PAD>", 1: "<UNK>", 2: "<SOS>", 3: "<EOS>"}
        self.current_idx = 4
    
    def build_vocab(self, texts: List[str]):
        for text in texts:
            for word in text.split():
                if word not in self.vocab:
                    self.vocab[word] = self.current_idx
                    self.reverse_vocab[self.current_idx] = word
                    self.current_idx += 1
    
    def encode(self, text: str) -> List[int]:
        tokens = [self.vocab.get(word, self.vocab["<UNK>"]) for word in text.split()]
        return [self.vocab["<SOS>"]] + tokens + [self.vocab["<EOS>"]]
    
    def decode(self, tokens: List[int]) -> str:
        words = [self.reverse_vocab.get(token, "<UNK>") for token in tokens]
        return " ".join([word for word in words if word not in ["<SOS>", "<EOS>", "<PAD>"]])

class AITrainingEvaluator:
    def __init__(self):
        self.metrics = {}
    
    def evaluate_model_performance(self, model: nn.Module, test_data: List[Tuple[str, str]], tokenizer: Tokenizer) -> Dict:
        """Evaluate model performance and return metrics"""
        model.eval()
        total_loss = 0.0
        total_correct = 0
        total_tokens = 0
        
        criterion = nn.CrossEntropyLoss(ignore_index=0)  # Ignore padding
        
        with torch.no_grad():
            for src_text, tgt_text in test_data:
                src_tokens = torch.tensor([tokenizer.encode(src_text)])
                tgt_tokens = torch.tensor([tokenizer.encode(tgt_text)])
                
                # Shift target for teacher forcing
                tgt_input = tgt_tokens[:, :-1]
                tgt_output = tgt_tokens[:, 1:]
                
                output = model(src_tokens, tgt_input)
                
                loss = criterion(output.view(-1, output.size(-1)), tgt_output.view(-1))
                total_loss += loss.item()
                
                # Calculate accuracy
                predictions = output.argmax(dim=-1)
                correct = (predictions == tgt_output).sum().item()
                total_correct += correct
                total_tokens += tgt_output.numel()
        
        avg_loss = total_loss / len(test_data)
        accuracy = total_correct / total_tokens if total_tokens > 0 else 0
        
        # Additional metrics
        perplexity = math.exp(avg_loss) if avg_loss < 100 else float('inf')
        
        self.metrics = {
            "avg_loss": avg_loss,
            "accuracy": accuracy,
            "perplexity": perplexity,
            "total_samples": len(test_data)
        }
        
        return self.metrics
    
    def is_quality_positive(self, metrics: Dict) -> bool:
        """Check if model quality is positive based on metrics"""
        # Define quality thresholds
        min_accuracy = 0.7
        max_perplexity = 10.0
        
        return (metrics.get("accuracy", 0) >= min_accuracy and 
                metrics.get("perplexity", float('inf')) <= max_perplexity)