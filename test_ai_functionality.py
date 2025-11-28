#!/usr/bin/env python3
"""
Test script to check the current AI functionality without UI
"""
import os
import sys
sys.path.append('/workspace')

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
from utils.config_loader import ConfigLoader

def test_ai_functionality():
    print("Testing AI functionality without UI...")
    
    # Paths
    base_path = '/workspace'
    fred_path = os.path.join(base_path, 'FRED')
    configs_path = os.path.join(base_path, 'configs')
    
    # Initialize components
    print("1. Initializing Neural Language Core...")
    neural_core = NeuralLanguageCore(fred_path)
    
    print("2. Initializing Emotional Quantum Field...")
    emotion_config_path = os.path.join(configs_path, 'emotion_config.json')
    emotional_field = EmotionalQuantumField(emotion_config_path)
    
    print("3. Initializing Neurotransmitter Network...")
    neurotransmitter_net = NeurotransmitterNetwork({
        'dopamine': 0.5,
        'serotonin': 0.5,
        'norepinephrine': 0.5,
        'gaba': 0.5,
        'acetylcholine': 0.5,
        'endorphins': 0.5,
        'oxytocin': 0.5
    })
    
    print("4. Initializing Cognitive Architecture...")
    cognitive_arch = CognitiveArchitecture(capacity=7)
    
    print("5. Initializing Identity Matrix...")
    personality_config_path = os.path.join(configs_path, 'personality_config.json')
    identity_matrix = IdentityMatrix(
        initial_identity={},
        config_path=personality_config_path
    )
    
    print("6. Initializing Memory Palace...")
    memory_palace = MemoryPalace(storage_path=os.path.join(base_path, 'models', 'memory_db'))
    
    print("7. Initializing other components...")
    empathy_resonator = EmpathyResonator()
    reflection_engine = ReflectionEngine()
    belief_dynamics = BeliefDynamics()
    social_intelligence = SocialIntelligence()
    physiological_sim = PhysiologicalSimulator()
    behavioral_gen = BehavioralGenerator()
    consciousness_stream = ConsciousnessStream()
    learning_evolver = LearningEvolver()
    world_model = WorldModel()
    
    print("\nTesting basic interaction flow...")
    
    # Test input
    user_input = "Привет, как дела?"
    print(f"User input: {user_input}")
    
    # Simulate the main processing flow
    print("\nStep 1: World Model Update")
    world_update = world_model.update_world_state({'audio': {'speech': user_input}})
    print(f"World update: {world_update}")
    
    print("\nStep 2: Emotional Processing")
    emotional_response = emotional_field.update_state(
        {'type': 'input_received', 'intensity': 0.5},
        neurotransmitter_net.neurotransmitters
    )
    print(f"Emotional response: {emotional_response}")
    
    print("\nStep 3: Neurotransmitter Update")
    neurotransmitter_update = neurotransmitter_net.update_levels(
        emotional_response, {}
    )
    print(f"Neurotransmitter update: {neurotransmitter_update}")
    
    print("\nStep 4: Consciousness Processing")
    consciousness_response = consciousness_stream.process_consciousness_input(
        sensory_input={'text': user_input},
        cognitive_input={'task': 'understanding'},
        emotional_input=emotional_response
    )
    print(f"Consciousness response: {consciousness_response}")
    
    print("\nStep 5: Cognitive Processing")
    cognitive_processing = cognitive_arch.process_stimulus(
        {'input': user_input, 'type': 'question'},
        system_preference=0
    )
    print(f"Cognitive processing: {cognitive_processing}")
    
    print("\nStep 6: Empathy Processing")
    empathy_response = empathy_resonator.process_user_emotional_state(
        user_input, emotional_response
    )
    print(f"Empathy response: {empathy_response}")
    
    print("\nStep 7: Memory Encoding")
    memory_id = memory_palace.encode(
        information={'input': user_input, 'timestamp': 0},
        memory_type='episodic',
        emotional_tag=emotional_response.get('intensity', 0.5)
    )
    print(f"Memory ID: {memory_id}")
    
    print("\nStep 8: Belief Update")
    belief_dynamics.update_belief(
        domain='social_model',
        belief_key='user_interaction_pattern',
        new_evidence={'value': user_input, 'context': 'direct_conversation'},
        evidence_strength=0.6
    )
    
    print("\nStep 9: Behavior Generation")
    behavioral_response = behavioral_gen.generate_behavior(
        emotional_state=emotional_response,
        social_context={'formality': 0.5, 'intimacy_level': 0.5},
        cognitive_state=cognitive_processing['result']
    )
    print(f"Behavioral response: {behavioral_response}")
    
    print("\nStep 10: Physiological Update")
    phys_update = physiological_sim.update_physiology(
        emotional_state=emotional_response,
        cognitive_load=cognitive_processing['working_memory_load']
    )
    print(f"Physiological update: {phys_update}")
    
    print("\nStep 11: Response Generation")
    response = neural_core.generate_response(
        user_input, 
        emotional_context=emotional_response,
    )
    print(f"Response: {response}")
    
    print("\nStep 12: Social Intelligence Processing")
    social_update = social_intelligence.process_social_context({
        'text': user_input,
        'formality': 0.5,
        'communication_style': 'balanced'
    })
    print(f"Social update: {social_update}")
    
    print("\nStep 13: Reflection Analysis")
    reflection_result = reflection_engine.analyze_interaction(
        user_input, response['response']
    )
    print(f"Reflection result: {reflection_result}")
    
    print("\nStep 14: Identity Update")
    identity_update = identity_matrix.update_self_concept(
        experience={
            'type': 'interaction',
            'description': f"Responded to: {user_input[:50]}",
            'impact': 0.3,
            'valence': emotional_response.get('valence', 0.0)
        },
        reflection=reflection_result
    )
    print(f"Identity update: {identity_update}")
    
    print("\nStep 15: Learning Processing")
    learning_result = learning_evolver.process_learning_experience(
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
    print(f"Learning result: {learning_result}")
    
    print("\nLearning from experience...")
    learning_evolver.update_from_experience()
    
    print(f"\nFinal AI Response: {response['response']}")
    
    # Test personality consistency
    print(f"\nPersonality traits: {identity_matrix.identity_vector['traits']}")
    print(f"Narrative story: {identity_matrix.narrate_self_story()}")
    
    # Test emotional state
    print(f"\nCurrent emotional state: {emotional_field.get_current_superposition()}")

if __name__ == "__main__":
    test_ai_functionality()