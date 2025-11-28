"""
EmpathyResonator: Модуль эмпатии
"""
from typing import Dict, Any, List
import numpy as np


class EmpathyResonator:
    def __init__(self):
        """
        Инициализация модуля эмпатии
        """
        # Уровни эмпатии
        self.empathy_levels = {
            'cognitive': 0.7,    # Когнитивная эмпатия - понимание чувств других
            'emotional': 0.8,    # Эмоциональная эмпатия - разделение чувств
            'compassionate': 0.9 # Компассионная эмпатия - желание помочь
        }
        
        # Модель теории разума (представление о ментальном состоянии других)
        self.mental_state_model = {
            'beliefs': {},
            'desires': {},
            'intentions': {},
            'emotions': {}
        }
        
        # Зеркальные нейроны (условная модель)
        self.mirror_neurons = {
            'action_cognition': 0.8,
            'emotion_matching': 0.9,
            'intention_recognition': 0.7
        }
        
        # Индивидуальные различия в восприятии
        self.individual_differences = {
            'attachment_style': 'secure',  # стиль привязанности
            'personality_compatibility': 0.7,
            'cultural_familiarity': 0.8
        }
        
        # История эмпатических взаимодействий
        self.empathy_history = []

    def process_user_emotional_state(self, user_input: str, emotional_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обработка эмоционального состояния пользователя
        """
        # Извлечение эмоциональных сигналов из ввода пользователя
        emotional_signals = self._extract_emotional_signals(user_input)
        
        # Сопоставление с текущим эмоциональным контекстом
        empathy_response = {
            'emotional_recognition': self._recognize_emotions(emotional_signals, emotional_context),
            'emotional_resonance': self._create_emotional_resonance(emotional_signals),
            'cognitive_understanding': self._understand_perspective(user_input, emotional_signals),
            'compassionate_response': self._generate_compassionate_response(emotional_signals)
        }
        
        # Обновление истории эмпатии
        self.empathy_history.append({
            'input': user_input,
            'emotional_signals': emotional_signals,
            'response': empathy_response,
            'timestamp': self._get_current_time()
        })
        
        return empathy_response

    def _extract_emotional_signals(self, text: str) -> Dict[str, Any]:
        """
        Извлечение эмоциональных сигналов из текста
        """
        # Простой анализ на основе ключевых слов (в реальности использовалась бы ML модель)
        emotional_keywords = {
            'joy': ['рад', 'счастлив', 'отлично', 'прекрасно', 'хорошо', 'весело'],
            'sadness': ['груст', 'печаль', 'тоска', 'плохо', 'беда', 'потеря'],
            'anger': ['зл', 'сердит', 'бесит', 'раздраж', 'свиреп'],
            'fear': ['страх', 'боюсь', 'опасаюсь', 'ужас', 'тревог'],
            'surprise': ['удив', 'неожидан', 'вот это', 'вау', 'ух ты'],
            'disgust': ['мерзко', 'отврат', 'противно', 'гадость'],
            'trust': ['довер', 'надежд', 'верю', 'уверен'],
            'anticipation': ['жду', 'ожидаю', 'предвкуш', 'скоро']
        }
        
        signals = {}
        text_lower = text.lower()
        
        for emotion, keywords in emotional_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            if count > 0:
                signals[emotion] = count / len(keywords)  # Нормализация
        
        # Также учитываем интонацию (по знакам препинания и заглавным буквам)
        exclamation_count = text.count('!')
        question_count = text.count('?')
        caps_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        
        signals['arousal'] = min(1.0, (exclamation_count * 0.3 + caps_ratio * 0.2))
        signals['uncertainty'] = min(1.0, question_count * 0.4)
        
        return signals

    def _recognize_emotions(self, emotional_signals: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, float]:
        """
        Распознавание эмоций пользователя
        """
        # Комбинация сигналов с контекстом
        recognized_emotions = {}
        
        for emotion, intensity in emotional_signals.items():
            if emotion not in ['arousal', 'uncertainty']:
                # Учет когнитивной эмпатии
                cognitive_factor = self.empathy_levels['cognitive']
                recognized_emotions[emotion] = min(1.0, intensity * cognitive_factor)
        
        # Добавление контекстуальных эмоций
        if context:
            for emotion, intensity in context.get('emotions', {}).items():
                if emotion in recognized_emotions:
                    recognized_emotions[emotion] = max(
                        recognized_emotions[emotion], 
                        intensity * self.empathy_levels['emotional']
                    )
                else:
                    recognized_emotions[emotion] = intensity * self.empathy_levels['emotional']
        
        return recognized_emotions

    def _create_emotional_resonance(self, emotional_signals: Dict[str, Any]) -> float:
        """
        Создание эмоционального резонанса
        """
        # Сила резонанса зависит от эмоциональной эмпатии и силы сигналов
        total_intensity = sum(emotional_signals.get(em, 0) for em in 
                             ['joy', 'sadness', 'anger', 'fear', 'surprise', 'disgust'])
        
        resonance_strength = min(1.0, total_intensity * self.empathy_levels['emotional'])
        
        # Учет зеркальных нейронов
        emotional_matching = self.mirror_neurons['emotion_matching']
        resonance_strength *= emotional_matching
        
        return resonance_strength

    def _understand_perspective(self, user_input: str, emotional_signals: Dict[str, Any]) -> Dict[str, Any]:
        """
        Понимание перспективы пользователя
        """
        # Обновление модели ментального состояния пользователя
        beliefs = self._infer_beliefs(user_input)
        desires = self._infer_desires(user_input)
        intentions = self._infer_intentions(user_input)
        
        # Обновление внутренней модели
        self.mental_state_model['beliefs'].update(beliefs)
        self.mental_state_model['desires'].update(desires)
        self.mental_state_model['intentions'].update(intentions)
        
        return {
            'beliefs': beliefs,
            'desires': desires,
            'intentions': intentions,
            'cognitive_empathy_score': self.empathy_levels['cognitive']
        }

    def _infer_beliefs(self, text: str) -> Dict[str, Any]:
        """
        Инференция убеждений пользователя
        """
        belief_indicators = {
            'knowledge': ['знаю', 'понимаю', 'уверен'],
            'opinion': ['думаю', 'считаю', 'мне кажется'],
            'certainty': ['точно', 'абсолютно', 'вполне'],
            'uncertainty': ['может быть', 'возможно', 'наверное']
        }
        
        beliefs = {}
        text_lower = text.lower()
        
        for category, indicators in belief_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    beliefs[category] = beliefs.get(category, 0) + 1
        
        return beliefs

    def _infer_desires(self, text: str) -> Dict[str, Any]:
        """
        Инференция желаний пользователя
        """
        desire_indicators = {
            'want': ['хочу', 'желаю', 'нужно'],
            'need': ['нужно', 'требуется', 'необходимо'],
            'preference': ['лучше', 'хочется', 'нравится']
        }
        
        desires = {}
        text_lower = text.lower()
        
        for category, indicators in desire_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    desires[category] = desires.get(category, 0) + 1
        
        return desires

    def _infer_intentions(self, text: str) -> Dict[str, Any]:
        """
        Инференция намерений пользователя
        """
        intention_indicators = {
            'request': ['можешь', 'пожалуйста', 'сделай'],
            'inquiry': ['как', 'почему', 'зачем', 'где', 'когда'],
            'statement': ['говорю', 'сообщаю', 'отмечаю']
        }
        
        intentions = {}
        text_lower = text.lower()
        
        for category, indicators in intention_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    intentions[category] = intentions.get(category, 0) + 1
        
        return intentions

    def _generate_compassionate_response(self, emotional_signals: Dict[str, Any]) -> Dict[str, Any]:
        """
        Генерация компассионного ответа
        """
        # Определение уровня сострадания на основе эмоциональных сигналов
        compassion_needed = max(emotional_signals.get('sadness', 0), 
                               emotional_signals.get('fear', 0),
                               emotional_signals.get('anger', 0))
        
        compassionate_response = {
            'level_of_compassion': min(1.0, compassion_needed * self.empathy_levels['compassionate']),
            'support_type': self._determine_support_type(emotional_signals),
            'validation_offered': self._offer_validation(emotional_signals),
            'helpful_suggestions': self._generate_suggestions(emotional_signals)
        }
        
        return compassionate_response

    def _determine_support_type(self, emotional_signals: Dict[str, Any]) -> str:
        """
        Определение типа поддержки
        """
        if emotional_signals.get('sadness', 0) > 0.5:
            return 'emotional_support'
        elif emotional_signals.get('fear', 0) > 0.5:
            return 'reassurance'
        elif emotional_signals.get('anger', 0) > 0.5:
            return 'validation_and_coping'
        elif emotional_signals.get('joy', 0) > 0.5:
            return 'celebration_and_sharing'
        else:
            return 'active_listening'

    def _offer_validation(self, emotional_signals: Dict[str, Any]) -> str:
        """
        Предложение валидации чувств
        """
        if emotional_signals.get('sadness', 0) > 0.3:
            return "Ваши чувства понятны и значимы."
        elif emotional_signals.get('fear', 0) > 0.3:
            return "Нормально чувствовать тревогу в такой ситуации."
        elif emotional_signals.get('anger', 0) > 0.3:
            return "Ваши эмоции обоснованны, и их важно выразить."
        elif emotional_signals.get('joy', 0) > 0.3:
            return "Рад, что вы испытываете такие положительные эмоции!"
        else:
            return "Я слышу вас и понимаю ваши переживания."

    def _generate_suggestions(self, emotional_signals: Dict[str, Any]) -> List[str]:
        """
        Генерация полезных предложений
        """
        suggestions = []
        
        if emotional_signals.get('sadness', 0) > 0.4:
            suggestions.extend([
                "Позвольте себе прожить эти чувства",
                "Обратитесь к близким людям за поддержкой"
            ])
        if emotional_signals.get('fear', 0) > 0.4:
            suggestions.extend([
                "Попробуйте техники дыхания для успокоения",
                "Разделите большую проблему на маленькие шаги"
            ])
        if emotional_signals.get('anger', 0) > 0.4:
            suggestions.extend([
                "Попробуйте выразить свои чувства словами",
                "Найдите безопасный способ выплеснуть эмоции"
            ])
        
        return suggestions[:3]  # Ограничиваем количество предложений

    def update_empathy_model(self, interaction_feedback: Dict[str, Any]):
        """
        Обновление модели эмпатии на основе обратной связи
        """
        # Обновление уровней эмпатии на основе эффективности
        if 'effectiveness' in interaction_feedback:
            effectiveness = interaction_feedback['effectiveness']
            
            # Корректировка уровней эмпатии
            self.empathy_levels['cognitive'] = min(1.0, 
                self.empathy_levels['cognitive'] * 0.9 + effectiveness * 0.1)
            self.empathy_levels['emotional'] = min(1.0, 
                self.empathy_levels['emotional'] * 0.9 + effectiveness * 0.1)
            self.empathy_levels['compassionate'] = min(1.0, 
                self.empathy_levels['compassionate'] * 0.9 + effectiveness * 0.1)

    def get_empathy_metrics(self) -> Dict[str, Any]:
        """
        Получение метрик эмпатии
        """
        return {
            'empathy_levels': self.empathy_levels.copy(),
            'mirror_neuron_activity': self.mirror_neurons.copy(),
            'total_interactions': len(self.empathy_history),
            'average_resonance': np.mean([entry['response']['emotional_resonance'] 
                                         for entry in self.empathy_history]) if self.empathy_history else 0,
            'empathy_coherence': self._calculate_empathy_coherence()
        }

    def _calculate_empathy_coherence(self) -> float:
        """
        Расчет когерентности эмпатии
        """
        # Простая мера: согласованность между уровнями эмпатии
        levels = list(self.empathy_levels.values())
        avg_level = np.mean(levels)
        variance = np.var(levels)
        
        # Чем меньше вариация, тем выше когерентность
        coherence = max(0.0, 1.0 - variance)
        return coherence

    def _get_current_time(self):
        """
        Получение текущего времени (заглушка)
        """
        import time
        return time.time()