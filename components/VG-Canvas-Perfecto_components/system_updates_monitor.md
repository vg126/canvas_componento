# System Updates Monitor

Surfaces a workflow for tracking platform changes: it triggers a `@SearchGPT` sweep and explains how to wash newly found updates back into the app.

```html
<!-- System Updates Tab -->
<div id="updates-tab" class="tab-content hidden">
    <div class="mb-6">
        <h1 class="text-3xl font-bold mb-2">🔄 Canvas System Updates</h1>
        <p class="text-gray-600 dark:text-gray-400">Monitor and integrate Canvas platform changes</p>
    </div>

    <div class="grid gap-6">
        <div class="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-lg border">
            <h3 class="text-xl font-bold mb-4">🔍 Update Detection</h3>
            <div class="space-y-4">
                <button id="checkUpdates" class="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700">
                    🌐 Search for Canvas Updates
                </button>
                <div id="updateResults" class="bg-white dark:bg-gray-700 p-4 rounded border min-h-32" style="display: none;">
                    <!-- Update search results -->
                </div>
            </div>
        </div>

        <div class="bg-yellow-50 dark:bg-yellow-900/20 p-6 rounded-lg border">
            <h3 class="text-xl font-bold mb-4">🧽 App Washing Process</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
                When updates are found, the "washing" process involves updating this app's knowledge base
                and testing matrix through the normal App-Creator workflow.
            </p>
            <div class="space-y-3">
                <div class="flex items-center space-x-2 text-sm">
                    <span class="w-6 h-6 bg-green-500 text-white rounded-full flex items-center justify-center">1</span>
                    <span>Detect changes via web search</span>
                </div>
                <div class="flex items-center space-x-2 text-sm">
                    <span class="w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center">2</span>
                    <span>Request Field Agent analysis of changes</span>
                </div>
                <div class="flex items-center space-x-2 text-sm">
                    <span class="w-6 h-6 bg-purple-500 text-white rounded-full flex items-center justify-center">3</span>
                    <span>Update feature database and testing matrix</span>
                </div>
                <div class="flex items-center space-x-2 text-sm">
                    <span class="w-6 h-6 bg-orange-500 text-white rounded-full flex items-center justify-center">4</span>
                    <span>Test new features in compatibility lab</span>
                </div>
            </div>
        </div>
    </div>
</div>
```

```javascript
document.getElementById('checkUpdates').onclick = async () => {
    document.getElementById('updateResults').style.display = 'block';
    document.getElementById('updateResults').innerHTML = '<div class="animate-pulse">🔍 Searching for Canvas updates...</div>';

    const searchQuery = `
Search for recent Poe Canvas application updates, new features, API changes, or documentation changes in 2024.
Focus on:
- New Canvas capabilities
- Poe Embed API changes
- Iframe sandbox policy updates
- New bot integration features
- Security or performance improvements

Provide structured findings with dates and sources.
    `;

    try {
        if (window.Poe?.sendUserMessage) {
            await window.Poe.sendUserMessage(`@SearchGPT ${searchQuery}`, {
                handler: "update-search-handler",
                stream: true,
                openChat: false
            });
        }
    } catch (error) {
        document.getElementById('updateResults').innerHTML = `<span class="text-red-500">Error: ${error.message}</span>`;
    }
};
```
