"""
WorldModel: Модель мира
"""
from typing import Dict, Any, List
import numpy as np
import time


class WorldModel:
    def __init__(self):
        """
        Инициализация модели мира
        """
        # Компоненты модели мира
        self.world_components = {
            'physical_model': {},      # Физическая модель мира
            'social_model': {},        # Социальная модель
            'conceptual_model': {},    # Концептуальная модель
            'temporal_model': {},      # Временная модель
            'causal_model': {}         # Причинно-следственная модель
        }
        
        # Объекты и сущности в мире
        self.entities = {}
        
        # Отношения между сущностями
        self.relations = {}
        
        # События в мире
        self.events = []
        
        # Пространственная модель
        self.spatial_model = {
            'layout': {},
            'distances': {},
            'boundaries': {}
        }
        
        # Временные шкалы
        self.temporal_scales = {
            'micro': 0.1,    # миллисекунды
            'short': 1.0,    # секунды
            'medium': 60.0,  # минуты
            'long': 3600.0   # часы
        }
        
        # Уровни абстракции
        self.abstraction_levels = {
            'concrete': 0.9,    # Конкретный уровень
            'abstract': 0.7,    # Абстрактный уровень
            'symbolic': 0.5,    # Символический уровень
            'conceptual': 0.3   # Концептуальный уровень
        }
        
        # Параметры модели
        self.model_accuracy = 0.8
        self.update_frequency = 1.0  # раз в секунду
        self.prediction_horizon = 10.0  # на 10 секунд вперед
        self.uncertainty_tolerance = 0.2

    def update_world_state(self, sensory_input: Dict[str, Any], 
                          action_outcome: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Обновление состояния модели мира на основе сенсорных данных и результатов действий
        """
        current_time = time.time()
        
        # Обработка сенсорного ввода
        processed_sensory = self._process_sensory_input(sensory_input, current_time)
        
        # Обновление физической модели
        self._update_physical_model(processed_sensory)
        
        # Обновление социальной модели
        self._update_social_model(processed_sensory)
        
        # Обновление концептуальной модели
        self._update_conceptual_model(processed_sensory)
        
        # Обновление причинно-следственной модели
        if action_outcome:
            self._update_causal_model(action_outcome)
        
        # Обновление временной модели
        self._update_temporal_model(current_time)
        
        # Обработка событий
        detected_events = self._process_events(processed_sensory, current_time)
        
        # Предсказание будущего состояния
        predictions = self._predict_future_states(current_time)
        
        return {
            'current_state': self._get_current_world_state(),
            'predictions': predictions,
            'detected_events': detected_events,
            'model_confidence': self._calculate_model_confidence(),
            'update_timestamp': current_time
        }

    def _process_sensory_input(self, sensory_input: Dict[str, Any], 
                              timestamp: float) -> Dict[str, Any]:
        """
        Обработка сенсорного ввода
        """
        processed = {}
        
        # Обработка визуальных данных
        if 'visual' in sensory_input:
            processed['visual'] = self._process_visual_input(sensory_input['visual'])
        
        # Обработка аудио данных
        if 'audio' in sensory_input:
            processed['audio'] = self._process_audio_input(sensory_input['audio'])
        
        # Обработка тактильных данных
        if 'tactile' in sensory_input:
            processed['tactile'] = self._process_tactile_input(sensory_input['tactile'])
        
        # Обработка других сенсорных данных
        for key, value in sensory_input.items():
            if key not in ['visual', 'audio', 'tactile']:
                processed[key] = value
        
        processed['timestamp'] = timestamp
        return processed

    def _process_visual_input(self, visual_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обработка визуальных данных
        """
        # Детекция объектов
        objects = visual_data.get('objects', [])
        
        processed_objects = []
        for obj in objects:
            processed_obj = {
                'id': obj.get('id'),
                'type': obj.get('type', 'unknown'),
                'position': obj.get('position', [0, 0, 0]),
                'size': obj.get('size', [1, 1, 1]),
                'state': obj.get('state', 'static'),
                'properties': obj.get('properties', {})
            }
            processed_objects.append(processed_obj)
        
        return {
            'objects': processed_objects,
            'scene_description': visual_data.get('scene_description', ''),
            'spatial_layout': visual_data.get('spatial_layout', {})
        }

    def _process_audio_input(self, audio_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обработка аудио данных
        """
        return {
            'sounds': audio_data.get('sounds', []),
            'speech_content': audio_data.get('speech', ''),
            'volume_level': audio_data.get('volume', 0.5),
            'direction': audio_data.get('direction', [0, 0, 1])
        }

    def _process_tactile_input(self, tactile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обработка тактильных данных
        """
        return {
            'pressure': tactile_data.get('pressure', 0.0),
            'temperature': tactile_data.get('temperature', 20.0),
            'texture': tactile_data.get('texture', 'smooth'),
            'location': tactile_data.get('location', [0, 0, 0])
        }

    def _update_physical_model(self, processed_sensory: Dict[str, Any]):
        """
        Обновление физической модели мира
        """
        if 'visual' in processed_sensory:
            visual_data = processed_sensory['visual']
            
            # Обновление объектов в физической модели
            for obj in visual_data['objects']:
                obj_id = obj['id']
                
                if obj_id not in self.entities:
                    self.entities[obj_id] = {
                        'type': obj['type'],
                        'position_history': [obj['position']],
                        'velocity': [0, 0, 0],
                        'properties': obj['properties']
                    }
                else:
                    # Обновление истории позиций для вычисления скорости
                    old_pos = self.entities[obj_id]['position_history'][-1]
                    new_pos = obj['position']
                    dt = 1.0  # условное время между обновлениями
                    
                    velocity = [(new_pos[i] - old_pos[i]) / dt for i in range(3)]
                    
                    self.entities[obj_id]['position_history'].append(new_pos)
                    self.entities[obj_id]['velocity'] = velocity
                    
                    # Ограничение длины истории
                    if len(self.entities[obj_id]['position_history']) > 10:
                        self.entities[obj_id]['position_history'] = \
                            self.entities[obj_id]['position_history'][-10:]

    def _update_social_model(self, processed_sensory: Dict[str, Any]):
        """
        Обновление социальной модели
        """
        # Обработка аудио для определения социальных взаимодействий
        if 'audio' in processed_sensory:
            speech_content = processed_sensory['audio'].get('speech_content', '')
            
            # Простая обработка речи для социальной модели
            if speech_content:
                self.world_components['social_model']['last_utterance'] = speech_content
                self.world_components['social_model']['communication_active'] = True
            else:
                self.world_components['social_model']['communication_active'] = False

    def _update_conceptual_model(self, processed_sensory: Dict[str, Any]):
        """
        Обновление концептуальной модели
        """
        # Обновление на основе визуальных и аудио данных
        if 'visual' in processed_sensory:
            scene_desc = processed_sensory['visual'].get('scene_description', '')
            if scene_desc:
                # Простое обновление концептуальной модели
                if 'concepts' not in self.world_components['conceptual_model']:
                    self.world_components['conceptual_model']['concepts'] = {}
                
                # Здесь в реальности происходило бы сложное концептуальное понимание
                self.world_components['conceptual_model']['current_scene'] = scene_desc

    def _update_causal_model(self, action_outcome: Dict[str, Any]):
        """
        Обновление причинно-следственной модели
        """
        action = action_outcome.get('action', 'unknown')
        outcome = action_outcome.get('outcome', 'unknown')
        context = action_outcome.get('context', {})
        
        # Создание или обновление причинно-следственной связи
        if action not in self.world_components['causal_model']:
            self.world_components['causal_model'][action] = []
        
        causal_link = {
            'outcome': outcome,
            'context': context,
            'frequency': 1,
            'reliability': 0.5,  # начальная надежность
            'timestamp': time.time()
        }
        
        # Проверка, существует ли уже такая связь
        existing_link = None
        for link in self.world_components['causal_model'][action]:
            if (link['outcome'] == outcome and 
                link['context'] == context):
                existing_link = link
                break
        
        if existing_link:
            # Обновление существующей связи
            existing_link['frequency'] += 1
            # Обновление надежности на основе частоты
            total_attempts = sum(l['frequency'] for l in 
                              self.world_components['causal_model'][action])
            existing_link['reliability'] = existing_link['frequency'] / total_attempts
        else:
            # Добавление новой связи
            self.world_components['causal_model'][action].append(causal_link)

    def _update_temporal_model(self, timestamp: float):
        """
        Обновление временной модели
        """
        self.world_components['temporal_model']['current_time'] = timestamp
        
        # Обновление временных шкал
        if 'events' not in self.world_components['temporal_model']:
            self.world_components['temporal_model']['events'] = []
        
        # Добавление временного маркера
        self.world_components['temporal_model']['events'].append({
            'timestamp': timestamp,
            'event_type': 'world_update'
        })

    def _process_events(self, processed_sensory: Dict[str, Any], 
                       timestamp: float) -> List[Dict[str, Any]]:
        """
        Обработка и определение событий в мире
        """
        detected_events = []
        
        # Обнаружение изменений в визуальных данных
        if 'visual' in processed_sensory:
            objects = processed_sensory['visual'].get('objects', [])
            
            for obj in objects:
                # Проверка, является ли объект новым или изменившимся
                obj_id = obj['id']
                
                if obj_id not in self.entities:
                    detected_events.append({
                        'type': 'object_appeared',
                        'object_id': obj_id,
                        'timestamp': timestamp
                    })
                else:
                    # Проверка движения объекта
                    old_pos = self.entities[obj_id]['position_history'][-2] if len(self.entities[obj_id]['position_history']) > 1 else obj['position']
                    new_pos = obj['position']
                    
                    distance_moved = np.sqrt(sum((new_pos[i] - old_pos[i])**2 for i in range(3)))
                    
                    if distance_moved > 0.1:  # порог движения
                        detected_events.append({
                            'type': 'object_moved',
                            'object_id': obj_id,
                            'old_position': old_pos,
                            'new_position': new_pos,
                            'distance': distance_moved,
                            'timestamp': timestamp
                        })
        
        # Добавление событий в историю
        for event in detected_events:
            self.events.append(event)
        
        # Ограничение истории событий
        if len(self.events) > 100:
            self.events = self.events[-50:]
        
        return detected_events

    def _predict_future_states(self, current_time: float) -> Dict[str, Any]:
        """
        Предсказание будущих состояний мира
        """
        predictions = {
            'physical_predictions': {},
            'social_predictions': {},
            'conceptual_predictions': {},
            'temporal_predictions': {},
            'causal_predictions': {}
        }
        
        # Физические предсказания (движение объектов)
        for obj_id, obj_data in self.entities.items():
            if len(obj_data['position_history']) >= 2:
                # Предсказание следующей позиции на основе текущей скорости
                current_pos = obj_data['position_history'][-1]
                velocity = obj_data['velocity']
                
                # Простое кинематическое предсказание
                dt = self.prediction_horizon
                predicted_pos = [current_pos[i] + velocity[i] * dt for i in range(3)]
                
                predictions['physical_predictions'][obj_id] = {
                    'predicted_position': predicted_pos,
                    'confidence': 0.8  # простая уверенность
                }
        
        # Социальные предсказания (основанные на текущем состоянии)
        if self.world_components['social_model'].get('communication_active', False):
            predictions['social_predictions']['response_expected'] = True
            predictions['social_predictions']['expected_response_time'] = 2.0
        
        return predictions

    def _get_current_world_state(self) -> Dict[str, Any]:
        """
        Получение текущего состояния модели мира
        """
        return {
            'entities': self.entities.copy(),
            'relations': self.relations.copy(),
            'spatial_model': self.spatial_model.copy(),
            'world_components': self.world_components.copy(),
            'model_accuracy': self.model_accuracy,
            'abstraction_levels': self.abstraction_levels.copy()
        }

    def _calculate_model_confidence(self) -> float:
        """
        Расчет уверенности в модели мира
        """
        # Уверенность зависит от согласованности наблюдений
        if not self.events:
            return 0.5  # нейтральная уверенность
        
        # Простая метрика: отношение последовательных согласованных наблюдений
        recent_events = self.events[-10:] if len(self.events) >= 10 else self.events
        
        # В реальности это было бы сложнее - анализ причинно-следственных связей
        consistency_score = len(recent_events) / 10 if len(self.events) >= 10 else len(self.events) / 10
        return min(1.0, consistency_score)

    def query_world(self, query_type: str, query_params: Dict[str, Any]) -> Any:
        """
        Запрос к модели мира
        """
        if query_type == 'entity_state':
            entity_id = query_params.get('entity_id')
            return self.entities.get(entity_id, None)
        
        elif query_type == 'spatial_relationship':
            entity1 = query_params.get('entity1')
            entity2 = query_params.get('entity2')
            return self._get_spatial_relationship(entity1, entity2)
        
        elif query_type == 'causal_relationship':
            action = query_params.get('action')
            return self.world_components['causal_model'].get(action, [])
        
        elif query_type == 'prediction':
            entity_id = query_params.get('entity_id')
            predictions = self._predict_future_states(time.time())
            return predictions['physical_predictions'].get(entity_id, None)
        
        else:
            return None

    def _get_spatial_relationship(self, entity1: str, entity2: str) -> Dict[str, Any]:
        """
        Получение пространственной связи между сущностями
        """
        if entity1 not in self.entities or entity2 not in self.entities:
            return {'relationship': 'unknown', 'distance': float('inf')}
        
        pos1 = self.entities[entity1]['position_history'][-1] if self.entities[entity1]['position_history'] else [0, 0, 0]
        pos2 = self.entities[entity2]['position_history'][-1] if self.entities[entity2]['position_history'] else [0, 0, 0]
        
        distance = np.sqrt(sum((pos1[i] - pos2[i])**2 for i in range(3)))
        
        # Определение отношения на основе расстояния
        if distance < 1.0:
            relationship = 'very_close'
        elif distance < 5.0:
            relationship = 'close'
        elif distance < 20.0:
            relationship = 'near'
        else:
            relationship = 'far'
        
        return {
            'relationship': relationship,
            'distance': distance,
            'position1': pos1,
            'position2': pos2
        }

    def update_beliefs_about_world(self, new_knowledge: Dict[str, Any]):
        """
        Обновление убеждений о мире на основе новой информации
        """
        # Обновление компонентов модели мира
        for component, updates in new_knowledge.items():
            if component in self.world_components:
                self.world_components[component].update(updates)
        
        # Обновление параметров модели
        if 'model_accuracy' in new_knowledge:
            self.model_accuracy = new_knowledge['model_accuracy']
        
        if 'prediction_horizon' in new_knowledge:
            self.prediction_horizon = new_knowledge['prediction_horizon']

    def get_world_summary(self) -> Dict[str, Any]:
        """
        Получение сводки о модели мира
        """
        return {
            'entity_count': len(self.entities),
            'event_count': len(self.events),
            'model_accuracy': self.model_accuracy,
            'prediction_horizon': self.prediction_horizon,
            'temporal_extent': self._get_temporal_extent(),
            'spatial_extent': self._get_spatial_extent(),
            'causal_complexity': self._calculate_causal_complexity()
        }

    def _get_temporal_extent(self) -> float:
        """
        Получение временного охвата модели
        """
        if not self.events:
            return 0.0
        
        start_time = self.events[0]['timestamp']
        end_time = self.events[-1]['timestamp']
        return end_time - start_time

    def _get_spatial_extent(self) -> Dict[str, float]:
        """
        Получение пространственного охвата модели
        """
        if not self.entities:
            return {'min_x': 0, 'max_x': 0, 'min_y': 0, 'max_y': 0, 'min_z': 0, 'max_z': 0}
        
        all_positions = []
        for entity_data in self.entities.values():
            if entity_data['position_history']:
                all_positions.extend(entity_data['position_history'])
        
        if not all_positions:
            return {'min_x': 0, 'max_x': 0, 'min_y': 0, 'max_y': 0, 'min_z': 0, 'max_z': 0}
        
        xs = [pos[0] for pos in all_positions]
        ys = [pos[1] for pos in all_positions]
        zs = [pos[2] for pos in all_positions]
        
        return {
            'min_x': min(xs), 'max_x': max(xs),
            'min_y': min(ys), 'max_y': max(ys),
            'min_z': min(zs), 'max_z': max(zs)
        }

    def _calculate_causal_complexity(self) -> int:
        """
        Расчет сложности причинно-следственной модели
        """
        total_relations = 0
        for action, relations in self.world_components['causal_model'].items():
            total_relations += len(relations)
        return total_relations