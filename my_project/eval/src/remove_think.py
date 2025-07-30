import json, os

def load_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]

def save_jsonl(data_list, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        for data in data_list:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')
           
def remove_think(data):
    data = data.split('</think>')[1].strip()
    return data
def load_json(data):
    return json.loads(data)

file_name = 'ai_script_eval_with_human'
input_path = os.path.join(os.path.dirname(__file__), f'../text_script/eval_output/{file_name}.jsonl')
output_path = os.path.join(os.path.dirname(__file__), f'../text_script/eval_output/{file_name}_1.jsonl')

data_list = load_jsonl(input_path)

for i,data in enumerate(data_list):
    data['Qwen3-32B'] = remove_think(data['Qwen3-32B'])
    # try:
    #     data['r1-0528'] = load_json(data['r1-0528'])
    # print(type(data['r1-0528']))
    # data['r1-0528'] = json.loads(data['r1-0528'])
    # except:
    #     print(data['r1-0528'])
    #     raise Exception('r1-0528 is not a json')

save_jsonl(data_list, output_path)
