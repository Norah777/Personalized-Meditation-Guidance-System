import json
import os
import numpy as np
import pandas as pd
from collections import defaultdict

score_fields = [
    "Personalization Fitness Score",
    "Content Professionalism Score",
    "Language Expression Quality Score",
    "Final Score"
]

input_path = os.path.join(os.path.dirname(__file__), '../text_script/eval_output/human_script_eval_with_human.jsonl')
output_path = os.path.join(os.path.dirname(__file__), '../text_script/eval_output/human_compare_llm_human.xlsx')

# 支持的模型key
model_keys = ["r1-0528", "human", "Qwen3-32B"]


def safe_mean(arr):
    return float(np.mean(arr)) if arr else None

def safe_std(arr):
    return float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0

def main():
    group = defaultdict(lambda: {k: defaultdict(list) for k in model_keys})
    # 全局统计
    global_scores = {k: defaultdict(list) for k in model_keys}
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            id_ = data.get("id")
            for k in model_keys:
                model_scores = data.get(k, {})
                if isinstance(model_scores, str):
                    try:
                        model_scores = json.loads(model_scores)
                    except Exception:
                        model_scores = {}
                for field in score_fields:
                    val = model_scores.get(field)
                    if isinstance(val, (int, float)):
                        group[id_][k][field].append(val)
                        global_scores[k][field].append(val)

    rows = []
    for id_ in sorted(group.keys()):
        for field in score_fields:
            means = {k: safe_mean(group[id_][k][field]) for k in model_keys}
            stds = {k: safe_std(group[id_][k][field]) for k in model_keys}
            # 两两均值差
            diff_r1_human = means["r1-0528"] - means["human"] if means["r1-0528"] is not None and means["human"] is not None else None
            diff_r1_qwen = means["r1-0528"] - means["Qwen3-32B"] if means["r1-0528"] is not None and means["Qwen3-32B"] is not None else None
            diff_human_qwen = means["human"] - means["Qwen3-32B"] if means["human"] is not None and means["Qwen3-32B"] is not None else None
            rows.append({
                "id": id_,
                "Score Type": field,
                "r1-0528 Mean": means["r1-0528"],
                "human Mean": means["human"],
                "Qwen3-32B Mean": means["Qwen3-32B"],
                "r1-0528 Std": stds["r1-0528"],
                "human Std": stds["human"],
                "Qwen3-32B Std": stds["Qwen3-32B"],
                "r1-0528 - human": diff_r1_human,
                "r1-0528 - Qwen3-32B": diff_r1_qwen,
                "human - Qwen3-32B": diff_human_qwen
            })

    # 全局均值输出
    print("\n=== 全局平均分 ===")
    for field in score_fields:
        print(f"{field}:")
        for k in model_keys:
            vals = global_scores[k][field]
            avg = safe_mean(vals)
            print(f"  {k}: {avg:.2f}" if avg is not None else f"  {k}: None")

    df = pd.DataFrame(rows)
    df.to_excel(output_path, index=False)
    print(f"\nDone! Output saved to {output_path}")

if __name__ == "__main__":
    main() 