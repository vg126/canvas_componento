# Theme Foundation

Defines the design tokens shared across light/dark variants and registers Tailwind overrides before the page loads.

## CSS variable palette

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
```

* Provides a neutral baseline for light mode while exposing semantic colors for buttons, alerts, and typography.

The file then layers named themes via `[data-theme="dark"]`, `[data-theme="terminal"]`, `[data-theme="paper"]`, `[data-theme="sakura"]`, and `[data-theme="ayu"]`, each overriding the same custom properties so components automatically inherit the new look without extra classes.

Utility classes such as `.themed-bg-primary`, `.themed-message-user`, `.themed-thinking`, `.themed-menu`, and `.themed-scroll` map DOM nodes to the appropriate variables, keeping the templates Tailwind-friendly while still theme-aware.

## Tailwind setup

```javascript
tailwind.config = {
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                primary: '#5D5CDE',
                'primary-hover': '#4F4ED1'
            }
        }
    },
    corePlugins: {
        preflight: false
    }
}
```

* Extends the palette so Tailwind utility classes like `bg-primary` are available if needed.
* Disables `preflight` to avoid conflicting with Canvas-hosted styles.

Console warnings from Tailwind are silenced for production-like cleanliness by wrapping `console.warn` and ignoring messages that mention Tailwind or production mode.

## Runtime application

```javascript
const THEMES = ['dark', 'terminal', 'paper', 'sakura', 'ayu'];
let currentTheme = 'dark';

function applyTheme(themeName) {
    document.body.style.transition = 'none';

    document.documentElement.setAttribute('data-theme', themeName);

    const metaTheme = document.querySelector('meta[name="theme-color"]');
    if (metaTheme) {
        const accentColor = getComputedStyle(document.documentElement)
            .getPropertyValue('--accent').trim();
        metaTheme.content = accentColor;
    }

    requestAnimationFrame(() => {
        document.body.style.transition = '';
    });

    currentTheme = themeName;
}

function cycleTheme() {
    const currentIndex = THEMES.indexOf(currentTheme);
    const nextIndex = (currentIndex + 1) % THEMES.length;
    applyTheme(THEMES[nextIndex]);
}
```

* Applies the selected theme by toggling the `data-theme` attribute on `<html>` and temporarily disables transitions to avoid flicker.
* Keeps track of the current theme for quick cycling via the header button or keyboard triggers.
