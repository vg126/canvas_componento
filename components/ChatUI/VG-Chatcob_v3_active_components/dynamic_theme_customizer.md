# Dynamic Theme Customizer

Interactive controls for crafting custom palettes, previewing them live, and persisting named presets without touching localStorage.

## Color math utilities

```javascript
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

    return [h * 360, s * 100, l * 100];
}

function hslToHex(h, s, l) {
    h /= 360;
    s /= 100;
    l /= 100;

    const c = (1 - Math.abs(2 * l - 1)) * s;
    const x = c * (1 - Math.abs((h * 6) % 2 - 1));
    const m = l - c / 2;
    let r = 0, g = 0, b = 0;

    if (0 <= h * 6 && h * 6 < 1) {
        r = c; g = x; b = 0;
    } else if (1 <= h * 6 && h * 6 < 2) {
        r = x; g = c; b = 0;
    } else if (2 <= h * 6 && h * 6 < 3) {
        r = 0; g = c; b = x;
    } else if (3 <= h * 6 && h * 6 < 4) {
        r = 0; g = x; b = c;
    } else if (4 <= h * 6 && h * 6 < 5) {
        r = x; g = 0; b = c;
    } else if (5 <= h * 6 && h * 6 < 6) {
        r = c; g = 0; b = x;
    }

    r = Math.round((r + m) * 255);
    g = Math.round((g + m) * 255);
    b = Math.round((b + m) * 255);

    return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}
```

```javascript
function generateThemeColors(primaryColor, backgroundColor, textColor) {
    const [primaryH, primaryS, primaryL] = hexToHsl(primaryColor);
    const [bgH, bgS, bgL] = hexToHsl(backgroundColor);
    const [textH, textS, textL] = hexToHsl(textColor);

    const primaryHover = hslToHex(primaryH, primaryS, Math.max(primaryL - 10, 0));

    const bgSecondary = hslToHex(bgH, bgS, Math.min(bgL + (bgL < 50 ? 5 : -5), 100));
    const bgTertiary = hslToHex(bgH, bgS, Math.min(bgL + (bgL < 50 ? 10 : -10), 100));

    const textSecondary = hslToHex(textH, Math.max(textS - 20, 0), textL > 50 ? textL - 15 : textL + 15);
    const textTertiary = hslToHex(textH, Math.max(textS - 30, 0), textL > 50 ? textL - 25 : textL + 25);

    const border = hslToHex(bgH, bgS, textL > 50 ? bgL + 15 : bgL - 15);
    const borderLight = hslToHex(bgH, bgS, textL > 50 ? bgL + 10 : bgL - 10);

    return {
        primary: primaryColor,
        primaryHover: primaryHover,
        bgPrimary: backgroundColor,
        bgSecondary: bgSecondary,
        bgTertiary: bgTertiary,
        textPrimary: textColor,
        textSecondary: textSecondary,
        textTertiary: textTertiary,
        border: border,
        borderLight: borderLight,
        accent: primaryColor
    };
}
```

* Produces a full theme token set from three base colors, ensuring hover, border, and tertiary shades remain in harmony.

## Applying and saving themes

```javascript
function applyCustomTheme() {
    const primaryColor = document.getElementById('primaryColorPicker').value;
    const backgroundColor = document.getElementById('backgroundColorPicker').value;
    const textColor = document.getElementById('textColorPicker').value;

    const themeColors = generateThemeColors(primaryColor, backgroundColor, textColor);

    const customThemeCSS = `
        [data-theme="custom"] {
            --primary: ${themeColors.primary};
            --primary-hover: ${themeColors.primaryHover};
            --bg-primary: ${themeColors.bgPrimary};
            --bg-secondary: ${themeColors.bgSecondary};
            --bg-tertiary: ${themeColors.bgTertiary};
            --text-primary: ${themeColors.textPrimary};
            --text-secondary: ${themeColors.textSecondary};
            --text-tertiary: ${themeColors.textTertiary};
            --border: ${themeColors.border};
            --border-light: ${themeColors.borderLight};
            --accent: ${themeColors.accent};
            --font-main: 'Inter', system-ui, sans-serif;
            --success: #10b981;
            --error: #ef4444;
            --warning: #f59e0b;
            --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
            --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
        }
    `;

    let customStyleElement = document.getElementById('custom-theme-style');
    if (!customStyleElement) {
        customStyleElement = document.createElement('style');
        customStyleElement.id = 'custom-theme-style';
        document.head.appendChild(customStyleElement);
    }
    customStyleElement.textContent = customThemeCSS;

    applyTheme('custom');

    showNotification('Custom theme applied!');
    closeThemeModal();
}
```

```javascript
function saveCustomTheme() {
    const themeName = document.getElementById('themeNameInput').value.trim();
    if (!themeName) {
        showNotification('Please enter a theme name', 'error');
        return;
    }

    const primaryColor = document.getElementById('primaryColorPicker').value;
    const backgroundColor = document.getElementById('backgroundColorPicker').value;
    const textColor = document.getElementById('textColorPicker').value;

    appState.savedThemes[themeName] = {
        primary: primaryColor,
        background: backgroundColor,
        text: textColor
    };

    document.getElementById('themeNameInput').value = '';

    renderSavedThemes();
    showNotification(`Theme "${themeName}" saved!`);
}
```

```javascript
function loadCustomTheme(themeName) {
    const theme = appState.savedThemes[themeName];
    if (!theme) return;

    document.getElementById('primaryColorPicker').value = theme.primary;
    document.getElementById('primaryColorHex').value = theme.primary;
    document.getElementById('backgroundColorPicker').value = theme.background;
    document.getElementById('backgroundColorHex').value = theme.background;
    document.getElementById('textColorPicker').value = theme.text;
    document.getElementById('textColorHex').value = theme.text;

    updateThemePreview();
    showNotification(`Theme "${themeName}" loaded!`);
}

function deleteCustomTheme(themeName) {
    delete appState.savedThemes[themeName];
    renderSavedThemes();
    showNotification(`Theme "${themeName}" deleted!`);
}
```

`appState.savedThemes` tracks all named presets in-memory, avoiding browser storage yet still supporting load/delete cycles during the session.

## Previewing and listing themes

```javascript
function renderSavedThemes() {
    const container = document.getElementById('savedThemesList');
    if (!container) return;

    if (Object.keys(appState.savedThemes).length === 0) {
        container.innerHTML = '<div class="text-xs themed-text-tertiary">No saved themes</div>';
        return;
    }

    let html = '';
    Object.keys(appState.savedThemes).forEach(themeName => {
        const theme = appState.savedThemes[themeName];
        html += `
            <div class="flex items-center justify-between p-2 themed-bg-tertiary rounded text-xs">
                <div class="flex items-center gap-2">
                    <div class="w-4 h-4 rounded border" style="background: linear-gradient(45deg, ${theme.primary}, ${theme.background});"></div>
                    <span class="themed-text-primary">${themeName}</span>
                </div>
                <div class="flex gap-1">
                    <button onclick="loadCustomTheme('${themeName}')" class="themed-btn px-2 py-1 text-xs rounded">Load</button>
                    <button onclick="deleteCustomTheme('${themeName}')" class="themed-btn px-2 py-1 text-xs rounded" style="color: var(--error);">Del</button>
                </div>
            </div>
        `;
    });

    container.innerHTML = html;
}
```

```javascript
function updateThemePreview() {
    const primaryColor = document.getElementById('primaryColorPicker').value;
    const backgroundColor = document.getElementById('backgroundColorPicker').value;
    const textColor = document.getElementById('textColorPicker').value;

    const previewContainer = document.getElementById('themePreview');
    const previewButton = document.getElementById('previewButton');
    const previewMessage = document.getElementById('previewMessage');

    if (previewContainer && previewButton && previewMessage) {
        previewContainer.style.backgroundColor = backgroundColor;
        previewContainer.style.color = textColor;

        previewButton.style.backgroundColor = primaryColor;
        previewButton.style.color = 'white';

        const themeColors = generateThemeColors(primaryColor, backgroundColor, textColor);
        previewMessage.style.backgroundColor = themeColors.bgSecondary;
        previewMessage.style.color = textColor;
        previewMessage.style.border = `1px solid ${themeColors.border}`;
    }
}
```

```javascript
function renderPresetThemes() {
    const container = document.getElementById('presetThemes');
    if (!container) return;

    const presetThemeData = {
        'dark': { name: '🌙 Dark', colors: ['#5D5CDE', '#0f172a', '#e2e8f0'] },
        'terminal': { name: '💻 Terminal', colors: ['#00ff00', '#000000', '#00ff00'] },
        'paper': { name: '📄 Paper', colors: ['#8b5a2b', '#fefefe', '#2d2d2d'] },
        'sakura': { name: '🌸 Sakura', colors: ['#ff6b9d', '#fff8fc', '#2d1b20'] },
        'ayu': { name: '🔥 Ayu', colors: ['#ffcc02', '#0b0b0b', '#ffcc02'] }
    };

    let html = '';
    Object.entries(presetThemeData).forEach(([themeKey, themeInfo]) => {
        const [primary, bg, text] = themeInfo.colors;
        html += `
            <button
                onclick="applyTheme('${themeKey}'); closeThemeModal();"
                class="flex items-center gap-2 p-2 themed-btn rounded text-xs transition-colors"
                title="Apply ${themeInfo.name} theme"
            >
                <div class="w-4 h-4 rounded border" style="background: linear-gradient(45deg, ${primary}, ${bg});"></div>
                <span>${themeInfo.name}</span>
            </button>
        `;
    });

    container.innerHTML = html;
}
```

## Modal wiring

```javascript
function openThemeModal() {
    const modal = document.getElementById('themeModal');

    if (currentTheme !== 'custom') {
        document.getElementById('primaryColorPicker').value = '#5D5CDE';
        document.getElementById('primaryColorHex').value = '#5D5CDE';
        document.getElementById('backgroundColorPicker').value = '#0f172a';
        document.getElementById('backgroundColorHex').value = '#0f172a';
        document.getElementById('textColorPicker').value = '#e2e8f0';
        document.getElementById('textColorHex').value = '#e2e8f0';
    }

    renderPresetThemes();
    renderSavedThemes();
    updateThemePreview();
    setupThemeEventListeners();

    modal.classList.remove('hidden');
}

function closeThemeModal() {
    document.getElementById('themeModal').classList.add('hidden');
}
```

```javascript
function setupThemeEventListeners() {
    const colorInputs = [
        { picker: 'primaryColorPicker', hex: 'primaryColorHex' },
        { picker: 'backgroundColorPicker', hex: 'backgroundColorHex' },
        { picker: 'textColorPicker', hex: 'textColorHex' }
    ];

    colorInputs.forEach(({ picker, hex }) => {
        const pickerEl = document.getElementById(picker);
        const hexEl = document.getElementById(hex);

        if (pickerEl && hexEl) {
            pickerEl.addEventListener('input', (e) => {
                hexEl.value = e.target.value;
                updateThemePreview();
            });

            hexEl.addEventListener('input', (e) => {
                if (/^#[0-9A-F]{6}$/i.test(e.target.value)) {
                    pickerEl.value = e.target.value;
                    updateThemePreview();
                }
            });
        }
    });
}
```

* Ensures picker and hex inputs stay synchronized and rerenders the preview as the user types.
* Presents built-in presets alongside saved themes so users can quickly revert or explore alternatives.
