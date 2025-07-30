#!/bin/bash

# 設置輸出目錄
output_dir="output_test1"
user_prompt="被背刺了，然后他们一直私下里说我背刺别人，说我嘴碎，造谣我，但实际上我就从来没说过这些话，都是他们说的，把锅全扣到我身上了，我现在根本不想去学校，我喜欢学习，但是我就是讨厌在学校里看见他们"
emotional_state="委屈"

# 運行腳本
python main.py --user_prompt "$user_prompt" --emotional_state "$emotional_state" --output_path "$output_dir"