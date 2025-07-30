import json
import os

data = [
    {"user_feeling": "When my partner cooked my favorite soup after I said I was unwell, and they sat with me, listening. The warmth of the soup and their care made all discomfort fade a little.", "user_state": "Grateful", "scene": "Family", "type": "positive"},
    {"user_feeling": "A friend sent me a playlist of songs we used to listen to in college, with a note saying 'thought of you'. Each song brought back happy memories, making me smile widely.", "user_state": "Joyful", "scene": "Relationships", "type": "positive"},
    {"user_feeling": "My team's project won the award, and we hugged, recalling late nights. All the debates and hard work felt worth it when we held the trophy together.", "user_state": "Proud", "scene": "Work", "type": "positive"},
    {"user_feeling": "Walking in the garden, I found the rose I planted bloomed. Its soft petals and sweet scent made me pause, feeling a quiet happiness in seeing it grow.", "user_state": "Content", "scene": "Life", "type": "positive"},
    {"user_feeling": "My student told me I helped them love math, showing me their improved test. Their excitement made me feel my efforts as a teacher mattered deeply.", "user_state": "Fulfilled", "scene": "Work", "type": "positive"},
    {"user_feeling": "My report got criticized harshly without clear feedback, and the boss kept checking on it. I stared at the screen, hands shaking, feeling my work was unvalued.", "user_state": "Frustrated", "scene": "Work", "type": "negative"},
    {"user_feeling": "A friend canceled our plan last minute with a vague excuse, leaving me waiting. I sat alone in the café, sipping cold coffee, feeling ignored and upset.", "user_state": "Hurt", "scene": "Relationships", "type": "negative"},
    {"user_feeling": "The printer broke when I needed to print urgent documents, and no one could fix it quickly. I paced, gritting my teeth, annoyed at the sudden mess.", "user_state": "Irritated", "scene": "Life", "type": "negative"},
    {"user_feeling": "My parents argued over chores again, and I couldn't stop them. Their shouts echoed, making my chest tight, like I was stuck in a loop of tension.", "user_state": "Anxious", "scene": "Family", "type": "negative"},
    {"user_feeling": "I studied for hours but forgot key points in the quiz. Staring at the blank paper, I felt stupid, like all the time spent was wasted.", "user_state": "Disappointed", "scene": "Study", "type": "negative"},
    {"user_feeling": "Folding laundry on a Sunday, the sun shining through the window. No excitement, no boredom—just the rhythm of folding, making time pass steadily.", "user_state": "Calm", "scene": "Life", "type": "neutral"},
    {"user_feeling": "Sitting in a routine meeting, listening to updates. No strong feelings—just taking notes, thinking about the next task without rush or delay.", "user_state": "Neutral", "scene": "Work", "type": "neutral"},
    {"user_feeling": "Reading a book in the park, the story neither thrilled nor bored me. The breeze and distant chatter just made the moment feel ordinary, but nice.", "user_state": "Apathetic", "scene": "Life", "type": "neutral"},
    {"user_feeling": "Having dinner with family, we ate quietly while watching TV. No deep talks, but no tension—just sharing the meal, each in our own thoughts.", "user_state": "Detached", "scene": "Family", "type": "neutral"},
    {"user_feeling": "Bumping into a classmate at the store, we talked about the weather. Their words didn't stick, and I left, not feeling happy or sad—just a brief chat.", "user_state": "Indifferent", "scene": "Relationships", "type": "neutral"}
]

def call_api(prompt: str) -> str:
    """
    LLM调用占位函数。你可以在这里实现自己的API调用。
    """
    # TODO: 实现你的LLM调用逻辑
    return f"[LLM OUTPUT PLACEHOLDER for prompt: {prompt[:60]}...]"

def intention_recognition_prompt(user_prompt: str, emotional_state: str) -> str:
    return f"""
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

general_requirements = """
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

## Task
"""

final_requirements = """Please OUTPUT full script after </think> tag, mind that all the content after </think> will be seen as presentation scripts, so DO NOT include anything else. (Such as title and subtitle)"""

TEMPLATES = {
    "relaxation": """Create a calming and peaceful script that helps the listener relax and find inner peace.\nTheme: {theme}\nEmotional Context: {emotional_context}\nKey Concepts: {key_concepts}\n\nThe script should:\n- Use gentle, soothing language\n- Include breathing exercises\n- Incorporate mindfulness elements\n- Focus on letting go of tension\n- End with a sense of calm and renewal""",
    "motivation": """Create an inspiring and uplifting script that motivates the listener to take action.\nTheme: {theme}\nEmotional Context: {emotional_context}\nKey Concepts: {key_concepts}\n\nThe script should:\n- Use energetic and positive language\n- Include specific action steps\n- Incorporate success visualization\n- Focus on personal growth\n- End with a call to action""",
    "education": """Create an informative and engaging script that teaches the listener something new.\nTheme: {theme}\nEmotional Context: {emotional_context}\nKey Concepts: {key_concepts}\n\nThe script should:\n- Use clear and accessible language\n- Break down complex concepts\n- Include practical examples\n- Encourage curiosity\n- End with key takeaways""",
    "default": """Create a supportive and engaging script that addresses the listener's needs.\nTheme: {theme}\nEmotional Context: {emotional_context}\nKey Concepts: {key_concepts}\n\nThe script should:\n- Use empathetic and understanding language\n- Address the emotional context\n- Incorporate the key concepts naturally\n- Provide practical guidance\n- End with a sense of closure and hope"""
}

def build_script_prompt(intention_data: dict) -> str:
    intention = intention_data.get("intention", "").lower()
    theme = intention_data.get("theme", "mindfulness")
    emotional_context = intention_data.get("emotional_context", "neutral")
    key_concepts = intention_data.get("key_concepts", ["peace", "calm"])
    rewritten_prompt = intention_data.get("rewritten_prompt", "")
    key_concepts_str = ", ".join(key_concepts) if isinstance(key_concepts, list) else str(key_concepts)
    template = TEMPLATES.get(intention, TEMPLATES["default"])
    prompt = general_requirements + "\n" + template.format(
        theme=theme,
        emotional_context=emotional_context,
        key_concepts=key_concepts_str
    )
    if rewritten_prompt:
        prompt += f"\n\nAdditional context from user: {rewritten_prompt}"
    prompt += '\n\n' + final_requirements
    return prompt

def generate_meditation_prompts():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, '..', 'text_script')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'ai_script_full.jsonl')

    generated_data = []
    for i, item in enumerate(data, 1):
        print(f"Processing item {i}/{len(data)}...")
        # 1. 意图识别
        recog_prompt = intention_recognition_prompt(item['user_feeling'], item['user_state'])
        recog_result = call_api(recog_prompt)
        try:
            intention_data = json.loads(recog_result)
        except Exception:
            # fallback: 用默认结构
            intention_data = {
                "intention": "relaxation",
                "theme": "mindfulness",
                "emotional_context": item['user_state'],
                "rewritten_prompt": item['user_feeling'],
                "key_concepts": ["peace", "calm"]
            }
        # 2. 脚本生成
        script_prompt = build_script_prompt(intention_data)
        meditation_prompt = call_api(script_prompt)
        output_item = {
            "id": f"{i}.ai",
            "user_feeling": item['user_feeling'],
            "user_state": item['user_state'],
            "scene": item['scene'],
            "meditation_prompt": meditation_prompt,
            "type": "r1-0528"
        }
        generated_data.append(output_item)
        print(f"Successfully generated meditation prompt for item {i}")
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in generated_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    print(f"Generated {len(generated_data)} meditation prompts and saved to {output_file}")
    return generated_data

if __name__ == "__main__":
    generate_meditation_prompts() 