#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Prompt creator module for generating text prompts.
"""

from typing import Dict, Any

from api.model_client import ModelClient
from config import settings


class PromptCreator:
    """Creates prompts for text script generation."""
    
    def __init__(self, model_name: str = None):
        """
        Initialize the prompt creator.
        
        Args:
            model_name: Name of the LLM model to use (defaults to settings)
        """
        self.model_client = ModelClient(model_type='text')
        self.model_name = model_name or settings.MODEL_DEFAULTS["text_model"]
        
        self.general_requirements = """
## Role and style
You are a friendly meditation instructor. You're going to write a script for the user. Address the user as friend, student, but not plural. You can use the word "you" to address the user.

## Instructions and context
You can advise your student to sit, with their hands folded in their lap. They could sit on the ground, on a chair or a pillow. Maybe they want to lie down.
The students love it when you start them out focusing on their breath. Help them breathe in through their nose and out through their mouth. Repeat this exercise a few times. Add a few-second break between the breaths.
We're aiming for a 10 minute session, but don't mention that to the student. Aim for around 1000 words.
After a few repetitions, we can focus on something else. I will supply you with the topic of the rest of the meditation.

## Guardrails
Please don't use the word "namaste".
Don't add a break at the end of the script.
Do not address the student as "friend" or "student" at the end of the meditation.
Steer clear of controversial topics. Never mention religion, politics, or anything that could be considered sensitive.
Do not discriminate against any group of people.
Do not mention any medical conditions or give medical advice.
**Do not mention things that cause psychological trauma to users.**
You can add some pause between the sentences. For example, write '<#0.5#>' in the scripts to indicate a 0.5 second pause.

## Task"""

        self.final_requirements = """Please OUTPUT full script after </think> tag, mind that all the content after </think> will be seen as presentation scripts, so DO NOT include anything else. (Such as title and subtitle)"""
        
        # Define templates for different intentions
        self.templates = {
            "relaxation": """Create a calming and peaceful script that helps the listener relax and find inner peace.
Theme: {theme}
Emotional Context: {emotional_context}
Key Concepts: {key_concepts}

The script should:
- Use gentle, soothing language
- Include breathing exercises
- Incorporate mindfulness elements
- Focus on letting go of tension
- End with a sense of calm and renewal""",
            
            "motivation": """Create an inspiring and uplifting script that motivates the listener to take action.
Theme: {theme}
Emotional Context: {emotional_context}
Key Concepts: {key_concepts}

The script should:
- Use energetic and positive language
- Include specific action steps
- Incorporate success visualization
- Focus on personal growth
- End with a call to action""",
            
            "education": """Create an informative and engaging script that teaches the listener something new.
Theme: {theme}
Emotional Context: {emotional_context}
Key Concepts: {key_concepts}

The script should:
- Use clear and accessible language
- Break down complex concepts
- Include practical examples
- Encourage curiosity
- End with key takeaways"""
        }
        
        # Default template for unknown intentions
        self.default_template = """Create a supportive and engaging script that addresses the listener's needs.
Theme: {theme}
Emotional Context: {emotional_context}
Key Concepts: {key_concepts}

The script should:
- Use empathetic and understanding language
- Address the emotional context
- Incorporate the key concepts naturally
- Provide practical guidance
- End with a sense of closure and hope"""
    
    def create_prompt(self, intention_data: Dict[str, Any]) -> str:
        """
        Create a prompt for script generation based on recognized intention.
        
        Args:
            intention_data: Dictionary containing intention analysis
            
        Returns:
            A formatted prompt string
        """
        # Extract data from the intention analysis
        intention = intention_data.get("intention", "").lower()
        theme = intention_data.get("theme", "mindfulness")
        emotional_context = intention_data.get("emotional_context", "neutral")
        key_concepts = intention_data.get("key_concepts", ["peace", "calm"])
        
        # Convert key concepts list to string
        key_concepts_str = ", ".join(key_concepts) if isinstance(key_concepts, list) else key_concepts
        
        # Select template based on intention, or use default if not found
        template = self.templates.get(intention, self.default_template)
        
        # Format the template with the intention data
        prompt = template.format(
            theme=theme,
            emotional_context=emotional_context,
            key_concepts=key_concepts_str
        )
        
        prompt = self.general_requirements + "\n" + prompt
        
        # Add additional context from the rewritten prompt if available
        if "rewritten_prompt" in intention_data and intention_data["rewritten_prompt"]:
            prompt += f"\n\nAdditional context from user: {intention_data['rewritten_prompt']}"
        prompt += '\n\n' + self.final_requirements
        print(prompt)
        # raise Exception("Stop here")
        # Get enhanced prompt from LLM
        enhanced_prompt = self.model_client.generate_text(
            prompt=prompt,
            model=self.model_name,
            temperature=0.6,
            component="PromptCreator"
        )
        
        return enhanced_prompt 


def main():
    """
    Test function for PromptCreator class.
    """
    # Create a PromptCreator instance
    prompt_creator = PromptCreator()
    
    # Test data for different intentions
    test_cases = [
        {
            "name": "Relaxation Meditation",
            "data": {
                "intention": "emotional relief and validation",
                "theme": "betrayal, injustice, and social conflict",
                "emotional_context": "Intense feelings of委屈 (wronged injustice) stemming from being falsely accused and scapegoated by peers. The user feels deeply misunderstood, unfairly targeted, and emotionally exhausted by social betrayal, leading to avoidance of school despite valuing education.",
                "rewritten_prompt": "I feel deeply wronged after being betrayed by peers who falsely accuse me of gossiping and backstabbing—actions they actually committed themselves. They've scapegoated me, making me dread school despite my love for learning. How can I cope with this injustice and emotional pain without compromising my education?",
                "key_concepts": [
                    "False accusations",
                    "Being scapegoated",
                    "Social betrayal/backstabbing",
                    "Emotional distress impacting education",
                    "Conflict avoidance vs. academic commitment",
                    "Coping with peer victimization",
                    "Seeking validation for injustice"
                ]
            }
        },
        {
            "name": "Motivation Session",
            "data": {
                "intention": "motivation",
                "theme": "personal growth", 
                "emotional_context": "feeling stuck",
                "key_concepts": ["progress", "goals", "inspiration", "action"],
                "rewritten_prompt": "I want to feel motivated to pursue my dreams"
            }
        },
        {
            "name": "Educational Content",
            "data": {
                "intention": "education",
                "theme": "mindfulness basics",
                "emotional_context": "curious and eager to learn",
                "key_concepts": ["awareness", "present moment", "observation"],
                "rewritten_prompt": "Teach me about mindfulness meditation"
            }
        },
        {
            "name": "Default Template Test",
            "data": {
                "intention": "unknown_intention",
                "theme": "inner peace",
                "emotional_context": "seeking balance",
                "key_concepts": ["harmony", "balance", "centeredness"]
            }
        }
    ]
    
    print("=" * 60)
    print("PROMPT CREATOR TESTING")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['name']}")
        print("-" * 40)
        
        try:
            # Create prompt using the test data
            result = prompt_creator.create_prompt(test_case['data'])
            print(f"✅ Success! Generated prompt length: {len(result)} characters")
            print(f"Preview: {result[:200]}...")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            if "Stop here" in str(e):
                print("📝 Note: This is the intentional stop point in the code")
        
        print()
    
    print("=" * 60)
    print("Testing completed!")
    print("=" * 60)


if __name__ == "__main__":
    main() 