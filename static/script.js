const chatWindow = document.getElementById('chat-window');
const input = document.getElementById('user-input');

function appendMessage(role, text) {
  const wrap = document.createElement('div');
  wrap.className = `msg ${role}`;

  const avatar = document.createElement('div');
  avatar.className = 'avatar';
  avatar.textContent = role === 'bot' ? '🤖' : '🧢';

  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;

  wrap.appendChild(avatar);
  wrap.appendChild(bubble);
  chatWindow.appendChild(wrap);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return wrap;
}

function showTyping() {
  const wrap = document.createElement('div');
  wrap.className = 'msg bot typing';
  wrap.id = 'typing-indicator';

  const avatar = document.createElement('div');
  avatar.className = 'avatar';
  avatar.textContent = '🤖';

  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';

  wrap.appendChild(avatar);
  wrap.appendChild(bubble);
  chatWindow.appendChild(wrap);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function removeTyping() {
  const t = document.getElementById('typing-indicator');
  if (t) t.remove();
}

async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  input.value = '';
  appendMessage('user', text);
  showTyping();

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();
    removeTyping();
    appendMessage('bot', data.response || data.error || 'Algo deu errado.');
  } catch {
    removeTyping();
    appendMessage('bot', 'Não consegui conectar ao servidor. Verifique se o Flask está rodando.');
  }
}

function sendSuggestion(btn) {
  input.value = btn.textContent;
  sendMessage();
}

input.addEventListener('keydown', e => { if (e.key === 'Enter') sendMessage(); });

window.addEventListener('load', () => {
  appendMessage('bot', 'Olá! Sou o PokeChat 👋 Pergunte-me sobre fraquezas, tipos ou o que é superefetivo contra qualquer Pokémon!');
});
