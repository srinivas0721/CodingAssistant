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
  
  const messagesContainer = document.getElementById('messages');
  const messageDiv = createElement('div', 'message assistant');
  const contentWrapper = document.createElement('div');
  contentWrapper.className = 'message-content';
  messageDiv.appendChild(contentWrapper);
  messagesContainer.appendChild(messageDiv);

  try {
    const response = await fetch(`${API_URL}/ask/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...currentContext,
        question: question
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let accumulatedText = '';
    let agentUsed = '';
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6));
            if (data.token) {
              accumulatedText += data.token;
              const rawHtml = marked.parse(accumulatedText);
              const sanitizedHtml = DOMPurify.sanitize(rawHtml);
              contentWrapper.innerHTML = sanitizedHtml;
              messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
            if (data.done) {
              agentUsed = data.agent_used;
            }
          } catch (e) {
            console.error('Error parsing SSE data:', e);
          }
        }
      }
    }

    if (buffer && buffer.startsWith('data: ')) {
      try {
        const data = JSON.parse(buffer.slice(6));
        if (data.token) {
          accumulatedText += data.token;
          const rawHtml = marked.parse(accumulatedText);
          const sanitizedHtml = DOMPurify.sanitize(rawHtml);
          contentWrapper.innerHTML = sanitizedHtml;
          messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
        if (data.done) {
          agentUsed = data.agent_used;
        }
      } catch (e) {
        console.error('Error parsing final SSE data:', e);
      }
    }

    if (agentUsed) {
      const badge = createElement('div', 'agent-badge', agentUsed);
      messageDiv.appendChild(badge);
    }
    
    chatHistory.push({
      question: question,
      answer: accumulatedText,
      agent: agentUsed
    });

  } catch (error) {
    contentWrapper.textContent = `Error: ${error.message}. Make sure the backend is running on ${API_URL}`;
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
