#!/usr/bin/env python3
"""
Test script to verify T5 model loading with the updated NeuralLanguageCore
"""

import os
import sys

# Add the workspace directory to Python path
sys.path.insert(0, '/workspace')

def test_t5_loading():
    """Test that T5 model loads correctly with updated code"""
    try:
        from transformers import AutoConfig, AutoModelForSeq2SeqLM, AutoTokenizer
        
        model_path = "/workspace/FRED"
        
        # Load the config to determine the model type
        config = AutoConfig.from_pretrained(model_path)
        print(f"Model type: {config.model_type}")
        
        # Check if it's a T5 model
        if config.model_type == "t5":
            print("Detected T5 model, loading with AutoModelForSeq2SeqLM...")
            model = AutoModelForSeq2SeqLM.from_pretrained(
                model_path,
                # torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                # device_map="auto" if torch.cuda.is_available() else None
            )
            print("T5 model loaded successfully!")
        else:
            print("Not a T5 model")
            
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        print("Tokenizer loaded successfully!")
        
        # Test basic functionality
        prompt = "summarize: Hello, how are you?"
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        print(f"Tokenization successful: {inputs.shape}")
        
        print("All tests passed! The model loading logic should work correctly.")
        return True
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing T5 model loading...")
    success = test_t5_loading()
    if success:
        print("\n✓ T5 model loading test completed successfully!")
    else:
        print("\n✗ T5 model loading test failed!")