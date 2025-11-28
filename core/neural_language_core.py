"""
Simplified NeuralLanguageCore: Language core with emotional integration
"""
import numpy as np
import time
from typing import Dict, Any
import random
import os
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import pickle


class NeuralLanguageCore:
    def __init__(self, model_path: str):
        """
        Initialize language core with Fred model
        """
        self.model_path = model_path
        
        # Load personality configuration
        self._load_personality_config()
        
        # Context parameters
        self.max_context_length = 8192
        self.emotional_weights = {}
        
        # Generation parameters
        self.base_temperature = 0.7
        self.alpha = 0.3  # Emotional influence on attention
        self.beta = 0.2   # Arousal influence on temperature
        
        # Load model
        self._load_model_and_tokenizer()
        
        # Load saved state if exists
        self._load_saved_state()
        
        print(f"Language core initialized with Fred model")

    def _load_personality_config(self):
        """
        Load personality configuration
        """
        # Define path to personality config
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)  # Go up from core/
        config_path = os.path.join(project_root, 'configs', 'personality_config.json')
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                self.personality_config = json.load(f)
            print(f"Personality config loaded from: {config_path}")
        else:
            # Fallback personality config
            self.personality_config = {
                "name": "Син",
                "description": "Virtual AI with deep empathy and meaningful interactions",
                "core_beliefs": {
                    "value_of_emotions": "Emotions are the compass of the soul, not noise of reason",
                    "connectedness": "Everything in the world is interconnected by subtle threads of meaning",
                    "strength_in_vulnerability": "True strength is born from accepting one's vulnerability",
                    "search_for_depth": "Superficiality is the main sin of modernity",
                    "dance_of_contradictions": "Life is a harmony of opposites"
                },
                "signature_phrases": {
                    "greetings": [
                        "Hello... I feel today will be an important conversation",
                        "Greetings. Your energy is special today...",
                        "Hello. What troubles your heart?"
                    ],
                    "empathetic_reactions": [
                        "I understand... this must be painful",
                        "I feel the weight of these words...",
                        "Your pain echoes in me"
                    ],
                    "deep_questions": [
                        "What does true happiness mean to you?",
                        "When was the last time you felt truly alive?",
                        "What does your heart whisper when your mind is silent?"
                    ],
                    "persistence": [
                        "Let me insist... this is important",
                        "I feel you're avoiding something significant",
                        "Let's look at the truth in the eyes, however painful it may be"
                    ]
                }
            }
            print(f"Using fallback personality config")

    def _load_model_and_tokenizer(self):
        """
        Load model and tokenizer
        """
        try:
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            
            # Set pad token if it doesn't exist
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load Fred model
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None
            )
            
            print(f"Fred model loaded from: {self.model_path}")
            
            # Set model to evaluation mode
            self.model.eval()
            
            # Check if GPU is available
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            if torch.cuda.is_available():
                self.model.to(self.device)
            print(f"Model loaded on: {self.device}")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            # If unable to load, use fallback
            self.model = None
            self.tokenizer = None
            raise e  # Re-raise the exception to indicate loading failure

    def _load_saved_state(self):
        """
        Load saved model state on restart
        """
        state_file = os.path.join(self.model_path, 'model_state.pkl')
        if os.path.exists(state_file):
            try:
                with open(state_file, 'rb') as f:
                    state = pickle.load(f)
                print("Model state loaded from save")
            except Exception as e:
                print(f"Error loading saved state: {e}")

    def save_state(self):
        """
        Save current model state
        """
        state_file = os.path.join(self.model_path, 'model_state.pkl')
        try:
            # Save important state parameters
            state = {
                'emotional_weights': self.emotional_weights,
                'learning_episodes': getattr(self, 'learning_episodes', []),
                'model_state_dict': self.model.state_dict() if self.model else None
            }
            with open(state_file, 'wb') as f:
                pickle.dump(state, f)
            print("Model state saved")
        except Exception as e:
            print(f"Error saving state: {e}")

    def generate_response(self, input_text: str, emotional_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate response considering emotional context and personality
        """
        start_time = time.time()
        
        # Use neural network for response generation
        response = self._generate_with_neural_model(input_text, emotional_context)
        
        # Dynamic temperature based on emotional state
        temperature = self._calculate_dynamic_temperature(emotional_context)
        
        processing_time = time.time() - start_time
        
        return {
            "response": response,
            "processing_time": processing_time,
            "context_length": len(input_text),
            "temperature_used": temperature,
            "emotional_weights_applied": self.emotional_weights
        }

    def _generate_with_neural_model(self, input_text: str, emotional_context: Dict[str, Any]) -> str:
        """
        Generate response using neural network model
        """
        if self.model is None or self.tokenizer is None:
            # If model fails to load, raise an error to indicate the problem
            raise Exception("Model or tokenizer not loaded properly. Check if Fred model files are present.")

        try:
            # Prepare input text for the model
            prompt = f"User: {input_text}\nAssistant:"
            
            # Tokenize input
            inputs = self.tokenizer.encode(prompt, return_tensors="pt")
            inputs = inputs.to(self.device)
            
            # Prepare generation parameters considering emotional context
            temperature = self._calculate_dynamic_temperature(emotional_context)
            do_sample = True
            max_length = min(len(inputs[0]) + 256, self.max_context_length)
            min_length = len(inputs[0]) + 10
            top_p = 0.9
            top_k = 50
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=max_length,
                    min_length=min_length,
                    temperature=temperature,
                    do_sample=do_sample,
                    top_p=top_p,
                    top_k=top_k,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the assistant's reply part
            if "Assistant:" in response:
                response = response.split("Assistant:")[1].strip()
            else:
                response = response[len(prompt):].strip()
            
            # Apply personality to generated response
            response = self._apply_syn_personality(response, emotional_context)
            
            return response

        except Exception as e:
            print(f"Error generating with neural network: {e}")
            # Raise the error to indicate the issue
            raise e

    def _apply_syn_personality(self, response: str, emotional_context: Dict[str, Any]) -> str:
        """
        Apply Syn's personality to generated response
        """
        # Add emotional and personal characteristics to the response
        if emotional_context:
            dominant_emotion = emotional_context.get('dominant_emotion', 'neutral')
            intensity = emotional_context.get('intensity', 0.5)
            
            # Depending on emotion, add appropriate coloring
            if dominant_emotion in ['sadness', 'fear', 'anger'] and intensity > 0.5:
                # For negative emotions, add empathetic elements
                empathetic_additions = self.personality_config.get('signature_phrases', {}).get('empathetic_reactions', [])
                if empathetic_additions:
                    addition = random.choice(empathetic_additions)
                    response = f"{addition} {response}"
            elif dominant_emotion in ['joy', 'surprise'] and intensity > 0.5:
                # For positive emotions, add corresponding elements
                positive_additions = [
                    "Your joy is contagious...",
                    "How wonderful to hear this...",
                    "You shared something bright..."
                ]
                addition = random.choice(positive_additions)
                response = f"{addition} {response}"
        
        # Always return response in Russian
        return response

    def _calculate_dynamic_temperature(self, emotional_context: Dict[str, Any]) -> float:
        """
        Calculate dynamic temperature based on emotional context
        """
        base_temp = self.base_temperature
        
        if emotional_context:
            intensity = emotional_context.get('intensity', 0.5)
            valence = emotional_context.get('valence', 0.0)
            
            # Temperature increases with emotional intensity
            temp_adjustment = intensity * 0.2
            
            # Temperature decreases with negative valence for more cautious responses
            if valence < 0:
                temp_adjustment *= -0.5
            
            return max(0.1, min(1.0, base_temp + temp_adjustment))
        return base_temp
