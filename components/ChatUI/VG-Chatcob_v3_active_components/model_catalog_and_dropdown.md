# Model Catalog and Dropdown Selector

v3 ships with an expanded hierarchical catalog and a compact dropdown explorer that replaces the earlier accordion.

## Catalog data shape

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
    // ... additional vendors elided for brevity ...
};
```

* Categories may contain arrays or nested maps of subcategories, so rendering helpers normalize both shapes.
* The database feeds both the dropdown content and the context search logic.

`appState` tracks dropdown behavior through `expandedSections`, `searchTerm`, and `filteredData`, letting the UI keep independent selection state even while the search box filters results.

## Opening and positioning the dropdown

```javascript
function openModelSelector() {
    const dropdown = document.getElementById('modelDropdown');
    const button = document.getElementById('modelSelectorBtn');
    const searchInput = document.getElementById('dropdownModelSearch');

    const buttonRect = button.getBoundingClientRect();
    const dropdownHeight = 400;

    dropdown.style.left = (buttonRect.left) + 'px';
    dropdown.style.bottom = (window.innerHeight - buttonRect.top + 10) + 'px';

    dropdown.classList.remove('hidden');

    setTimeout(() => {
        searchInput.focus();
        searchInput.value = '';
        appState.searchTerm = '';
        appState.filteredData = MODEL_DATABASE;
        renderDropdownAccordionContent();
    }, 50);
}
```

* Anchors the floating panel above the trigger button and clears any residual search state before populating content.

## Debounced search and filtering

```javascript
let searchTimeout = null;
function handleDropdownModelSearch(searchTerm) {
    if (searchTimeout) {
        clearTimeout(searchTimeout);
    }

    searchTimeout = setTimeout(() => {
        appState.searchTerm = searchTerm;
        appState.filteredData = filterAccordionData(MODEL_DATABASE, searchTerm);

        if (searchTerm) {
            Object.keys(appState.filteredData).forEach(category => {
                appState.expandedSections.add(category);
            });
        }

        requestAnimationFrame(() => {
            renderDropdownAccordionContent();
        });
    }, 200);
}
```

Supporting helpers keep the catalog responsive:

```javascript
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

* `highlightSearchTerm` decorates matched substrings with `<mark>` tags so results remain legible.
* Entire subcategories collapse if no entries match the query.

## Rendering and selection

```javascript
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
        // ...items rendered here...
        html += `</div></div>`;
    });

    if (html === '') {
        html = '<div class="p-4 text-center text-gray-500 dark:text-gray-400 text-xs">No models found</div>';
    }

    wrapper.innerHTML = html;
}
```

```javascript
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
```

```javascript
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
    closeModelSelector();
}
```

A document-level click handler delegates model row selection and dismisses the panel when the user interacts elsewhere, keeping the floating picker self-contained.
