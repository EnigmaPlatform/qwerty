"""
РЕАЛИЗАЦИЯ main.py:

ТРЕБОВАНИЯ:
1. Централизованный запуск всей системы
2. Загрузка всех моделей из корневой папки проекта
3. Комплексная инициализация всех модулей
4. Единая система логгирования и мониторинга

ДЕТАЛИ РЕАЛИЗАЦИИ:
- Последовательная инициализация модулей в правильном порядке
- Глобальный обработчик ошибок и исключений
- Система health-check для всех модулей
- Интерфейс взаимодействия с пользователем
- Периодическое сохранение состояния системы

КОДОВАЯ СТРУКТУРА:
"""
import os
import logging
import time
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


class EmotionalAISystem:
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.logger = SystemLogger(os.path.join(base_path, 'logs'))
        self.metrics = MetricsCollector()
        self.config = ConfigLoader.load_all_configs(base_path)
        
        # Инициализация модулей в правильном порядке
        self.init_modules()
        
    def init_modules(self):
        try:
            # Определение пути к папке FRED из директории запуска main.py
            execution_base_path = os.path.dirname(os.path.abspath(__file__))
            fred_path = os.path.join(execution_base_path, 'FRED')
            
            # Сканирование содержимого папки FRED
            print(f"Сканирование папки FRED: {fred_path}")
            if os.path.exists(fred_path):
                fred_contents = os.listdir(fred_path)
                print(f"Содержимое папки FRED: {fred_contents}")
                
                # Определение необходимых файлов для корректной работы
                required_extensions = ['.bin', '.json', '.txt', '.model', '.pt', '.ckpt', '.safetensors']
                executable_files = []
                
                for item in fred_contents:
                    item_path = os.path.join(fred_path, item)
                    if os.path.isfile(item_path):
                        _, ext = os.path.splitext(item)
                        if ext.lower() in required_extensions:
                            executable_files.append(item)
                
                print(f"Найденные исполняемые/модельные файлы в FRED: {executable_files}")
            else:
                print(f"Папка FRED не найдена по пути: {fred_path}")
                # Используем старый путь в качестве резерва
                fred_path = os.path.join(self.base_path, 'models/fred-t5')
            
            # 1. Базовая инициализация
            self.neural_core = NeuralLanguageCore(fred_path)
            
            # 2. Эмоциональная система
            self.emotional_field = EmotionalQuantumField(
                os.path.join(self.base_path, 'configs/emotion_config.json')
            )
            
            # 3. Нейротрансмиттерная сеть
            self.neurotransmitter_net = NeurotransmitterNetwork(
                self.config['neurotransmitter_initial']
            )
            
            # 4. Когнитивная архитектура
            self.cognitive_arch = CognitiveArchitecture(
                capacity=self.config.get('working_memory_capacity', 7)
            )
            
            # 5. Система идентичности
            self.identity_matrix = IdentityMatrix(
                initial_identity=self.config.get('initial_identity', {})
            )
            
            # 6. Система памяти
            self.memory_palace = MemoryPalace(
                storage_path=os.path.join(self.base_path, 'models/memory_db/')
            )
            
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
                # Проверяем наличие метода получения состояния
                if hasattr(module, 'get_') or hasattr(module, '_get_current'):
                    health_status[name] = 'OK'
                else:
                    health_status[name] = 'PARTIAL'
            except Exception:
                health_status[name] = 'ERROR'
        
        return health_status


def main():
    # Определение корневой папки проекта
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Создание необходимых директорий
    os.makedirs(os.path.join(base_path, 'logs'), exist_ok=True)
    os.makedirs(os.path.join(base_path, 'models', 'memory_db'), exist_ok=True)
    
    # Инициализация системы
    system = EmotionalAISystem(base_path)
    
    # Запуск интерфейса взаимодействия
    print("Эмоциональный ИИ инициализирован. Готов к общению.")
    print("Для выхода введите 'выход', 'exit' или 'quit'")
    
    while True:
        try:
            user_input = input("Вы: ")
            if user_input.lower() in ['выход', 'exit', 'quit']:
                break
                
            response = system.process_interaction(user_input)
            print(f"ИИ: {response}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Ошибка: {e}")
    
    # Корректное завершение
    system.logger.log_system_event("SYSTEM_SHUTDOWN", "Normal shutdown")


if __name__ == "__main__":
    main()