# Chat Message Pipeline

State container and renderer functions that keep the chat transcript in sync with user and model messages.

```javascript
let appState = {
    selectedModel: 'Claude-Sonnet-4',
    isAccordionExpanded: false,
    expandedSections: new Set(),
    searchTerm: '',
    filteredData: MODEL_DATABASE,
    chatHistory: [],
    modelFlags: {}, // Store flag values per model
    savedThemes: {} // Store custom themes instead of localStorage
};

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

```javascript
function addMessage(content, isUser = false, status = 'complete') {
    // Clear the "start conversation" message if it exists
    const startMessage = chatContainer.querySelector('.text-center');
    if (startMessage && startMessage.textContent.includes('Start a conversation')) {
        startMessage.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`;

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

    messageDiv.appendChild(messageContent);

    // Always append to the end of chat container
    chatContainer.appendChild(messageDiv);

    // Store in chat history if complete
    if (status === 'complete') {
        appState.chatHistory.push({
            content: content,
            isUser: isUser,
            timestamp: new Date().toISOString(),
            model: isUser ? null : appState.selectedModel
        });
    }

    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;

    return messageContent;
}
```

```javascript
function parseThinkingLog(content) {
    // Comprehensive patterns for various thinking formats
    const thinkingPatterns = [
        // Exact patterns with line boundaries
        { pattern: /^Thinking\.\.\.\s*$/m, type: 'simple' },
        { pattern: /^\*Thinking\.\.\.\*\s*$/m, type: 'italic' },
        { pattern: /^\*\*Thinking\*\*\s*$/m, type: 'bold' },
        { pattern: /^# Thinking\s*$/m, type: 'heading' },
        { pattern: /<thinking>/i, type: 'xml' },

        // Blockquote patterns (for models using > prefixes)
        { pattern: /^>\s*Thinking\.\.\./m, type: 'blockquote' },
        { pattern: /^>\s*\*Thinking\.\.\.\*/m, type: 'blockquote-italic' },

        // More flexible patterns
        { pattern: /^Thinking:?\s*\n/m, type: 'colon' },
        { pattern: /^Internal thoughts:?\s*\n/im, type: 'internal' }
    ];

    let detectedPattern = null;
    let matchInfo = null;

    // Try to detect thinking pattern
    for (const patternInfo of thinkingPatterns) {
        const match = content.match(patternInfo.pattern);
        if (match) {
            detectedPattern = patternInfo;
            matchInfo = match;
            break;
        }
    }

    // If no thinking pattern detected, return content as-is
    if (!detectedPattern) {
        return {
            hasThinking: false,
            thinkingContent: '',
            actualResponse: content
        };
    }

    try {
        let thinkingContent = '';
        let actualResponse = content;

        if (detectedPattern.type === 'xml') {
            // Handle XML-style thinking tags
            const match = content.match(/<thinking>([\s\S]*?)<\/thinking>/i);
            if (match) {
                thinkingContent = match[1].trim();
                actualResponse = content.replace(/<thinking>[\s\S]*?<\/thinking>/i, '').trim();
            }
        } else if (detectedPattern.type.includes('blockquote')) {
            // Handle blockquote-style thinking (lines starting with >)
            const lines = content.split('\n');
            let inThinking = false;
            let thinkingLines = [];
            let responseLines = [];

            for (const line of lines) {
                if (line.match(/^>\s*(Thinking|\*Thinking)/)) {
                    inThinking = true;
                    thinkingLines.push(line.replace(/^>\s*/, ''));
                } else if (inThinking && line.startsWith('>')) {
                    // Continue collecting blockquote lines
                    thinkingLines.push(line.replace(/^>\s*/, ''));
                } else if (inThinking && !line.startsWith('>') && line.trim() === '') {
                    // Empty line might be part of thinking
                    thinkingLines.push('');
                } else {
                    // We've exited the thinking section
                    if (inThinking || !line.match(/^>\s*(Thinking|\*Thinking)/)) {
                        inThinking = false;
                        responseLines.push(line);
                    }
                }
            }

            thinkingContent = thinkingLines.join('\n').trim();
            actualResponse = responseLines.join('\n').trim();
        } else {
            // Handle other patterns - find where thinking ends
            const thinkingStart = matchInfo.index + matchInfo[0].length;

            // Look for common end patterns
            const endPatterns = [
                /\n\n(?=[A-Z])/,          // Double newline before capital letter
                /\n\n(?=\w+:)/,           // Double newline before label
                /\n---\n/,                // Markdown divider
                /\n\n(?=The |I |Based |Looking |Since |To |In |For |Let |Here |This )/,  // Common response starters
                /\n\*\*[A-Z]/,            // Bold heading
                /\n#{1,6}\s/,             // Markdown heading
                /\n\n.*?:\n/,             // Section header
                /(?=\n\nNow,? |Actually,? |So,? |Alright,? |Okay,? )/  // Conversational transitions
            ];

            let endIndex = -1;
            const remainingContent = content.substring(thinkingStart);

            for (const endPattern of endPatterns) {
                const match = remainingContent.search(endPattern);
                if (match !== -1 && (endIndex === -1 || match < endIndex)) {
                    endIndex = match;
                }
            }

            if (endIndex !== -1) {
                thinkingContent = remainingContent.substring(0, endIndex).trim();
                actualResponse = remainingContent.substring(endIndex).trim();
            } else {
                // If no clear end pattern, try to be conservative
                // Look for the first substantial paragraph after thinking
                const paragraphs = remainingContent.split(/\n\n+/);
                if (paragraphs.length > 1) {
                    // Take first paragraph as thinking, rest as response
                    thinkingContent = paragraphs[0].trim();
                    actualResponse = paragraphs.slice(1).join('\n\n').trim();
                } else {
                    // Last resort: treat everything as response to avoid losing content
                    return {
                        hasThinking: false,
                        thinkingContent: '',
                        actualResponse: content
                    };
                }
            }
        }

        // Clean up extracted content
        thinkingContent = thinkingContent
            .replace(/^(Thinking\.\.\.|\*Thinking\.\.\.\*|Thinking:|Internal thoughts:)\s*/i, '')
            .trim();

        // Validate that we have meaningful content
        const hasValidThinking = thinkingContent.length > 10 &&
                               actualResponse.length > 0 &&
                               !thinkingContent.includes('error') &&
                               !thinkingContent.includes('undefined');

        if (!hasValidThinking) {
            // If extraction seems wrong, return original content
            return {
                hasThinking: false,
                thinkingContent: '',
                actualResponse: content
            };
        }

        return {
            hasThinking: true,
            thinkingContent: thinkingContent,
            actualResponse: actualResponse
        };

    } catch (error) {
        console.error('Error parsing thinking log:', error);
        // On any error, return content as-is to avoid losing it
        return {
            hasThinking: false,
            thinkingContent: '',
            actualResponse: content
        };
    }
}
```

```javascript
function createMessageWithThinking(content, isUser = false, status = 'complete') {
    // Clear the "start conversation" message if it exists
    const startMessage = chatContainer.querySelector('.text-center');
    if (startMessage && startMessage.textContent.includes('Start a conversation')) {
        startMessage.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 group`;

    // Create wrapper for message content and menu
    const messageWrapper = document.createElement('div');
    messageWrapper.className = `relative flex items-start ${isUser ? 'flex-row-reverse' : 'flex-row'} gap-2`;

    if (isUser) {
        // User messages - simple display
        const messageContent = document.createElement('div');
        messageContent.className = 'themed-message-user max-w-xs lg:max-w-md px-4 py-2 rounded-lg';
        messageContent.textContent = content;
        messageWrapper.appendChild(messageContent);
    } else {
        // AI messages - parse thinking log
        const parsed = parseThinkingLog(content);
        const messageContent = document.createElement('div');
        messageContent.className = 'max-w-xs lg:max-w-md';

        let html = '';

        // Add thinking section if present
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
                        <div class="themed-thinking-content text-xs font-mono whitespace-pre-wrap p-2 rounded">${escapeHtml(parsed.thinkingContent)}</div>
                    </div>
                </div>
            `;
        }

        // Add actual response
        const responseContent = status === 'incomplete'
            ? marked.parse(parsed.actualResponse || content) + '<span class="animate-pulse">|</span>'
            : marked.parse(parsed.actualResponse || content);

        html += `
            <div class="themed-message-ai px-4 py-2 rounded-lg">
                ${responseContent}
            </div>
        `;

        messageContent.innerHTML = html;
        messageWrapper.appendChild(messageContent);
    }

    // Add three-dot menu if message is complete
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
