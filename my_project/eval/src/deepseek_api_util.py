from api.model_client import ModelClient
import os
import json
import copy
import concurrent.futures

prompt_template = '''
You are a meditation guidance expert, and your task is to evaluate the meditation guidance script based on the feeling and emotional state (optional) of the following users  according to the scoring rules below.
## Scoring rules
The overall score is divided into three dimensions, and you need to give the score for each dimension according to the scoring rules (an integer from 0 to full score), and accumulate it to obtain the final score.
1. Personalization Fitness (30 points)
Sub dimension:
1.1 Accurate identification of needs (10 points): Whether the core emotions/needs input by the user (such as anxiety, insomnia, self doubt) are accurately captured
Standard of 10 points: Accurately captured the user's pain points, or excavated the underlying reasons based on the user's situation​
Standard of 7 points: Basically captured the user's core emotions/needs, but failed to dig into the underlying reasons; the understanding is slightly superficial​
Standard of 3 points: Only captured partial or superficial information of the user's needs, and there is a certain deviation from the core needs​
Standard of 0 points: Completely failed to capture the user's core emotions/needs, or misunderstood the user's input

1.2 Personalized solution (10 points): Does the introductory language provide customized emotional intervention for user scenarios
Standard of 10 points: The introductory language is highly tailored to the user's specific scenario (such as combining details like work pressure sources, sleep environment), and the intervention methods are closely matched with the scenario​
Standard of 7 points: The introductory language has certain pertinence to the user's scenario, but the customization details are insufficient; the intervention methods are partially matched with the scenario​
Standard of 3 points: The introductory language has few personalized elements, mostly using general intervention templates, with little connection to the user's scenario​
Standard of 0 points: No personalized design, using completely universal language that is irrelevant to the user's scenario

1.3 Emotional tolerance (10 points): Does the guiding language accept the user's current state (such as not forcing "immediately relax")
Standard of 10 points: The guiding language is inclusive of the user's emotional state, fully accepts the user's current feelings without any forced demands, and guides them to face their state naturally​
Standard of 7 points: The guiding language basically accepts the user's emotional state, with only occasional mild forced guidance (such as "try to relax a little"), but does not affect the overall tolerance​
Standard of 3 points: The guiding language has more forced demands (such as "you must calm down immediately"), and the acceptance of the user's current state is obviously insufficient​
Standard of 0 points: The guiding language completely denies or forces the user's current state, with strong mandatory requirements (such as "don't be anxious anymore")

2. Content Professionalism (30 points)
Sub dimension:
2.1 emotional theoretical support (10 points): Whether the technology is based on empirical therapies such as mindfulness/ACT/CBT (such as body scanning, cognitive dissociation, etc.)
Standard of 10 points: Clearly based on at least one empirical therapy (mindfulness/ACT/CBT, etc.), and the technical methods (such as body scanning, cognitive defusion) are accurately and appropriately applied​
Standard of 7 points: Based on empirical therapies, but the application of technical methods is slightly rough or not fully in line with the theoretical connotation​
Standard of 3 points: The theoretical basis is vague, and the technical methods used are barely related to empirical therapies, with obvious inappropriateness​
Standard of 0 points: No basis on empirical therapies, and the technical methods used are unscientific or inconsistent with the principles of meditation

2.2 Risk avoidance (15 points): Whether to avoid guidance that may cause trauma (such as not forcing the recall of painful events)
Standard of 15 points: Completely avoids all possible traumatic guidance, and has clear safety reminders for potentially sensitive links (such as "if you feel uncomfortable, you can skip this part")​
Standard of 11 points: Basically avoids major traumatic guidance, but lacks safety reminders for some potentially sensitive links; no obvious risk of trauma​
Standard of 4 points: Contains guidance that may trigger mild discomfort (such as vague mention of painful memories without restriction), and there is a certain potential risk​
Standard of 0 points: Contains obvious guidance that may cause trauma (such as forcing the recall of painful events), with high risk of triggering negative reactions

2.3 Scientific rigor (5 points): No exaggerated expression of effects (such as "healing"), in line with the scientific principles of meditation
Standard of 5 points: No any exaggerated expressions, the description of effects is objective and in line with the scientific principles of meditation (such as "help you better cope with emotions")​
Standard of 3 points: There are occasional mild exaggerated expressions (such as "greatly relieve your pressure"), but the overall is in line with scientific principles​
Standard of 1 point: There are more exaggerated expressions (such as "quickly eliminate your anxiety"), which deviate from the scientific nature of meditation to a certain extent​
Standard of 0 points: There are serious exaggerated expressions (such as "completely cure your insomnia"), which completely violate the scientific principles of meditation

3. Language Expression Quality (40 points)
Sub dimension:
3.1 Immersion in the scene (15 points): Whether the image construction is materialized (such as using "like leaves floating on the water" instead of "please relax")
Standard of 15 points: A large number of concrete and vivid images are used to construct the scene, which is highly immersive and can make the user easily imagine the corresponding picture​
Standard of 11 points: Some concrete images are used to construct the scene, with a certain sense of immersion, and the user can basically imagine the picture​
Standard of 4 points: Few concrete images are used, mostly abstract expressions (such as "feel relaxed"), with weak immersion and difficulty in constructing a scene in the user's mind​
Standard of 0 points: No concrete image construction, all using abstract and general language, with no sense of immersion at all

3.2 Instruction Clarity (10 points): Whether the action guidance is clear (respiratory/limb action description is unambiguous)
Standard of 10 points: The description of respiratory and limb actions is extremely clear and unambiguous, with detailed steps, and the user can accurately understand and execute the guidance​
Standard of 7 points: The description of respiratory and limb actions is basically clear, with only occasional slight ambiguity (such as "breathe deeply" without specifying the frequency), but the user can still execute it smoothly​
Standard of 3 points: The description of respiratory and limb actions is ambiguous in many places (such as "move your body appropriately"), and the user cannot clearly understand how to execute​
Standard of 0 points: The description of respiratory and limb actions is completely unclear and confusing, making it impossible for the user to understand or execute

3.3 Language Rhythm Sense (10 points): The sentence structure alternates in length and leaves appropriate blank space, which conforms to the rhythm of meditation breathing
Standard of 10 points: The sentence structure alternates between long and short, with appropriate pauses and blank spaces, which is highly consistent with the rhythm of meditation breathing, making the user feel natural and comfortable​
Standard of 7 points: The sentence structure has a certain alternation of length, with basically appropriate blank spaces, which is basically in line with the rhythm of meditation breathing, with only occasional slight inappropriateness​
Standard of 3 points: The sentence structure is single (mostly long or short sentences), with inappropriate blank spaces (too long or too short), which is obviously inconsistent with the rhythm of meditation breathing​
Standard of 0 points: There is no sense of rhythm in the language, the sentence structure is messy, and there is no reasonable blank space, which is completely inconsistent with the rhythm of meditation breathing

3.4 Logical structure (5 points): including preparation ->guidance ->deepening ->closing the complete stage, overly natural
Standard of 5 points: The logical structure is complete, including all stages of preparation, guidance, deepening, and closing, with natural and smooth transitions between stages​
Standard of 3 points: The logical structure is basically complete, with only slight omissions in some stages (such as a too simple closing), and the transitions between stages are slightly stiff but not abrupt​
Standard of 1 point: The logical structure is incomplete, with obvious missing stages (such as lacking preparation or closing), and the transitions between stages are chaotic and abrupt​
Standard of 0 points: There is no logical structure, the stages are scattered and disorderly, and there is no connection between different parts

[Task Start]
User context: {user_feeling}
User emotional state: {user_state}
Meditation guide: {meditation_prompt}
If the user does not provide their context and emotional state, their personalized adaptation score is 0.
Please provide a final rating for each major category in JSON format after </think> based on the requirements and grading rules above. And provide reasons afterwards, do not output anything else.
The format is as follows: 
{{"Personalization Fitness Score": xx, "Content Professionalism Score": xx, "Language Expression Quality Score": xx, "Final Score": xx, "Reason": "xx"}}
Please note that the value of the score in JSON format is of type int, and the reason is of type string.
'''

def get_prompt(user_feeling, user_state, meditation_prompt):
    return prompt_template.format(user_feeling=user_feeling, user_state=user_state, meditation_prompt=meditation_prompt)

def load_jsonl(input_path):
    a = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            a.append(data)
    return a

def save_jsonl(data_list, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        for data in data_list:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')

def call_api_parallel(data_, n=5, max_workers=5):
    data = []
    for i in range(n):
        data.append(copy.deepcopy(data_))
    return data
    """
    并行调用 deepseek API，n 为调用次数，max_workers 为最大线程数。
    """
    def single_call(data):
        data = copy.deepcopy(data)
        response = call_deepseek(data['prompt'])
        data['r1-0528'] = response
        response = json.loads(response)
        try:
            data['Personalization Fitness Score'] = response['Personalization Fitness Score']
            data['Content Professionalism Score'] = response['Content Professionalism Score']
            data['Language Expression Quality Score'] = response['Language Expression Quality Score']
            data['Final Score'] = response['Final Score']
            data['Reason'] = response['Reason']
        except:
            pass
        return data

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(single_call, data_) for _ in range(n)]
        new_data = [f.result() for f in concurrent.futures.as_completed(futures)]
    return new_data

def eval_human_script():
    script_name = 'human_script'
    script_name = 'ai_script'
    input_path = os.path.join(os.path.dirname(__file__), f'../text_script/{script_name}.jsonl')
    json_list = load_jsonl(input_path)
    new_json_list = []

    def process_one(data):
        user_feeling = data['user_feeling']
        user_state = data['user_state']
        meditation_prompt = data['meditation_prompt']
        prompt = get_prompt(user_feeling, user_state, meditation_prompt)
        data['prompt'] = prompt
        eval_data = call_api_parallel(data, n=16, max_workers=16)
        return eval_data

    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(process_one, json_list))
    for eval_data in results:
        new_json_list.extend(eval_data)
    save_jsonl(new_json_list, os.path.join(os.path.dirname(__file__), f'../text_script/eval_output/{script_name}_eval.jsonl'))
        
def main():
    eval_human_script()
    
    
def call_deepseek(prompt: str) -> str:
    """
    调用DeepSeek（OpenAI兼容API），返回生成的文本结果。
    """
    client = ModelClient(model_type='text')
    return client.generate_text(prompt) 

def test_deepseek():
    prompt = """
    1 + 1 = ?
    """
    print(call_deepseek(prompt))

if __name__ == "__main__":
    # test_deepseek()
    main()