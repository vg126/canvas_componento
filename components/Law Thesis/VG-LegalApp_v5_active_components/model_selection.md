# Accordion Model Selector

## Model Catalogue Data
```js
        const multimodalModels = {
            "Favorites": [
                "@GPT-5",
                "@GPT-4.1",
                "@o3-pro",
                "@o1",
                "@Gemini-2.5-Pro",
                "@Claude-Opus-4-Reasoning",
                "@Claude-Opus-4.1",
                "@Claude-Opus-4-Search",
                "@Claude-Sonnet-4-Search",
                "@Grok-4",
                "@Mistral-Large-2"
            ],
            "Web Search": [
                "@Claude-Opus-4-Search",
                "@Claude-Sonnet-4-Search",
                "@Gemini-2.5-Flash",
                "@Gemini-2.5-Pro",
                "@Grok-4",
                "@Perplexity-Sonar",
                "@Perplexity-Sonar-Rsn-Pro",
                "@GPT-4o-Search",
                "@Linkup-Deep-Search"   
            ],
            "GPT": {
                "GPT-5 Series": [
                    "@GPT-5-Chat",
                    "@GPT-5",
                    "@GPT-5-mini",
                    "@GPT-5-nano"
                ],
                "GPT-4 Series": [
                    "@GPT-4.1",
                    "@GPT-4o-Search",
                    "@GPT-4-Classic",
                    "@GPT-4-Classic-0314",
                    "@GPT-4-Turbo",
                    "@GPT-4.1-mini",
                    "@GPT-4.1-nano",
                    "@GPT-4o",
                    "@GPT-4o-mini",
                    "@GPT-4o-mini-Search",
                    "@GPT-4o-Aug"
                ],
                "GPT-3.5 Series": [
                    "@GPT-3.5-Turbo",
                    "@GPT-3.5-Turbo-Instruct",
                    "@GPT-3.5-Turbo-Raw"
                ],
                "o-Series (Reasoning)": [
                    "@o1",
                    "@o3",
                    "@o3-pro",
                    "@o1-mini",
                    "@o3-mini",
                    "@o3-mini-high",
                    "@o4-mini",
                    "@o3-Pro"
                ]
            },
            "GPT - Open Weight": {
                "120B Parameter Models": [
                    "@GPT-OSS-120B-T",
                    "@GPT-OSS-120B",
                    "@GPT-OSS-120B-CS",
                    "@OpenAI-GPT-OSS-120B"
                ],
                "20B Parameter Models": [
                    "@GPT-OSS-20B-T",
                    "@GPT-OSS-20B",
                    "@OpenAI-GPT-OSS-20B"
                ]
            },
            "Google": {
                "Gemini 2.5 Series": [
                    "@Gemini-2.5-Pro",
                    "@Gemini-2.5-Flash",
                    "@Gemini-2.5-Flash-Lite",
                    "@Gemini-2.5-Flash-Image"
                ],
                "Gemini 2.0 Series": [
                    "@Gemini-2.0-Flash",
                    "@Gemini-2.0-Flash-Lite",
                    "@Gemini-2.0-Flash-Preview"
                ],
                "Gemini 1.5 Series": [
                    "@Gemini-1.5-Pro",
                    "@Gemini-1.5-Pro-Search",
                    "@Gemini-1.5-Flash",
                    "@Gemini-1.5-Flash-Search"
                ],
                "Gemma Series": [
                    "@Gemma-3-27B",
                    "@Gemma-2-27b-T"
                ]
            },
            "Claude": {
                "Opus Series": [
                    "@Claude-Opus-4.1",
                    "@Claude-Opus-4",
                    "@Claude-Opus-4-Reasoning",
                    "@Claude-Opus-4-Search",
                    "@Claude-Opus-3"
                ],
                "Sonnet Series": [
                    "@Claude-Sonnet-4",
                    "@Claude-Sonnet-4-Reasoning",
                    "@Claude-Sonnet-4-Search",
                    "@Claude-Sonnet-3.5",
                    "@Claude-Sonnet-3.5-June",
                    "@Claude-Sonnet-3.5-Search",
                    "@Claude-Sonnet-3.7",
                    "@Claude-Sonnet-3.7-Reasoning",
                    "@Claude-Sonnet-3.7-Search"
                ],
                "Haiku Series": [
                    "@Claude-Haiku-3.5",
                    "@Claude-Haiku-3",
                    "@Claude-Haiku-3.5-Search"
                ]
            },
            "Grok": [
                "@Grok-4",
                "@Grok-3",
                "@Grok-3-Mini",
                "@Grok-Code-Fast-1",
                "@Grok-2"
            ],
            "Llama 4": [
                "@Llama-4-Scout-B10",
                "@Llama-4-Maverick",
                "@Llama-4-Scout-T",
                "@Llama-4-Scout-CS",
                "@Llama-4-Scout",
                "@Llama-4-Maverick-T",
                "@Llama-4-Maverick-B10"
            ],
            "Llama 3.X": {
                "The Behemoths (405B)": [
                    "@Llama-3.1-405B",
                    "@Llama-3.1-405B-T",
                    "@Llama-3.1-405B-FW",
                    "@Llama-3.1-405B-FP16"
                ],
                "The Curated 70B Fleet": [
                    "@Llama-3-70b-Groq",
                    "@Llama-3.3-70B",
                    "@Llama-3.1-Nemotron",
                    "@Llama-3.3-70B-DI",
                    "@Llama-3.3-70B-CS",
                    "@Llama-3.3-70B-Vers",
                    "@Llama-3-70B-FP16",
                    "@Llama-3-70B-T",
                    "@Llama-3.1-70B",
                    "@Llama-3.1-70B-FP16",
                    "@Llama-3.1-70B-FW",
                    "@Llama-3.1-70B-T",
                    "@Llama-3.3-70B-FW",
                    "@Llama-3.3-70B-N"
                ],
                "The 8B Fleet": [
                    "@Llama-3-8B-T",
                    "@Llama-3-8b-Groq",
                    "@Llama-3.1-8B",
                    "@Llama-3.1-8B-CS",
                    "@Llama-3.1-8B-DI",
                    "@Llama-3.1-8B-FP16",
                    "@Llama-3.1-8B-FW",
                    "@Llama-3.1-8B-T-128k"
                ]
            },
            "Qwen (235B+)": {
                "480B": [
                    "@Qwen3-480B-Coder-CS",
                    "@Qwen3-Coder-480B-T",
                    "@Qwen3-Coder-480B-N"
                ],
                "235B": [
                    "@Qwen-3-235B-2507-T",
                    "@Qwen3-235B-2507-FW",
                    "@Qwen3-235B-2507-CS",
                    "@Qwen3-235B-A22B",
                    "@Qwen3-235B-A22B-DI",
                    "@Qwen3-235B-A22B-N",
                    "@Qwen3-235B-Think-CS"
                ],
                "72B": [
                    "@Qwen-72B-T",
                    "@Qwen2-72B-Instruct-T",
                    "@Qwen2.5-VL-72B-T",
                    "@Qwen-2.5-72B-T"
                ],
                "30–32B": [
                    "@Qwen3-30B-A3B-Instruct",
                    "@Qwen2.5-Coder-32B",
                    "@Qwen2.5-Coder-32B-T",
                    "@Qwen3-32B-CS",
                    "@Qwen3-Coder-30B-A3B"
                ],
                "≤32B & VL": [
                    "@Qwen-2.5-7B-T",
                    "@Qwen-2.5-VL-32b"
                ],
                "General": [
                    "@Qwen3-Coder"
                ]
            },
            "DeepSeek": {
                "R1 Series (Reasoning)": [
                    "@DeepSeek-R1",
                    "@DeepSeek-R1-FW",
                    "@DeepSeek-R1-DI",
                    "@DeepSeek-R1-N",
                    "@DeepSeek-R1-Distill",
                    "@DeepSeek-R1-Turbo-DI"
                ],
                "V3 Series (Foundation)": [
                    "@DeepSeek-V3.1",
                    "@DeepSeek-V3.1-N",
                    "@Deepseek-V3-FW",
                    "@DeepSeek-V3",
                    "@DeepSeek-V3-DI",
                    "@DeepSeek-V3-Turbo-DI"
                ],
                "Specialized & Hybrids": [
                    "@DeepSeek-Prover-V2",
                    "@DeepClaude"
                ]
            },
            "Mistral": {
                "Large Series": [
                    "@Mistral-Large-2"
                ],
                "Medium Series": [
                    "@Mistral-Medium-3",
                    "@Mistral-Medium",
                    "@Magistral-Medium-2506-Thinking"
                ],
                "Small Series (Vision-Enabled)": [
                    "@Mistral-Small-3.2",
                    "@Mistral-Small-3.1",
                    "@Mistral-Small-3",
                    "@Mistral-7B-v0.3-DI",
                    "@Mistral-7B-v0.3-T"
                ],
                "Specialized & MoE Models": [
                    "@Mistral-NeMo",
                    "@Mixtral8x22b-Inst-FW"
                ]
            },
            "Perplexity": [
                "@Perplexity-R1-1776",
                "@Perplexity-Sonar",
                "@Perplexity-Sonar-Pro",
                "@Perplexity-Sonar-Rsn",
                "@Perplexity-Sonar-Rsn-Pro"
            ],
            "Wildcards (A-K)": [
                "@Aya-Expanse-32B",
                "@Aya-Vision",
                "@Command-R",
                "@Command-R-Plus",
                "@GLM-4.5",
                "@GLM-4.5-Air",
                "@GLM-4.5-Air-T",
                "@GLM-4.5-FW",
                "@Inception-Mercury",
                "@Inception-Mercury-Coder",
                "@Bagoodex-Web-Search",
                "@Hermes-3-70B",
                "@Kimi-K2",
                "@Kimi-K2-Instruct",
                "@Kimi-K2-T"
            ],
            "Wildcards (L-Z)": [
                "@Linkup-Standard",
                "@MiniMax-M1",
                "@Phi-4-DI",
                "@QwQ-32B-B10",
                "@QwQ-32B-Preview-T",
                "@QwQ-32B-T",
                "@Reka-Core",
                "@Reka-Flash",
                "@Reka-Research",
                "@Tako",
                "@Solar-Pro-2"
            ]
        };

        // State for model selections
        let selectedBotModels = ['', '', '', '', '', ''];

        // ===== ACCORDION MODEL SELECTOR CLASS =====
        class AccordionModelSelector {
            constructor(botId) {
                this.botId = botId;
                this.selectedModel = '';
                this.container = document.getElementById(`accordion-root-${botId}`);
                this.selectorContainer = document.getElementById(`selector-container-${botId}`);
                this.searchInput = document.getElementById(`model-search-${botId}`);
                this.clearBtn = document.getElementById(`clear-btn-${botId}`);
                this.isCollapsed = true;
                this.searchTerm = '';
                this.currentData = multimodalModels;
                this.highlightedIndex = -1;
                this.init();
            }

            init() {
                this.render();
                this.attachEventListeners();
                this.selectorContainer.classList.add('collapsed');
                this.bindSearchInput();
            }

            bindSearchInput() {
```

## AccordionModelSelector Class
```js
                const input = this.searchInput;
                if (!input) return;
                const stop = (e) => { e.stopPropagation(); e.stopImmediatePropagation(); };
                input.addEventListener('click', stop);
                input.addEventListener('mousedown', stop);
                input.addEventListener('pointerdown', stop);
                input.addEventListener('touchstart', (e) => { stop(e); input.focus(); }, { passive: false });

                input.addEventListener('input', (e) => {
                    const currentValue = (e.target.value || '').trim();
                    this.searchTerm = currentValue;
                    
                    // If user is typing something different from selected model, auto-clear selection
                    if (this.selectedModel && currentValue !== this.selectedModel && currentValue !== '') {
                        this.autoClearSelection();
                    }
                    
                    this.applySearch();
                    // Auto-expand to show matches when typing
                    if (this.isCollapsed && this.searchTerm) this.expand();
                    // Reset keyboard navigation when search changes
                    this.highlightedIndex = -1;
                    this.updateHighlight();
                });
                
                input.addEventListener('keydown', (e) => {
                    if (e.key === 'Escape') {
                        e.preventDefault();
                        input.value = '';
                        this.searchTerm = '';
                        this.applySearch();
                        this.highlightedIndex = -1;
                        this.updateHighlight();
                    } else if (e.key === 'ArrowDown') {
                        e.preventDefault();
                        if (this.isCollapsed) this.expand();
                        this.navigateDown();
                    } else if (e.key === 'ArrowUp') {
                        e.preventDefault();
                        if (this.isCollapsed) this.expand();
                        this.navigateUp();
                    } else if (e.key === 'Enter') {
                        e.preventDefault();
                        if (this.highlightedIndex >= 0) {
                            this.selectHighlightedModel();
                        }
                    }
                });
                
                // Add focus behavior to make it clear the input is editable
                input.addEventListener('focus', (e) => {
                    if (this.selectedModel) {
                        input.select(); // Select all text to make editing easier
                    }
                    if (this.isCollapsed) this.expand();
                });
            }

            sanitizeId(str) {
                return str.replace(/[^a-zA-Z0-9-]/g, '-').toLowerCase();
            }

            render(data = this.currentData) {
                this.currentData = data;
                let html = '';
                
                Object.entries(data).forEach(([provider, pdata]) => {
                    const providerId = this.sanitizeId(provider);
                    const modelCount = this.countModels(pdata);
                    
                    html += `
                        <div class="accordion-item">
                            <div class="accordion-header" data-provider="${providerId}">
                                <span class="accordion-title">${provider}</span>
                                <span style="display: flex; align-items: center; gap: 6px;">
                                    <span class="model-count">${modelCount}</span>
                                    <svg class="accordion-icon" fill="currentColor" viewBox="0 0 20 20">
                                        <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                                    </svg>
                                </span>
                            </div>
                            <div class="accordion-content" id="content-${providerId}-${this.botId}">
                                ${this.renderSeries(pdata, providerId)}
                            </div>
                        </div>
                    `;
                });
                
                this.container.innerHTML = html;

                // Auto-expand when searching so results are visible
                if (this.searchTerm) {
                    this.container.querySelectorAll('.accordion-header').forEach(h => h.classList.add('active'));
                    this.container.querySelectorAll('.accordion-content').forEach(c => c.classList.add('active'));
                    this.container.querySelectorAll('.series-header').forEach(h => h.classList.add('active'));
                    this.container.querySelectorAll('.series-content').forEach(c => c.classList.add('active'));
                }

                // Re-apply selected highlight and reflect value
                if (this.selectedModel) {
                    const sel = this.container.querySelector(`.model-item[data-model="${CSS.escape(this.selectedModel)}"]`);
                    if (sel) sel.classList.add('selected');
                    if (this.searchInput) this.searchInput.value = this.selectedModel;
                } else {
                    if (this.searchInput && !this.searchTerm) {
                        this.searchInput.value = '';
                        this.searchInput.placeholder = 'Search or select model...';
                    }
                }
            }

            renderSeries(data, providerId) {
                let html = '';
                
                if (Array.isArray(data)) {
                    const list = this.sortModels(data);
                    list.forEach(model => {
                        const modelId = this.sanitizeId(model);
                        html += `
                            <div class="model-item" data-model="${model}" data-model-id="${modelId}">
                                ${model}
                            </div>
                        `;
                    });
                } else {
                    Object.entries(data).forEach(([series, models]) => {
                        const seriesId = this.sanitizeId(series);
                        
                        if (models.length === 0) {
                            html += `
                                <div class="series-item">
                                    <div class="series-header" style="color: var(--text-secondary); font-style: italic;">
                                        <span>${series} (empty)</span>
                                    </div>
                                </div>
                            `;
                        } else {
                            const list = this.sortModels(models);
                            html += `
                                <div class="series-item">
                                    <div class="series-header" data-series="${seriesId}">
                                        <span>${series}</span>
                                        <span style="display: flex; align-items: center; gap: 6px;">
                                            <span class="model-count">${list.length}</span>
                                            <svg class="accordion-icon" style="width: 14px; height: 14px;" fill="currentColor" viewBox="0 0 20 20">
                                                <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
                                            </svg>
                                        </span>
                                    </div>
                                    <div class="series-content" id="series-${seriesId}-${this.botId}">
                                        ${list.map(model => {
                                            const modelId = this.sanitizeId(model);
                                            return `
                                                <div class="model-item" data-model="${model}" data-model-id="${modelId}">
                                                    ${model}
                                                </div>
                                            `;
                                        }).join('')}
                                    </div>
                                </div>
                            `;
                        }
                    });
                }
                
                return html;
            }

            normalizeName(name) {
                return (name || '').replace(/^@/, '').toLowerCase();
            }

            sortModels(models) {
                let list = Array.from(models);
                if (!this.searchTerm) {
                    return list.sort((a, b) => this.normalizeName(a).localeCompare(this.normalizeName(b)));
                }
                const term = this.searchTerm.toLowerCase();
                const starts = [];
                const contains = [];
                list.forEach(m => {
                    const n = this.normalizeName(m);
                    if (n.startsWith(term)) starts.push(m);
                    else if (n.includes(term)) contains.push(m);
                });
                starts.sort((a, b) => this.normalizeName(a).localeCompare(this.normalizeName(b)));
                contains.sort((a, b) => this.normalizeName(a).localeCompare(this.normalizeName(b)));
                return [...starts, ...contains];
            }

            getFilteredData() {
                const term = this.searchTerm.toLowerCase();
                if (!term) return multimodalModels;
                const out = {};
                Object.entries(multimodalModels).forEach(([provider, pdata]) => {
                    if (Array.isArray(pdata)) {
                        const filtered = pdata.filter(m => this.normalizeName(m).includes(term));
                        if (filtered.length) out[provider] = filtered;
                    } else {
                        const seriesOut = {};
                        Object.entries(pdata).forEach(([series, models]) => {
                            const filtered = models.filter(m => this.normalizeName(m).includes(term));
                            if (filtered.length) seriesOut[series] = filtered;
                        });
                        if (Object.keys(seriesOut).length) out[provider] = seriesOut;
                    }
                });
                return out;
            }

            applySearch() {
                const data = this.getFilteredData();
                this.render(data);
            }

            countModels(data) {
                if (Array.isArray(data)) {
                    return data.length;
                }
                
                let count = 0;
                Object.values(data).forEach(models => {
                    if (Array.isArray(models)) {
                        count += models.length;
                    } else if (typeof models === 'object' && models !== null) {
                        // Handle nested structure like Qwen series
                        Object.values(models).forEach(nestedModels => {
                            if (Array.isArray(nestedModels)) {
                                count += nestedModels.length;
                            }
                        });
                    }
                });
                return count;
            }

            attachEventListeners() {
                this.container.addEventListener('click', (e) => {
                    e.stopPropagation();
                    
                    const header = e.target.closest('.accordion-header');
                    if (header) {
                        this.toggleAccordionSection(header);
                        return;
                    }
                    
                    const seriesHeader = e.target.closest('.series-header');
                    if (seriesHeader && seriesHeader.dataset.series) {
                        this.toggleSeries(seriesHeader);
                        return;
                    }
                    
                    const modelItem = e.target.closest('.model-item');
                    if (modelItem) {
                        this.selectModel(modelItem);
                        return;
                    }
                });
            }

            toggleAccordionSection(header) {
                const providerId = header.dataset.provider;
                const content = document.getElementById(`content-${providerId}-${this.botId}`);
                const isActive = header.classList.contains('active');
                
                this.container.querySelectorAll('.accordion-header').forEach(h => {
                    h.classList.remove('active');
                });
                this.container.querySelectorAll('.accordion-content').forEach(c => {
                    c.classList.remove('active');
                });
                
                if (!isActive) {
                    header.classList.add('active');
                    content.classList.add('active');
                }
            }

            toggleSeries(header) {
                const seriesId = header.dataset.series;
                const content = document.getElementById(`series-${seriesId}-${this.botId}`);
                const isActive = header.classList.contains('active');
                
                const provider = header.closest('.accordion-content');
                provider.querySelectorAll('.series-header').forEach(h => {
                    h.classList.remove('active');
                });
                provider.querySelectorAll('.series-content').forEach(c => {
                    c.classList.remove('active');
                });
                
                if (!isActive) {
                    header.classList.add('active');
                    content.classList.add('active');
                }
            }
```

## How it works
- **Curated catalogue** groups more than a dozen provider families (OpenAI GPT, Claude, Gemini, Qwen, DeepSeek, Mistral, Perplexity, etc.) so bot owners can align each workflow step with the right capability tier.
- **Single-selection accordion** keeps the UI compact: providers expand to series, series expand to model rows, and the currently chosen model is mirrored into the search box.
- **Search & keyboard navigation** let power users type to filter, arrow through visible rows, press Enter to commit, or Escape to reset the filter without leaving the control.
- **State synchronisation** writes the selected handle into the shared `selectedBotModels` array, ensuring both the Input and Results tabs show the same model choice.
- **Quality-of-life affordances** include auto-clear when a new search diverges from the stored model, highlight management, scroll helpers, and a clear button that only appears after a selection is made.
