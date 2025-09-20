# Chat UI Renderer

Functions responsible for displaying messages in the interface.

```javascript
function renderChatHistory() {
    // Clear existing messages except the start message
    const startMessage = chatContainer.querySelector('.text-center');
    chatContainer.innerHTML = '';

    if (appState.chatHistory.length === 0) {
        // Add back the start message if no history
        const emptyDiv = document.createElement('div');
        emptyDiv.className = 'text-center text-gray-500 dark:text-gray-400 text-sm';
        emptyDiv.textContent = 'Start a conversation with your selected model';
        chatContainer.appendChild(emptyDiv);
        return;
    }

    // Render all messages from history
    appState.chatHistory.forEach(message => {
        addMessageToUI(message.content, message.isUser, 'complete');
    });
}

// Add message to UI only (separated from history management)
function addMessageToUI(content, isUser = false, status = 'complete') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 group`;

    // Create wrapper for message content and menu
    const messageWrapper = document.createElement('div');
    messageWrapper.className = `relative flex items-start ${isUser ? 'flex-row-reverse' : 'flex-row'} gap-2`;

    const messageContent = document.createElement('div');
    messageContent.className = `max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
        isUser
            ? 'themed-message-user'
            : 'themed-message-ai'
    }`;

    if (status === 'incomplete') {
        if (isUser) {
            messageContent.textContent = content;
        } else {
            messageContent.innerHTML = marked.parse(content) + '<span class="animate-pulse">|</span>';
        }
    } else {
        if (isUser) {
            messageContent.textContent = content;
        } else {
            messageContent.innerHTML = marked.parse(content);
        }
    }

    messageWrapper.appendChild(messageContent);

    // Add three-dot menu if message is complete
    if (status === 'complete') {
        const menuButton = createMessageMenu(content, isUser);
        messageWrapper.appendChild(menuButton);
    }

    messageDiv.appendChild(messageWrapper);
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    return messageContent;
}
```
