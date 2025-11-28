"""
EmotionalQuantumField: Квантовая эмоциональная система
"""
import json
import numpy as np
from typing import Dict, Any, List
import math


class EmotionalQuantumField:
    def __init__(self, config_path: str):
        """
        Инициализация квантового эмоционального поля
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.base_emotions = list(self.config['base_emotions'].keys())
        self.n_emotions = len(self.base_emotions)
        
        # Создание матрицы взаимовлияний эмоций (24x24)
        self.emotion_matrix = np.random.rand(self.n_emotions, self.n_emotions) * 0.1
        np.fill_diagonal(self.emotion_matrix, 1.0)  # Диагональные элементы = 1 для самовлияния
        
        # Инициализация волновой функции (суперпозиция эмоций)
        self.psi = np.zeros(self.n_emotions, dtype=complex)
        self.psi[0] = 1.0  # Начальное состояние - первая эмоция доминирует
        
        # Нейротрансмиттерные влияния
        self.neurotransmitter_effects = {
            'dopamine': {'joy': 0.8, 'anticipation': 0.6, 'fear': -0.3},
            'serotonin': {'joy': 0.7, 'trust': 0.5, 'sadness': -0.6},
            'norepinephrine': {'fear': 0.8, 'surprise': 0.7, 'anger': 0.5},
            'gaba': {'fear': -0.7, 'anger': -0.5, 'joy': 0.2},
            'acetylcholine': {'surprise': 0.7, 'anticipation': 0.6, 'confusion': -0.4},
            'endorphins': {'joy': 0.9, 'pain': -0.8, 'contentment': 0.8},
            'oxytocin': {'love': 0.9, 'trust': 0.8, 'fear': -0.4}
        }
        
        # Параметры системы
        self.superposition_depth = 5
        self.collapse_threshold = 0.7
        self.hbar = 1.0  # Редуцированная постоянная Планка (условная единица)

    def update_state(self, stimulus: Dict[str, Any], neurotransmitters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обновление эмоционального состояния на основе стимула и нейротрансмиттеров
        """
        # Определение типа стимула и его влияния
        stimulus_type = stimulus.get('type', 'neutral')
        stimulus_intensity = stimulus.get('intensity', 0.5)
        
        # Обновление волновой функции на основе стимула
        stimulus_emotion_idx = self._get_emotion_index_from_stimulus(stimulus_type)
        if stimulus_emotion_idx is not None:
            # Влияние стимула на волновую функцию
            self._apply_stimulus_to_wavefunction(stimulus_emotion_idx, stimulus_intensity)
        
        # Применение нейротрансмиттерных эффектов
        self._apply_neurotransmitter_effects(neurotransmitters)
        
        # Временная эволюция по уравнению Шрёдингера
        self._time_evolution()
        
        # Проверка коллапса волновой функции при наблюдении
        observation_strength = stimulus.get('observer_effect', 0.0)
        if observation_strength > self.collapse_threshold:
            self._collapse_wavefunction(observation_strength)
        
        return self._get_current_emotional_state()

    def _get_emotion_index_from_stimulus(self, stimulus_type: str) -> int:
        """
        Получение индекса эмоции на основе типа стимула
        """
        if stimulus_type in self.config['emotional_triggers']:
            emotion_name = self.config['emotional_triggers'][stimulus_type]['emotion']
            if emotion_name in self.base_emotions:
                return self.base_emotions.index(emotion_name)
        return None

    def _apply_stimulus_to_wavefunction(self, emotion_idx: int, intensity: float):
        """
        Применение влияния стимула к волновой функции
        """
        # Усиление амплитуды определенной эмоции
        self.psi[emotion_idx] += intensity * 0.5
        # Нормализация волновой функции
        norm = np.linalg.norm(self.psi)
        if norm > 0:
            self.psi /= norm

    def _apply_neurotransmitter_effects(self, neurotransmitters: Dict[str, Any]):
        """
        Применение влияния нейротрансмиттеров к волновой функции
        """
        for nt_name, level in neurotransmitters.items():
            if nt_name in self.neurotransmitter_effects:
                effects = self.neurotransmitter_effects[nt_name]
                for emotion_name, effect_strength in effects.items():
                    if emotion_name in self.base_emotions:
                        emotion_idx = self.base_emotions.index(emotion_name)
                        # Применение эффекта нейротрансмиттера к волновой функции
                        self.psi[emotion_idx] += level * effect_strength * 0.1
        
        # Нормализация после всех изменений
        norm = np.linalg.norm(self.psi)
        if norm > 0:
            self.psi /= norm

    def _time_evolution(self):
        """
        Временная эволюция волновой функции по уравнению Шрёдингера
        iℏ ∂ψ/∂t = Hψ
        """
        # Простая модель гамильтониана (в реальности была бы более сложной)
        H = np.random.rand(self.n_emotions, self.n_emotions) + 1j * np.random.rand(self.n_emotions, self.n_emotions)
        H = (H + np.conj(H.T)) / 2  # Сделать эрмитовым
        
        # Временной шаг
        dt = 0.01
        # Эволюция: psi(t+dt) = exp(-i*H*dt/hbar) * psi(t)
        U = scipy.linalg.expm(-1j * H * dt / self.hbar)  # Используем унитарный оператор
        self.psi = U @ self.psi
        
        # Нормализация
        norm = np.linalg.norm(self.psi)
        if norm > 0:
            self.psi /= norm

    def _collapse_wavefunction(self, observer_effect: float):
        """
        Коллапс волновой функции при наблюдении
        """
        # Вероятности для каждой эмоции (квадрат модуля амплитуды)
        probabilities = np.abs(self.psi) ** 2
        
        # Выбор эмоции на основе вероятностей
        chosen_idx = np.random.choice(len(probabilities), p=probabilities)
        
        # Коллапс к определенному состоянию
        new_psi = np.zeros_like(self.psi)
        new_psi[chosen_idx] = 1.0
        self.psi = new_psi

    def get_current_superposition(self) -> Dict[str, Any]:
        """
        Получение текущей суперпозиции эмоций
        """
        probabilities = np.abs(self.psi) ** 2
        emotion_probs = {}
        for i, emotion in enumerate(self.base_emotions):
            emotion_probs[emotion] = float(probabilities[i])
        
        return {
            'emotions': emotion_probs,
            'dominant_emotion': self.base_emotions[np.argmax(probabilities)],
            'dominant_probability': float(np.max(probabilities)),
            'superposition_level': float(np.sum(probabilities[probabilities > 0.01])),  # Уровень суперпозиции
            'entropy': float(-np.sum(probabilities * np.log(probabilities + 1e-10)))  # Энтропия
        }

    def apply_observation(self, observer_effect: float) -> Dict[str, Any]:
        """
        Применение эффекта наблюдения, вызывающего коллапс
        """
        if observer_effect > self.collapse_threshold:
            self._collapse_wavefunction(observer_effect)
        
        return self.get_current_superposition()

    def calculate_emotional_entropy(self) -> float:
        """
        Расчет эмоциональной энтропии
        """
        probabilities = np.abs(self.psi) ** 2
        entropy = -np.sum(probabilities * np.log(probabilities + 1e-10))
        return float(entropy)

    def _get_current_emotional_state(self) -> Dict[str, Any]:
        """
        Получение полного текущего эмоционального состояния
        """
        superposition = self.get_current_superposition()
        
        # Расчет валидности, возбуждения и доминирования для доминирующей эмоции
        dominant_emotion = superposition['dominant_emotion']
        emotion_data = self.config['base_emotions'].get(dominant_emotion, {})
        
        return {
            'dominant_emotion': dominant_emotion,
            'intensity': superposition['dominant_probability'],
            'valence': emotion_data.get('valence', 0.0),
            'arousal': emotion_data.get('arousal', 0.0),
            'dominance': emotion_data.get('dominance', 0.0),
            'superposition_state': superposition,
            'emotional_entropy': self.calculate_emotional_entropy(),
            'coherence': float(np.sum(np.abs(self.psi)**2))  # Уровень когерентности
        }


import scipy.linalg