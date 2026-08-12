const assert = require("assert");
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const projectRoot = path.resolve(__dirname, "..");
const appPath = path.join(projectRoot, "第7章", "static", "app.js");
const appCode = fs.readFileSync(appPath, "utf8");

function createElement(tagName) {
  const element = {
    tagName,
    _innerHTML: "",
    textContent: "",
    title: "",
    className: "",
    type: "",
    scrollTop: 0,
    scrollHeight: 0,
    children: [],
    classList: { add() {} },
    append(...items) {
      this.children.push(...items);
    },
    addEventListener() {},
    focus() {},
  };
  Object.defineProperty(element, "innerHTML", {
    get() {
      return this._innerHTML;
    },
    set(value) {
      this._innerHTML = value;
      this.children = [];
    },
  });
  return element;
}

const elements = new Map([
  ["#chat-list", createElement("div")],
  ["#messages", createElement("section")],
  ["#chat-title", createElement("span")],
  ["#guess-form", createElement("form")],
  ["#guess-input", createElement("input")],
  ["#new-chat", createElement("button")],
]);

const context = {
  console,
  document: {
    querySelector(selector) {
      return elements.get(selector);
    },
    createElement,
  },
  fetch: async (url) => {
    const chat = {
      id: "2026-08-12_11-18-24",
      title: "2026-08-12_11-18-24",
      created_at: "2026-08-12_11-18-24",
      messages: [{ role: "assistant", content: "DeepSeek 出题" }],
    };
    const data = url === "/api/chats"
      ? {
          current_chat_id: chat.id,
          chats: [{ ...chat, message_count: 1 }],
        }
      : chat;

    return {
      ok: true,
      json: async () => ({ code: 0, message: "success", data }),
    };
  },
};

vm.createContext(context);
vm.runInContext(appCode, context);

async function main() {
  await context.loadChats();
  assert.strictEqual(elements.get("#chat-list").children.length, 1);
  assert.strictEqual(elements.get("#chat-title").textContent, "2026-08-12_11-18-24");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
