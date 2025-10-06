const API_URL = CONFIG.API_URL;

let currentContext = null;
let chatHistory = [];


function createElement(tag, className, textContent) {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (textContent) el.textContent = textContent;
  return el;
}

function addMessage(content, type, agentUsed = null) {
  const messagesContainer = document.getElementById('messages');
  const messageDiv = createElement('div', `message ${type}`);
  
  if (type === 'assistant') {
    const contentWrapper = document.createElement('div');
    contentWrapper.className = 'message-content';
    const rawHtml = marked.parse(content);
    const sanitizedHtml = DOMPurify.sanitize(rawHtml);
    contentWrapper.innerHTML = sanitizedHtml;
    messageDiv.appendChild(contentWrapper);
  } else {
    messageDiv.textContent = content;
  }
  
  if (agentUsed) {
    const badge = createElement('div', 'agent-badge', `${agentUsed}`);
    messageDiv.appendChild(badge);
  }
  
  messagesContainer.appendChild(messageDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

async function sendMessage(question) {
  if (!question.trim() || !currentContext) return;

  addMessage(question, 'user');
  
  const loadingDiv = createElement('div', 'message loading', 'Thinking...');
  const messagesContainer = document.getElementById('messages');
  messagesContainer.appendChild(loadingDiv);

  try {
    const response = await fetch(`${API_URL}/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...currentContext,
        question: question
      })
    });

    loadingDiv.remove();

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    addMessage(data.answer, 'assistant', data.agent_used);
    
    chatHistory.push({
      question: question,
      answer: data.answer,
      agent: data.agent_used
    });

  } catch (error) {
    loadingDiv.remove();
    addMessage(`Error: ${error.message}. Make sure the backend is running on ${API_URL}`, 'assistant');
  }

  document.getElementById('input').value = '';
}

async function initializeChat() {
  
  const root = document.getElementById('root');
  
  root.innerHTML = `
    <div class="chat-container">
      <div class="chat-header">💬 CP Assistant</div>
      <div id="messages" class="chat-messages"></div>
      <div class="chat-input-container">
        <div class="chat-input">
          <input 
            type="text" 
            id="input" 
            placeholder="Ask me anything about this problem..."
            autocomplete="off"
          />
          <button id="send">Send</button>
        </div>
      </div>
    </div>
  `;

  chrome.storage.local.get(['context'], (result) => {
    if (result.context) {
      currentContext = result.context;
      const site = currentContext.site.charAt(0).toUpperCase() + currentContext.site.slice(1);
      addMessage(`Connected to ${site}${currentContext.problem_title ? ': ' + currentContext.problem_title : ''}. How can I help you?`, 'assistant');
    } else {
      addMessage('Please open this from a coding platform (LeetCode, Codeforces, or CodeChef)', 'assistant');
    }
  });

  const input = document.getElementById('input');
  const sendBtn = document.getElementById('send');

  sendBtn.addEventListener('click', () => {
    sendMessage(input.value);
  });

  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      sendMessage(input.value);
    }
  });
}

document.addEventListener('DOMContentLoaded', initializeChat);
