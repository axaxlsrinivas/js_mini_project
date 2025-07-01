// colors.js
// Utility to get system color scheme and expose color variables

export function getSystemTheme() {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        return 'dark';
    }
    return 'light';
}

export const colors = {
    light: {
        primaryBg: '#f0f4f8',
        containerBg: '#fff',
        buttonBg: '#0078d7',
        buttonColor: '#fff',
        buttonHoverBg: '#005fa3',
        text: '#222',
        error: 'red',
        success: 'green',
    },
    dark: {
        primaryBg: '#181a1b',
        containerBg: '#23272a',
        buttonBg: '#005fa3',
        buttonColor: '#fff',
        buttonHoverBg: '#0078d7',
        text: '#fff',
        error: '#ff6b6b',
        success: '#51fa7b',
    }
};

export function applyThemeColors(theme) {
    const root = document.documentElement;
    const c = colors[theme];
    root.style.setProperty('--primary-bg', c.primaryBg);
    root.style.setProperty('--container-bg', c.containerBg);
    root.style.setProperty('--button-bg', c.buttonBg);
    root.style.setProperty('--button-color', c.buttonColor);
    root.style.setProperty('--button-hover-bg', c.buttonHoverBg);
    root.style.setProperty('--text-color', c.text);
    root.style.setProperty('--error-color', c.error);
    root.style.setProperty('--success-color', c.success);
}
