import os
import json
from collections import defaultdict
import statistics
import math

def load_jsonl(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]

def save_jsonl(data_list, path):
    with open(path, 'w', encoding='utf-8') as f:
        for data in data_list:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')

def cal_avg_score(input_path, output_path, model_name):
    data = load_jsonl(input_path)
    groups = defaultdict(list)
    # 支持id或filename分组
    for item in data:
        key = item.get('id') or item.get('filename')
        groups[key].append(item)

    avg_list = []
    for key, items in groups.items():
        n = len(items)
        if n == 0:
            continue
        # 只对有分数字段的求平均、方差、标准差、最大值、最小值
        score_fields = [
            'Personalization Fitness Score',
            'Content Professionalism Score',
            'Language Expression Quality Score',
            'Final Score'
        ]
        avg_item = dict(items[0])  # 复制一份基础信息
        avg_dict = {}
        for field in score_fields:
            # 从模型名下的字典中获取分数
            vals = []
            for x in items:
                model_data = x.get(model_name, {})
                if isinstance(model_data, dict):
                    score = model_data.get(field)
                    if isinstance(score, (int, float)):
                        vals.append(score)
            
            if vals:
                avg = sum(vals) / len(vals)
                # 计算方差
                variance = statistics.variance(vals) if len(vals) > 1 else 0.0
                # 计算标准差
                std_dev = math.sqrt(variance)
                # 计算最大值和最小值
                max_val = max(vals)
                min_val = min(vals)
                
                avg_dict[f"{field}_avg"] = round(avg, 2)
                avg_dict[f"{field}_variance"] = round(variance, 2)
                avg_dict[f"{field}_std"] = round(std_dev, 2)
                avg_dict[f"{field}_max"] = max_val
                avg_dict[f"{field}_min"] = min_val
                avg_dict[f"{field}_count"] = len(vals)  # 添加样本数量
            else:
                avg_dict[f"{field}_avg"] = None
                avg_dict[f"{field}_variance"] = None
                avg_dict[f"{field}_std"] = None
                avg_dict[f"{field}_max"] = None
                avg_dict[f"{field}_min"] = None
                avg_dict[f"{field}_count"] = 0
        avg_item[model_name] = avg_dict
        avg_list.append(avg_item)
    save_jsonl(avg_list, output_path)

if __name__ == '__main__':
    base_dir = os.path.dirname(__file__)
    file_name = 'ai_script'
    input_path = os.path.join(base_dir, f'../text_script/eval_output/{file_name}_eval_with_human.jsonl')
    output_path = os.path.join(base_dir, f'../text_script/eval_output/{file_name}_avg.jsonl')
    model_name = 'Qwen3-32B'  # 可根据实际模型名修改
    cal_avg_score(input_path, output_path, model_name)
