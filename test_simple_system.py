#!/usr/bin/env python3
"""
Тестирование упрощенной системы Emotional AI
"""
import os
import sys
from core.neural_language_core import NeuralLanguageCore
from core.emotional_quantum_field import EmotionalQuantumField


def test_simple_system():
    print("Тестируем упрощенную систему Emotional AI...")
    
    # Определяем пути
    base_path = os.path.dirname(os.path.abspath(__file__))
    configs_path = os.path.join(base_path, 'configs')
    fred_path = os.path.join(base_path, 'FRED')
    
    print(f"Путь к конфигурациям: {configs_path}")
    print(f"Путь к модели Fred: {fred_path}")
    
    # Проверяем существование файлов
    if not os.path.exists(fred_path):
        print(f"Ошибка: директория FRED не найдена: {fred_path}")
        return False
    
    if not os.path.exists(configs_path):
        print(f"Ошибка: директория configs не найдена: {configs_path}")
        return False
    
    print("Конфигурации и модель найдены")
    
    # Инициализируем только основные компоненты
    try:
        print("Инициализация нейронного ядра...")
        neural_core = NeuralLanguageCore(fred_path)
        print("Нейронное ядро инициализировано успешно")
        
        print("Инициализация эмоционального поля...")
        emotion_config_path = os.path.join(configs_path, 'emotion_config.json')
        emotional_field = EmotionalQuantumField(emotion_config_path)
        print("Эмоциональное поле инициализировано успешно")
        
        # Тестируем генерацию ответа
        print("\nТестируем генерацию ответа...")
        test_input = "Привет, как дела?"
        emotional_context = {
            'dominant_emotion': 'joy',
            'intensity': 0.5,
            'valence': 0.3
        }
        
        response = neural_core.generate_response(test_input, emotional_context)
        print(f"Вход: {test_input}")
        print(f"Ответ: {response['response']}")
        print(f"Время обработки: {response['processing_time']:.2f} сек")
        
        return True
        
    except Exception as e:
        print(f"Ошибка при инициализации: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_simple_system()
    if success:
        print("\n✓ Тест упрощенной системы прошел успешно!")
    else:
        print("\n✗ Тест упрощенной системы завершился с ошибкой")
        sys.exit(1)