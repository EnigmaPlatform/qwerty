"""
ConfigLoader: Загрузчик конфигураций
"""
import yaml
import json
import os
from typing import Dict, Any


class ConfigLoader:
    @staticmethod
    def load_all_configs(base_path: str) -> Dict[str, Any]:
        """Загрузка всех конфигурационных файлов"""
        configs = {}
        
        # Загрузка основной конфигурации системы
        system_config_path = os.path.join(base_path, 'configs', 'system_config.yaml')
        if os.path.exists(system_config_path):
            with open(system_config_path, 'r', encoding='utf-8') as f:
                configs['system'] = yaml.safe_load(f)
        else:
            # Значения по умолчанию
            configs['system'] = {
                'modules': {
                    'neural_language_core': {'enabled': True},
                    'emotional_quantum_field': {'enabled': True},
                    'neurotransmitter_network': {'enabled': True}
                }
            }
        
        # Загрузка конфигурации эмоций
        emotion_config_path = os.path.join(base_path, 'configs', 'emotion_config.json')
        if os.path.exists(emotion_config_path):
            with open(emotion_config_path, 'r', encoding='utf-8') as f:
                configs['emotion'] = json.load(f)
        
        # Загрузка конфигурации личности
        personality_config_path = os.path.join(base_path, 'configs', 'personality_config.json')
        if os.path.exists(personality_config_path):
            with open(personality_config_path, 'r', encoding='utf-8') as f:
                configs['personality'] = json.load(f)
        
        # Сбор значений по умолчанию для инициализации модулей
        configs['neurotransmitter_initial'] = {
            'dopamine': 0.5,
            'serotonin': 0.6,
            'norepinephrine': 0.4,
            'gaba': 0.5,
            'acetylcholine': 0.5,
            'endorphins': 0.3,
            'oxytocin': 0.4
        }
        
        configs['initial_identity'] = configs.get('personality', {
            'identity_traits': {
                'openness': 0.8,
                'conscientiousness': 0.7,
                'extraversion': 0.6,
                'agreeableness': 0.9,
                'neuroticism': 0.4
            }
        })
        
        configs['working_memory_capacity'] = 7
        
        return configs