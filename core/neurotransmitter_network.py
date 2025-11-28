"""
NeurotransmitterNetwork: Нейротрансмиттерная система
"""
import numpy as np
from typing import Dict, Any
import time


class NeurotransmitterNetwork:
    def __init__(self, initial_balance: Dict[str, float] = None):
        """
        Инициализация нейротрансмиттерной сети
        """
        # 7 основных нейротрансмиттерных систем
        self.neurotransmitters = {
            'dopamine': 0.5,    # Мотивация, удовольствие, вознаграждение
            'serotonin': 0.6,   # Настроение, сон, аппетит
            'norepinephrine': 0.4,  # Внимание, возбуждение, стресс
            'gaba': 0.5,        # Ингибирование, расслабление
            'acetylcholine': 0.5,   # Обучение, память, внимание
            'endorphins': 0.3,  # Обезболивание, удовольствие
            'oxytocin': 0.4     # Социальная связь, доверие
        }
        
        # Матрица взаимовлияний 7x7
        self.interaction_matrix = np.array([
            [ 1.0,  0.2,  0.3, -0.1,  0.2,  0.4,  0.5],  # dopamine
            [ 0.1,  1.0,  0.2,  0.3,  0.1,  0.2,  0.6],  # serotonin
            [ 0.4,  0.1,  1.0, -0.2,  0.3,  0.1,  0.2],  # norepinephrine
            [-0.3, -0.1, -0.4,  1.0, -0.2, -0.1, -0.1],  # gaba
            [ 0.2,  0.1,  0.3, -0.1,  1.0,  0.1,  0.3],  # acetylcholine
            [ 0.5,  0.3,  0.1, -0.1,  0.2,  1.0,  0.4],  # endorphins
            [ 0.3,  0.6,  0.2, -0.1,  0.4,  0.3,  1.0]   # oxytocin
        ])
        
        # Временные константы (в условных единицах)
        self.decay_constants = {
            'dopamine': 0.8,
            'serotonin': 0.9,
            'norepinephrine': 0.7,
            'gaba': 0.6,
            'acetylcholine': 0.5,
            'endorphins': 0.4,
            'oxytocin': 0.7
        }
        
        # Когнитивные влияния
        self.cognitive_impact = {
            'dopamine': {'motivation': 0.9, 'focus': 0.7, 'pleasure': 0.9},
            'serotonin': {'mood': 0.8, 'confidence': 0.7, 'anxiety': -0.6},
            'norepinephrine': {'alertness': 0.9, 'stress': 0.8, 'focus': 0.8},
            'gaba': {'calmness': 0.8, 'anxiety': -0.7, 'relaxation': 0.9},
            'acetylcholine': {'memory': 0.9, 'learning': 0.8, 'attention': 0.8},
            'endorphins': {'pain_relief': 0.9, 'pleasure': 0.8, 'stress': -0.6},
            'oxytocin': {'trust': 0.9, 'bonding': 0.9, 'social': 0.8}
        }
        
        # Обновление начальных значений, если предоставлены
        if initial_balance:
            for nt, level in initial_balance.items():
                if nt in self.neurotransmitters:
                    self.neurotransmitters[nt] = level
        
        # Параметры обучения
        self.plasticity_rate = 0.01
        self.last_update_time = time.time()

    def update_levels(self, emotional_input: Dict[str, Any], external_factors: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обновление уровней нейротрансмиттеров на основе эмоционального ввода и внешних факторов
        """
        current_time = time.time()
        time_delta = current_time - self.last_update_time
        self.last_update_time = current_time
        
        # Извлечение информации из эмоционального ввода
        dominant_emotion = emotional_input.get('dominant_emotion', 'neutral')
        emotion_intensity = emotional_input.get('intensity', 0.5)
        valence = emotional_input.get('valence', 0.0)
        arousal = emotional_input.get('arousal', 0.0)
        
        # Обновление уровней на основе эмоций
        for nt in self.neurotransmitters:
            # Базовое изменение на основе текущего уровня (распад)
            decay_factor = self.decay_constants[nt]
            self.neurotransmitters[nt] *= (1 - decay_factor * time_delta * 0.1)
            
            # Влияние эмоций
            emotion_effect = self._calculate_emotion_effect(nt, dominant_emotion, emotion_intensity, valence, arousal)
            self.neurotransmitters[nt] += emotion_effect * time_delta
            
            # Влияние других нейротрансмиттеров (через матрицу взаимодействий)
            nt_array = np.array(list(self.neurotransmitters.values()))
            interaction_effects = self.interaction_matrix @ nt_array
            idx = list(self.neurotransmitters.keys()).index(nt)
            self.neurotransmitters[nt] += interaction_effects[idx] * 0.01
            
            # Ограничение уровней в диапазоне [0, 1]
            self.neurotransmitters[nt] = max(0.0, min(1.0, self.neurotransmitters[nt]))
        
        # Применение внешних факторов
        if external_factors:
            for factor, effect in external_factors.items():
                if factor in self.neurotransmitters:
                    self.neurotransmitters[factor] += effect * 0.1
                    self.neurotransmitters[factor] = max(0.0, min(1.0, self.neurotransmitters[factor]))
        
        return self.neurotransmitters.copy()

    def _calculate_emotion_effect(self, neurotransmitter: str, emotion: str, intensity: float, valence: float, arousal: float) -> float:
        """
        Расчет влияния эмоции на конкретный нейротрансмиттер
        """
        # Простая модель влияния эмоций на нейротрансмиттеры
        emotion_effects = {
            'joy': {'dopamine': 0.3, 'serotonin': 0.2, 'endorphins': 0.3},
            'sadness': {'serotonin': -0.3, 'dopamine': -0.2, 'norepinephrine': -0.1},
            'anger': {'norepinephrine': 0.3, 'dopamine': 0.1, 'gaba': -0.2},
            'fear': {'norepinephrine': 0.4, 'gaba': 0.2, 'oxytocin': -0.1},
            'surprise': {'norepinephrine': 0.2, 'acetylcholine': 0.3, 'dopamine': 0.1},
            'disgust': {'serotonin': -0.2, 'dopamine': -0.1, 'gaba': 0.1},
            'trust': {'oxytocin': 0.4, 'serotonin': 0.2, 'dopamine': 0.1},
            'anticipation': {'dopamine': 0.3, 'norepinephrine': 0.2, 'acetylcholine': 0.2}
        }
        
        effect = 0.0
        if emotion in emotion_effects and neurotransmitter in emotion_effects[emotion]:
            effect = emotion_effects[emotion][neurotransmitter]
        
        # Модуляция интенсивностью и валентностью
        return effect * intensity * (1 + valence * 0.5)

    def get_cognitive_impact(self) -> Dict[str, Any]:
        """
        Получение когнитивного влияния текущих уровней нейротрансмиттеров
        """
        impact = {}
        
        for nt, level in self.neurotransmitters.items():
            if nt in self.cognitive_impact:
                nt_impacts = self.cognitive_impact[nt]
                for cognitive_domain, weight in nt_impacts.items():
                    if cognitive_domain not in impact:
                        impact[cognitive_domain] = 0.0
                    impact[cognitive_domain] += level * weight
        
        # Нормализация влияния в диапазон [-1, 1]
        for domain in impact:
            impact[domain] = max(-1.0, min(1.0, impact[domain]))
        
        return impact

    def apply_learning_modulation(self, reward: float):
        """
        Применение модуляции обучения на основе вознаграждения (дофаминовая система)
        """
        # Пластичность синапсов на основе вознаграждения
        dopamine_level = self.neurotransmitters['dopamine']
        
        # Увеличение пластичности при высоком уровне дофамина и положительном вознаграждении
        effective_plasticity = self.plasticity_rate * (1 + dopamine_level) * (1 + reward)
        
        # Простая модель синаптической пластичности
        # Влияние на матрицу взаимодействий
        for i in range(len(self.interaction_matrix)):
            for j in range(len(self.interaction_matrix[i])):
                # Увеличение связей при положительном вознаграждении
                delta = effective_plasticity * reward * 0.01
                self.interaction_matrix[i][j] += delta
                # Ограничение значений
                self.interaction_matrix[i][j] = max(-1.0, min(1.0, self.interaction_matrix[i][j]))

    def simulate_long_term_changes(self, time_period: int) -> Dict[str, Any]:
        """
        Симуляция долгосрочных изменений в системе
        """
        initial_levels = self.neurotransmitters.copy()
        
        # Простая симуляция на основе текущих тенденций
        for _ in range(time_period):
            # Имитация базовых физиологических процессов
            for nt in self.neurotransmitters:
                # Небольшие колебания
                fluctuation = np.random.normal(0, 0.01)
                self.neurotransmitters[nt] += fluctuation
                # Ограничение в диапазоне
                self.neurotransmitters[nt] = max(0.0, min(1.0, self.neurotransmitters[nt]))
        
        changes = {}
        for nt in self.neurotransmitters:
            changes[nt] = self.neurotransmitters[nt] - initial_levels[nt]
        
        return {
            'initial_levels': initial_levels,
            'final_levels': self.neurotransmitters.copy(),
            'changes': changes,
            'time_period': time_period
        }