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
            # Автоматическое определение путей для всех файлов
            execution_base_path = os.path.dirname(os.path.abspath(__file__))
            
            # Определение пути к модели FRED
            fred_path = self._find_fred_path(execution_base_path)
            
            # Определение пути к конфигурациям
            configs_path = self._find_configs_path(execution_base_path)
            
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
        possible_paths = [
            os.path.join(base_path, 'FRED'),
            os.path.join(base_path, 'models', 'FRED'),
            os.path.join(base_path, 'models', 'fred-t5'),
            os.path.join(base_path, 'models'),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                # Проверяем, есть ли в директории необходимые файлы модели
                files = os.listdir(path)
                model_files = [f for f in files if f.endswith(('.bin', '.json', '.pt', '.ckpt', '.safetensors'))]
                if len(model_files) >= 3:  # Если есть хотя бы 3 файла модели
                    return path
        
        # Если не найдено, выбрасываем ошибку
        raise FileNotFoundError(f"Could not find FRED model in any of the expected locations: {possible_paths}")
    
    def _find_configs_path(self, base_path: str) -> str:
        """Автоматическое определение пути к конфигурациям"""
        possible_paths = [
            os.path.join(base_path, 'configs'),
            os.path.join(base_path, 'config'),
            os.path.join(base_path, 'configuration'),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                files = os.listdir(path)
                config_files = [f for f in files if f.endswith('.json') or f.endswith('.yaml')]
                if len(config_files) > 0:
                    return path
        
        # Если не найдено, выбрасываем ошибку
        raise FileNotFoundError(f"Could not find configs directory in any of the expected locations: {possible_paths}")
    
    def _find_memory_path(self, base_path: str) -> str:
        """Автоматическое определение пути к базе данных памяти"""
        possible_paths = [
            os.path.join(base_path, 'models', 'memory_db'),
            os.path.join(base_path, 'memory'),
            os.path.join(base_path, 'data', 'memory'),
        ]
        
        for path in possible_paths:
            os.makedirs(path, exist_ok=True)  # Создаем директорию, если она не существует
            if os.path.exists(path):
                return path
        
        # Если не найдено, создаем и возвращаем
        memory_path = os.path.join(base_path, 'models', 'memory_db')
        os.makedirs(memory_path, exist_ok=True)
        return memory_path

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
        self.root = tk.Tk()
        self.root.title("Emotional AI System - Hacker Interface")
        self.root.geometry("1000x700")
        
        # Устанавливаем темный стиль
        self.setup_dark_theme()
        
        # Создаем интерфейс
        self.create_widgets()
        
        # Текущий режим (чат, обучение, метрики)
        self.current_mode = "chat"
        
        # Обновляем интерфейс
        self.update_display()
    
    def setup_dark_theme(self):
        """Настройка темной темы с неоново-зелеными элементами"""
        self.root.configure(bg='#0a0a0a')
        
        # Настройка стилей для ttk виджетов
        style = ttk.Style()
        style.theme_use('clam')
        
        # Определение цветов
        bg_color = '#0a0a0a'  # Темный фон
        text_color = '#00ff00'  # Неоново-зеленый текст
        accent_color = '#00cc00'  # Акцентный цвет
        input_bg = '#111111'  # Фон для ввода
        button_bg = '#003300'  # Фон кнопок
        
        # Настройка стилей
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=text_color, font=('Courier', 10, 'bold'))
        style.configure('TButton', background=button_bg, foreground=text_color, 
                       font=('Courier', 10, 'bold'), borderwidth=2)
        style.map('TButton', background=[('active', accent_color)])
        style.configure('TNotebook', background=bg_color, tabposition='n')
        style.configure('TNotebook.Tab', background=button_bg, foreground=text_color, 
                       font=('Courier', 10, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', accent_color)])
    
    def create_widgets(self):
        """Создание виджетов интерфейса"""
        # Основной контейнер
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="EMOTIONAL AI SYSTEM", font=('Courier', 20, 'bold'))
        title_label.pack(pady=10)
        
        # Создаем вкладки
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Вкладка чата
        self.chat_frame = ttk.Frame(notebook)
        notebook.add(self.chat_frame, text='  ЧАТ  ')
        
        # Вкладка обучения
        self.training_frame = ttk.Frame(notebook)
        notebook.add(self.training_frame, text='  ОБУЧЕНИЕ  ')
        
        # Вкладка метрик
        self.metrics_frame = ttk.Frame(notebook)
        notebook.add(self.metrics_frame, text='  МЕТРИКИ  ')
        
        # Создаем интерфейс для каждой вкладки
        self.create_chat_interface()
        self.create_training_interface()
        self.create_metrics_interface()
    
    def create_chat_interface(self):
        """Создание интерфейса чата"""
        # Область чата
        chat_area_frame = ttk.Frame(self.chat_frame)
        chat_area_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Текстовая область для чата
        self.chat_display = scrolledtext.ScrolledText(
            chat_area_frame, 
            wrap=tk.WORD, 
            state=tk.DISABLED,
            bg='#0a0a0a', 
            fg='#00ff00', 
            font=('Courier', 10),
            insertbackground='#00ff00'
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        
        # Область ввода
        input_frame = ttk.Frame(self.chat_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        self.user_input = ttk.Entry(
            input_frame, 
            font=('Courier', 12),
            style='Dark.TEntry'
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.user_input.bind('<Return>', self.send_message)
        
        send_button = ttk.Button(
            input_frame, 
            text="ОТПРАВИТЬ", 
            command=self.send_message
        )
        send_button.pack(side=tk.RIGHT)
        
        # Health check кнопка
        health_button = ttk.Button(
            self.chat_frame,
            text="ПРОВЕРКА СИСТЕМЫ",
            command=self.run_health_check
        )
        health_button.pack(pady=5)
        
        # Инициализация истории чата
        self.chat_history = []
        self.add_to_chat("СИСТЕМА", "Эмоциональный ИИ инициализирован. Готов к общению.")
    
    def create_training_interface(self):
        """Создание интерфейса обучения"""
        # Объяснение
        info_label = ttk.Label(
            self.training_frame, 
            text="ОБУЧЕНИЕ ИИ: Введите входные данные и ожидаемый результат для обучения системы"
        )
        info_label.pack(pady=10)
        
        # Фреймы для ввода
        input_frame = ttk.Frame(self.training_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="ВХОДНЫЕ ДАННЫЕ:").pack(anchor=tk.W)
        self.training_input = scrolledtext.ScrolledText(
            input_frame, 
            height=3,
            bg='#111111', 
            fg='#00ff00', 
            font=('Courier', 10)
        )
        self.training_input.pack(fill=tk.X, pady=5)
        
        expected_frame = ttk.Frame(self.training_frame)
        expected_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(expected_frame, text="ОЖИДАЕМЫЙ РЕЗУЛЬТАТ:").pack(anchor=tk.W)
        self.training_expected = scrolledtext.ScrolledText(
            expected_frame, 
            height=3,
            bg='#111111', 
            fg='#00ff00', 
            font=('Courier', 10)
        )
        self.training_expected.pack(fill=tk.X, pady=5)
        
        # Кнопка обучения
        train_button = ttk.Button(
            self.training_frame,
            text="НАЧАТЬ ОБУЧЕНИЕ",
            command=self.start_training
        )
        train_button.pack(pady=10)
        
        # Область вывода результата
        result_frame = ttk.Frame(self.training_frame)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ttk.Label(result_frame, text="РЕЗУЛЬТАТ ОБУЧЕНИЯ:").pack(anchor=tk.W)
        self.training_result = scrolledtext.ScrolledText(
            result_frame, 
            height=8,
            bg='#111111', 
            fg='#00ff00', 
            font=('Courier', 10)
        )
        self.training_result.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def create_metrics_interface(self):
        """Создание интерфейса метрик"""
        # Область метрик
        metrics_area = ttk.Frame(self.metrics_frame)
        metrics_area.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Кнопка обновления метрик
        refresh_button = ttk.Button(
            self.metrics_frame,
            text="ОБНОВИТЬ МЕТРИКИ",
            command=self.update_metrics_display
        )
        refresh_button.pack(pady=5)
        
        # Текстовая область для метрик
        self.metrics_display = scrolledtext.ScrolledText(
            metrics_area, 
            wrap=tk.WORD,
            bg='#0a0a0a', 
            fg='#00ff00', 
            font=('Courier', 10)
        )
        self.metrics_display.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Отображаем начальные метрики
        self.update_metrics_display()
    
    def add_to_chat(self, sender: str, message: str):
        """Добавление сообщения в чат"""
        self.chat_display.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(
            tk.END, 
            f"[{timestamp}] {sender}: {message}\n",
            ('green',)  # Стиль для неоново-зеленого текста
        )
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)  # Прокрутка к концу
        
        # Сохраняем в историю
        self.chat_history.append({
            'timestamp': timestamp,
            'sender': sender,
            'message': message
        })
    
    def send_message(self, event=None):
        """Отправка сообщения"""
        user_text = self.user_input.get()
        if not user_text.strip():
            return
            
        # Добавляем сообщение пользователя в чат
        self.add_to_chat("ВЫ", user_text)
        self.user_input.delete(0, tk.END)
        
        # Обрабатываем сообщение ИИ
        try:
            ai_response = self.system.process_interaction(user_text)
            self.add_to_chat("ИИ", ai_response)
        except Exception as e:
            self.add_to_chat("СИСТЕМА", f"Ошибка обработки: {str(e)}")
    
    def run_health_check(self):
        """Выполнение проверки системы"""
        try:
            health_status = self.system.health_check()
            status_text = "РЕЗУЛЬТАТ ПРОВЕРКИ СИСТЕМЫ:\n\n"
            for module, status in health_status.items():
                status_text += f"{module}: {status}\n"
            
            self.add_to_chat("СИСТЕМА", status_text.strip())
        except Exception as e:
            self.add_to_chat("СИСТЕМА", f"Ошибка проверки системы: {str(e)}")
    
    def start_training(self):
        """Начало процесса обучения"""
        input_text = self.training_input.get("1.0", tk.END).strip()
        expected_text = self.training_expected.get("1.0", tk.END).strip()
        
        if not input_text or not expected_text:
            messagebox.showwarning("Предупреждение", "Пожалуйста, заполните оба поля: входные данные и ожидаемый результат.")
            return
        
        try:
            # Выполняем обучение
            success = self.system.train_on_interaction(input_text, expected_text)
            
            if success:
                result_text = f"ОБУЧЕНИЕ ЗАВЕРШЕНО УСПЕШНО\n\nВход: {input_text}\nОжидаемый результат: {expected_text}\n\nСистема обучена на основе предоставленных данных."
                self.training_result.delete("1.0", tk.END)
                self.training_result.insert("1.0", result_text)
                
                # Очищаем поля ввода
                self.training_input.delete("1.0", tk.END)
                self.training_expected.delete("1.0", tk.END)
            else:
                self.training_result.delete("1.0", tk.END)
                self.training_result.insert("1.0", "ОШИБКА ОБУЧЕНИЯ: Произошла ошибка во время процесса обучения.")
        except Exception as e:
            self.training_result.delete("1.0", tk.END)
            self.training_result.insert("1.0", f"ОШИБКА ОБУЧЕНИЯ: {str(e)}")
    
    def update_metrics_display(self):
        """Обновление отображения метрик"""
        try:
            metrics = self.system.get_metrics_summary()
            
            metrics_text = "МЕТРИКИ СИСТЕМЫ:\n\n"
            for key, value in metrics.items():
                if isinstance(value, dict):
                    metrics_text += f"{key}:\n"
                    for sub_key, sub_value in value.items():
                        metrics_text += f"  {sub_key}: {sub_value}\n"
                else:
                    metrics_text += f"{key}: {value}\n"
            
            self.metrics_display.delete("1.0", tk.END)
            self.metrics_display.insert("1.0", metrics_text)
        except Exception as e:
            error_text = f"ОШИБКА ПОЛУЧЕНИЯ МЕТРИК: {str(e)}"
            self.metrics_display.delete("1.0", tk.END)
            self.metrics_display.insert("1.0", error_text)
    
    def update_display(self):
        """Обновление отображения в зависимости от режима"""
        pass
    
    def run(self):
        """Запуск интерфейса"""
        self.root.mainloop()


def main():
    # Определение корневой папки проекта
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Создание необходимых директорий
    os.makedirs(os.path.join(base_path, 'logs'), exist_ok=True)
    os.makedirs(os.path.join(base_path, 'models', 'memory_db'), exist_ok=True)
    
    try:
        # Инициализация системы
        system = EmotionalAISystem(base_path)
        
        # Создание и запуск UI
        ui = EmotionalAIUI(system)
        ui.run()
        
    except Exception as e:
        print(f"Ошибка инициализации системы: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()