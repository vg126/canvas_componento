# Poe Streaming and Prompt Flow

The v3 surface coordinates streaming responses from Poe, converts local state into annotated prompts, and mirrors the backend progress with a header spinner.

## Streaming handler

```javascript
window.Poe.registerHandler("chat-handler", (result) => {
    const msg = result.responses[0];

    if (msg.status === "error") {
        const errorElement = addMessage("Error: " + (msg.statusText || "Something went wrong"), false, 'complete');
        hideLoadingSpinner();
    } else if (msg.status === "incomplete") {
        if (!window.currentResponseElement) {
            window.currentResponseElement = addMessage(msg.content, false, 'incomplete');
        } else {
            const responseContent = msg.content + '<span class="animate-pulse">|</span>';
            window.currentResponseElement.innerHTML = marked.parse(responseContent);
        }
    } else if (msg.status === "complete") {
        if (window.currentResponseElement) {
            const messageContainer = window.currentResponseElement.closest('.flex');
            if (messageContainer) {
                messageContainer.remove();
            }
        }

        createMessageWithThinking(msg.content, false, 'complete');

        appState.chatHistory.push({
            content: msg.content,
            isUser: false,
            timestamp: new Date().toISOString(),
            model: appState.selectedModel
        });

        window.currentResponseElement = null;
        hideLoadingSpinner();
    }
});
```

* Handles error, streaming, and final states in a single dispatcher.
* Replaces the streaming placeholder with a freshly rendered message so the thinking log parser can run on the final transcript.
* Persists only complete responses into `appState.chatHistory`.

## Spinner lifecycle

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

* A simple reference counter avoids flicker when multiple requests overlap.
* The header icon is clickable (`stopLoadingSpinner`) so users can dismiss a stuck indicator.

## Prompt assembly and dispatch

```javascript
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    const selectedModel = appState.selectedModel;

    addMessageToUI(message, true);

    messageInput.value = '';
    messageInput.style.height = 'auto';

    conversationManager.syncWithChatHistory(appState.chatHistory);

    const contextResult = conversationManager.generateContext(message, {
        metadata: {
            isUser: true,
            model: selectedModel,
            timestamp: new Date().toISOString()
        }
    });

    appState.chatHistory.push({
        content: message,
        isUser: true,
        timestamp: new Date().toISOString(),
        model: null
    });

    const flagString = generateFlagString(selectedModel);
    const finalPrompt = `@${selectedModel} ${contextResult.contextPrompt}${flagString}`;

    showLoadingSpinner();

    try {
        await window.Poe.sendUserMessage(finalPrompt, {
            handler: "chat-handler",
            stream: true,
            openChat: false,
            attachments: selectedFiles.length > 0 ? selectedFiles : undefined
        });

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

* Uses the conversation manager to build a context-aware prompt before persisting the user entry to history.
* Appends model flag switches (if any) via `generateFlagString`.
* Clears attachments and resets the input after Poe acknowledges the submission.
