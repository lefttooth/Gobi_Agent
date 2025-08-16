from langchain.agents import initialize_agent, Tool
from langchain_community.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
from tools.wind_speed import WindSpeedTool

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
llm = ChatOpenAI(
<<<<<<< HEAD
    openai_api_key="",  # 替换为你的 DeepSeek API key
    openai_api_base="https://api.deepseek.com/v1",  # DeepSeek OpenAI兼容API地址
=======
    openai_api_key=api_key,
    openai_api_base="https://api.deepseek.com/v1",
>>>>>>> f593865 (sql env)
    model="deepseek-chat"
)

from langchain.tools import Tool
wind_speed_tool = Tool.from_function(
    func=WindSpeedTool()._run,
    name="get_wind_speed_at_point",
    description="输入经纬度，返回风速.tif中该点的风速值。"
)

# 构建 agent，集成风速工具
agent = initialize_agent(
    tools=[wind_speed_tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

if __name__ == "__main__":
    # 示例问题：查询指定坐标的风速
    question = "请查询坐标100.39499837692665, 40.69149268636249的风速值"
    result = agent.invoke(question)
    print(result)

name: str = "get_wind_speed_at_point"
description: str = "输入经纬度，返回风速.tif中该点的风速值。"
