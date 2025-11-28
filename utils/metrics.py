"""
MetricsCollector: Система метрик
"""
import time
from datetime import datetime
from typing import Dict, Any, List
import statistics


class MetricsCollector:
    def __init__(self, collection_interval: int = 60):
        self.collection_interval = collection_interval
        self.interactions = []
        self.module_metrics = {}
        self.start_time = time.time()
        
        # Ключевые показатели эффективности
        self.kpis = {
            'emotional_coherence_index': [],
            'cognitive_load_factor': [],
            'social_intelligence_quotient': [],
            'learning_progress_rate': [],
            'system_stability_score': []
        }
    
    def record_interaction(self, interaction_data: Dict[str, Any]):
        """Запись данных взаимодействия"""
        interaction_data['recorded_at'] = time.time()
        self.interactions.append(interaction_data)
        
        # Обновление KPI на основе взаимодействия
        self._update_kpis(interaction_data)
    
    def _update_kpis(self, interaction_data: Dict[str, Any]):
        """Обновление ключевых показателей эффективности"""
        # Emotional Coherence Index (ECI)
        emotional_state = interaction_data.get('emotional_state', {})
        eci = emotional_state.get('emotional_entropy', 0.5)  # Чем ниже энтропия, тем выше когерентность
        self.kpis['emotional_coherence_index'].append(1 - eci)  # Инвертируем, чтобы больше было лучше
        
        # Cognitive Load Factor (CLF)
        cognitive_load = interaction_data.get('cognitive_load', 0.5)
        self.kpis['cognitive_load_factor'].append(cognitive_load)
        
        # System Stability Score (SSS) - на основе времени обработки
        processing_time = interaction_data.get('processing_time', 1.0)
        # Чем ближе к оптимальному времени, тем выше стабильность
        optimal_time = 0.5
        stability_score = 1 / (1 + abs(processing_time - optimal_time))
        self.kpis['system_stability_score'].append(stability_score)
    
    def record_module_metric(self, module: str, metric_name: str, value: float):
        """Запись метрики модуля"""
        if module not in self.module_metrics:
            self.module_metrics[module] = {}
        
        if metric_name not in self.module_metrics[module]:
            self.module_metrics[module][metric_name] = []
        
        self.module_metrics[module][metric_name].append({
            'value': value,
            'timestamp': time.time()
        })
    
    def get_system_metrics(self, time_window: int = 3600) -> Dict[str, Any]:
        """Получение метрик системы за определенное время"""
        current_time = time.time()
        cutoff_time = current_time - time_window
        
        # Фильтрация взаимодействий за последнее время
        recent_interactions = [
            interaction for interaction in self.interactions
            if interaction['recorded_at'] > cutoff_time
        ]
        
        if not recent_interactions:
            return {'message': 'No recent interactions'}
        
        # Расчет основных метрик
        processing_times = [i['processing_time'] for i in recent_interactions]
        avg_processing_time = sum(processing_times) / len(processing_times)
        
        # Оценка эмоциональной стабильности
        emotional_stabilities = []
        for interaction in recent_interactions:
            emotional_state = interaction.get('emotional_state', {})
            coherence = emotional_state.get('emotional_entropy', 0.5)
            emotional_stabilities.append(1 - coherence)
        
        avg_emotional_stability = sum(emotional_stabilities) / len(emotional_stabilities) if emotional_stabilities else 0.5
        
        return {
            'time_window_seconds': time_window,
            'interaction_count': len(recent_interactions),
            'average_processing_time': avg_processing_time,
            'average_emotional_stability': avg_emotional_stability,
            'total_interactions': len(self.interactions),
            'system_uptime': current_time - self.start_time,
            'kpi_averages': {k: sum(v) / len(v) if v else 0 for k, v in self.kpis.items()},
            'kpi_trends': self._calculate_kpi_trends()
        }
    
    def _calculate_kpi_trends(self) -> Dict[str, str]:
        """Расчет трендов KPI"""
        trends = {}
        for kpi_name, values in self.kpis.items():
            if len(values) >= 2:
                recent_avg = sum(values[-5:]) / min(5, len(values))  # Среднее последних 5
                earlier_avg = sum(values[:5]) / min(5, len(values))  # Среднее первых 5
                
                if recent_avg > earlier_avg * 1.1:
                    trends[kpi_name] = 'improving'
                elif recent_avg < earlier_avg * 0.9:
                    trends[kpi_name] = 'declining'
                else:
                    trends[kpi_name] = 'stable'
            else:
                trends[kpi_name] = 'insufficient_data'
        
        return trends
    
    def detect_anomalies(self) -> List[Dict[str, Any]]:
        """Обнаружение аномалий в метриках"""
        anomalies = []
        
        # Проверка аномалий времени обработки
        if self.interactions:
            processing_times = [i['processing_time'] for i in self.interactions[-20:]]  # последние 20
            if processing_times:
                mean_time = statistics.mean(processing_times)
                stdev_time = statistics.stdev(processing_times) if len(processing_times) > 1 else 0
                
                for i, interaction in enumerate(self.interactions[-20:]):
                    if stdev_time > 0 and abs(interaction['processing_time'] - mean_time) > 2 * stdev_time:
                        anomalies.append({
                            'type': 'processing_time_anomaly',
                            'interaction_index': len(self.interactions) - 20 + i,
                            'value': interaction['processing_time'],
                            'mean': mean_time,
                            'threshold': 2 * stdev_time
                        })
        
        return anomalies
    
    def generate_health_report(self) -> Dict[str, Any]:
        """Генерация отчета о здоровье системы"""
        total_interactions = len(self.interactions)
        
        if total_interactions == 0:
            return {
                'status': 'no_data',
                'message': 'No interactions recorded yet'
            }
        
        # Агрегированные метрики
        processing_times = [i['processing_time'] for i in self.interactions]
        avg_processing_time = sum(processing_times) / len(processing_times)
        
        # Эмоциональные метрики
        emotional_entropies = []
        for interaction in self.interactions[-50:]:  # последние 50
            emotional_state = interaction.get('emotional_state', {})
            entropy = emotional_state.get('emotional_entropy', 0.5)
            emotional_entropies.append(entropy)
        
        avg_emotional_entropy = sum(emotional_entropies) / len(emotional_entropies) if emotional_entropies else 0.5
        
        # Вычисление общего индекса здоровья
        time_efficiency_score = max(0, min(1, 2 - avg_processing_time))  # Чем быстрее, тем лучше
        emotional_coherence_score = 1 - avg_emotional_entropy  # Чем ниже энтропия, тем лучше
        
        overall_health = (time_efficiency_score + emotional_coherence_score) / 2
        
        return {
            'status': 'operational',
            'overall_health_score': overall_health,
            'total_interactions': total_interactions,
            'average_processing_time': avg_processing_time,
            'average_emotional_coherence': emotional_coherence_score,
            'current_time': datetime.now().isoformat(),
            'system_uptime_hours': (time.time() - self.start_time) / 3600,
            'recent_anomalies_count': len(self.detect_anomalies()),
            'kpi_summary': {k: sum(v) / len(v) if v else 0 for k, v in self.kpis.items()}
        }