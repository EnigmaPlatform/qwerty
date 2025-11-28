"""
Тестирование интеграции модулей
"""
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import EmotionalAISystem


class TestIntegration(unittest.TestCase):
    def setUp(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.system = EmotionalAISystem(base_path)

    def test_system_initialization(self):
        """Тест инициализации всей системы"""
        self.assertIsNotNone(self.system)
        self.assertIsNotNone(self.system.neural_core)
        self.assertIsNotNone(self.system.emotional_field)
        self.assertIsNotNone(self.system.neurotransmitter_net)

    def test_health_check(self):
        """Тест проверки работоспособности системы"""
        health_status = self.system.health_check()
        
        self.assertIsNotNone(health_status)
        self.assertIn('neural_core', health_status)
        self.assertIn('emotional_field', health_status)

    def test_basic_interaction(self):
        """Тест базового взаимодействия"""
        # Проверяем, что система может обработать простой ввод
        response = self.system.process_interaction("Привет")
        
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)


if __name__ == '__main__':
    unittest.main()