const API_URL = 'https://codingassistant-q24x.onrender.com';

function loadMarkedLibrary() {
  return new Promise((resolve) => {
    if (window.marked && window.DOMPurify) {
      resolve();
      return;
    }
    
    let loadedCount = 0;
    const checkComplete = () => {
      loadedCount++;
      if (loadedCount === 2) resolve();
    };
    
    const markedScript = document.createElement('script');
    markedScript.src = 'https://cdn.jsdelivr.net/npm/marked/marked.min.js';
    markedScript.onload = checkComplete;
    document.head.appendChild(markedScript);
    
    const purifyScript = document.createElement('script');
    purifyScript.src = 'https://cdn.jsdelivr.net/npm/dompurify@3.0.6/dist/purify.min.js';
    purifyScript.onload = checkComplete;
    document.head.appendChild(purifyScript);
  });
}

function extractCodeChefContext() {
  const context = {
    site: 'codechef',
    problem_title: '',
    problem_statement: '',
    user_code: '',
    language: 'unknown'
  };

  const titleElement = document.querySelector('.problem-heading h1') ||
                       document.querySelector('[class*="ProblemName"]');
  if (titleElement) {
    context.problem_title = titleElement.textContent.trim();
  }

  const problemStatement = document.querySelector('.problem-statement') ||
                          document.querySelector('[class*="ProblemStatement"]') ||
                          document.querySelector('#problem-statement');
  if (problemStatement) {
    context.problem_statement = problemStatement.innerText.trim();
  }

  const codeEditor = document.querySelector('.CodeMirror') ||
                     document.querySelector('textarea[name="source"]');
  if (codeEditor) {
    if (codeEditor.classList.contains('CodeMirror')) {
      const cm = codeEditor.CodeMirror;
      if (cm) {
        context.user_code = cm.getValue();
      }
    } else if (codeEditor.tagName === 'TEXTAREA') {
      context.user_code = codeEditor.value;
    }
  }

  const langSelector = document.querySelector('select[name="language"]') ||
                      document.querySelector('[class*="LanguageSelect"]');
  if (langSelector) {
    if (langSelector.tagName === 'SELECT') {
      context.language = langSelector.options[langSelector.selectedIndex].text.toLowerCase();
    } else {
      context.language = langSelector.textContent.trim().toLowerCase();
    }
  }

  return context;
}

async function createChatModal() {
  await loadMarkedLibrary();
  
  if (document.getElementById('cp-assistant-modal')) {
    document.getElementById('cp-assistant-modal').style.display = 'flex';
    return;
  }

  const modal = document.createElement('div');
  modal.id = 'cp-assistant-modal';
  modal.innerHTML = `
    <div class="cp-modal-overlay">
      <div class="cp-modal-content">
        <div class="cp-modal-header">
          <span>💬 CP Assistant</span>
          <button class="cp-close-btn">&times;</button>
        </div>
        <div class="cp-modal-messages" id="cp-messages"></div>
        <div class="cp-modal-input">
          <input type="text" id="cp-input" placeholder="Ask me anything..." />
          <button id="cp-send-btn">Send</button>
        </div>
      </div>
    </div>
  `;

  const styles = document.createElement('style');
  styles.textContent = `
    #cp-assistant-modal {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 999999;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .cp-modal-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .cp-modal-content {
      background: white;
      width: 500px;
      height: 600px;
      border-radius: 12px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    }
    .cp-modal-header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 16px;
      border-radius: 12px 12px 0 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 600;
    }
    .cp-close-btn {
      background: none;
      border: none;
      color: white;
      font-size: 28px;
      cursor: pointer;
      line-height: 1;
      padding: 0;
      width: 30px;
      height: 30px;
    }
    .cp-modal-messages {
      flex: 1;
      overflow-y: auto;
      padding: 16px;
      background: #f7fafc;
    }
    .cp-message {
      margin-bottom: 12px;
      padding: 12px;
      border-radius: 8px;
      max-width: 85%;
    }
    .cp-message.user {
      background: #667eea;
      color: white;
      margin-left: auto;
    }
    .cp-message.assistant {
      background: white;
      color: #2d3748;
      border: 1px solid #e2e8f0;
    }
    .cp-message.loading {
      background: white;
      color: #718096;
      font-style: italic;
      border: 1px solid #e2e8f0;
    }
    .cp-modal-input {
      padding: 16px;
      background: white;
      border-top: 1px solid #e2e8f0;
      display: flex;
      gap: 8px;
      border-radius: 0 0 12px 12px;
    }
    .cp-modal-input input {
      flex: 1;
      padding: 10px 12px;
      border: 1px solid #cbd5e0;
      border-radius: 6px;
      font-size: 14px;
      font-family: inherit;
    }
    .cp-modal-input input:focus {
      outline: none;
      border-color: #667eea;
    }
    .cp-modal-input button {
      padding: 10px 20px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-weight: 600;
    }
    .cp-agent-badge {
      font-size: 11px;
      background: #edf2f7;
      color: #4a5568;
      padding: 2px 8px;
      border-radius: 4px;
      margin-top: 8px;
      display: inline-block;
    }
    .message-content h1, .message-content h2, .message-content h3 {
      margin-top: 16px;
      margin-bottom: 8px;
      color: #2d3748;
      font-weight: 600;
    }
    .message-content h1 { font-size: 1.4em; }
    .message-content h2 { font-size: 1.2em; }
    .message-content h3 { font-size: 1.1em; }
    .message-content p {
      margin: 8px 0;
      line-height: 1.6;
    }
    .message-content ul, .message-content ol {
      margin: 8px 0;
      padding-left: 24px;
    }
    .message-content li {
      margin: 4px 0;
      line-height: 1.5;
    }
    .message-content code {
      background: #f7fafc;
      padding: 2px 6px;
      border-radius: 3px;
      font-family: 'Courier New', monospace;
      font-size: 0.9em;
      color: #c7254e;
    }
    .message-content pre {
      background: #f7fafc;
      padding: 12px;
      border-radius: 6px;
      overflow-x: auto;
      margin: 8px 0;
    }
    .message-content pre code {
      background: none;
      padding: 0;
      color: #2d3748;
    }
    .message-content strong {
      font-weight: 600;
      color: #2d3748;
    }
    .message-content em {
      font-style: italic;
    }
    .message-content blockquote {
      border-left: 3px solid #667eea;
      padding-left: 12px;
      margin: 8px 0;
      color: #4a5568;
      font-style: italic;
    }
  `;

  document.head.appendChild(styles);
  document.body.appendChild(modal);

  const context = extractCodeChefContext();

  document.querySelector('.cp-close-btn').addEventListener('click', () => {
    modal.style.display = 'none';
  });

  document.querySelector('.cp-modal-overlay').addEventListener('click', (e) => {
    if (e.target.classList.contains('cp-modal-overlay')) {
      modal.style.display = 'none';
    }
  });

  const sendMessage = async () => {
    const input = document.getElementById('cp-input');
    const question = input.value.trim();
    if (!question) return;

    const messagesDiv = document.getElementById('cp-messages');
    
    const userMsg = document.createElement('div');
    userMsg.className = 'cp-message user';
    userMsg.textContent = question;
    messagesDiv.appendChild(userMsg);

    const loadingMsg = document.createElement('div');
    loadingMsg.className = 'cp-message loading';
    loadingMsg.textContent = 'Thinking...';
    messagesDiv.appendChild(loadingMsg);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    input.value = '';

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...context,
          question: question
        })
      });

      loadingMsg.remove();

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      const assistantMsg = document.createElement('div');
      assistantMsg.className = 'cp-message assistant';
      
      const contentWrapper = document.createElement('div');
      contentWrapper.className = 'message-content';
      const rawHtml = marked.parse(data.answer);
      const sanitizedHtml = DOMPurify.sanitize(rawHtml);
      contentWrapper.innerHTML = sanitizedHtml;
      assistantMsg.appendChild(contentWrapper);
      
      const badge = document.createElement('div');
      badge.className = 'cp-agent-badge';
      badge.textContent = data.agent_used;
      assistantMsg.appendChild(badge);
      
      messagesDiv.appendChild(assistantMsg);
      messagesDiv.scrollTop = messagesDiv.scrollHeight;

    } catch (error) {
      loadingMsg.remove();
      const errorMsg = document.createElement('div');
      errorMsg.className = 'cp-message assistant';
      errorMsg.textContent = `Error: ${error.message}. Make sure the backend is running.`;
      messagesDiv.appendChild(errorMsg);
      messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
  };

  document.getElementById('cp-send-btn').addEventListener('click', sendMessage);
  document.getElementById('cp-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
  });
}

function injectChatButton() {
  if (document.getElementById('cp-assistant-btn')) return;

  const button = document.createElement('button');
  button.id = 'cp-assistant-btn';
  button.innerHTML = '💬 CP Assistant';
  button.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 10000;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 25px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    transition: all 0.3s ease;
  `;

  button.addEventListener('mouseenter', () => {
    button.style.transform = 'translateY(-2px)';
    button.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.6)';
  });

  button.addEventListener('mouseleave', () => {
    button.style.transform = 'translateY(0)';
    button.style.boxShadow = '0 4px 15px rgba(102, 126, 234, 0.4)';
  });

  button.addEventListener('click', createChatModal);

  document.body.appendChild(button);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', injectChatButton);
} else {
  injectChatButton();
}
