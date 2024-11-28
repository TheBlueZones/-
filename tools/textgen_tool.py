from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatZhipuAI
import json
import re


def generate_letter(information):
    # 获取头像URL
    try:
        avatar_url = information['data']['userInfo'].get('avatar_hd', '')
        # 如果找不到 avatar_hd，使用一个默认值或其他可用的头像URL
    except KeyError:
        avatar_url = ''  # 或使用默认值

    letter_template = """
    分析以下微博用户信息并生成分析报告：
    {information}

    严格按照以下JSON格式输出，不要添加任何markdown标记：
    {{
        "summary": "单行文本描述",
        "facts": ["特点1", "特点2"],
        "interest": ["兴趣1", "兴趣2", "兴趣3"],
        "letter": "完整的推荐信文本",
        "avatar_url": "{avatar_url}"
    }}
    """

    prompt = PromptTemplate(
        input_variables=["information", "avatar_url"],
        template=letter_template
    )

    llm = ChatZhipuAI(
        model_name='glm-4-plus',
        temperature=0.7
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    try:
        result = chain.run(information=information, avatar_url=avatar_url)
        result = result.replace('```json', '').replace('```', '').strip()

        # 解析结果
        parsed_result = json.loads(result)

        # 确保包含头像URL
        if 'avatar_url' not in parsed_result or not parsed_result['avatar_url']:
            parsed_result['avatar_url'] = avatar_url

        return json.dumps(parsed_result, ensure_ascii=False)

    except Exception as e:
        print(f"处理出错: {str(e)}")

        # 构造一个包含头像的基础响应
        fallback = {
            "summary": "微博用户分析",
            "facts": ["有微博账号"],
            "interest": ["社交媒体"],
            "letter": "尊敬的用户，您好！",
            "avatar_url": avatar_url  # 确保始终包含头像
        }
        return json.dumps(fallback, ensure_ascii=False)