import json
import os
import sys

# 添加pipeline路径到sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
my_project_dir = os.path.dirname(current_dir)
pipeline_dir = os.path.join(my_project_dir, '..', 'pipeline')
sys.path.append(pipeline_dir)
sys.path.append(my_project_dir)  # 添加my_project目录

# 修改导入方式
try:
    from pipeline.orchestrator import Orchestrator
except ImportError:
    # 如果上面的导入失败，尝试直接导入
    sys.path.append(os.path.join(my_project_dir, '..'))
    from my_project.pipeline.orchestrator import Orchestrator

data = [{"user_feeling": "When my partner cooked my favorite soup after I said I was unwell, and they sat with me, listening. The warmth of the soup and their care made all discomfort fade a little.", "user_state": "Grateful", "scene": "Family", "type": "positive"},
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
{"user_feeling": "Bumping into a classmate at the store, we talked about the weather. Their words didn't stick, and I left, not feeling happy or sad—just a brief chat.", "user_state": "Indifferent", "scene": "Relationships", "type": "neutral"}]

def generate_meditation_prompts():
    """为每个数据项生成冥想提示"""
    # 初始化Orchestrator
    orchestrator = Orchestrator()
    
    # 创建输出目录
    output_dir = os.path.join(current_dir, '..', 'text_script')
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成冥想提示
    generated_data = []
    
    for i, item in enumerate(data, 1):
        print(f"Processing item {i}/{len(data)}...")
        # 调用generate_text_only生成冥想提示
        try:
            meditation_prompt = orchestrator.generate_text_only(
                user_prompt=item['user_feeling'],
                emotional_state=item['user_state'].lower()
            )
            
            # 创建输出数据项
            output_item = {
                "id": f"{i}.ai",
                "user_feeling": item['user_feeling'],
                "user_state": item['user_state'],
                "meditation_prompt": meditation_prompt,
                "type": "r1-0528",
                "scene": item['scene']
            }
            
            generated_data.append(output_item)
            print(f"Successfully generated meditation prompt for item {i}")
            
        except Exception as e:
            print(f"Error generating meditation prompt for item {i}: {e}")
            # 如果生成失败，创建一个空的冥想提示
            output_item = {
                "id": f"{i}.ai",
                "user_feeling": item['user_feeling'],
                "user_state": item['user_state'],
                "meditation_prompt": "",
                "type": "r1-0528"
            }
            generated_data.append(output_item)
    
    # 保存到JSONL文件
    output_file = os.path.join(output_dir, 'ai_script.jsonl')
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in generated_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"Generated {len(generated_data)} meditation prompts and saved to {output_file}")
    return generated_data

if __name__ == "__main__":
    generate_meditation_prompts()




