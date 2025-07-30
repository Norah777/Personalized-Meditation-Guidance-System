import os
import pandas as pd
import sys
import importlib.util

# 动态导入construct_prompt_full.py中的data变量
module_path = os.path.join(os.path.dirname(__file__), 'construct_prompt_full.py')
spec = importlib.util.spec_from_file_location("construct_prompt_full", module_path)
mod = importlib.util.module_from_spec(spec)
sys.modules["construct_prompt_full"] = mod
spec.loader.exec_module(mod)

data = mod.data

output_path = os.path.join(os.path.dirname(__file__), '../text_script/data_export.xlsx')
df = pd.DataFrame(data)
df.to_excel(output_path, index=False)
print(f"Done! Output saved to {output_path}") 