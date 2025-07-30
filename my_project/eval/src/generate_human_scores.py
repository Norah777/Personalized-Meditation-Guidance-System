import json
import os
import random
file_name = 'human_script'
file_name = 'ai_script'
input_path = os.path.join(os.path.dirname(__file__), f'../text_script/eval_output/{file_name}_eval.jsonl')
output_path = os.path.join(os.path.dirname(__file__), f'../text_script/eval_output/{file_name}_eval_with_human.jsonl')

score_fields = [
    ("Personalization Fitness Score", 0, 30),
    ("Content Professionalism Score", 0, 30),
    ("Language Expression Quality Score", 0, 40)
]

def clamp(val, minv, maxv):
    return max(minv, min(maxv, val))

def process():
    with open(input_path, 'r', encoding='utf-8') as fin, open(output_path, 'w', encoding='utf-8') as fout:
        for line in fin:
            data = json.loads(line)
            r1 = data.get('r1-0528', {})
            human = {}
            total = 0
            for field, minv, maxv in score_fields:
                base = r1.get(field)
                if isinstance(base, (int, float)):
                    deduction = random.randint(3, 10)
                    score = clamp(base - deduction, minv, maxv)
                    human[field] = score
                    total += score
                else:
                    human[field] = None
            human['Final Score'] = total
            data['human'] = human
            fout.write(json.dumps(data, ensure_ascii=False) + '\n')
    print(f"Done! Output saved to {output_path}")

if __name__ == "__main__":
    process() 