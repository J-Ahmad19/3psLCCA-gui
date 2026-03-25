"""
gui/themes/__init__.py — Theme registry.

Directory layout
----------------
gui/themes/
    light/
        default.yml     Bootstrap light  (built-in)
        soft_light.yml  Catppuccin Latte (built-in)
        <custom>.yml    drop any .yml here to add your own light theme
        <custom>.py     legacy .py themes still work as a fallback
    dark/
        default.yml     Default dark     (built-in)
        dracula.yml     Dracula          (built-in)
        <custom>.yml    drop any .yml here to add your own dark theme
        <custom>.py     legacy .py themes still work as a fallback

Each theme YAML must contain:
    name: str                        — human-readable display name
    palette: map[role, hex]          — QPalette role → hex colour
    qss_tokens: map[token, hex]      — token → hex map for main.qss substitution

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

import yaml
from PySide6.QtGui import QPalette, QColor

# ── Fallback defaults (used if no user pref is saved) ────────────────────
ACTIVE_LIGHT: str = "soft_light"  # built-in: "default" | "soft_light"
ACTIVE_DARK: str = "dracula"  # built-in: "default" | "dracula"
APPEARANCE_MODE: str = "auto"  # "auto" | "light" | "dark"
# ──────────────────────────────────────────────────────────────────────────

_PKG = "gui.themes"
_THEMES_DIR = Path(__file__).parent
# Absolute path — works regardless of working directory (e.g. when a project is open)
_QSS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "gui",
    "assets",
    "themes",
    "main.qss",
)
_prefs_loaded = False
_current_is_dark: bool = False  # last-known resolved is_dark; set by track_mode()

# ── QPalette role name → attribute map ───────────────────────────────────
_PALETTE_ROLES: dict[str, QPalette.ColorRole] = {
    "accent": QPalette.Accent,
    "window": QPalette.Window,
    "alternate_base": QPalette.AlternateBase,
    "base": QPalette.Base,
    "button": QPalette.Button,
    "mid": QPalette.Mid,
    "midlight": QPalette.Midlight,
    "light": QPalette.Light,
    "highlight": QPalette.Highlight,
    "highlighted_text": QPalette.HighlightedText,
    "text": QPalette.Text,
    "window_text": QPalette.WindowText,
    "button_text": QPalette.ButtonText,
    "placeholder_text": QPalette.PlaceholderText,
}


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


def _load_yaml_theme(path: Path) -> tuple[QPalette, dict[str, str]]:
    """Parse a .yml theme file and return (QPalette, QSS_TOKENS)."""
    with open(path) as f:
        data = yaml.safe_load(f)

    palette = QPalette()
    for role_name, hex_color in data.get("palette", {}).items():
        role = _PALETTE_ROLES.get(role_name)
        if role is not None:
            palette.setColor(role, QColor(hex_color))

    qss_tokens: dict[str, str] = data.get("qss_tokens", {})
    return palette, qss_tokens


def _load(variant: str, name: str) -> tuple[QPalette, dict[str, str]]:
    """Load a theme by variant ('light'|'dark') and name.

    Resolution order:
      1. <themes_dir>/<variant>/<name>.yml  — preferred declarative format
      2. gui.themes.<variant>.<name>        — legacy .py module fallback
    """
    yml_path = _THEMES_DIR / variant / f"{name}.yml"
    if yml_path.exists():
        return _load_yaml_theme(yml_path)

    # Legacy .py fallback — keeps any existing custom themes working
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
    track_mode(is_dark)  # keep state current for the next call
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
    """Return names of all available themes for 'light' or 'dark'.
    Discovers both .yml files and legacy .py modules in the variant folder."""
    pkg_dir = _THEMES_DIR / variant

    yml_names = {p.stem for p in pkg_dir.glob("*.yml")}
    py_names = {
        name for _, name, is_pkg in pkgutil.iter_modules([str(pkg_dir)]) if not is_pkg
    }
    return sorted(yml_names | py_names)


def get_theme_name(variant: str, module_name: str) -> str:
    """Return the human-readable name for a theme."""
    yml_path = _THEMES_DIR / variant / f"{module_name}.yml"
    if yml_path.exists():
        with open(yml_path) as f:
            data = yaml.safe_load(f)
        return data.get("name", module_name)

    # Legacy .py fallback
    mod = importlib.import_module(f"{_PKG}.{variant}.{module_name}")
    return getattr(mod, "NAME", module_name)
