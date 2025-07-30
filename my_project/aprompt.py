# 1 intention_recognizer
analysis_prompt = f"""
Analyze the following user input and emotional state. 
Identify the primary intention, theme, and context.

User Input: {user_prompt}
Emotional State: {emotional_state}

Please provide:
1. Primary intention (e.g., relaxation, motivation, education, etc.)
2. Underlying theme (e.g., nature, success, mindfulness, etc.)
3. Emotional context (considering both the stated emotional state and the content)
4. A refined/rewritten version of the prompt that captures the essence
5. Key concepts that should be addressed

Please format the response as a JSON object with the keys: intention, theme, emotional_context, rewritten_prompt, and key_concepts.
Do not output anything else after the JSON object.
"""




# 2 prompt_creator，general_requirements, final_requirements

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



# 3 image_creator

base_prompt = f"""
Create a {intention}-focused image that captures the essence of {theme}.
The image should convey a sense of {emotional_context} and incorporate elements of {key_concepts_str}.
"""

# image prompt creator prompt
# Use LLM to enhance the base prompt with more details
enhancement_prompt = f"""
Create a detailed, vivid, and specific image generation prompt based on the following theme and concepts.
Make it suitable for an AI image generator (like DALL-E) by including specific visual elements,
lighting, mood, style, and composition details.

Base prompt: {base_prompt}

The image should be:
- High quality and aesthetically pleasing
- Suitable for a meditation or mindfulness video
- Emotionally resonant with the theme and concepts
- Not containing any text or human faces
- Avoiding any controversial, disturbing or explicit content

Enhance the prompt with specific details about:
- Visual elements and symbolism
- Color palette and lighting
- Artistic style
- Composition and perspective

Return ONLY the enhanced prompt text, without any explanations, introductions or additional notes."""


