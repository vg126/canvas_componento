# Poe Integration & Markdown Rendering

Hooks the app into Canvas' `window.Poe` bridge so that quick tests, field reports, and update scans stream results back into the UI. Responses are parsed through `marked` for rich display.

```javascript
if (window.Poe?.registerHandler) {
    window.Poe.registerHandler("quick-test-handler", (result) => {
        const response = result.responses[0];
        const resultDiv = document.getElementById('quickTestResult');

        if (response.status === "complete") {
            resultDiv.innerHTML = marked.parse(response.content || "");
        } else if (response.status === "error") {
            resultDiv.innerHTML = `<span class="text-red-500">Error: ${response.statusText}</span>`;
        }
    });

    window.Poe.registerHandler("field-agent-handler", (result) => {
        const response = result.responses[0];
        const contentDiv = document.getElementById('analysisContent');

        if (response.status === "error") {
            contentDiv.innerHTML = `<span class="text-red-500">Error: ${response.statusText}</span>`;
        } else {
            contentDiv.innerHTML = marked.parse(response.content || "");

            if (response.status === "complete") {
                // Add to analysis history
                const analysisType = document.getElementById('analysisType').value;
                analysisHistory.push({
                    type: analysisType,
                    timestamp: new Date().toISOString(),
                    summary: response.content.substring(0, 100) + "..."
                });
                updateAnalysisHistory();
            }
        }
    });

    window.Poe.registerHandler("update-search-handler", (result) => {
        const response = result.responses[0];
        const resultDiv = document.getElementById('updateResults');

        if (response.status === "error") {
            resultDiv.innerHTML = `<span class="text-red-500">Error: ${response.statusText}</span>`;
        } else {
            resultDiv.innerHTML = marked.parse(response.content || "");
        }
    });
}
```
