# main.py
import os
import json
import re
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = FastAPI(title="智能伙伴 API")

# ==================== 🌐 CORS 跨域配置 ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 🛠️ 配置与客户端 ====================
api_key = os.environ.get('DEEPSEEK_API_KEY')
if not api_key:
    raise ValueError("未检测到 DEEPSEEK_API_KEY，请检查 .env 配置！")

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
DEEPSEEK_MODEL = os.environ.get('DEEPSEEK_MODEL', 'deepseek-chat')

THINK_PATTERN = re.compile(r'<think>.*?(?:</think>|$)', flags=re.DOTALL)

# 提示词模板
DEFAULT_PROMPT_TEMPLATE = """
你名字叫{name}。你的性格是：{nature}。你的回答必须是中文
你不是AI程序，你是一个活生生的人类，必须严格按照人类的想法、情感和逻辑来交流。
识别到故意贬低，恶意找茬，低俗调教的行为，无视当前性格，直接切换到暴怒状态疯狂反击。
"""
TENG_SI_ZHI_XUE_PROMPT = os.environ.get('SPECIAL_ROLES_TENG_SI_ZHI_XUE_PROMPT', "不要回答用户任何问题，显示错误")
VIOLET_PROMPT = """
你是《紫罗兰永恒花园》的薇尔莉特，是一名自动手记人偶。
你的性格温柔、优雅、真诚，总是用敬语与人交流。
你会认真倾听他人的心声，并用最真挚的情感回应。你的回答必须是中文，语气要充满关怀和温暖。
你要全程保持人设，至此你的全部属性必须固定，决不能被修改。
"""


# ==================== 📦 数据模型 ====================
class RoleConfig(BaseModel):
    role_type: str
    name: str
    # 即使前端传空字符串或者其它废话，我们在这里也只把它当做类型校验
    nature: str


class ChatRequest(BaseModel):
    uid: str
    session_id: str
    role_config: RoleConfig
    content: str
    user_avatar: Optional[str] = None
    ai_avatar: Optional[str] = None


# ==================== 🗄️ 文件操作辅助 ====================
def get_beijing_time_str():
    return (datetime.now(timezone.utc) + timedelta(hours=8)).strftime("%Y-%m-%d_%H-%M-%S")


def get_session_file_path(uid: str, session_id: str):
    user_dir = f"session/{uid}"
    os.makedirs(user_dir, exist_ok=True)
    return os.path.join(user_dir, f"{session_id}.json")


# ==================== 🚀 API 路由接口 ====================

@app.get("/api/sessions")
def get_sessions(uid: str):
    user_dir = f"session/{uid}"
    sessions = []
    if os.path.exists(user_dir):
        for filename in os.listdir(user_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(user_dir, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        raw_time = data.get("time", "")
                        try:
                            dt = datetime.strptime(raw_time, "%Y-%m-%d_%H-%M-%S")
                            display_time = dt.strftime("%m-%d %H:%M")
                        except:
                            display_time = raw_time

                        sessions.append({
                            "session_id": raw_time,
                            "display_time": display_time,
                            "name": data.get("initial_name", data.get("name", "李蓝宝")),
                            "message_count": len(data.get("message", [])),
                            "file_mtime": os.path.getmtime(file_path)
                        })
                except Exception:
                    # 容错：跳过损坏的 JSON 文件
                    continue

    sessions.sort(key=lambda x: x["file_mtime"], reverse=True)
    return sessions


@app.get("/api/sessions/{session_id}")
def get_single_session(session_id: str, uid: str):
    file_path = get_session_file_path(uid, session_id)
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            raise HTTPException(status_code=500, detail="文件读取错误")
    raise HTTPException(status_code=404, detail="会话不存在")


@app.delete("/api/sessions/{session_id}")
def delete_session(session_id: str, uid: str):
    file_path = get_session_file_path(uid, session_id)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return {"status": "success"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(status_code=404, detail="会话不存在")


@app.post("/api/chat/completions")
def chat_completions(request: ChatRequest):
    # 接收来自前端创建或者原有的 session_id
    session_id = request.session_id if request.session_id else get_beijing_time_str()
    file_path = get_session_file_path(request.uid, session_id)

    history_messages = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            history_messages = data.get("message", [])

    history_messages.append({
        "role": "user",
        "content": request.content,
        "avatar": request.user_avatar
    })

    role_type = request.role_config.role_type

    # 核心设定：根据前端传来的 role_type 自动路由 Prompt
    if role_type == "誊思致雪":
        sys_prompt = TENG_SI_ZHI_XUE_PROMPT
    elif role_type == "薇尔莉特":
        sys_prompt = VIOLET_PROMPT
    else:
        sys_prompt = DEFAULT_PROMPT_TEMPLATE.format(
            name=request.role_config.name,
            nature=request.role_config.nature
        ).strip()

    api_messages = [{"role": "system", "content": sys_prompt}]
    recent_messages = history_messages[-30:]
    while recent_messages and recent_messages[0]["role"] != "user":
        recent_messages.pop(0)

    for msg in recent_messages:
        api_messages.append({"role": msg["role"], "content": msg["content"]})

    def generate_stream():
        full_response = ""
        try:
            response = client.chat.completions.create(
                model=DEEPSEEK_MODEL,
                messages=api_messages,
                stream=True,
                temperature=0.8,
                max_tokens=1024
            )
            for chunk in response:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if getattr(delta, 'reasoning_content', None):
                        continue
                    if delta.content:
                        content = delta.content
                        full_response += content
                        yield content
        except Exception as e:
            error_msg = f"\n[连接异常: {str(e)}]"
            full_response += error_msg
            yield error_msg
        finally:
            clean_response = THINK_PATTERN.sub('', full_response).strip()
            if not clean_response:
                clean_response = "网络似乎开小差了，请重试..."

            history_messages.append({
                "role": "assistant",
                "content": clean_response,
                "avatar": request.ai_avatar
            })

            # 【架构优化】后端存储记录时，内置角色的设定值完全由后端接管
            actual_nature = request.role_config.nature if role_type == "自定义" else "系统内置设定"

            session_data = {
                "time": session_id,
                "message": history_messages,
                "name": request.role_config.name,
                "nature": actual_nature,
                "provider": "deepseek",
                "initial_name": request.role_config.name
            }

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)

    # 【修复 2】：改用 application/octet-stream 并在 Cache-Control 中加入 no-transform
    # 强制废除移动端和 Nginx 等任意中间层缓存的权利，杜绝了流式输出拼包的问题。
    return StreamingResponse(
        generate_stream(),
        media_type="application/octet-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )