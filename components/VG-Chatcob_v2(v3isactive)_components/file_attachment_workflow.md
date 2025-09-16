# File Attachment Workflow

Input resizing and attachment preview logic for sending files alongside prompts.

```javascript
const chatContainer = document.getElementById('chatContainer');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const modelSelector = document.getElementById('modelSelector');
const fileInput = document.getElementById('fileInput');
const attachBtn = document.getElementById('attachBtn');
const filePreview = document.getElementById('filePreview');
const fileName = document.getElementById('fileName');
const removeFile = document.getElementById('removeFile');

let selectedFiles = [];

// Auto-resize textarea
messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

// File handling
attachBtn.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', function(e) {
    selectedFiles = Array.from(e.target.files);
    if (selectedFiles.length > 0) {
        const fileNames = selectedFiles.map(f => f.name).join(', ');
        fileName.textContent = fileNames;
        filePreview.classList.remove('hidden');
    }
});

removeFile.addEventListener('click', function() {
    selectedFiles = [];
    fileInput.value = '';
    filePreview.classList.add('hidden');
});
```
