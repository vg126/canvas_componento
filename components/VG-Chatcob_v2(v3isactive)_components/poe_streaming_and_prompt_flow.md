# Poe Streaming and Prompt Flow

Handles outbound prompts, streaming responses, and spinner state while coordinating context and flag options.

```javascript
window.Poe.registerHandler("chat-handler", (result) => {
    const msg = result.responses[0];

    if (msg.status === "error") {
        const errorElement = addMessage("Error: " + (msg.statusText || "Something went wrong"), false, 'complete');
        hideLoadingSpinner();
    } else if (msg.status === "incomplete") {
        // Update existing response message
        if (!window.currentResponseElement) {
            // Create new streaming message with simple content
            window.currentResponseElement = addMessage(msg.content, false, 'incomplete');
        } else {
            // Update existing message content directly
            const responseContent = msg.content + '<span class="animate-pulse">|</span>';
            window.currentResponseElement.innerHTML = marked.parse(responseContent);
        }
    } else if (msg.status === "complete") {
        // Final response - always create fresh message to avoid contamination
        if (window.currentResponseElement) {
            // Remove incomplete message
            const messageContainer = window.currentResponseElement.closest('.flex');
            if (messageContainer) {
                messageContainer.remove();
            }
        }

        // Create fresh complete message with thinking log support
        createMessageWithThinking(msg.content, false, 'complete');

        // Save to chat history
        appState.chatHistory.push({
            content: msg.content,
            isUser: false,
            timestamp: new Date().toISOString(),
            model: appState.selectedModel
        });

        // Clear current response reference and hide spinner
        window.currentResponseElement = null;
        hideLoadingSpinner();
    }
});
```

```javascript
let activeRequests = 0;

function showLoadingSpinner() {
    activeRequests++;
    document.getElementById('loadingSpinner').classList.remove('hidden');
}

function hideLoadingSpinner() {
    activeRequests = Math.max(0, activeRequests - 1);
    if (activeRequests === 0) {
        document.getElementById('loadingSpinner').classList.add('hidden');
    }
}

function stopLoadingSpinner() {
    activeRequests = 0;
    document.getElementById('loadingSpinner').classList.add('hidden');
}
```

```javascript
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    const selectedModel = appState.selectedModel;

    // Add user message to chat UI only (not to history yet)
    addMessageToUI(message, true);

    // Clear input and files
    messageInput.value = '';
    messageInput.style.height = 'auto';

    // Sync conversation manager with existing chat history (user messages only)
    conversationManager.syncWithChatHistory(appState.chatHistory);

    // Generate context-aware prompt using conversation manager
    const contextResult = conversationManager.generateContext(message, {
        metadata: {
            isUser: true,
            model: selectedModel,
            timestamp: new Date().toISOString()
        }
    });

    // Now add the current message to history after context generation
    appState.chatHistory.push({
        content: message,
        isUser: true,
        timestamp: new Date().toISOString(),
        model: null
    });

    // Generate flags and prepare the final prompt
    const flagString = generateFlagString(selectedModel);
    const finalPrompt = `@${selectedModel} ${contextResult.contextPrompt}${flagString}`;

    // Show loading spinner
    showLoadingSpinner();

    try {
        await window.Poe.sendUserMessage(finalPrompt, {
            handler: "chat-handler",
            stream: true,
            openChat: false,
            attachments: selectedFiles.length > 0 ? selectedFiles : undefined
        });

        // Clear files after sending
        if (selectedFiles.length > 0) {
            selectedFiles = [];
            fileInput.value = '';
            filePreview.classList.add('hidden');
        }

    } catch (err) {
        addMessage("Error sending message: " + err.message, false, 'error');
        hideLoadingSpinner();
    }
}
```
