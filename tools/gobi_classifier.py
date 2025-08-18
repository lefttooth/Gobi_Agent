from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from tools.wind_speed import WindSpeedTool

class GobiClassifierTool(BaseTool):
    name: str = "gobi_classifier"
    description: str = "根据风速值判断是否为戈壁。风速大于4m/s为戈壁，小于等于4m/s为非戈壁。输入经纬度，自动调用风速工具并返回分类结果。"

    class ArgsSchema(BaseModel):
        longitude: float = Field(..., description="经度")
        latitude: float = Field(..., description="纬度")

    args_schema = ArgsSchema

    def _run(self, *args, **kwargs) -> str:
        import json
        import ast
        longitude = None
        latitude = None
        # 先从 kwargs 获取
        if "longitude" in kwargs:
            longitude = kwargs["longitude"]
        if "latitude" in kwargs:
            latitude = kwargs["latitude"]
        # 再从 args 获取
        if longitude is None and len(args) > 0:
            # 如果是 JSON 字符串
            if isinstance(args[0], str):
                try:
                    params = json.loads(args[0])
                    longitude = params.get("longitude")
                    latitude = params.get("latitude")
                except Exception:
                    # 尝试解析为元组字符串
                    try:
                        tup = ast.literal_eval(args[0])
                        if isinstance(tup, tuple) and len(tup) == 2:
                            longitude, latitude = tup
                        elif isinstance(tup, list) and len(tup) == 2:
                            longitude, latitude = tup
                    except Exception:
                        # 尝试逗号分隔
                        try:
                            lon, lat = [float(x.strip()) for x in args[0].split(",")]
                            longitude, latitude = lon, lat
                        except Exception:
                            pass
            elif isinstance(args[0], dict):
                longitude = args[0].get("longitude")
                latitude = args[0].get("latitude")
            else:
                longitude = args[0]
        if latitude is None and len(args) > 1:
            latitude = args[1]
        if longitude is None or latitude is None:
            raise ValueError("必须提供经度和纬度参数")
        wind_speed = WindSpeedTool()._run(longitude=longitude, latitude=latitude)
        if wind_speed > 4:
            return f"风速为{wind_speed:.2f}m/s，判定为戈壁。"
        else:
            return f"风速为{wind_speed:.2f}m/s，判定为非戈壁。"
