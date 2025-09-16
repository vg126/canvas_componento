# Conversation Context Manager

A reusable utility that builds a context window for the current prompt, trims excess history, and exposes analytics hooks for UI integrations.

## Construction and storage

```javascript
class ConversationContextManager {
    constructor(options = {}) {
        this.options = {
            maxHistoryLength: options.maxHistoryLength || 50,
            maxContextTokens: options.maxContextTokens || 8000,
            includeTimestamps: options.includeTimestamps || false,
            autoTruncate: options.autoTruncate !== false,
            contextSeparator: options.contextSeparator || '===',
            numberedHistory: options.numberedHistory !== false,
            ...options
        };

        this.conversationHistory = [];
        this.contextHistory = [];
        this.sessionId = this.generateSessionId();
        this.contextChangeListeners = new Set();
    }
```

* Default limits can be overridden per instance and copy across all helper methods.
* Generates a session ID up front so downstream analytics can correlate entries.

## Recording messages and generating prompts

```javascript
addMessage(message, metadata = {}) {
    const messageEntry = {
        content: message.trim(),
        timestamp: new Date().toISOString(),
        sessionId: this.sessionId,
        id: this.generateMessageId(),
        ...metadata
    };

    this.conversationHistory.push(messageEntry);

    if (this.options.autoTruncate && this.conversationHistory.length > this.options.maxHistoryLength) {
        this.truncateHistory(this.options.maxHistoryLength);
    }

    this.notifyContextChange('messageAdded', messageEntry);
    return messageEntry;
}
```

```javascript
generateContext(currentMessage, options = {}) {
    const contextOptions = { ...this.options, ...options };

    this.addMessage(currentMessage, options.metadata);

    const previousMessages = this.conversationHistory.slice(0, -1);

    if (previousMessages.length === 0) {
        return {
            contextPrompt: currentMessage,
            hasContext: false,
            messageCount: 1,
            contextLength: currentMessage.length
        };
    }

    const contextPrompt = this.formatContextPrompt(currentMessage, previousMessages, contextOptions);

    return {
        contextPrompt,
        hasContext: true,
        messageCount: this.conversationHistory.length,
        previousMessageCount: previousMessages.length,
        contextLength: contextPrompt.length,
        estimatedTokens: this.estimateTokenCount(contextPrompt)
    };
}
```

* Records the live message before building context so the class stays in sync with the UI.
* Returns useful metadata (estimated tokens, counts) for telemetry or UI display.

## Prompt formatting

```javascript
formatContextPrompt(currentMessage, previousMessages, options = {}) {
    const separator = options.contextSeparator || this.options.contextSeparator;
    const useNumbers = options.numberedHistory !== false;
    const includeTimestamps = options.includeTimestamps || this.options.includeTimestamps;

    let contextPrompt = '';

    contextPrompt += `You are having a conversation with a user through a chat interface. Please respond naturally to their message below.\n\n`;

    if (previousMessages.length > 0) {
        contextPrompt += `${separator} Previous Conversation ${separator}\n`;

        previousMessages.forEach((msg, index) => {
            let line = '';

            if (useNumbers) {
                line += `${index + 1}. `;
            }

            if (includeTimestamps) {
                const time = new Date(msg.timestamp).toLocaleTimeString();
                line += `[${time}] `;
            }

            const cleanContent = this.stripParametersFromContent(msg.content);
            line += cleanContent;
            contextPrompt += line + '\n';
        });

        contextPrompt += '\n';
    }

    contextPrompt += `${separator} Current Prompt ${separator}\n`;
    contextPrompt += currentMessage;

    return contextPrompt;
}
```

* Prepends a conversational framing line before detailing previous turns.
* Removes `--flag value` parameter strings from historical messages so the backstory stays readable.

## Utility helpers

```javascript
estimateTokenCount(text) {
    if (!text) return 0;
    return Math.ceil(text.length / 4);
}
```

```javascript
truncateHistory(maxLength) {
    if (this.conversationHistory.length > maxLength) {
        const removed = this.conversationHistory.splice(0, this.conversationHistory.length - maxLength);
        this.notifyContextChange('historyTruncated', { removedCount: removed.length });
    }
}
```

```javascript
smartTruncate(maxTokens) {
    let totalTokens = 0;
    let keepIndex = this.conversationHistory.length;

    for (let i = this.conversationHistory.length - 1; i >= 0; i--) {
        const msgTokens = this.estimateTokenCount(this.conversationHistory[i].content);
        if (totalTokens + msgTokens > maxTokens) {
            keepIndex = i + 1;
            break;
        }
        totalTokens += msgTokens;
    }

    if (keepIndex > 0) {
        const removed = this.conversationHistory.splice(0, keepIndex);
        this.notifyContextChange('smartTruncated', {
            removedCount: removed.length,
            estimatedTokensSaved: this.estimateTokenCount(removed.map(m => m.content).join(' '))
        });
    }
}
```

```javascript
clearHistory() {
    const clearedCount = this.conversationHistory.length;
    this.conversationHistory = [];
    this.notifyContextChange('historyCleared', { clearedCount });
}
```

```javascript
getContextStats() {
    const totalMessages = this.conversationHistory.length;
    const totalChars = this.conversationHistory.reduce((sum, msg) => sum + msg.content.length, 0);
    const estimatedTokens = this.estimateTokenCount(this.conversationHistory.map(m => m.content).join(' '));

    return {
        totalMessages,
        totalCharacters: totalChars,
        estimatedTokens,
        averageMessageLength: totalMessages > 0 ? Math.round(totalChars / totalMessages) : 0,
        sessionId: this.sessionId,
        oldestMessage: totalMessages > 0 ? this.conversationHistory[0].timestamp : null,
        newestMessage: totalMessages > 0 ? this.conversationHistory[totalMessages - 1].timestamp : null
    };
}
```

* Provides summary statistics so dashboards can display running totals.

## Syncing and events

```javascript
syncWithChatHistory(chatHistory) {
    this.conversationHistory = [];
    chatHistory.forEach(historyItem => {
        if (historyItem.isUser) {
            this.addMessage(historyItem.content, {
                isUser: true,
                model: null,
                timestamp: historyItem.timestamp
            });
        }
    });
}
```

```javascript
addContextChangeListener(callback) {
    this.contextChangeListeners.add(callback);
    return () => this.contextChangeListeners.delete(callback);
}

notifyContextChange(eventType, data) {
    this.contextChangeListeners.forEach(callback => {
        try {
            callback(eventType, data, this.getContextStats());
        } catch (error) {
            console.error('Error in context change listener:', error);
        }
    });
}
```

* `syncWithChatHistory` primes the manager with existing user turns before generating a new prompt.
* The event bus enables external observers to track truncation, resets, and new messages.

## Miscellaneous helpers

```javascript
generateSessionId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

generateMessageId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}
```

```javascript
stripParametersFromContent(content) {
    if (!content || typeof content !== 'string') {
        return content;
    }

    const parameterPattern = /\s*--[a-zA-Z_][a-zA-Z0-9_]*\s+[^\s--]+(?:\s+[^\s--]+)*/g;

    let cleaned = content.replace(parameterPattern, '');
    cleaned = cleaned.replace(/\s+/g, ' ').trim();

    return cleaned;
}
```

* Session and message IDs use timestamp-based randomness so duplicates are unlikely without additional dependencies.
* `stripParametersFromContent` keeps prompts readable by removing any inline command-line style flags from history.
