# Tab Navigation Shell

Implements the top-level documentation tabs that drive which workflow panel is active. Buttons share a data attribute consumed by the `switchTab` helper.

```html
<!-- Navigation Tabs -->
<div class="sticky top-0 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 z-10">
    <div class="container mx-auto px-4">
        <div class="flex space-x-1 overflow-x-auto">
            <button class="tab-btn active" data-tab="architecture">🏗️ System Architecture</button>
            <button class="tab-btn" data-tab="testing">🧪 Feature Testing Lab</button>
            <button class="tab-btn" data-tab="doctor">👨‍⚕️ Doctor Inside Patient</button>
            <button class="tab-btn" data-tab="updates">🔄 System Updates</button>
            <button class="tab-btn" data-tab="findings">📊 Live Findings</button>
        </div>
    </div>
</div>
```

```javascript
// Tab Management
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.getAttribute('data-tab');
        switchTab(tabName);
    });
});

function switchTab(tabName) {
    // Update buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-tab') === tabName) {
            btn.classList.add('active');
        }
    });

    // Show content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.add('hidden');
    });
    document.getElementById(tabName + '-tab').classList.remove('hidden');
}
```
