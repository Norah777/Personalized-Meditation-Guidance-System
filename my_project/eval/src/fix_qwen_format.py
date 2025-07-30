import json
import os

input_path = os.path.join(os.path.dirname(__file__), '../text_script/eval_output/ai_script_eval_with_human_1.jsonl')
output_path = os.path.join(os.path.dirname(__file__), '../text_script/eval_output/ai_script_eval_with_human_1_fixed.jsonl')

with open(input_path, 'r', encoding='utf-8') as fin, open(output_path, 'w', encoding='utf-8') as fout:
    for line in fin:
        data = json.loads(line)
        qwen = data.get('Qwen3-32B')
        # 如果是字符串且能被解析为dict，则转为dict
        if isinstance(qwen, str):
            try:
                qwen_dict = json.loads(qwen)
                data['Qwen3-32B'] = qwen_dict
            except Exception:
                pass  # 保持原样
        fout.write(json.dumps(data, ensure_ascii=False) + '\n')

print(f"Done! Output saved to {output_path}") 