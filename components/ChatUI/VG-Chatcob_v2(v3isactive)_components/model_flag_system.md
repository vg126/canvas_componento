# Model Flag System

Flag metadata and modal controls that let users adjust model-specific generation parameters.

```javascript
const MODEL_FLAGS = {
    // Claude Models with corrected values
    "Claude-Opus-4": {
        "thinking_budget": {
            "type": "stepped",
            "steps": [0, 4096, 8192, 12288, 16384, 20480, 24576, 28672, 30768],
            "default": "default"
        }
    },
    "Claude-Opus-4-Reasoning": {
        "thinking_budget": {
            "type": "stepped",
            "steps": [0, 4096, 8192, 12288, 16384, 20480, 24576, 28672, 30768],
            "default": "default"
        }
    },
    "Claude-Opus-4-Search": {
        "thinking_budget": {
            "type": "stepped",
            "steps": [0, 4096, 8192, 12288, 16384, 20480, 24576, 28672, 32768],
            "default": "default"
        }
    },
    "Claude-Opus-4.1": {
        "thinking_budget": {
            "type": "stepped",
            "steps": [0, 4096, 8192, 12288, 16384, 20480, 24576, 28672, 31999],
            "default": "default"
        }
    },
    "Claude-Sonnet-3.7": {
        "thinking_budget": {
            "type": "stepped",
            "steps": [0, 4096, 8192, 12288, 16384],
            "default": "default"
        }
    }
    // Additional entries continue for other Claude, GPT, Grok, Tako, Linkup, etc.
};
```

```javascript
function openFlagModal() {
    const modal = document.getElementById('flagModal');
    const flagContent = document.getElementById('flagContent');
    const selectedModel = appState.selectedModel;

    // Check if model has flags
    const modelFlags = MODEL_FLAGS[selectedModel];

    if (!modelFlags) {
        flagContent.innerHTML = `
            <div class="text-center text-gray-500 dark:text-gray-400 py-8">
                <div class="text-4xl mb-2">🚫</div>
                <p>No flags available for ${selectedModel}</p>
            </div>
        `;
    } else {
        // Initialize model flags if not exists
        if (!appState.modelFlags[selectedModel]) {
            appState.modelFlags[selectedModel] = {};
        }

        // Render flag controls
        let html = `<div class="mb-4"><h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Available flags for ${selectedModel}:</h4></div>`;

        Object.entries(modelFlags).forEach(([flagName, config]) => {
            html += createSteppedFlag(selectedModel, flagName, config);
        });

        flagContent.innerHTML = html;

        // Add event listeners after rendering
        setupFlagEventListeners(selectedModel, modelFlags);
    }

    modal.classList.remove('hidden');
}

function closeFlagModal() {
    document.getElementById('flagModal').classList.add('hidden');
}
```

```javascript
function createSteppedFlag(model, flagName, config) {
    if (config.type === 'stepped') {
        const currentValue = appState.modelFlags[model][flagName] || config.default;
        const steps = ['default', ...config.steps];
        const currentIndex = steps.indexOf(currentValue);

        return `
            <div class="mb-4 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    ${flagName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </label>
                <div class="flex items-center gap-3">
                    <input
                        type="range"
                        id="flag-${flagName}"
                        min="0"
                        max="${steps.length - 1}"
                        value="${currentIndex >= 0 ? currentIndex : 0}"
                        step="1"
                        class="flex-1 h-2 bg-gray-200 dark:bg-gray-600 rounded-lg appearance-none cursor-pointer flag-slider"
                        data-model="${model}"
                        data-flag="${flagName}"
                        data-steps='${JSON.stringify(steps)}'
                    />
                    <span id="flag-value-${flagName}" class="text-sm font-mono text-gray-600 dark:text-gray-400 min-w-16 text-right">
                        ${currentValue}
                    </span>
                </div>
            </div>
        `;
    } else if (config.type === 'advanced') {
        return createAdvancedSettings(model, flagName, config);
    }
    return '';
}

function createAdvancedSettings(model, flagName, config) {
    let html = `
        <div class="mb-4 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <h5 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Advanced Settings</h5>
    `;

    Object.entries(config.fields).forEach(([fieldName, fieldConfig]) => {
        const fieldId = `${model}-${flagName}-${fieldName}`;
        const currentValue = appState.modelFlags[model][fieldName] || fieldConfig.default;

        if (fieldConfig.type === 'select') {
            html += `
                <div class="mb-3">
                    <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                        ${fieldName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </label>
                    <select
                        id="${fieldId}"
                        class="w-full px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                        data-model="${model}"
                        data-field="${fieldName}"
                    >
                        ${fieldConfig.options.map(option =>
                            `<option value="${option}" ${currentValue === option ? 'selected' : ''}>${option}</option>`
                        ).join('')}
                    </select>
                </div>
            `;
        } else if (fieldConfig.type === 'text') {
            html += `
                <div class="mb-3" id="${fieldId}-container">
                    <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                        ${fieldName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </label>
                    <input
                        type="text"
                        id="${fieldId}"
                        value="${currentValue || ''}"
                        class="w-full px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                        placeholder="${fieldConfig.placeholder || ''}"
                        data-model="${model}"
                        data-field="${fieldName}"
                    />
                </div>
            `;
        } else if (fieldConfig.type === 'checkbox') {
            html += `
                <div class="mb-3">
                    <label class="flex items-center text-xs text-gray-600 dark:text-gray-400">
                        <input
                            type="checkbox"
                            id="${fieldId}"
                            ${currentValue ? 'checked' : ''}
                            class="mr-2"
                            data-model="${model}"
                            data-field="${fieldName}"
                        />
                        ${fieldName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </label>
                </div>
            `;
        }
    });

    html += `</div>`;
    return html;
}
```

```javascript
function setupFlagEventListeners(model, modelFlags) {
    Object.keys(modelFlags).forEach(flagName => {
        const config = modelFlags[flagName];

        if (config.type === 'stepped') {
            const slider = document.getElementById(`flag-${flagName}`);
            const valueDisplay = document.getElementById(`flag-value-${flagName}`);

            if (slider && valueDisplay) {
                // Handle slider changes
                slider.addEventListener('input', (e) => {
                    const steps = JSON.parse(e.target.dataset.steps);
                    const index = parseInt(e.target.value);
                    const value = steps[index];

                    // Update display
                    valueDisplay.textContent = value;

                    // Update state
                    appState.modelFlags[model][flagName] = value;
                });

                // Handle clicks anywhere on slider track for snapping
                slider.addEventListener('click', (e) => {
                    const rect = slider.getBoundingClientRect();
                    const percent = (e.clientX - rect.left) / rect.width;
                    const steps = JSON.parse(e.target.dataset.steps);
                    const nearestIndex = Math.round(percent * (steps.length - 1));

                    slider.value = nearestIndex;
                    const value = steps[nearestIndex];

                    // Update display
                    valueDisplay.textContent = value;

                    // Update state
                    appState.modelFlags[model][flagName] = value;
                });
            }
        } else if (config.type === 'advanced') {
            // Setup advanced settings listeners
            Object.entries(config.fields).forEach(([fieldName, fieldConfig]) => {
                const fieldId = `${model}-${flagName}-${fieldName}`;
                const element = document.getElementById(fieldId);

                if (element) {
                    if (fieldConfig.type === 'select') {
                        element.addEventListener('change', (e) => {
                            appState.modelFlags[model][fieldName] = e.target.value;
                            handleConditionalFields(model, flagName, config);
                        });
                    } else if (fieldConfig.type === 'text') {
                        element.addEventListener('input', (e) => {
                            appState.modelFlags[model][fieldName] = e.target.value;
                        });
                    } else if (fieldConfig.type === 'checkbox') {
                        element.addEventListener('change', (e) => {
                            appState.modelFlags[model][fieldName] = e.target.checked;
                        });
                    }
                }
            });
        }
    });
}

function handleConditionalFields(model, flagName, config) {
    Object.entries(config.fields).forEach(([fieldName, fieldConfig]) => {
        if (fieldConfig.depends_on) {
            const fieldId = `${model}-${flagName}-${fieldName}`;
            const container = document.getElementById(`${fieldId}-container`);
            const dependentValue = appState.modelFlags[model][fieldConfig.depends_on];

            if (container) {
                if (dependentValue === fieldConfig.depends_value) {
                    container.classList.remove('hidden');
                } else {
                    container.classList.add('hidden');
                    // Clear value when hidden
                    appState.modelFlags[model][fieldName] = '';
                }
            }
        }
    });
}

function generateFlagString(model) {
    const flags = appState.modelFlags[model];
    if (!flags) return '';

    const flagParts = [];
    Object.entries(flags).forEach(([flagName, value]) => {
        if (value !== 'default') {
            flagParts.push(`--${flagName} ${value}`);
        }
    });

    return flagParts.length > 0 ? ' ' + flagParts.join(' ') : '';
}
```
