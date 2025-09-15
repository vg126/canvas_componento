# Theme System

Functions that switch interface themes and support dynamic theme customization.

```javascript
function applyTheme(themeName) {
    // Disable transitions during theme change
    document.body.style.transition = 'none';

    document.documentElement.setAttribute('data-theme', themeName);

    // Update mobile browser theme color
    const metaTheme = document.querySelector('meta[name="theme-color"]');
    if (metaTheme) {
        const accentColor = getComputedStyle(document.documentElement)
            .getPropertyValue('--accent').trim();
        metaTheme.content = accentColor;
    }

    // Re-enable transitions after paint
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

// Convert hex to HSL for color calculations
function hexToHsl(hex) {
    const r = parseInt(hex.slice(1, 3), 16) / 255;
    const g = parseInt(hex.slice(3, 5), 16) / 255;
    const b = parseInt(hex.slice(5, 7), 16) / 255;

    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    let h, s, l = (max + min) / 2;

    if (max === min) {
        h = s = 0;
    } else {
        const d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch (max) {
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }
        h /= 6;
    }

    return {
        h: Math.round(h * 360),
        s: Math.round(s * 100),
        l: Math.round(l * 100)
    };
}
```
