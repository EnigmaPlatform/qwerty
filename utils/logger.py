"""
SystemLogger: Система логгирования
"""
import logging
import os
import json
from datetime import datetime
from typing import Dict, Any


class SystemLogger:
    def __init__(self, log_directory: str = "logs/"):
        self.log_directory = log_directory
        os.makedirs(log_directory, exist_ok=True)
        
        # Настройка стандартного логгера
        self.logger = logging.getLogger('EmotionalAI')
        self.logger.setLevel(logging.INFO)
        
        # Создание обработчика для файла
        log_file = os.path.join(log_directory, f"emotional_ai_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Форматирование
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        # Добавление обработчика к логгеру
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
        
        # Также сохраняем в JSON формате для структурированного логгирования
        self.json_log_file = os.path.join(log_directory, f"emotional_ai_structured_{datetime.now().strftime('%Y%m%d')}.json")
    
    def log_system_event(self, event_type: str, message: str, extra_data: Dict[str, Any] = None):
        """Логирование системного события"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'message': message,
            'extra_data': extra_data or {}
        }
        
        # Логгирование в стандартный лог
        self.logger.info(f"[{event_type}] {message}")
        
        # Логгирование в JSON файл
        with open(self.json_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def log_module_event(self, module_name: str, level: str, message: str, metrics: Dict[str, Any] = None):
        """Логирование события модуля"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'module': module_name,
            'level': level,
            'message': message,
            'metrics': metrics or {}
        }
        
        # Логгирование в стандартный лог
        self.logger.log(getattr(logging, level.upper(), logging.INFO), 
                       f"[{module_name}] {message}")
        
        # Логгирование в JSON файл
        with open(self.json_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def get_system_health(self) -> Dict[str, Any]:
        """Получение информации о здоровье системы"""
        return {
            'logger_status': 'active',
            'log_directory': self.log_directory,
            'current_log_file': self.json_log_file,
            'log_count': self._count_logs()
        }
    
    def _count_logs(self) -> int:
        """Подсчет количества логов"""
        try:
            with open(self.json_log_file, 'r', encoding='utf-8') as f:
                return sum(1 for line in f)
        except FileNotFoundError:
            return 0
    
    def export_logs(self, time_range: tuple) -> list:
        """Экспорт логов за определенный период"""
        logs = []
        try:
            with open(self.json_log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    log_entry = json.loads(line.strip())
                    logs.append(log_entry)
        except FileNotFoundError:
            pass
        
        return logs