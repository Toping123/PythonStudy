from pathlib import Path
import importlib.util
import json
import tempfile
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHATROOM_PATH = PROJECT_ROOT / "第3章" / "03. AI聊天室.py"


def load_chatroom_module():
    spec = importlib.util.spec_from_file_location("ai_chatroom", CHATROOM_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TestAiChatroom(unittest.TestCase):
    def make_storage_path(self, temp_dir: str) -> Path:
        return Path(temp_dir) / "chat_history.json"

    def test_build_system_prompt_uses_nickname_and_personality(self):
        module = load_chatroom_module()

        prompt = module.build_system_prompt("小甜甜", "活泼开朗的东北姑娘")

        self.assertIn("小甜甜", prompt)
        self.assertIn("活泼开朗的东北姑娘", prompt)

    def test_ensure_session_state_creates_one_conversation(self):
        module = load_chatroom_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            state = {}

            module.ensure_session_state(state, storage_path=self.make_storage_path(temp_dir))

            self.assertEqual(1, len(state["conversations"]))
            self.assertIn(state["current_conversation_id"], state["conversations"])

    def test_new_conversation_does_nothing_when_current_conversation_is_empty(self):
        module = load_chatroom_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            state = {}
            module.ensure_session_state(state, storage_path=self.make_storage_path(temp_dir))
            first_id = state["current_conversation_id"]

            second_id = module.new_conversation(state)

            self.assertEqual(first_id, second_id)
            self.assertEqual(1, len(state["conversations"]))

    def test_new_conversation_creates_after_current_conversation_has_messages(self):
        module = load_chatroom_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            state = {}
            module.ensure_session_state(state, storage_path=self.make_storage_path(temp_dir))
            first_id = state["current_conversation_id"]
            state["conversations"][first_id]["messages"].append(
                {"role": "user", "content": "你好"}
            )

            second_id = module.new_conversation(state)

            self.assertNotEqual(first_id, second_id)
            self.assertEqual(2, len(state["conversations"]))
            self.assertEqual(second_id, state["current_conversation_id"])

    def test_each_conversation_keeps_independent_persona(self):
        module = load_chatroom_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            state = {}
            module.ensure_session_state(state, storage_path=self.make_storage_path(temp_dir))
            first_id = state["current_conversation_id"]
            module.set_conversation_persona(state, first_id, "小红", "温柔")
            state["conversations"][first_id]["messages"].append(
                {"role": "user", "content": "你好"}
            )
            second_id = module.new_conversation(state)
            module.set_conversation_persona(state, second_id, "小蓝", "活泼")

            self.assertEqual(("小红", "温柔"), module.get_conversation_persona(state, first_id))
            self.assertEqual(("小蓝", "活泼"), module.get_conversation_persona(state, second_id))

    def test_delete_current_conversation_switches_or_recreates(self):
        module = load_chatroom_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            state = {}
            module.ensure_session_state(state, storage_path=self.make_storage_path(temp_dir))
            first_id = state["current_conversation_id"]
            state["conversations"][first_id]["messages"].append(
                {"role": "user", "content": "让当前会话不再为空"}
            )
            second_id = module.new_conversation(state)

            module.delete_conversation(state, second_id)

            self.assertEqual(first_id, state["current_conversation_id"])

            module.delete_conversation(state, first_id)

            self.assertEqual(1, len(state["conversations"]))
            self.assertIn(state["current_conversation_id"], state["conversations"])

    def test_save_and_load_persistent_state_round_trips_conversations(self):
        module = load_chatroom_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            storage_path = self.make_storage_path(temp_dir)
            state = {}
            module.ensure_session_state(state, storage_path=storage_path)
            current_id = state["current_conversation_id"]
            state["conversations"][current_id]["messages"].append(
                {"role": "user", "content": "之前聊过什么？"}
            )
            module.set_conversation_persona(state, current_id, "Toping", "耐心温柔的编程助手")

            module.save_persistent_state(state, storage_path)
            loaded = module.load_persistent_state(storage_path)
            saved_json = json.loads(storage_path.read_text(encoding="utf-8"))

            self.assertNotIn("nickname", saved_json)
            self.assertNotIn("personality", saved_json)
            self.assertEqual(current_id, loaded["current_conversation_id"])
            self.assertEqual(
                "Toping",
                loaded["conversations"][current_id]["nickname"],
            )
            self.assertEqual(
                "耐心温柔的编程助手",
                loaded["conversations"][current_id]["personality"],
            )
            self.assertEqual(
                [{"role": "user", "content": "之前聊过什么？"}],
                loaded["conversations"][current_id]["messages"],
            )

    def test_ensure_session_state_loads_saved_conversations_on_startup(self):
        module = load_chatroom_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            storage_path = self.make_storage_path(temp_dir)
            storage_path.write_text(
                json.dumps(
                    {
                        "current_conversation_id": "old-session",
                        "conversations": {
                            "old-session": {
                                "title": "old-session",
                                "nickname": "历史助手",
                                "personality": "记性很好",
                                "messages": [{"role": "assistant", "content": "我还记得。"}],
                            }
                        },
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            state = {}

            module.ensure_session_state(state, storage_path=storage_path)

            self.assertEqual("old-session", state["current_conversation_id"])
            self.assertEqual(
                ("历史助手", "记性很好"),
                module.get_conversation_persona(state, "old-session"),
            )
            self.assertEqual(
                [{"role": "assistant", "content": "我还记得。"}],
                state["conversations"]["old-session"]["messages"],
            )


if __name__ == "__main__":
    unittest.main()
