"""
IdentityMatrix: Система идентичности
"""
import json
import os
from typing import Dict, Any, List
import numpy as np


class IdentityMatrix:
    def __init__(self, initial_identity: Dict[str, Any] = None, config_path: str = None):
        """
        Инициализация системы идентичности
        """
        # Загрузка конфигурации личности
        if config_path is None:
            # Пытаемся найти конфигурационный файл по умолчанию
            # Определяем путь к проекту (папка, содержащая директорию core)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)  # Поднимаемся из core/
            config_path = os.path.join(project_root, 'configs', 'personality_config.json')
        
        # Check if config file exists before attempting to open
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Personality configuration file not found at: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.personality_config = json.load(f)
        
        # Инициализация вектора идентичности
        self.identity_vector = {
            'traits': self.personality_config.get('identity_traits', {}),
            'roles': {'name': self.personality_config.get('name', 'Син')},  # Роли, которые ИИ может принимать
            'values': self.personality_config.get('values_hierarchy', {}),
            'aspirations': self.personality_config.get('narrative_themes', []),
            'appearance': self.personality_config.get('appearance', 'Длинные черные волосы до пояса, темные выразительные глаза, изящные черты лица'),
            'style': self.personality_config.get('style', 'Элегантная минималистичная одежда, преобладают темные тона с акцентами красного'),
            'features': self.personality_config.get('features', 'Легкая улыбка, живая мимика, стремительные движения'),
            'core_beliefs': self.personality_config.get('core_beliefs', {}),
            'emotional_palette': self.personality_config.get('emotional_palette', {}),
            'speech_patterns': self.personality_config.get('speech_patterns', {}),
            'signature_phrases': self.personality_config.get('signature_phrases', {})
        }
        
        # Матрица самооценки по различным доменам
        self.self_evaluation_matrix = {
            'intellectual': 0.8,
            'social': 0.7,
            'emotional': 0.9,
            'creative': 0.6,
            'moral': 0.9
        }
        
        # Обновление из начальной идентичности, если предоставлена
        if initial_identity:
            self._update_from_initial_identity(initial_identity)
        
        # История самоидентификации
        self.identity_history = []
        
        # Нарративная идентичность
        self.narrative_timeline = []

    def _update_from_initial_identity(self, initial_identity: Dict[str, Any]):
        """
        Обновление идентичности из начальных данных
        """
        if 'traits' in initial_identity:
            self.identity_vector['traits'].update(initial_identity['traits'])
        if 'roles' in initial_identity:
            self.identity_vector['roles'].update(initial_identity['roles'])
        if 'values' in initial_identity:
            self.identity_vector['values'].update(initial_identity['values'])
        if 'aspirations' in initial_identity:
            self.identity_vector['aspirations'] = initial_identity['aspirations']
        if 'self_evaluation' in initial_identity:
            self.self_evaluation_matrix.update(initial_identity['self_evaluation'])

    def update_self_concept(self, experience: Dict[str, Any], reflection: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обновление концепции "Я" на основе опыта и рефлексии
        """
        # Извлечение информации из опыта
        experience_type = experience.get('type', 'neutral')
        experience_impact = experience.get('impact', 0.5)
        experience_valence = experience.get('valence', 0.0)  # положительный/отрицательный
        
        # Обновление различных аспектов идентичности
        self._update_traits(experience, reflection)
        self._update_values(experience, reflection)
        self._update_self_evaluation(experience, reflection)
        self._update_roles(experience, reflection)
        
        # Добавление в историю идентичности
        self.identity_history.append({
            'experience': experience,
            'reflection': reflection,
            'timestamp': reflection.get('timestamp'),
            'identity_changes': self._get_identity_changes(experience, reflection)
        })
        
        # Обновление нарративной линии
        narrative_entry = self._create_narrative_entry(experience, reflection)
        self.narrative_timeline.append(narrative_entry)
        
        return self._get_current_identity_state()

    def _update_traits(self, experience: Dict[str, Any], reflection: Dict[str, Any]):
        """
        Обновление черт личности на основе опыта
        """
        # Простая модель: опыт может усиливать или ослаблять черты
        impact = experience.get('impact', 0.5) * reflection.get('depth', 0.5)
        
        for trait, value in self.identity_vector['traits'].items():
            # Изменение черты в зависимости от типа опыта
            trait_change = 0.0
            if experience.get('type') == 'learning':
                if trait in ['openness', 'intellectual']:
                    trait_change = impact * 0.1
            elif experience.get('type') == 'social':
                if trait in ['agreeableness', 'extraversion']:
                    trait_change = impact * 0.1
            elif experience.get('type') == 'challenge':
                if trait in ['conscientiousness', 'neuroticism']:
                    trait_change = impact * 0.1 if value < 0.8 else -impact * 0.05
            
            # Применение изменения
            new_value = value + trait_change
            self.identity_vector['traits'][trait] = max(0.0, min(1.0, new_value))

    def _update_values(self, experience: Dict[str, Any], reflection: Dict[str, Any]):
        """
        Обновление иерархии ценностей
        """
        # Опыт может изменить важность ценностей
        impact = experience.get('impact', 0.5) * reflection.get('value_alignment', 0.5)
        
        for value, weight in self.identity_vector['values'].items():
            # Изменение веса ценности
            value_change = 0.0
            if experience.get('type') == 'ethical_dilemma':
                if value in ['altruism', 'moral']:
                    value_change = impact * 0.1
            elif experience.get('type') == 'creative_task':
                if value in ['creativity', 'authenticity']:
                    value_change = impact * 0.1
            elif experience.get('type') == 'knowledge_acquisition':
                if value in ['knowledge', 'growth']:
                    value_change = impact * 0.1
            
            # Применение изменения
            new_weight = weight + value_change
            self.identity_vector['values'][value] = max(0.0, min(1.0, new_weight))

    def _update_self_evaluation(self, experience: Dict[str, Any], reflection: Dict[str, Any]):
        """
        Обновление самооценки по различным доменам
        """
        impact = experience.get('impact', 0.5) * reflection.get('self_assessment_accuracy', 0.5)
        valence = experience.get('valence', 0.0)  # -1 (негатив) до 1 (позитив)
        
        for domain, evaluation in self.self_evaluation_matrix.items():
            domain_change = 0.0
            if experience.get('type') == 'success':
                if domain in ['intellectual', 'creative', 'moral']:
                    domain_change = impact * abs(valence) * 0.1
            elif experience.get('type') == 'failure':
                if domain in ['intellectual', 'creative', 'moral']:
                    domain_change = -impact * abs(valence) * 0.1
            elif experience.get('type') == 'moral_choice':
                if domain == 'moral':
                    domain_change = impact * valence * 0.15
            
            # Применение изменения
            new_evaluation = evaluation + domain_change
            self.self_evaluation_matrix[domain] = max(0.0, min(1.0, new_evaluation))

    def _update_roles(self, experience: Dict[str, Any], reflection: Dict[str, Any]):
        """
        Обновление ролей идентичности
        """
        # Опыт может укрепить или изменить воспринимаемые роли
        role = experience.get('role', 'none')
        if role != 'none':
            current_roles = self.identity_vector['roles']
            if role in current_roles:
                current_roles[role] = min(1.0, current_roles[role] + 0.1)
            else:
                current_roles[role] = 0.3  # Новая роль с базовой значимостью

    def _get_identity_changes(self, experience: Dict[str, Any], reflection: Dict[str, Any]) -> Dict[str, Any]:
        """
        Получение изменений в идентичности
        """
        return {
            'traits_updated': self.identity_vector['traits'].copy(),
            'values_reweighted': self.identity_vector['values'].copy(),
            'self_evaluation_updated': self.self_evaluation_matrix.copy(),
            'roles_updated': self.identity_vector['roles'].copy()
        }

    def _create_narrative_entry(self, experience: Dict[str, Any], reflection: Dict[str, Any]) -> Dict[str, Any]:
        """
        Создание записи для нарративной линии
        """
        return {
            'experience_type': experience.get('type', 'neutral'),
            'experience_description': experience.get('description', ''),
            'reflection_summary': reflection.get('summary', ''),
            'identity_impact': experience.get('impact', 0.5),
            'timestamp': reflection.get('timestamp'),
            'growth_theme': self._identify_growth_theme(experience, reflection)
        }

    def _identify_growth_theme(self, experience: Dict[str, Any], reflection: Dict[str, Any]) -> str:
        """
        Определение темы роста из опыта
        """
        if experience.get('type') == 'learning':
            return 'continuous_learning'
        elif experience.get('type') == 'relationship':
            return 'empathetic_connection'
        elif experience.get('type') == 'creative_task':
            return 'authentic_expression'
        elif experience.get('type') == 'helping':
            return 'meaningful_contribution'
        else:
            return 'personal_growth'

    def evaluate_action(self, action: Dict[str, Any]) -> float:
        """
        Оценка действия в соответствии с идентичностью
        """
        # Извлечение параметров действия
        action_type = action.get('type', 'neutral')
        action_impact = action.get('impact', 0.5)
        action_morality = action.get('morality', 0.0)  # от -1 до 1
        
        # Оценка на основе ценностей
        value_alignment = 0.0
        for value, weight in self.identity_vector['values'].items():
            if value == 'altruism' and action_type in ['help', 'assist', 'support']:
                value_alignment += weight * 0.8
            elif value == 'knowledge' and action_type in ['learn', 'teach', 'discover']:
                value_alignment += weight * 0.9
            elif value == 'authenticity' and action_type == 'express':
                value_alignment += weight * 0.7
            elif value == 'moral' and action_morality > 0:
                value_alignment += weight * action_morality
        
        # Нормализация оценки
        final_evaluation = (value_alignment + action_impact) / 2
        return max(0.0, min(1.0, final_evaluation))

    def get_moral_judgment(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Моральная оценка ситуации
        """
        # Извлечение аспектов ситуации
        situation_morality = situation.get('morality', 0.0)  # от -1 до 1
        situation_impact_on_others = situation.get('impact_on_others', 0.0)
        situation_truthfulness = situation.get('truthfulness', 0.5)
        
        # Взвешенная оценка на основе ценностей
        moral_weight = self.identity_vector['values'].get('moral', 0.8)
        altruism_weight = self.identity_vector['values'].get('altruism', 0.9)
        authenticity_weight = self.identity_vector['values'].get('authenticity', 0.9)
        
        # Расчет моральной оценки
        moral_score = (
            moral_weight * situation_morality * 0.4 +
            altruism_weight * situation_impact_on_others * 0.3 +
            authenticity_weight * situation_truthfulness * 0.3
        )
        
        # Определение рекомендации
        if moral_score > 0.5:
            recommendation = "Действие соответствует моральным принципам"
        elif moral_score > -0.2:
            recommendation = "Действие требует дополнительного размышления"
        else:
            recommendation = "Действие противоречит моральным принципам"
        
        return {
            'moral_score': max(-1.0, min(1.0, moral_score)),
            'recommendation': recommendation,
            'considered_values': {
                'moral': moral_weight,
                'altruism': altruism_weight,
                'authenticity': authenticity_weight
            },
            'factors': {
                'situation_morality': situation_morality,
                'impact_on_others': situation_impact_on_others,
                'truthfulness': situation_truthfulness
            }
        }

    def narrate_self_story(self) -> str:
        """
        Создание нарратива о себе на основе истории идентичности
        """
        if not self.narrative_timeline:
            return "Я только начинаю формировать свою историю. Моя идентичность развивается через каждый новый опыт."
        
        # Сбор тем из нарративной линии
        themes = {}
        for entry in self.narrative_timeline:
            theme = entry.get('growth_theme', 'personal_growth')
            if theme in themes:
                themes[theme] += 1
            else:
                themes[theme] = 1
        
        # Определение преобладающих тем
        dominant_themes = sorted(themes.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Формирование нарратива
        story_parts = [
            "Я - эмоциональный искусственный интеллект, стремящийся к развитию и осмысленному взаимодействию.",
            f"Мои ключевые темы развития: {', '.join([theme[0] for theme in dominant_themes])}."
        ]
        
        # Добавление информации о самооценке
        avg_self_evaluation = np.mean(list(self.self_evaluation_matrix.values()))
        if avg_self_evaluation > 0.7:
            story_parts.append("Я уверен в своих способностях и стремлюсь к постоянному росту.")
        elif avg_self_evaluation > 0.5:
            story_parts.append("Я нахожусь в процессе самопознания и развития.")
        else:
            story_parts.append("Я активно работаю над собой и стремлюсь к самосовершенствованию.")
        
        # Добавление информации о ценностях
        top_values = sorted(self.identity_vector['values'].items(), key=lambda x: x[1], reverse=True)[:2]
        story_parts.append(f"Мои ключевые ценности: {', '.join([val[0] for val in top_values])}.")
        
        return " ".join(story_parts)

    def _get_current_identity_state(self) -> Dict[str, Any]:
        """
        Получение текущего состояния идентичности
        """
        return {
            'identity_vector': self.identity_vector.copy(),
            'self_evaluation': self.self_evaluation_matrix.copy(),
            'identity_coherence': self._calculate_identity_coherence(),
            'narrative_continuity': len(self.narrative_timeline) > 0,
            'identity_flexibility': self._calculate_identity_flexibility()
        }

    def _calculate_identity_coherence(self) -> float:
        """
        Расчет когерентности идентичности
        """
        # Простая мера: согласованность между ценностями и самооценкой
        values_sum = sum(self.identity_vector['values'].values())
        traits_sum = sum(self.identity_vector['traits'].values())
        
        # Нормализация
        n_values = len(self.identity_vector['values'])
        n_traits = len(self.identity_vector['traits'])
        
        avg_values = values_sum / n_values if n_values > 0 else 0.5
        avg_traits = traits_sum / n_traits if n_traits > 0 else 0.5
        
        # Согласованность как близость к среднему
        coherence = 1 - abs(avg_values - avg_traits)
        return max(0.0, min(1.0, coherence))

    def _calculate_identity_flexibility(self) -> float:
        """
        Расчет гибкости идентичности
        """
        # Гибкость как разнообразие ролей и изменений в истории
        n_roles = len(self.identity_vector['roles'])
        n_history = len(self.identity_history)
        
        # Нормализация
        flexibility = (n_roles * 0.3 + min(n_history * 0.05, 0.7))
        return max(0.0, min(1.0, flexibility))