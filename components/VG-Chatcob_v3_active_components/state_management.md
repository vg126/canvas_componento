# State Management and Modals

The v3 app bundles an export/import pipeline built on a lightweight `StateManager` and a modal orchestrator that surfaces copy/paste flows inside the Canvas shell.

## StateManager

```javascript
class StateManager {
    constructor(options = {}) {
        this.options = {
            appName: options.appName || 'ChatApp',
            version: options.version || '1.0',
            storageKey: options.storageKey || 'chatAppState',
            ...options
        };
        this.state = appState;
    }

    exportAsJSON(options = {}) {
        const exportData = {
            appName: this.options.appName,
            version: this.options.version,
            selectedModel: this.state.selectedModel,
            modelFlags: this.state.modelFlags,
            chatHistory: this.state.chatHistory,
            timestamp: new Date().toISOString()
        };
        return JSON.stringify(exportData, null, options.prettify !== false ? 2 : 0);
    }
```

```javascript
async copyStateToClipboard() {
    try {
        const jsonString = this.exportAsJSON();
        await navigator.clipboard.writeText(jsonString);
        showNotification('State copied to clipboard!');
        return true;
    } catch (error) {
        showNotification('Failed to copy state: ' + error.message, 'error');
        return false;
    }
}
```

```javascript
downloadState(filename = null) {
    try {
        const jsonString = this.exportAsJSON();
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
        const defaultFilename = `${this.options.appName.toLowerCase()}_state_${timestamp}.json`;

        const blob = new Blob([jsonString], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename || defaultFilename;
        link.click();
        URL.revokeObjectURL(url);

        showNotification('State downloaded successfully!');
        return true;
    } catch (error) {
        showNotification('Failed to download state: ' + error.message, 'error');
        return false;
    }
}
```

```javascript
importState(importData) {
    try {
        if (!importData || typeof importData !== 'object') {
            throw new Error('Invalid import data format');
        }

        if (importData.selectedModel) {
            this.state.selectedModel = importData.selectedModel;
        }
        if (importData.modelFlags) {
            this.state.modelFlags = importData.modelFlags;
        }
        if (importData.chatHistory) {
            this.state.chatHistory = importData.chatHistory;
        }

        updateModelDisplay();
        renderChatHistory();
        showNotification('State imported successfully!');
        return true;
    } catch (error) {
        showNotification('Failed to import state: ' + error.message, 'error');
        return false;
    }
}

importFromJSON(jsonString) {
    try {
        const importData = JSON.parse(jsonString);
        return this.importState(importData);
    } catch (error) {
        showNotification('Invalid JSON format: ' + error.message, 'error');
        return false;
    }
}
```

```javascript
triggerFileUpload() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.style.display = 'none';

    input.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                stateModalManager.showImportModal(event.target.result);
            };
            reader.readAsText(file);
        }
    });

    document.body.appendChild(input);
    input.click();
    document.body.removeChild(input);
}
```

* Export data is computed on demand; the manager never mutates `localStorage` or caches JSON.
* `triggerFileUpload` uses a transient `<input>` so the UI remains uncluttered.

## StateModalManager

```javascript
class StateModalManager {
    constructor(stateManager) {
        this.stateManager = stateManager;
        this.currentModal = null;
    }

    showImportModal(prefilledData = '') {
        this.currentModal = this.createModal('import-modal', 'Import State', `
            <div class="p-4">
                <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">Paste your exported state JSON below:</p>
                <textarea
                    id="import-textarea"
                    class="w-full h-64 p-3 border border-gray-300 dark:border-gray-600 rounded-lg text-sm font-mono bg-white dark:bg-gray-700 text-gray-900 dark:text-white resize-vertical"
                    placeholder="Paste your JSON state here..."
                >${prefilledData}</textarea>
                <div class="flex justify-end gap-3 mt-4">
                    <button onclick="stateModalManager.closeModal()" class="px-4 py-2 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded">
                        Cancel
                    </button>
                    <button onclick="stateModalManager.executeImport()" class="px-4 py-2 bg-primary text-white hover:bg-primary-hover rounded">
                        Import State
                    </button>
                </div>
            </div>
        `);
    }
```

```javascript
showExportModal() {
    const exportData = this.stateManager.exportAsJSON({ prettify: true });

    this.currentModal = this.createModal('export-modal', 'Export State', `
        <div class="p-4">
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">Copy the JSON below or use the action buttons:</p>
            <textarea
                id="export-textarea"
                class="w-full h-64 p-3 border border-gray-300 dark:border-gray-600 rounded-lg text-sm font-mono bg-white dark:bg-gray-700 text-gray-900 dark:text-white resize-vertical"
                readonly
            >${exportData}</textarea>
            <div class="flex gap-2 mt-3 mb-4">
                <button onclick="stateModalManager.copyExportData()" class="px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded">
                    📋 Copy to Clipboard
                </button>
                <button onclick="stateModalManager.downloadExport()" class="px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded">
                    💾 Download File
                </button>
            </div>
            <div class="flex justify-end">
                <button onclick="stateModalManager.closeModal()" class="px-4 py-2 bg-primary text-white hover:bg-primary-hover rounded">
                    Close
                </button>
            </div>
        </div>
    `);

    setTimeout(() => {
        const textarea = document.getElementById('export-textarea');
        if (textarea) textarea.select();
    }, 100);
}
```

```javascript
createModal(id, title, content) {
    this.closeModal();

    const modal = document.createElement('div');
    modal.id = id;
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    modal.innerHTML = `
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg w-96 max-w-90vw max-h-90vh overflow-y-auto">
            <div class="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white">${title}</h3>
                <button onclick="stateModalManager.closeModal()" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>
            ${content}
        </div>
    `;

    document.body.appendChild(modal);

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            this.closeModal();
        }
    });

    return modal;
}
```

```javascript
executeImport() {
    const textarea = document.getElementById('import-textarea');
    if (!textarea.value.trim()) {
        showNotification('Please paste JSON state data', 'error');
        return;
    }

    const success = this.stateManager.importFromJSON(textarea.value);
    if (success) {
        this.closeModal();
    }
}

async copyExportData() {
    const textarea = document.getElementById('export-textarea');
    if (textarea) {
        try {
            await navigator.clipboard.writeText(textarea.value);
            showNotification('Export data copied to clipboard!');
        } catch (err) {
            textarea.select();
            document.execCommand('copy');
            showNotification('Export data copied to clipboard!');
        }
    }
}

downloadExport() {
    this.stateManager.downloadState();
    this.closeModal();
}

closeModal() {
    if (this.currentModal) {
        document.body.removeChild(this.currentModal);
        this.currentModal = null;
    }
}
```

* All modals are injected dynamically so Canvas keeps its static HTML untouched.
* Export modal pre-selects the JSON for quick copying and exposes both clipboard and file download paths.

## Global helpers and chat export

```javascript
const stateManagerInstance = new StateManager({
    appName: 'ChatApp',
    version: '1.0',
    storageKey: 'chatAppState'
});

const stateModalManager = new StateModalManager(stateManagerInstance);

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
```

`downloadChat` converts the in-memory transcript into Markdown for offline review:

```javascript
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

* Offers a Markdown export distinct from JSON state dumps, capturing message timestamps and speaker labels.
