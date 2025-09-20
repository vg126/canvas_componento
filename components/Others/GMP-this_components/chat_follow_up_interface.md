# Chat Follow-up Interface

Extends the analysis with a lightweight chat stream so users can ask additional questions tied to the generated GMP output.

```javascript
// Chat functionality
sendChatBtn.addEventListener('click', sendChatMessage);
chatInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendChatMessage();
    }
});

async function sendChatMessage() {
    const message = chatInput.value.trim();
    if (!message) return;

    const messageId = Date.now().toString();
    addChatMessage(message, 'user');
    chatInput.value = '';

    const prompt = `Based on the previous GMP analysis, please answer this follow-up question: "${message}"\n\nContext: The user has received a complete analysis using one of the Genesis Mapping Protocols. Please provide a focused response that relates to the analysis and helps deepen understanding.`;

    await window.Poe.sendUserMessage(
        `@${aiModel.value} ${prompt}`,
        {
            handler: "gmp-analysis",
            stream: true,
            openChat: false,
            handlerContext: { type: "chat", messageId: messageId }
        }
    );

    addChatMessage('', 'ai', messageId);
}

function addChatMessage(content, sender, messageId = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-bubble flex ${sender === 'user' ? 'justify-end' : 'justify-start'}`;

    const bubble = document.createElement('div');
    bubble.className = `max-w-[80%] p-3 rounded-lg ${
        sender === 'user'
            ? 'bg-primary text-white ml-4'
            : 'bg-gray-200 dark:bg-gray-700 mr-4'
    }`;

    if (messageId) {
        bubble.id = `chat-${messageId}`;
    }

    bubble.innerHTML = sender === 'user' ? content : (content || 'Thinking...');
    messageDiv.appendChild(bubble);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function updateChatMessage(messageId, content, isComplete) {
    const bubble = document.getElementById(`chat-${messageId}`);
    if (bubble) {
        // Remove thinking tags from chat responses
        const cleanContent = content.replace(/<thinking>[\s\S]*?<\/thinking>/g, '').trim();
        bubble.innerHTML = formatMarkdown(cleanContent) || 'Thinking...';
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}
```
