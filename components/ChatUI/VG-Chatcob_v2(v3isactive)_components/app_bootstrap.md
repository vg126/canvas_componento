# App Bootstrap and Global Wiring

Click handling, helper exports, and startup hooks that connect the individual modules into the running interface.

```javascript
document.addEventListener('click', function(event) {
    // Handle model item clicks in dropdown
    const dropdownModelItem = event.target.closest('#dropdownAccordionWrapper .model-item');
    if (dropdownModelItem) {
        const model = dropdownModelItem.dataset.model;
        if (model) {
            selectDropdownModel(model);
        }
        return;
    }

    // Close model dropdown when clicking outside
    const dropdown = document.getElementById('modelDropdown');
    const button = document.getElementById('modelSelectorBtn');

    if (!dropdown.classList.contains('hidden') &&
        !dropdown.contains(event.target) &&
        !button.contains(event.target)) {
        closeModelSelector();
    }

    // Close flag modal when clicking outside
    const flagModal = document.getElementById('flagModal');
    const flagBtn = document.getElementById('flagBtn');
    const flagModalContent = flagModal.querySelector('div');

    if (!flagModal.classList.contains('hidden') &&
        !flagModalContent.contains(event.target) &&
        !flagBtn.contains(event.target)) {
        closeFlagModal();
    }

    // Close theme modal when clicking outside
    const themeModal = document.getElementById('themeModal');
    const themeBtn = document.querySelector('button[onclick="openThemeModal()"]');
    const themeModalContent = themeModal.querySelector('div');

    if (!themeModal.classList.contains('hidden') &&
        !themeModalContent.contains(event.target) &&
        !themeBtn.contains(event.target)) {
        closeThemeModal();
    }

    // Close message menus when clicking outside
    if (!event.target.closest('.relative')) {
        hideMessageMenu();
    }

    // Dynamic modals are handled by their own click listeners
});
```

```javascript
function clearContext() {
    // TODO: Implement context clearing via Poe chat DOM manipulation
    // Note: This is experimental and complex - requires PC development environment
    showNotification('Context clearing is experimental - coming soon!', 'error');
}

const conversationManager = new ConversationContextManager({
    maxHistoryLength: 30,
    maxContextTokens: 8000,
    includeTimestamps: false,
    numberedHistory: true
});

const stateManagerInstance = new StateManager({
    appName: 'ChatApp',
    version: '1.0',
    storageKey: 'chatAppState'
});

const stateModalManager = new StateModalManager(stateManagerInstance);
```

```javascript
function copyStateToClipboard() {
    stateManagerInstance.copyStateToClipboard();
}

function openPasteModal() {
    stateModalManager.showImportModal();
}

function downloadState() {
    stateManagerInstance.downloadState();
}

function uploadState() {
    stateManagerInstance.triggerFileUpload();
}

function downloadChat() {
    if (appState.chatHistory.length === 0) {
        showNotification('No chat history to download', 'error');
        return;
    }

    let chatText = `# Chat Conversation\n`;
    chatText += `**Generated:** ${new Date().toLocaleString()}\n`;
    chatText += `**Selected Model:** ${appState.selectedModel}\n\n`;
    chatText += `---\n\n`;

    appState.chatHistory.forEach((message) => {
        const time = new Date(message.timestamp).toLocaleTimeString();
        if (message.isUser) {
            chatText += `**[${time}] You:**\n${message.content}\n\n`;
        } else {
            const modelName = message.model || 'AI';
            chatText += `**[${time}] ${modelName}:**\n${message.content}\n\n`;
        }
    });

    const blob = new Blob([chatText], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
    link.download = `chat_conversation_${timestamp}.md`;

    link.click();
    URL.revokeObjectURL(url);
    showNotification('Chat conversation downloaded!');
}
```

```javascript
window.copyStateToClipboard = copyStateToClipboard;
window.openModelSelector = openModelSelector;
window.closeModelSelector = closeModelSelector;
window.handleDropdownModelSearch = handleDropdownModelSearch;
window.toggleDropdownSection = toggleDropdownSection;
window.selectDropdownModel = selectDropdownModel;
window.openFlagModal = openFlagModal;
window.closeFlagModal = closeFlagModal;
window.stopLoadingSpinner = stopLoadingSpinner;
window.openPasteModal = openPasteModal;
window.downloadState = downloadState;
window.uploadState = uploadState;
window.downloadChat = downloadChat;
window.cycleTheme = cycleTheme;
window.clearContext = clearContext;

// Theme system global functions
window.openThemeModal = openThemeModal;
window.closeThemeModal = closeThemeModal;
window.applyCustomTheme = applyCustomTheme;
window.saveCustomTheme = saveCustomTheme;
window.loadCustomTheme = loadCustomTheme;
window.deleteCustomTheme = deleteCustomTheme;

// Make state managers available globally for onclick handlers
window.stateModalManager = stateModalManager;
```

```javascript
function initializeApp() {
    updateModelDisplay();
}

sendBtn.addEventListener('click', sendMessage);
messageInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    // Apply dark theme by default
    applyTheme('dark');
});
```
