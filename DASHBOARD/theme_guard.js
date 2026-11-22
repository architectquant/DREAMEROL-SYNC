const THEME_MARKER = "/*startDM*/";
const THEME_BLOCK = /\/\*startDM\*\/[\s\S]*?\/\*endDM\*\//g;

export function stripExternalThemeStyle(styleText) {
    if (typeof styleText !== "string") return "";
    if (!styleText.includes(THEME_MARKER)) return styleText;
    return styleText.replace(THEME_BLOCK, "").trim();
}

export function installThemeGuard() {
    if (typeof document === "undefined" || typeof MutationObserver === "undefined") return null;

    const root = document.documentElement;
    if (!root) return null;

    const forcedColors =
        typeof window !== "undefined" &&
        typeof window.matchMedia === "function" &&
        window.matchMedia("(forced-colors: active)").matches;
    if (forcedColors) {
        root.dataset.themeGuard = "off";
        return null;
    }

    const observerOptions = {
        attributes: true,
        attributeFilter: ["style"],
        childList: true,
        subtree: true,
    };
    let cleaned = 0;
    let scheduled = false;
    let observer = null;

    function clean() {
        if (observer) observer.disconnect();

        const elements = new Set([root, document.body, ...document.querySelectorAll('[style*="startDM"]')]);
        for (const element of elements) {
            if (!element || typeof element.getAttribute !== "function") continue;
            const style = element.getAttribute("style");
            if (!style || !style.includes(THEME_MARKER)) continue;
            const next = stripExternalThemeStyle(style);
            if (next === style) continue;
            if (next) element.setAttribute("style", next);
            else element.removeAttribute("style");
            cleaned += 1;
        }

        root.dataset.themeGuard = "on";
        root.dataset.themeGuardCleaned = String(cleaned);
        if (observer) observer.observe(root, observerOptions);
    }

    function schedule() {
        if (scheduled) return;
        scheduled = true;
        const run = () => {
            scheduled = false;
            clean();
        };
        if (typeof requestAnimationFrame === "function") requestAnimationFrame(run);
        else setTimeout(run, 0);
    }

    observer = new MutationObserver(schedule);
    clean();
    observer.observe(root, observerOptions);
    document.addEventListener("DOMContentLoaded", schedule, { once: true });
    window.addEventListener("load", schedule, { once: true });
    window.addEventListener("pageshow", schedule);

    return {
        get cleaned() {
            return cleaned;
        },
        observer,
    };
}

installThemeGuard();
