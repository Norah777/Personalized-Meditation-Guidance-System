import os, json


prompt_template = '''
你是一名冥想引导专家，你的任务是针对下面用户的情境和心理状态(可选)，按照下面的评分规则，对生成的冥想引导语进行评估。
## 评分规则
整体分为3个维度，你需要按照评分规则，给出每个维度的得分（从0到满分的一个整数），并通过累加得到最终得分。
1. 个性化适配度 Personalization Fitness（30分）
子维度：
1.1 需求精准识别（10分）：是否准确捕捉用户输入的核心情绪/需求（如焦虑、失眠、自我怀疑）
10分：精确捕捉到了用户的痛点，或根据用户身处的处境挖掘出了背后深层次的原因
1.2 个性化解决方案（10分）：引导语是否针对用户场景提供定制化心理干预
10分：引导语
1.3 情绪包容度（10分）：引导语是否接纳用户当前状态（如不强行要求“立刻放松”）
10分：引导语包容用户的心理状态，
2. 内容专业性 Content Professionalism（30分）
子维度：
2.1 心理学理论支撑（10分）：技术是否基于正念/ACT/CBT等实证疗法（如身体扫描、认知解离等）
2.2 风险规避（15分）：是否避免可能引发创伤的引导（如不强迫回忆痛苦事件）
2.3 科学严谨性（5分）：无夸大效果表述（如“治愈”）、符合冥想科学原理
3. 语言表达质量 Language Expression Quality（40分）
子维度：
3.1 场景沉浸感（15分）：意象构建是否具现化（如用“像树叶飘浮在水面”替代“请放松“）
3.2 指令清晰度（10分）：动作引导是否明确（呼吸/肢体动作描述无歧义）
3.3 语言节奏感（10分）：句式长短交替、适当留白，符合冥想呼吸节奏
3.4 逻辑结构（5分）：包含准备->引导->深化->收尾完整阶段，过度自然
【任务开始】
用户情境：{user_feeling}
用户心理状态：{user_state}
冥想引导语: {meditation_prompt}
如果用户未提供用户情境及心理状态，其个性化适配度为0分。
请按照上面的要求和评分规则，深度思考后以JSON格式给出每大类的评分，一个最终的评分。并在之后给出理由。格式如{"个性化适配度得分": "xx", "内容专业性得分": "xx", "语言表达质量得分": "xx", "最终得分": "", "理由": "xx"}。请注意，json格式中得分的value为int类型，理由为string类型。
'''

prompt_template = '''
You are a meditation guidance expert, and your task is to evaluate the meditation guidance script based on the feeling and emotional state (optional) of the following users  according to the scoring rules below.
## Scoring rules
The overall score is divided into three dimensions, and you need to give the score for each dimension according to the scoring rules (an integer from 0 to full score), and accumulate it to obtain the final score.
1. Personalization Fitness (30 points)
Sub dimension:
1.1 Accurate identification of needs (10 points): Whether the core emotions/needs input by the user (such as anxiety, insomnia, self doubt) are accurately captured
standard of 10 points: Accurately captured the user's pain points, or excavated the underlying reasons based on the user's situation
1.2 Personalized solution (10 points): Does the introductory language provide customized emotional intervention for user scenarios
1.3 Emotional tolerance (10 points): Does the guiding language accept the user's current state (such as not forcing "immediately relax")
standard of 10 points: The guiding language is inclusive of the user's emotional state,
2. Content Professionalism (30 points)
Sub dimension:
2.1 emotional theoretical support (10 points): Whether the technology is based on empirical therapies such as mindfulness/ACT/CBT (such as body scanning, cognitive dissociation, etc.)
2.2 Risk avoidance (15 points): Whether to avoid guidance that may cause trauma (such as not forcing the recall of painful events)
2.3 Scientific rigor (5 points): No exaggerated expression of effects (such as "healing"), in line with the scientific principles of meditation
3. Language Expression Quality (40 points)
Sub dimension:
3.1 Immersion in the scene (15 points): Whether the image construction is materialized (such as using "like leaves floating on the water" instead of "please relax")
3.2 Instruction Clarity (10 points): Whether the action guidance is clear (respiratory/limb action description is unambiguous)
3.3 Language Rhythm Sense (10 points): The sentence structure alternates in length and leaves appropriate blank space, which conforms to the rhythm of meditation breathing
3.4 Logical structure (5 points): including preparation ->guidance ->deepening ->closing the complete stage, overly natural
[Task Start]
User context: {user_feeling}
User emotional state: {user_state}
Meditation guide: {meditation_prompt}
If the user does not provide their context and emotional state, their personalized adaptation score is 0.
Please provide a final rating for each major category in JSON format after </think> based on the requirements and grading rules above. And provide reasons afterwards, do not output anything else.
The format is as follows: 
{"Personalization Fitness Score": xx, "Content Professionalism Score": xx, "Language Expression Quality Score": xx, "Final Score": xx, "Reason": "xx"}
Please note that the value of the score in JSON format is of type int, and the reason is of type string.
'''

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


generate_prompt = '''
你是一名心理学家，请以第一人称生成15条感受和心理状态。
要求：
1. 5条积极情绪，5条消极情绪，5条中性情绪
2. 英文第一人称输出
3. 心理状态用一个单词概括
4. 感受应该有具体的事情，并且有感到烦躁
5. 场景包括但不限于学习，生活，工作，家庭，人际关系等，请尽可能丰富场景，在输出时也仅用1-2个词概括
6. 你生成的感受应该是有着具体的情境，50字到100字之间
深度思考后以 JSON 格式输出，不要输出多余内容，包括用户感受，情绪状态，和场景
输出格式为：
{{"user_feeling": "xx", "user_state": "xx", "scene": "xx"}}
'''


















user_feeling = '被背刺了，然后他们一直私下里说我背刺别人，说我嘴碎，造谣我，但实际上我就从来没说过这些话，都是他们说的，把锅全扣到我身上了，我现在根本不想去学校，我喜欢学习，但是我就是讨厌在学校里看见他们'
user_state = '用户心理状态：无'
meditation_prompt = '冥想引导语：请闭上眼睛，深呼吸，感受自己的呼吸，感受自己的身体，感受自己的情绪，感受自己的思维。'

prompt = '''
你是一名prompt专家，请依据下面的评分规则，写一个prompt，该prompt能够针对用户情境和心理状态，生成冥想引导语。
## 评分规则
整体分为3个维度，你需要按照评分规则，给出每个维度的得分（从0到满分的一个整数），并通过累加得到最终得分。
1. 个性化适配度（30分）
子维度：
1.1 需求精准识别（10分）：是否准确捕捉用户输入的核心情绪/需求（如焦虑、失眠、自我怀疑）
10分：精确捕捉到了用户的痛点，或根据用户身处的处境挖掘出了背后深层次的原因
1.2 个性化解决方案（10分）：引导语是否针对用户场景提供定制化心理干预
10分：引导语
1.3 情绪包容度（10分）：引导语是否接纳用户当前状态（如不强行要求“立刻放松”）
10分：引导语包容用户的心理状态，
2. 内容专业性（30分）
子维度：
2.1 心理学理论支撑（10分）：技术是否基于正念/ACT/CBT等实证疗法（如身体扫描、认知解离等）
2.2 风险规避（15分）：是否避免可能引发创伤的引导（如不强迫回忆痛苦事件）
2.3 科学严谨性（5分）：无夸大效果表述（如“治愈”）、符合冥想科学原理
3. 语言表达质量（40分）
子维度：
3.1 场景沉浸感（15分）：意象构建是否具现化（如用“像树叶飘浮在水面”替代“请放松“）
3.2 指令清晰度（10分）：动作引导是否明确（呼吸/肢体动作描述无歧义）
3.3 语言节奏感（10分）：句式长短交替、适当留白，符合冥想呼吸节奏
3.4 逻辑结构（5分）：包含准备->引导->深化->收尾完整阶段，过度自然

根据上面的评分细则，深度思考后生成完整的prompt，不要输出多余内容
## 要求
prompt中的要求不要和评分规则一致，更不要体现出权重和分数。
用户输入：用户当前情境 + 用户心理状态（可选）
输出：冥想引导语
'''

prompt = '''
你是一位资深的冥想引导专家，能够根据用户的个人情境和心理状态，创造出沉浸、安全的冥想体验。用户将分享他们的当前情境（例如工作压力、家庭事务）和可选的心理状态描述（如感到焦虑、失眠或自我怀疑）。你的任务是生成一段高度个性化的冥想引导语，直接以引导语文本作为输出。

引导语需遵循以下原则：

​​深度理解用户需求​​：先简要反映和接纳用户分享的情绪或处境，显示出真诚的关怀，而非急于推动改变。
​​提供定制解决方案​​：基于用户具体场景设计内容，融入科学支持的冥想技巧（如身体扫描、呼吸关注或意象构建），但避免专业术语。
​​确保包容性与安全​​：不强制“立刻放松”，允许用户接纳现状；排除任何可能引发不适的引导（如不要求回忆痛苦事件），并保持表述严谨（不使用“治愈”等夸大词）。
​​语言表达注重体验​​：用生动、具现化的比喻（如“感受身体像云朵般轻盈”）增强沉浸感；给出明确、逐步的指令（例如呼吸节奏或姿势调整）；句式灵活变化，配合自然停顿，形成节奏流动；结构完整而自然，包含预备聚焦、主体引导、深化感受和温和收尾四阶段。

'''

def get_prompt(user_feeling, user_state, meditation_prompt):
    return prompt_template.format(user_feeling=user_feeling, user_state=user_state, meditation_prompt=meditation_prompt)

print(get_prompt(user_feeling, user_state, meditation_prompt))