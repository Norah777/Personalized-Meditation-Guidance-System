import json
import os

input_path = os.path.join(os.path.dirname(__file__), '../text_script/eval_output/human_script_avg.jsonl')
output_path = os.path.join(os.path.dirname(__file__), '../text_script/eval_output/human_script_avg_with_human.jsonl')

json_list = []
with open(input_path, 'r', encoding='utf-8') as fin, open(output_path, 'w', encoding='utf-8') as fout:
    for line in fin:
        data = json.loads(line)
        data['human'] = data.get('r1-0528', {})
        json_list.append(data)
        # fout.write(json.dumps(data, ensure_ascii=False) + '\n')

def save_jsonl(data_list, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        for data in data_list:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')
            
def get_score(data):
    pf_score = data['Personalization Fitness Score_avg']
    cp_score = data['Content Professionalism Score_avg']
    le_score = data['Language Expression Quality Score_avg']
    final_score = data['Final Score_avg']
    return pf_score, cp_score, le_score, final_score

def main():
    for data in json_list:
        pf_score, cp_score, le_score, final_score = get_score(data['r1-0528'])
        data['human'] = {
            'pf_score': pf_score,
            'cp_score': cp_score,
            'le_score': le_score,
            'final_score': final_score
        }

            
if __name__ == "__main__":
    main()

print(f"Done! Output saved to {output_path}") 