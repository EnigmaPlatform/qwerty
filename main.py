"""
РЕАЛИЗАЦИЯ main.py:

ТРЕБОВАНИЯ:
1. Централизованный запуск всей системы
2. Загрузка всех моделей из корневой папки проекта
3. Комплексная инициализация всех модулей
4. Единая система логгирования и мониторинга
5. UI интерфейс с хакерским стилем (темное окно с неоново зелеными буквами)

ДЕТАЛИ РЕАЛИЗАЦИИ:
- Последовательная инициализация модулей в правильном порядке
- Глобальный обработчик ошибок и исключений
- Система health-check для всех модулей
- Интерфейс взаимодействия с пользователем
- Периодическое сохранение состояния системы
- Автоматическое определение путей для всех файлов
- UI с функционалом: взаимодействие с ИИ, обучение, метрики

КОДОВАЯ СТРУКТУРА:
"""
import os
import sys
import logging
import time
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
from core.neural_language_core import NeuralLanguageCore
from core.emotional_quantum_field import EmotionalQuantumField
from core.neurotransmitter_network import NeurotransmitterNetwork
from core.cognitive_architecture import CognitiveArchitecture
from core.identity_matrix import IdentityMatrix
from core.memory_palace import MemoryPalace
from core.empathy_resonator import EmpathyResonator
from core.reflection_engine import ReflectionEngine
from core.belief_dynamics import BeliefDynamics
from core.social_intelligence import SocialIntelligence
from core.physiological_simulator import PhysiologicalSimulator
from core.behavioral_generator import BehavioralGenerator
from core.consciousness_stream import ConsciousnessStream
from core.learning_evolver import LearningEvolver
from core.world_model import WorldModel
from utils.logger import SystemLogger
from utils.metrics import MetricsCollector
from utils.config_loader import ConfigLoader
from core.enhanced_ui import EnhancedEmotionalAIUI  # Updated to use enhanced UI



class EmotionalAISystem:
    def __init__(self, base_path: str):
        # Автоматическое определение всех путей
        execution_base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Определение пути к логам
        logs_path = self._find_logs_path(execution_base_path)
        
        self.base_path = base_path
        self.logger = SystemLogger(logs_path)
        self.metrics = MetricsCollector()
        
        # Определение остальных путей
        configs_path = self._find_configs_path(execution_base_path)
        self.config = ConfigLoader.load_all_configs(configs_path)
        
        # Инициализация модулей в правильном порядке
        self.init_modules(configs_path, execution_base_path)
        
    def init_modules(self, configs_path: str, execution_base_path: str):
        try:
            # Автоматическое определение путей для всех файлов
            # Определение пути к модели FRED
            fred_path = self._find_fred_path(execution_base_path)
            
            # Определение пути к базе данных памяти
            memory_path = self._find_memory_path(execution_base_path)
            
            # 1. Базовая инициализация
            self.neural_core = NeuralLanguageCore(fred_path)
            
            # 2. Эмоциональная система
            emotion_config_path = os.path.join(configs_path, 'emotion_config.json')
            self.emotional_field = EmotionalQuantumField(emotion_config_path)
            
            # 3. Нейротрансмиттерная сеть
            self.neurotransmitter_net = NeurotransmitterNetwork(
                self.config['neurotransmitter_initial']
            )
            
            # 4. Когнитивная архитектура
            self.cognitive_arch = CognitiveArchitecture(
                capacity=self.config.get('working_memory_capacity', 7)
            )
            
            # 5. Система идентичности
            personality_config_path = os.path.join(configs_path, 'personality_config.json')
            self.identity_matrix = IdentityMatrix(
                initial_identity=self.config.get('initial_identity', {}),
                config_path=personality_config_path
            )
            
            # 6. Система памяти
            self.memory_palace = MemoryPalace(storage_path=memory_path)
            
            # 7. Модуль эмпатии
            self.empathy_resonator = EmpathyResonator()
            
            # 8. Двигатель рефлексии
            self.reflection_engine = ReflectionEngine()
            
            # 9. Динамика убеждений
            self.belief_dynamics = BeliefDynamics()
            
            # 10. Социальный интеллект
            self.social_intelligence = SocialIntelligence()
            
            # 11. Физиологический симулятор
            self.physiological_sim = PhysiologicalSimulator()
            
            # 12. Генератор поведения
            self.behavioral_gen = BehavioralGenerator()
            
            # 13. Поток сознания
            self.consciousness_stream = ConsciousnessStream()
            
            # 14. Система обучения
            self.learning_evolver = LearningEvolver()
            
            # 15. Модель мира
            self.world_model = WorldModel()
            
            self.logger.log_system_event("SYSTEM_INITIALIZED", "All modules loaded successfully")
            
        except Exception as e:
            self.logger.log_system_event("INIT_ERROR", f"Failed to initialize: {str(e)}")
            raise
    
    def _find_fred_path(self, base_path: str) -> str:
        """Автоматическое определение пути к модели FRED"""
        # Сначала ищем в текущей директории
        current_path = os.path.join(base_path, 'FRED')
        if os.path.exists(current_path):
            return current_path
        
        # Затем ищем в поддиректориях
        search_paths = [
            os.path.join(base_path, 'models', 'FRED'),
            os.path.join(base_path, 'models', 'fred-t5'),
            os.path.join(base_path, 'models'),
            os.path.join(base_path, 'FRED'),
        ]
        
        for path in search_paths:
            if os.path.exists(path):
                # Проверяем, есть ли в директории необходимые файлы модели
                try:
                    files = os.listdir(path)
                    # Ищем файлы модели (модельные файлы, токенизатор, конфиги)
                    model_files = [f for f in files if any(ext in f.lower() for ext in ['.bin', '.json', '.pt', '.ckpt', '.safetensors', 'tokenizer', 'config'])]
                    if len(model_files) >= 3:  # Если есть хотя бы 3 файла модели
                        return path
                except PermissionError:
                    continue
        
        # Если не найдено, выбрасываем ошибку
        raise FileNotFoundError(f"Could not find FRED model in any of the expected locations: {search_paths}")
    
    def _find_configs_path(self, base_path: str) -> str:
        """Автоматическое определение пути к конфигурациям"""
        search_paths = [
            os.path.join(base_path, 'configs'),
            os.path.join(base_path, 'config'),
            os.path.join(base_path, 'configuration'),
            os.path.join(base_path, 'settings'),
        ]
        
        for path in search_paths:
            if os.path.exists(path):
                try:
                    files = os.listdir(path)
                    # Ищем JSON или YAML файлы конфигурации
                    config_files = [f for f in files if f.endswith(('.json', '.yaml', '.yml'))]
                    if len(config_files) > 0:
                        return path
                except PermissionError:
                    continue
        
        # Если не найдено, выбрасываем ошибку
        raise FileNotFoundError(f"Could not find configs directory in any of the expected locations: {search_paths}")
    
    def _find_memory_path(self, base_path: str) -> str:
        """Автоматическое определение пути к базе данных памяти"""
        search_paths = [
            os.path.join(base_path, 'models', 'memory_db'),
            os.path.join(base_path, 'memory'),
            os.path.join(base_path, 'data', 'memory'),
            os.path.join(base_path, 'storage', 'memory'),
        ]
        
        for path in search_paths:
            try:
                os.makedirs(path, exist_ok=True)  # Создаем директорию, если она не существует
                if os.path.exists(path):
                    return path
            except PermissionError:
                continue
        
        # Если не найдено, создаем и возвращаем
        memory_path = os.path.join(base_path, 'models', 'memory_db')
        os.makedirs(memory_path, exist_ok=True)
        return memory_path
    
    def _find_logs_path(self, base_path: str) -> str:
        """Автоматическое определение пути к логам"""
        search_paths = [
            os.path.join(base_path, 'logs'),
            os.path.join(base_path, 'log'),
            os.path.join(base_path, 'data', 'logs'),
        ]
        
        for path in search_paths:
            try:
                os.makedirs(path, exist_ok=True)  # Создаем директорию, если она не существует
                if os.path.exists(path):
                    return path
            except PermissionError:
                continue
        
        # Если не найдено, создаем и возвращаем
        logs_path = os.path.join(base_path, 'logs')
        os.makedirs(logs_path, exist_ok=True)
        return logs_path

    def process_interaction(self, user_input: str) -> str:
        """Основной цикл обработки взаимодействия"""
        start_time = time.time()
        
        try:
            # 1. Обновление модели мира
            world_update = self.world_model.update_world_state({
                'audio': {'speech': user_input}
            })
            
            # 2. Эмоциональная обработка входа
            emotional_response = self.emotional_field.update_state(
                {'type': 'input_received', 'intensity': 0.5},
                self.neurotransmitter_net.neurotransmitters
            )
            
            # 3. Нейрохимическое обновление
            neurotransmitter_update = self.neurotransmitter_net.update_levels(
                emotional_response, {}
            )
            
            # 4. Обработка в потоке сознания
            consciousness_response = self.consciousness_stream.process_consciousness_input(
                sensory_input={'text': user_input},
                cognitive_input={'task': 'understanding'},
                emotional_input=emotional_response
            )
            
            # 5. Когнитивная обработка
            cognitive_processing = self.cognitive_arch.process_stimulus(
                {'input': user_input, 'type': 'question'},
                system_preference=0
            )
            
            # 6. Обработка эмпатии
            empathy_response = self.empathy_resonator.process_user_emotional_state(
                user_input, emotional_response
            )
            
            # 7. Обновление памяти
            memory_id = self.memory_palace.encode(
                information={'input': user_input, 'timestamp': time.time()},
                memory_type='episodic',
                emotional_tag=emotional_response.get('intensity', 0.5)
            )
            
            # 8. Обновление убеждений
            self.belief_dynamics.update_belief(
                domain='social_model',
                belief_key='user_interaction_pattern',
                new_evidence={'value': user_input, 'context': 'direct_conversation'},
                evidence_strength=0.6
            )
            
            # 9. Генерация поведения
            behavioral_response = self.behavioral_gen.generate_behavior(
                emotional_state=emotional_response,
                social_context={'formality': 0.5, 'intimacy_level': 0.5},
                cognitive_state=cognitive_processing['result']
            )
            
            # 10. Обновление физиологического состояния
            phys_update = self.physiological_sim.update_physiology(
                emotional_state=emotional_response,
                cognitive_load=cognitive_processing['working_memory_load']
            )
            
            # 11. Генерация ответа с учетом всех систем
            response = self.neural_core.generate_response(
                user_input, 
                emotional_context=emotional_response,
            )
            
            # 12. Обновление социального интеллекта
            social_update = self.social_intelligence.process_social_context({
                'text': user_input,
                'formality': 0.5,
                'communication_style': 'balanced'
            })
            
            # 13. Анализ взаимодействия в движке рефлексии
            reflection_result = self.reflection_engine.analyze_interaction(
                user_input, response['response']
            )
            
            # 14. Обновление идентичности
            identity_update = self.identity_matrix.update_self_concept(
                experience={
                    'type': 'interaction',
                    'description': f"Responded to: {user_input[:50]}",
                    'impact': 0.3,
                    'valence': emotional_response.get('valence', 0.0)
                },
                reflection=reflection_result
            )
            
            # 15. Обучение на взаимоделе
            learning_result = self.learning_evolver.process_learning_experience(
                experience={
                    'input': user_input,
                    'response': response['response'],
                    'context': 'conversation',
                    'skill_area': 'communication'
                },
                feedback={
                    'outcome': 'completed',
                    'reward': 0.5,
                    'novelty': 0.2,
                    'social_validation': 0.3
                }
            )
            
            # 16. Обновление системы на основе опыта
            self.learning_evolver.update_from_experience()
            
            # Логгирование метрик
            processing_time = time.time() - start_time
            interaction_data = {
                'input': user_input,
                'response': response['response'],
                'processing_time': processing_time,
                'emotional_state': emotional_response,
                'cognitive_load': cognitive_processing['working_memory_load'],
                'timestamp': datetime.now(),
                'behavioral_response': behavioral_response
            }
            self.metrics.record_interaction(interaction_data)
            
            return response['response']
            
        except Exception as e:
            self.logger.log_system_event("PROCESSING_ERROR", f"Interaction failed: {str(e)}")
            return "Произошла внутренняя ошибка обработки."

    def health_check(self) -> dict:
        """Проверка работоспособности всех модулей"""
        health_status = {}
        
        modules = {
            'neural_core': self.neural_core,
            'emotional_field': self.emotional_field,
            'neurotransmitter_net': self.neurotransmitter_net,
            'cognitive_arch': self.cognitive_arch,
            'identity_matrix': self.identity_matrix,
            'memory_palace': self.memory_palace,
            'empathy_resonator': self.empathy_resonator,
            'reflection_engine': self.reflection_engine,
            'belief_dynamics': self.belief_dynamics,
            'social_intelligence': self.social_intelligence,
            'physiological_sim': self.physiological_sim,
            'behavioral_gen': self.behavioral_gen,
            'consciousness_stream': self.consciousness_stream,
            'learning_evolver': self.learning_evolver,
            'world_model': self.world_model
        }
        
        for name, module in modules.items():
            try:
                # Проверяем наличие методов получения состояния или простую функциональность
                if hasattr(module, 'get_current_superposition'):
                    # Для эмоционального поля
                    module.get_current_superposition()
                    health_status[name] = 'OK'
                elif hasattr(module, 'get_memory_statistics'):
                    # Для системы памяти
                    module.get_memory_statistics()
                    health_status[name] = 'OK'
                elif hasattr(module, 'get_') or hasattr(module, '_get_current'):
                    # Общая проверка на методы получения состояния
                    health_status[name] = 'OK'
                else:
                    # Если методов получения состояния нет, просто проверяем, что модуль существует
                    health_status[name] = 'LOADED'
            except Exception as e:
                health_status[name] = f'ERROR: {str(e)}'
        
        return health_status
    
    def get_metrics_summary(self) -> dict:
        """Получение сводки метрик"""
        return self.metrics.generate_health_report()
    
    def train_on_interaction(self, user_input: str, expected_output: str, feedback: float = 1.0):
        """Обучение на основе взаимодействия с учителем"""
        try:
            # Создаем опыт обучения
            learning_experience = {
                'input': user_input,
                'expected_output': expected_output,
                'actual_output': self.process_interaction(user_input),
                'context': 'supervised_learning',
                'skill_area': 'communication'
            }
            
            # Обновляем систему обучения
            self.learning_evolver.process_learning_experience(
                experience=learning_experience,
                feedback={
                    'outcome': 'supervised',
                    'reward': feedback,
                    'novelty': 0.1,
                    'social_validation': feedback
                }
            )
            
            # Применяем обучение
            self.learning_evolver.update_from_experience()
            
            return True
        except Exception as e:
            self.logger.log_system_event("TRAINING_ERROR", f"Training failed: {str(e)}")
            return False


class EmotionalAIUI:
    def __init__(self, system: EmotionalAISystem):
        self.system = system
        # Using the enhanced UI instead of the basic one
        self.enhanced_ui = EnhancedEmotionalAIUI(system)
    
    def run(self):
        """Run the enhanced UI"""
        self.enhanced_ui.run()


def main():
    # Определение корневой папки проекта
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    try:
        # Инициализация системы (автоматическое определение всех путей)
        system = EmotionalAISystem(base_path)
        
        # Создание и запуск UI
        ui = EmotionalAIUI(system)
        ui.run()
        
    except Exception as e:
        print(f"Ошибка инициализации системы: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()