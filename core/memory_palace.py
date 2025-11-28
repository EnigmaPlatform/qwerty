"""
MemoryPalace: Система памяти
"""
from typing import Dict, Any, List
import time
import pickle
import os


class MemoryPalace:
    def __init__(self, storage_path: str = "models/memory_db/"):
        """
        Инициализация системы памяти
        """
        self.storage_path = storage_path
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)
        
        # Типы памяти
        self.sensory_memory = []  # Кратковременная сенсорная память
        self.short_term_memory = []  # Кратковременная память
        self.long_term_memory = {
            'episodic': [],  # Эпизодическая память (события)
            'semantic': [],  # Семантическая память (знания)
            'procedural': []  # Процедурная память (навыки)
        }
        
        # Параметры памяти
        self.sensory_duration = 0.5  # 0.5 секунд
        self.short_term_capacity = 7  # +- 2 элемента
        self.short_term_duration = 30  # 30 секунд
        
        # Временные метки для управления устареванием
        self.memory_timestamps = {}
        
        # Загрузка сохраненного состояния, если существует
        self.load_memory_state()

    def encode(self, information: Any, memory_type: str = 'semantic', emotional_tag: float = 0.0) -> str:
        """
        Кодирование информации в память
        """
        memory_id = f"mem_{int(time.time() * 1000)}_{hash(str(information)) % 10000}"
        
        memory_entry = {
            'id': memory_id,
            'content': information,
            'type': memory_type,
            'emotional_tag': emotional_tag,
            'timestamp': time.time(),
            'access_count': 0,
            'strength': 0.5  # Начальная сила воспоминания
        }
        
        # Добавление в соответствующий тип памяти
        if memory_type == 'sensory':
            self.sensory_memory.append(memory_entry)
            self._manage_sensory_memory()
        elif memory_type == 'short_term':
            self.short_term_memory.append(memory_entry)
            self._manage_short_term_memory()
        elif memory_type == 'episodic':
            self.long_term_memory['episodic'].append(memory_entry)
        elif memory_type == 'semantic':
            self.long_term_memory['semantic'].append(memory_entry)
        elif memory_type == 'procedural':
            self.long_term_memory['procedural'].append(memory_entry)
        else:
            self.long_term_memory['semantic'].append(memory_entry)  # По умолчанию
        
        # Учет эмоциональной окраски для силы воспоминания
        if abs(emotional_tag) > 0.5:
            memory_entry['strength'] = min(1.0, memory_entry['strength'] + abs(emotional_tag) * 0.3)
        
        self.memory_timestamps[memory_id] = memory_entry['timestamp']
        
        return memory_id

    def _manage_sensory_memory(self):
        """
        Управление сенсорной памятью (очистка устаревшей)
        """
        current_time = time.time()
        self.sensory_memory = [
            mem for mem in self.sensory_memory 
            if current_time - mem['timestamp'] <= self.sensory_duration
        ]

    def _manage_short_term_memory(self):
        """
        Управление кратковременной памятью (ограничение по объему и времени)
        """
        current_time = time.time()
        
        # Ограничение по объему
        if len(self.short_term_memory) > self.short_term_capacity:
            # Удаление наименее важных элементов (с наименьшей силой и эмоциональной окраской)
            self.short_term_memory.sort(key=lambda x: x['strength'] + abs(x['emotional_tag']), reverse=True)
            self.short_term_memory = self.short_term_memory[:self.short_term_capacity]
        
        # Ограничение по времени
        self.short_term_memory = [
            mem for mem in self.short_term_memory 
            if current_time - mem['timestamp'] <= self.short_term_duration
        ]

    def consolidate_to_long_term(self, memory_ids: List[str] = None, consolidation_factor: float = 1.0):
        """
        Консолидация памяти из кратковременной в долговременную
        """
        if memory_ids is None:
            # Консолидировать все элементы из кратковременной памяти
            memories_to_move = self.short_term_memory[:]
        else:
            # Найти указанные элементы
            memories_to_move = [mem for mem in self.short_term_memory if mem['id'] in memory_ids]
        
        for memory in memories_to_move:
            # Повышение силы воспоминания при консолидации
            memory['strength'] = min(1.0, memory['strength'] + 0.2 * consolidation_factor)
            memory['type'] = 'semantic'  # По умолчанию в семантическую
            
            # Перемещение в долговременную память
            self.long_term_memory['semantic'].append(memory)
            self.short_term_memory.remove(memory)

    def retrieve(self, query: Any = None, memory_type: str = 'all', max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Извлечение информации из памяти
        """
        results = []
        
        # Выбор списка памяти для поиска
        if memory_type == 'sensory':
            memory_list = self.sensory_memory
        elif memory_type == 'short_term':
            memory_list = self.short_term_memory
        elif memory_type == 'episodic':
            memory_list = self.long_term_memory['episodic']
        elif memory_type == 'semantic':
            memory_list = self.long_term_memory['semantic']
        elif memory_type == 'procedural':
            memory_list = self.long_term_memory['procedural']
        elif memory_type == 'all':
            memory_list = (self.sensory_memory + self.short_term_memory + 
                          self.long_term_memory['episodic'] + 
                          self.long_term_memory['semantic'] + 
                          self.long_term_memory['procedural'])
        else:
            memory_list = self.long_term_memory['semantic']
        
        # Поиск по запросу (простое совпадение)
        if query is not None:
            query_str = str(query).lower()
            for memory in memory_list:
                content_str = str(memory['content']).lower()
                if query_str in content_str:
                    memory['access_count'] += 1
                    # Увеличение силы воспоминания при доступе
                    memory['strength'] = min(1.0, memory['strength'] + 0.05)
                    results.append(memory)
        else:
            # Просто возвращаем последние элементы
            results = memory_list[-max_results:]
            for memory in results:
                memory['access_count'] += 1
        
        # Сортировка по силе и актуальности
        results.sort(key=lambda x: (x['strength'], x['emotional_tag'], x['timestamp']), reverse=True)
        
        return results[:max_results]

    def forget(self, memory_id: str = None, memory_type: str = 'all', decay_factor: float = 0.1):
        """
        Забывание (ослабление или удаление воспоминаний)
        """
        if memory_id:
            # Удаление конкретного воспоминания
            for memory_list in [self.sensory_memory, self.short_term_memory]:
                for i, mem in enumerate(memory_list):
                    if mem['id'] == memory_id:
                        memory_list.pop(i)
                        return True
            
            for key, memory_list in self.long_term_memory.items():
                if memory_type == 'all' or key == memory_type:
                    for i, mem in enumerate(memory_list):
                        if mem['id'] == memory_id:
                            memory_list.pop(i)
                            return True
        else:
            # Применение фактора забывания ко всем воспоминаниям
            all_lists = [self.sensory_memory, self.short_term_memory]
            for key, memory_list in self.long_term_memory.items():
                if memory_type == 'all' or key == memory_type:
                    all_lists.append(memory_list)
            
            for memory_list in all_lists:
                for memory in memory_list:
                    # Ослабление силы воспоминания
                    memory['strength'] = max(0.0, memory['strength'] - decay_factor)
                    # Удаление очень слабых воспоминаний
                    if memory['strength'] < 0.1:
                        memory_list.remove(memory)
        
        return False

    def get_memory_statistics(self) -> Dict[str, Any]:
        """
        Получение статистики по памяти
        """
        return {
            'sensory_count': len(self.sensory_memory),
            'short_term_count': len(self.short_term_memory),
            'long_term_counts': {k: len(v) for k, v in self.long_term_memory.items()},
            'total_memories': (
                len(self.sensory_memory) + 
                len(self.short_term_memory) + 
                sum(len(v) for v in self.long_term_memory.values())
            ),
            'storage_path': self.storage_path
        }

    def save_memory_state(self):
        """
        Сохранение состояния памяти на диск
        """
        state = {
            'sensory_memory': self.sensory_memory,
            'short_term_memory': self.short_term_memory,
            'long_term_memory': self.long_term_memory,
            'memory_timestamps': self.memory_timestamps
        }
        
        with open(os.path.join(self.storage_path, 'memory_state.pkl'), 'wb') as f:
            pickle.dump(state, f)

    def load_memory_state(self):
        """
        Загрузка состояния памяти с диска
        """
        state_path = os.path.join(self.storage_path, 'memory_state.pkl')
        if os.path.exists(state_path):
            with open(state_path, 'rb') as f:
                state = pickle.load(f)
            
            self.sensory_memory = state.get('sensory_memory', [])
            self.short_term_memory = state.get('short_term_memory', [])
            self.long_term_memory = state.get('long_term_memory', {
                'episodic': [], 
                'semantic': [], 
                'procedural': []
            })
            self.memory_timestamps = state.get('memory_timestamps', {})

    def associate_memories(self, memory_id1: str, memory_id2: str, strength: float = 0.5):
        """
        Создание ассоциаций между воспоминаниями
        """
        # В реальной реализации здесь будет граф ассоциаций
        # Пока просто увеличиваем силу воспоминаний
        for memory_list in [self.sensory_memory, self.short_term_memory]:
            for memory in memory_list:
                if memory['id'] in [memory_id1, memory_id2]:
                    memory['strength'] = min(1.0, memory['strength'] + strength * 0.1)
        
        for memory_list in self.long_term_memory.values():
            for memory in memory_list:
                if memory['id'] in [memory_id1, memory_id2]:
                    memory['strength'] = min(1.0, memory['strength'] + strength * 0.1)