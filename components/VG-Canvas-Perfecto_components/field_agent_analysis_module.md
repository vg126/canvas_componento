# Field Agent Analysis Module

Allows the Canvas app to call `@App-Creator` from within the sandbox and collect reports. The UI captures focus and context, shows streaming output, and stores a history.

```html
<!-- Doctor Inside Patient Tab -->
<div id="doctor-tab" class="tab-content hidden">
    <div class="mb-6">
        <h1 class="text-3xl font-bold mb-2">👨‍⚕️ Doctor Inside Patient Analysis</h1>
        <p class="text-gray-600 dark:text-gray-400">Call App-Creator from within Canvas for inside analysis</p>
    </div>

    <div class="grid gap-6">
        <!-- Analysis Request Interface -->
        <div class="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20 p-6 rounded-lg border">
            <h3 class="text-xl font-bold mb-4">🔍 Request Inside Analysis</h3>
            <div class="space-y-4">
                <div>
                    <label class="block font-medium mb-2">Analysis Focus</label>
                    <select id="analysisType" class="w-full p-3 text-base border rounded bg-white dark:bg-gray-700">
                        <option value="architecture">System Architecture Review</option>
                        <option value="feature-compatibility">Feature Compatibility Analysis</option>
                        <option value="performance">Performance & Optimization Review</option>
                        <option value="security">Security Boundary Analysis</option>
                        <option value="user-experience">User Experience Evaluation</option>
                        <option value="custom">Custom Analysis Request</option>
                    </select>
                </div>
                <div>
                    <label class="block font-medium mb-2">Specific Questions/Context</label>
                    <textarea id="analysisContext" class="w-full p-3 text-base border rounded bg-white dark:bg-gray-700" rows="3"
                        placeholder="Describe what you'd like App-Creator to analyze from inside this Canvas system..."></textarea>
                </div>
                <button id="requestAnalysis" class="w-full bg-green-600 text-white p-3 rounded-lg hover:bg-green-700 font-medium">
                    🩺 Request Field Agent Analysis
                </button>
            </div>
        </div>

        <!-- Analysis Results -->
        <div id="analysisResults" class="bg-white dark:bg-gray-800 p-6 rounded-lg border" style="display: none;">
            <h3 class="text-xl font-bold mb-4">📋 Field Agent Report</h3>
            <div id="analysisContent" class="prose dark:prose-invert max-w-none">
                <!-- Analysis results will appear here -->
            </div>
        </div>

        <!-- Analysis History -->
        <div class="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
            <h3 class="font-medium mb-3">📚 Analysis History</h3>
            <div id="analysisHistory" class="space-y-2 text-sm">
                <p class="text-gray-500 dark:text-gray-400">No analyses performed yet...</p>
            </div>
        </div>
    </div>
</div>
```

```javascript
document.getElementById('requestAnalysis').onclick = async () => {
    const analysisType = document.getElementById('analysisType').value;
    const context = document.getElementById('analysisContext').value;

    const systemPrompt = `
**CANVAS FIELD AGENT ANALYSIS REQUEST**

You are App-Creator operating as a "Field Agent" - called from INSIDE a Canvas application via sendUserMessage.

**Your Mission**: Analyze this Canvas system from the inside perspective.

**System Architecture Context**:
- You're in a dual-world system (Canvas UI State vs Poe Chat Context)
- Canvas apps have no localStorage (security sandboxed)
- Real context persists in underlying Poe chat, not Canvas display
- This app serves as: Guide + Lab + Live Documentation

**Analysis Type**: ${analysisType}
**Specific Context**: ${context}

**Your Payload Includes**:
- All HTML/CSS/JS code of this app (from chat history)
- Previous conversation context about Canvas architecture
- Any test results or findings from this session

**Your Response Should**:
- Analyze from the "inside experience" perspective
- Identify system behaviors you can observe from this vantage point
- Note any architectural insights visible from within Canvas
- Suggest improvements or discoveries
- Keep focus on practical Canvas development implications

**Remember**: You're experiencing this system as it actually executes, not theoretically. Report what you observe from inside.
    `;

    document.getElementById('analysisResults').style.display = 'block';
    document.getElementById('analysisContent').innerHTML = '<div class="animate-pulse">🔍 Field Agent analyzing...</div>';

    try {
        if (window.Poe?.sendUserMessage) {
            await window.Poe.sendUserMessage(`@App-Creator ${systemPrompt}`, {
                handler: "field-agent-handler",
                stream: true,
                openChat: false
            });
        } else {
            document.getElementById('analysisContent').innerHTML = '<span class="text-red-500">Poe API not available</span>';
        }
    } catch (error) {
        document.getElementById('analysisContent').innerHTML = `<span class="text-red-500">Error: ${error.message}</span>`;
    }
};
```
