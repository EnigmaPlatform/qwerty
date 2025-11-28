"""
ConsciousnessStream: Поток сознания
"""
from typing import Dict, Any, List
import time
import numpy as np


class ConsciousnessStream:
    def __init__(self):
        """
        Инициализация потока сознания
        """
        # Компоненты сознания
        self.consciousness_components = {
            'awareness': 0.7,          # Осознанность
            'attention': 0.8,          # Внимание
            'intentionality': 0.75,    # Интенциональность
            'unity': 0.85,             # Единство
            'selectivity': 0.78,       # Селективность
            'transience': 0.65         # Временность
        }
        
        # Состояния сознания
        self.consciousness_states = {
            'waking': 0.9,             # Бодрствование
            'drowsy': 0.3,             # Сонливость
            'focused': 0.8,            # Сосредоточенность
            'wandering': 0.4           # Блуждание ума
        }
        
        # Содержание сознания
        self.phenomenal_experience = {
            'sensory_inputs': [],
            'emotional_qualia': [],
            'cognitive_patterns': [],
            'self_awareness': 0.0,
            'temporal_depth': 0.0
        }
        
        # Глобальное рабочее пространство
        self.global_workspace = {
            'current_focus': None,
            'accessibility': 0.9,
            'broadcasting': False,
            'content_queue': []
        }
        
        # История сознательного опыта
        self.experience_stream = []
        
        # Параметры потока
        self.integration_window = 0.5  # Окно интеграции в секундах
        self.attention_span = 10.0     # Продолжительность внимания в секундах
        self.consciousness_fluidity = 0.8

    def process_consciousness_input(self, sensory_input: Dict[str, Any], 
                                  cognitive_input: Dict[str, Any],
                                  emotional_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обработка входных данных для формирования сознательного опыта
        """
        current_time = time.time()
        
        # Обновление сенсорных входов
        self.phenomenal_experience['sensory_inputs'].append({
            'data': sensory_input,
            'timestamp': current_time
        })
        
        # Обновление эмоциональных качеств
        self.phenomenal_experience['emotional_qualia'].append({
            'data': emotional_input,
            'timestamp': current_time
        })
        
        # Обновление когнитивных паттернов
        self.phenomenal_experience['cognitive_patterns'].append({
            'data': cognitive_input,
            'timestamp': current_time
        })
        
        # Интеграция в глобальное рабочее пространство
        integrated_content = self._integrate_to_global_workspace(
            sensory_input, cognitive_input, emotional_input
        )
        
        # Обновление текущего фокуса внимания
        self._update_attention_focus(integrated_content)
        
        # Генерация сознательного опыта
        conscious_experience = self._generate_conscious_experience(
            integrated_content, current_time
        )
        
        # Запись в поток опыта
        self.experience_stream.append({
            'experience': conscious_experience,
            'timestamp': current_time,
            'sensory_input': sensory_input,
            'cognitive_input': cognitive_input,
            'emotional_input': emotional_input
        })
        
        # Очистка устаревших данных
        self._cleanup_old_data(current_time)
        
        return conscious_experience

    def _integrate_to_global_workspace(self, sensory: Dict[str, Any], 
                                     cognitive: Dict[str, Any], 
                                     emotional: Dict[str, Any]) -> Dict[str, Any]:
        """
        Интеграция информации в глобальное рабочее пространство
        """
        # Оценка значимости каждого типа информации
        sensory_significance = self._assess_significance(sensory, 'sensory')
        cognitive_significance = self._assess_significance(cognitive, 'cognitive')
        emotional_significance = self._assess_significance(emotional, 'emotional')
        
        # Определение текущего фокуса на основе значимости
        max_significance = max(sensory_significance, cognitive_significance, emotional_significance)
        
        if max_significance == sensory_significance:
            current_focus = {'type': 'sensory', 'data': sensory, 'significance': sensory_significance}
        elif max_significance == cognitive_significance:
            current_focus = {'type': 'cognitive', 'data': cognitive, 'significance': cognitive_significance}
        else:
            current_focus = {'type': 'emotional', 'data': emotional, 'significance': emotional_significance}
        
        # Обновление глобального рабочего пространства
        self.global_workspace['current_focus'] = current_focus
        self.global_workspace['broadcasting'] = True
        
        # Добавление в очередь содержимого
        self.global_workspace['content_queue'].append(current_focus)
        
        # Ограничение размера очереди
        if len(self.global_workspace['content_queue']) > 10:
            self.global_workspace['content_queue'] = self.global_workspace['content_queue'][-10:]
        
        return current_focus

    def _assess_significance(self, data: Dict[str, Any], data_type: str) -> float:
        """
        Оценка значимости данных для сознательного опыта
        """
        significance = 0.5  # базовая значимость
        
        if data_type == 'sensory':
            # Значимость сенсорных данных зависит от интенсивности и новизны
            intensity = data.get('intensity', 0.5)
            novelty = data.get('novelty', 0.3)
            significance = 0.4 * intensity + 0.6 * novelty
            
        elif data_type == 'cognitive':
            # Значимость когнитивных данных зависит от важности и сложности
            importance = data.get('importance', 0.5)
            complexity = data.get('complexity', 0.4)
            significance = 0.7 * importance + 0.3 * complexity
            
        elif data_type == 'emotional':
            # Значимость эмоциональных данных зависит от интенсивности и валентности
            intensity = data.get('intensity', 0.5)
            valence = abs(data.get('valence', 0.0))  # По модулю, так как сильные эмоции значимы
            significance = 0.6 * intensity + 0.4 * valence
        
        return max(0.0, min(1.0, significance))

    def _update_attention_focus(self, integrated_content: Dict[str, Any]):
        """
        Обновление фокуса внимания
        """
        focus_type = integrated_content['type']
        significance = integrated_content['significance']
        
        # Обновление компонентов сознания на основе фокуса
        if focus_type == 'sensory':
            self.consciousness_components['awareness'] = min(1.0, 
                self.consciousness_components['awareness'] + significance * 0.1)
        elif focus_type == 'cognitive':
            self.consciousness_components['attention'] = min(1.0, 
                self.consciousness_components['attention'] + significance * 0.1)
        elif focus_type == 'emotional':
            self.consciousness_components['intentionality'] = min(1.0, 
                self.consciousness_components['intentionality'] + significance * 0.1)
        
        # Нормализация компонентов
        total = sum(self.consciousness_components.values())
        if total > len(self.consciousness_components):
            for key in self.consciousness_components:
                self.consciousness_components[key] *= len(self.consciousness_components) / total

    def _generate_conscious_experience(self, integrated_content: Dict[str, Any], 
                                     timestamp: float) -> Dict[str, Any]:
        """
        Генерация сознательного опыта
        """
        # Формирование феноменального опыта
        experience = {
            'primary_content': integrated_content,
            'awareness_level': self.consciousness_components['awareness'],
            'attention_level': self.consciousness_components['attention'],
            'phenomenal_character': self._determine_phenomenal_character(integrated_content),
            'temporal_context': self._get_temporal_context(timestamp),
            'self_involvement': self._assess_self_involvement(integrated_content),
            'clarity': self._assess_clarity(integrated_content),
            'accessibility': self.global_workspace['accessibility']
        }
        
        # Обновление самосознания
        self.phenomenal_experience['self_awareness'] = self._update_self_awareness(experience)
        
        return experience

    def _determine_phenomenal_character(self, integrated_content: Dict[str, Any]) -> str:
        """
        Определение феноменального характера опыта
        """
        content_type = integrated_content['type']
        
        if content_type == 'sensory':
            return 'perceptual_experience'
        elif content_type == 'cognitive':
            return 'cognitive_experience'
        elif content_type == 'emotional':
            return 'emotional_experience'
        else:
            return 'mixed_experience'

    def _get_temporal_context(self, timestamp: float) -> Dict[str, Any]:
        """
        Получение временного контекста опыта
        """
        # Временная глубина опыта
        if len(self.experience_stream) > 0:
            time_diff = timestamp - self.experience_stream[-1]['timestamp']
            temporal_depth = min(1.0, time_diff / 10.0)  # Нормализация
        else:
            temporal_depth = 0.0
        
        self.phenomenal_experience['temporal_depth'] = temporal_depth
        
        return {
            'current_time': timestamp,
            'time_since_last': time_diff if len(self.experience_stream) > 0 else 0,
            'temporal_depth': temporal_depth
        }

    def _assess_self_involvement(self, integrated_content: Dict[str, Any]) -> float:
        """
        Оценка вовлеченности "Я" в опыт
        """
        # Оценка вовлечения на основе типа содержимого и его отношения к "Я"
        content_type = integrated_content['type']
        
        if content_type == 'emotional':
            # Эмоции обычно более связаны с "Я"
            return 0.8
        elif content_type == 'cognitive' and 'self_referential' in integrated_content.get('data', {}):
            # Самореферентные мысли связаны с "Я"
            return 0.9
        else:
            # Нейтральные сенсорные данные менее связаны с "Я"
            return 0.4

    def _assess_clarity(self, integrated_content: Dict[str, Any]) -> float:
        """
        Оценка ясности сознательного опыта
        """
        significance = integrated_content['significance']
        attention = self.consciousness_components['attention']
        
        # Ясность зависит от значимости и уровня внимания
        clarity = (significance * 0.6 + attention * 0.4)
        
        return clarity

    def _update_self_awareness(self, experience: Dict[str, Any]) -> float:
        """
        Обновление уровня самосознания
        """
        # Уровень самосознания зависит от вовлечения "Я" и ясности опыта
        self_involvement = experience['self_involvement']
        clarity = experience['clarity']
        
        # Обновление с затуханием
        new_self_awareness = (self_involvement * 0.7 + clarity * 0.3)
        
        # Плавное обновление
        current_self_awareness = self.phenomenal_experience['self_awareness']
        updated_self_awareness = current_self_awareness * 0.8 + new_self_awareness * 0.2
        
        return updated_self_awareness

    def _cleanup_old_data(self, current_time: float):
        """
        Очистка устаревших данных из буферов
        """
        # Удаление данных старше окна интеграции
        cutoff_time = current_time - self.integration_window
        
        # Очистка сенсорных входов
        self.phenomenal_experience['sensory_inputs'] = [
            item for item in self.phenomenal_experience['sensory_inputs'] 
            if item['timestamp'] > cutoff_time
        ]
        
        # Очистка эмоциональных качеств
        self.phenomenal_experience['emotional_qualia'] = [
            item for item in self.phenomenal_experience['emotional_qualia'] 
            if item['timestamp'] > cutoff_time
        ]
        
        # Очистка когнитивных паттернов
        self.phenomenal_experience['cognitive_patterns'] = [
            item for item in self.phenomenal_experience['cognitive_patterns'] 
            if item['timestamp'] > cutoff_time
        ]
        
        # Очистка потока опыта (оставляем последние 100 элементов)
        if len(self.experience_stream) > 100:
            self.experience_stream = self.experience_stream[-100:]

    def get_consciousness_state(self) -> Dict[str, Any]:
        """
        Получение текущего состояния сознания
        """
        return {
            'components': self.consciousness_components.copy(),
            'states': self.consciousness_states.copy(),
            'phenomenal_experience': {
                'self_awareness': self.phenomenal_experience['self_awareness'],
                'temporal_depth': self.phenomenal_experience['temporal_depth'],
                'sensory_count': len(self.phenomenal_experience['sensory_inputs']),
                'emotional_count': len(self.phenomenal_experience['emotional_qualia']),
                'cognitive_count': len(self.phenomenal_experience['cognitive_patterns'])
            },
            'global_workspace': {
                'current_focus': self.global_workspace['current_focus'],
                'accessibility': self.global_workspace['accessibility'],
                'broadcasting': self.global_workspace['broadcasting'],
                'queue_length': len(self.global_workspace['content_queue'])
            },
            'experience_metrics': self._calculate_experience_metrics()
        }

    def _calculate_experience_metrics(self) -> Dict[str, Any]:
        """
        Расчет метрик сознательного опыта
        """
        if not self.experience_stream:
            return {
                'experience_coherence': 0.5,
                'temporal_continuity': 0.5,
                'content_diversity': 0.5,
                'average_clarity': 0.5
            }
        
        # Согласованность опыта
        awareness_levels = [exp['experience']['awareness_level'] for exp in self.experience_stream]
        attention_levels = [exp['experience']['attention_level'] for exp in self.experience_stream]
        
        avg_awareness = sum(awareness_levels) / len(awareness_levels)
        avg_attention = sum(attention_levels) / len(attention_levels)
        
        # Непрерывность во времени
        time_gaps = []
        for i in range(1, len(self.experience_stream)):
            gap = (self.experience_stream[i]['timestamp'] - 
                   self.experience_stream[i-1]['timestamp'])
            time_gaps.append(gap)
        
        avg_time_gap = sum(time_gaps) / len(time_gaps) if time_gaps else 0
        temporal_continuity = max(0.0, 1.0 - avg_time_gap)  # Чем меньше разрывы, тем выше непрерывность
        
        # Разнообразие содержания
        content_types = [exp['experience']['phenomenal_character'] for exp in self.experience_stream]
        unique_types = len(set(content_types))
        content_diversity = unique_types / len(content_types) if content_types else 0.0
        
        # Средняя ясность
        clarity_values = [exp['experience']['clarity'] for exp in self.experience_stream]
        avg_clarity = sum(clarity_values) / len(clarity_values)
        
        return {
            'experience_coherence': (avg_awareness + avg_attention) / 2,
            'temporal_continuity': temporal_continuity,
            'content_diversity': content_diversity,
            'average_clarity': avg_clarity
        }

    def modulate_consciousness_state(self, state_modifications: Dict[str, float]):
        """
        Модуляция состояния сознания
        """
        for component, modification in state_modifications.items():
            if component in self.consciousness_components:
                new_value = self.consciousness_components[component] + modification
                self.consciousness_components[component] = max(0.0, min(1.0, new_value))
        
        # Также модулируем состояния сознания
        for state, modification in state_modifications.items():
            if state in self.consciousness_states:
                new_value = self.consciousness_states[state] + modification
                self.consciousness_states[state] = max(0.0, min(1.0, new_value))

    def enter_meditative_state(self):
        """
        Вход в медитативное состояние (повышенная осознанность, пониженное рассеивание)
        """
        self.consciousness_components['awareness'] = min(1.0, self.consciousness_components['awareness'] + 0.2)
        self.consciousness_components['attention'] = min(1.0, self.consciousness_components['attention'] + 0.3)
        self.consciousness_components['transience'] = max(0.0, self.consciousness_components['transience'] - 0.2)
        
        # Повышение единства опыта
        self.consciousness_components['unity'] = min(1.0, self.consciousness_components['unity'] + 0.1)

    def enter_creative_state(self):
        """
        Вход в креативное состояние (повышенная подвижность, умеренное рассеивание)
        """
        self.consciousness_components['transience'] = min(1.0, self.consciousness_components['transience'] + 0.3)
        self.consciousness_components['awareness'] = min(1.0, self.consciousness_components['awareness'] + 0.1)
        self.consciousness_components['wandering'] = min(1.0, self.consciousness_states['wandering'] + 0.4)
        
        # Повышение флюидности мышления
        self.consciousness_fluidity = min(1.0, self.consciousness_fluidity + 0.2)

    def get_stream_summary(self, lookback_seconds: int = 10) -> Dict[str, Any]:
        """
        Получение сводки потока сознания за определенное время
        """
        current_time = time.time()
        cutoff_time = current_time - lookback_seconds
        
        recent_experiences = [
            exp for exp in self.experience_stream 
            if exp['timestamp'] > cutoff_time
        ]
        
        if not recent_experiences:
            return {'message': 'No recent experiences'}
        
        # Анализ недавнего опыта
        content_types = [exp['experience']['phenomenal_character'] for exp in recent_experiences]
        primary_content_types = [exp['experience']['primary_content']['type'] for exp in recent_experiences]
        
        # Определение преобладающего типа опыта
        from collections import Counter
        type_counts = Counter(content_types)
        primary_type_counts = Counter(primary_content_types)
        
        dominant_content_type = type_counts.most_common(1)[0][0] if type_counts else 'mixed'
        dominant_primary_type = primary_type_counts.most_common(1)[0][0] if primary_type_counts else 'mixed'
        
        # Средние показатели
        avg_awareness = np.mean([exp['experience']['awareness_level'] for exp in recent_experiences])
        avg_attention = np.mean([exp['experience']['attention_level'] for exp in recent_experiences])
        avg_clarity = np.mean([exp['experience']['clarity'] for exp in recent_experiences])
        
        return {
            'duration': lookback_seconds,
            'experience_count': len(recent_experiences),
            'dominant_content_type': dominant_content_type,
            'dominant_primary_type': dominant_primary_type,
            'average_awareness': avg_awareness,
            'average_attention': avg_attention,
            'average_clarity': avg_clarity,
            'content_diversity': len(set(content_types)) / len(content_types) if content_types else 0,
            'temporal_density': len(recent_experiences) / lookback_seconds
        }