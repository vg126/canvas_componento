# Theme Modal & Controls

Presents a floating palette launcher that opens a modal of curated theme presets. Selecting an option updates the `data-theme` attribute and toggles ornamental classes.

```html
<!-- Theme Button (Fixed Position) -->
<button
    id="themeButton"
    onclick="openThemeModal()"
    class="fixed bottom-6 right-6 w-12 h-12 bg-purple-600 hover:bg-purple-700 text-white rounded-full shadow-lg transition-all duration-200 flex items-center justify-center z-50 text-xl"
    title="Theme Settings"
>
    🎨
</button>

<!-- Theme Modal -->
<div id="themeModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 hidden">
    <div class="bg-white dark:bg-gray-800 rounded-lg w-96 max-w-90vw max-h-90vh overflow-y-auto shadow-2xl">
        <div class="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-600">
            <h3 class="text-lg font-semibold">🎨 Theme Settings</h3>
            <button onclick="closeThemeModal()" class="text-gray-500 hover:text-gray-700 dark:hover:text-gray-300">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
            </button>
        </div>
        <div class="p-4 space-y-4">
            <!-- Default Theme -->
            <button
                onclick="applyTheme('default'); closeThemeModal();"
                class="w-full flex items-center gap-3 p-3 bg-gray-50 hover:bg-gray-100 dark:bg-gray-700 dark:hover:bg-gray-600 rounded-lg transition-colors"
            >
                <div class="w-6 h-6 rounded border bg-gradient-to-r from-blue-500 to-purple-500"></div>
                <span class="font-medium">📄 Clean Default</span>
            </button>

            <!-- Terminal Theme -->
            <button
                onclick="applyTheme('terminal'); closeThemeModal();"
                class="w-full flex items-center gap-3 p-3 bg-gray-50 hover:bg-gray-100 dark:bg-gray-700 dark:hover:bg-gray-600 rounded-lg transition-colors"
            >
                <div class="w-6 h-6 rounded border bg-gradient-to-r from-green-400 to-black"></div>
                <span class="font-medium">💻 Terminal Hacker</span>
            </button>

            <!-- Steampunk Theme -->
            <button
                onclick="applyTheme('steampunk'); closeThemeModal();"
                class="w-full flex items-center gap-3 p-3 bg-gray-50 hover:bg-gray-100 dark:bg-gray-700 dark:hover:bg-gray-600 rounded-lg transition-colors"
            >
                <div class="w-6 h-6 rounded border bg-gradient-to-r from-yellow-600 to-amber-800"></div>
                <span class="font-medium">⚙️ Steampunk Victorian</span>
            </button>

            <!-- Neon Theme -->
            <button
                onclick="applyTheme('neon'); closeThemeModal();"
                class="w-full flex items-center gap-3 p-3 bg-gray-50 hover:bg-gray-100 dark:bg-gray-700 dark:hover:bg-gray-600 rounded-lg transition-colors"
            >
                <div class="w-6 h-6 rounded border bg-gradient-to-r from-pink-500 to-cyan-400"></div>
                <span class="font-medium">🌈 Neon Cyberpunk</span>
            </button>

            <!-- Forest Theme -->
            <button
                onclick="applyTheme('forest'); closeThemeModal();"
                class="w-full flex items-center gap-3 p-3 bg-gray-50 hover:bg-gray-100 dark:bg-gray-700 dark:hover:bg-gray-600 rounded-lg transition-colors"
            >
                <div class="w-6 h-6 rounded border bg-gradient-to-r from-green-500 to-emerald-600"></div>
                <span class="font-medium">🌲 Forest Harmony</span>
            </button>
        </div>
    </div>
</div>
```

```javascript
function applyTheme(themeName) {
    document.documentElement.setAttribute('data-theme', themeName);

    if (themeName === 'terminal') {
        document.body.classList.add('terminal-mode');
    } else {
        document.body.classList.remove('terminal-mode');
    }

    if (themeName === 'steampunk') {
        document.body.classList.add('steampunk-mode');
    } else {
        document.body.classList.remove('steampunk-mode');
    }

    if (themeName === 'neon') {
        document.body.classList.add('neon-mode');
    } else {
        document.body.classList.remove('neon-mode');
    }
}

function openThemeModal() {
    document.getElementById('themeModal').classList.remove('hidden');
}

function closeThemeModal() {
    document.getElementById('themeModal').classList.add('hidden');
}
```
