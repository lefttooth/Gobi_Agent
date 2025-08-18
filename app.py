from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from agent import agent


app = FastAPI()
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# 允许跨域，便于前端开发
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "分类系统后端已初始化，chat接口已启用。"}

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    # 直接调用 agent 进行推理
    result = agent.invoke(req.message)
    # 兼容 agent 返回 dict 或 str
    if isinstance(result, dict) and "output" in result:
        return {"reply": result["output"]}
    return {"reply": str(result)}
