# Analysis Workflow

Orchestrates the request/response loop with Poe, covering AI recommendations, direct protocol analysis, and streaming updates back into the UI.

```javascript
// Register Poe handlers
window.Poe.registerHandler("gmp-analysis", (result, context) => {
    const msg = result.responses[0];

    if (msg.status === "error") {
        showError("Analysis failed: " + msg.statusText);
        setLoading(false);
    } else if (msg.status === "incomplete") {
        // Show streaming progress
        if (context.type === "recommendation") {
            updateRecommendation(msg.content);
        } else if (context.type === "analysis") {
            updateAnalysis(msg.content, false);
        } else if (context.type === "chat") {
            updateChatMessage(context.messageId, msg.content, false);
        }
    } else if (msg.status === "complete") {
        if (context.type === "recommendation") {
            finalizeRecommendation(msg.content);
        } else if (context.type === "analysis") {
            finalizeAnalysis(msg.content);
        } else if (context.type === "chat") {
            updateChatMessage(context.messageId, msg.content, true);
        }
        setLoading(false);
    }
});

// Main analysis function
async function analyzeConceptWithGMP() {
    const concept = conceptInput.value.trim();
    const selectedGMP = gmpSelect.value;
    const selectedAI = aiModel.value;

    if (!concept || !gmpFileContent) {
        showError("Please enter a concept and upload the GMP file.");
        return;
    }

    setLoading(true);
    resultsSection.classList.remove('hidden');

    try {
        if (selectedGMP === "ai-recommend") {
            // First get AI recommendation
            await getGMPRecommendation(concept, selectedAI);
        } else {
            // Direct analysis with selected GMP
            await performAnalysis(concept, selectedGMP, selectedAI);
        }
    } catch (error) {
        showError("Error: " + error.message);
        setLoading(false);
    }
}

async function getGMPRecommendation(concept, aiModel) {
    const prompt = `Based on this concept: "${concept}"\n\nPlease analyze which Genesis Mapping Protocols would be most suitable and recommend the top 3 options with brief explanations of why each would work well for this concept.\n\nFocus on:\n- The nature of the concept (tangible/intangible, simple/complex)\n- Which GMP approaches would yield the most insightful analysis\n- Brief rationale for each recommendation\n\nPlease format your response as:\n1. **[GMP Name]**: [Brief explanation]\n2. **[GMP Name]**: [Brief explanation]\n3. **[GMP Name]**: [Brief explanation]`;

    await window.Poe.sendUserMessage(
        `@${aiModel} ${prompt}`,
        {
            handler: "gmp-analysis",
            stream: true,
            openChat: false,
            handlerContext: { type: "recommendation" },
            attachments: gmpFileContent ? [new File([gmpFileContent], "gmp-combined.md", { type: "text/markdown" })] : []
        }
    );
}

async function performAnalysis(concept, gmpId, aiModel) {
    const prompt = `Using the ${gmpId.toUpperCase()} framework from the attached file, please perform a complete analysis of this concept: "${concept}"\n\nPlease follow the exact structure and methodology specified in the ${gmpId.toUpperCase()} protocol. Include all stages/layers as defined in that specific framework.\n\nPresent the analysis with:\n- Clear stage/layer headers with emojis as specified\n- Both analytical and experiential tracks where applicable\n- Any unique features specific to this GMP (analogies, edge cases, etc.)\n- Progressive depth as outlined in the framework\n\nFormat the response in a clear, structured manner that follows the exact template of the selected GMP.`;

    await window.Poe.sendUserMessage(
        `@${aiModel} ${prompt}`,
        {
            handler: "gmp-analysis",
            stream: true,
            openChat: false,
            handlerContext: { type: "analysis", gmpId: gmpId },
            attachments: gmpFileContent ? [new File([gmpFileContent], "gmp-combined.md", { type: "text/markdown" })] : []
        }
    );
}

function updateRecommendation(content) {
    const recommendationContent = document.getElementById('recommendationContent');
    recommendationContent.innerHTML = formatMarkdown(content);
    gmpRecommendation.classList.remove('hidden');
}

function finalizeRecommendation(content) {
    updateRecommendation(content);

    // Add selection buttons
    const recommendationOptions = document.getElementById('recommendationOptions');
    recommendationOptions.innerHTML = `
        <button onclick="selectRecommendedGMP('auto')" class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors">
            Use First Recommendation
        </button>
        <button onclick="showGMPSelector()" class="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors">
            Choose Manually
        </button>
    `;
}

function updateAnalysis(content, isComplete) {
    currentAnalysis = content;
    currentProgressiveStage = 1; // Reset progressive counter
    displayStages(parseStages(content), isComplete);
}

function finalizeAnalysis(content) {
    updateAnalysis(content, true);
}

analyzeBtn.addEventListener('click', analyzeConceptWithGMP);
```
