# File Attachment and Input Ergonomics

Helpers that adapt the composer area, maintain a preview of pending uploads, and propagate attachments into `sendMessage`.

## Textarea resizing

```javascript
messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});
```

* Expands the textarea up to 120px tall before reintroducing scrolling.
* Keeps the composer compact once the user clears the field.

## Attachment preview lifecycle

```javascript
const fileInput = document.getElementById('fileInput');
const attachBtn = document.getElementById('attachBtn');
const filePreview = document.getElementById('filePreview');
const fileName = document.getElementById('fileName');
const removeFile = document.getElementById('removeFile');

let selectedFiles = [];

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

* Uses a hidden `<input type="file" multiple>` and a themed button to trigger the native picker.
* Displays a comma-separated list of filenames and reveals the preview panel when attachments exist.
* Clears both the DOM input element and the `selectedFiles` array when the user clicks **Remove**.

## Dispatch integration

`sendMessage` checks `selectedFiles` and forwards the array to Poe as the `attachments` option. After a successful send the array, hidden input, and preview state are reset so subsequent messages start fresh.
