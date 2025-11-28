"""
Visualization: Визуализация состояний
"""
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Any, List
import json


class Visualization:
    def __init__(self):
        pass

    def plot_emotional_state(self, emotional_data: Dict[str, Any], title: str = "Emotional State"):
        """Визуализация эмоционального состояния"""
        if 'superposition_state' in emotional_data:
            emotions = list(emotional_data['superposition_state']['emotions'].keys())
            values = list(emotional_data['superposition_state']['emotions'].values())
        else:
            # Если есть только доминирующая эмоция
            emotions = [emotional_data.get('dominant_emotion', 'unknown')]
            values = [emotional_data.get('intensity', 0.5)]
        
        plt.figure(figsize=(12, 6))
        y_pos = np.arange(len(emotions))
        
        plt.bar(y_pos, values, align='center', alpha=0.7)
        plt.xticks(y_pos, emotions, rotation=45)
        plt.ylabel('Intensity')
        plt.title(title)
        plt.tight_layout()
        plt.show()

    def plot_neurotransmitter_levels(self, nt_levels: Dict[str, float], title: str = "Neurotransmitter Levels"):
        """Визуализация уровней нейротрансмиттеров"""
        neurotransmitters = list(nt_levels.keys())
        values = list(nt_levels.values())
        
        plt.figure(figsize=(10, 6))
        y_pos = np.arange(len(neurotransmitters))
        
        plt.bar(y_pos, values, align='center', alpha=0.7)
        plt.xticks(y_pos, neurotransmitters)
        plt.ylabel('Level')
        plt.title(title)
        plt.ylim(0, 1)
        plt.tight_layout()
        plt.show()

    def plot_cognitive_load(self, cognitive_data: Dict[str, Any], title: str = "Cognitive Load"):
        """Визуализация когнитивной нагрузки"""
        if 'working_memory_load' in cognitive_data:
            load = cognitive_data['working_memory_load']
            labels = ['Used', 'Available']
            sizes = [load, 1 - load]
            colors = ['red', 'lightgreen']
            
            plt.figure(figsize=(8, 8))
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
            plt.title(title)
            plt.show()
        else:
            print("No cognitive load data available")

    def plot_system_metrics(self, metrics: Dict[str, Any], title: str = "System Metrics"):
        """Визуализация системных метрик"""
        kpi_names = list(metrics.get('kpi_averages', {}).keys())
        kpi_values = list(metrics.get('kpi_averages', {}).values())
        
        if kpi_values:
            plt.figure(figsize=(12, 6))
            y_pos = np.arange(len(kpi_names))
            
            plt.bar(y_pos, kpi_values, align='center', alpha=0.7)
            plt.xticks(y_pos, kpi_names, rotation=45)
            plt.ylabel('Value')
            plt.title(title)
            plt.tight_layout()
            plt.show()
        else:
            print("No KPI data available")

    def plot_learning_progress(self, skill_progressions: Dict[str, Any], title: str = "Learning Progress"):
        """Визуализация прогресса в обучении"""
        for skill, data in skill_progressions.items():
            if 'improvement_history' in data and data['improvement_history']:
                timestamps = [entry['timestamp'] for entry in data['improvement_history']]
                levels = [entry['new_level'] for entry in data['improvement_history']]
                
                plt.figure(figsize=(10, 6))
                plt.plot(timestamps, levels, marker='o')
                plt.title(f"{title} - {skill}")
                plt.xlabel('Time')
                plt.ylabel('Skill Level')
                plt.grid(True)
                plt.show()