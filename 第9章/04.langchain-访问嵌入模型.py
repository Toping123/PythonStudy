from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

# 示例模板
example_prompt = PromptTemplate.from_template("词语：{word}，反义词：{antonym}")

# 示例数据（动态数据注入）
example_data = [
    {"word": "大", "antonym": "小"},
    {"word": "上", "antonym": "下"},
]

few_shot_template = FewShotPromptTemplate(
    example_prompt=example_prompt,
    examples=example_data,
    prefix="告知我词语的反义词，我提供以下示例",
    suffix="基于我的示例，告诉我{input_word}的反义词",
    input_variables=['input_word']
)

prompt_text = few_shot_template.invoke(input={"input_word": "左"}).to_string()
print(prompt_text)

# 构造通义千问模型
model = Tongyi(model="qwen-max")

# 调用invoke进行提问（非流式）
print("通义千问回复:")
print(model.invoke(input=prompt_text))
