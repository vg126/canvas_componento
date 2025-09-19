# Flag Manager

## Model Flag Definitions
```js
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
            "@Linkup-Deep-Search": {
                advanced_settings: {
                    type: "advanced",
                    fields: {
                        domain_filter_mode: { type: "select", options: ["none", "Include", "Exclude"], default: "none" },
                        include_domains: { type: "text", placeholder: "e.g. github.com", depends_on: "domain_filter_mode", depends_value: "Include" },
                        exclude_domains: { type: "text", placeholder: "e.g. reddit.com", depends_on: "domain_filter_mode", depends_value: "Exclude" },
                        prioritize_domains: { type: "text", placeholder: "e.g. stackoverflow.com" },
                        from_date: { type: "text", placeholder: "YYYY-MM-DD" },
                        to_date: { type: "text", placeholder: "YYYY-MM-DD" },
                        include_images: { type: "checkbox", default: false },
                        image_count: { type: "text", placeholder: "Number (e.g. 5)" }
                    }
                }
            },
            "@Linkup-Standard": {
                thinking_budget: { type: "slider", min: 0, max: 32768, default: "default" },
                advanced_settings: {
                    type: "advanced",
                    fields: {
                        domain_filter_mode: { type: "select", options: ["none", "Include", "Exclude"], default: "none" },
                        include_domains: { type: "text", placeholder: "e.g. github.com", depends_on: "domain_filter_mode", depends_value: "Include" },
                        exclude_domains: { type: "text", placeholder: "e.g. reddit.com", depends_on: "domain_filter_mode", depends_value: "Exclude" },
                        prioritize_domains: { type: "text", placeholder: "e.g. stackoverflow.com" },
                        from_date: { type: "text", placeholder: "YYYY-MM-DD" },
                        to_date: { type: "text", placeholder: "YYYY-MM-DD" },
                        include_images: { type: "checkbox", default: false },
                        image_count: { type: "text", placeholder: "Number (e.g. 5)" }
                    }
                }
            },
            "@Bagoodex-Web-Search": {
                advanced_settings: {
                    type: "advanced",
                    fields: {
                        domain_filter: { type: "text", placeholder: "e.g. legal-tools.org" },
                        exclude_words: { type: "text", placeholder: "e.g. bemba" },
                        search_images: { type: "checkbox", default: false },
                        search_knowledge: { type: "checkbox", default: false },
                        search_location: { type: "checkbox", default: false },
                        search_videos: { type: "checkbox", default: false },
                        search_weather: { type: "checkbox", default: false }
                    }
                }
            }
        };

        /* ============================================
           IMPROVED ACCORDION MANAGER CLASS
           ============================================ */

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
```

## FlagManager Class
```js
        class FlagManager {
            constructor() {
                this.modelFlags = {};
            }

            // Get flags for a specific model
            getModelFlags(modelName) {
                return MODEL_FLAGS[modelName] || {};
            }

            // Check if model has flags
            hasFlags(modelName) {
                return !!MODEL_FLAGS[modelName];
            }

            // Set flag value for a model instance
            setFlag(modelName, flagName, value) {
                if (!this.modelFlags[modelName]) {
                    this.modelFlags[modelName] = {};
                }
                this.modelFlags[modelName][flagName] = value;
            }

            // Get flag value for a model instance
            getFlag(modelName, flagName) {
                return this.modelFlags[modelName]?.[flagName] || 'default';
            }

            // Generate flag string for API call
            generateFlagString(modelName) {
                const flags = this.modelFlags[modelName];
                if (!flags) return '';

                const flagParts = [];
                
                Object.entries(flags).forEach(([flagName, value]) => {
                    if (flagName === 'advanced_settings' && typeof value === 'object') {
                        // Handle advanced settings
                        Object.entries(value).forEach(([subFlag, subValue]) => {
                            if (subValue && subValue !== 'none' && subValue !== false) {
                                if (typeof subValue === 'boolean') {
                                    flagParts.push(`--${subFlag} true`);
                                } else {
                                    // Special handling for Linkup models
                                    const isLinkup = modelName.includes('Linkup');
                                    if (isLinkup) {
                                        flagParts.push(`--${subFlag} ${subValue}`);
                                    } else {
                                        flagParts.push(`--${subFlag} "${subValue}"`);
                                    }
                                }
                            }
                        });
                    } else if (value !== 'default') {
                        flagParts.push(`--${flagName} ${value}`);
                    }
                });

                return flagParts.length > 0 ? ' ' + flagParts.join(' ') : '';
            }

            // Reset flags for a model
            resetFlags(modelName) {
                delete this.modelFlags[modelName];
            }

            // Get all models with their current flag states
            getAllModelStates() {
                return { ...this.modelFlags };
            }

            // Set all model states (for import/export)
            setAllModelStates(states) {
                this.modelFlags = { ...states };
            }
        }

        // Initialize global managers
        const accordionManager = new AccordionManager();
```

## How it works
- **Model-specific toggles** declare slider, stepped, checkbox, and advanced forms so each provider exposes the tuning options Poe accepts (thinking budget, reasoning effort, domain filters, etc.).
- **Dynamic rendering** uses `updateFlagsVisibility` and `renderFlagControls` to reveal controls only when a selected model has entries in `MODEL_FLAGS`, keeping the UI lean by default.
- **State persistence** records flag selections per model inside `this.modelFlags`, enabling export/import through `getAllModelStates` and `setAllModelStates`.
- **Command string builder** (`generateFlagString`) converts the current selection into Poe-ready CLI flags, flattening advanced settings and quoting values where required.
- **Reset helpers** let operators clear individual models or whole sessions when switching engines, preventing stale tuning parameters from leaking into new runs.
