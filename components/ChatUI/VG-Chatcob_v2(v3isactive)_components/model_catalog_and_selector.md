# Model Catalog and Selector

Structured catalog of available models and the dropdown selector that lets users pick a target model quickly.

```javascript
const MODEL_DATABASE = {
    "Favorites": [
        "GPT-5", "App-Creator", "o3-pro", "o1", "Gemini-2.5-Pro", "Claude-Opus-4-Reasoning",
        "Claude-Opus-4.1", "Claude-Opus-4-Search", "Claude-Sonnet-4-Search", "Grok-4", "Mistral-Large-2"
    ],
    "Web Search": [
        "Web-Search", "Claude-Opus-4-Search", "Claude-Sonnet-4-Search", "Claude-Sonnet-3.7-Search",
        "Claude-Sonnet-3.5-Search", "Claude-Haiku-3.5-Search", "Gemini-2.5-Pro", "Gemini-2.5-Flash",
        "Gemini-1.5-Pro-Search", "Gemini-1.5-Flash-Search", "GPT-4o-Search", "GPT-4o-mini-Search",
        "Grok-4", "Perplexity-Sonar", "Perplexity-Sonar-Pro", "Perplexity-Sonar-Rsn",
        "Perplexity-Sonar-Rsn-Pro", "Linkup-Deep-Search", "Linkup-Standard", "Bagoodex-Web-Search",
        "Reka-Research", "GPT-Researcher"
    ],
    "GPT": {
        "GPT-5 Series": ["GPT-5", "GPT-5-Chat", "GPT-5-mini", "GPT-5-nano"],
        "GPT-4 Series": [
            "GPT-4.1", "GPT-4.1-mini", "GPT-4.1-nano", "GPT-4o", "GPT-4o-Aug", "GPT-4o-Search",
            "GPT-4o-mini", "GPT-4o-mini-Search", "GPT-4-Classic", "GPT-4-Classic-0314",
            "GPT-4-Turbo", "ChatGPT-4o-Latest"
        ],
        "GPT-3.5 Series": ["GPT-3.5-Turbo", "GPT-3.5-Turbo-Instruct", "GPT-3.5-Turbo-Raw"],
        "o-Series": ["o1", "o1-mini", "o3", "o3-pro", "o3-mini", "o3-mini-high", "o4-mini"]
    },
    "GPT - Open Weight": {
        "120B Models": [
            "GPT-OSS-120B", "GPT-OSS-120B-T", "GPT-OSS-120B-CS", "GPT-OSS-120B-Omni", "OpenAI-GPT-OSS-120B"
        ],
        "20B Models": ["GPT-OSS-20B", "GPT-OSS-20B-T", "OpenAI-GPT-OSS-20B"]
    },
    "Google": {
        "Gemini 2.5": ["Gemini-2.5-Pro", "Gemini-2.5-Flash", "Gemini-2.5-Flash-Lite", "Gemini-2.5-Flash-Image"],
        "Gemini 2.0": ["Gemini-2.0-Flash", "Gemini-2.0-Flash-Lite", "Gemini-2.0-Flash-Preview"],
        "Gemini 1.5": ["Gemini-1.5-Pro", "Gemini-1.5-Pro-Search", "Gemini-1.5-Flash", "Gemini-1.5-Flash-Search"],
        "Gemma": ["Gemma-3-27B", "Gemma-2-27b-T"]
    },
    "Claude": {
        "Opus": [
            "Claude-Opus-4.1", "Claude-Opus-4", "Claude-Opus-4-Reasoning",
            "Claude-Opus-4-Search", "Claude-Opus-3"
        ],
        "Sonnet": [
            "Claude-Sonnet-4", "Claude-Sonnet-4-Reasoning", "Claude-Sonnet-4-Search",
            "Claude-Sonnet-3.7", "Claude-Sonnet-3.7-Reasoning", "Claude-Sonnet-3.7-Search",
            "Claude-Sonnet-3.5", "Claude-Sonnet-3.5-June", "Claude-Sonnet-3.5-Search"
        ],
        "Haiku": ["Claude-Haiku-3.5", "Claude-Haiku-3.5-Search", "Claude-Haiku-3"]
    }
    // Additional vendors continue in the source file (Grok, Llama, Qwen, DeepSeek, Mistral, Perplexity, Reasoning, Specialty Tools, Wildcards)
};
```

```javascript
function renderModelItem(model, isSubcategory = false) {
    const isSelected = appState.selectedModel === model;
    const paddingClass = isSubcategory ? 'pl-8' : 'pl-6';

    return `
        <div class="model-item ${paddingClass} pr-3 py-2 cursor-pointer ${isSelected ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'}"
             data-model="${model}">
            <div class="flex items-center justify-between">
                <span class="text-sm ${isSelected ? 'font-medium' : ''}">${highlightSearchTerm(model, appState.searchTerm)}</span>
                ${isSelected ? '<span class="text-blue-500 text-xs">✓</span>' : ''}
            </div>
        </div>
    `;
}

function processCategoryItems(items, searchTerm) {
    if (Array.isArray(items)) {
        return filterItems(items, searchTerm);
    } else {
        const result = [];
        Object.values(items).forEach(subitems => {
            if (Array.isArray(subitems)) {
                result.push(...filterItems(subitems, searchTerm));
            }
        });
        return result;
    }
}

function filterItems(items, searchTerm) {
    if (!searchTerm || !Array.isArray(items)) return items;
    return items.filter(item =>
        item.toLowerCase().includes(searchTerm.toLowerCase())
    );
}

function highlightSearchTerm(text, searchTerm) {
    if (!searchTerm) return text;
    const regex = new RegExp(`(${searchTerm})`, 'gi');
    return text.replace(regex, '<mark class="bg-yellow-200 dark:bg-yellow-800">$1</mark>');
}

function filterAccordionData(data, searchTerm) {
    if (!searchTerm) return data;

    const filtered = {};

    Object.entries(data).forEach(([category, items]) => {
        if (Array.isArray(items)) {
            const filteredItems = filterItems(items, searchTerm);
            if (filteredItems.length > 0) {
                filtered[category] = filteredItems;
            }
        } else {
            const filteredSubcategories = {};
            Object.entries(items).forEach(([subcat, subitems]) => {
                const filteredSub = filterItems(subitems, searchTerm);
                if (filteredSub.length > 0) {
                    filteredSubcategories[subcat] = filteredSub;
                }
            });
            if (Object.keys(filteredSubcategories).length > 0) {
                filtered[category] = filteredSubcategories;
            }
        }
    });

    return filtered;
}
```

```javascript
function updateModelDisplay() {
    const searchInput = document.getElementById('modelSearch');
    const currentModelDisplay = document.getElementById('currentModelDisplay');

    if (searchInput) {
        searchInput.placeholder = `Search models... (Current: ${appState.selectedModel})`;
        searchInput.value = '';
    }

    if (currentModelDisplay) {
        currentModelDisplay.textContent = appState.selectedModel;
    }

    appState.searchTerm = '';
    appState.filteredData = MODEL_DATABASE;
}

function openModelSelector() {
    const dropdown = document.getElementById('modelDropdown');
    const button = document.getElementById('modelSelectorBtn');
    const searchInput = document.getElementById('dropdownModelSearch');

    // Position dropdown above the button
    const buttonRect = button.getBoundingClientRect();
    const dropdownHeight = 400; // max height

    dropdown.style.left = (buttonRect.left) + 'px';
    dropdown.style.bottom = (window.innerHeight - buttonRect.top + 10) + 'px';

    dropdown.classList.remove('hidden');

    // Focus search input and render content
    setTimeout(() => {
        searchInput.focus();
        searchInput.value = '';
        appState.searchTerm = '';
        appState.filteredData = MODEL_DATABASE;
        renderDropdownAccordionContent();
    }, 50);
}

function closeModelSelector() {
    const dropdown = document.getElementById('modelDropdown');
    dropdown.classList.add('hidden');
}

let searchTimeout = null;
function handleDropdownModelSearch(searchTerm) {
    // Clear previous timeout
    if (searchTimeout) {
        clearTimeout(searchTimeout);
    }

    // Debounce search by 200ms
    searchTimeout = setTimeout(() => {
        appState.searchTerm = searchTerm;
        appState.filteredData = filterAccordionData(MODEL_DATABASE, searchTerm);

        // Auto-expand sections with results when searching
        if (searchTerm) {
            Object.keys(appState.filteredData).forEach(category => {
                appState.expandedSections.add(category);
            });
        }

        // Use requestAnimationFrame for smooth rendering
        requestAnimationFrame(() => {
            renderDropdownAccordionContent();
        });
    }, 200);
}

function renderDropdownAccordionContent() {
    const wrapper = document.getElementById('dropdownAccordionWrapper');
    if (!wrapper) return;

    let html = '';

    Object.entries(appState.filteredData).forEach(([category, items]) => {
        const isExpanded = appState.expandedSections.has(category);
        const categoryItems = processCategoryItems(items, appState.searchTerm);

        if (categoryItems.length === 0 && appState.searchTerm) return;

        html += `
            <div class="border-b border-gray-200 dark:border-gray-600">
                <div class="flex items-center justify-between p-2 cursor-pointer bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                     onclick="toggleDropdownSection('${category}', event)">
                    <span class="font-medium text-xs text-gray-900 dark:text-white">${category}</span>
                    <div class="flex items-center space-x-1">
                        <span class="text-xs text-gray-500 dark:text-gray-400">(${categoryItems.length})</span>
                        <span class="text-gray-500 dark:text-gray-400 transition-transform duration-200 ${isExpanded ? 'rotate-90' : ''}">${isExpanded ? '▼' : '▶'}</span>
                    </div>
                </div>
                <div class="transition-all duration-200 overflow-hidden ${isExpanded ? '' : 'max-h-0'}">
        `;

        if (Array.isArray(items)) {
            categoryItems.forEach(item => {
                html += renderDropdownModelItem(item);
            });
        } else {
            Object.entries(items).forEach(([subcategory, subitems]) => {
                const filteredSubitems = filterItems(subitems, appState.searchTerm);
                if (filteredSubitems.length === 0 && appState.searchTerm) return;

                html += `
                    <div class="pl-3 border-l border-gray-200 dark:border-gray-600">
                        <div class="text-xs font-medium text-gray-600 dark:text-gray-400 p-1 bg-gray-25 dark:bg-gray-750">${subcategory}</div>
                `;

                filteredSubitems.forEach(item => {
                    html += renderDropdownModelItem(item, true);
                });

                html += `</div>`;
            });
        }

        html += `</div></div>`;
    });

    if (html === '') {
        html = '<div class="p-4 text-center text-gray-500 dark:text-gray-400 text-xs">No models found</div>';
    }

    wrapper.innerHTML = html;
}

function renderDropdownModelItem(model, isSubcategory = false) {
    const isSelected = appState.selectedModel === model;
    const paddingClass = isSubcategory ? 'pl-6' : 'pl-4';

    return `
        <div class="model-item ${paddingClass} pr-2 py-1 cursor-pointer ${isSelected ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'}"
             data-model="${model}">
            <div class="flex items-center justify-between">
                <span class="text-xs ${isSelected ? 'font-medium' : ''}">${highlightSearchTerm(model, appState.searchTerm)}</span>
                ${isSelected ? '<span class="text-blue-500 text-xs">✓</span>' : ''}
            </div>
        </div>
    `;
}

function toggleDropdownSection(category, event) {
    if (event) {
        event.stopPropagation();
    }
    if (appState.expandedSections.has(category)) {
        appState.expandedSections.delete(category);
    } else {
        appState.expandedSections.add(category);
    }
    renderDropdownAccordionContent();
}

function selectDropdownModel(model) {
    appState.selectedModel = model;
    updateModelDisplay();
    closeModelSelector(); // Close dropdown
}
```
