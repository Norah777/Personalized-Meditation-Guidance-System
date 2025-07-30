import os
import json

input_dir = os.path.join(os.path.dirname(__file__), '../human_script')
output_file = os.path.join(os.path.dirname(__file__), '../human_script.jsonl')

with open(output_file, 'w', encoding='utf-8') as fout:
    for fname in sorted(os.listdir(input_dir)):
        fpath = os.path.join(input_dir, fname)
        if os.path.isfile(fpath):
            with open(fpath, 'r', encoding='utf-8') as fin:
                content = fin.read()
            # Write as JSONL: {"filename": ..., "content": ...}
            json.dump({"id": fname, "user_feeling": "", "user_state": "", "meditation_prompt": content, "type": "human"}, fout, ensure_ascii=False)
            fout.write('\n') 