"""
BeliefDynamics: Динамика убеждений
"""
from typing import Dict, Any, List
import numpy as np


class BeliefDynamics:
    def __init__(self):
        """
        Инициализация системы динамики убеждений
        """
        # База убеждений
        self.beliefs = {
            'world_model': {},      # Убеждения о мире
            'self_model': {},       # Убеждения о себе
            'social_model': {},     # Убеждения о социуме
            'moral_principles': {}  # Моральные принципы
        }
        
        # Степени уверенности в убеждениях
        self.confidence_levels = {}
        
        # Связи между убеждениями
        self.belief_connections = {}
        
        # История изменений убеждений
        self.belief_history = []
        
        # Параметры динамики
        self.stability_factor = 0.9    # Фактор стабильности (сопротивление изменениям)
        self.update_threshold = 0.3    # Порог для обновления убеждений
        self.coherence_weight = 0.8    # Вес когерентности при обновлениях

    def update_belief(self, domain: str, belief_key: str, new_evidence: Dict[str, Any], 
                     evidence_strength: float = 1.0) -> Dict[str, Any]:
        """
        Обновление убеждения на основе новых доказательств
        """
        # Получение текущего убеждения
        current_belief = self.beliefs[domain].get(belief_key, None)
        
        # Расчет новой веры на основе доказательств
        updated_belief = self._calculate_updated_belief(
            current_belief, new_evidence, evidence_strength
        )
        
        # Проверка когерентности с другими убеждениями
        if self._check_coherence(domain, belief_key, updated_belief):
            # Обновление убеждения
            self.beliefs[domain][belief_key] = updated_belief
            
            # Обновление уровня уверенности
            new_confidence = self._calculate_confidence(
                current_belief, new_evidence, evidence_strength
            )
            self.confidence_levels[f"{domain}.{belief_key}"] = new_confidence
            
            # Запись в историю
            self._log_belief_update(domain, belief_key, current_belief, 
                                  updated_belief, new_evidence, evidence_strength)
            
            # Обновление связанных убеждений
            self._update_related_beliefs(domain, belief_key, updated_belief)
            
            return {
                'status': 'updated',
                'old_value': current_belief,
                'new_value': updated_belief,
                'confidence': new_confidence
            }
        else:
            return {
                'status': 'rejected_due_to_incoherence',
                'reason': 'New belief conflicts with existing belief system',
                'proposed_value': updated_belief
            }

    def _calculate_updated_belief(self, current_belief: Any, new_evidence: Dict[str, Any], 
                                 evidence_strength: float) -> Any:
        """
        Расчет обновленного убеждения на основе доказательств
        """
        if current_belief is None:
            # Если убеждения не существовало, создаем его на основе доказательств
            return new_evidence.get('value', new_evidence)
        
        # Простая модель обновления: взвешенное среднее
        if isinstance(current_belief, (int, float)) and 'value' in new_evidence:
            # Обновление числового убеждения
            current_value = current_belief
            new_value = new_evidence['value']
            
            # Взвешенное обновление с учетом силы доказательства
            updated_value = (current_value * (1 - evidence_strength * 0.5) + 
                           new_value * evidence_strength * 0.5)
            return updated_value
        else:
            # Для сложных убеждений возвращаем новое доказательство
            return new_evidence

    def _check_coherence(self, domain: str, belief_key: str, proposed_belief: Any) -> bool:
        """
        Проверка когерентности нового убеждения с существующей системой
        """
        # Проверка явных противоречий
        for other_domain, other_beliefs in self.beliefs.items():
            for other_key, other_belief in other_beliefs.items():
                if other_domain == domain and other_key == belief_key:
                    continue  # Это то же самое убеждение
                
                # Проверка на противоречие (упрощенная модель)
                contradiction = self._check_contradiction(
                    proposed_belief, other_belief, f"{domain}.{belief_key}", f"{other_domain}.{other_key}"
                )
                if contradiction > 0.7:  # Высокий уровень противоречия
                    return False
        
        return True

    def _check_contradiction(self, belief1: Any, belief2: Any, 
                           belief1_id: str, belief2_id: str) -> float:
        """
        Проверка противоречия между двумя убеждениями
        """
        # Упрощенная проверка противоречий
        if isinstance(belief1, (int, float)) and isinstance(belief2, (int, float)):
            # Для числовых убеждений: противоречие при сильной полярности
            if belief1 * belief2 < 0:  # Противоположные знаки
                return abs(belief1) * abs(belief2)
        
        # Проверка по идентификаторам убеждений (если известны противоречивые пары)
        contradictory_pairs = [
            ('moral_principles.honesty', 'moral_principles.deception'),
            ('world_model.deterministic', 'world_model.random')
        ]
        
        if (belief1_id, belief2_id) in contradictory_pairs or (belief2_id, belief1_id) in contradictory_pairs:
            return 1.0
        
        return 0.0

    def _calculate_confidence(self, current_belief: Any, new_evidence: Dict[str, Any], 
                            evidence_strength: float) -> float:
        """
        Расчет уровня уверенности в убеждении
        """
        if current_belief is None:
            # Новое убеждение получает уверенность, пропорциональную силе доказательства
            return min(1.0, evidence_strength)
        
        # Обновление уверенности с учетом согласованности доказательств
        current_confidence = self.confidence_levels.get(
            f"{self._get_domain_for_belief(current_belief)}.{self._get_key_for_belief(current_belief)}", 
            0.5
        )
        
        # Уверенность увеличивается при подтверждающих доказательствах
        if self._evidence_supports_belief(current_belief, new_evidence):
            new_confidence = current_confidence * 0.8 + evidence_strength * 0.2
        else:
            # Уверенность уменьшается при противоречащих доказательствах
            new_confidence = current_confidence * (1 - evidence_strength * 0.3)
        
        return max(0.0, min(1.0, new_confidence))

    def _evidence_supports_belief(self, belief: Any, evidence: Dict[str, Any]) -> bool:
        """
        Проверка, поддерживает ли доказательство убеждение
        """
        # Упрощенная проверка соответствия
        if isinstance(belief, (int, float)) and 'value' in evidence:
            # Для числовых убеждений проверяем знак
            return np.sign(belief) == np.sign(evidence['value'])
        return True

    def _get_domain_for_belief(self, belief: Any) -> str:
        """
        Получение домена для убеждения (заглушка)
        """
        return 'world_model'  # По умолчанию

    def _get_key_for_belief(self, belief: Any) -> str:
        """
        Получение ключа для убеждения (заглушка)
        """
        return 'general'  # По умолчанию

    def _log_belief_update(self, domain: str, belief_key: str, old_value: Any, 
                          new_value: Any, evidence: Dict[str, Any], strength: float):
        """
        Логирование обновления убеждения
        """
        log_entry = {
            'timestamp': self._get_current_time(),
            'domain': domain,
            'belief_key': belief_key,
            'old_value': old_value,
            'new_value': new_value,
            'evidence': evidence,
            'evidence_strength': strength,
            'confidence': self.confidence_levels.get(f"{domain}.{belief_key}", 0.5)
        }
        self.belief_history.append(log_entry)

    def _update_related_beliefs(self, domain: str, belief_key: str, updated_belief: Any):
        """
        Обновление связанных убеждений
        """
        # В реальности здесь происходило бы распространение изменений по сети убеждений
        # Пока реализуем простую версию
        pass

    def get_belief(self, domain: str, belief_key: str) -> Dict[str, Any]:
        """
        Получение убеждения с информацией о нем
        """
        belief_value = self.beliefs[domain].get(belief_key)
        confidence = self.confidence_levels.get(f"{domain}.{belief_key}", 0.0)
        
        return {
            'value': belief_value,
            'confidence': confidence,
            'domain': domain,
            'key': belief_key,
            'coherence': self._assess_belief_coherence(domain, belief_key)
        }

    def _assess_belief_coherence(self, domain: str, belief_key: str) -> float:
        """
        Оценка когерентности убеждения с остальной системой
        """
        # Простая оценка: среднее сопротивление противоречиям
        total_coherence = 0.0
        comparison_count = 0
        
        current_belief = self.beliefs[domain][belief_key]
        current_id = f"{domain}.{belief_key}"
        
        for other_domain, other_beliefs in self.beliefs.items():
            for other_key, other_belief in other_beliefs.items():
                if other_domain == domain and other_key == belief_key:
                    continue
                
                contradiction = self._check_contradiction(
                    current_belief, other_belief, current_id, f"{other_domain}.{other_key}"
                )
                total_coherence += (1 - contradiction)
                comparison_count += 1
        
        if comparison_count == 0:
            return 1.0  # Когерентность не может быть оценена
        
        return total_coherence / comparison_count

    def get_belief_system_state(self) -> Dict[str, Any]:
        """
        Получение состояния системы убеждений
        """
        return {
            'beliefs': self.beliefs.copy(),
            'confidence_levels': self.confidence_levels.copy(),
            'belief_count': self._count_beliefs(),
            'system_coherence': self._calculate_system_coherence(),
            'change_frequency': self._calculate_change_frequency(),
            'belief_domains': list(self.beliefs.keys())
        }

    def _count_beliefs(self) -> int:
        """
        Подсчет общего количества убеждений
        """
        return sum(len(domain_beliefs) for domain_beliefs in self.beliefs.values())

    def _calculate_system_coherence(self) -> float:
        """
        Расчет общей когерентности системы убеждений
        """
        if self._count_beliefs() == 0:
            return 1.0
        
        total_coherence = 0.0
        belief_count = 0
        
        for domain, beliefs in self.beliefs.items():
            for key in beliefs:
                total_coherence += self._assess_belief_coherence(domain, key)
                belief_count += 1
        
        return total_coherence / belief_count if belief_count > 0 else 1.0

    def _calculate_change_frequency(self) -> float:
        """
        Расчет частоты изменений убеждений
        """
        if len(self.belief_history) < 2:
            return 0.0
        
        # Рассчитываем частоту за последний час (3600 секунд)
        import time
        current_time = time.time()
        recent_changes = [
            change for change in self.belief_history 
            if current_time - change['timestamp'] <= 3600
        ]
        
        return len(recent_changes) / 3600.0  # Изменений в секунду

    def challenge_belief(self, domain: str, belief_key: str, counter_evidence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Вызов убеждения в соответствии с контр-доказательствами
        """
        current_belief = self.beliefs[domain].get(belief_key)
        if current_belief is None:
            return {'status': 'no_belief_to_challenge', 'message': 'Belief does not exist'}
        
        # Оценка силы контр-доказательства
        counter_strength = counter_evidence.get('strength', 0.5)
        
        # Уменьшение уверенности в убеждении
        current_confidence = self.confidence_levels.get(f"{domain}.{belief_key}", 0.5)
        new_confidence = max(0.0, current_confidence - counter_strength * 0.3)
        self.confidence_levels[f"{domain}.{belief_key}"] = new_confidence
        
        # Если уверенность падает ниже порога, убеждение может быть пересмотрено
        if new_confidence < 0.2:
            return {
                'status': 'belief_questioned',
                'original_belief': current_belief,
                'confidence_reduction': current_confidence - new_confidence,
                'recommendation': 'Consider reevaluating this belief'
            }
        
        return {
            'status': 'belief_challenged',
            'confidence_reduction': current_confidence - new_confidence,
            'remaining_confidence': new_confidence
        }

    def integrate_new_knowledge(self, knowledge: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Интеграция нового знания в систему убеждений
        """
        integration_results = []
        
        for domain, domain_knowledge in knowledge.items():
            if domain in self.beliefs:
                for key, value in domain_knowledge.items():
                    result = self.update_belief(
                        domain, 
                        key, 
                        {'value': value, 'source': 'knowledge_integration'},
                        evidence_strength=0.6
                    )
                    integration_results.append(result)
        
        return integration_results

    def _get_current_time(self) -> float:
        """
        Получение текущего времени
        """
        import time
        return time.time()