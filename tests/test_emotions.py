"""
Тестирование эмоциональной системы
"""
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.emotional_quantum_field import EmotionalQuantumField


class TestEmotionalQuantumField(unittest.TestCase):
    def setUp(self):
        self.emotional_field = EmotionalQuantumField('configs/emotion_config.json')

    def test_initialization(self):
        """Тест инициализации эмоционального поля"""
        self.assertIsNotNone(self.emotional_field)
        self.assertEqual(len(self.emotional_field.base_emotions), 24)

    def test_emotional_state_update(self):
        """Тест обновления эмоционального состояния"""
        stimulus = {'type': 'compliment', 'intensity': 0.8}
        neurotransmitters = {'dopamine': 0.7, 'serotonin': 0.6}
        
        result = self.emotional_field.update_state(stimulus, neurotransmitters)
        
        self.assertIsNotNone(result)
        self.assertIn('dominant_emotion', result)
        self.assertIn('intensity', result)

    def test_superposition_state(self):
        """Тест получения суперпозиции состояний"""
        superposition = self.emotional_field.get_current_superposition()
        
        self.assertIsNotNone(superposition)
        self.assertIn('emotions', superposition)
        self.assertIn('dominant_emotion', superposition)

    def test_emotional_entropy(self):
        """Тест расчета эмоциональной энтропии"""
        entropy = self.emotional_field.calculate_emotional_entropy()
        
        self.assertIsInstance(entropy, float)
        self.assertGreaterEqual(entropy, 0.0)


if __name__ == '__main__':
    unittest.main()