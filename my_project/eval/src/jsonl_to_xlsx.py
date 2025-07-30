import json
import os
import pandas as pd

# 默认输入输出路径
file_name = 'ai_script_avg'
input_path = os.path.join(os.path.dirname(__file__), f'../text_script/eval_output/{file_name}.jsonl')
output_path = input_path.replace('.jsonl', '.xlsx')

# 读取jsonl
data = []
with open(input_path, 'r', encoding='utf-8') as fin:
    for line in fin:
        data.append(json.loads(line))

# 转为DataFrame并保存为xlsx
df = pd.DataFrame(data)
df.to_excel(output_path, index=False)

print(f"Done! Output saved to {output_path}") 