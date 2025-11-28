"""
CognitiveArchitecture: Когнитивная архитектура с двумя системами мышления
"""
import numpy as np
from typing import Dict, Any, List
import time


class CognitiveArchitecture:
    def __init__(self, capacity: int = 7):
        """
        Инициализация когнитивной архитектуры
        """
        self.working_memory_capacity = capacity
        self.working_memory = []
        self.long_term_memory = []
        
        # Параметры двухсистемной модели
        self.system1_threshold = 0.3  # Порог для активации System 1
        self.system2_threshold = 0.7  # Порог для активации System 2
        
        # Исполнительные функции
        self.executive_functions = {
            'updating': 0.7,      # Обновление информации в рабочей памяти
            'inhibition': 0.8,    # Торможение неуместных реакций
            'shifting': 0.6       # Переключение между задачами
        }
        
        # Метапознание
        self.metacognitive_monitoring = 0.8
        self.confidence_in_system1 = 0.6
        self.confidence_in_system2 = 0.8
        
        # Статистика использования систем
        self.system1_usage = 0
        self.system2_usage = 0
        
        # Временные параметры
        self.last_processing_time = 0.0

    def process_stimulus(self, stimulus: Dict[str, Any], system_preference: int = 0) -> Dict[str, Any]:
        """
        Обработка стимула с использованием одной из двух систем мышления
        system_preference: 0 - автоматический выбор, 1 - System 1, 2 - System 2
        """
        start_time = time.time()
        
        stimulus_complexity = stimulus.get('complexity', 0.5)
        emotional_salience = stimulus.get('emotional_salience', 0.5)
        familiarity = stimulus.get('familiarity', 0.3)
        
        # Определение, какую систему использовать
        if system_preference == 0:
            # Автоматический выбор системы
            system_to_use = self._select_system(stimulus_complexity, emotional_salience, familiarity)
        else:
            system_to_use = system_preference
        
        if system_to_use == 1:
            self.system1_usage += 1
            result = self._system1_processing(stimulus)
        else:
            self.system2_usage += 1
            result = self._system2_processing(stimulus)
        
        processing_time = time.time() - start_time
        self.last_processing_time = processing_time
        
        # Обновление рабочей памяти
        self._update_working_memory(result['output'])
        
        return {
            'result': result,
            'system_used': system_to_use,
            'processing_time': processing_time,
            'working_memory_load': len(self.working_memory) / self.working_memory_capacity
        }

    def _select_system(self, complexity: float, emotional_salience: float, familiarity: float) -> int:
        """
        Выбор системы на основе характеристик стимула
        """
        # System 1 используется для знакомых, эмоционально заряженных, но не очень сложных стимулов
        system1_score = (familiarity * 0.4) + (emotional_salience * 0.4) + ((1 - complexity) * 0.2)
        
        # System 2 используется для сложных, новых, требующих анализа стимулов
        system2_score = (complexity * 0.5) + ((1 - familiarity) * 0.3) + (emotional_salience * 0.2)
        
        if system1_score > self.system1_threshold and system1_score > system2_score:
            return 1
        elif system2_score > self.system2_threshold and system2_score > system1_score:
            return 2
        else:
            # По умолчанию использовать System 1 для быстрого реагирования
            return 1

    def _system1_processing(self, stimulus: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обработка с помощью System 1 (быстрая, интуитивная)
        """
        input_text = stimulus.get('input', '')
        
        # Простые эвристики и шаблоны
        response = self._apply_heuristics(input_text)
        
        # Быстрые ассоциации
        associations = self._fast_associations(input_text)
        
        return {
            'output': response,
            'associations': associations,
            'confidence': self.confidence_in_system1,
            'processing_type': 'intuitive'
        }

    def _system2_processing(self, stimulus: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обработка с помощью System 2 (медленная, аналитическая)
        """
        input_text = stimulus.get('input', '')
        goal = stimulus.get('goal', 'respond')
        
        # Аналитическая обработка
        analysis = self._analytical_processing(input_text, goal)
        
        # Логические рассуждения
        reasoning = self._logical_reasoning(analysis)
        
        # Проверка согласованности
        if self._check_consistency(reasoning):
            response = reasoning.get('conclusion', input_text)
        else:
            # Если несогласованность, возвращаемся к System 1 или переспрашиваем
            response = self._apply_heuristics(input_text)
        
        return {
            'output': response,
            'analysis': analysis,
            'reasoning': reasoning,
            'confidence': self.confidence_in_system2,
            'processing_type': 'analytical'
        }

    def _apply_heuristics(self, text: str) -> str:
        """
        Применение эвристик к тексту
        """
        # Простые эвристики: если вопрос, то отвечаем вопросом или да/нет
        if text.endswith('?'):
            if 'как' in text.lower() or 'каким образом' in text.lower():
                return "Это интересный вопрос, требующий размышления."
            elif 'ли' in text.lower() or 'да' in text.lower() or 'нет' in text.lower():
                return "Возможно, ответ лежит в области ваших знаний."
            else:
                return "Это вызывает интерес к размышлениям."
        else:
            return f"Я размышляю о: {text[:50]}..."

    def _fast_associations(self, text: str) -> List[str]:
        """
        Быстрые ассоциации с текстом
        """
        # Простые ассоциации
        associations = []
        if 'радость' in text.lower() or 'счастье' in text.lower():
            associations.extend(['позитив', 'удовольствие', 'удовлетворение'])
        elif 'печаль' in text.lower() or 'грусть' in text.lower():
            associations.extend(['негатив', 'потеря', 'тоска'])
        elif 'страх' in text.lower():
            associations.extend(['опасность', 'угроза', 'осторожность'])
        elif 'любовь' in text.lower():
            associations.extend(['привязанность', 'забота', 'сострадание'])
        
        return associations[:3]  # Ограничиваем количество ассоциаций

    def _analytical_processing(self, text: str, goal: str) -> Dict[str, Any]:
        """
        Аналитическая обработка текста
        """
        # Разбор структуры текста
        words = text.split()
        length = len(words)
        complexity_score = min(1.0, length / 50.0)  # Простая оценка сложности
        
        # Определение типа текста
        if text.endswith('?'):
            text_type = 'question'
        elif any(word in text.lower() for word in ['предположим', 'если', 'допустим']):
            text_type = 'hypothetical'
        elif any(word in text.lower() for word in ['потому что', 'следовательно', 'поэтому']):
            text_type = 'argument'
        else:
            text_type = 'statement'
        
        return {
            'length': length,
            'complexity': complexity_score,
            'type': text_type,
            'key_elements': words[:5] if len(words) > 5 else words
        }

    def _logical_reasoning(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Логические рассуждения на основе анализа
        """
        # Простые логические правила
        if analysis['type'] == 'question':
            conclusion = f"Вопрос касается {analysis['key_elements'][0] if analysis['key_elements'] else 'неизвестной темы'}"
        elif analysis['type'] == 'argument':
            conclusion = f"Аргумент имеет структуру с основными элементами: {', '.join(analysis['key_elements'])}"
        else:
            conclusion = f"Высказывание содержит информацию о: {', '.join(analysis['key_elements'])}"
        
        return {
            'premises': analysis['key_elements'],
            'conclusion': conclusion,
            'validity': 0.8  # Простая оценка достоверности
        }

    def _check_consistency(self, reasoning: Dict[str, Any]) -> bool:
        """
        Проверка логической согласованности
        """
        # Простая проверка: если достоверность выше порога, считаем согласованным
        return reasoning.get('validity', 0.0) > 0.5

    def get_working_memory_state(self) -> List[Any]:
        """
        Получение состояния рабочей памяти
        """
        return self.working_memory.copy()

    def _update_working_memory(self, new_item: Any):
        """
        Обновление рабочей памяти
        """
        self.working_memory.append(new_item)
        
        # Ограничение размера рабочей памяти
        if len(self.working_memory) > self.working_memory_capacity:
            # Простое правило: удалить самый старый элемент
            self.working_memory.pop(0)

    def engage_system2(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """
        Принудительное вовлечение System 2 для решения сложной задачи
        """
        return self.process_stimulus(problem, system_preference=2)

    def metacognitive_monitor(self) -> Dict[str, Any]:
        """
        Метапознавательный мониторинг
        """
        total_processes = self.system1_usage + self.system2_usage
        system1_ratio = self.system1_usage / total_processes if total_processes > 0 else 0
        system2_ratio = self.system2_usage / total_processes if total_processes > 0 else 0
        
        return {
            'system1_ratio': system1_ratio,
            'system2_ratio': system2_ratio,
            'total_processes': total_processes,
            'executive_function_scores': self.executive_functions,
            'working_memory_load': len(self.working_memory) / self.working_memory_capacity,
            'metacognitive_awareness': self.metacognitive_monitoring,
            'last_processing_time': self.last_processing_time
        }