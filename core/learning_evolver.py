"""
LearningEvolver: Система обучения
"""
from typing import Dict, Any, List
import numpy as np
import time


class LearningEvolver:
    def __init__(self):
        """
        Инициализация системы обучения
        """
        # Компоненты обучения
        self.learning_components = {
            'associative_learning': 0.7,    # Ассоциативное обучение
            'reinforcement_learning': 0.8,  # Обучение с подкреплением
            'observational_learning': 0.6,  # Обучение через наблюдение
            'insight_learning': 0.5,        # Обучение через озарение
            'imprinting': 0.3               # Импринтинг (ранние усвоения)
        }
        
        # Параметры обучения
        self.learning_rate = 0.1
        self.forgetting_rate = 0.01
        self.transfer_efficiency = 0.6
        self.meta_learning_rate = 0.2
        
        # История обучения
        self.learning_episodes = []
        self.skill_progressions = {}
        self.knowledge_graph = {}
        
        # Система мотивации
        self.motivation_system = {
            'curiosity_drive': 0.7,
            'achievement_drive': 0.6,
            'social_drive': 0.8,
            'survival_drive': 0.4  # Для симуляции выживательных инстинктов
        }
        
        # Оценка эффективности обучения
        self.performance_metrics = {
            'accuracy_improvement': 0.0,
            'speed_improvement': 0.0,
            'adaptation_rate': 0.0,
            'generalization_ability': 0.0
        }
        
        # Гиперпараметры для адаптации
        self.hyperparameters = {
            'learning_rate': 0.1,
            'exploration_rate': 0.3,
            'exploitation_rate': 0.7,
            'memory_decay': 0.01
        }

    def process_learning_experience(self, experience: Dict[str, Any], 
                                  feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обработка обучающего опыта с обратной связью
        """
        start_time = time.time()
        
        # Классификация типа опыта
        experience_type = self._classify_experience_type(experience)
        
        # Обновление соответствующей системы обучения
        learning_outcome = self._apply_learning_rule(experience, feedback, experience_type)
        
        # Обновление навыков и знаний
        self._update_skills_and_knowledge(experience, learning_outcome)
        
        # Обновление мотивационной системы
        self._update_motivation(feedback)
        
        # Запись эпизода обучения
        episode = {
            'experience': experience,
            'feedback': feedback,
            'experience_type': experience_type,
            'learning_outcome': learning_outcome,
            'timestamp': start_time,
            'processing_time': time.time() - start_time
        }
        self.learning_episodes.append(episode)
        
        # Очистка старых эпизодов
        if len(self.learning_episodes) > 1000:
            self.learning_episodes = self.learning_episodes[-500:]
        
        return {
            'learning_outcome': learning_outcome,
            'skill_updates': learning_outcome.get('skill_updates', {}),
            'knowledge_updates': learning_outcome.get('knowledge_updates', {}),
            'motivation_changes': self.motivation_system.copy()
        }

    def _classify_experience_type(self, experience: Dict[str, Any]) -> str:
        """
        Классификация типа обучающего опыта
        """
        if 'association' in experience:
            return 'associative'
        elif 'reward' in experience or 'feedback' in experience:
            return 'reinforcement'
        elif 'observation' in experience:
            return 'observational'
        elif 'problem_solving' in experience and experience.get('insight_moment', False):
            return 'insight'
        elif 'early_learning' in experience:
            return 'imprinting'
        else:
            return 'associative'  # по умолчанию

    def _apply_learning_rule(self, experience: Dict[str, Any], 
                           feedback: Dict[str, Any], 
                           exp_type: str) -> Dict[str, Any]:
        """
        Применение соответствующего правила обучения
        """
        if exp_type == 'associative':
            return self._associative_learning(experience, feedback)
        elif exp_type == 'reinforcement':
            return self._reinforcement_learning(experience, feedback)
        elif exp_type == 'observational':
            return self._observational_learning(experience, feedback)
        elif exp_type == 'insight':
            return self._insight_learning(experience, feedback)
        elif exp_type == 'imprinting':
            return self._imprinting_learning(experience, feedback)
        else:
            return self._default_learning(experience, feedback)

    def _associative_learning(self, experience: Dict[str, Any], 
                            feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ассоциативное обучение (условные рефлексы, связи между стимулами)
        """
        # Извлечение стимулов и реакций
        stimulus = experience.get('stimulus', 'unknown')
        response = experience.get('response', 'unknown')
        outcome = feedback.get('outcome', 'neutral')
        
        # Создание или обновление ассоциативной связи
        if stimulus not in self.knowledge_graph:
            self.knowledge_graph[stimulus] = {}
        
        if response not in self.knowledge_graph[stimulus]:
            self.knowledge_graph[stimulus][response] = {
                'strength': 0.1,
                'frequency': 0,
                'last_updated': time.time()
            }
        
        # Обновление силы связи на основе результата
        current_strength = self.knowledge_graph[stimulus][response]['strength']
        reward_factor = 1.0 if outcome == 'positive' else -0.5 if outcome == 'negative' else 0.0
        
        new_strength = current_strength + self.learning_rate * reward_factor
        new_strength = max(0.0, min(1.0, new_strength))
        
        self.knowledge_graph[stimulus][response]['strength'] = new_strength
        self.knowledge_graph[stimulus][response]['frequency'] += 1
        
        # Обновление компонента ассоциативного обучения
        self.learning_components['associative_learning'] = min(1.0, 
            self.learning_components['associative_learning'] + 0.01 * reward_factor)
        
        return {
            'type': 'associative',
            'stimulus': stimulus,
            'response': response,
            'strength_change': new_strength - current_strength,
            'association_strength': new_strength
        }

    def _reinforcement_learning(self, experience: Dict[str, Any], 
                              feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обучение с подкреплением (Q-обучение, временные различия)
        """
        state = experience.get('state', 'unknown')
        action = experience.get('action', 'unknown')
        reward = feedback.get('reward', 0.0)
        next_state = experience.get('next_state')
        
        # Инициализация Q-значений
        if state not in self.knowledge_graph:
            self.knowledge_graph[state] = {'q_values': {}}
        
        if action not in self.knowledge_graph[state]['q_values']:
            self.knowledge_graph[state]['q_values'][action] = 0.0
        
        # Обновление Q-значения (упрощенное TD-обучение)
        old_q = self.knowledge_graph[state]['q_values'][action]
        max_next_q = max(self.knowledge_graph.get(next_state, {}).get('q_values', {}).values()) if next_state else 0.0
        
        # Q-learning update rule: Q(s,a) = Q(s,a) + α[r + γ*max Q(s',a') - Q(s,a)]
        learning_rate = self.hyperparameters['learning_rate']
        discount_factor = 0.9  # γ
        
        new_q = old_q + learning_rate * (reward + discount_factor * max_next_q - old_q)
        self.knowledge_graph[state]['q_values'][action] = new_q
        
        # Обновление компонента обучения с подкреплением
        improvement_factor = abs(new_q - old_q)
        self.learning_components['reinforcement_learning'] = min(1.0, 
            self.learning_components['reinforcement_learning'] + 0.02 * improvement_factor)
        
        return {
            'type': 'reinforcement',
            'state': state,
            'action': action,
            'reward': reward,
            'q_value_change': new_q - old_q,
            'new_q_value': new_q
        }

    def _observational_learning(self, experience: Dict[str, Any], 
                              feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обучение через наблюдение (социальное обучение)
        """
        observed_behavior = experience.get('observed_behavior', {})
        model = experience.get('model', 'unknown')
        outcome = feedback.get('outcome', 'neutral')
        
        # Обновление знаний о поведении модели
        if model not in self.knowledge_graph:
            self.knowledge_graph[model] = {'observed_behaviors': {}}
        
        behavior_name = observed_behavior.get('name', 'unknown')
        behavior_outcome = observed_behavior.get('outcome', outcome)
        
        if behavior_name not in self.knowledge_graph[model]['observed_behaviors']:
            self.knowledge_graph[model]['observed_behaviors'][behavior_name] = {
                'success_count': 0,
                'failure_count': 0,
                'total_observations': 0
            }
        
        obs_data = self.knowledge_graph[model]['observed_behaviors'][behavior_name]
        obs_data['total_observations'] += 1
        
        if behavior_outcome == 'positive':
            obs_data['success_count'] += 1
        else:
            obs_data['failure_count'] += 1
        
        # Вероятность успеха наблюдаемого поведения
        success_prob = obs_data['success_count'] / obs_data['total_observations']
        
        # Обновление компонента наблюдательного обучения
        self.learning_components['observational_learning'] = min(1.0, 
            self.learning_components['observational_learning'] + 0.01 * success_prob)
        
        return {
            'type': 'observational',
            'model': model,
            'behavior': behavior_name,
            'success_probability': success_prob,
            'total_observations': obs_data['total_observations']
        }

    def _insight_learning(self, experience: Dict[str, Any], 
                        feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обучение через озарение (понимание связей)
        """
        problem = experience.get('problem', 'unknown')
        solution_path = experience.get('solution_path', [])
        insight_level = experience.get('insight_level', 0.5)
        
        # Обновление знаний о решении проблемы
        if problem not in self.knowledge_graph:
            self.knowledge_graph[problem] = {'solution_paths': []}
        
        self.knowledge_graph[problem]['solution_paths'].append({
            'path': solution_path,
            'insight_level': insight_level,
            'timestamp': time.time()
        })
        
        # Обновление компонента обучения через озарение
        self.learning_components['insight_learning'] = min(1.0, 
            self.learning_components['insight_learning'] + 0.05 * insight_level)
        
        return {
            'type': 'insight',
            'problem': problem,
            'solution_path': solution_path,
            'insight_level': insight_level,
            'path_count': len(self.knowledge_graph[problem]['solution_paths'])
        }

    def _imprinting_learning(self, experience: Dict[str, Any], 
                           feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        Импринтинг (ранние фундаментальные усвоения)
        """
        core_concept = experience.get('core_concept', 'unknown')
        value = experience.get('value', 1.0)  # Сила усвоения
        
        # Импринтинг укореняет концепцию глубоко
        if core_concept not in self.knowledge_graph:
            self.knowledge_graph[core_concept] = {'imprinted': True, 'value': value}
        else:
            # Укрепление уже существующей концепции
            self.knowledge_graph[core_concept]['value'] = max(
                self.knowledge_graph[core_concept]['value'], value
            )
        
        # Обновление компонента импринтинга
        self.learning_components['imprinting'] = min(1.0, 
            self.learning_components['imprinting'] + 0.1 * value)
        
        return {
            'type': 'imprinting',
            'concept': core_concept,
            'imprint_strength': value,
            'is_new_imprint': core_concept not in self.knowledge_graph or 
                             not self.knowledge_graph[core_concept].get('imprinted', False)
        }

    def _default_learning(self, experience: Dict[str, Any], 
                        feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обработка опыта по умолчанию (ассоциативное)
        """
        return self._associative_learning(experience, feedback)

    def _update_skills_and_knowledge(self, experience: Dict[str, Any], 
                                   learning_outcome: Dict[str, Any]):
        """
        Обновление навыков и знаний на основе результата обучения
        """
        # Обновление прогрессии навыков
        skill_area = experience.get('skill_area', 'general')
        performance_improvement = learning_outcome.get('strength_change', 0.0) or \
                                 learning_outcome.get('q_value_change', 0.0) or \
                                 learning_outcome.get('insight_level', 0.0) * 0.1
        
        if skill_area not in self.skill_progressions:
            self.skill_progressions[skill_area] = {
                'current_level': 0.5,
                'improvement_history': []
            }
        
        current_level = self.skill_progressions[skill_area]['current_level']
        new_level = max(0.0, min(1.0, current_level + performance_improvement * 0.1))
        
        self.skill_progressions[skill_area]['current_level'] = new_level
        self.skill_progressions[skill_area]['improvement_history'].append({
            'timestamp': time.time(),
            'improvement': performance_improvement,
            'new_level': new_level
        })
        
        # Ограничение истории улучшений
        if len(self.skill_progressions[skill_area]['improvement_history']) > 50:
            self.skill_progressions[skill_area]['improvement_history'] = \
                self.skill_progressions[skill_area]['improvement_history'][-50:]

    def _update_motivation(self, feedback: Dict[str, Any]):
        """
        Обновление мотивационной системы
        """
        reward = feedback.get('reward', 0.0)
        novelty = feedback.get('novelty', 0.0)
        social_feedback = feedback.get('social_validation', 0.0)
        
        # Обновление различных мотивационных систем
        self.motivation_system['curiosity_drive'] = max(0.1, min(1.0, 
            self.motivation_system['curiosity_drive'] + novelty * 0.1))
        
        self.motivation_system['achievement_drive'] = max(0.1, min(1.0, 
            self.motivation_system['achievement_drive'] + max(0, reward) * 0.05))
        
        self.motivation_system['social_drive'] = max(0.1, min(1.0, 
            self.motivation_system['social_drive'] + social_feedback * 0.1))

    def update_from_experience(self):
        """
        Основной метод обновления системы на основе накопленного опыта
        """
        if not self.learning_episodes:
            return
        
        # Анализ последних эпизодов для оптимизации гиперпараметров
        recent_episodes = self.learning_episodes[-20:]  # последние 20 эпизодов
        
        # Вычисление эффективности обучения
        success_count = sum(1 for ep in recent_episodes 
                          if ep['feedback'].get('outcome') == 'positive')
        success_rate = success_count / len(recent_episodes) if recent_episodes else 0.0
        
        # Обновление гиперпараметров на основе эффективности
        if success_rate < 0.5:
            # Если эффективность низкая, увеличиваем скорость обучения и исследование
            self.hyperparameters['learning_rate'] = min(0.5, 
                self.hyperparameters['learning_rate'] * 1.1)
            self.hyperparameters['exploration_rate'] = min(0.8, 
                self.hyperparameters['exploration_rate'] * 1.05)
        else:
            # Если эффективность высокая, можно немного уменьшить скорость
            self.hyperparameters['learning_rate'] = max(0.05, 
                self.hyperparameters['learning_rate'] * 0.99)
        
        # Обновление оценок эффективности
        self.performance_metrics['accuracy_improvement'] = success_rate
        self.performance_metrics['adaptation_rate'] = self._calculate_adaptation_rate()
        self.performance_metrics['generalization_ability'] = self._calculate_generalization_ability()

    def _calculate_adaptation_rate(self) -> float:
        """
        Расчет скорости адаптации
        """
        if len(self.learning_episodes) < 2:
            return 0.5
        
        # Оценка, как быстро система адаптируется к изменениям
        recent_changes = 0
        for i in range(1, min(10, len(self.learning_episodes))):
            # Сравниваем результаты обучения
            prev_outcome = self.learning_episodes[-i-1]['learning_outcome']
            curr_outcome = self.learning_episodes[-i]['learning_outcome']
            
            if abs(prev_outcome.get('strength_change', 0) - 
                   curr_outcome.get('strength_change', 0)) > 0.1:
                recent_changes += 1
        
        return min(1.0, recent_changes / 5)  # Нормализация

    def _calculate_generalization_ability(self) -> float:
        """
        Расчет способности к обобщению
        """
        # Простая эвристика: если система часто применяет знания в новых контекстах
        if len(self.knowledge_graph) == 0:
            return 0.5
        
        # Подсчет отношений между знаниями (связность графа знаний)
        total_connections = 0
        for key, value in self.knowledge_graph.items():
            if isinstance(value, dict) and 'q_values' in value:
                total_connections += len(value['q_values'])
            elif isinstance(value, dict) and 'observed_behaviors' in value:
                total_connections += len(value['observed_behaviors'])
        
        # Нормализация: чем больше связей на знание, тем выше обобщение
        avg_connections = total_connections / len(self.knowledge_graph) if self.knowledge_graph else 0
        return min(1.0, avg_connections / 5)  # Условная нормализация

    def get_learning_progress(self) -> Dict[str, Any]:
        """
        Получение прогресса в обучении
        """
        return {
            'learning_components': self.learning_components.copy(),
            'skill_progressions': self.skill_progressions.copy(),
            'knowledge_graph_size': len(self.knowledge_graph),
            'total_learning_episodes': len(self.learning_episodes),
            'performance_metrics': self.performance_metrics.copy(),
            'motivation_levels': self.motivation_system.copy(),
            'learning_efficiency': self._calculate_learning_efficiency()
        }

    def _calculate_learning_efficiency(self) -> float:
        """
        Расчет общей эффективности обучения
        """
        if not self.learning_episodes:
            return 0.5
        
        # Эффективность как комбинация различных факторов
        recent_episodes = self.learning_episodes[-50:] if len(self.learning_episodes) >= 50 else self.learning_episodes
        
        positive_outcomes = sum(1 for ep in recent_episodes 
                              if ep['feedback'].get('outcome') == 'positive')
        success_rate = positive_outcomes / len(recent_episodes) if recent_episodes else 0.5
        
        # Учет разнообразия типов обучения
        experience_types = [ep['experience_type'] for ep in recent_episodes]
        type_diversity = len(set(experience_types)) / len(experience_types) if experience_types else 0.5
        
        # Комбинирование факторов
        efficiency = (success_rate * 0.6 + type_diversity * 0.4)
        
        return efficiency

    def adapt_learning_strategy(self, task_complexity: float, 
                              feedback_quality: float) -> Dict[str, Any]:
        """
        Адаптация стратегии обучения в зависимости от сложности задачи и качества обратной связи
        """
        # Регулировка параметров в зависимости от сложности и обратной связи
        if task_complexity > 0.7:
            # Для сложных задач увеличиваем наблюдательное и озаренческое обучение
            self.learning_components['observational_learning'] = min(1.0, 
                self.learning_components['observational_learning'] + 0.1)
            self.learning_components['insight_learning'] = min(1.0, 
                self.learning_components['insight_learning'] + 0.05)
            
            # Увеличиваем параметры исследования
            self.hyperparameters['exploration_rate'] = min(0.9, 
                self.hyperparameters['exploration_rate'] + 0.05)
        else:
            # Для простых задач усиливаем ассоциативное и подкрепляющее обучение
            self.learning_components['associative_learning'] = min(1.0, 
                self.learning_components['associative_learning'] + 0.05)
            self.learning_components['reinforcement_learning'] = min(1.0, 
                self.learning_components['reinforcement_learning'] + 0.1)
        
        if feedback_quality > 0.8:
            # При высоком качестве обратной связи увеличиваем скорость обучения
            self.hyperparameters['learning_rate'] = min(0.3, 
                self.hyperparameters['learning_rate'] * 1.1)
        else:
            # При низком качестве уменьшаем скорость обучения
            self.hyperparameters['learning_rate'] = max(0.05, 
                self.hyperparameters['learning_rate'] * 0.95)
        
        return {
            'updated_components': self.learning_components.copy(),
            'updated_hyperparameters': self.hyperparameters.copy(),
            'strategy_adjustment': f"Complexity-based adaptation for complexity {task_complexity}"
        }

    def transfer_learning(self, source_domain: str, target_domain: str) -> Dict[str, Any]:
        """
        Перенос обучения из одного домена в другой
        """
        # Извлечение знаний из исходного домена
        source_knowledge = {}
        for key, value in self.knowledge_graph.items():
            if source_domain in key or (isinstance(value, dict) and source_domain in str(value)):
                source_knowledge[key] = value
        
        # Применение знаний к целевому домену с учетом схожести
        transferred_knowledge = {}
        for key, value in source_knowledge.items():
            new_key = key.replace(source_domain, target_domain)
            if new_key != key:  # Только если произошла замена
                transferred_knowledge[new_key] = value
                # Учет эффективности переноса
                transfer_factor = self.transfer_efficiency
                if isinstance(value, dict) and 'strength' in value:
                    value['strength'] *= transfer_factor
        
        # Интеграция перенесенных знаний
        self.knowledge_graph.update(transferred_knowledge)
        
        return {
            'source_domain': source_domain,
            'target_domain': target_domain,
            'transferred_items': len(transferred_knowledge),
            'transfer_efficiency': self.transfer_efficiency
        }