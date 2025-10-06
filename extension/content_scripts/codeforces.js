function extractCodeforcesContext() {
  const context = {
    site: 'codeforces',
    problem_title: '',
    problem_statement: '',
    user_code: '',
    language: 'unknown'
  };

  const titleElement = document.querySelector('.problem-statement .title');
  if (titleElement) {
    context.problem_title = titleElement.textContent.trim();
  }

  const problemStatement = document.querySelector('.problem-statement');
  if (problemStatement) {
    context.problem_statement = problemStatement.innerText.trim();
  }

  const codeEditor = document.querySelector('#sourceCodeTextarea') ||
                     document.querySelector('textarea[name="source"]') ||
                     document.querySelector('.CodeMirror');
  if (codeEditor) {
    if (codeEditor.tagName === 'TEXTAREA') {
      context.user_code = codeEditor.value;
    } else if (codeEditor.classList.contains('CodeMirror')) {
      const cm = codeEditor.CodeMirror;
      if (cm) {
        context.user_code = cm.getValue();
      }
    }
  }

  const langSelector = document.querySelector('select[name="programTypeId"]');
  if (langSelector) {
    context.language = langSelector.options[langSelector.selectedIndex].text.toLowerCase();
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
    const context = extractCodeforcesContext();
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
