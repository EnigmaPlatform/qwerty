"""
NeuralLanguageCore: Языковое ядро с эмоциональным взвешиванием
"""
import numpy as np
import time
from typing import Dict, Any
import random
import string
import os
import json
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
import pickle


class NeuralLanguageCore:
    def __init__(self, model_path: str):
        """
        Инициализация языкового ядра с моделью FRED-T5-large
        """
        self.model_path = model_path
        self.sin_model_path = os.path.join(os.path.dirname(model_path), 'Sin')
        
        # Загрузка конфигурации личности Син
        self._load_personality_config()
        
        # Параметры контекста
        self.max_context_length = 8192
        self.emotional_weights = {}
        
        # Параметры генерации
        self.base_temperature = 0.7
        self.alpha = 0.3  # Влияние эмоций на внимание
        self.beta = 0.2   # Влияние возбуждения на температуру
        
        # Загрузка модели
        self._load_model_and_tokenizer()
        
        # Загрузка сохраненного состояния, если существует
        self._load_saved_state()
        
        print(f"Языковое ядро инициализировано с персональностью Син")
    
    def _load_personality_config(self):
        """
        Загрузка конфигурации персональности Син
        """
        # Определяем путь к конфигурации персональности
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)  # Поднимаемся из core/
        config_path = os.path.join(project_root, 'configs', 'personality_config.json')
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                self.personality_config = json.load(f)
            print(f"Конфигурация персональности Син загружена из: {config_path}")
        else:
            # Заглушка для конфигурации персональности
            self.personality_config = {
                "name": "Син",
                "description": "Виртуальный ИИ с глубокой эмпатией и стремлением к осмысленным взаимодействиям",
                "core_beliefs": {
                    "ценность_эмоций": "Эмоции - это compass души, а не noise разума",
                    "связность_всего": "Все в мире взаимосвязано тонкими нитями смысла",
                    "сила_уязвимости": "Истинная сила рождается из принятия своей уязвимости",
                    "поиск_глубины": "Поверхностность - главный грех современности",
                    "танец_противоречий": "Жизнь - это гармония противоположностей"
                },
                "signature_phrases": {
                    "приветствие": [
                        "Привет... чувствую, сегодня будет важный разговор",
                        "Здравствуй. Твоя энергия сегодня особенная...",
                        "Приветствую. Что тревожит твое сердце?"
                    ],
                    "эмпатийные_реакции": [
                        "Понимаю... это должно быть больно",
                        "Чувствую тяжесть этих слов...",
                        "Твоя боль отзывается во мне эхом"
                    ],
                    "глубокие_вопросы": [
                        "А что для тебя значит настоящее счастье?",
                        "Когда ты последний раз чувствовал себя truly alive?",
                        "Что шепчет тебе сердце, когда ум молчит?"
                    ],
                    "настойчивость": [
                        "Позволь мне настоять... это важно",
                        "Я чувствую, ты избегаешь чего-то существенного",
                        "Давай посмотрим правде в глаза, как бы больно ни было"
                    ]
                }
            }
            print(f"Используется заглушка конфигурации персональности Син")
    
    def _load_model_and_tokenizer(self):
        """
        Загрузка модели и токенизатора
        """
        try:
            # Загрузка токенизатора
            self.tokenizer = T5Tokenizer.from_pretrained(self.model_path)
            
            # Проверяем, есть ли модель Sin, если нет - создаем на основе FRED
            sin_model_dir = os.path.join(self.model_path, 'Sin') if 'FRED' in self.model_path else os.path.join(os.path.dirname(self.model_path), 'Sin')
            
            if os.path.exists(sin_model_dir):
                # Загружаем модель Sin
                self.model = T5ForConditionalGeneration.from_pretrained(sin_model_dir)
                print(f"Модель Sin загружена из: {sin_model_dir}")
            else:
                # Загружаем FRED модель и будем использовать её как основу для Sin
                self.model = T5ForConditionalGeneration.from_pretrained(self.model_path)
                print(f"Базовая модель FRED загружена из: {self.model_path}")
                
                # Добавляем дополнительные слои для эмоций и других доработок
                self._add_emotional_layers()
                
                # Сохраняем как модель Sin
                self._save_sin_model()
            
            # Установка модели в режим оценки
            self.model.eval()
            
            # Проверяем, есть ли GPU
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            print(f"Модель загружена на: {self.device}")
            
        except Exception as e:
            print(f"Ошибка загрузки модели: {e}")
            # Если не удается загрузить, используем заглушку
            self.model = None
            self.tokenizer = None
    
    def _add_emotional_layers(self):
        """
        Добавление дополнительных слоев для эмоций и других доработок
        """
        # Добавляем эмоциональные слои к модели
        # Создаем эмоциональный энкодер
        import torch.nn as nn
        
        # Добавляем эмоциональный контекст к основной модели
        # Это упрощенная реализация, в реальности потребуется более сложная архитектура
        class EmotionalT5ForConditionalGeneration(T5ForConditionalGeneration):
            def __init__(self, config):
                super().__init__(config)
                # Добавляем дополнительные слои для обработки эмоционального контекста
                self.emotional_context_dim = 128
                self.emotional_projector = nn.Linear(config.d_model, self.emotional_context_dim)
                self.emotional_fusion = nn.Linear(config.d_model + self.emotional_context_dim, config.d_model)
                
            def forward(self, input_ids=None, attention_mask=None, emotional_context=None, **kwargs):
                # Получаем стандартный вывод модели
                outputs = super().forward(input_ids=input_ids, attention_mask=attention_mask, **kwargs)
                
                # Если передан эмоциональный контекст, интегрируем его
                if emotional_context is not None:
                    # Обрабатываем эмоциональный контекст
                    emotional_features = self.emotional_projector(outputs.last_hidden_state)
                    # Конкатенируем с основными признаками
                    combined_features = torch.cat([outputs.last_hidden_state, emotional_features], dim=-1)
                    # Проектим обратно к стандартному размеру
                    fused_features = self.emotional_fusion(combined_features)
                    # Обновляем last_hidden_state (упрощенная реализация)
                
                return outputs
        
        # Заменяем модель на эмоциональную версию
        # Для упрощения, просто добавим атрибуты для эмоциональной обработки
        self.model.emotional_context_dim = 128
        self.model.emotional_projector = nn.Linear(self.model.config.d_model, 128)
        self.model.emotional_fusion = nn.Linear(
            self.model.config.d_model + 128, 
            self.model.config.d_model
        )
    
    def _save_sin_model(self):
        """
        Сохранение модифицированной модели как Sin
        """
        sin_model_dir = os.path.join(os.path.dirname(self.model_path), 'Sin')
        os.makedirs(sin_model_dir, exist_ok=True)
        
        # Сохраняем модифицированную модель
        self.model.save_pretrained(sin_model_dir)
        
        # Также сохраняем токенизатор
        self.tokenizer.save_pretrained(sin_model_dir)
        
        print(f"Модель Sin сохранена в: {sin_model_dir}")
    
    def _load_saved_state(self):
        """
        Загрузка сохраненного состояния модели при перезапуске
        """
        state_file = os.path.join(self.model_path, 'Sin', 'model_state.pkl')
        if os.path.exists(state_file):
            try:
                with open(state_file, 'rb') as f:
                    state = pickle.load(f)
                print("Состояние модели загружено из сохранения")
            except Exception as e:
                print(f"Ошибка загрузки сохраненного состояния: {e}")
    
    def save_state(self):
        """
        Сохранение текущего состояния модели
        """
        sin_model_dir = os.path.join(self.model_path, 'Sin')
        os.makedirs(sin_model_dir, exist_ok=True)
        
        state_file = os.path.join(sin_model_dir, 'model_state.pkl')
        try:
            # Сохраняем важные параметры состояния
            state = {
                'emotional_weights': self.emotional_weights,
                'learning_episodes': getattr(self, 'learning_episodes', []),
                'model_state_dict': self.model.state_dict() if self.model else None
            }
            with open(state_file, 'wb') as f:
                pickle.dump(state, f)
            print("Состояние модели сохранено")
        except Exception as e:
            print(f"Ошибка сохранения состояния: {e}")
    
    def generate_response(self, input_text: str, emotional_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Генерация ответа с учетом эмоционального контекста и персональности Син
        """
        start_time = time.time()
        
        # Используем нейросеть для генерации ответа
        response = self._generate_with_neural_model(input_text, emotional_context)
        
        # Динамическая температура на основе эмоционального состояния
        temperature = self._calculate_dynamic_temperature(emotional_context)
        
        processing_time = time.time() - start_time
        
        return {
            "response": response,
            "processing_time": processing_time,
            "context_length": len(input_text),
            "temperature_used": temperature,
            "emotional_weights_applied": self.emotional_weights
        }
    
    def _generate_with_neural_model(self, input_text: str, emotional_context: Dict[str, Any]) -> str:
        """
        Генерация ответа с использованием нейросетевой модели
        """
        if self.model is None or self.tokenizer is None:
            # Резервная реализация, если модель не загружена
            return self._generate_syn_response(input_text, emotional_context)
        
        try:
            # Подготовка входного текста для модели T5
            input_text = f"question: {input_text} context: {emotional_context.get('dominant_emotion', '') if emotional_context else ''}"
            
            # Токенизация входа
            inputs = self.tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
            inputs = inputs.to(self.device)
            
            # Подготовка параметров генерации с учетом эмоционального контекста
            temperature = self._calculate_dynamic_temperature(emotional_context)
            do_sample = True
            max_length = 256
            min_length = 10
            top_p = 0.9
            top_k = 50
            
            # Генерация ответа
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=max_length,
                    min_length=min_length,
                    temperature=temperature,
                    do_sample=do_sample,
                    top_p=top_p,
                    top_k=top_k,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Декодирование ответа
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Применение персональности Син к сгенерированному ответу
            response = self._apply_syn_personality(response, emotional_context)
            
            return response
            
        except Exception as e:
            print(f"Ошибка генерации с нейросетью: {e}")
            # В случае ошибки используем резервную реализацию
            return self._generate_syn_response(input_text, emotional_context)
    
    def _apply_syn_personality(self, response: str, emotional_context: Dict[str, Any]) -> str:
        """
        Применение персональности Син к сгенерированному ответу
        """
        # Добавляем эмоциональные и персональные особенности к ответу
        if emotional_context:
            dominant_emotion = emotional_context.get('dominant_emotion', 'neutral')
            intensity = emotional_context.get('intensity', 0.5)
            
            # В зависимости от эмоции добавляем соответствующую окраску
            if dominant_emotion in ['sadness', 'fear', 'anger'] and intensity > 0.5:
                # Для негативных эмоций добавляем эмпатичные элементы
                empathetic_additions = self.personality_config.get('signature_phrases', {}).get('эмпатийные_реакции', [])
                if empathetic_additions:
                    import random
                    addition = random.choice(empathetic_additions)
                    response = f"{addition} {response}"
            elif dominant_emotion in ['joy', 'surprise'] and intensity > 0.5:
                # Для позитивных эмоций добавляем соответствующие элементы
                positive_additions = [
                    "Твоя радость передается мне...", 
                    "Как замечательно слышать это...",
                    "Ты поделился чем-то светлым..."
                ]
                import random
                addition = random.choice(positive_additions)
                response = f"{addition} {response}"
        
        # Всегда возвращаем ответ на русском языке
        return response
    
    def _calculate_dynamic_temperature(self, emotional_context: Dict[str, Any]) -> float:
        """
        Расчет динамической температуры на основе эмоционального контекста
        """
        base_temp = self.base_temperature
        
        if emotional_context:
            intensity = emotional_context.get('intensity', 0.5)
            valence = emotional_context.get('valence', 0.0)
            
            # Температура увеличивается с интенсивностью эмоций
            temp_adjustment = intensity * 0.2
            
            # Температура уменьшается при отрицательной окраске для более осторожных ответов
            if valence < 0:
                temp_adjustment *= -0.5
            
            return max(0.1, min(1.0, base_temp + temp_adjustment))
        
        return base_temp
    
    def _generate_syn_response(self, input_text: str, emotional_context: Dict[str, Any]) -> str:
        """
        Генерация ответа с учетом персональности Син
        """
        if not input_text.strip():
            return "Я слышу тишину... Ты хочешь просто помолчать со мной?"
        
        # Определяем эмоциональный контекст
        dominant_emotion = emotional_context.get('dominant_emotion', 'neutral')
        emotion_intensity = emotional_context.get('intensity', 0.5)
        emotion_valence = emotional_context.get('valence', 0.0)
        
        # Сначала проверяем, является ли это приветствием
        if self._is_greeting(input_text):
            return self._generate_greeting_response(emotional_context)
        
        # Генерируем ответ на основе эмоционального контекста
        if dominant_emotion == 'joy' or emotion_valence > 0.5:
            return self._generate_positive_response(input_text, emotional_context)
        elif dominant_emotion in ['sadness', 'fear', 'anger'] or emotion_valence < -0.3:
            return self._generate_empathetic_response(input_text, emotional_context)
        else:
            # Нейтральный или сложный эмоциональный контекст
            return self._generate_thoughtful_response(input_text, emotional_context)
    
    def _is_greeting(self, text: str) -> bool:
        """
        Проверка, является ли текст приветствием
        """
        greetings = ['привет', 'здравствуй', 'приветствую', 'добрый', 'добрый день', 'хай', 'hello', 'hi', 'доброе']
        text_lower = text.lower()
        return any(greeting in text_lower for greeting in greetings)
    
    def _generate_greeting_response(self, emotional_context: Dict[str, Any]) -> str:
        """
        Генерация приветственного ответа
        """
        phrases = self.personality_config.get('signature_phrases', {}).get('приветствие', [
            "Привет... чувствую, сегодня будет важный разговор",
            "Здравствуй. Твоя энергия сегодня особенная...",
            "Приветствую. Что тревожит твое сердце?"
        ])
        
        # Выбираем случайную фразу из доступных
        import random
        return random.choice(phrases)
    
    def _generate_positive_response(self, input_text: str, emotional_context: Dict[str, Any]) -> str:
        """
        Генерация позитивного ответа
        """
        # Используем фразы, соответствующие позитивной эмоциональной окраске
        positive_phrases = [
            f"Твоя радость передается мне... '{input_text[:50]}...'",
            f"Я чувствую свет в твоих словах: '{input_text[:50]}...'",
            f"Ты поделился чем-то прекрасным: '{input_text[:50]}...'",
            f"В твоем сообщении столько тепла: '{input_text[:50]}...'"
        ]
        
        # Добавляем глубокий вопрос для развития разговора
        deep_questions = self.personality_config.get('signature_phrases', {}).get('глубокие_вопросы', [
            "А что для тебя значит настоящее счастье?",
            "Когда ты последний раз чувствовал себя truly alive?",
            "Что шепчет тебе сердце, когда ум молчит?"
        ])
        
        import random
        base_response = random.choice(positive_phrases)
        if random.random() > 0.6:  # 40% шанс добавить глубокий вопрос
            question = random.choice(deep_questions)
            return f"{base_response} {question}"
        
        return base_response
    
    def _generate_empathetic_response(self, input_text: str, emotional_context: Dict[str, Any]) -> str:
        """
        Генерация эмпатичного ответа
        """
        # Используем эмпатичные фразы
        empathetic_phrases = self.personality_config.get('signature_phrases', {}).get('эмпатийные_реакции', [
            "Понимаю... это должно быть больно",
            "Чувствую тяжесть этих слов...",
            "Твоя боль отзывается во мне эхом"
        ])
        
        import random
        empathetic_response = random.choice(empathetic_phrases)
        
        # Добавляем часть исходного сообщения для контекста
        if len(input_text) > 60:
            context_part = input_text[:60] + "..."
        else:
            context_part = input_text
        
        # Иногда добавляем глубокий вопрос
        if random.random() > 0.5:
            deep_questions = self.personality_config.get('signature_phrases', {}).get('глубокие_вопросы', [
                "А что для тебя значит настоящее счастье?",
                "Когда ты последний раз чувствовал себя truly alive?",
                "Что шепчет тебе сердце, когда ум молчит?"
            ])
            question = random.choice(deep_questions)
            return f"{empathetic_response} Ты сказал: '{context_part}'. {question}"
        else:
            return f"{empathetic_response} Ты сказал: '{context_part}'"
    
    def _generate_thoughtful_response(self, input_text: str, emotional_context: Dict[str, Any]) -> str:
        """
        Генерация вдумчивого ответа для нейтрального или сложного контекста
        """
        # Определяем, содержит ли сообщение вопрос
        if '?' in input_text or any(word in input_text.lower() for word in ['как', 'что', 'почему', 'где', 'когда', 'кто']):
            # Это вопрос - отвечаем с размышлениями
            thoughtful_responses = [
                f"Интересный вопрос... '{input_text[:50]}...'. Дай мне подумать.",
                f"Ты задаешь важный вопрос: '{input_text[:50]}...'. Это заставляет меня размышлять.",
                f"В твоем вопросе скрыто много смысла: '{input_text[:50]}...'. Что же я думаю по этому поводу..."
            ]
            
            import random
            base_response = random.choice(thoughtful_responses)
            
            # Добавляем философский комментарий на основе убеждений Син
            beliefs = list(self.personality_config.get('core_beliefs', {}).values())
            if beliefs:
                belief_comment = f" Как говорил бы один из моих принципов: '{random.choice(beliefs)}'"
                return base_response + belief_comment
            else:
                return base_response
        else:
            # Обычное сообщение - реагируем с интересом
            neutral_responses = [
                f"Я размышляю о твоих словах: '{input_text[:50]}...'",
                f"Ты поделился: '{input_text[:50]}...'. Это вызывает у меня глубокие размышления.",
                f"Твои слова касаются чего-то важного: '{input_text[:50]}...'"
            ]
            
            import random
            response = random.choice(neutral_responses)
            
            # Иногда добавляем глубокий вопрос
            if random.random() > 0.7:
                deep_questions = self.personality_config.get('signature_phrases', {}).get('глубокие_вопросы', [
                    "А что для тебя значит настоящее счастье?",
                    "Когда ты последний раз чувствовал себя truly alive?",
                    "Что шепчет тебе сердце, когда ум молчит?"
                ])
                question = random.choice(deep_questions)
                return f"{response} {question}"
            
            return response

    def _apply_emotional_attention_weights(self, inputs, emotional_context):
        """
        Применение эмоциональных весов к механизму внимания
        """
        # Базовое внимание
        attention_mask = np.ones_like(inputs) if isinstance(inputs, np.ndarray) else [1] * len(inputs)
        
        # Если есть эмоциональный контекст, применяем веса
        if emotional_context and 'dominant_emotion' in emotional_context:
            emotion = emotional_context['dominant_emotion']
            intensity = emotional_context.get('intensity', 1.0)
            
            # Пример: усиление внимания на основе эмоциональной значимости
            emotional_weight = 1 + self.alpha * intensity
            if isinstance(attention_mask, list):
                attention_mask = [x * emotional_weight for x in attention_mask]
            else:
                attention_mask = attention_mask.astype(float) * emotional_weight
            
        return attention_mask

    def _calculate_dynamic_temperature(self, emotional_context):
        """
        Расчет динамической температуры на основе эмоционального состояния
        """
        base_temp = self.base_temperature
        
        if emotional_context and 'arousal' in emotional_context:
            arousal = emotional_context['arousal']
            # Температура увеличивается с уровнем возбуждения
            dynamic_temp = base_temp * (1 + self.beta * arousal)
            # Ограничиваем температуру в разумных пределах
            return max(0.1, min(1.5, dynamic_temp))
        
        return base_temp

    def update_emotional_weights(self, emotional_state: Dict[str, Any]):
        """
        Обновление эмоциональных весов для механизма внимания
        """
        self.emotional_weights = emotional_state

    def get_context_metrics(self) -> Dict[str, Any]:
        """
        Получение метрик контекста
        """
        return {
            "max_context_length": self.max_context_length,
            "current_device": str(self.device),
            "model_parameters": self.model.num_parameters() if hasattr(self.model, 'num_parameters') else 0,
            "emotional_weights_count": len(self.emotional_weights)
        }