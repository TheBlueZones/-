from langchain_community.chat_models import ChatZhipuAI
from langchain.prompts import PromptTemplate
from langchain.agents import Tool, AgentExecutor, create_react_agent
from tools.search_tool import get_UID
import os

# 设置智谱AI API密钥


def lookup_V(flower_type: str):
    llm = ChatZhipuAI(
        model_name="glm-4-plus",
        temperature=0,
        # 也可以直接在这里设置API密钥
        zhipuai_api_key="c5fb87a5e747c34bf5164f952c7f896d.KUs6sw8d8FxyJ7p5" # 替换为你的实际API密钥
    )

    template = """按照以下步骤查找与 {input} 相关的微博用户ID：

        可用工具:
        {tools}
        可用工具名称: {tool_names}

        使用以下格式:
        Thought: 你的思考过程
        Action: 要使用的工具名称
        Action Input: 工具的输入
        Observation: 工具的输出
        ... (这个思考/行动/观察可以重复多次)
        Thought: 我现在知道最终答案
        Final Answer: 用户ID（纯数字）

        开始查找:
        {agent_scratchpad}"""

    tools = [
        Tool(
            name="Search Weibo User",
            func=get_UID,
            description="用于搜索微博用户，输入关键词，返回相关用户ID"
        )
    ]

    prompt = PromptTemplate(
        template=template,
        input_variables=["input", "tools", "tool_names", "agent_scratchpad"]
    )

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        handle_parsing_errors=True,
        verbose=True
    )

    try:
        result = agent_executor.invoke({"input": flower_type})
        import re
        if result and isinstance(result, dict) and "output" in result:
            ids = re.findall(r'\d+', str(result["output"]))
            if ids:
                return ids[0]
        raise ValueError("未找到有效的用户ID")
    except Exception as e:
        print(f"搜索出错: {str(e)}")
        raise

if __name__ == "__main__":
    print(lookup_V("体育"))