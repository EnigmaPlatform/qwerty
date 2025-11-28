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


class NeuralLanguageCore:
    def __init__(self, model_path: str):
        """
        Инициализация языкового ядра с моделью FRED-T5-large
        """
        self.model_path = model_path
        
        # Загрузка конфигурации личности Син
        self._load_personality_config()
        
        # Параметры контекста
        self.max_context_length = 8192
        self.emotional_weights = {}
        
        # Параметры генерации
        self.base_temperature = 0.7
        self.alpha = 0.3  # Влияние эмоций на внимание
        self.beta = 0.2   # Влияние возбуждения на температуру
        
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
        Загрузка модели и токенизатора (заглушка для работы без тяжелых библиотек)
        """
        print(f"Попытка загрузки модели из: {self.model_path}")
        
        if os.path.exists(self.model_path):
            print(f"Модель найдена в: {self.model_path}")
        else:
            print(f"Директория модели не найдена: {self.model_path}")
    
    def generate_response(self, input_text: str, emotional_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Генерация ответа с учетом эмоционального контекста и персональности Син
        """
        start_time = time.time()
        
        # Генерация ответа с использованием персональности Син
        response = self._generate_syn_response(input_text, emotional_context)
        
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