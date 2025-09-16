# Application Bootstrap

Collects global helpers on `window`, wires DOM events, and kicks off the initial render/theme selection when Canvas loads the HTML shell.

## Exposing helpers for inline handlers

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

window.openThemeModal = openThemeModal;
window.closeThemeModal = closeThemeModal;
window.applyCustomTheme = applyCustomTheme;
window.saveCustomTheme = saveCustomTheme;
window.loadCustomTheme = loadCustomTheme;
window.deleteCustomTheme = deleteCustomTheme;
```

* Keeps the HTML markup clean by referencing functions declared in the module scope rather than embedding logic inline.
* Includes a placeholder `clearContext` stub for future DOM-level context resets.

## Initialization and listeners

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
```

* The send button and Enter key (without Shift) both trigger `sendMessage`, keeping composition behavior consistent.

```javascript
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    applyTheme('dark');
});
```

* Defers initialization until Canvas injects the DOM, then renders the default model name and applies the dark theme immediately.
