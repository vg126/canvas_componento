# Workflow Runner Logic

```js
            }
        };

        // ===== PHASE 2A: BOT EXECUTION TIMEOUT SYSTEM =====
        
        function resetBotState(botNumber) {
            console.log(`[DRBanger] Resetting Bot ${botNumber} state`);
            
            // Clear bot from active executions
            activeBotExecutions.delete(botNumber);
            
            // Clear timeout if exists
            if (botExecutionTimeouts.has(botNumber)) {
                clearTimeout(botExecutionTimeouts.get(botNumber));
                botExecutionTimeouts.delete(botNumber);
                console.log(`[DRBanger] Cleared timeout for Bot ${botNumber}`);
            }
            
            // Reset UI state
            const stepMap = { 1: 'step1Status', 2: 'step2Status', 3: 'step3Status', 4: 'step4Status', 5: 'step5Status', 6: 'step6Status' };
            updateStepStatus(stepMap[botNumber], 'idle');
            
            // Reset status display
            const statusElement = document.getElementById(`bot${botNumber}Status`);
            if (statusElement) {
                statusElement.textContent = "";
                statusElement.className = 'text-sm text-gray-600 dark:text-gray-400 mb-2';
            }
            
            // Update all button states
            updateAllButtonStates();
            updateFloatingButton();
            
            console.log(`[DRBanger] Bot ${botNumber} state reset complete`);
        }

        // ===== UTILITY FUNCTIONS =====
        
        function updateStepStatus(stepId, status) {
            const element = document.getElementById(stepId);
            if (!element) return;

            element.classList.remove('bg-gray-200', 'dark:bg-gray-700', 'bg-blue-500', 'bg-green-500', 'bg-red-500');
            element.classList.remove('text-gray-700', 'dark:text-gray-300', 'text-white');

            switch (status) {
                case 'active':
                    element.classList.add('bg-blue-500', 'text-white');
                    break;
                case 'complete':
                    element.classList.add('bg-green-500', 'text-white');
                    break;
                case 'error':
                    element.classList.add('bg-red-500', 'text-white');
                    break;
                default:
                    element.classList.add('bg-gray-200', 'dark:bg-gray-700', 'text-gray-700', 'dark:text-gray-300');
            }
        }

        function handleBotResponse(result, botNum, onComplete) {
            const status = document.getElementById(`${botNum}Status`);
            const output = document.getElementById(`${botNum}Output`);
            
            // Update model display in results section
            updateBotModelDisplay(botNum);
            
            if (result.responses && result.responses.length > 0) {
                const response = result.responses[0];
                
                if (response.status === "error") {
                    console.error(`[DRBanger] Bot ${botNum} error:`, response.statusText);
                    status.textContent = "❌ Error occurred";
                    status.className = 'text-sm text-red-600 dark:text-red-400 mb-2';
                    output.innerHTML = `<div class="text-red-600">Error: ${response.statusText || 'Unknown error'}</div>`;
                    onBotEnd(botNum.replace('bot', ''));
                    updateStepStatus(`step${botNum.replace('bot', '')}Status`, 'error');
                    
                    // Log bot error (not accumulated)
                    addLogEntry('bot_error', `${botNum} Error`, response.statusText || 'Unknown error');
                } else if (response.status === "incomplete") {
                    status.textContent = "⏳ Generating response...";
                    status.className = 'text-sm text-blue-600 dark:text-blue-400 mb-2';
                    output.innerHTML = marked.parse(response.content || "Loading...");
                    
                    // Accumulate streaming logs instead of creating new entries each time
                    updateStreamingLog(botNum, response.content);
                } else if (response.status === "complete") {
                    console.log(`[DRBanger] Bot ${botNum} completed successfully`);
                    status.textContent = "✅ Complete";
                    status.className = 'text-sm text-green-600 dark:text-green-400 mb-2';
                    output.innerHTML = marked.parse(response.content);
                    onBotEnd(botNum.replace('bot', ''));
                    
                    // Finalize streaming log
                    finalizeStreamingLog(botNum, response.content);
                    
                    if (onComplete && typeof onComplete === 'function') {
                        onComplete();
                    }
                }
            } else {
                console.error(`[DRBanger] ${botNum}: No response received`);
                onBotEnd(botNum.replace('bot', ''));
                showErrorToast(`${botNum}: No response received`);
                addLogEntry('bot_error', `${botNum} Error`, 'No response received');
            }
        }

        // New function to update model display in results section
        function updateBotModelDisplay(botNum) {
            const botNumber = parseInt(botNum.replace('bot', ''));
            const modelDisplayElement = document.getElementById(`${botNum}ModelDisplay`);
            
            if (modelDisplayElement) {
                const selectedModel = selectedBotModels[botNumber - 1];
                if (selectedModel) {
                    modelDisplayElement.textContent = selectedModel;
                    modelDisplayElement.className = 'text-xs font-mono bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 px-2 py-1 rounded';
                } else {
                    modelDisplayElement.textContent = 'No model selected';
                    modelDisplayElement.className = 'text-xs font-mono bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 px-2 py-1 rounded';
                }
            }
        }

        // Streaming log accumulation functions
        function updateStreamingLog(botNum, content) {
            if (!content || content.length < 50) return; // Avoid spam for very short content
            
            const logKey = `${botNum}_streaming`;
            
            if (!streamingLogs[logKey]) {
                // Create new streaming log entry
                const entry = {
                    id: Date.now(),
                    type: 'bot_output',
                    title: `${botNum} Streaming`,
                    content: content,
                    timestamp: new Date().toLocaleString(),
                    isStreaming: true
                };
                
                streamingLogs[logKey] = entry;
                logEntries.push(entry);
                addStreamingLogToDOM(entry);
                updateLogCount();
            } else {
                // Update existing streaming log
                streamingLogs[logKey].content = content;
                updateStreamingLogInDOM(logKey, content);
            }
        }

        function finalizeStreamingLog(botNum, finalContent) {
            const logKey = `${botNum}_streaming`;
            
            if (streamingLogs[logKey]) {
                // Update to final content and mark as complete
                streamingLogs[logKey].content = finalContent;
                streamingLogs[logKey].title = `${botNum} Complete`;
                streamingLogs[logKey].type = 'bot_complete';
                streamingLogs[logKey].isStreaming = false;
                
                // Update DOM
                updateStreamingLogInDOM(logKey, finalContent, true);
                
                // Clean up
                delete streamingLogs[logKey];
            } else {
                // No streaming log exists, create completion log
                addLogEntry('bot_complete', `${botNum} Complete`, `Final output: ${finalContent.substring(0, 300)}${finalContent.length > 300 ? '...' : ''}`);
            }
        }

        function addStreamingLogToDOM(entry) {
            const loggingContent = document.getElementById('loggingContent');
            const loggingEmpty = document.getElementById('loggingEmpty');
            
            if (loggingEmpty && !loggingEmpty.classList.contains('hidden')) {
                loggingEmpty.classList.add('hidden');
            }
            
            const entryDiv = document.createElement('div');
            entryDiv.className = `log-entry streaming border-l-4 pl-4 py-2 mb-2 border-purple-500 bg-purple-50 dark:bg-purple-900/20`;
            entryDiv.style.fontFamily = loggingSettings.font;
            entryDiv.id = `log-${entry.id}`;
            
            const isLongContent = entry.content.length > 200;
            const contentPreview = isLongContent ? entry.content.substring(0, 200) + '...' : entry.content;
            
            entryDiv.innerHTML = `
                <div class="flex justify-between items-start mb-1">
                    <div class="flex items-center space-x-2">
                        <span class="font-semibold ${loggingSettings.size} text-purple-800 dark:text-purple-200">${entry.title} ⚡</span>
                        <span class="text-xs text-gray-500 dark:text-gray-400">${entry.timestamp}</span>
                        ${isLongContent ? `<button onclick="toggleLogExpand('log-${entry.id}')" class="text-xs text-blue-600 dark:text-blue-400 hover:underline">expand</button>` : ''}
                    </div>
                </div>
                <div class="text-sm text-purple-800 dark:text-purple-200 font-mono whitespace-pre-wrap overflow-x-auto">
                    <div id="log-${entry.id}-preview" class="max-h-32 overflow-y-auto">
                        ${contentPreview}
                    </div>
                    ${isLongContent ? `<div id="log-${entry.id}-full" class="hidden max-h-96 overflow-y-auto">${entry.content}</div>` : ''}
                </div>
            `;
            
            loggingContent.appendChild(entryDiv);
            loggingContent.scrollTop = loggingContent.scrollHeight;
        }

        function updateStreamingLogInDOM(logKey, content, isComplete = false) {
            const entry = streamingLogs[logKey];
            if (!entry) return;
            
            const entryDiv = document.getElementById(`log-${entry.id}`);
            if (!entryDiv) return;
            
            const isLongContent = content.length > 200;
            const contentPreview = isLongContent ? content.substring(0, 200) + '...' : content;
            
            // Update title if complete
            const titleSpan = entryDiv.querySelector('.font-semibold');
            if (isComplete && titleSpan) {
                titleSpan.textContent = `${entry.title.split(' ')[0]} Complete ✅`;
                entryDiv.className = entryDiv.className.replace('border-purple-500 bg-purple-50 dark:bg-purple-900/20', 'border-green-600 bg-green-100 dark:bg-green-900/30');
                titleSpan.className = titleSpan.className.replace('text-purple-800 dark:text-purple-200', 'text-green-900 dark:text-green-100');
            }
            
            // Update content
            const previewDiv = entryDiv.querySelector(`#log-${entry.id}-preview`);
            const fullDiv = entryDiv.querySelector(`#log-${entry.id}-full`);
            
            if (previewDiv) {
                previewDiv.textContent = contentPreview;
            }
            if (fullDiv) {
                fullDiv.textContent = content;
            }
            
            // Auto-scroll to bottom
            const loggingContent = document.getElementById('loggingContent');
            loggingContent.scrollTop = loggingContent.scrollHeight;
        }

        // ===== CASCADING DROPDOWN SYSTEM =====
        function initializeCascadingDropdowns() {
            if (!sstDatabase || !Array.isArray(sstDatabase)) return;
            
            const domainSelect = document.getElementById('sstDomainSelect');
            const techniqueSelect = document.getElementById('sstTechniqueSelect');

            // Populate domain dropdown
            domainSelect.innerHTML = '<option value="">Select a domain...</option>';
            sstDatabase.forEach(domain => {
                const option = document.createElement('option');
                option.value = domain.domain;
                option.textContent = domain.domain;
                domainSelect.appendChild(option);
            });

            // Domain selection handler
            domainSelect.addEventListener('change', function() {
                const selectedDomain = this.value;
                techniqueSelect.innerHTML = '<option value="">Select a technique...</option>';
                techniqueSelect.disabled = !selectedDomain;

                if (selectedDomain) {
                    const domainData = sstDatabase.find(d => d.domain === selectedDomain);
                    if (domainData) {
                        domainData.techniques.forEach(tech => {
                            const option = document.createElement('option');
                            option.value = JSON.stringify({ name: tech.name, method: tech.method });
                            option.textContent = tech.name;
                            techniqueSelect.appendChild(option);
                        });
                        techniqueSelect.disabled = false;
                    }
                }
            });

            // Technique selection handler - auto-apply to SST box
            techniqueSelect.addEventListener('change', function() {
                if (this.value) {
                    try {
                        const { name, method } = JSON.parse(this.value);
                        const formattedSST = `**SST TECHNIQUE**: ${name}\n**APPLICATION METHOD**: ${method}`;
                        document.getElementById('sstCapsule').value = formattedSST;
                        console.log('[DRBanger] SST auto-applied:', formattedSST);
                        
                        // Reset dropdowns
                        domainSelect.value = '';
                        techniqueSelect.innerHTML = '<option value="">Select a technique...</option>';
                        techniqueSelect.disabled = true;
                    } catch (error) {
                        console.error('[DRBanger] Error applying selected SST:', error);
                        showErrorToast('Error applying selected SST');
                    }
                }
            });
        }

        // ===== SIMPLIFIED BOT EXECUTION TRACKING =====
        
        let currentWorkflowBot = 1;
        let workflowRunning = false;
        let activeBotExecutions = new Set(); // Track currently running bots for UI feedback only
        let botExecutionTimeouts = new Map(); // Track timeout IDs for bot executions

        function updateFloatingButton() {
            const button = document.getElementById('nextBotButton');
            const text = document.getElementById('nextBotText');
            const spinner = document.getElementById('nextBotSpinner');
            
            // Only disable floating button if it's specifically running
            const floatingBotRunning = activeBotExecutions.has(currentWorkflowBot);
            
            if (floatingBotRunning) {
                text.classList.add('hidden');
                spinner.classList.remove('hidden');
                button.disabled = true;
                button.classList.add('opacity-50', 'cursor-not-allowed');
                text.textContent = `⏳ Running Bot ${currentWorkflowBot}...`;
            } else {
                text.classList.remove('hidden');
                spinner.classList.add('hidden');
                button.disabled = false;
                button.classList.remove('opacity-50', 'cursor-not-allowed');
                
                if (currentWorkflowBot <= 6) {
                    text.textContent = `▶️ Next: Bot ${currentWorkflowBot}`;
                } else {
                    text.textContent = `🔄 Restart: Bot 1`;
                    currentWorkflowBot = 1;
                }
            }
        }

        function advanceWorkflow() {
            // Allow workflow to proceed even if other bots are running
            console.log(`[DRBanger] Floating button executing Bot ${currentWorkflowBot}`);
            executeBot(currentWorkflowBot);
        }

        function onBotComplete(botNumber) {
            console.log(`[DRBanger] Bot ${botNumber} completed, syncing workflow`);
            
            // If this was the workflow bot, advance the sequence
            if (botNumber === currentWorkflowBot) {
                if (currentWorkflowBot === 6) {
                    currentWorkflowBot = 1;
                    showStateToast('🎉 Workflow complete! Ready to restart.');
                } else {
                    currentWorkflowBot++;
                }
            }
            
            updateFloatingButton();
            updateAllButtonStates(); // Sync all buttons
        }

        function onBotStart(botNumber) {
            console.log(`[DRBanger] Bot ${botNumber} started, tracking for UI`);
            activeBotExecutions.add(botNumber);
            
            updateFloatingButton();
            updateAllButtonStates();
        }

        function onBotEnd(botNumber) {
            console.log(`[DRBanger] Bot ${botNumber} ended, updating UI`);
            activeBotExecutions.delete(botNumber);
            
            // PHASE 2A: Clear timeout when bot ends
            if (botExecutionTimeouts.has(botNumber)) {
                clearTimeout(botExecutionTimeouts.get(botNumber));
                botExecutionTimeouts.delete(botNumber);
                console.log(`[DRBanger] Cleared timeout for Bot ${botNumber} on normal completion`);
            }
            
            updateFloatingButton();
            updateAllButtonStates();
        }

        // ===== SIMPLIFIED BUTTON STATE MANAGEMENT =====
        function updateAllButtonStates() {
            for (let i = 1; i <= 6; i++) {
                const isRunning = activeBotExecutions.has(i);
                
                // Update input tab buttons - show loading state but DON'T disable multiple executions
                const inputButton = document.getElementById(`executeBot${i}`);
                const inputText = document.getElementById(`executeBot${i}Text`);
                const inputSpinner = document.getElementById(`executeBot${i}Spinner`);
                
                if (inputButton) {
                    // Always keep buttons enabled for multiple executions
                    inputButton.disabled = false;
                    inputButton.classList.remove('opacity-50', 'cursor-not-allowed');
                    
                    if (isRunning) {
                        if (inputText) inputText.classList.add('invisible');
                        if (inputSpinner) inputSpinner.classList.remove('hidden');
                    } else {
                        if (inputText) inputText.classList.remove('invisible');
                        if (inputSpinner) inputSpinner.classList.add('hidden');
                    }
                }
                
                // Update results tab buttons - same logic
                const resultsButton = document.getElementById(`executeBot${i}Results`);
                if (resultsButton) {
                    resultsButton.disabled = false;
                    resultsButton.classList.remove('opacity-50', 'cursor-not-allowed');
                }
                
                // Update Bot 6 panel button
                if (i === 6) {
                    const panelButton = document.getElementById('executeBot6Panel');
                    const panelText = document.getElementById('executeBot6PanelText');
                    const panelSpinner = document.getElementById('executeBot6PanelSpinner');
                    
                    
                    if (panelButton) {
                        panelButton.disabled = false;
                        panelButton.classList.remove('opacity-50', 'cursor-not-allowed');
                        
                        if (isRunning) {
                            if (panelText) panelText.classList.add('invisible');
                            if (panelSpinner) panelSpinner.classList.remove('hidden');
                        } else {
                            if (panelText) panelText.classList.remove('invisible');
                            if (panelSpinner) panelSpinner.classList.add('hidden');
                        }
                    }
                }
            }
        }

        // ===== POE HANDLERS =====
        
        ['bot1', 'bot2', 'bot3', 'bot4', 'bot5', 'bot6'].forEach(botId => {
            window.Poe.registerHandler(`${botId}-handler`, (result) => {
                const stepMap = { bot1: 'step1Status', bot2: 'step2Status', bot3: 'step3Status', bot4: 'step4Status', bot5: 'step5Status', bot6: 'step6Status' };
                
                handleBotResponse(result, botId, () => {
                    updateStepStatus(stepMap[botId], 'complete');
                    
                    // Special handling for Bot 6 - extract SST and put in main box
                    if (botId === 'bot6' && result.responses && result.responses.length > 0) {
                        const content = result.responses[0].content;
                        const sstMatch = content.match(/\*\*SST TECHNIQUE\*\*:\s*(.*?)\n\*\*APPLICATION METHOD\*\*:\s*(.*?)(?:\n|$)/s);
                        if (sstMatch) {
                            const formattedSST = `**SST TECHNIQUE**: ${sstMatch[1].trim()}\n**APPLICATION METHOD**: ${sstMatch[2].trim()}`;
                            document.getElementById('sstCapsule').value = formattedSST;
                            console.log('[DRBanger] Bot 6 auto-fed SST to main box:', formattedSST);
                        }
                    }
                    
                    // Advance floating button workflow
                    const botNumber = parseInt(botId.replace('bot', ''));
                    onBotComplete(botNumber);
                });
            });
        });

        // ===== BOT EXECUTION FUNCTIONS =====
        
        async function executeBot(botNumber) {
            console.log(`[DRBanger] Executing Bot ${botNumber}`);
            
            const legalText = document.getElementById('legalText').value.trim();
            const sstTechnique = document.getElementById('sstCapsule').value.trim();
            
            const botSelector = botSelectors.find(s => s.botId === `bot${botNumber}`);
            const botName = botSelector ? botSelector.selectedModel : selectedBotModels[botNumber - 1];
            
            // NEW: Get the injected instruction for the current bot
            const customInstruction = injectedInstructions[botNumber];

            addLogEntry('bot_start', `Bot ${botNumber} Started`, `Executing ${botName || 'No model'} with ${legalText ? 'legal text' : 'no legal text'} and ${sstTechnique ? 'SST technique' : 'no SST'}`);
            
            const cleanBotName = botName ? botName.replace(/^@/, '') : '';
            
            if (!cleanBotName) {
                showErrorToast(`Bot ${botNumber}: No model selected`);
                onBotEnd(botNumber); // Use onBotEnd to sync UI
                addLogEntry('bot_error', `Bot ${botNumber} Error`, 'No model selected');
                return;
            }
            
            const stepMap = { 1: 'step1Status', 2: 'step2Status', 3: 'step3Status', 4: 'step4Status', 5: 'step5Status', 6: 'step6Status' };
            
            let prompt;
            
            onBotStart(botNumber); // Use onBotStart to sync UI
            updateStepStatus(stepMap[botNumber], 'active');
            document.getElementById(`bot${botNumber}Status`).textContent = "🚀 Starting analysis...";
            
            // PHASE 2A: Set timeout for bot execution (180 seconds)
            const timeoutId = setTimeout(() => {
                console.warn(`[DRBanger] Bot ${botNumber} timed out after 180 seconds`);
                showErrorToast(`Bot ${botNumber} timed out - resetting state`);
                resetBotState(botNumber);
                addLogEntry('bot_error', `Bot ${botNumber} Timeout`, 'Execution timed out after 3 minutes');
            }, 180000); // 180 seconds = 3 minutes
            
            botExecutionTimeouts.set(botNumber, timeoutId);
            console.log(`[DRBanger] Set timeout for Bot ${botNumber}:`, timeoutId);
            
            try {
                switch (botNumber) {
                    case 1:
                        if (!legalText || !sstTechnique) {
                            showErrorToast("Bot 1: Missing legal text or SST technique - proceeding anyway");
                            console.warn('[DRBanger] Bot 1 missing inputs but proceeding');
                        }
                        if (customPrompts.bot1) {
                            prompt = customPrompts.bot1
                                .replace(/\${legalText}/g, legalText || "[NO LEGAL TEXT PROVIDED]")
                                .replace(/\${sstTechnique}/g, sstTechnique || "[NO SST TECHNIQUE PROVIDED]");
                        } else {
                            prompt = botPrompts.bot1(legalText || "[NO LEGAL TEXT PROVIDED]", sstTechnique || "[NO SST TECHNIQUE PROVIDED]", customInstruction);
                        }
                        break;
                        
                    case 2:
                        const bot1Output = document.getElementById('bot1Output').textContent;
                        if (!bot1Output) {
                            showErrorToast("Bot 2: No Bot 1 output available - proceeding anyway");
                            console.warn('[DRBanger] Bot 2 missing Bot 1 output but proceeding');
                        }
                        if (customPrompts.bot2) {
                            prompt = customPrompts.bot2
                                .replace(/\${bot1Output}/g, bot1Output || "[NO BOT 1 OUTPUT]")
                                .replace(/\${legalText}/g, legalText || "[NO LEGAL TEXT]");
                        } else {
                            prompt = botPrompts.bot2(bot1Output || "[NO BOT 1 OUTPUT]", legalText || "[NO LEGAL TEXT]", customInstruction);
                        }
                        break;
                        
                    case 3:
                        const bot2Output = document.getElementById('bot2Output').textContent;
                        const bot1Output3 = document.getElementById('bot1Output').textContent;
                        if (!bot2Output || !bot1Output3) {
                            showErrorToast("Bot 3: Missing previous bot outputs - proceeding anyway");
                            console.warn('[DRBanger] Bot 3 missing previous outputs but proceeding');
                        }
                        if (customPrompts.bot3) {
                            prompt = customPrompts.bot3
                                .replace(/\${bot2Output}/g, bot2Output || "[NO BOT 2 OUTPUT]")
                                .replace(/\${bot1Output}/g, bot1Output3 || "[NO BOT 1 OUTPUT]");
                        } else {
                            prompt = botPrompts.bot3(bot2Output || "[NO BOT 2 OUTPUT]", bot1Output3 || "[NO BOT 1 OUTPUT]", customInstruction);
                        }
                        break;
                        
                    case 4:
                        const bot2Output4 = document.getElementById('bot2Output').textContent;
                        const bot3Output = document.getElementById('bot3Output').textContent;
                        if (!bot2Output4 || !bot3Output) {
                            showErrorToast("Bot 4: Missing Bot 2/3 outputs - proceeding anyway");
                            console.warn('[DRBanger] Bot 4 missing previous outputs but proceeding');
                        }
                         if (customPrompts.bot4) {
                            prompt = customPrompts.bot4
                                .replace(/\${bot2Output}/g, bot2Output4 || "[NO BOT 2 OUTPUT]")
                                .replace(/\${bot3Output}/g, bot3Output || "[NO BOT 3 OUTPUT]")
                                .replace(/\${legalText}/g, legalText || "[NO LEGAL TEXT]")
                                .replace(/\${sstTechnique}/g, sstTechnique || "[NO SST]");
                        } else {
                            prompt = botPrompts.bot4(bot2Output4 || "[NO BOT 2 OUTPUT]", bot3Output || "[NO BOT 3 OUTPUT]", legalText || "[NO LEGAL TEXT]", sstTechnique || "[NO SST]", customInstruction);
                        }
                        break;
                        
                    case 5:
                        const bot4Output = document.getElementById('bot4Output').textContent;
                        if (!bot4Output) {
                            showErrorToast("Bot 5: No Bot 4 output available - proceeding anyway");
                            console.warn('[DRBanger] Bot 5 missing Bot 4 output but proceeding');
                        }
                         if (customPrompts.bot5) {
                            prompt = customPrompts.bot5.replace(/\${bot4Output}/g, bot4Output || "[NO BOT 4 OUTPUT]");
                        } else {
                            prompt = botPrompts.bot5(bot4Output || "[NO BOT 4 OUTPUT]", customInstruction);
                        }
                        break;
                        
                    case 6:
                        const conversationHistory = [1, 2, 3, 4, 5].map(i => {
                            const output = document.getElementById(`bot${i}Output`).textContent;
                            return output ? `Bot ${i} Output:\n${output}\n\n` : `Bot ${i} Output: [NO OUTPUT]\n\n`;
                        }).join('');
                        
                        const customDomain = document.getElementById('customDomain').value.trim();
                        const userInstruction = document.getElementById('customInstruction').value.trim();
                        
                        if (customPrompts.bot6) {
                            prompt = customPrompts.bot6
                                .replace(/\${conversationHistory}/g, conversationHistory)
                                .replace(/\${customDomain}/g, customDomain || '[NULL - Select optimal domain based on analysis gaps]')
                                .replace(/\${customInstruction}/g, userInstruction || '[NULL - Use standard generation protocol]');
                        } else {
                            prompt = botPrompts.bot6(conversationHistory, customDomain, userInstruction, customInstruction);
                        }
                        break;
                        
                    default:
                        showErrorToast("Invalid bot number");
                        onBotEnd(botNumber);
                        return;
                }
                
                let inputPreview = "Inputs:\n";
                if (legalText) inputPreview += `Legal Text: ${legalText.substring(0, 100)}${legalText.length > 100 ? '...' : ''}\n`;
                if (sstTechnique) inputPreview += `SST: ${sstTechnique.substring(0, 100)}${sstTechnique.length > 100 ? '...' : ''}\n`;
                if(customInstruction) inputPreview += `Custom Instruction: ${customInstruction.substring(0, 100)}${customInstruction.length > 100 ? '...' : ''}\n`;
                addLogEntry('bot_input', `Bot ${botNumber} Input`, inputPreview);
                
                console.log(`[DRBanger] Bot ${botNumber} executing with prompt length:`, prompt.length);
                
                await window.Poe.sendUserMessage(`@${cleanBotName} ${prompt}`, {
                    handler: `bot${botNumber}-handler`,
                    stream: true,
                    openChat: false
                });
                
            } catch (error) {
                console.error(`[DRBanger] Bot ${botNumber} execution error:`, error);
                showErrorToast(`Bot ${botNumber} error: ${error.message}`);
                updateStepStatus(stepMap[botNumber], 'error');
                resetBotState(botNumber); // PHASE 2A: Use resetBotState instead of onBotEnd for cleanup
                addLogEntry('bot_error', `Bot ${botNumber} Error`, `Execution failed: ${error.message}`);
            }
        }

        // ===== EVENT LISTENERS =====
        
        // Initialize all systems
        setupInputButtons();
        setupBotButtons();
        setupClearButtons();
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
```

## How it works
- **Step-aware status chips** are updated through `updateStepStatus`, colouring the six workflow badges as each bot moves from idle → active → complete/error across both tabs.
- **Poe streaming adapter** (`handleBotResponse`) keeps status text and rendered Markdown in sync, finishing with `onBotEnd` cleanup and optional SST auto-feed from Bot 6.
- **Floating Next Bot control** tracks `currentWorkflowBot` and active executions so operators can march through the chain or pick bots manually without desynchronising the UI.
- **Timeout protection** registers a three-minute safety timer per bot; if Poe never returns, the handler clears spinners, resets buttons, and emits a log entry explaining the timeout.
- **Prompt assembly** in `executeBot` stitches inputs, prior bot outputs, and optional injected instructions into template strings, then streams to `window.Poe.sendUserMessage` while logging both the request preview and the running response.
