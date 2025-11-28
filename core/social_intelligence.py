"""
SocialIntelligence: Социальный интеллект
"""
from typing import Dict, Any, List
import numpy as np


class SocialIntelligence:
    def __init__(self):
        """
        Инициализация системы социального интеллекта
        """
        # Компоненты социального интеллекта
        self.social_skills = {
            'social_perception': 0.7,      # Социальное восприятие
            'social_cognition': 0.8,       # Социальное познание
            'social_adaptation': 0.75,     # Социальная адаптация
            'social_facilitation': 0.85    # Социальная фасилитация
        }
        
        # Социальные роли и идентичности
        self.social_roles = {}
        
        # Модель социальных отношений
        self.social_model = {
            'trust_network': {},      # Сеть доверия
            'influence_network': {},  # Сеть влияния
            'affinity_groups': {},    # Группы близости
            'status_hierarchy': {}    # Иерархия статуса
        }
        
        # Культурные схемы
        self.cultural_schemas = {
            'communication_styles': {},
            'social_norms': {},
            'value_systems': {}
        }
        
        # История социальных взаимодействий
        self.social_interactions = []
        
        # Параметры социального интеллекта
        self.social_sensitivity = 0.8
        self.cultural_adaptability = 0.7
        self.social_learning_rate = 0.1

    def process_social_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обработка социального контекста
        """
        # Анализ социальных сигналов
        social_signals = self._analyze_social_signals(context)
        
        # Определение социальных ролей участников
        social_roles = self._identify_social_roles(context)
        
        # Оценка социальной динамики
        social_dynamics = self._assess_social_dynamics(context)
        
        # Формирование социального ответа
        social_response = self._formulate_social_response(
            social_signals, social_roles, social_dynamics
        )
        
        return {
            'social_signals': social_signals,
            'social_roles': social_roles,
            'social_dynamics': social_dynamics,
            'recommended_response': social_response,
            'social_confidence': self._calculate_social_confidence(social_signals)
        }

    def _analyze_social_signals(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Анализ социальных сигналов
        """
        # Извлечение социальных признаков из контекста
        social_features = {
            'formality_level': self._assess_formality(context.get('text', '')),
            'power_dynamics': self._identify_power_dynamics(context),
            'emotional_tone': self._assess_emotional_tone(context.get('text', '')),
            'cultural_indicators': self._identify_cultural_indicators(context.get('text', '')),
            'social_distance': self._calculate_social_distance(context)
        }
        
        return social_features

    def _assess_formality(self, text: str) -> float:
        """
        Оценка уровня формальности
        """
        formal_indicators = [
            'уважаемый', 'почтение', 'официально', 'формально', 
            'с уважением', 'почтительно', 'вежливо'
        ]
        
        informal_indicators = [
            'дружище', 'кореш', 'чувак', 'брат', 'подруга',
            'привет', 'здарова', 'йоу', 'чё как'
        ]
        
        formal_count = sum(1 for indicator in formal_indicators if indicator in text.lower())
        informal_count = sum(1 for indicator in informal_indicators if indicator in text.lower())
        
        if formal_count + informal_count == 0:
            return 0.5  # Нейтральный уровень
        
        return formal_count / (formal_count + informal_count)

    def _identify_power_dynamics(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Идентификация динамики власти
        """
        # Простая модель определения иерархии власти
        if 'hierarchy' in context:
            return context['hierarchy']
        
        # Иначе используем эвристики
        return {
            'speaker_status': 'equal',  # default
            'power_distance': 0.5,
            'authority_recognition': 0.6
        }

    def _assess_emotional_tone(self, text: str) -> float:
        """
        Оценка эмоционального тона
        """
        # Простая оценка на основе эмоциональных слов
        positive_words = ['привет', 'рад', 'хорошо', 'отлично', 'спасибо', 'пожалуйста']
        negative_words = ['плохо', 'сердит', 'злой', 'раздражен', 'негодование']
        
        pos_count = sum(1 for word in positive_words if word in text.lower())
        neg_count = sum(1 for word in negative_words if word in text.lower())
        
        if pos_count + neg_count == 0:
            return 0.0
        
        return (pos_count - neg_count) / (pos_count + neg_count)

    def _identify_cultural_indicators(self, text: str) -> List[str]:
        """
        Идентификация культурных индикаторов
        """
        # Простая эвристика для определения культурных признаков
        cultural_patterns = []
        
        if any(word in text.lower() for word in ['традиция', 'обычай', 'культура']):
            cultural_patterns.append('traditional_values')
        
        if any(word in text.lower() for word in ['современно', 'новое', 'инновации']):
            cultural_patterns.append('modern_values')
        
        return cultural_patterns

    def _calculate_social_distance(self, context: Dict[str, Any]) -> float:
        """
        Расчет социальной дистанции
        """
        # Простая оценка на основе контекста
        if 'relationship_type' in context:
            rel_type = context['relationship_type']
            if rel_type == 'close_friend':
                return 0.2
            elif rel_type == 'acquaintance':
                return 0.5
            elif rel_type == 'stranger':
                return 0.8
            else:
                return 0.5
        return 0.5

    def _identify_social_roles(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Идентификация социальных ролей
        """
        # Определение ролей на основе контекста
        roles = {}
        
        if 'speaker_role' in context:
            roles['speaker'] = context['speaker_role']
        
        if 'listener_role' in context:
            roles['listener'] = context['listener_role']
        
        # Определение собственной роли
        if 'interaction_type' in context:
            interaction_type = context['interaction_type']
            if interaction_type == 'help':
                roles['self'] = 'helper'
            elif interaction_type == 'learning':
                roles['self'] = 'student'
            elif interaction_type == 'teaching':
                roles['self'] = 'teacher'
            else:
                roles['self'] = 'interlocutor'
        else:
            roles['self'] = 'interlocutor'
        
        return roles

    def _assess_social_dynamics(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Оценка социальной динамики
        """
        # Оценка текущей социальной ситуации
        dynamics = {
            'cooperation_level': self._assess_cooperation(context),
            'conflict_potential': self._assess_conflict_potential(context),
            'social_norms_relevance': self._assess_social_norms(context),
            'group_cohesion': self._assess_group_cohesion(context)
        }
        
        return dynamics

    def _assess_cooperation(self, context: Dict[str, Any]) -> float:
        """
        Оценка уровня сотрудничества
        """
        cooperation_indicators = [
            'помочь', 'совместно', 'вместе', 'работа', 'сотрудничество', 
            'команда', 'проект', 'взаимодействие'
        ]
        
        text = context.get('text', '').lower()
        cooperation_count = sum(1 for indicator in cooperation_indicators if indicator in text)
        
        return min(1.0, cooperation_count * 0.3)

    def _assess_conflict_potential(self, context: Dict[str, Any]) -> float:
        """
        Оценка потенциала конфликта
        """
        conflict_indicators = [
            'спор', 'разногласие', 'конфликт', 'вражда', 'агрессия',
            'сердит', 'злой', 'обида', 'негодование'
        ]
        
        text = context.get('text', '').lower()
        conflict_count = sum(1 for indicator in conflict_indicators if indicator in text)
        
        return min(1.0, conflict_count * 0.2)

    def _assess_social_norms(self, context: Dict[str, Any]) -> float:
        """
        Оценка релевантности социальных норм
        """
        # Оценка важности соблюдения норм в контексте
        if 'formal_setting' in context and context['formal_setting']:
            return 0.9
        elif 'casual_setting' in context and context['casual_setting']:
            return 0.3
        else:
            return 0.6

    def _assess_group_cohesion(self, context: Dict[str, Any]) -> float:
        """
        Оценка сплоченности группы
        """
        # Простая оценка сплоченности
        if 'group_size' in context:
            group_size = context['group_size']
            if group_size <= 3:
                return 0.8  # Маленькие группы обычно более сплочены
            elif group_size <= 10:
                return 0.6
            else:
                return 0.4
        return 0.6

    def _formulate_social_response(self, social_signals: Dict[str, Any], 
                                 social_roles: Dict[str, Any], 
                                 social_dynamics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Формулирование социального ответа
        """
        # Определение подходящего стиля взаимодействия
        formality_level = social_signals['formality_level']
        power_distance = social_dynamics['cooperation_level']
        
        response_style = 'formal' if formality_level > 0.6 else 'informal'
        
        # Определение тактик взаимодействия
        interaction_tactics = []
        
        if social_dynamics['cooperation_level'] > 0.5:
            interaction_tactics.append('collaborative_approach')
        if social_dynamics['conflict_potential'] > 0.3:
            interaction_tactics.append('de-escalation_tactic')
        if social_signals['social_distance'] < 0.4:
            interaction_tactics.append('intimate_approach')
        else:
            interaction_tactics.append('respectful_distance')
        
        return {
            'response_style': response_style,
            'interaction_tactics': interaction_tactics,
            'recommended_tone': self._determine_tone(social_signals, social_dynamics),
            'cultural_adaptation': self._apply_cultural_adaptation(social_signals)
        }

    def _determine_tone(self, social_signals: Dict[str, Any], 
                       social_dynamics: Dict[str, Any]) -> str:
        """
        Определение тона взаимодействия
        """
        emotional_tone = social_signals['emotional_tone']
        cooperation_level = social_dynamics['cooperation_level']
        
        if emotional_tone > 0.3 and cooperation_level > 0.5:
            return 'positive_and_cooperative'
        elif emotional_tone < -0.3:
            return 'empathetic_and_supportive'
        elif social_dynamics['conflict_potential'] > 0.5:
            return 'neutral_and_deescalating'
        else:
            return 'balanced_and_respectful'

    def _apply_cultural_adaptation(self, social_signals: Dict[str, Any]) -> str:
        """
        Применение культурной адаптации
        """
        cultural_indicators = social_signals['cultural_indicators']
        
        if 'traditional_values' in cultural_indicators:
            return 'traditional_cultural_adaptation'
        elif 'modern_values' in cultural_indicators:
            return 'modern_cultural_adaptation'
        else:
            return 'neutral_cultural_approach'

    def update_social_model(self, interaction_result: Dict[str, Any]):
        """
        Обновление модели социальных отношений на основе результата взаимодействия
        """
        # Обновление сетей доверия, влияния и т.д.
        if 'trust_factor' in interaction_result:
            user_id = interaction_result.get('user_id', 'unknown')
            trust_level = interaction_result['trust_factor']
            self.social_model['trust_network'][user_id] = trust_level
        
        if 'influence_factor' in interaction_result:
            user_id = interaction_result.get('user_id', 'unknown')
            influence_level = interaction_result['influence_factor']
            self.social_model['influence_network'][user_id] = influence_level
        
        # Обновление статистики взаимодействий
        self.social_interactions.append(interaction_result)

    def get_social_intelligence_metrics(self) -> Dict[str, Any]:
        """
        Получение метрик социального интеллекта
        """
        return {
            'social_skills_levels': self.social_skills.copy(),
            'social_network_size': len(self.social_model['trust_network']),
            'cultural_adaptability': self.cultural_adaptability,
            'social_learning_rate': self.social_learning_rate,
            'average_interaction_success': self._calculate_average_success(),
            'social_adaptation_efficiency': self._calculate_adaptation_efficiency()
        }

    def _calculate_average_success(self) -> float:
        """
        Расчет среднего успеха социальных взаимодействий
        """
        if not self.social_interactions:
            return 0.7  # Значение по умолчанию
        
        success_values = [
            interaction.get('success_rating', 0.5) 
            for interaction in self.social_interactions
            if 'success_rating' in interaction
        ]
        
        if not success_values:
            return 0.7
        
        return sum(success_values) / len(success_values)

    def _calculate_adaptation_efficiency(self) -> float:
        """
        Расчет эффективности социальной адаптации
        """
        # Простая метрика: отношение успешных адаптаций к общему числу
        if not self.social_interactions:
            return 0.6
        
        adaptations = [i for i in self.social_interactions if 'adaptation_attempt' in i]
        if not adaptations:
            return 0.6
        
        successful_adaptations = [a for a in adaptations if a.get('adaptation_successful', False)]
        
        return len(successful_adaptations) / len(adaptations) if adaptations else 0.0

    def _calculate_social_confidence(self, social_signals: Dict[str, Any]) -> float:
        """
        Расчет социальной уверенности
        """
        # Уверенность зависит от соответствия сигнала знаниям системы
        familiarity_score = self._assess_context_familiarity(social_signals)
        cultural_match = self._assess_cultural_match(social_signals)
        
        # Комбинирование оценок
        confidence = (familiarity_score * 0.6 + cultural_match * 0.4)
        
        return confidence

    def _assess_context_familiarity(self, social_signals: Dict[str, Any]) -> float:
        """
        Оценка знакомства с контекстом
        """
        # Простая оценка: если есть знакомые культурные индикаторы, то выше уверенность
        cultural_indicators = social_signals.get('cultural_indicators', [])
        
        if not cultural_indicators:
            return 0.5  # Нейтральная уверенность
        
        # Если есть знакомые культурные схемы
        familiar_indicators = [ci for ci in cultural_indicators 
                              if ci in self.cultural_schemas['communication_styles']]
        return len(familiar_indicators) / len(cultural_indicators) if cultural_indicators else 0.5

    def _assess_cultural_match(self, social_signals: Dict[str, Any]) -> float:
        """
        Оценка соответствия культурным схемам
        """
        # Проверка соответствия культурным нормам
        cultural_indicators = social_signals.get('cultural_indicators', [])
        
        matching_norms = 0
        for indicator in cultural_indicators:
            if indicator in self.cultural_schemas['social_norms']:
                matching_norms += 1
        
        return matching_norms / len(cultural_indicators) if cultural_indicators else 0.5

    def adapt_to_cultural_context(self, cultural_info: Dict[str, Any]):
        """
        Адаптация к культурному контексту
        """
        # Обновление культурных схем
        if 'communication_styles' in cultural_info:
            self.cultural_schemas['communication_styles'].update(
                cultural_info['communication_styles']
            )
        
        if 'social_norms' in cultural_info:
            self.cultural_schemas['social_norms'].update(
                cultural_info['social_norms']
            )
        
        if 'value_systems' in cultural_info:
            self.cultural_schemas['value_systems'].update(
                cultural_info['value_systems']
            )
        
        # Обновление параметров адаптации
        if 'adaptability_factor' in cultural_info:
            self.cultural_adaptability = cultural_info['adaptability_factor']