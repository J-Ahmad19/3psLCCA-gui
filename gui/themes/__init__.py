"""
gui/themes/__init__.py — Theme registry.

Directory layout
----------------
gui/themes/
    light/
        default.py      Bootstrap light  (built-in)
        soft_light.py   Catppuccin Latte (built-in)
        <custom>.py     drop any .py here to add your own light theme
    dark/
        default.py      Default dark     (built-in)
        dracula.py      Dracula          (built-in)
        <custom>.py     drop any .py here to add your own dark theme

Each theme module must export three names:
    NAME: str                   — human-readable display name
    palette: QPalette           — the Qt colour palette
    QSS_TOKENS: dict[str, str]  — token → hex map for main.qss substitution

Selecting active themes
-----------------------
Change via the Settings panel in the app sidebar (persisted to user prefs).
Fallback defaults are ACTIVE_LIGHT / ACTIVE_DARK below.
"""
from __future__ import annotations

import importlib
import os
import pkgutil
from pathlib import Path

from PySide6.QtGui import QPalette

# ── Fallback defaults (used if no user pref is saved) ────────────────────
ACTIVE_LIGHT:    str = "soft_light"  # built-in: "default" | "soft_light"
ACTIVE_DARK:     str = "dracula"     # built-in: "default" | "dracula"
APPEARANCE_MODE: str = "auto"        # "auto" | "light" | "dark"
# ──────────────────────────────────────────────────────────────────────────

_PKG = "gui.themes"
# Absolute path — works regardless of working directory (e.g. when a project is open)
_QSS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "gui", "assets", "themes", "main.qss",
)
_prefs_loaded = False
_current_is_dark: bool = False   # last-known resolved is_dark; set by track_mode()


def _ensure_prefs() -> None:
    """Load persisted theme choices from user prefs (once, lazily)."""
    global ACTIVE_LIGHT, ACTIVE_DARK, APPEARANCE_MODE, _prefs_loaded
    if _prefs_loaded:
        return
    _prefs_loaded = True
    try:
        import core.start_manager as sm
        v = sm.get_pref("active_light_theme")
        if v:
            ACTIVE_LIGHT = v
        v = sm.get_pref("active_dark_theme")
        if v:
            ACTIVE_DARK = v
        v = sm.get_pref("appearance_mode")
        if v in ("auto", "light", "dark"):
            APPEARANCE_MODE = v
    except Exception:
        pass


def _load(variant: str, name: str) -> tuple[QPalette, dict[str, str]]:
    """Import gui.themes.<variant>.<name> and return (palette, QSS_TOKENS)."""
    mod = importlib.import_module(f"{_PKG}.{variant}.{name}")
    return mod.palette, mod.QSS_TOKENS


def get_light_theme() -> tuple[QPalette, dict[str, str]]:
    """Return (palette, QSS_TOKENS) for the active light theme."""
    _ensure_prefs()
    return _load("light", ACTIVE_LIGHT)


def get_dark_theme() -> tuple[QPalette, dict[str, str]]:
    """Return (palette, QSS_TOKENS) for the active dark theme."""
    _ensure_prefs()
    return _load("dark", ACTIVE_DARK)


def set_active_theme(variant: str, name: str) -> None:
    """Set the active theme for 'light' or 'dark' and persist to user prefs."""
    global ACTIVE_LIGHT, ACTIVE_DARK
    if variant == "light":
        ACTIVE_LIGHT = name
    else:
        ACTIVE_DARK = name
    try:
        import core.start_manager as sm
        sm.set_pref(f"active_{variant}_theme", name)
    except Exception:
        pass


def set_appearance_mode(mode: str) -> None:
    """Set appearance mode: 'auto' | 'light' | 'dark'. Persists to user prefs."""
    global APPEARANCE_MODE
    if mode not in ("auto", "light", "dark"):
        return
    APPEARANCE_MODE = mode
    try:
        import core.start_manager as sm
        sm.set_pref("appearance_mode", mode)
    except Exception:
        pass


def resolve_is_dark(os_is_dark: bool) -> bool:
    """Return True if dark theme should be used, respecting APPEARANCE_MODE."""
    _ensure_prefs()
    if APPEARANCE_MODE == "dark":
        return True
    if APPEARANCE_MODE == "light":
        return False
    return os_is_dark  # "auto"


def track_mode(is_dark: bool) -> None:
    """Record the last-resolved is_dark state. Called by main._apply_theme()
    so reapply() always has a reliable baseline instead of guessing from palette."""
    global _current_is_dark
    _current_is_dark = is_dark


def reapply(app=None) -> None:
    """Re-apply the current active themes to the running QApplication."""
    from PySide6.QtWidgets import QApplication
    if app is None:
        app = QApplication.instance()
    if app is None:
        return
    # Use tracked state — don't read palette (it already reflects the last theme)
    is_dark = resolve_is_dark(_current_is_dark)
    track_mode(is_dark)   # keep state current for the next call
    palette, tokens = get_dark_theme() if is_dark else get_light_theme()

    app.setPalette(palette)

    if os.path.exists(_QSS_PATH):
        try:
            with open(_QSS_PATH) as f:
                qss = f.read()
            for token, value in tokens.items():
                qss = qss.replace(token, value)
            # Clear first — forces Qt to fully re-evaluate all style rules
            # on every existing widget, including window backgrounds.
            app.setStyleSheet("")
            app.setStyleSheet(qss)
        except Exception:
            pass

    # Force every top-level window (and its children) to repaint immediately.
    # Without this, palette(window) backgrounds stay stale until the next
    # resize/focus event.
    for w in app.topLevelWidgets():
        w.style().unpolish(w)
        w.style().polish(w)
        w.update()


def list_themes(variant: str) -> list[str]:
    """Return module names of all available themes for 'light' or 'dark'.
    Any .py dropped into the variant folder is automatically discovered."""
    pkg_dir = Path(__file__).parent / variant
    return sorted(
        name
        for _, name, is_pkg in pkgutil.iter_modules([str(pkg_dir)])
        if not is_pkg
    )


def get_theme_name(variant: str, module_name: str) -> str:
    """Return the human-readable NAME from a theme module."""
    mod = importlib.import_module(f"{_PKG}.{variant}.{module_name}")
    return getattr(mod, "NAME", module_name)
