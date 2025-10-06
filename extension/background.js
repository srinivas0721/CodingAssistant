chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'openChat') {
    chrome.storage.local.set({ context: request.context }, () => {
      chrome.action.openPopup();
    });
  }
});
