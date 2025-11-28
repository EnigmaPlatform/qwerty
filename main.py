"""
Simplified implementation of main.py for Emotional AI System

This version focuses on:
1. Loading only the Fred model with emotional integration
2. Minimal dependencies
3. Core functionality for generating responses
4. Simple UI for interaction
"""
import os
import sys
import time
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
from core.neural_language_core import NeuralLanguageCore
from core.emotional_quantum_field import EmotionalQuantumField


class SimpleEmotionalAISystem:
    def __init__(self, base_path: str):
        execution_base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Initialize core modules
        self.init_modules(execution_base_path)

    def init_modules(self, execution_base_path: str):
        try:
            # Path to Fred model
            fred_path = os.path.join(execution_base_path, 'FRED')
            if not os.path.exists(fred_path):
                raise FileNotFoundError(f"Could not find Fred model in expected location: {fred_path}")
            
            # Initialize neural core with Fred model
            self.neural_core = NeuralLanguageCore(fred_path)
            
            # Initialize emotional system
            emotion_config_path = os.path.join(execution_base_path, 'configs', 'emotion_config.json')
            self.emotional_field = EmotionalQuantumField(emotion_config_path)
            
            print("Core modules loaded successfully")
            
        except Exception as e:
            print(f"Failed to initialize: {str(e)}")
            raise

    def process_interaction(self, user_input: str) -> str:
        """Main interaction processing loop"""
        start_time = time.time()
        
        try:
            # 1. Emotional processing of input
            emotional_response = self.emotional_field.update_state(
                {'type': 'input_received', 'intensity': 0.5},
                {}  # Simplified neurotransmitter state
            )
            
            # 2. Generate response considering all systems
            response = self.neural_core.generate_response(
                user_input, 
                emotional_context=emotional_response,
            )
            
            return response['response']
            
        except Exception as e:
            print(f"Interaction failed: {str(e)}")
            return "Произошла внутренняя ошибка обработки."

class SimpleEmotionalAIUI:
    def __init__(self, system: SimpleEmotionalAISystem):
        self.system = system
        self.root = tk.Tk()
        self.root.title("Emotional AI System - Син")
        self.root.geometry("800x600")
        
        # Set dark theme
        self.root.configure(bg='#0a0a0a')
        
        # Create UI elements
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#0a0a0a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Chat history display
        chat_label = tk.Label(main_frame, text="Чат с Син:", fg='#00ff00', bg='#0a0a0a', font=("Consolas", 12, "bold"))
        chat_label.pack(anchor=tk.W)
        
        self.chat_display = scrolledtext.ScrolledText(
            main_frame, 
            wrap=tk.WORD, 
            bg='#1a1a1a', 
            fg='#00ff00', 
            insertbackground='#00ff00',
            selectbackground='#005500',
            font=("Consolas", 10)
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Input frame
        input_frame = tk.Frame(main_frame, bg='#0a0a0a')
        input_frame.pack(fill=tk.X)
        
        # Input field
        input_label = tk.Label(input_frame, text="Ваше сообщение:", fg='#00ff00', bg='#0a0a0a', font=("Consolas", 10))
        input_label.pack(anchor=tk.W)
        
        self.user_input = tk.Entry(input_frame, bg='#1a1a1a', fg='#00ff00', insertbackground='#00ff00', font=("Consolas", 10))
        self.user_input.pack(fill=tk.X, pady=(0, 10))
        self.user_input.bind("<Return>", self.send_message)
        
        # Send button
        send_button = tk.Button(
            input_frame, 
            text="Отправить", 
            command=self.send_message,
            bg='#003300', 
            fg='#00ff00',
            activebackground='#005500',
            activeforeground='#00ff00',
            font=("Consolas", 10, "bold")
        )
        send_button.pack()
        
        # Add initial message
        self.add_to_chat("Син", "Привет... чувствую, сегодня будет важный разговор")
    
    def add_to_chat(self, sender, message):
        """Add message to chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def send_message(self, event=None):
        """Send user message and get response"""
        user_message = self.user_input.get().strip()
        if not user_message:
            return
        
        # Add user message to chat
        self.add_to_chat("Вы", user_message)
        self.user_input.delete(0, tk.END)
        
        # Get and add response
        try:
            response = self.system.process_interaction(user_message)
            self.add_to_chat("Син", response)
        except Exception as e:
            self.add_to_chat("Син", f"Ошибка: {str(e)}")
    
    def run(self):
        """Run the UI"""
        self.root.mainloop()


def main():
    # Determine project root
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    try:
        # Initialize system
        system = SimpleEmotionalAISystem(base_path)
        
        # Create and run UI
        ui = SimpleEmotionalAIUI(system)
        ui.run()
        
    except Exception as e:
        print(f"Ошибка инициализации системы: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()