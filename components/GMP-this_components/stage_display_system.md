# Stage Display System

Turns the streamed markdown response into interactive accordion cards, supporting both progressive reveal and "show all" views.

```javascript
function parseStages(content) {
    // Remove thinking tags first
    content = content.replace(/<thinking>[\s\S]*?<\/thinking>/g, '');

    // Parse the markdown content to extract stages
    const lines = content.split('\n');
    const stages = [];
    let currentStage = null;
    let currentContent = [];

    for (const line of lines) {
        // More flexible regex to catch various stage formats
        const stageMatch = line.match(/^([🌱🟢🟡🟠🔵🟣🟥⚡🔍🌀🧩🌍🚀🔬💡⚙️🎯🧱📜🏛️✨🔁🪶🕸️🪤🛠️🎭💎]+)\s*.*?(?:Stage|Layer|Junction|Pod|Step)/i) ||
                            line.match(/^###?\s*([🌱🟢🟡🟠🔵🟣🟥⚡🔍🌀🧩🌍🚀🔬💡⚙️🎯🧱📜🏛️✨🔁🪶🕸️🪤🛠️🎭💎]+)/i) ||
                            line.match(/^([🌱🟢🟡🟠🔵🟣🟥⚡🔍🌀🧩🌍🚀🔬💡⚙️🎯🧱📜🏛️✨🔁🪶🕸️🪤🛠️🎭💎]+).*?(?:\d+|0|:)/i);

        if (stageMatch) {
            if (currentStage) {
                currentStage.content = currentContent.join('\n').trim();
                if (currentStage.content) {
                    stages.push(currentStage);
                }
            }
            currentStage = {
                title: line.trim(),
                content: '',
                id: `stage-${stages.length}`
            };
            currentContent = [];
        } else if (currentStage && line.trim()) {
            currentContent.push(line);
        }
    }

    if (currentStage && currentContent.length > 0) {
        currentStage.content = currentContent.join('\n').trim();
        if (currentStage.content) {
            stages.push(currentStage);
        }
    }

    // If no stages found with emoji matching, try a fallback approach
    if (stages.length === 0) {
        console.log("No stages found with emoji matching, trying fallback approach...");
        const fallbackStages = [];
        const sections = content.split(/\n(?=#{1,3}\s)/);

        sections.forEach((section, index) => {
            if (section.trim()) {
                const lines = section.split('\n');
                const title = lines[0].replace(/^#{1,3}\s*/, '').trim();
                const content = lines.slice(1).join('\n').trim();

                if (title && content) {
                    fallbackStages.push({
                        title: title,
                        content: content,
                        id: `stage-${index}`
                    });
                }
            }
        });

        return fallbackStages;
    }

    console.log(`Parsed ${stages.length} stages:`, stages.map(s => s.title));
    return stages;
}

function displayStages(stages, isComplete) {
    currentStages = stages;

    if (showingAllStages) {
        displayAllStages();
    } else {
        displayProgressiveStages(isComplete);
    }
}

// Track current progressive stage
let currentProgressiveStage = 1;

function displayProgressiveStages(isComplete) {
    // Show only up to current progressive stage
    stagesContainer.innerHTML = '';

    const visibleStages = Math.min(currentProgressiveStage, currentStages.length);

    for (let i = 0; i < visibleStages; i++) {
        const stage = currentStages[i];
        const stageCard = createStageCard(stage, i);
        stageCard.classList.add('no-animation'); // Remove blinking
        stagesContainer.appendChild(stageCard);
    }

    // Show "Next Stage" button if there are more stages
    if (currentProgressiveStage < currentStages.length) {
        addNextStageButton();
    }
}

function displayAllStages() {
    stagesContainer.innerHTML = '';

    currentStages.forEach((stage, index) => {
        const stageCard = createStageCard(stage, index);
        stageCard.classList.add('no-animation'); // Remove blinking
        stagesContainer.appendChild(stageCard);
    });
}

function createStageCard(stage, index) {
    const card = document.createElement('div');
    card.className = 'stage-card bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden';
    card.style.animationDelay = `${index * 0.1}s`;

    card.innerHTML = `
        <div class="accordion-header bg-gradient-to-r from-primary to-purple-600 text-white p-4 cursor-pointer" onclick="toggleStage('${stage.id}')">
            <div class="flex justify-between items-center">
                <h3 class="text-lg font-semibold">${stage.title}</h3>
                <svg class="accordion-icon w-5 h-5 transform transition-transform" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                </svg>
            </div>
        </div>
        <div id="${stage.id}" class="accordion-content">
            <div class="p-6 prose dark:prose-invert max-w-none">
                ${formatMarkdown(stage.content)}
            </div>
        </div>
    `;

    return card;
}

function addNextStageButton() {
    const nextButton = document.createElement('div');
    nextButton.className = 'text-center py-6';
    nextButton.innerHTML = `
        <button onclick="showNextStage()" class="bg-primary text-white px-6 py-3 rounded-lg font-medium hover:bg-primary/90 transition-colors">
            Show Next Stage →
        </button>
    `;
    stagesContainer.appendChild(nextButton);
}

function showNextStage() {
    currentProgressiveStage += 1;
    displayProgressiveStages(true);
}

function toggleStage(stageId) {
    const content = document.getElementById(stageId);
    const icon = content.previousElementSibling.querySelector('.accordion-icon');

    if (content.classList.contains('open')) {
        content.classList.remove('open');
        icon.style.transform = 'rotate(0deg)';
    } else {
        content.classList.add('open');
        icon.style.transform = 'rotate(180deg)';
    }
}

// Show all stages toggle
showAllBtn.addEventListener('click', function() {
    showingAllStages = !showingAllStages;

    if (showingAllStages) {
        displayAllStages();
        showAllBtn.textContent = 'Progressive View';
    } else {
        showingAllStages = false;
        displayProgressiveStages(true);
        showAllBtn.textContent = 'Show All Stages';
    }
});
```
