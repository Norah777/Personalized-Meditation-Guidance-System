import json
import os
from collections import defaultdict

def calc_jsonl_avg_score(jsonl_path):
    """
    计算jsonl文件中所有评分字段的平均分
    :param jsonl_path: jsonl文件路径
    :return: dict，key为评分字段，value为平均分
    """
    score_fields = [
        "Personalization Fitness Score_avg",
        "Content Professionalism Score_avg",
        "Language Expression Quality Score_avg",
        "Final Score_avg"
    ]
    sums = defaultdict(float)
    counts = defaultdict(int)
    total = 0

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            scores = data.get("r1-0528", {})
            for field in score_fields:
                val = scores.get(field)
                if isinstance(val, (int, float)):
                    sums[field] += val
                    counts[field] += 1
            total += 1

    avg_result = {}
    for field in score_fields:
        if counts[field]:
            avg_result[field] = round(sums[field] / counts[field], 2)
        else:
            avg_result[field] = None

    print(f"Total items: {total}")
    for field in score_fields:
        print(f"{field}: {avg_result[field]}")
    return avg_result

if __name__ == "__main__":
    # 默认路径，可修改
    path = os.path.join(os.path.dirname(__file__), "../text_script/eval_output/human_script_avg.jsonl")
    calc_jsonl_avg_score(path) 