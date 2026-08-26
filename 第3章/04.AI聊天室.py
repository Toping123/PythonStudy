from datetime import datetime
import json
import os
from pathlib import Path
from typing import MutableMapping


DEFAULT_NICKNAME = "Toping"
DEFAULT_PERSONALITY = "活泼开朗的小伙"
DEFAULT_MODEL = "deepseek-v4-pro"
DEFAULT_DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEFAULT_STORAGE_PATH = Path(__file__).with_name("ai_chatroom_history")


try:
    import streamlit as st
except ModuleNotFoundError:
    st = None


def create_conversation_title() -> str:
    """创建类似 2026-01-14_10-54-21 的会话标题。"""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def normalize_conversation(
    conversation_id: str,
    conversation: MutableMapping,
) -> MutableMapping:
    """补齐会话字段。"""
    conversation.setdefault("id", conversation_id)
    conversation.setdefault("title", conversation_id)
    conversation.setdefault("messages", [])
    conversation.setdefault("nickname", DEFAULT_NICKNAME)
    conversation.setdefault("personality", DEFAULT_PERSONALITY)
    return conversation


def get_conversation_button_type(is_current: bool) -> str:
    """当前会话使用 primary 按钮样式，普通会话使用 secondary。"""
    return "primary" if is_current else "secondary"


def get_conversation_persona(
    state: MutableMapping,
    conversation_id: str | None = None,
) -> tuple[str, str]:
    """读取指定会话的独立昵称与性格。"""
    conversations = state.setdefault("conversations", {})
    selected_id = conversation_id or state.get("current_conversation_id")
    conversation = conversations.get(selected_id, {})
    return (
        conversation.get("nickname") or DEFAULT_NICKNAME,
        conversation.get("personality") or DEFAULT_PERSONALITY,
    )


def set_conversation_persona(
    state: MutableMapping,
    conversation_id: str,
    nickname: str,
    personality: str,
) -> None:
    """更新指定会话的独立昵称与性格。"""
    conversations = state.setdefault("conversations", {})
    conversation = conversations[conversation_id]
    conversation["nickname"] = nickname.strip() or DEFAULT_NICKNAME
    conversation["personality"] = personality.strip() or DEFAULT_PERSONALITY


def new_conversation(state: MutableMapping) -> str:
    """新建会话并切换到该会话；当前会话为空时不重复创建。"""
    conversations = state.setdefault("conversations", {})
    current_id = state.get("current_conversation_id")
    if current_id in conversations:
        current_conversation = normalize_conversation(
            current_id,
            conversations[current_id],
        )
        if not current_conversation["messages"]:
            return current_id

    nickname, personality = get_conversation_persona(state, current_id)
    conversation_id = create_conversation_title()
    counter = 1

    while conversation_id in conversations:
        counter += 1
        conversation_id = f"{create_conversation_title()}_{counter}"

    conversations[conversation_id] = {
        "title": conversation_id,
        "nickname": nickname,
        "personality": personality,
        "messages": [],
    }
    state["current_conversation_id"] = conversation_id
    return conversation_id


def load_persistent_state(storage_path: str | Path = DEFAULT_STORAGE_PATH) -> dict:
    """从本地目录读取历史会话；每个会话对应一个 JSON 文件。"""
    path = Path(storage_path)
    if not path.is_dir():
        return {}

    try:
        current_data = json.loads((path / "current.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        current_data = {}

    conversations = {}
    for conversation_path in sorted(path.glob("*.json")):
        if conversation_path.name == "current.json":
            continue
        try:
            conversation = json.loads(conversation_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(conversation, dict):
            continue

        conversation_id = conversation.get("id") or conversation_path.stem
        conversations[conversation_id] = normalize_conversation(
            conversation_id,
            conversation,
        )

    if not conversations:
        return {}

    return {
        "current_conversation_id": current_data.get("current_conversation_id"),
        "conversations": conversations,
    }


def save_persistent_state(
    state: MutableMapping,
    storage_path: str | Path = DEFAULT_STORAGE_PATH,
) -> None:
    """把聊天状态保存到本地目录：当前会话索引 + 每会话单独 JSON。"""
    path = Path(storage_path)
    path.mkdir(parents=True, exist_ok=True)

    current_id = state.get("current_conversation_id")
    active_filenames = {"current.json"}
    for conversation_id, conversation in state.get("conversations", {}).items():
        normalize_conversation(conversation_id, conversation)
        conversation_path = path / f"{conversation_id}.json"
        temp_conversation_path = conversation_path.with_suffix(".json.tmp")
        temp_conversation_path.write_text(
            json.dumps(conversation, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temp_conversation_path.replace(conversation_path)
        active_filenames.add(conversation_path.name)

    current_data = {
        "current_conversation_id": current_id,
    }
    current_path = path / "current.json"
    temp_current_path = current_path.with_suffix(".json.tmp")
    temp_current_path.write_text(
        json.dumps(current_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temp_current_path.replace(current_path)

    for json_path in path.glob("*.json"):
        if json_path.name not in active_filenames:
            json_path.unlink()


def ensure_session_state(
    state: MutableMapping,
    storage_path: str | Path = DEFAULT_STORAGE_PATH,
) -> None:
    """初始化 Streamlit 会话状态。"""
    if not state.get("_persistent_state_loaded"):
        persisted_state = load_persistent_state(storage_path)
        for key in ("current_conversation_id", "conversations"):
            if key in persisted_state and key not in state:
                state[key] = persisted_state[key]
        state["_persistent_state_loaded"] = True

    state.setdefault("conversations", {})

    if not state["conversations"]:
        new_conversation(state)
    else:
        for conversation_id, conversation in state["conversations"].items():
            normalize_conversation(
                conversation_id,
                conversation,
            )

    current_id = state.get("current_conversation_id")
    if current_id not in state["conversations"]:
        state["current_conversation_id"] = next(iter(state["conversations"]))


def delete_conversation(state: MutableMapping, conversation_id: str) -> None:
    """删除会话；如果删空，则自动补一个新会话。"""
    conversations = state.setdefault("conversations", {})
    conversations.pop(conversation_id, None)

    if not conversations:
        new_conversation(state)
        return

    if state.get("current_conversation_id") == conversation_id:
        state["current_conversation_id"] = next(iter(conversations))


def build_system_prompt(nickname: str, personality: str) -> str:
    """根据侧边栏配置生成 AI 角色提示词。"""
    safe_nickname = nickname.strip() or DEFAULT_NICKNAME
    safe_personality = personality.strip() or DEFAULT_PERSONALITY
    return (
        f"你的昵称是「{safe_nickname}」。"
        f"你的性格设定是：{safe_personality}。"
        "请始终用这个人设与用户自然聊天，回答要真诚、简洁、有温度。"
    )


if st is not None:
    @st.cache_resource
    def get_openai_client(api_key: str, base_url: str | None):
        """缓存 OpenAI 兼容客户端，避免每次刷新页面都重新创建。"""
        from openai import OpenAI

        return OpenAI(api_key=api_key, base_url=base_url)
else:
    def get_openai_client(api_key: str, base_url: str | None):
        """测试环境没有 Streamlit 时的兜底实现。"""
        from openai import OpenAI

        return OpenAI(api_key=api_key, base_url=base_url)


def get_api_config() -> tuple[str | None, str | None, str]:
    """读取 API 配置，优先 OpenAI，兼容课程里的 DeepSeek 示例。"""
    openai_key = os.environ.get("OPENAI_API_KEY")
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
    api_key = openai_key or deepseek_key

    base_url = os.environ.get("OPENAI_BASE_URL")
    if not openai_key and deepseek_key:
        base_url = base_url or DEFAULT_DEEPSEEK_BASE_URL

    model = os.environ.get("OPENAI_MODEL") or os.environ.get("DEEPSEEK_MODEL") or DEFAULT_MODEL
    return api_key, base_url, model


def ask_ai(messages: list[dict[str, str]], nickname: str, personality: str) -> str:
    """调用 OpenAI 兼容聊天接口。"""
    api_key, base_url, model = get_api_config()
    if not api_key:
        return "还没有配置 API Key。请先设置环境变量 OPENAI_API_KEY 或 DEEPSEEK_API_KEY。"

    client = get_openai_client(api_key, base_url)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": build_system_prompt(nickname, personality)},
            *messages,
        ],
        stream=False,
    )
    return response.choices[0].message.content


def render_sidebar() -> None:
    """渲染左侧控制面板。"""
    st.sidebar.markdown("## AI控制面板")

    if st.sidebar.button("🖊️ 新建会话", use_container_width=True):
        new_conversation(st.session_state)
        save_persistent_state(st.session_state)
        st.rerun()

    st.sidebar.markdown("### 会话历史")
    conversations = list(st.session_state["conversations"].items())
    for conversation_id, conversation in conversations:
        cols = st.sidebar.columns([4, 1])
        is_current = conversation_id == st.session_state["current_conversation_id"]
        button_label = f"📄 {conversation["title"]}"
        button_type = get_conversation_button_type(is_current)

        if cols[0].button(
            button_label,
            key=f"switch_{conversation_id}",
            use_container_width=True,
            type=button_type,
        ):
            st.session_state["current_conversation_id"] = conversation_id
            save_persistent_state(st.session_state)
            st.rerun()

        if cols[1].button("❌", key=f"delete_{conversation_id}", use_container_width=True):
            delete_conversation(st.session_state, conversation_id)
            save_persistent_state(st.session_state)
            st.rerun()
    st.sidebar.markdown("### AI助手信息")
    current_id = st.session_state["current_conversation_id"]
    current_nickname, current_personality = get_conversation_persona(st.session_state, current_id)
    nickname = st.sidebar.text_input(
        "昵称",
        value=current_nickname,
        placeholder="例如：小甜甜",
        key=f"nickname_{current_id}",
    )
    personality = st.sidebar.text_area(
        "性格",
        value=current_personality,
        placeholder="例如：活泼开朗的东北姑娘",
        height=120,
        key=f"personality_{current_id}",
    )
    set_conversation_persona(st.session_state, current_id, nickname, personality)
    save_persistent_state(st.session_state)


def render_messages(current_conversation: dict) -> None:
    """渲染聊天记录。"""
    for message in current_conversation["messages"]:
        avatar = "🧑" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.write(message["content"])


def inject_style() -> None:
    """添加少量样式，让页面更接近暗色聊天窗口。"""
    st.markdown(
        """
        <style>
        .stApp {
            background: #0f1118;
            color: #f4f4f5;
        }
        section[data-testid="stSidebar"] {
            background: #2a2a38;
        }
        section[data-testid="stSidebar"] button {
            border-radius: 8px;
        }
        div[data-testid="stChatMessage"] {
            background: #1b1b27;
            border-radius: 12px;
            padding: 10px 12px;
            margin-bottom: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    """Streamlit 应用入口。"""
    if st is None:
        raise RuntimeError("请先安装 streamlit：pip install streamlit")

    st.set_page_config(
        page_title="Toping助手",
        page_icon="🤖",
        layout="wide",
    )
    inject_style()
    ensure_session_state(st.session_state)
    render_sidebar()

    current_id = st.session_state["current_conversation_id"]
    current_conversation = st.session_state["conversations"][current_id]

    st.title("🤖 Toping助手")
    render_messages(current_conversation)

    user_input = st.chat_input("请输入您要问的问题")
    if user_input:
        current_conversation["messages"].append({"role": "user", "content": user_input})
        save_persistent_state(st.session_state)
        with st.chat_message("user", avatar="🧑"):
            st.write(user_input)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("AI 正在思考..."):
                try:
                    answer = ask_ai(
                        current_conversation["messages"],
                        current_conversation["nickname"],
                        current_conversation["personality"],
                    )
                except Exception as error:
                    answer = f"调用 AI 接口失败：{error}"
                st.write(answer)

        current_conversation["messages"].append({"role": "assistant", "content": answer})
        save_persistent_state(st.session_state)


if __name__ == "__main__":
    main()
