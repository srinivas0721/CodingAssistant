function extractLeetCodeContext() {
  const context = {
    site: 'leetcode',
    problem_title: '',
    problem_statement: '',
    user_code: '',
    language: 'unknown'
  };

  const titleElement = document.querySelector('[data-cy="question-title"]') || 
                       document.querySelector('.text-title-large');
  if (titleElement) {
    context.problem_title = titleElement.textContent.trim();
  }

  const problemContent = document.querySelector('[data-track-load="description_content"]') ||
                         document.querySelector('.elfjS') ||
                         document.querySelector('[class*="question-content"]');
  if (problemContent) {
    context.problem_statement = problemContent.innerText.trim();
  }

  const codeEditor = document.querySelector('.view-lines') || 
                     document.querySelector('[class*="monaco-editor"]');
  if (codeEditor) {
    context.user_code = codeEditor.innerText.trim();
  }

  const langSelector = document.querySelector('[id*="lang"]') ||
                      document.querySelector('button[id*="headlessui-listbox-button"]');
  if (langSelector) {
    context.language = langSelector.textContent.trim().toLowerCase();
  }

  return context;
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

  button.addEventListener('click', () => {
    const context = extractLeetCodeContext();
    chrome.runtime.sendMessage({
      action: 'openChat',
      context: context
    });
  });

  document.body.appendChild(button);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', injectChatButton);
} else {
  injectChatButton();
}
