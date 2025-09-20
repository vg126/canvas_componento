# Bot Panel Template

## Template
```html
<div id="bot1Container" class="mb-6 p-6 bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 rounded-lg border border-purple-200 dark:border-purple-800">
  <div class="mb-4">
    <div class="flex items-center justify-between mb-3">
      <h3 class="font-semibold text-purple-800 dark:text-purple-200 text-lg">🤖 Bot 1 - Initial Transformation</h3>
      <span id="bot1Status" class="text-sm text-purple-600 dark:text-purple-400"></span>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4">
      <div>
        <label class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">Model Selection</label>
        <div id="bot1Model" class="accordion-container"></div>
      </div>
      <div>
        <label class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">Prompt Status</label>
        <div id="bot1PromptStatus" class="text-sm text-gray-600 dark:text-gray-400 p-2 bg-white dark:bg-gray-800 rounded border border-gray-200 dark:border-gray-700">
          <span class="text-gray-500">No prompt loaded</span>
        </div>
      </div>
    </div>

    <div id="bot1Flags" class="hidden flag-container">
      <div id="bot1FlagControls"></div>
    </div>

    <button id="executeBot1" class="w-full px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors font-medium relative" onclick="executeBot(1)">
      <span id="executeBot1Text">⚡ Execute Bot 1</span>
      <div id="executeBot1Spinner" class="hidden absolute inset-0 flex items-center justify-center">
        <div class="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
      </div>
    </button>
  </div>

  <div class="border-t border-purple-200 dark:border-purple-700 pt-4">
    <div class="flex items-center justify-between mb-2">
      <h4 class="font-medium text-purple-700 dark:text-purple-300">Output</h4>
      <div class="flex space-x-2">
        <button onclick="copyBotOutput(1)" class="text-gray-500 hover:text-gray-700 dark:hover:text-gray-300" title="Copy">📋</button>
        <button onclick="downloadBotOutput(1)" class="text-gray-500 hover:text-gray-700 dark:hover:text-gray-300" title="Download">💾</button>
        <button onclick="clearBotOutput(1)" class="text-gray-500 hover:text-gray-700 dark:hover:text-gray-300" title="Clear">🗑️</button>
      </div>
    </div>
    <div id="bot1Output" class="prose dark:prose-invert max-w-none bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700 min-h-[100px] max-h-[400px] overflow-y-auto"></div>
  </div>
</div>
```

## How it works
- **Status header** labels each bot's specialism and surfaces a live status span (`bot1Status`) that the execution logic updates during streaming.
- **Model + prompt row** pairs the accordion picker with a prompt health tile so operators immediately see whether a template has been injected or needs attention.
- **Flag container** stays hidden until `flagManager` detects configurable parameters for the selected model, then renders sliders, selects, or advanced forms inside `bot1FlagControls`.
- **Execution control** swaps between text and spinner while `executeBot(1)` runs, ensuring each bot can signal busy/idle states independently.
- **Output toolbar** standardises copy/download/clear actions across all panels, writing the rendered Markdown transcript into `bot1Output` for later review or export.
