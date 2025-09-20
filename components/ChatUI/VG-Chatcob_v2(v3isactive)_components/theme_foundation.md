# Theme Foundation

Base CSS variables and reusable classes that drive the look and feel of `VG-Chatcob_v2(v3isactive).html`.

```css
/* Base theme definition */
:root {
    --primary: #5D5CDE;
    --primary-hover: #4F4ED1;
    --bg-primary: #ffffff;
    --bg-secondary: #f7f7f7;
    --bg-tertiary: #f1f5f9;
    --text-primary: #1a1a1a;
    --text-secondary: #666666;
    --text-tertiary: #94a3b8;
    --border: #e0e0e0;
    --border-light: #f1f5f9;
    --accent: #5D5CDE;
    --success: #10b981;
    --error: #ef4444;
    --warning: #f59e0b;
    --font-main: 'Inter', system-ui, sans-serif;
    --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}

/* Dark theme */
[data-theme="dark"] {
    --bg-primary: #0f172a;
    --bg-secondary: #1e293b;
    --bg-tertiary: #334155;
    --text-primary: #e2e8f0;
    --text-secondary: #94a3b8;
    --text-tertiary: #64748b;
    --border: #374151;
    --border-light: #475569;
    --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.3);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.3);
}

/* Terminal theme */
[data-theme="terminal"] {
    --primary: #00ff00;
    --primary-hover: #00cc00;
    --bg-primary: #000000;
    --bg-secondary: #0a0a0a;
    --bg-tertiary: #1a1a1a;
    --text-primary: #00ff00;
    --text-secondary: #00cc00;
    --text-tertiary: #008800;
    --border: #003300;
    --border-light: #004400;
    --accent: #00ff00;
    --font-main: 'Courier New', monospace;
}

/* Paper theme */
[data-theme="paper"] {
    --primary: #8b5a2b;
    --primary-hover: #7a4f26;
    --bg-primary: #fefefe;
    --bg-secondary: #f8f8f6;
    --bg-tertiary: #f0f0ee;
    --text-primary: #2d2d2d;
    --text-secondary: #5a5a5a;
    --text-tertiary: #8a8a8a;
    --border: #e8e8e6;
    --border-light: #f0f0ee;
    --accent: #8b5a2b;
}

/* Sakura theme */
[data-theme="sakura"] {
    --primary: #ff6b9d;
    --primary-hover: #ff5588;
    --bg-primary: #fff8fc;
    --bg-secondary: #ffeef7;
    --bg-tertiary: #ffe4f2;
    --text-primary: #2d1b20;
    --text-secondary: #6b4c57;
    --text-tertiary: #9d7b87;
    --border: #f0d0e0;
    --border-light: #f8e4f0;
    --accent: #ff6b9d;
}

/* Ayu theme - Dark black with yellow/orange */
[data-theme="ayu"] {
    --primary: #ffcc02;
    --primary-hover: #ffaa00;
    --bg-primary: #0b0b0b;
    --bg-secondary: #1a1a1a;
    --bg-tertiary: #2a2a2a;
    --text-primary: #ffcc02;
    --text-secondary: #ff8f40;
    --text-tertiary: #ffa500;
    --border: #333333;
    --border-light: #404040;
    --accent: #ffcc02;
    --font-main: 'Inter', system-ui, sans-serif;
}

/* Apply theme variables to body */
body {
    background-color: var(--bg-primary);
    color: var(--text-primary);
    font-family: var(--font-main);
    transition: background-color 0.3s ease, color 0.3s ease;
}

/* Comprehensive Theme-aware Components */
.themed-bg-primary { background-color: var(--bg-primary); }
.themed-bg-secondary { background-color: var(--bg-secondary); }
.themed-bg-tertiary { background-color: var(--bg-tertiary); }
.themed-text-primary { color: var(--text-primary); }
.themed-text-secondary { color: var(--text-secondary); }
.themed-text-tertiary { color: var(--text-tertiary); }
.themed-border { border-color: var(--border); }
.themed-border-light { border-color: var(--border-light); }
.themed-primary { color: var(--primary); }
.themed-accent { color: var(--accent); }

/* Button Themes */
.themed-btn {
    background-color: var(--bg-secondary);
    color: var(--text-secondary);
    border: 1px solid var(--border);
    transition: all 0.2s ease;
}
.themed-btn:hover {
    background-color: var(--bg-tertiary);
    color: var(--text-primary);
}

.themed-btn-primary {
    background-color: var(--primary);
    color: white;
    border: 1px solid var(--primary);
}
.themed-btn-primary:hover {
    background-color: var(--primary-hover);
    border-color: var(--primary-hover);
}

/* Input Themes */
.themed-input {
    background-color: var(--bg-primary);
    color: var(--text-primary);
    border: 1px solid var(--border);
}
.themed-input:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 2px rgba(93, 92, 222, 0.2);
}
.themed-input::placeholder {
    color: var(--text-tertiary);
}

/* Modal Themes */
.themed-modal {
    background-color: var(--bg-primary);
    border: 1px solid var(--border);
    box-shadow: var(--shadow-lg);
}
.themed-modal-overlay {
    background-color: rgba(0, 0, 0, 0.5);
}

/* Message Themes */
.themed-message-user {
    background-color: var(--primary);
    color: white;
}
.themed-message-ai {
    background-color: var(--bg-secondary);
    color: var(--text-primary);
    border: 1px solid var(--border-light);
}
```

```css
/* Dropdown Themes */
.themed-dropdown {
    background-color: var(--bg-primary);
    border: 1px solid var(--border);
    box-shadow: var(--shadow-lg);
}
.themed-dropdown-item {
    color: var(--text-primary);
}
.themed-dropdown-item:hover {
    background-color: var(--bg-tertiary);
}
.themed-dropdown-item.selected {
    background-color: var(--primary)20;
    color: var(--primary);
}

/* Thinking Section Themes */
.themed-thinking {
    background-color: var(--bg-tertiary);
    border: 1px solid var(--border);
}
.themed-thinking-header {
    background-color: var(--bg-secondary);
    color: var(--text-secondary);
}
.themed-thinking-header:hover {
    background-color: var(--bg-tertiary);
}
.themed-thinking-content {
    background-color: var(--bg-primary);
    color: var(--text-tertiary);
    border: 1px solid var(--border-light);
}

/* Menu & Utility Styles */
.themed-menu {
    background-color: var(--bg-primary);
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
}
.themed-menu-item {
    color: var(--text-primary);
}
.themed-menu-item:hover {
    background-color: var(--bg-tertiary);
}
.themed-menu-item.danger {
    color: var(--error);
}
.themed-menu-item.danger:hover {
    background-color: var(--error)10;
}

.themed-file-preview {
    background-color: var(--bg-tertiary);
    border: 1px solid var(--border);
}

.themed-spinner {
    color: var(--primary);
}

.themed-scroll::-webkit-scrollbar {
    width: 6px;
}
.themed-scroll::-webkit-scrollbar-track {
    background: var(--bg-secondary);
}
.themed-scroll::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 3px;
}
.themed-scroll::-webkit-scrollbar-thumb:hover {
    background: var(--text-tertiary);
}
```
