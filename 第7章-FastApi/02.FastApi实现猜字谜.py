from datetime import datetime
import json
import logging
import os
from pathlib import Path
from typing import Any, Protocol

import uvicorn
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.responses import JSONResponse


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_STORAGE_PATH = BASE_DIR / "riddle_chat_history"
STATIC_DIR = BASE_DIR / "static"
DEFAULT_DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEFAULT_DEEPSEEK_MODEL = "deepseek-chat"

SYSTEM_PROMPT = (
    "你是一个汉字字谜游戏主持人。你负责出题、判断用户答案、给提示并推进下一题。"
    "规则：每次只围绕一个汉字字谜互动；用户答错时不要直接公布答案，只给一个简短提示；"
    "用户答对或要求新题时，再出一道新的汉字字谜；回复要简洁、亲切、有游戏感。"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
)
logger = logging.getLogger(__name__)


class GuessRequest(BaseModel):
    """用户提交猜字谜答案的请求体。"""

    content: str


def api_success(data: Any = None, message: str = "success") -> dict[str, Any]:
    """构造统一的成功响应结构。"""

    return {"code": 0, "message": message, "data": data}


def api_error(code: int, message: str, data: Any = None) -> dict[str, Any]:
    """构造统一的错误响应结构。"""

    return {"code": code, "message": message, "data": data}


class RiddleAgent(Protocol):
    """字谜出题与判题代理协议。"""

    def start_chat(self) -> str:
        """开始一局新游戏，并返回第一条助手消息。"""

        ...

    def answer(self, chat: dict[str, Any], user_text: str) -> str:
        """根据聊天历史和用户输入生成判题回复。"""

        ...


class DeepSeekRiddleAgent:
    """使用 DeepSeek 兼容 OpenAI SDK 的聊天接口驱动猜字谜游戏。"""

    def __init__(self) -> None:
        """从环境变量读取 DeepSeek API 配置。"""

        self.api_key = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("OPENAI_API_KEY")
        self.base_url = os.environ.get("DEEPSEEK_BASE_URL") or os.environ.get(
            "OPENAI_BASE_URL",
            DEFAULT_DEEPSEEK_BASE_URL,
        )
        self.model = os.environ.get("DEEPSEEK_MODEL") or os.environ.get(
            "OPENAI_MODEL",
            DEFAULT_DEEPSEEK_MODEL,
        )
        logger.info(
            "DeepSeekRiddleAgent initialized: base_url=%s model=%s has_api_key=%s",
            self.base_url,
            self.model,
            bool(self.api_key),
        )

    def start_chat(self) -> str:
        """请求 DeepSeek 生成第一道汉字字谜。"""

        logger.info("Requesting first riddle from DeepSeek")
        return self._chat(
            [
                {
                    "role": "user",
                    "content": "请开始一局猜字谜游戏，先欢迎用户，然后给出第一道汉字字谜。不要直接说答案。",
                }
            ]
        )

    def answer(self, chat: dict[str, Any], user_text: str) -> str:
        """把当前会话上下文和用户答案发送给 DeepSeek 判题。"""

        history = [
            {"role": message["role"], "content": message["content"]}
            for message in chat.get("messages", [])
            if message.get("role") in {"user", "assistant"} and message.get("content")
        ]
        history.append({"role": "user", "content": user_text})
        logger.info(
            "Requesting riddle answer: chat_id=%s history_count=%s user_text_length=%s",
            chat.get("id"),
            len(history),
            len(user_text),
        )
        return self._chat(history)

    def _chat(self, messages: list[dict[str, str]]) -> str:
        """调用 DeepSeek 聊天接口并返回助手文本。"""

        if not self.api_key:
            logger.warning("DeepSeek API key is missing")
            return "还没有配置 DEEPSEEK_API_KEY，先在环境变量中设置后我就可以请 DeepSeek 出题了。"

        try:
            from openai import OpenAI
        except ModuleNotFoundError:
            logger.exception("openai package is not installed")
            return "还没有安装 openai 包，请先执行：pip install openai"

        logger.info("Calling DeepSeek chat completion: model=%s messages=%s", self.model, len(messages))
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages,
            ],
            stream=False,
            temperature=1.5,
        )
        logger.info("DeepSeek chat completion returned")
        return response.choices[0].message.content or "DeepSeek 暂时没有返回内容，请再试一次。"


def create_chat_id(storage_path: Path) -> str:
    """按当前创建时间生成聊天文件名，必要时追加序号避免重名。"""

    chat_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    counter = 1
    while (storage_path / f"{chat_id}.json").exists():
        counter += 1
        chat_id = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{counter}"
    logger.info("Created chat id: chat_id=%s storage_path=%s", chat_id, storage_path)
    return chat_id


def make_chat_summary(chat: dict[str, Any]) -> dict[str, Any]:
    """把完整聊天对象转换成列表展示所需的摘要数据。"""

    return {
        "id": chat["id"],
        "title": chat["title"],
        "created_at": chat["created_at"],
        "message_count": len(chat["messages"]),
    }


def load_chats(storage_path: Path) -> dict[str, dict[str, Any]]:
    """从本地目录加载所有聊天 JSON 文件。"""

    if not storage_path.is_dir():
        logger.info("Chat storage directory does not exist: storage_path=%s", storage_path)
        return {}

    chats: dict[str, dict[str, Any]] = {}
    for chat_path in sorted(storage_path.glob("*.json")):
        try:
            chat = json.loads(chat_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            logger.exception("Failed to load chat file: path=%s", chat_path)
            continue
        if not isinstance(chat, dict) or "id" not in chat:
            logger.warning("Skip invalid chat file: path=%s", chat_path)
            continue
        chats[chat["id"]] = chat

    logger.info("Loaded chats: storage_path=%s count=%s", storage_path, len(chats))
    return chats


def save_chat(storage_path: Path, chat: dict[str, Any]) -> None:
    """把单个聊天对象保存为独立 JSON 文件。"""

    storage_path.mkdir(parents=True, exist_ok=True)
    chat_path = storage_path / f"{chat['id']}.json"
    temp_path = chat_path.with_suffix(".json.tmp")
    temp_path.write_text(json.dumps(chat, ensure_ascii=False, indent=2), encoding="utf-8")
    temp_path.replace(chat_path)
    logger.info(
        "Saved chat: chat_id=%s path=%s message_count=%s",
        chat["id"],
        chat_path,
        len(chat.get("messages", [])),
    )


def create_chat(storage_path: Path, riddle_agent: RiddleAgent) -> dict[str, Any]:
    """创建新聊天并让 DeepSeek 生成第一道字谜。"""

    storage_path.mkdir(parents=True, exist_ok=True)
    chat_id = create_chat_id(storage_path)
    logger.info("Creating chat: chat_id=%s", chat_id)
    chat = {
        "id": chat_id,
        "title": chat_id,
        "created_at": chat_id,
        "messages": [{"role": "assistant", "content": riddle_agent.start_chat()}],
    }
    save_chat(storage_path, chat)
    return chat


def get_chat_or_404(storage_path: Path, chat_id: str) -> dict[str, Any]:
    """读取指定聊天；不存在时抛出 404 异常。"""

    chat_path = storage_path / f"{chat_id}.json"
    if not chat_path.exists():
        logger.warning("Chat not found: chat_id=%s path=%s", chat_id, chat_path)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="聊天不存在")
    try:
        chat = json.loads(chat_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        logger.exception("Chat file format is invalid: chat_id=%s path=%s", chat_id, chat_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="聊天文件格式错误",
        ) from error
    logger.info("Loaded chat: chat_id=%s message_count=%s", chat_id, len(chat.get("messages", [])))
    return chat


def build_chat_list_response(
    storage_path: Path,
    riddle_agent: RiddleAgent,
    current_chat_id: str | None = None,
) -> dict[str, Any]:
    """构造聊天列表响应数据，空目录时自动创建第一局游戏。"""

    chats = load_chats(storage_path)
    if not chats:
        logger.info("No chat history found; creating initial chat")
        chat = create_chat(storage_path, riddle_agent)
        chats = {chat["id"]: chat}
        current_chat_id = chat["id"]
    elif current_chat_id not in chats:
        current_chat_id = sorted(chats)[-1]

    summaries = [make_chat_summary(chats[chat_id]) for chat_id in sorted(chats)]
    logger.info("Built chat list response: current_chat_id=%s count=%s", current_chat_id, len(summaries))
    return {"current_chat_id": current_chat_id, "chats": summaries}


def create_app(
    storage_path: str | Path = DEFAULT_STORAGE_PATH,
    riddle_agent: RiddleAgent | None = None,
) -> FastAPI:
    """创建并配置 FastAPI 应用实例。"""

    storage = Path(storage_path)
    agent = riddle_agent or DeepSeekRiddleAgent()
    my_app = FastAPI(title="汉字谜盒")
    logger.info("Creating FastAPI app: storage_path=%s", storage)

    if STATIC_DIR.exists():
        logger.info("Mounting static directory: path=%s", STATIC_DIR)
        my_app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @my_app.exception_handler(HTTPException)
    def handle_http_exception(request: Request, exception: HTTPException):
        """把 HTTPException 转换成统一接口响应。"""

        logger.warning(
            "HTTP exception: method=%s path=%s status=%s detail=%s",
            request.method,
            request.url.path,
            exception.status_code,
            exception.detail,
        )
        return JSONResponse(
            status_code=exception.status_code,
            content=api_error(exception.status_code, str(exception.detail)),
        )

    @my_app.exception_handler(Exception)
    def handle_exception(request: Request, exception: Exception):
        """把未处理异常转换成统一接口响应。"""

        logger.exception("Unhandled exception: method=%s path=%s", request.method, request.url.path)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=api_error(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "服务器内部错误",
            ),
        )

    @my_app.get("/")
    def index():
        """返回猜字谜网页入口。"""

        index_path = STATIC_DIR / "index.html"
        if not index_path.exists():
            logger.warning("Static index file is missing: path=%s", index_path)
            return {"message": "请先创建 static/index.html"}
        logger.info("Serving index page: path=%s", index_path)
        return FileResponse(index_path)

    @my_app.get("/api/chats")
    def list_api_chats():
        """查询聊天列表。"""

        logger.info("API list chats")
        return api_success(build_chat_list_response(storage, agent))

    @my_app.post("/api/chats", status_code=status.HTTP_201_CREATED)
    def create_api_chat():
        """创建新聊天。"""

        logger.info("API create chat")
        return api_success(create_chat(storage, agent))

    @my_app.get("/api/chats/{chat_id}")
    def get_api_chat(chat_id: str):
        """查询单个聊天详情。"""

        logger.info("API get chat: chat_id=%s", chat_id)
        return api_success(get_chat_or_404(storage, chat_id))

    @my_app.delete("/api/chats/{chat_id}")
    def delete_api_chat(chat_id: str):
        """删除指定聊天并返回更新后的聊天列表。"""

        chat_path = storage / f"{chat_id}.json"
        if not chat_path.exists():
            logger.warning("API delete chat failed; chat not found: chat_id=%s", chat_id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="聊天不存在")
        chat_path.unlink()
        logger.info("API deleted chat: chat_id=%s path=%s", chat_id, chat_path)
        return api_success(build_chat_list_response(storage, agent))

    @my_app.post("/api/chats/{chat_id}/guess")
    def guess_api_chat(chat_id: str, request: GuessRequest):
        """提交答案并返回 DeepSeek 的判题结果。"""

        chat = get_chat_or_404(storage, chat_id)
        user_text = request.content.strip()
        logger.info("API guess chat: chat_id=%s user_text_length=%s", chat_id, len(user_text))
        reply = agent.answer(chat, user_text)
        chat["messages"].append({"role": "user", "content": user_text})
        chat["messages"].append({"role": "assistant", "content": reply})
        save_chat(storage, chat)
        return api_success(chat)

    return my_app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=int(os.environ.get("PORT", "8000")))
