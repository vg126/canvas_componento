# UI Utilities and Reset

Shared helpers that keep the interface polished—formatting markdown, surfacing errors, toggling loading states, and resetting the workspace for a new concept.

```javascript
function formatMarkdown(content) {
    return content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code class="bg-gray-100 dark:bg-gray-700 px-1 rounded">$1</code>')
        .replace(/\n/g, '<br>');
}

function setLoading(loading) {
    const loadingSpinner = document.getElementById('loadingSpinner');
    const analyzeText = document.getElementById('analyzeText');

    if (loading) {
        loadingSpinner.classList.remove('hidden');
        analyzeText.textContent = 'Analyzing...';
        analyzeBtn.disabled = true;
    } else {
        loadingSpinner.classList.add('hidden');
        analyzeText.textContent = 'Analyze Concept';
        updateAnalyzeButton();
    }
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 px-4 py-3 rounded-lg mb-4';
    errorDiv.textContent = message;
    resultsSection.insertBefore(errorDiv, resultsSection.firstChild);

    setTimeout(() => errorDiv.remove(), 5000);
}

clearBtn.addEventListener('click', function() {
    conceptInput.value = '';
    gmpSelect.value = 'ai-recommend';
    gmpFile.value = '';
    gmpFileContent = null;
    resultsSection.classList.add('hidden');
    gmpRecommendation.classList.add('hidden');
    stagesContainer.innerHTML = '';
    chatMessages.innerHTML = '';
    currentAnalysis = null;
    currentStages = [];
    showingAllStages = false;
    updateAnalyzeButton();
});

// Helper functions for recommendations
function selectRecommendedGMP(choice) {
    // This would be implemented to parse the recommendation and auto-select
    // For now, just proceed with analysis
    performAnalysis(conceptInput.value.trim(), 'gmp-o3', aiModel.value);
}

function showGMPSelector() {
    gmpRecommendation.classList.add('hidden');
    // User can then manually select from dropdown
}
```
