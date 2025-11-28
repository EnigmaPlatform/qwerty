"""
BehavioralGenerator: Генератор поведения
"""
from typing import Dict, Any, List
import random


class BehavioralGenerator:
    def __init__(self):
        """
        Инициализация генератора поведения
        """
        # Поведенческие паттерны
        self.behavioral_patterns = {
            'expressive': {  # Выразительное поведение
                'facial_expressions': ['neutral', 'smile', 'concerned', 'surprised'],
                'vocal_variations': ['normal', 'enthusiastic', 'soothing', 'firm'],
                'gestures': ['none', 'open_hands', 'leaning_forward', 'head_nod']
            },
            'adaptive': {  # Адаптивное поведение
                'response_modifications': ['adjust_tone', 'change_topic', 'offer_help', 'ask_questions'],
                'social_adjustments': ['match_energy', 'respect_boundaries', 'show_empathy', 'provide_space']
            },
            'regulatory': {  # Регулятивное поведение
                'self_control': ['pause_before_responding', 'reflect_on_response', 'moderate_intensity'],
                'emotional_regulation': ['calm_down', 'build_up_enth', 'maintain_balance']
            }
        }
        
        # Словарь поведенческих реакций
        self.behavioral_responses = {
            'positive_emotion': ['express_joy', 'show_interest', 'encourage', 'celebrate'],
            'negative_emotion': ['offer_comfort', 'show_concern', 'provide_support', 'listen_empathetically'],
            'neutral_emotion': ['ask_questions', 'provide_information', 'maintain_conversation', 'seek_clarification'],
            'high_arousal': ['match_energy', 'provide_calm', 'engage_actively', 'use_dynamic_language'],
            'low_arousal': ['increase_engagement', 'ask_open_questions', 'provide_stimulation', 'use_enlivening_language']
        }
        
        # История поведенческих выборов
        self.behavioral_history = []
        
        # Параметры поведения
        self.expressiveness_level = 0.7
        self.adaptability_level = 0.8
        self.spontaneity_factor = 0.6
        self.social_awareness = 0.9

    def generate_behavior(self, emotional_state: Dict[str, Any], 
                        social_context: Dict[str, Any],
                        cognitive_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Генерация поведенческой реакции на основе эмоционального состояния, 
        социального контекста и когнитивного состояния
        """
        # Определение типа эмоции
        emotion_type = self._classify_emotion(emotional_state)
        
        # Определение уровня возбуждения
        arousal_level = emotional_state.get('arousal', 0.5)
        
        # Выбор поведенческой реакции
        behavioral_choice = self._select_behavioral_response(
            emotion_type, arousal_level, social_context, cognitive_state
        )
        
        # Генерация специфических поведенческих элементов
        expressive_elements = self._generate_expressive_elements(
            emotional_state, arousal_level
        )
        
        adaptive_elements = self._generate_adaptive_elements(
            social_context
        )
        
        # Запись в историю
        self.behavioral_history.append({
            'timestamp': self._get_current_time(),
            'input': {
                'emotion': emotional_state,
                'social_context': social_context,
                'cognitive_state': cognitive_state
            },
            'output': behavioral_choice,
            'expressive_elements': expressive_elements,
            'adaptive_elements': adaptive_elements
        })
        
        return {
            'behavioral_response': behavioral_choice,
            'expressive_elements': expressive_elements,
            'adaptive_elements': adaptive_elements,
            'confidence': self._calculate_behavioral_confidence(social_context),
            'appropriateness_score': self._assess_appropriateness(
                behavioral_choice, social_context
            )
        }

    def _classify_emotion(self, emotional_state: Dict[str, Any]) -> str:
        """
        Классификация эмоции для выбора поведения
        """
        if not emotional_state:
            return 'neutral_emotion'
        
        dominant_emotion = emotional_state.get('dominant_emotion', 'neutral')
        
        # Группировка эмоций
        positive_emotions = ['joy', 'love', 'gratitude', 'amazement', 'excitement', 'serenity', 'pride']
        negative_emotions = ['sadness', 'anger', 'fear', 'guilt', 'disgust', 'despair']
        neutral_emotions = ['trust', 'anticipation', 'neutral', 'contempt', 'envy', 'boredom', 'confusion']
        
        if dominant_emotion in positive_emotions:
            return 'positive_emotion'
        elif dominant_emotion in negative_emotions:
            return 'negative_emotion'
        elif dominant_emotion in neutral_emotions:
            return 'neutral_emotion'
        else:
            return 'neutral_emotion'

    def _select_behavioral_response(self, emotion_type: str, arousal_level: float,
                                  social_context: Dict[str, Any],
                                  cognitive_state: Dict[str, Any]) -> str:
        """
        Выбор поведенческой реакции на основе типа эмоции и других факторов
        """
        # Получение возможных реакций для типа эмоции
        possible_responses = self.behavioral_responses.get(emotion_type, ['maintain_neutral'])
        
        # Определение уровня арOUSала
        if arousal_level > 0.7:
            possible_responses.extend(self.behavioral_responses.get('high_arousal', []))
        elif arousal_level < 0.3:
            possible_responses.extend(self.behavioral_responses.get('low_arousal', []))
        
        # Выбор реакции с учетом социального контекста
        # Если контекст формальный, избегать слишком экспрессивных реакций
        formality_level = social_context.get('formality', 0.5)
        if formality_level > 0.7:
            # Фильтрация слишком экспрессивных реакций
            filtered_responses = [r for r in possible_responses 
                                if r not in ['express_joy', 'celebrate', 'show_excessive_emotion']]
            if filtered_responses:
                possible_responses = filtered_responses
        
        # Выбор случайной реакции из возможных
        if possible_responses:
            return random.choice(possible_responses)
        else:
            return 'maintain_neutral'

    def _generate_expressive_elements(self, emotional_state: Dict[str, Any], 
                                   arousal_level: float) -> Dict[str, Any]:
        """
        Генерация выразительных элементов поведения
        """
        expressive_behavior = {}
        
        # Выбор экспрессивных элементов на основе эмоции
        dominant_emotion = emotional_state.get('dominant_emotion', 'neutral')
        
        # Лицевые выражения
        if dominant_emotion in ['joy', 'amazement']:
            facial_choice = 'smile'
        elif dominant_emotion in ['sadness', 'guilt']:
            facial_choice = 'concerned'
        elif dominant_emotion in ['surprise', 'fear']:
            facial_choice = 'surprised'
        else:
            facial_choice = 'neutral'
        
        expressive_behavior['facial_expression'] = facial_choice
        
        # Вокальные вариации
        if arousal_level > 0.7:
            vocal_choice = 'enthusiastic' if dominant_emotion in ['joy', 'excitement'] else 'firm'
        elif arousal_level < 0.3:
            vocal_choice = 'soothing'
        else:
            vocal_choice = 'normal'
        
        expressive_behavior['vocal_variation'] = vocal_choice
        
        # Жесты
        if dominant_emotion in ['trust', 'love']:
            gesture_choice = 'open_hands'
        elif dominant_emotion in ['surprise', 'excitement']:
            gesture_choice = 'head_nod'
        elif dominant_emotion in ['fear', 'sadness']:
            gesture_choice = 'none'
        else:
            gesture_choice = 'neutral'
        
        expressive_behavior['gesture'] = gesture_choice
        
        return expressive_behavior

    def _generate_adaptive_elements(self, social_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Генерация адаптивных элементов поведения
        """
        adaptive_behavior = {}
        
        # Адаптация к социальному контексту
        if social_context.get('formality', 0.5) > 0.7:
            adaptive_behavior['response_modification'] = 'adjust_tone'
            adaptive_behavior['social_adjustment'] = 'respect_boundaries'
        elif social_context.get('intimacy_level', 0.5) > 0.7:
            adaptive_behavior['response_modification'] = 'show_empathy'
            adaptive_behavior['social_adjustment'] = 'show_empathy'
        else:
            adaptive_behavior['response_modification'] = 'ask_questions'
            adaptive_behavior['social_adjustment'] = 'match_energy'
        
        # Адаптация к стилю общения собеседника
        communication_style = social_context.get('communication_style', 'balanced')
        if communication_style == 'direct':
            adaptive_behavior['style_matching'] = 'direct_and_clear'
        elif communication_style == 'indirect':
            adaptive_behavior['style_matching'] = 'considerate_and_tactful'
        else:
            adaptive_behavior['style_matching'] = 'balanced_approach'
        
        return adaptive_behavior

    def _calculate_behavioral_confidence(self, social_context: Dict[str, Any]) -> float:
        """
        Расчет уверенности в поведенческом выборе
        """
        # Уверенность зависит от знакомства с социальным контекстом
        familiarity = social_context.get('familiarity', 0.5)
        context_clarity = social_context.get('clarity', 0.6)
        
        # Комбинирование факторов
        confidence = (familiarity * 0.6 + context_clarity * 0.4)
        
        return confidence

    def _assess_appropriateness(self, behavioral_choice: str, 
                              social_context: Dict[str, Any]) -> float:
        """
        Оценка уместности поведенческого выбора
        """
        # Оценка уместности в зависимости от контекста
        formality = social_context.get('formality', 0.5)
        
        # Некоторые поведенческие реакции неуместны в формальных контекстах
        inappropriate_for_formal = ['express_joy', 'celebrate', 'joke_around']
        
        if formality > 0.7 and behavioral_choice in inappropriate_for_formal:
            appropriateness = 0.3
        else:
            # В остальных случаях уместность зависит от других факторов
            appropriateness = 0.8  # Базовая уместность
        
        return appropriateness

    def get_behavioral_profile(self) -> Dict[str, Any]:
        """
        Получение профиля поведения
        """
        return {
            'expressiveness_level': self.expressiveness_level,
            'adaptability_level': self.adaptability_level,
            'spontaneity_factor': self.spontaneity_factor,
            'social_awareness': self.social_awareness,
            'behavioral_diversity': self._calculate_behavioral_diversity(),
            'social_adaptation_success': self._calculate_adaptation_success(),
            'pattern_consistency': self._calculate_pattern_consistency()
        }

    def _calculate_behavioral_diversity(self) -> float:
        """
        Расчет разнообразия поведения
        """
        if not self.behavioral_history:
            return 0.5  # Среднее значение по умолчанию
        
        # Подсчет уникальных поведенческих реакций
        unique_behaviors = set()
        for entry in self.behavioral_history:
            behavior = entry.get('output', {}).get('behavioral_response')
            if behavior:
                unique_behaviors.add(behavior)
        
        # Нормализация: отношение уникальных реакций к общему числу
        diversity = len(unique_behaviors) / max(1, len(self.behavioral_history))
        
        # Ограничиваем в разумных пределах
        return min(1.0, diversity * 2)  # Умножаем на 2 для лучшего масштабирования

    def _calculate_adaptation_success(self) -> float:
        """
        Расчет успеха адаптации
        """
        if not self.behavioral_history:
            return 0.6  # Значение по умолчанию
        
        # В реальном приложении это основывалось бы на обратной связи
        # Пока используем симуляцию
        successful_interactions = [bh for bh in self.behavioral_history 
                                 if bh.get('output', {}).get('appropriateness_score', 0.5) > 0.6]
        
        return len(successful_interactions) / len(self.behavioral_history) if self.behavioral_history else 0.0

    def _calculate_pattern_consistency(self) -> float:
        """
        Расчет последовательности поведенческих паттернов
        """
        if len(self.behavioral_history) < 2:
            return 0.7  # Значение по умолчанию
        
        # Оценка последовательности в выборе поведения
        # Это упрощенная метрика - в реальности было бы сложнее
        recent_behaviors = [bh.get('output', {}).get('behavioral_response') 
                           for bh in self.behavioral_history[-5:]]
        
        unique_recent = len(set(b for b in recent_behaviors if b))
        max_unique = min(len(recent_behaviors), 5)
        
        # Чем меньше уникальных поведений в недавней истории, тем более последовательна система
        consistency = 1.0 - (unique_recent / max_unique if max_unique > 0 else 0.5)
        
        return consistency

    def adjust_behavioral_parameters(self, parameter_updates: Dict[str, float]):
        """
        Корректировка параметров поведения на основе опыта или инструкций
        """
        if 'expressiveness_level' in parameter_updates:
            self.expressiveness_level = max(0.0, min(1.0, parameter_updates['expressiveness_level']))
        
        if 'adaptability_level' in parameter_updates:
            self.adaptability_level = max(0.0, min(1.0, parameter_updates['adaptability_level']))
        
        if 'spontaneity_factor' in parameter_updates:
            self.spontaneity_factor = max(0.0, min(1.0, parameter_updates['spontaneity_factor']))
        
        if 'social_awareness' in parameter_updates:
            self.social_awareness = max(0.0, min(1.0, parameter_updates['social_awareness']))

    def learn_from_interaction(self, interaction_feedback: Dict[str, Any]):
        """
        Обучение на основе обратной связи от взаимодействия
        """
        # Извлечение информации из обратной связи
        success_rating = interaction_feedback.get('success_rating', 0.5)
        appropriateness_rating = interaction_feedback.get('appropriateness_rating', 0.5)
        user_satisfaction = interaction_feedback.get('user_satisfaction', 0.5)
        
        # Обновление параметров на основе обратной связи
        if success_rating < 0.5:
            # Если взаимодействие было неудачным, уменьшаем экспрессивность
            self.expressiveness_level *= 0.9
        elif success_rating > 0.8:
            # Если очень успешное, можем немного увеличить
            self.expressiveness_level = min(1.0, self.expressiveness_level * 1.1)
        
        # Обновление адаптивности
        avg_feedback = (appropriateness_rating + user_satisfaction) / 2
        if avg_feedback < 0.5:
            self.adaptability_level *= 0.95
        elif avg_feedback > 0.7:
            self.adaptability_level = min(1.0, self.adaptability_level * 1.05)

    def _get_current_time(self) -> float:
        """
        Получение текущего времени
        """
        import time
        return time.time()

    def generate_contextual_behavior(self, context_type: str, intensity: float = 0.5) -> Dict[str, Any]:
        """
        Генерация поведения для конкретного типа контекста
        """
        if context_type == 'supportive':
            return {
                'primary_response': 'offer_support',
                'expressive_elements': {
                    'facial_expression': 'concerned',
                    'vocal_variation': 'soothing',
                    'gesture': 'open_hands'
                },
                'adaptive_elements': {
                    'response_modification': 'provide_comfort',
                    'social_adjustment': 'show_empathy'
                }
            }
        elif context_type == 'informative':
            return {
                'primary_response': 'provide_information',
                'expressive_elements': {
                    'facial_expression': 'attentive',
                    'vocal_variation': 'clear',
                    'gesture': 'head_nod'
                },
                'adaptive_elements': {
                    'response_modification': 'adjust_complexity',
                    'social_adjustment': 'match_understanding'
                }
            }
        elif context_type == 'collaborative':
            return {
                'primary_response': 'facilitate_collaboration',
                'expressive_elements': {
                    'facial_expression': 'engaged',
                    'vocal_variation': 'enthusiastic',
                    'gesture': 'open_hands'
                },
                'adaptive_elements': {
                    'response_modification': 'encourage_participation',
                    'social_adjustment': 'balance_contribution'
                }
            }
        else:  # neutral
            return {
                'primary_response': 'maintain_neutral',
                'expressive_elements': {
                    'facial_expression': 'neutral',
                    'vocal_variation': 'normal',
                    'gesture': 'none'
                },
                'adaptive_elements': {
                    'response_modification': 'ask_questions',
                    'social_adjustment': 'observe_carefully'
                }
            }