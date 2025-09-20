# Input Configuration Layout

## Template
```html
<div id="tab-content-input" class="tab-content active">
  <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 mb-6">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold">📝 Input Configuration</h2>
      <div class="flex space-x-2 text-sm">
        <button id="saveStateInput" class="p-2" title="Copy State to Clipboard">💾</button>
        <button id="downloadStateInput" class="p-2" title="Download State as File">📥</button>
        <button id="loadStateInput" class="p-2" title="Load State from File">📁</button>
        <button id="importStateInput" class="p-2" title="Import State from Clipboard">📋</button>
        <button id="downloadFlow" class="p-2" title="Download Responses">📄</button>
      </div>
    </div>

    <section class="mb-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
      <h3 class="font-semibold mb-3 text-blue-800 dark:text-blue-200">📁 File Upload Center</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <label class="text-sm space-y-2 text-center">
          <span class="block font-medium">Legal Texts Database</span>
          <input type="file" id="legalTextFile" accept=".json" class="w-full text-sm" />
          <span class="block text-xs text-gray-500">JSON array of legal texts</span>
        </label>
        <label class="text-sm space-y-2 text-center">
          <span class="block font-medium">SST Techniques Database</span>
          <input type="file" id="sstDatabaseFile" accept=".json" class="w-full text-sm" />
          <span class="block text-xs text-gray-500">Hierarchical SST database</span>
        </label>
        <label class="text-sm space-y-2 text-center">
          <span class="block font-medium">Bot Prompts Database</span>
          <input type="file" id="botPromptsFile" accept=".json" class="w-full text-sm" />
          <span class="block text-xs text-gray-500">Bot prompt templates</span>
        </label>
      </div>
      <div class="mt-3 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
        <span id="legalTextDatabaseStatus">No database loaded</span>
        <span id="sstDatabaseStatus">No database loaded</span>
        <span id="botPromptsDatabaseStatus">No database loaded</span>
      </div>
    </section>

    <section class="mb-4">
      <label class="block text-sm font-medium mb-2">Legal Text (e.g., ICC Article 17)</label>
      <div class="relative">
        <textarea id="legalText" rows="4" class="w-full p-3 border rounded-lg"></textarea>
        <div class="absolute top-2 right-2 flex space-x-1">
          <button id="copyLegalText" class="p-1" title="Copy to Clipboard">📋</button>
          <button id="feedLegalText" class="p-1" title="Feed to Preview">📤</button>
        </div>
      </div>
      <div class="mt-3 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
        <h4 class="font-semibold mb-2 text-blue-800 dark:text-blue-200 text-sm">📖 Legal Text Database</h4>
        <div class="flex items-center space-x-3 mt-2 text-sm">
          <div class="flex items-center space-x-2">
            <label class="text-gray-600 dark:text-gray-400">Find by ID:</label>
            <input type="text" id="legalTextSearch" class="w-20 px-2 py-1 border rounded" placeholder="ID" />
            <button id="loadLegalTextById" class="px-3 py-1 bg-blue-600 text-white rounded" disabled>Load</button>
          </div>
          <button id="randomizeLegalText" class="px-3 py-1 bg-green-600 text-white rounded" disabled>🎲 Random</button>
        </div>
      </div>
    </section>

    <section class="mb-4">
      <label class="block text-sm font-medium mb-2">SST Technique</label>
      <div class="relative">
        <textarea id="sstCapsule" rows="3" class="w-full p-3 border rounded-lg"></textarea>
        <div class="absolute top-2 right-2 flex space-x-1">
          <button id="copySSTCapsule" class="p-1" title="Copy to Clipboard">📋</button>
          <button id="feedSSTCapsule" class="p-1" title="Feed to Preview">📤</button>
        </div>
      </div>
      <div class="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
        <h3 class="font-semibold mb-3 text-blue-800 dark:text-blue-200">🎯 Manual SST Selection</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-3">
          <label class="block text-sm font-medium">Domain
            <select id="sstDomainSelect" class="w-full p-2 border rounded">
              <option value="">Select a domain...</option>
            </select>
          </label>
          <label class="block text-sm font-medium">Technique
            <select id="sstTechniqueSelect" class="w-full p-2 border rounded" disabled>
              <option value="">Select a technique...</option>
            </select>
          </label>
        </div>
        <div class="flex flex-wrap gap-2 text-sm">
          <button id="loadTechniqueCapsule" class="px-3 py-1 bg-blue-600 text-white rounded" disabled>📥 Load Technique Capsule</button>
          <button id="previewTechnique" class="px-3 py-1 bg-purple-600 text-white rounded" disabled>👁️ Preview Technique</button>
          <button id="sampleSSTBtn" class="px-4 py-2 bg-gray-200 dark:bg-gray-600 text-sm rounded">🎲 Sample Random SST</button>
        </div>
      </div>
    </section>
  </div>
</div>
```

## How it works
- **State-first controls** keep clipboard, download, and import buttons visible so researchers can snapshot the entire session before running any analyses.
- **File Upload Centre** ingests three optional JSON payloads (legal texts, SST techniques, bot prompts) and displays their load status, making it obvious when the internal libraries are ready.
- **Legal Text authoring** combines freeform drafting with quick database recall: users can load specific IDs, randomise a sample, copy to clipboard, or stage the content for downstream preview tools.
- **SST Technique authoring** mirrors the legal text editor, but adds cascading dropdowns for selecting pre-built SST capsules and helper buttons for previewing or sampling techniques.
- **Assistive buttons** remain disabled until supporting data is loaded, preventing broken flows while guiding users through the recommended preparation order.
