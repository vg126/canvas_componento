# Message Menus and Notifications

Utility helpers that expose copy/remove actions and transient feedback for chat interactions.

```javascript
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-3 rounded-lg text-white z-50 ${
        type === 'error' ? 'bg-red-500' : 'bg-green-500'
    }`;
    notification.textContent = message;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function createMessageMenu(content, isUser) {
    const menu = document.createElement('div');
    menu.className = 'flex-shrink-0 self-start mt-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200';

    menu.innerHTML = `
        <div class="relative">
            <button
                class="themed-btn w-6 h-6 flex items-center justify-center rounded text-sm"
                onclick="toggleMessageMenu(this)"
                title="Message options"
            >
                ⋮
            </button>
            <div class="message-menu themed-menu hidden absolute top-full ${isUser ? 'right-0' : 'left-0'} mt-1 rounded-lg py-1 z-10 min-w-24">
                <button
                    onclick="copyMessage('${btoa(content)}'); hideMessageMenu()"
                    class="themed-menu-item w-full px-3 py-1 text-left text-xs transition-colors"
                >
                    📋 Copy
                </button>
                <button
                    onclick="removeMessage(this); hideMessageMenu()"
                    class="themed-menu-item danger w-full px-3 py-1 text-left text-xs transition-colors"
                >
                    🗑️ Remove
                </button>
            </div>
        </div>
    `;

    return menu;
}

window.toggleThinking = function(thinkingId) {
    const thinkingDiv = document.getElementById(thinkingId);
    const icon = document.getElementById(thinkingId + '-icon');

    if (thinkingDiv.classList.contains('hidden')) {
        thinkingDiv.classList.remove('hidden');
        icon.textContent = '▼';
        icon.classList.add('rotate-90');
    } else {
        thinkingDiv.classList.add('hidden');
        icon.textContent = '▶';
        icon.classList.remove('rotate-90');
    }
};

window.toggleMessageMenu = function(button) {
    const menu = button.parentElement.querySelector('.message-menu');

    // Close all other menus first
    document.querySelectorAll('.message-menu').forEach(m => {
        if (m !== menu) m.classList.add('hidden');
    });

    menu.classList.toggle('hidden');
};

window.hideMessageMenu = function() {
    document.querySelectorAll('.message-menu').forEach(m => m.classList.add('hidden'));
};

window.copyMessage = function(encodedContent) {
    try {
        const content = atob(encodedContent);
        navigator.clipboard.writeText(content);
        showNotification('Message copied to clipboard!');
    } catch (err) {
        showNotification('Failed to copy message', 'error');
    }
};

window.removeMessage = function(button) {
    const messageDiv = button.closest('.flex');
    if (messageDiv) {
        // Find the message content to match against chat history
        const messageContent = messageDiv.querySelector('.themed-message-user, .themed-message-ai');
        if (messageContent) {
            const content = messageContent.textContent || messageContent.innerText;

            // Remove from appState.chatHistory by finding matching content
            const messageIndex = appState.chatHistory.findIndex(msg => msg.content === content.trim());
            if (messageIndex !== -1) {
                appState.chatHistory.splice(messageIndex, 1);
            }
        }

        messageDiv.remove();
        showNotification('Message removed');
    }
};

document.addEventListener('click', function(e) {
    if (!e.target.closest('.relative')) {
        hideMessageMenu();
    }
});
```
