# Input and File Handling

Watches the GMP knowledge upload and concept textarea so the analyzer only activates when both are provided.

```javascript
// File upload handler
gmpFile.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            gmpFileContent = e.target.result;
            updateAnalyzeButton();
        };
        reader.readAsText(file);
    }
});

// Input validation
function updateAnalyzeButton() {
    const hasInput = conceptInput.value.trim().length > 0;
    const hasFile = gmpFileContent !== null;
    analyzeBtn.disabled = !(hasInput && hasFile);
}

conceptInput.addEventListener('input', updateAnalyzeButton);
```
