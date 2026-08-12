let currentChatId = null;
let chats = [];

const chatList = document.querySelector("#chat-list");
const messages = document.querySelector("#messages");
const chatTitle = document.querySelector("#chat-title");
const form = document.querySelector("#guess-form");
const input = document.querySelector("#guess-input");
const newChatButton = document.querySelector("#new-chat");

async function requestJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const body = await response.json();
  if (!response.ok) {
    throw new Error(body.message || "请求失败");
  }
  if (Object.prototype.hasOwnProperty.call(body, "code") && body.code !== 0) {
    throw new Error(body.message || "请求失败");
  }
  return Object.prototype.hasOwnProperty.call(body, "data") ? body.data : body;
}

function renderChatList() {
  chatList.innerHTML = "";
  chats = Array.isArray(chats) ? chats : [];
  if (chats.length === 0) {
    chatList.innerHTML = '<div class="empty">暂无游戏</div>';
    return;
  }

  [...chats].reverse().forEach((chat) => {
    const row = document.createElement("div");
    row.className = "chat-row";

    const button = document.createElement("button");
    button.type = "button";
    button.className = `chat-button${chat.id === currentChatId ? " active" : ""}`;
    button.textContent = `🪄 ${chat.title}`;
    button.title = chat.title;
    button.addEventListener("click", () => selectChat(chat.id));

    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.className = "delete-button";
    deleteButton.textContent = "×";
    deleteButton.title = "删除聊天";
    deleteButton.addEventListener("click", (event) => {
      event.stopPropagation();
      deleteChat(chat.id);
    });

    row.append(button, deleteButton);
    chatList.append(row);
  });
}

function renderMessages(chat) {
  chat = chat || { title: "-", messages: [] };
  chatTitle.textContent = chat.title;
  messages.innerHTML = "";

  const chatMessages = Array.isArray(chat.messages) ? chat.messages : [];
  chatMessages.forEach((message) => {
    const item = document.createElement("div");
    item.className = `message ${message.role}`;

    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = message.role === "user" ? "🤓" : "🪄";

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = message.content;

    item.append(avatar, bubble);
    messages.append(item);
  });

  messages.scrollTop = messages.scrollHeight;
}

async function loadChats(preferredChatId = null) {
  const data = await requestJson("/api/chats");
  chats = Array.isArray(data.chats) ? data.chats : [];
  const preferredExists = preferredChatId && chats.some((chat) => chat.id === preferredChatId);
  currentChatId = preferredExists ? preferredChatId : data.current_chat_id;
  renderChatList();
  if (currentChatId) {
    await selectChat(currentChatId);
  }
}

async function selectChat(chatId) {
  currentChatId = chatId;
  renderChatList();
  const chat = await requestJson(`/api/chats/${encodeURIComponent(chatId)}`);
  renderMessages(chat);
}

async function createChat() {
  const chat = await requestJson("/api/chats", { method: "POST" });
  await loadChats(chat.id);
  input.focus();
}

async function deleteChat(chatId) {
  const data = await requestJson(`/api/chats/${encodeURIComponent(chatId)}`, { method: "DELETE" });
  chats = Array.isArray(data.chats) ? data.chats : [];
  currentChatId = data.current_chat_id;
  renderChatList();
  if (currentChatId) {
    await selectChat(currentChatId);
  } else {
    messages.innerHTML = "";
    chatTitle.textContent = "-";
  }
}

async function sendGuess(event) {
  event.preventDefault();
  const content = input.value.trim();
  if (!content || !currentChatId) {
    return;
  }

  input.value = "";
  const chat = await requestJson(`/api/chats/${encodeURIComponent(currentChatId)}/guess`, {
    method: "POST",
    body: JSON.stringify({ content }),
  });
  renderMessages(chat);
  await loadChats(currentChatId);
}

newChatButton.addEventListener("click", createChat);
form.addEventListener("submit", sendGuess);

loadChats().catch((error) => {
  messages.innerHTML = `<div class="empty">${error.message}</div>`;
});
