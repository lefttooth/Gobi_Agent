from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "分类系统后端已初始化，未实现具体功能。"}

# 可在此扩展更多 API 路由
