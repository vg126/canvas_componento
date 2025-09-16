# State Manager

Exports, imports, and persists application state, enabling sharing and recovery of conversations.

```javascript
class StateManager {
    constructor(options = {}) {
        this.options = {
            appName: options.appName || 'ChatApp',
            version: options.version || '1.0',
            storageKey: options.storageKey || 'chatAppState',
            ...options
        };
        this.state = appState; // Use existing state
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
            renderChatHistory(); // Render chat history to UI
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
}
```
