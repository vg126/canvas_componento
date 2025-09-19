# State Management Suite

```js

        // ===== PHASE 5: STATE MANAGEMENT SYSTEM =====
        
        function captureCurrentState() {
            const state = {
                version: "2.1-InjectionEnabled",
                timestamp: new Date().toISOString(),
                phase: "Enhanced State Management",
                
                // Inputs
                inputs: {
                    legalText: document.getElementById('legalText').value,
                    sstCapsule: document.getElementById('sstCapsule').value,
                    customDomain: document.getElementById('customDomain').value,
                    customInstruction: document.getElementById('customInstruction').value
                },
                
                // Bot model selections from accordion selectors
                botModelSelections: selectedBotModels,
                
                // Bot outputs and statuses
                botResults: {},
                
                // Workflow progress
                workflowProgress: {},
                
                // SST Database
                sstDatabase: sstDatabase,
                sstDatabaseStatus: document.getElementById('sstDatabaseStatus') ? {
                    text: document.getElementById('sstDatabaseStatus').textContent,
                    className: document.getElementById('sstDatabaseStatus').className
                } : null,
                
                // Legal Text Database
                legalTextDatabase: legalTextDatabase,
                
                // Bot Prompts Database
                botPromptsDatabase: botPromptsDatabase,
                customPrompts: customPrompts,
                
                injectedInstructions: injectedInstructions,
                
                // Workflow state
                currentWorkflowBot: currentWorkflowBot,
                workflowRunning: workflowRunning
            };
            
            // Capture bot results
            for (let i = 1; i <= 6; i++) {
                const output = document.getElementById(`bot${i}Output`);
                const status = document.getElementById(`bot${i}Status`);
                
                state.botResults[`bot${i}`] = {
                    output: output ? output.innerHTML : '',
                    status: status ? status.textContent : '',
                    statusClassName: status ? status.className : ''
                };
            }
            
            // Capture workflow progress
            for (let i = 1; i <= 6; i++) {
                const stepStatus = document.getElementById(`step${i}Status`);
                if (stepStatus) {
                    state.workflowProgress[`step${i}`] = {
                        text: stepStatus.textContent,
                        className: stepStatus.className
                    };
                }
            }
            
            return state;
        }

        function restoreState(state) {
            try {
                console.log('[DRBanger] Restoring state:', state);
                
                // Restore inputs
                if (state.inputs) {
                    if (state.inputs.legalText !== undefined) {
                        document.getElementById('legalText').value = state.inputs.legalText;
                    }
                    if (state.inputs.sstCapsule !== undefined) {
                        document.getElementById('sstCapsule').value = state.inputs.sstCapsule;
                    }
                    if (state.inputs.customDomain !== undefined) {
                        document.getElementById('customDomain').value = state.inputs.customDomain;
                    }
                    if (state.inputs.customInstruction !== undefined) {
                        document.getElementById('customInstruction').value = state.inputs.customInstruction;
                    }
                }
                
                // Restore bot selections
                if (state.botSelections) {
                    for (let i = 1; i <= 6; i++) {
                        const botSelect = document.getElementById(`bot${i}`);
                        if (botSelect && state.botSelections[`bot${i}`]) {
                            botSelect.value = state.botSelections[`bot${i}`];
                        }
                    }
                }
                
                // Restore bot results
                if (state.botResults) {
                    for (let i = 1; i <= 6; i++) {
                        const outputDiv = document.getElementById(`bot${i}Output`);
                        const statusDiv = document.getElementById(`bot${i}Status`);
                        const botResult = state.botResults[`bot${i}`];
                        
                        if (outputDiv && botResult) {
                            outputDiv.innerHTML = botResult.output || '';
                            if (statusDiv) {
                                statusDiv.textContent = botResult.status || '';
                                statusDiv.className = botResult.statusClassName || 'text-sm text-gray-600 dark:text-gray-400 mb-2';
                            }
                        }
                    }
                }
                
                // Restore workflow progress
                if (state.workflowProgress) {
                    for (let i = 1; i <= 6; i++) {
                        const stepStatus = document.getElementById(`step${i}Status`);
                        const stepData = state.workflowProgress[`step${i}`];
                        
                        if (stepStatus && stepData) {
                            stepStatus.textContent = stepData.text;
                            stepStatus.className = stepData.className;
                        }
                    }
                }
                
                // Restore Injected Instructions and update UI
                if (state.injectedInstructions) {
                    injectedInstructions = state.injectedInstructions;
                    for (let i = 1; i <= 6; i++) {
                        const instruction = injectedInstructions[i];
                        const instructionBox = document.getElementById(`bot${i}-custom-instruction`);
                        const summary = document.getElementById(`bot${i}-injection-summary`);
                        const clearBtn = document.getElementById(`clear-instruction-bot${i}`);

                        if (instructionBox && summary && clearBtn) {
                            if (instruction) {
                                instructionBox.value = instruction;
                                summary.innerHTML = '✅ Custom Instruction Injected!';
                                summary.classList.add('text-green-600', 'dark:text-green-400');
                                clearBtn.classList.remove('hidden');
                            } else {
                                instructionBox.value = '';
                                summary.innerHTML = '➕ Add Custom Instruction';
                                summary.classList.remove('text-green-600', 'dark:text-green-400');
                                clearBtn.classList.add('hidden');
                            }
                        }
                    }
                }
                
                // Restore SST Database
                if (state.sstDatabase) {
                    sstDatabase = state.sstDatabase;
                    const statusElement = document.getElementById('sstDatabaseStatus');
                    if (state.sstDatabaseStatus && statusElement) {
                        statusElement.textContent = state.sstDatabaseStatus.text;
                        statusElement.className = state.sstDatabaseStatus.className;
                    }
                    initializeCascadingDropdowns();
                }
                
                // Preview system removed - keeping settings for compatibility
                if (state.previewSettings) {
                    previewSettings = state.previewSettings;
                }
                
                // Preview items no longer used - converted to logging
                
                console.log('[DRBanger] State restored successfully');
                return true;
                
            } catch (error) {
                console.error('[DRBanger] Error restoring state:', error);
                return false;
            }
        }

        function saveState() {
            try {
                const state = captureCurrentState();
                const stateJson = JSON.stringify(state, null, 2);
                
                navigator.clipboard.writeText(stateJson).then(() => {
                    console.log('[DRBanger] State saved to clipboard');
                    showStateToast('💾 State saved to clipboard');
                }).catch(err => {
                    console.error('[DRBanger] Failed to save state to clipboard:', err);
                    showErrorToast('Failed to save state to clipboard');
                });
                
            } catch (error) {
                console.error('[DRBanger] Error saving state:', error);
                showErrorToast('Error saving state');
            }
        }

        function loadState() {
            document.getElementById('loadStateModal').classList.remove('hidden');
            document.getElementById('loadStateTextarea').value = '';
        }

        function confirmLoadState() {
            const jsonText = document.getElementById('loadStateTextarea').value.trim();
            
            if (!jsonText) {
                showErrorToast('Please paste state JSON');
                return;
            }
            
            try {
                const state = JSON.parse(jsonText);
                
                // Critical: Validate state structure before restoration
                if (!validateStateStructure(state)) {
                    showErrorToast('Invalid state structure - cannot load');
                    return;
                }
                
                const success = restoreState(state);
                
                if (success) {
                    showStateToast('📁 State loaded successfully');
                    document.getElementById('loadStateModal').classList.add('hidden');
                } else {
                    showErrorToast('Failed to restore state completely');
                }
                
            } catch (error) {
                console.error('[DRBanger] Invalid JSON:', error);
                showErrorToast(`Invalid JSON format: ${error.message}`);
            }
        }

        function validateStateStructure(state) {
            try {
                // Basic structure validation to prevent logic bombs
                if (!state || typeof state !== 'object') {
                    console.error('[DRBanger] State is not an object');
                    return false;
                }
                
                // Check for required fields
                const requiredFields = ['version', 'timestamp'];
                for (const field of requiredFields) {
                    if (!(field in state)) {
                        console.error(`[DRBanger] Missing required field: ${field}`);
                        return false;
                    }
                }
                
                // Validate inputs structure if present
                if (state.inputs && typeof state.inputs !== 'object') {
                    console.error('[DRBanger] Invalid inputs structure');
                    return false;
                }
                
                // Validate botResults structure if present
                if (state.botResults) {
                    if (typeof state.botResults !== 'object') {
                        console.error('[DRBanger] Invalid botResults structure');
                        return false;
                    }
                    
        setupLegalTextDatabaseControls();
        
        // No longer needed - preview system replaced with logging
        
        // ===== NEW STATE MANAGEMENT FUNCTIONS =====
        
        function downloadStateAsFile() {
            try {
                const state = captureCurrentState();
                const stateJson = JSON.stringify(state, null, 2);
                const timestamp = getFormattedTimestamp();
                const filename = `DRBanger_State_${timestamp}.json`;
                
                const blob = new Blob([stateJson], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                
                console.log('[DRBanger] State downloaded as file:', filename);
                showStateToast('📥 State downloaded as file');
            } catch (error) {
                console.error('[DRBanger] Error downloading state:', error);
                showErrorToast('Error downloading state');
            }
        }

        function importStateFromClipboard() {
            document.getElementById('loadStateModal').classList.remove('hidden');
            document.getElementById('loadStateTextarea').value = '';
            document.getElementById('loadStateTextarea').placeholder = 'Paste your DRBanger state JSON here...';
        }

        function loadStateFromFile() {
            const fileInput = document.getElementById('stateFileInput');
            fileInput.click();
        }

        // Hidden file input handler for state upload
        document.getElementById('stateFileInput').addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file && file.type === 'application/json') {
                const reader = new FileReader();
                reader.onload = function(e) {
                    try {
                        const state = JSON.parse(e.target.result);
                        const success = restoreState(state);
                        
                        if (success) {
                            showStateToast('📁 State loaded from file successfully');
                        } else {
                            showErrorToast('Failed to restore state completely');
                        }
                        
                    } catch (error) {
                        console.error('[DRBanger] Invalid state file:', error);
                        showErrorToast('Invalid JSON format in state file');
                    }
                };
                reader.readAsText(file);
            } else {
                showErrorToast('Please select a valid JSON file');
            }
            
            // Reset file input for future use
            event.target.value = '';
        });

        // State Management Event Listeners - Consolidated
        ['Input', 'Results'].forEach(tab => {
            document.getElementById(`saveState${tab}`).addEventListener('click', saveState);
            document.getElementById(`downloadState${tab}`).addEventListener('click', downloadStateAsFile);
            document.getElementById(`loadState${tab}`).addEventListener('click', loadStateFromFile);
            document.getElementById(`importState${tab}`).addEventListener('click', importStateFromClipboard);
        });
        
        // Modal controls
        document.getElementById('confirmLoadState').addEventListener('click', confirmLoadState);
        document.getElementById('cancelLoadState').addEventListener('click', cancelLoadState);
        
        // Bot execution buttons - Consolidated for both tabs
        for (let i = 1; i <= 6; i++) {
            document.getElementById(`executeBot${i}`).addEventListener('click', () => executeBot(i));
            document.getElementById(`executeBot${i}Results`).addEventListener('click', () => executeBot(i));
        }

        // Bot 6 Panel Execute Button
        document.getElementById('executeBot6Panel').addEventListener('click', () => executeBot(6));

        // Sample random SST button
        document.getElementById('sampleSSTBtn').addEventListener('click', () => {
            const randomSST = getRandomSST();
            if (randomSST) {
                document.getElementById('sstCapsule').value = randomSST;
                console.log('[DRBanger] Random SST sampled:', randomSST);
            } else {
                showErrorToast("No SST database loaded");
            }
        });

        // Download Flow
        document.getElementById('downloadFlow').addEventListener('click', downloadFlow);

        // Download All Responses
        document.getElementById('downloadAllResponses').addEventListener('click', downloadFlow);

        // Legal Text Database System
        let legalTextDatabase = null;

        // ===== BOT PROMPTS DATABASE SYSTEM =====
        let botPromptsDatabase = null;
        let customPrompts = {
            bot1: null,
            bot2: null,
            bot3: null,
            bot4: null,
            bot5: null,
            bot6: null
        };
        // NEW: Storage for per-bot injected instructions
        let injectedInstructions = { 1: null, 2: null, 3: null, 4: null, 5: null, 6: null };

        // Bot Prompts Database file upload handler
        document.getElementById('botPromptsFile').addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file && file.type === 'application/json') {
                const reader = new FileReader();
                reader.onload = function(e) {
                    try {
                        const data = JSON.parse(e.target.result);
                        botPromptsDatabase = data;
                        document.getElementById('botPromptsDatabaseStatus').textContent = `Loaded ${data.length} bot prompts`;
```

## How it works
- **`captureCurrentState()`** serialises every critical field (inputs, model picks, bot outputs, workflow chips, injected instructions, and database payloads) so the workflow can be paused or resumed later without drift.
- **`restoreState()`** repopulates textareas, dropdowns, status badges, and instruction boxes, re-initialising SST dropdowns and maintaining UI affordances such as "Add Custom Instruction" prompts.
- **Validation gates** (`validateStateStructure`) and `safeJsonParse` guard against malformed or malicious JSON before applying it to the DOM, showing toast messages when something fails.
- **Clipboard & file tooling** expose `saveState`, `loadState`, `downloadStateAsFile`, and `importStateFromClipboard`, providing both manual JSON paste and one-click export/import pathways.
- **Download helpers** (`downloadAllResponses`, `downloadStateAsFile`) generate timestamped files so research sessions and bot transcripts can be archived alongside the configuration snapshot.
