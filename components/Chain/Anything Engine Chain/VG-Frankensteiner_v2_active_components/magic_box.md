# Magic Box (Genie) Flow

## Template
```html
<section class="mb-6 p-6 bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 rounded-lg border border-purple-200 dark:border-purple-800">
  <h3 class="font-semibold mb-4 text-purple-800 dark:text-purple-200 text-lg">⚡ Magic Box (Genie) - Universal Engine Designer</h3>
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
    <div class="lg:col-span-2 space-y-4">
      <label class="block text-sm font-medium mb-2">Input Text or Description</label>
      <textarea id="magicBoxInput" rows="8" class="w-full p-4 border rounded-lg" placeholder="Enter any text, problem, idea, or description..."></textarea>
      <div class="flex items-center space-x-4">
        <label class="block text-sm font-medium mb-2">File Attachment (Optional)
          <input type="file" id="magicBoxFile" class="w-full text-sm" accept="*/*" />
        </label>
        <div class="flex-shrink-0">
          <label class="block text-sm font-medium mb-2">Processing Model</label>
          <div id="magicBoxModel" class="accordion-container w-64"></div>
        </div>
      </div>
    </div>
    <div class="space-y-4">
      <label class="block text-sm font-medium mb-2">Bot Count</label>
      <select id="botCountSelector" class="w-full p-2 border rounded">
        <option value="1">1 Bot</option>
        <option value="2">2 Bots</option>
        <option value="3">3 Bots</option>
        <option value="4" selected>4 Bots</option>
        <option value="5">5 Bots</option>
        <option value="6">6 Bots</option>
        <option value="7">7 Bots</option>
        <option value="8">8 Bots</option>
        <option value="9">9 Bots</option>
        <option value="10">10 Bots</option>
      </select>
      <button id="executeMagicBox" class="w-full px-6 py-3 bg-purple-600 text-white rounded-lg relative">
        <span id="executeMagicBoxText">⚡ Generate Engine</span>
        <div id="executeMagicBoxSpinner" class="hidden absolute inset-0 flex items-center justify-center">
          <div class="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
        </div>
      </button>
      <div id="magicBoxFlags" class="hidden flag-container">
        <div id="magicBoxFlagControls"></div>
      </div>
      <div id="magicBoxStatus" class="text-sm text-gray-600 dark:text-gray-400 min-h-[20px]"></div>
    </div>
  </div>
</section>
```

## Execution Logic
```js
async function executeMagicBox() {
  const input = document.getElementById('magicBoxInput').value;
  const fileInput = document.getElementById('magicBoxFile');
  const status = document.getElementById('magicBoxStatus');
  const spinner = document.getElementById('executeMagicBoxSpinner');
  const text = document.getElementById('executeMagicBoxText');
  const botCountSelector = document.getElementById('botCountSelector');

  if (!input.trim() && !fileInput.files[0]) {
    status.textContent = 'Please provide text input or upload a file';
    return;
  }

  spinner.classList.remove('hidden');
  text.classList.add('invisible');
  status.textContent = 'Processing with Magic Box...';

  try {
    updateProcessingLog('Starting Magic Box processing...');

    let promptText = input.trim();
    if (fileInput.files[0]) {
      updateProcessingLog(`Reading file: ${fileInput.files[0].name}`);
      const fileContent = await readFileContent(fileInput.files[0]);
      promptText = promptText ? `${promptText}\n\nFile Content:\n${fileContent}` : fileContent;
    }

    const selectedModel = getSelectedModel('magicBoxModel');
    const botCount = parseInt(botCountSelector.value);
    const flagString = flagManager.generateFlagString(selectedModel);

    const magicBoxPrompt = `ROLE: Anything Engine Architect
SYSTEM: Anything Engine System Designer

CRITICAL CANVAS CONTEXT:
You are designing for Poe Canvas where window.Poe.sendUserMessage sends ALL previous messages in the conversation. This means Bot 3 receives Bot 1 and Bot 2's outputs whether wanted or not. Your prompts SHOULD handle this.

CORE PHILOSOPHY:
Your primary role is to populate the existing multi-stage framework of the Anything Engine by generating its three core operative components, based on the user's request:

* The Keys: The Keys are the core intellectual tools for the engine. Each Key defines a unique perspective or method that will be used to operate upon a Subject. You are to generate a set of distinct Keys that intelligently reflect the user's core request.

* The Subjects (from the Input bank): The Subjects are illustrative topics or pieces of raw content that the engine will process. They serve as the material for the Keys to act upon. You should generate a diverse set of Subjects to demonstrate the engine's capabilities within the universe defined by the user's mandate.

* The Prompts: The Prompts are the operational instructions for each bot in the chain, defining a clear role and a step-by-step workflow. They should be written as flexible templates tailored to the user's mandate. A bot's prompt should be designed to use the provided Key and Subject as its primary operational material.

The engine's power is derived from two key principles that you should build into your generated prompts:

1. Task Specialization: Each bot in the sequence can dedicate its full processing capacity to its dedicated task. The chain can be designed with a mix of bot types, including both reasoning and web search models, to achieve a more focused and detailed output.
2. Chained Contextualization: To manage the Poe Canvas environment, prompts (from the second bot onward) should be designed to treat the full output from previous steps as available background context. The prompt should then instruct the bot to perform its own unique, specialized task to actively build upon, refine, and improve the existing material, ensuring an incremental and value-adding workflow.

YOUR TASK:
Design a complete ${botCount}-bot engine from the user's input. Generate:
1. 5-15 keys (Bank 1)
2. 5-8 input samples (Bank 2)
3. EXACTLY ${botCount} bot prompts (Bank 3)
4. An engine description explaining the approach

OUTPUT FORMAT (JSON ONLY):
{
  "engine_name": "short_descriptive_engine_name",
  "engine_description": "2-3 paragraph description of the system",
  "keys": [
    {"id": 1, "name": "key_name", "method": "clear_operational_method"}
  ],
  "input": [
    {"id": 1, "content": "sample_subject_content"}
  ],
  "prompts": [
    {"id": 1, "bot_number": 1, "role": "role_name", "instructions": "complete_prompt_text"}
  ]
}

REMEMBER:
- Generate EXACTLY ${botCount} prompts.
- Prompts from the second bot onward should handle the Canvas context accumulation as described in the philosophy.

USER INPUT:
${promptText}

Generate the complete engine now as valid JSON only.`;

    updateProcessingLog(`Sending to ${selectedModel}...`);
    await window.Poe.sendUserMessage(`${selectedModel} ${magicBoxPrompt}${flagString}`, {
      handler: 'magic-box-handler',
      stream: true,
      openChat: false,
    });
  } catch (error) {
    console.error('Magic Box error:', error);
    status.textContent = `Error: ${error.message}`;
    updateProcessingLog(`Error: ${error.message}`);
  } finally {
    spinner.classList.add('hidden');
    text.classList.remove('invisible');
  }
}

function handleMagicBoxResponse(result) {
  const status = document.getElementById('magicBoxStatus');

  if (result.responses && result.responses.length > 0) {
    const response = result.responses[0];

    if (response.status === 'error') {
      status.textContent = 'Error occurred during processing';
      updateProcessingLog(`Error: ${response.statusText || 'Unknown error'}`);
    } else if (response.status === 'incomplete') {
      status.textContent = 'Generating transformation engine...';
      if (response.content && response.content.trim()) {
        activeResponseIds.magicbox_streaming = updateProcessingLog({
          title: 'Magic Box streaming response',
          content: response.content,
        }, true, activeResponseIds.magicbox_streaming);
      }
    } else if (response.status === 'complete') {
      status.textContent = 'Magic Box processing complete!';
      updateProcessingLog('Magic Box completed successfully');
      updateProcessingLog({ title: 'Magic Box complete response', content: response.content }, true);
      delete activeResponseIds.magicbox_streaming;

      try {
        const content = response.content.trim();
        const jsonMatch = content.match(/```json\s*([\s\S]*?)\s*```/) ||
                         content.match(/```\s*([\s\S]*?)\s*```/) ||
                         content.match(/\{[\s\S]*\}/);

        if (!jsonMatch) throw new Error('Could not extract JSON from response');

        const jsonString = jsonMatch[1] || jsonMatch[0];
        const parsedData = JSON.parse(jsonString);

        updateProcessingLog({
          title: 'Magic Box parsed JSON structure',
          content: JSON.stringify(parsedData, null, 2),
        }, true);

        bankData.engineName = parsedData.engine_name || 'UnnamedEngine';
        updateProcessingLog(`Engine name: ${bankData.engineName}`);

        if (parsedData.keys) {
          bankData.keys = parsedData.keys;
          updateBankStatus('keysStatus', `Loaded ${parsedData.keys.length} keys`);
        }
        if (parsedData.input) {
          bankData.input = parsedData.input;
          updateBankStatus('inputStatus', `Loaded ${parsedData.input.length} inputs`);
        }
        if (parsedData.prompts) {
          bankData.prompts = parsedData.prompts;
          updateBankStatus('promptsStatus', `Loaded ${parsedData.prompts.length} prompts`);
          populateBotsFromPrompts();
        }

        updatePreview(parsedData.engine_description, bankData.keys, bankData.input, bankData.prompts);
        enableRandomButtons();
      } catch (parseError) {
        console.error('Magic Box parsing error:', parseError);
        status.textContent = 'Could not parse engine structure';
        updateProcessingLog(`Parsing error: ${parseError.message}`);
      }
    }
  }
}

window.Poe.registerHandler('magic-box-handler', result => handleMagicBoxResponse(result));
```

## Architect Prompt Blueprint
The template literal above resolves to the following operator-facing brief when rendered (placeholders wrapped in `{{ }}` indicate runtime substitutions):

```text
ROLE: Anything Engine Architect
SYSTEM: Anything Engine System Designer

CRITICAL CANVAS CONTEXT:
You are designing for Poe Canvas where window.Poe.sendUserMessage sends ALL previous messages in the conversation. This means Bot 3 receives Bot 1 and Bot 2's outputs whether wanted or not. Your prompts SHOULD handle this.

CORE PHILOSOPHY:
Your primary role is to populate the existing multi-stage framework of the Anything Engine by generating its three core operative components, based on the user's request:

* The Keys: The Keys are the core intellectual tools for the engine. Each Key defines a unique perspective or method that will be used to operate upon a Subject. You are to generate a set of distinct Keys that intelligently reflect the user's core request.

* The Subjects (from the Input bank): The Subjects are illustrative topics or pieces of raw content that the engine will process. They serve as the material for the Keys to act upon. You should generate a diverse set of Subjects to demonstrate the engine's capabilities within the universe defined by the user's mandate.

* The Prompts: The Prompts are the operational instructions for each bot in the chain, defining a clear role and a step-by-step workflow. They should be written as flexible templates tailored to the user's mandate. A bot's prompt should be designed to use the provided Key and Subject as its primary operational material.

The engine's power is derived from two key principles that you should build into your generated prompts:

1. Task Specialization: Each bot in the sequence can dedicate its full processing capacity to its dedicated task. The chain can be designed with a mix of bot types, including both reasoning and web search models, to achieve a more focused and detailed output.
2. Chained Contextualization: To manage the Poe Canvas environment, prompts (from the second bot onward) should be designed to treat the full output from previous steps as available background context. The prompt should then instruct the bot to perform its own unique, specialized task to actively build upon, refine, and improve the existing material, ensuring an incremental and value-adding workflow.

YOUR TASK:
Design a complete {{BOT_COUNT}}-bot engine from the user's input. Generate:
1. 5-15 keys (Bank 1)
2. 5-8 input samples (Bank 2)
3. EXACTLY {{BOT_COUNT}} bot prompts (Bank 3)
4. An engine description explaining the approach

OUTPUT FORMAT (JSON ONLY):
{
  "engine_name": "short_descriptive_engine_name",
  "engine_description": "2-3 paragraph description of the system",
  "keys": [
    {"id": 1, "name": "key_name", "method": "clear_operational_method"}
  ],
  "input": [
    {"id": 1, "content": "sample_subject_content"}
  ],
  "prompts": [
    {"id": 1, "bot_number": 1, "role": "role_name", "instructions": "complete_prompt_text"}
  ]
}

REMEMBER:
- Generate EXACTLY {{BOT_COUNT}} prompts.
- Prompts from the second bot onward should handle the Canvas context accumulation as described in the philosophy.

USER INPUT:
{{PROMPT_TEXT}}

Generate the complete engine now as valid JSON only.
```

*Dynamic slots:* `{{BOT_COUNT}}` mirrors the selected bot count, `{{PROMPT_TEXT}}` contains the staged Magic Box description plus any attached file contents, and the rendered prompt inherits any flag string appended to the model call.

## How it works
- **Guided inputs** collect a freeform brief, optional file, chosen model, and bot-count target, revealing additional tuning flags when the selected model supports them.
- **Execution button state** swaps text for a spinner while Magic Box runs, with status messages and processing log entries so operators know exactly what the Genie is doing.
- **Streaming handler** keeps the status panel and log updated in real time, then parses the returned JSON to hydrate the Keys/Input/Prompt banks and preview cards.
- **Bank synchronisation** stores the parsed engine into `bankData`, updates bank status chips, and triggers helper utilities (`populateBotsFromPrompts`, `enableRandomButtons`) for the execution page.
