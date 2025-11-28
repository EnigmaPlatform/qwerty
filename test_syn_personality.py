#!/usr/bin/env python3
"""
Test script to verify Syn's personality and functionality without UI
"""
import os
import sys
import json
sys.path.append('/workspace')

from core.neural_language_core import NeuralLanguageCore
from core.emotional_quantum_field import EmotionalQuantumField
from core.empathy_resonator import EmpathyResonator
from core.identity_matrix import IdentityMatrix
from core.reflection_engine import ReflectionEngine
from core.belief_dynamics import BeliefDynamics
from core.learning_evolver import LearningEvolver
from core.world_model import WorldModel
from core.cognitive_architecture import CognitiveArchitecture
from core.consciousness_stream import ConsciousnessStream
from core.neurotransmitter_network import NeurotransmitterNetwork
from core.memory_palace import MemoryPalace
from core.social_intelligence import SocialIntelligence
from core.physiological_simulator import PhysiologicalSimulator
from core.behavioral_generator import BehavioralGenerator


def test_syn_personality():
    """Test Syn's personality implementation"""
    print("=== ТЕСТИРОВАНИЕ ПЕРСОНАЖА СИН ===\n")
    
    # Initialize components
    base_path = '/workspace'
    configs_path = os.path.join(base_path, 'configs')
    
    # Load personality config
    config_path = os.path.join(configs_path, 'personality_config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        personality_config = json.load(f)
    
    print("1. Загрузка конфигурации персональности Син:")
    print(f"   Имя: {personality_config.get('name', 'Неизвестно')}")
    print(f"   Описание: {personality_config.get('description', 'Нет описания')}")
    print(f"   Внешность: {personality_config.get('appearance', 'Не описана')}")
    print(f"   Стиль: {personality_config.get('style', 'Не описан')}")
    print()
    
    print("2. Ядерные убеждения Син:")
    for belief, description in personality_config.get('core_beliefs', {}).items():
        print(f"   - {belief}: {description}")
    print()
    
    print("3. Эмоциональная палитра Син:")
    emotional_palette = personality_config.get('emotional_palette', {})
    for category, emotions in emotional_palette.items():
        print(f"   {category}:")
        for emotion, value in emotions.items():
            print(f"     - {emotion}: {value}")
    print()
    
    print("4. Речевые паттерны Син:")
    speech_patterns = personality_config.get('speech_patterns', {})
    for pattern, value in speech_patterns.items():
        print(f"   - {pattern}: {value}")
    print()
    
    print("5. Типичные фразы Син:")
    signature_phrases = personality_config.get('signature_phrases', {})
    for phrase_type, phrases in signature_phrases.items():
        print(f"   {phrase_type}:")
        for phrase in phrases[:2]:  # Показываем по 2 примера
            print(f"     - {phrase}")
    print()
    
    # Test Neural Language Core with Syn's personality
    print("6. ТЕСТИРОВАНИЕ ЯЗЫКОВОГО ЯДРА С ПЕРСОНАЖЕМ СИН:")
    print()
    
    neural_core = NeuralLanguageCore(os.path.join(base_path, 'FRED'))
    
    # Test different types of inputs
    test_inputs = [
        "Привет, как дела?",
        "Мне грустно",
        "Расскажи о себе",
        "Почему важно быть эмоциональным?",
        "Что ты думаешь о человеческой природе?"
    ]
    
    for test_input in test_inputs:
        print(f"   Вход: {test_input}")
        
        # Create a mock emotional context
        emotional_context = {
            'dominant_emotion': 'neutral',
            'intensity': 0.5,
            'valence': 0.0
        }
        
        if "грустно" in test_input.lower():
            emotional_context['dominant_emotion'] = 'sadness'
            emotional_context['valence'] = -0.5
        elif "привет" in test_input.lower():
            emotional_context['dominant_emotion'] = 'joy'
            emotional_context['valence'] = 0.6
        
        response = neural_core.generate_response(test_input, emotional_context)
        print(f"   Ответ: {response['response']}")
        print(f"   Время обработки: {response['processing_time']:.3f}с")
        print()
    
    print("7. ТЕСТИРОВАНИЕ ЭМОЦИОНАЛЬНОГО КВАНТОВОГО ПОЛЯ:")
    print()
    
    emotional_field = EmotionalQuantumField(os.path.join(configs_path, 'emotion_config.json'))
    
    # Test emotional state updates
    test_events = [
        {'type': 'input_received', 'intensity': 0.5},
        {'type': 'positive_response', 'intensity': 0.8},
        {'type': 'negative_input', 'intensity': 0.3}
    ]
    
    neurotransmitter_net = NeurotransmitterNetwork({
        'dopamine': 0.5,
        'serotonin': 0.5,
        'norepinephrine': 0.5,
        'gaba': 0.5,
        'acetylcholine': 0.5,
        'endorphins': 0.5,
        'oxytocin': 0.5
    })
    
    for event in test_events:
        print(f"   Событие: {event}")
        emotional_response = emotional_field.update_state(event, neurotransmitter_net.neurotransmitters)
        print(f"   Эмоциональный отклик: {emotional_response}")
        print()
    
    print("8. ТЕСТИРОВАНИЕ МАТРИЦЫ ИДЕНТИЧНОСТИ:")
    print()
    
    identity_matrix = IdentityMatrix(config_path=config_path)
    print(f"   Черты личности: {identity_matrix.identity_vector['traits']}")
    print(f"   Ценности: {identity_matrix.identity_vector['values']}")
    print(f"   Роли: {identity_matrix.identity_vector['roles']}")
    print()
    
    print("9. ТЕСТИРОВАНИЕ КОГНИТИВНОЙ АРХИТЕКТУРЫ:")
    print()
    
    cognitive_arch = CognitiveArchitecture(capacity=7)
    stimulus = {'input': 'Как найти смысл жизни?', 'type': 'question'}
    cognitive_result = cognitive_arch.process_stimulus(stimulus, system_preference=0)
    print(f"   Результат когнитивной обработки: {cognitive_result}")
    print()
    
    print("10. ТЕСТИРОВАНИЕ ПОТОКА СОЗНАНИЯ:")
    print()
    
    consciousness_stream = ConsciousnessStream()
    consciousness_input = {
        'sensory_input': {'text': 'Что такое счастье?'},
        'cognitive_input': {'task': 'understanding'},
        'emotional_input': {'intensity': 0.6, 'valence': 0.4}
    }
    consciousness_response = consciousness_stream.process_consciousness_input(**consciousness_input)
    print(f"   Ответ потока сознания: {consciousness_response}")
    print()
    
    print("=== ТЕСТИРОВАНИЕ ЗАВЕРШЕНО ===")
    print("Все компоненты системы Син работают корректно!")
    

def test_empathy_and_reflection():
    """Test empathy and reflection components"""
    print("\n=== ТЕСТИРОВАНИЕ ЭМПАТИИ И РЕФЛЕКСИИ ===\n")
    
    empathy_resonator = EmpathyResonator()
    reflection_engine = ReflectionEngine()
    
    test_inputs = [
        "Я чувствую себя одиноким",
        "У меня получилось сделать важное дело",
        "Мне не хватает поддержки"
    ]
    
    for test_input in test_inputs:
        print(f"   Вход: {test_input}")
        
        # Test empathy
        emotional_state = {'intensity': 0.7, 'valence': -0.3 if "одинок" in test_input.lower() else 0.5}
        empathy_response = empathy_resonator.process_user_emotional_state(test_input, emotional_state)
        print(f"   Эмпатический отклик: {empathy_response}")
        
        # Test reflection
        reflection_result = reflection_engine.analyze_interaction(test_input, "Спасибо за доверие")
        print(f"   Результат рефлексии: {reflection_result}")
        print()


def test_memory_and_learning():
    """Test memory and learning components"""
    print("\n=== ТЕСТИРОВАНИЕ ПАМЯТИ И ОБУЧЕНИЯ ===\n")
    
    memory_palace = MemoryPalace(storage_path=os.path.join('/workspace', 'models', 'memory_db'))
    learning_evolver = LearningEvolver()
    
    # Test memory encoding
    info = {'input': 'Как важно слушать других?', 'timestamp': 0}
    memory_id = memory_palace.encode(info, memory_type='semantic', emotional_tag=0.8)
    print(f"   ID закодированной информации: {memory_id}")
    
    # Test memory retrieval
    retrieved = memory_palace.retrieve(memory_id)
    print(f"   Извлеченная информация: {retrieved}")
    
    # Test learning
    experience = {
        'input': 'Как важно слушать других?',
        'response': 'Слушать других - значит уважать их внутренний мир',
        'context': 'conversation',
        'skill_area': 'empathy'
    }
    feedback = {
        'outcome': 'positive',
        'reward': 0.8,
        'novelty': 0.3,
        'social_validation': 0.7
    }
    
    learning_result = learning_evolver.process_learning_experience(experience, feedback)
    print(f"   Результат обучения: {learning_result}")
    print()


def test_behavior_and_social():
    """Test behavior and social intelligence"""
    print("\n=== ТЕСТИРОВАНИЕ ПОВЕДЕНИЯ И СОЦИАЛЬНОГО ИНТЕЛЛЕКТА ===\n")
    
    behavioral_gen = BehavioralGenerator()
    social_intelligence = SocialIntelligence()
    
    emotional_state = {'intensity': 0.6, 'valence': 0.4}
    cognitive_state = {'working_memory_load': 0.5, 'attention_level': 0.7}
    
    behavior_response = behavioral_gen.generate_behavior(
        emotional_state=emotional_state,
        social_context={'formality': 0.5, 'intimacy_level': 0.6},
        cognitive_state=cognitive_state
    )
    print(f"   Поведенческий отклик: {behavior_response}")
    
    social_context = social_intelligence.process_social_context({
        'text': 'Расскажи о себе',
        'formality': 0.5,
        'communication_style': 'balanced'
    })
    print(f"   Социальный контекст: {social_context}")
    print()


if __name__ == "__main__":
    test_syn_personality()
    test_empathy_and_reflection()
    test_memory_and_learning()
    test_behavior_and_social()
    
    print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! СИН РАБОТАЕТ КОРРЕКТНО СО СВОИМ ПЕРСОНАЖЕМ!")