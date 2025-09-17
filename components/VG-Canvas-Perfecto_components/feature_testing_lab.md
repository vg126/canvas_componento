# Feature Testing Lab

Provides a lightweight harness for validating prompt/server bot capabilities. Categories populate dynamically and tests dispatch via `window.Poe.sendUserMessage`.

```html
<!-- Feature Testing Lab Tab -->
<div id="testing-tab" class="tab-content hidden">
    <div class="mb-6">
        <h1 class="text-3xl font-bold mb-2">🧪 Canvas Feature Compatibility Lab</h1>
        <p class="text-gray-600 dark:text-gray-400">Test Server Bot & Prompt Bot features in Canvas environment</p>
    </div>

    <div class="grid gap-4">
        <div class="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
            <h3 class="font-medium mb-3">Select Category</h3>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-2" id="categoryGrid">
                <!-- Populated by JS -->
            </div>
        </div>

        <div class="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg" id="featureTestSection" style="display: none;">
            <div class="grid md:grid-cols-2 gap-4">
                <div>
                    <h3 class="font-medium mb-3">Feature Test</h3>
                    <div class="space-y-3">
                        <select id="featureSelect" class="w-full p-2 text-base border rounded bg-white dark:bg-gray-700">
                            <option>Select a feature...</option>
                        </select>
                        <select id="testBot" class="w-full p-2 text-base border rounded bg-white dark:bg-gray-700">
                            <option value="@Claude-Sonnet-4">@Claude-Sonnet-4</option>
                            <option value="@GPT-4o">@GPT-4o</option>
                        </select>
                        <button id="runQuickTest" class="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700">
                            🧪 Quick Test
                        </button>
                    </div>
                </div>
                <div>
                    <h3 class="font-medium mb-3">Results</h3>
                    <div id="quickTestResult" class="bg-white dark:bg-gray-700 p-3 rounded border min-h-24 text-sm">
                        Results will appear here...
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
```

```javascript
// Feature Database (from your research)
const featureDatabase = {
    "Core Prompt Construction": [
        { name: "Plain-text instructions", types: ["Prompt Bot"], testPrompt: "Act as a helpful assistant with expertise in marine biology." },
        { name: "Templating with {{user_prompt}}", types: ["Prompt Bot"], testPrompt: "Context: {{user_prompt}} Please analyze this systematically." }
    ],
    "Response Behavior": [
        { name: "Temperature control", types: ["Prompt Bot", "Server Bot"], testPrompt: "Write a creative story. Make it very consistent and predictable." },
        { name: "stop_sequences", types: ["Server Bot"], testPrompt: "Count to 10 then write STOP to end." }
    ],
    "Output Formatting": [
        { name: "Markdown rendering", types: ["Prompt Bot"], testPrompt: "Format this with **bold**, *italic*, and `code` formatting." },
        { name: "HTML code blocks", types: ["Server Bot"], testPrompt: "Create a simple HTML button that changes color on click." }
    ]
};

let testResults = {};

// Initialize Feature Testing
function initTesting() {
    const categoryGrid = document.getElementById('categoryGrid');
    Object.keys(featureDatabase).forEach(category => {
        const btn = document.createElement('button');
        btn.className = 'p-2 bg-white dark:bg-gray-700 rounded border hover:border-blue-500 text-sm';
        btn.textContent = category;
        btn.onclick = () => selectCategory(category);
        categoryGrid.appendChild(btn);
    });
}

function selectCategory(category) {
    const select = document.getElementById('featureSelect');
    select.innerHTML = '<option>Select a feature...</option>';

    featureDatabase[category].forEach(feature => {
        const option = document.createElement('option');
        option.value = JSON.stringify(feature);
        option.textContent = feature.name;
        select.appendChild(option);
    });

    document.getElementById('featureTestSection').style.display = 'block';
}

// Quick Test Function
document.getElementById('runQuickTest').onclick = async () => {
    const featureData = document.getElementById('featureSelect').value;
    const bot = document.getElementById('testBot').value;

    if (featureData === 'Select a feature...') return;

    const feature = JSON.parse(featureData);
    const resultDiv = document.getElementById('quickTestResult');

    resultDiv.innerHTML = '<div class="animate-pulse">🧪 Testing...</div>';

    const testPrompt = `${bot} ${feature.testPrompt}`;

    try {
        if (window.Poe?.sendUserMessage) {
            await window.Poe.sendUserMessage(testPrompt, {
                handler: "quick-test-handler",
                stream: false,
                openChat: false
            });
        } else {
            resultDiv.innerHTML = '<span class="text-red-500">Poe API not available</span>';
        }
    } catch (error) {
        resultDiv.innerHTML = `<span class="text-red-500">Error: ${error.message}</span>`;
    }
};

// Initialize
initTesting();
```
