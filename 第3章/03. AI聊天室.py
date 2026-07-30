from datetime import datetime
import os
from typing import MutableMapping


DEFAULT_NICKNAME = "Toping"
DEFAULT_PERSONALITY = "活泼开朗的小伙"
DEFAULT_MODEL = "deepseek-v4-pro"
DEFAULT_DEEPSEEK_BASE_URL = "https://api.deepseek.com"


try:
    import streamlit as st
except ModuleNotFoundError:
    st = None


def create_conversation_title() -> str:
    """创建类似 2026-01-14_10-54-21 的会话标题。"""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def new_conversation(state: MutableMapping) -> str:
    """新建会话并切换到该会话。"""
    conversation_id = create_conversation_title()
    counter = 1
    conversations = state.setdefault("conversations", {})

    while conversation_id in conversations:
        counter += 1
        conversation_id = f"{create_conversation_title()}_{counter}"

    conversations[conversation_id] = {
        "title": conversation_id,
        "messages": [],
    }
    state["current_conversation_id"] = conversation_id
    return conversation_id


def ensure_session_state(state: MutableMapping) -> None:
    """初始化 Streamlit 会话状态。"""
    state.setdefault("nickname", DEFAULT_NICKNAME)
    state.setdefault("personality", DEFAULT_PERSONALITY)
    state.setdefault("conversations", {})

    if not state["conversations"]:
        new_conversation(state)

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
        st.rerun()

    st.sidebar.markdown("### 会话历史")
    conversations = list(st.session_state["conversations"].items())
    for conversation_id, conversation in conversations:
        cols = st.sidebar.columns([4, 1])
        is_current = conversation_id == st.session_state["current_conversation_id"]
        button_label = f"📄 {conversation['title']}"

        if cols[0].button(button_label, key=f"switch_{conversation_id}", use_container_width=True):
            st.session_state["current_conversation_id"] = conversation_id
            st.rerun()

        if cols[1].button("❌", key=f"delete_{conversation_id}", use_container_width=True):
            delete_conversation(st.session_state, conversation_id)
            st.rerun()

        if is_current:
            st.sidebar.caption("当前会话")

    st.sidebar.markdown("### AI助手信息")
    st.session_state["nickname"] = st.sidebar.text_input(
        "昵称",
        value=st.session_state["nickname"],
        placeholder="例如：小甜甜",
    )
    st.session_state["personality"] = st.sidebar.text_area(
        "性格",
        value=st.session_state["personality"],
        placeholder="例如：活泼开朗的东北姑娘",
        height=120,
    )


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
        with st.chat_message("user", avatar="🧑"):
            st.write(user_input)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("AI 正在思考..."):
                try:
                    answer = ask_ai(
                        current_conversation["messages"],
                        st.session_state["nickname"],
                        st.session_state["personality"],
                    )
                except Exception as error:
                    answer = f"调用 AI 接口失败：{error}"
                st.write(answer)

        current_conversation["messages"].append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()
