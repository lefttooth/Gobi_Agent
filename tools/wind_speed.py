import rasterio
from rasterio.transform import rowcol
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class WindSpeedTool(BaseTool):
    name: str = "get_wind_speed_at_point"
    description: str = "输入经纬度，返回风速.tif中该点的风速值。"

    class ArgsSchema(BaseModel):
        longitude: float = Field(..., description="经度")
        latitude: float = Field(..., description="纬度")

    args_schema = ArgsSchema

    def _run(self, *args, **kwargs) -> float:
        import json
        import ast
        print(f"[DEBUG] args: {args}, kwargs: {kwargs}")
        longitude = None
        latitude = None
        tif_path = "data/风速.tif"
        # 先从 kwargs 获取
        if "longitude" in kwargs:
            longitude = kwargs["longitude"]
        if "latitude" in kwargs:
            latitude = kwargs["latitude"]
        if "tif_path" in kwargs:
            tif_path = kwargs["tif_path"]
        # 再从 args 获取
        if longitude is None and len(args) > 0:
            # 如果是 JSON 字符串
            if isinstance(args[0], str):
                try:
                    # 尝试解析为 dict
                    params = json.loads(args[0])
                    longitude = params.get("longitude")
                    latitude = params.get("latitude")
                    tif_path = params.get("tif_path", tif_path)
                except Exception as e:
                    print(f"[DEBUG] JSON decode error: {e}")
                    # 尝试解析为元组字符串
                    try:
                        tup = ast.literal_eval(args[0])
                        if isinstance(tup, tuple) and len(tup) == 2:
                            longitude, latitude = tup
                    except Exception as e2:
                        print(f"[DEBUG] tuple decode error: {e2}")
            elif isinstance(args[0], dict):
                longitude = args[0].get("longitude")
                latitude = args[0].get("latitude")
                tif_path = args[0].get("tif_path", tif_path)
            else:
                longitude = args[0]
        if latitude is None and len(args) > 1:
            latitude = args[1]
        if longitude is None or latitude is None:
            raise ValueError("必须提供经度和纬度参数")
        with rasterio.open(tif_path) as src:
            row, col = rowcol(src.transform, float(longitude), float(latitude))
            value = src.read(1)[row, col]
            return float(value)

    def _arun(self, lon: float, lat: float, tif_path: str = "data/风速.tif"):
        raise NotImplementedError("异步暂不支持")

# 工具实例，可用于 langchain agent
wind_speed_tool = WindSpeedTool()

if __name__ == "__main__":
    lon = 100.39499837692665
    lat = 40.69149268636249
    value = wind_speed_tool.run(lon, lat)
    print(f"坐标({lon}, {lat})的风速值为: {value}")
