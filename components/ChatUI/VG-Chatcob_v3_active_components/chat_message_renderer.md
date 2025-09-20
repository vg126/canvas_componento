# Chat Message Renderer

Utilities that keep the visual transcript in sync with `appState.chatHistory`, add streaming placeholders, and expose optional thinking logs for model responses.

## History projection

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
```

* Rebuilds the container every time history changes so the DOM always matches `appState`.
* Restores the onboarding prompt whenever the user deletes all messages.

## Base bubble creation

```javascript
function addMessageToUI(content, isUser = false, status = 'complete') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 group`;

    // Create wrapper for message content and menu
    const messageWrapper = document.createElement('div');
    messageWrapper.className = `relative flex items-start ${isUser ? 'flex-row-reverse' : 'flex-row'} gap-2`;

    const messageContent = document.createElement('div');
    messageContent.className = `max-w-sm lg:max-w-2xl px-4 py-2 rounded-lg ${
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

* User bubbles are rendered as plain text while assistant messages are piped through `marked` for Markdown support.
* Streaming states append a blinking cursor to signal ongoing output.
* A trailing menu button is only injected when the message is finalized.

## Thinking log aware renderer

Assistant outputs optionally contain a private "thinking" transcript. The helper below extracts and collapses that section while ensuring the visible reply stays intact.

```javascript
function parseThinkingLog(content) {
    const thinkingMatch = content.match(/^(.*?)thinking[^\n]*\n(.*?)(?=\n\n[A-Z][a-z]|\n\n\w+!|\n\n\w+\?|$)/ims);

    if (!thinkingMatch) {
        return {
            hasThinking: false,
            thinkingContent: '',
            actualResponse: content
        };
    }

    const beforeThinking = thinkingMatch[1].trim();
    const potentialThinking = thinkingMatch[2].trim();

    if (potentialThinking.length > 30) {
        const afterThinkingMatch = content.match(/thinking[^\n]*\n.*?\n\n([A-Z].*)/ims);

        if (afterThinkingMatch && afterThinkingMatch[1]) {
            return {
                hasThinking: true,
                thinkingContent: potentialThinking,
                actualResponse: afterThinkingMatch[1]
            };
        }
    }

    return {
        hasThinking: false,
        thinkingContent: '',
        actualResponse: content
    };
}
```

* Uses regex guards so the visible answer is never lost if the thinking block cannot be confidently isolated.

```javascript
function createMessageWithThinking(content, isUser = false, status = 'complete') {
    const startMessage = chatContainer.querySelector('.text-center');
    if (startMessage && startMessage.textContent.includes('Start a conversation')) {
        startMessage.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 group`;

    const messageWrapper = document.createElement('div');
    messageWrapper.className = `relative flex items-start ${isUser ? 'flex-row-reverse' : 'flex-row'} gap-2`;

    if (isUser) {
        const messageContent = document.createElement('div');
        messageContent.className = 'themed-message-user max-w-sm lg:max-w-2xl px-4 py-2 rounded-lg';
        messageContent.textContent = content;
        messageWrapper.appendChild(messageContent);
    } else {
        const parsed = parseThinkingLog(content);
        const messageContent = document.createElement('div');
        messageContent.className = 'max-w-sm lg:max-w-2xl';

        let html = '';

        if (parsed.hasThinking && status === 'complete') {
            const thinkingId = 'thinking-' + Date.now();
            html += `
                <div class="themed-thinking mb-2 rounded-lg overflow-hidden">
                    <button
                        onclick="toggleThinking('${thinkingId}')"
                        class="themed-thinking-header w-full px-3 py-2 text-left text-xs font-medium flex items-center justify-between transition-colors"
                    >
                        <span class="flex items-center">
                            🤔 <span class="ml-1">Thinking</span>
                        </span>
                        <span id="${thinkingId}-icon" class="transform transition-transform duration-200">▶</span>
                    </button>
                    <div id="${thinkingId}" class="hidden px-3 pb-3">
                        <div class="themed-thinking-content text-xs font-mono whitespace-pre-wrap p-2 rounded">${parsed.thinkingContent}</div>
                    </div>
                </div>
            `;
        }

        const responseContent = status === 'incomplete'
            ? (parsed.actualResponse || content) + '<span class="animate-pulse">|</span>'
            : marked.parse(parsed.actualResponse || content);

        html += `
            <div class="themed-message-ai px-4 py-2 rounded-lg">
                ${responseContent}
            </div>
        `;

        messageContent.innerHTML = html;
        messageWrapper.appendChild(messageContent);
    }

    if (status === 'complete') {
        const menuButton = createMessageMenu(content, isUser);
        messageWrapper.appendChild(menuButton);
    }

    messageDiv.appendChild(messageWrapper);
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    return messageDiv.querySelector(isUser ? '.themed-message-user' : '.themed-message-ai');
}
```

* Collapses the default empty-state prompt so fresh threads do not show onboarding text once a reply lands.
* Assigns unique IDs to each thinking toggle button and binds them to `window.toggleThinking` for expand/collapse.
* Streams use the same blinking cursor approach until the handler swaps in a finalized message bubble.

## Menu controls and clipboard helpers

```javascript
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
```

* Ties into document-level click listeners so only one menu stays open at a time.
* Encodes message payloads with `btoa` before placing them in inline attributes.

Global helpers (`toggleThinking`, `toggleMessageMenu`, `hideMessageMenu`, `copyMessage`, `removeMessage`) expose the DOM behavior to inline handlers and keep `appState.chatHistory` synchronized with deletions.
