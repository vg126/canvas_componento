# Model Flag System

Allows per-model parameter overrides using sliders and conditional advanced settings, and injects the resulting switches into outgoing prompts.

## Flag metadata

`MODEL_FLAGS` maps model IDs to available controls. Each entry can declare either a stepped slider or a nested `advanced` block. A truncated example:

```javascript
const MODEL_FLAGS = {
    "Claude-Opus-4": {
        "thinking_budget": {
            "type": "stepped",
            "steps": [0, 4096, 8192, 12288, 16384, 20480, 24576, 28672, 30768],
            "default": "default"
        }
    },
    "Linkup-Deep-Search": {
        "advanced_settings": {
            "type": "advanced",
            "fields": {
                "domain_filter_mode": {
                    "type": "select",
                    "options": ["none", "Include", "Exclude"],
                    "default": "none"
                },
                "include_domains": {
                    "type": "text",
                    "placeholder": "e.g. github.com",
                    "depends_on": "domain_filter_mode",
                    "depends_value": "Include"
                },
                // ... additional controls elided ...
            }
        }
    }
};
```

`appState.modelFlags` stores the user's selections keyed by model so sliders retain their positions when revisiting a model.

## Modal entry point

```javascript
function openFlagModal() {
    const modal = document.getElementById('flagModal');
    const flagContent = document.getElementById('flagContent');
    const selectedModel = appState.selectedModel;

    const modelFlags = MODEL_FLAGS[selectedModel];

    if (!modelFlags) {
        flagContent.innerHTML = `
            <div class="text-center text-gray-500 dark:text-gray-400 py-8">
                <div class="text-4xl mb-2">🚫</div>
                <p>No flags available for ${selectedModel}</p>
            </div>
        `;
    } else {
        if (!appState.modelFlags[selectedModel]) {
            appState.modelFlags[selectedModel] = {};
        }

        let html = `<div class="mb-4"><h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Available flags for ${selectedModel}:</h4></div>`;

        Object.entries(modelFlags).forEach(([flagName, config]) => {
            html += createSteppedFlag(selectedModel, flagName, config);
        });

        flagContent.innerHTML = html;
        setupFlagEventListeners(selectedModel, modelFlags);
    }

    modal.classList.remove('hidden');
}
```

* Initializes persistent storage for the model on first open.
* Defers rendering to helper functions based on flag type.

## Rendering stepped sliders and advanced fields

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
```

Advanced sections render per-field controls and honor conditional visibility requirements:

```javascript
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
            const isVisible = !fieldConfig.depends_on ||
                            appState.modelFlags[model][fieldConfig.depends_on] === fieldConfig.depends_value;

            html += `
                <div class="mb-3 ${isVisible ? '' : 'hidden'}" id="${fieldId}-container">
                    <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                        ${fieldName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </label>
                    <input
                        type="text"
                        id="${fieldId}"
                        placeholder="${fieldConfig.placeholder || ''}"
                        value="${currentValue || ''}"
                        class="w-full px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
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

## Event wiring and conditional logic

```javascript
function setupFlagEventListeners(model, modelFlags) {
    Object.keys(modelFlags).forEach(flagName => {
        const config = modelFlags[flagName];

        if (config.type === 'stepped') {
            const slider = document.getElementById(`flag-${flagName}`);
            const valueDisplay = document.getElementById(`flag-value-${flagName}`);

            if (slider && valueDisplay) {
                slider.addEventListener('input', (e) => {
                    const steps = JSON.parse(e.target.dataset.steps);
                    const index = parseInt(e.target.value);
                    const value = steps[index];

                    valueDisplay.textContent = value;
                    appState.modelFlags[model][flagName] = value;
                });

                slider.addEventListener('click', (e) => {
                    const rect = slider.getBoundingClientRect();
                    const percent = (e.clientX - rect.left) / rect.width;
                    const steps = JSON.parse(e.target.dataset.steps);
                    const nearestIndex = Math.round(percent * (steps.length - 1));

                    slider.value = nearestIndex;
                    const value = steps[nearestIndex];

                    valueDisplay.textContent = value;
                    appState.modelFlags[model][flagName] = value;
                });
            }
        } else if (config.type === 'advanced') {
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
```

```javascript
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
                    appState.modelFlags[model][fieldName] = '';
                }
            }
        }
    });
}
```

## Prompt integration

```javascript
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

The flag string is appended to every prompt built in `sendMessage`, ensuring that custom reasoning budgets or advanced parameters accompany the request without mutating the visible chat transcript.
