# Accordion Model Picker (Rebuilt)

## Model Database
```js
        const MODEL_DATABASE = {
            "Favorites": [
                "@GPT-5", "@GPT-4.1", "@o3-pro", "@o1", "@Gemini-2.5-Pro",
                "@Claude-Opus-4-Reasoning", "@Claude-Opus-4.1", "@Claude-Opus-4-Search",
                "@Claude-Sonnet-4-Search", "@Grok-4", "@Mistral-Large-2"
            ],
            "Web Search": [
                "@Claude-Opus-4-Search", "@Claude-Sonnet-4-Search", "@Claude-Sonnet-3.7-Search",
                "@Gemini-2.5-Flash", "@Gemini-2.5-Pro", "@Grok-4",
                "@Perplexity-Sonar", "@Perplexity-Sonar-Rsn-Pro",
                "@GPT-4o-Search", "@Linkup-Deep-Search", "@Linkup-Standard",
                "@Bagoodex-Web-Search"
            ],
            "GPT": {
                "GPT-5 Series": ["@GPT-5-Chat", "@GPT-5", "@GPT-5-mini", "@GPT-5-nano"],
                "GPT-4 Series": [
                    "@GPT-4.1", "@GPT-4o-Search", "@GPT-4-Classic", "@GPT-4-Classic-0314",
                    "@GPT-4-Turbo", "@GPT-4.1-mini", "@GPT-4.1-nano", "@GPT-4o",
                    "@GPT-4o-mini", "@GPT-4o-mini-Search", "@GPT-4o-Aug", "@ChatGPT-4o-Latest"
                ],
                "GPT-3.5 Series": ["@GPT-3.5-Turbo", "@GPT-3.5-Turbo-Instruct", "@GPT-3.5-Turbo-Raw"],
                "o-Series": ["@o1", "@o3", "@o3-pro", "@o1-mini", "@o3-mini", "@o3-mini-high", "@o4-mini", "@o3-Pro"]
            },
            "GPT - Open Weight": {
                "120B Models": ["@GPT-OSS-120B-T", "@GPT-OSS-120B", "@GPT-OSS-120B-CS", "@OpenAI-GPT-OSS-120B"],
                "20B Models": ["@GPT-OSS-20B-T", "@GPT-OSS-20B", "@OpenAI-GPT-OSS-20B"]
            },
            "Google": {
                "Gemini 2.5": [
                    "@Gemini-2.5-Pro", "@Gemini-2.5-Flash", "@Gemini-2.5-Flash-Lite",
                    "@Gemini-2.5-Flash-Lite-Preview", "@Gemini-2.5-Flash-Image"
                ],
                "Gemini 2.0": ["@Gemini-2.0-Flash", "@Gemini-2.0-Flash-Lite", "@Gemini-2.0-Flash-Preview"],
                "Gemini 1.5": ["@Gemini-1.5-Pro", "@Gemini-1.5-Pro-Search", "@Gemini-1.5-Flash", "@Gemini-1.5-Flash-Search"],
                "Gemma": ["@Gemma-3-27B", "@Gemma-2-27b-T"]
            },
            "Claude": {
                "Opus": [
                    "@Claude-Opus-4.1", "@Claude-Opus-4", "@Claude-Opus-4-Reasoning",
                    "@Claude-Opus-4-Search", "@Claude-Opus-3"
                ],
                "Sonnet": [
                    "@Claude-Sonnet-4", "@Claude-Sonnet-4-Reasoning", "@Claude-Sonnet-4-Search",
                    "@Claude-Sonnet-3.5", "@Claude-Sonnet-3.5-June", "@Claude-Sonnet-3.5-Search",
                    "@Claude-Sonnet-3.7", "@Claude-Sonnet-3.7-Reasoning", "@Claude-Sonnet-3.7-Search"
                ],
                "Haiku": ["@Claude-Haiku-3.5", "@Claude-Haiku-3", "@Claude-Haiku-3.5-Search"]
            },
            "Grok": ["@Grok-4", "@Grok-3", "@Grok-3-Mini", "@Grok-Code-Fast-1", "@Grok-2"],
            "Llama 4": [
                "@Llama-4-Scout-B10", "@Llama-4-Maverick", "@Llama-4-Scout-T",
                "@Llama-4-Scout-CS", "@Llama-4-Scout", "@Llama-4-Maverick-T", "@Llama-4-Maverick-B10"
            ],
            "Llama 3.X": {
                "405B Models": ["@Llama-3.1-405B", "@Llama-3.1-405B-T", "@Llama-3.1-405B-FW", "@Llama-3.1-405B-FP16"],
                "70B Models": [
                    "@Llama-3-70b-Groq", "@Llama-3.3-70B", "@Llama-3.1-Nemotron",
                    "@Llama-3.3-70B-DI", "@Llama-3.3-70B-CS", "@Llama-3.3-70B-Vers",
                    "@Llama-3-70B-FP16", "@Llama-3-70B-T", "@Llama-3.1-70B",
                    "@Llama-3.1-70B-FP16", "@Llama-3.1-70B-FW", "@Llama-3.1-70B-T",
                    "@Llama-3.3-70B-FW", "@Llama-3.3-70B-N"
                ],
                "8B Models": [
                    "@Llama-3-8B-T", "@Llama-3-8b-Groq", "@Llama-3.1-8B",
                    "@Llama-3.1-8B-CS", "@Llama-3.1-8B-DI", "@Llama-3.1-8B-FP16",
                    "@Llama-3.1-8B-FW", "@Llama-3.1-8B-T-128k"
                ]
            },
            "Qwen": {
                "480B": ["@Qwen3-480B-Coder-CS", "@Qwen3-Coder-480B-T", "@Qwen3-Coder-480B-N"],
                "235B": [
                    "@Qwen-3-235B-2507-T", "@Qwen3-235B-2507-FW", "@Qwen3-235B-2507-CS",
                    "@Qwen3-235B-A22B", "@Qwen3-235B-A22B-DI", "@Qwen3-235B-A22B-N", "@Qwen3-235B-Think-CS"
                ],
                "72B": ["@Qwen-72B-T", "@Qwen2-72B-Instruct-T", "@Qwen2.5-VL-72B-T", "@Qwen-2.5-72B-T"],
                "32B": [
                    "@Qwen3-30B-A3B-Instruct", "@Qwen2.5-Coder-32B", "@Qwen2.5-Coder-32B-T",
                    "@Qwen3-32B-CS", "@Qwen3-Coder-30B-A3B"
                ],
                "Others": ["@Qwen-2.5-7B-T", "@Qwen-2.5-VL-32b", "@Qwen3-Coder"]
            },
            "DeepSeek": {
                "R1 Series": [
                    "@DeepSeek-R1", "@DeepSeek-R1-FW", "@DeepSeek-R1-DI", "@DeepSeek-R1-N",
                    "@DeepSeek-R1-Distill", "@DeepSeek-R1-Turbo-DI"
                ],
                "V3 Series": [
                    "@DeepSeek-V3.1", "@DeepSeek-V3.1-Chat", "@DeepSeek-V3.1-N",
                    "@Deepseek-V3-FW", "@DeepSeek-V3", "@DeepSeek-V3-DI", "@DeepSeek-V3-Turbo-DI"
                ],
                "Specialized": ["@DeepSeek-Prover-V2", "@DeepClaude"]
            },
            "Mistral": {
                "Large": ["@Mistral-Large-2"],
                "Medium": ["@Mistral-Medium-3", "@Mistral-Medium", "@Magistral-Medium-2506-Thinking"],
                "Small": [
                    "@Mistral-Small-3.2", "@Mistral-Small-3.1", "@Mistral-Small-3",
                    "@Mistral-7B-v0.3-DI", "@Mistral-7B-v0.3-T"
                ],
                "Specialized": ["@Mistral-NeMo", "@Mixtral8x22b-Inst-FW"]
            },
            "Perplexity": [
                "@Perplexity-R1-1776", "@Perplexity-Sonar", "@Perplexity-Sonar-Pro",
                "@Perplexity-Sonar-Rsn", "@Perplexity-Sonar-Rsn-Pro"
            ],
            "Others": [
                "@Aya-Expanse-32B", "@Aya-Vision", "@Command-R", "@Command-R-Plus",
                "@GLM-4.5", "@GLM-4.5-Air", "@GLM-4.5-Air-T", "@GLM-4.5-FW", "@GLM-4.5-Versatile",
                "@GPT-Researcher", "@Inception-Mercury", "@Inception-Mercury-Coder",
                "@Hermes-3-70B", "@Kimi-K2", "@Kimi-K2-0905-T", "@Kimi-K2-Instruct", "@Kimi-K2-T",
                "@MiniMax-M1", "@Phi-4-DI", "@QwQ-32B-B10", "@QwQ-32B-Preview-T", "@QwQ-32B-T",
                "@Reka-Core", "@Reka-Flash", "@Reka-Research", "@Tako", "@Solar-Pro-2"
            ]
        };

        // Model Flags Database
        const MODEL_FLAGS = {
            "@Claude-Opus-4": { thinking_budget: { type: "slider", min: 0, max: 30768, default: "default" }},
            "@Claude-Opus-4-Reasoning": { thinking_budget: { type: "slider", min: 0, max: 30768, default: "default" }},
            "@Claude-Opus-4-Search": { thinking_budget: { type: "slider", min: 0, max: 126000, default: "default" }},
            "@Claude-Opus-4.1": { thinking_budget: { type: "slider", min: 0, max: 31999, default: "default" }},
            "@Claude-Sonnet-3.7": { thinking_budget: { type: "slider", min: 0, max: 16384, default: "default" }},
            "@Claude-Sonnet-3.7-Reasoning": { thinking_budget: { type: "slider", min: 0, max: 126000, default: "default" }},
            "@Claude-Sonnet-3.7-Search": { thinking_budget: { type: "slider", min: 0, max: 126000, default: "default" }},
            "@Claude-Sonnet-4": { thinking_budget: { type: "slider", min: 0, max: 30768, default: "default" }},
            "@Claude-Sonnet-4-Reasoning": { thinking_budget: { type: "slider", min: 0, max: 61440, default: "default" }},
            "@Claude-Sonnet-4-Search": { thinking_budget: { type: "slider", min: 0, max: 126000, default: "default" }},
            "@Gemini-2.5-Flash": { 
                thinking_budget: { type: "slider_stepped", steps: [0, 4096, 8192, 12288, 16384, 20480, 24576], default: "default" }
            },
            "@Gemini-2.5-Flash-Lite": { 
                thinking_budget: { type: "slider_stepped", steps: [0, 4096, 8192, 12288, 16384, 20480, 24576], default: "default" }
            },
            "@Gemini-2.5-Pro": { 
                thinking_budget: { type: "slider_stepped", steps: [0, 4096, 8192, 12288, 16384, 20480, 24576, 28672, 32768], default: "default" }
            },
            "@GPT-5": { reasoning_effort: { type: "slider_stepped", steps: ["minimal", "low", "medium", "high"], default: "default" }},
            "@GPT-5-mini": { reasoning_effort: { type: "slider_stepped", steps: ["minimal", "low", "medium", "high"], default: "default" }},
            "@GPT-5-nano": { reasoning_effort: { type: "slider_stepped", steps: ["minimal", "low", "medium", "high"], default: "default" }},
            "@o1": { reasoning_effort: { type: "slider_stepped", steps: ["low", "medium", "high"], default: "default" }},
            "@o3": { reasoning_effort: { type: "slider_stepped", steps: ["low", "medium", "high"], default: "default" }},
            "@o3-mini": { reasoning_effort: { type: "slider_stepped", steps: ["low", "medium", "high"], default: "default" }},
            "@o3-pro": { reasoning_effort: { type: "slider_stepped", steps: ["low", "medium", "high"], default: "default" }},
            "@o4-mini": { reasoning_effort: { type: "slider_stepped", steps: ["low", "medium", "high"], default: "default" }},
            "@Grok-3-Mini": { reasoning_effort: { type: "slider_stepped", steps: ["low", "high"], default: "default" }},
            "@Tako": { specificity: { type: "slider", min: 0, max: 100, default: "default" }},
```

## AccordionManager Class
```js
        class AccordionManager {
            constructor(options = {}) {
                this.options = {
                    searchDebounceMs: 150,
                    animationDuration: 300,
                    ...options
                };
                
                this.accordions = new Map();
                this.expandedSections = new Map();
                this.searchDebounceTimers = new Map();
            }

            createAccordion(containerId, data, config = {}) {
                const accordion = {
                    id: containerId,
                    data: data,
                    filteredData: data,
                    isExpanded: false,
                    selectedItem: null,
                    searchTerm: '',
                    callbacks: {
                        onSelect: config.onSelect || (() => {}),
                        onSearch: config.onSearch || (() => {}),
                        onExpand: config.onExpand || (() => {}),
                        onCollapse: config.onCollapse || (() => {})
                    }
                };

                this.accordions.set(containerId, accordion);
                this.initializeAccordionDOM(containerId);
                return accordion;
            }

            initializeAccordionDOM(accordionId) {
                const container = document.getElementById(accordionId);
                if (!container) return;

                // Build the accordion structure
                container.innerHTML = `
                    <div class="accordion-header" onclick="accordionManager.toggleAccordion('${accordionId}')">
                        <div class="accordion-display">
                            <span class="accordion-model-text">Select Model</span>
                        </div>
                        <div class="accordion-search-wrapper">
                            <span class="accordion-search-icon">🔍</span>
                            <input class="accordion-search-input" 
                                   type="text"
                                   placeholder="Search models..." 
                                   onclick="event.stopPropagation()"
                                   oninput="accordionManager.handleSearch('${accordionId}', this.value)" />
                        </div>
                        <span class="accordion-chevron">▼</span>
                    </div>
                    <div class="accordion-content-wrapper">
                        <div class="accordion-content"></div>
                    </div>
                `;

                // Set initial selected model if provided
                const accordion = this.accordions.get(accordionId);
                if (accordion && accordion.selectedItem) {
                    this.updateSelectedDisplay(accordionId);
                }
            }

            toggleAccordion(accordionId, forceState = null) {
                const accordion = this.accordions.get(accordionId);
                if (!accordion) return;

                const container = document.getElementById(accordionId);
                if (!container) return;

                const wasExpanded = accordion.isExpanded;
                accordion.isExpanded = forceState !== null ? forceState : !accordion.isExpanded;

                // Close other accordions if opening this one
                if (accordion.isExpanded && !wasExpanded) {
                    this.accordions.forEach((other, otherId) => {
                        if (otherId !== accordionId && other.isExpanded) {
                            this.toggleAccordion(otherId, false);
                        }
                    });
                }

                // Update DOM state
                if (accordion.isExpanded) {
                    container.classList.add('expanded');
                    
                    // Focus search input
                    setTimeout(() => {
                        const searchInput = container.querySelector('.accordion-search-input');
                        if (searchInput) {
                            searchInput.focus();
                        }
                    }, 100);

                    // Render content if needed
                    const contentEl = container.querySelector('.accordion-content');
                    if (contentEl && !contentEl.innerHTML.trim()) {
                        this.renderAccordionContent(accordionId);
                    }

                    accordion.callbacks.onExpand(accordionId);
                } else {
                    container.classList.remove('expanded');
                    
                    // Clear search
                    const searchInput = container.querySelector('.accordion-search-input');
                    if (searchInput) {
                        searchInput.value = '';
                        accordion.searchTerm = '';
                        accordion.filteredData = accordion.data;
                    }

                    accordion.callbacks.onCollapse(accordionId);
                }
            }

            handleSearch(accordionId, searchTerm) {
                // Clear existing debounce timer
                if (this.searchDebounceTimers.has(accordionId)) {
                    clearTimeout(this.searchDebounceTimers.get(accordionId));
                }

                // Set new debounce timer
                const timer = setTimeout(() => {
                    this.setSearchTerm(accordionId, searchTerm);
                }, this.options.searchDebounceMs);

                this.searchDebounceTimers.set(accordionId, timer);
            }

            setSearchTerm(accordionId, searchTerm) {
                const accordion = this.accordions.get(accordionId);
                if (!accordion) return;

                accordion.searchTerm = searchTerm.toLowerCase();
                accordion.filteredData = this.filterAccordionData(accordion.data, accordion.searchTerm);
                
                this.renderAccordionContent(accordionId);
                accordion.callbacks.onSearch(searchTerm, accordion.filteredData);
            }

            renderAccordionContent(accordionId) {
                const accordion = this.accordions.get(accordionId);
                if (!accordion) return;

                const container = document.getElementById(accordionId);
                const contentEl = container?.querySelector('.accordion-content');
                if (!contentEl) return;

                let html = '';
                let hasContent = false;

                Object.entries(accordion.filteredData).forEach(([category, items]) => {
                    const categoryContent = this.renderCategory(category, items, accordionId);
                    if (categoryContent) {
                        html += categoryContent;
                        hasContent = true;
                    }
                });

                if (!hasContent) {
                    html = '<div class="accordion-empty">No models found</div>';
                }

                contentEl.innerHTML = html;

                // Auto-expand sections when searching
                if (accordion.searchTerm) {
                    this.autoExpandSearchResults(accordionId);
                }
            }

            renderCategory(category, items, accordionId) {
                const accordion = this.accordions.get(accordionId);
                const sectionKey = `${accordionId}-${category}`;
                const isExpanded = this.expandedSections.get(sectionKey) || accordion.searchTerm;

                // Get filtered items
                const filteredItems = this.getFilteredItems(items, accordion.searchTerm);
                if (filteredItems.length === 0 && accordion.searchTerm) return '';

                let html = `
                    <div class="accordion-section ${isExpanded ? 'expanded' : ''}" data-category="${category}">
                        <div class="accordion-section-header" onclick="accordionManager.toggleSection('${accordionId}', '${category}')">
                            <div class="accordion-section-info">
                                <span>${category}</span>
                                <span class="accordion-section-count">(${filteredItems.length})</span>
                            </div>
                            <span class="accordion-section-chevron">▶</span>
                        </div>
                        <div class="accordion-section-content">
                `;

                if (Array.isArray(items)) {
                    // Simple array
                    filteredItems.forEach(item => {
                        html += this.renderItem(item, accordionId);
                    });
                } else {
                    // Nested structure
                    Object.entries(items).forEach(([subcategory, subitems]) => {
                        const filteredSubitems = this.filterItems(subitems, accordion.searchTerm);
                        if (filteredSubitems.length > 0) {
                            html += `
                                <div class="accordion-subsection">
                                    <div class="accordion-subsection-header">${subcategory}</div>
                            `;
                            filteredSubitems.forEach(item => {
                                html += this.renderItem(item, accordionId);
                            });
                            html += '</div>';
                        }
                    });
                }

                html += '</div></div>';
                return html;
            }

            renderItem(item, accordionId) {
                const accordion = this.accordions.get(accordionId);
                const isSelected = accordion.selectedItem === item;
                const displayName = item.startsWith('@') ? item.slice(1) : item;

                return `
                    <div class="accordion-item ${isSelected ? 'selected' : ''}"
                         data-item="${item}"
                         onclick="accordionManager.selectItem('${accordionId}', '${item.replace(/'/g, "\\'")}')"
                         title="${displayName}">
                        ${displayName}
                    </div>
                `;
            }

            getFilteredItems(items, searchTerm) {
                if (Array.isArray(items)) {
                    return this.filterItems(items, searchTerm);
                } else {
                    const result = [];
                    Object.values(items).forEach(subitems => {
                        if (Array.isArray(subitems)) {
                            result.push(...this.filterItems(subitems, searchTerm));
                        }
                    });
                    return result;
                }
            }

            filterItems(items, searchTerm) {
                if (!searchTerm || !Array.isArray(items)) return items;
                return items.filter(item => 
                    item.toLowerCase().includes(searchTerm)
                );
            }

            filterAccordionData(data, searchTerm) {
                if (!searchTerm) return data;

                const filtered = {};
                
                Object.entries(data).forEach(([category, items]) => {
                    if (Array.isArray(items)) {
                        const filteredItems = this.filterItems(items, searchTerm);
                        if (filteredItems.length > 0) {
                            filtered[category] = filteredItems;
                        }
                    } else {
                        const filteredSubcategories = {};
                        Object.entries(items).forEach(([subcat, subitems]) => {
                            const filteredSub = this.filterItems(subitems, searchTerm);
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

            toggleSection(accordionId, category) {
                const sectionKey = `${accordionId}-${category}`;
                const isExpanded = this.expandedSections.get(sectionKey);
                this.expandedSections.set(sectionKey, !isExpanded);
                
                const container = document.getElementById(accordionId);
                const section = container?.querySelector(`[data-category="${category}"]`);
                if (section) {
                    section.classList.toggle('expanded', !isExpanded);
                }
            }

            autoExpandSearchResults(accordionId) {
                const container = document.getElementById(accordionId);
                container?.querySelectorAll('.accordion-section').forEach(section => {
                    section.classList.add('expanded');
                    const category = section.dataset.category;
                    if (category) {
                        this.expandedSections.set(`${accordionId}-${category}`, true);
                    }
                });
            }

            selectItem(accordionId, item) {
                const accordion = this.accordions.get(accordionId);
                if (!accordion) return;

                accordion.selectedItem = item;
                this.updateSelectedDisplay(accordionId);
                this.toggleAccordion(accordionId, false);
                
                accordion.callbacks.onSelect(item, accordionId);
            }

            updateSelectedDisplay(accordionId) {
                const accordion = this.accordions.get(accordionId);
                const container = document.getElementById(accordionId);
                if (!accordion || !container) return;

                const displayEl = container.querySelector('.accordion-model-text');
                if (displayEl && accordion.selectedItem) {
                    const displayName = accordion.selectedItem.startsWith('@') ? 
                        accordion.selectedItem.slice(1) : accordion.selectedItem;
                    displayEl.textContent = displayName;
                }
            }

            getSelection(accordionId) {
```

## How it works
- **Dual-mode header** flips between a compact "Select Model" display and a search input once expanded, keeping the collapsed state tiny while exposing full search when needed.
- **Provider → Series → Model hierarchy** renders categories and subcategories on demand, preserving expansion state and auto-expanding when a search term is active.
- **Debounced search** filters against the `MODEL_DATABASE`, updating counts inline and showing "No models found" when nothing matches.
- **Single-open accordion** collapses other pickers when a new one opens, while `selectItem` writes the handle back into callbacks for downstream logic (model assignment, flag toggles, etc.).
- **Utility helpers** (`getSelection`, `setSelection`, `clearSelection`, `destroy`) support state persistence and cleanup when users import/export configurations or hide bot panels.
