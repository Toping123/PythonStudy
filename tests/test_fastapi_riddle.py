from pathlib import Path
import importlib.util
import json
import re

from fastapi.testclient import TestClient


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RIDDLE_APP_PATH = PROJECT_ROOT / "第7章" / "02.FastApi实现猜字谜.py"


def load_riddle_module():
    spec = importlib.util.spec_from_file_location("fastapi_riddle", RIDDLE_APP_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FakeDeepSeekAgent:
    def __init__(self):
        self.started = 0
        self.guesses = []
        self.messages_at_answer = []

    def start_chat(self):
        self.started += 1
        return "DeepSeek 出题：门里站着一个人（打一字）。"

    def answer(self, chat, user_text):
        self.guesses.append((chat["id"], user_text))
        self.messages_at_answer = list(chat["messages"])
        return f"DeepSeek 判题：收到答案 {user_text}。下一题：七十二小时（打一字）。"


def assert_api_success(response, expected_status_code=200):
    assert response.status_code == expected_status_code
    body = response.json()
    assert set(body) == {"code", "message", "data"}
    assert body["code"] == 0
    assert body["message"] == "success"
    return body["data"]


def test_create_chat_writes_one_json_file_named_by_created_time(tmp_path):
    module = load_riddle_module()
    agent = FakeDeepSeekAgent()
    app = module.create_app(storage_path=tmp_path / "history", riddle_agent=agent)
    client = TestClient(app)

    response = client.post("/api/chats")

    chat = assert_api_success(response, expected_status_code=201)
    assert re.match(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}", chat["id"])
    chat_path = tmp_path / "history" / f"{chat['id']}.json"
    assert chat_path.exists()
    saved = json.loads(chat_path.read_text(encoding="utf-8"))
    assert saved["id"] == chat["id"]
    assert saved["messages"][0]["role"] == "assistant"
    assert saved["messages"][0]["content"].startswith("DeepSeek 出题")
    assert agent.started == 1


def test_list_chats_uses_unified_response_with_chat_list_data(tmp_path):
    module = load_riddle_module()
    app = module.create_app(storage_path=tmp_path / "history", riddle_agent=FakeDeepSeekAgent())
    client = TestClient(app)

    data = assert_api_success(client.get("/api/chats"))

    assert data["current_chat_id"]
    assert len(data["chats"]) == 1
    assert data["chats"][0]["id"] == data["current_chat_id"]


def test_guess_asks_deepseek_and_persists_the_reply(tmp_path):
    module = load_riddle_module()
    agent = FakeDeepSeekAgent()
    app = module.create_app(storage_path=tmp_path / "history", riddle_agent=agent)
    client = TestClient(app)
    chat_id = assert_api_success(client.post("/api/chats"), expected_status_code=201)["id"]

    response = client.post(f"/api/chats/{chat_id}/guess", json={"content": "闪"})

    data = assert_api_success(response)
    assert data["messages"][-2] == {"role": "user", "content": "闪"}
    assert data["messages"][-1] == {
        "role": "assistant",
        "content": "DeepSeek 判题：收到答案 闪。下一题：七十二小时（打一字）。",
    }
    assert agent.guesses == [(chat_id, "闪")]
    assert agent.messages_at_answer == [
        {"role": "assistant", "content": "DeepSeek 出题：门里站着一个人（打一字）。"}
    ]
    saved = json.loads((tmp_path / "history" / f"{chat_id}.json").read_text(encoding="utf-8"))
    assert saved["messages"] == data["messages"]


def test_delete_chat_removes_only_that_json_file_and_keeps_a_current_chat(tmp_path):
    module = load_riddle_module()
    app = module.create_app(storage_path=tmp_path / "history", riddle_agent=FakeDeepSeekAgent())
    client = TestClient(app)
    first_id = assert_api_success(client.post("/api/chats"), expected_status_code=201)["id"]
    second_id = assert_api_success(client.post("/api/chats"), expected_status_code=201)["id"]

    response = client.delete(f"/api/chats/{second_id}")

    data = assert_api_success(response)
    assert data["current_chat_id"] == first_id
    assert [chat["id"] for chat in data["chats"]] == [first_id]
    assert (tmp_path / "history" / f"{first_id}.json").exists()
    assert not (tmp_path / "history" / f"{second_id}.json").exists()


def test_missing_chat_uses_unified_error_response(tmp_path):
    module = load_riddle_module()
    app = module.create_app(storage_path=tmp_path / "history", riddle_agent=FakeDeepSeekAgent())
    client = TestClient(app)

    response = client.get("/api/chats/not-exists")

    assert response.status_code == 404
    body = response.json()
    assert set(body) == {"code", "message", "data"}
    assert body["code"] == 404
    assert body["message"]
    assert body["data"] is None
