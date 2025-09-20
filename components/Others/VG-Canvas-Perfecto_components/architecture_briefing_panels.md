# Architecture Briefing Panels

Documents the storytelling layout that explains Canvas vs Poe realities and key operating principles right inside the app.

```html
<!-- Architecture Documentation Tab -->
<div id="architecture-tab" class="tab-content">
    <div class="mb-6">
        <h1 class="text-3xl font-bold mb-2">🏗️ Canvas & Poe Dual-World Architecture</h1>
        <p class="text-gray-600 dark:text-gray-400">Living documentation of Canvas system realities</p>
    </div>

    <div class="grid gap-6">
        <!-- The Dual World System -->
        <div class="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 p-6 rounded-lg border">
            <h2 class="text-2xl font-bold mb-4">🌍 The Dual-World Reality</h2>
            <div class="grid md:grid-cols-2 gap-6">
                <div class="bg-white dark:bg-gray-800 p-4 rounded-lg border">
                    <h3 class="font-bold text-blue-600 dark:text-blue-400 mb-3">World 1: Poe Chat Context</h3>
                    <ul class="space-y-2 text-sm">
                        <li>✅ <strong>Real conversation context</strong></li>
                        <li>✅ <strong>Survives Canvas refresh</strong></li>
                        <li>✅ <strong>Drives actual AI responses</strong></li>
                        <li>✅ <strong>Accessible via sendUserMessage</strong></li>
                        <li>❌ <strong>Not directly controllable from Canvas</strong></li>
                    </ul>
                </div>
                <div class="bg-white dark:bg-gray-800 p-4 rounded-lg border">
                    <h3 class="font-bold text-purple-600 dark:text-purple-400 mb-3">World 2: Canvas UI State</h3>
                    <ul class="space-y-2 text-sm">
                        <li>✅ <strong>Visual interface & settings</strong></li>
                        <li>✅ <strong>Interactive elements</strong></li>
                        <li>✅ <strong>Exportable as JSON</strong></li>
                        <li>❌ <strong>Lost on refresh (by design)</strong></li>
                        <li>❌ <strong>No localStorage (security sandbox)</strong></li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- Critical Operations -->
        <div class="bg-yellow-50 dark:bg-yellow-900/20 p-6 rounded-lg border border-yellow-200 dark:border-yellow-800">
            <h3 class="text-xl font-bold mb-4">⚠️ Critical Operations & User Expectations</h3>
            <div class="grid md:grid-cols-3 gap-4 text-sm">
                <div class="bg-white dark:bg-gray-800 p-4 rounded border">
                    <h4 class="font-medium text-red-600 dark:text-red-400">Canvas Refresh Button</h4>
                    <p class="text-gray-600 dark:text-gray-400 mt-2">Users expect: Complete reset</p>
                    <p class="text-green-600 dark:text-green-400">Reality: Only UI resets, context persists</p>
                </div>
                <div class="bg-white dark:bg-gray-800 p-4 rounded border">
                    <h4 class="font-medium text-green-600 dark:text-green-400">Chat Clear Context</h4>
                    <p class="text-gray-600 dark:text-gray-400 mt-2">Location: Poe chat UI (paintbrush icon)</p>
                    <p class="text-green-600 dark:text-green-400">Reality: Actually clears conversation</p>
                </div>
                <div class="bg-white dark:bg-gray-800 p-4 rounded border">
                    <h4 class="font-medium text-orange-600 dark:text-orange-400">Canvas "Clear Context"</h4>
                    <p class="text-gray-600 dark:text-gray-400 mt-2">Status: Experimental/Impossible</p>
                    <p class="text-orange-600 dark:text-orange-400">Reality: UI placeholder only</p>
                </div>
            </div>
        </div>

        <!-- Developer Principles -->
        <div class="bg-gray-50 dark:bg-gray-800 p-6 rounded-lg">
            <h3 class="text-xl font-bold mb-4">🎯 Core Development Principles</h3>
            <div class="grid md:grid-cols-2 gap-4">
                <div class="space-y-3 text-sm">
                    <div class="flex items-start space-x-2">
                        <span class="text-blue-500 font-bold">1.</span>
                        <span><strong>Two Contexts Rule:</strong> Canvas display ≠ real context</span>
                    </div>
                    <div class="flex items-start space-x-2">
                        <span class="text-blue-500 font-bold">2.</span>
                        <span><strong>Refresh Reality:</strong> Visual reset ≠ context reset</span>
                    </div>
                    <div class="flex items-start space-x-2">
                        <span class="text-blue-500 font-bold">3.</span>
                        <span><strong>State Limitations:</strong> Export/import is UI-only</span>
                    </div>
                </div>
                <div class="space-y-3 text-sm">
                    <div class="flex items-start space-x-2">
                        <span class="text-purple-500 font-bold">4.</span>
                        <span><strong>Sync Necessity:</strong> Context reconstruction required</span>
                    </div>
                    <div class="flex items-start space-x-2">
                        <span class="text-purple-500 font-bold">5.</span>
                        <span><strong>Security Boundaries:</strong> No localStorage, limited DOM access</span>
                    </div>
                    <div class="flex items-start space-x-2">
                        <span class="text-purple-500 font-bold">6.</span>
                        <span><strong>Persistence Strategy:</strong> Use chat context via sendUserMessage</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
```
