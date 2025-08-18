from langchain.agents import initialize_agent, Tool
from langchain_community.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
from tools.wind_speed import WindSpeedTool
from tools.gobi_classifier import GobiClassifierTool

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
llm = ChatOpenAI(
    openai_api_key=api_key,  # 替换为你的 DeepSeek API key
    openai_api_base="https://api.deepseek.com/v1",  # DeepSeek OpenAI兼容API地址
    model="deepseek-chat"
)

from langchain.tools import Tool
wind_speed_tool = Tool.from_function(
    func=WindSpeedTool()._run,
    name="get_wind_speed_at_point",
    description="输入经纬度，返回风速.tif中该点的风速值。"
)
gobi_classifier_tool = Tool.from_function(
    func=GobiClassifierTool()._run,
    name="gobi_classifier",
    description="根据风速值判断是否为戈壁。风速大于4m/s为戈壁，小于等于4m/s为非戈壁。输入经纬度，自动调用风速工具并返回分类结果。"
)

# 构建 agent，集成风速工具
agent = initialize_agent(
    tools=[wind_speed_tool, gobi_classifier_tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

if __name__ == "__main__":
    # 让模型判断指定坐标是否为戈壁
    question = "请判断坐标100.39499837692665, 40.69149268636249是不是戈壁？"
    result = agent.invoke(question)
    print(result)

name: str = "get_wind_speed_at_point"
description: str = "输入经纬度，返回风速.tif中该点的风速值。"
