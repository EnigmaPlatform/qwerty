# Emotional AI System

## Overview
This is an advanced emotional AI system with multiple interconnected modules that simulate human-like cognitive and emotional processes.

## New UI Features
- **Hacker-style UI**: Dark theme with neon green text in a cyberpunk/hacker aesthetic
- **Tabbed Interface**: 
  - Chat interface for interacting with the AI
  - Training interface for supervised learning
  - Metrics dashboard to monitor system performance
- **Automatic Path Detection**: The system automatically finds all required files (models, configs, etc.) without hardcoded paths

## Key Features

### 1. Automatic Path Detection
The system automatically detects the locations of:
- FRED model files (config.json, model.bin, tokenizer.json)
- Configuration files (emotion_config.json, personality_config.json)
- Memory database directory
- All other required resources

### 2. UI Interface
The system now launches with a hacker-style UI when you run `python main.py`:
- **Dark theme** with **neon green text** in a cyberpunk aesthetic
- **Three main tabs**:
  - **Chat**: Real-time interaction with the emotional AI
  - **Training**: Supervised learning interface where you can provide input-output pairs for training
  - **Metrics**: System health and performance monitoring

### 3. Training Capabilities
- Supervised learning through the training interface
- Ability to provide expected outputs for specific inputs
- Real-time system improvement based on training data

### 4. Comprehensive Metrics
- System health monitoring
- Performance metrics tracking
- Interaction statistics
- Emotional and cognitive load analysis

## Usage

### Running the Application
```bash
python main.py
```

### Interacting with the UI
1. **Chat Tab**: Type messages in the input field and click "ОТПРАВИТЬ" or press Enter
2. **Training Tab**: Enter input text and expected output, then click "НАЧАТЬ ОБУЧЕНИЕ"
3. **Metrics Tab**: Click "ОБНОВИТЬ МЕТРИКИ" to see current system status

### Health Check
Use the "ПРОВЕРКА СИСТЕМЫ" button in the Chat tab to verify all system modules are operational.

## Architecture
The system includes multiple interconnected modules:
- Neural Language Core
- Emotional Quantum Field
- Neurotransmitter Network
- Cognitive Architecture
- Identity Matrix
- Memory Palace
- Empathy Resonator
- Reflection Engine
- Belief Dynamics
- Social Intelligence
- Physiological Simulator
- Behavioral Generator
- Consciousness Stream
- Learning Evolver
- World Model

## Requirements
- Python 3.7+
- PyTorch
- Transformers
- NumPy
- Tkinter (GUI)

## License
This project is licensed under the terms specified in the original project.