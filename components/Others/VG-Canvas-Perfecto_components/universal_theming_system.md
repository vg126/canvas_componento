# Universal Theming System

Defines reusable color tokens and typography that every interface element inherits. Alternate data-theme modes override the defaults while helper classes toggle ornamental effects.

```css
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

[data-theme="steampunk"] {
    --primary: #d4af37;
    --primary-hover: #b8941f;
    --bg-primary: #2c1810;
    --bg-secondary: #3d2318;
    --bg-tertiary: #4e2e20;
    --text-primary: #f4e4bc;
    --text-secondary: #d4af37;
    --text-tertiary: #b8941f;
    --border: #8b4513;
    --border-light: #a0522d;
    --accent: #ff6b35;
    --font-main: 'Georgia', serif;
}

[data-theme="neon"] {
    --primary: #ff0080;
    --primary-hover: #e6006b;
    --bg-primary: #0d0221;
    --bg-secondary: #1a0440;
    --bg-tertiary: #270660;
    --text-primary: #ff00ff;
    --text-secondary: #ff0080;
    --text-tertiary: #cc0066;
    --border: #4d0099;
    --border-light: #6600cc;
    --accent: #00ffff;
    --font-main: 'Orbitron', sans-serif;
}

[data-theme="forest"] {
    --primary: #228b22;
    --primary-hover: #1e7a1e;
    --bg-primary: #f0f8f0;
    --bg-secondary: #e8f5e8;
    --bg-tertiary: #d0f0d0;
    --text-primary: #2d4a2d;
    --text-secondary: #228b22;
    --text-tertiary: #6b8e6b;
    --border: #9acd32;
    --border-light: #adff2f;
    --accent: #ff6347;
    --font-main: 'Georgia', serif;
}

body {
    background-color: var(--bg-primary);
    color: var(--text-primary);
    font-family: var(--font-main);
    transition: all 0.3s ease;
}

.themed-bg-primary { background-color: var(--bg-primary); }
.themed-bg-secondary { background-color: var(--bg-secondary); }
.themed-bg-tertiary { background-color: var(--bg-tertiary); }
.themed-text-primary { color: var(--text-primary); }
.themed-text-secondary { color: var(--text-secondary); }
.themed-border { border-color: var(--border); }

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
}

.themed-input {
    background-color: var(--bg-primary);
    color: var(--text-primary);
    border: 1px solid var(--border);
}

.terminal-mode .container {
    border: 2px solid var(--accent);
    border-radius: 12px;
}

.steampunk-mode::before {
    content: "⚙️";
    position: fixed;
    top: 20px;
    right: 80px;
    font-size: 24px;
    opacity: 0.3;
    z-index: 1;
}

.neon-mode {
    box-shadow: 0 0 20px var(--accent);
}
```

```javascript
if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.documentElement.classList.add('dark');
}
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
    if (event.matches) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
});
```
