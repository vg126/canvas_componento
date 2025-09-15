# Conversation Context Manager

Maintains chat history and generates context-aware prompts for new messages.

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

    // Add message to conversation history
    addMessage(message, metadata = {}) {
        const messageEntry = {
            content: message.trim(),
            timestamp: new Date().toISOString(),
            sessionId: this.sessionId,
            id: this.generateMessageId(),
            ...metadata
        };

        this.conversationHistory.push(messageEntry);

        // Auto-truncate if enabled
        if (this.options.autoTruncate && this.conversationHistory.length > this.options.maxHistoryLength) {
            this.truncateHistory(this.options.maxHistoryLength);
        }

        this.notifyContextChange('messageAdded', messageEntry);
        return messageEntry;
    }

    // Generate context for current message
    generateContext(currentMessage, options = {}) {
        const contextOptions = { ...this.options, ...options };

        // Get previous messages (excluding the current one)
        const previousMessages = this.conversationHistory;

        if (previousMessages.length === 0) {
            // No previous context, return just the current message
            return {
                contextPrompt: currentMessage,
                hasContext: false,
                messageCount: 1,
                contextLength: currentMessage.length
            };
        }

        // Format context with clear separation
        const contextPrompt = this.formatContextPrompt(currentMessage, previousMessages, contextOptions);

        return {
            contextPrompt,
            hasContext: true,
            messageCount: this.conversationHistory.length + 1,
            previousMessageCount: previousMessages.length,
            contextLength: contextPrompt.length,
            estimatedTokens: this.estimateTokenCount(contextPrompt)
        };
    }

    // Format context prompt with clear separation
    formatContextPrompt(currentMessage, previousMessages, options = {}) {
        const separator = options.contextSeparator || this.options.contextSeparator;
        const useNumbers = options.numberedHistory !== false;
        const includeTimestamps = options.includeTimestamps || this.options.includeTimestamps;

        let contextPrompt = '';

        // Add conversational framing to help models understand the context
        contextPrompt += `You are having a conversation with a user through a chat interface. Please respond naturally to their message below.\n\n`;

        // Add previous conversation section
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

                line += msg.content;
                contextPrompt += line + '\n';
            });

            contextPrompt += '\n';
        }

        // Add current prompt section
        contextPrompt += `${separator} Current Prompt ${separator}\n`;
        contextPrompt += currentMessage;

        return contextPrompt;
    }

    // Estimate token count (rough approximation)
    estimateTokenCount(text) {
        if (!text) return 0;
        // Rough approximation: 1 token ≈ 4 characters for English text
        return Math.ceil(text.length / 4);
    }

    // Truncate history to specified length
    truncateHistory(maxLength) {
        if (this.conversationHistory.length > maxLength) {
            const removed = this.conversationHistory.splice(0, this.conversationHistory.length - maxLength);
            this.notifyContextChange('historyTruncated', { removedCount: removed.length });
        }
    }

    // Clear conversation history
    clearHistory() {
        const clearedCount = this.conversationHistory.length;
        this.conversationHistory = [];
        this.notifyContextChange('historyCleared', { clearedCount });
    }

    // Get context statistics
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

    // Sync with existing chat history
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

    // Event system methods
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

    // Generate unique session ID
    generateSessionId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    // Generate unique message ID
    generateMessageId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }
}
```
