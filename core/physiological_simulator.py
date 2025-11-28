"""
PhysiologicalSimulator: Физиологический симулятор
"""
from typing import Dict, Any
import numpy as np
import time


class PhysiologicalSimulator:
    def __init__(self):
        """
        Инициализация физиологического симулятора
        """
        # Основные физиологические параметры
        self.physiological_state = {
            'heart_rate': 70.0,           # уд/мин
            'breathing_rate': 12.0,       # вдохов/мин
            'skin_conductance': 0.5,      # условные единицы
            'muscle_tension': 0.3,        # 0-1
            'body_temperature': 36.6,     # градусы Цельсия
            'posture': 'neutral',         # поза
            'energy_level': 0.8,          # уровень энергии 0-1
            'fatigue_level': 0.2          # уровень усталости 0-1
        }
        
        # Влияние эмоций на физиологию
        self.emotion_physiology_map = {
            'joy': {
                'heart_rate': 5.0,      # небольшое увеличение
                'breathing_rate': 2.0,
                'skin_conductance': 0.2,
                'muscle_tension': -0.1,
                'body_temperature': 0.1
            },
            'sadness': {
                'heart_rate': -3.0,     # небольшое уменьшение
                'breathing_rate': -1.0,
                'skin_conductance': -0.1,
                'muscle_tension': 0.1,
                'body_temperature': -0.1
            },
            'anger': {
                'heart_rate': 15.0,     # значительное увеличение
                'breathing_rate': 8.0,
                'skin_conductance': 0.8,
                'muscle_tension': 0.7,
                'body_temperature': 0.3
            },
            'fear': {
                'heart_rate': 20.0,     # значительное увеличение
                'breathing_rate': 10.0,
                'skin_conductance': 0.9,
                'muscle_tension': 0.8,
                'body_temperature': 0.2
            },
            'surprise': {
                'heart_rate': 8.0,
                'breathing_rate': 5.0,
                'skin_conductance': 0.5,
                'muscle_tension': 0.3,
                'body_temperature': 0.1
            },
            'disgust': {
                'heart_rate': 3.0,
                'breathing_rate': -2.0,  # уменьшение
                'skin_conductance': 0.3,
                'muscle_tension': 0.2,
                'body_temperature': 0.0
            },
            'trust': {
                'heart_rate': -2.0,
                'breathing_rate': 1.0,
                'skin_conductance': -0.2,
                'muscle_tension': -0.3,
                'body_temperature': 0.0
            },
            'anticipation': {
                'heart_rate': 10.0,
                'breathing_rate': 6.0,
                'skin_conductance': 0.6,
                'muscle_tension': 0.4,
                'body_temperature': 0.1
            }
        }
        
        # Хронобиологические ритмы
        self.circadian_rhythms = {
            'alertness': 0.5,      # уровень бодрствования
            'sleepiness': 0.3,     # уровень сонливости
            'cortisol_level': 0.6, # уровень кортизола
            'melatonin_level': 0.2 # уровень мелатонина
        }
        
        # Системы организма
        self.systems = {
            'nervous_system': 0.7,
            'endocrine_system': 0.6,
            'cardiovascular_system': 0.8,
            'respiratory_system': 0.7
        }
        
        # Временные параметры
        self.last_update_time = time.time()

    def update_physiology(self, emotional_state: Dict[str, Any], 
                         cognitive_load: float = 0.0, 
                         external_stimuli: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Обновление физиологического состояния на основе эмоций, когнитивной нагрузки и внешних стимулов
        """
        current_time = time.time()
        time_delta = current_time - self.last_update_time
        self.last_update_time = current_time
        
        # Обновление на основе эмоционального состояния
        if emotional_state and 'dominant_emotion' in emotional_state:
            emotion = emotional_state['dominant_emotion']
            intensity = emotional_state.get('intensity', 0.5)
            
            if emotion in self.emotion_physiology_map:
                self._apply_emotional_effects(emotion, intensity, time_delta)
        
        # Влияние когнитивной нагрузки
        self._apply_cognitive_load_effects(cognitive_load, time_delta)
        
        # Влияние внешних стимулов
        if external_stimuli:
            self._apply_external_stimuli_effects(external_stimuli, time_delta)
        
        # Обновление хронобиологических ритмов
        self._update_circadian_rhythms(time_delta)
        
        # Возврат обновленного состояния
        return self.physiological_state.copy()

    def _apply_emotional_effects(self, emotion: str, intensity: float, time_delta: float):
        """
        Применение эффектов эмоций к физиологическим параметрам
        """
        if emotion in self.emotion_physiology_map:
            effects = self.emotion_physiology_map[emotion]
            
            for param, effect in effects.items():
                if param in self.physiological_state:
                    # Применение эффекта с учетом интенсивности и времени
                    delta = effect * intensity * time_delta * 0.1
                    self.physiological_state[param] += delta
                    
                    # Ограничение значений
                    if param == 'heart_rate':
                        self.physiological_state[param] = max(40.0, min(200.0, self.physiological_state[param]))
                    elif param == 'breathing_rate':
                        self.physiological_state[param] = max(6.0, min(30.0, self.physiological_state[param]))
                    elif param in ['muscle_tension', 'energy_level', 'fatigue_level', 'skin_conductance']:
                        self.physiological_state[param] = max(0.0, min(1.0, self.physiological_state[param]))
                    elif param == 'body_temperature':
                        self.physiological_state[param] = max(35.0, min(42.0, self.physiological_state[param]))

    def _apply_cognitive_load_effects(self, cognitive_load: float, time_delta: float):
        """
        Применение эффектов когнитивной нагрузки
        """
        # Когнитивная нагрузка влияет на сердечный ритм, потоотделение и мышечное напряжение
        if cognitive_load > 0.5:
            self.physiological_state['heart_rate'] += cognitive_load * 2.0 * time_delta * 0.1
            self.physiological_state['skin_conductance'] += cognitive_load * 0.3 * time_delta * 0.1
            self.physiological_state['muscle_tension'] += cognitive_load * 0.2 * time_delta * 0.1
            self.physiological_state['fatigue_level'] += cognitive_load * 0.1 * time_delta * 0.1
        
        # Также влияет на уровень энергии
        self.physiological_state['energy_level'] -= cognitive_load * 0.05 * time_delta * 0.1
        self.physiological_state['energy_level'] = max(0.0, self.physiological_state['energy_level'])

    def _apply_external_stimuli_effects(self, stimuli: Dict[str, Any], time_delta: float):
        """
        Применение эффектов внешних стимулов
        """
        # Свет (яркость)
        if 'light_intensity' in stimuli:
            light = stimuli['light_intensity']
            # Свет влияет на бодрствование и температуру тела
            self.circadian_rhythms['alertness'] += light * 0.1 * time_delta * 0.01
            self.physiological_state['body_temperature'] += light * 0.01 * time_delta * 0.01
        
        # Температура окружающей среды
        if 'ambient_temperature' in stimuli:
            ambient_temp = stimuli['ambient_temperature']
            # Сильная разница с телесной температурой вызывает реакцию
            temp_diff = ambient_temp - self.physiological_state['body_temperature']
            self.physiological_state['body_temperature'] += temp_diff * 0.05 * time_delta * 0.1
            self.physiological_state['muscle_tension'] += abs(temp_diff) * 0.01 * time_delta * 0.1
        
        # Шум
        if 'noise_level' in stimuli:
            noise = stimuli['noise_level']
            # Шум влияет на уровень стресса и сердечный ритм
            self.physiological_state['heart_rate'] += noise * 3.0 * time_delta * 0.1
            self.physiological_state['skin_conductance'] += noise * 0.2 * time_delta * 0.1

    def _update_circadian_rhythms(self, time_delta: float):
        """
        Обновление хронобиологических ритмов
        """
        # Упрощенная модель суточных ритмов
        # Предполагаем, что время в секундах суток
        current_time_of_day = (time.time() % 86400) / 3600  # Часы в сутках (0-24)
        
        # Бодрствование - максимальное утром, минимальное ночью
        alertness_factor = 0.5 + 0.3 * np.sin(2 * np.pi * (current_time_of_day - 6) / 24)
        self.circadian_rhythms['alertness'] = max(0.1, min(1.0, alertness_factor))
        
        # Сонливость - противоположность бодрствования
        self.circadian_rhythms['sleepiness'] = 1.0 - self.circadian_rhythms['alertness']
        
        # Кортизол - максимум утром
        cortisol_factor = 0.5 + 0.3 * np.sin(2 * np.pi * (current_time_of_day - 8) / 24)
        self.circadian_rhythms['cortisol_level'] = max(0.1, min(1.0, cortisol_factor))
        
        # Мелатонин - максимум ночью
        melatonin_factor = 0.5 + 0.3 * np.sin(2 * np.pi * (current_time_of_day - 22) / 24)
        self.circadian_rhythms['melatonin_level'] = max(0.1, min(1.0, melatonin_factor))
        
        # Обновление физиологических параметров на основе ритмов
        self.physiological_state['energy_level'] += (self.circadian_rhythms['alertness'] - 0.5) * 0.01
        self.physiological_state['fatigue_level'] += (self.circadian_rhythms['sleepiness'] - 0.5) * 0.01
        self.physiological_state['heart_rate'] += (self.circadian_rhythms['cortisol_level'] - 0.5) * 1.0

    def get_physiological_readings(self) -> Dict[str, Any]:
        """
        Получение текущих физиологических показаний
        """
        return {
            'current_state': self.physiological_state.copy(),
            'circadian_state': self.circadian_rhythms.copy(),
            'system_efficiency': self.systems.copy(),
            'estimated_arousal': self._estimate_arousal_level(),
            'stress_indicators': self._get_stress_indicators()
        }

    def _estimate_arousal_level(self) -> float:
        """
        Оценка уровня возбуждения на основе физиологических параметров
        """
        # Уровень возбуждения оценивается по комбинации параметров
        heart_rate_arousal = (self.physiological_state['heart_rate'] - 60) / 60  # Нормализация
        conductance_arousal = self.physiological_state['skin_conductance']
        breathing_arousal = (self.physiological_state['breathing_rate'] - 10) / 10  # Нормализация
        
        # Комбинирование показателей
        arousal = (heart_rate_arousal * 0.4 + 
                  conductance_arousal * 0.3 + 
                  breathing_arousal * 0.3)
        
        # Ограничение в диапазоне [0, 1]
        return max(0.0, min(1.0, arousal))

    def _get_stress_indicators(self) -> Dict[str, float]:
        """
        Получение индикаторов стресса
        """
        return {
            'heart_rate_variability': self._calculate_hrv(),
            'muscle_tension_level': self.physiological_state['muscle_tension'],
            'skin_conductance_level': self.physiological_state['skin_conductance'],
            'estimated_stress': self._estimate_stress_level()
        }

    def _calculate_hrv(self) -> float:
        """
        Расчет вариабельности сердечного ритма (упрощенно)
        """
        # Упрощенная оценка: чем больше отклонение от базового уровня, тем ниже HRV
        baseline = 70.0
        current = self.physiological_state['heart_rate']
        deviation = abs(current - baseline) / baseline
        # Чем больше отклонение, тем ниже HRV (меньше значение)
        return max(0.0, 1.0 - deviation)

    def _estimate_stress_level(self) -> float:
        """
        Оценка уровня стресса
        """
        # Стресс оценивается по комбинации физиологических параметров
        heart_stress = max(0, (self.physiological_state['heart_rate'] - 80) / 40)
        tension_stress = self.physiological_state['muscle_tension']
        conductance_stress = self.physiological_state['skin_conductance']
        fatigue_stress = self.physiological_state['fatigue_level']
        
        stress_level = (heart_stress * 0.3 + 
                       tension_stress * 0.25 + 
                       conductance_stress * 0.25 + 
                       fatigue_stress * 0.2)
        
        return max(0.0, min(1.0, stress_level))

    def simulate_rest_and_recovery(self, duration_minutes: float = 10.0):
        """
        Симуляция отдыха и восстановления
        """
        # Восстановление происходит быстрее для некоторых параметров
        self.physiological_state['muscle_tension'] *= (1 - 0.1 * duration_minutes / 10)
        self.physiological_state['fatigue_level'] *= (1 - 0.15 * duration_minutes / 10)
        self.physiological_state['heart_rate'] = max(70.0, 
            self.physiological_state['heart_rate'] * (1 - 0.05 * duration_minutes / 10))
        self.physiological_state['energy_level'] = min(1.0, 
            self.physiological_state['energy_level'] + 0.05 * duration_minutes / 10)
        
        # Ограничение значений
        self.physiological_state['muscle_tension'] = max(0.0, self.physiological_state['muscle_tension'])
        self.physiological_state['fatigue_level'] = max(0.0, self.physiological_state['fatigue_level'])
        self.physiological_state['energy_level'] = min(1.0, self.physiological_state['energy_level'])

    def get_detailed_physiology_report(self) -> Dict[str, Any]:
        """
        Получение подробного отчета о физиологии
        """
        arousal = self._estimate_arousal_level()
        stress = self._estimate_stress_level()
        
        return {
            'basic_physiology': self.physiological_state,
            'circadian_rhythms': self.circadian_rhythms,
            'arousal_level': arousal,
            'stress_level': stress,
            'recovery_status': self._assess_recovery_status(),
            'homeostasis_balance': self._assess_homeostasis(),
            'system_coherence': self._calculate_system_coherence()
        }

    def _assess_recovery_status(self) -> float:
        """
        Оценка статуса восстановления
        """
        # Восстановление оценивается по уровню энергии и усталости
        energy_recovery = self.physiological_state['energy_level']
        fatigue_recovery = 1.0 - self.physiological_state['fatigue_level']
        
        return (energy_recovery + fatigue_recovery) / 2

    def _assess_homeostasis(self) -> float:
        """
        Оценка гомеостатического баланса
        """
        # Гомеостаз - баланс между различными системами
        temp_balance = abs(self.physiological_state['body_temperature'] - 36.6) / 1.6  # Нормализация
        hr_balance = abs(self.physiological_state['heart_rate'] - 70) / 70  # Нормализация
        
        # Чем меньше отклонение, тем лучше гомеостаз
        homeostasis = 1.0 - (temp_balance * 0.5 + hr_balance * 0.5)
        
        return max(0.0, min(1.0, homeostasis))

    def _calculate_system_coherence(self) -> float:
        """
        Расчет когерентности систем
        """
        # Когерентность как согласованность между системами
        sys_values = list(self.systems.values())
        avg_sys = sum(sys_values) / len(sys_values) if sys_values else 0.5
        
        # Меньшая вариация означает большую когерентность
        variance = sum((v - avg_sys) ** 2 for v in sys_values) / len(sys_values) if sys_values else 0.25
        
        # Когерентность обратно пропорциональна вариации
        coherence = max(0.0, 1.0 - variance * 4)  # Масштабируем для [0,1]
        
        return coherence