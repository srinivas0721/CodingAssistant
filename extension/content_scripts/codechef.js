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
    const context = extractCodeChefContext();
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
