"""
gui/themes/light/soft_light.py — Soft light theme based on Catppuccin Latte.

Designed to reduce eye fatigue: warm background, ~8:1 text contrast (vs ~15:1
for the Bootstrap default), warm purple-grey text instead of near-black.

Catppuccin Latte reference: https://github.com/catppuccin/catppuccin
    Base      #eff1f5   Mantle    #e6e9ef   Crust     #dce0e8
    Surface0  #ccd0da   Surface1  #bcc0cc   Overlay0  #9ca0b0
    Subtext0  #6c6f85   Text      #4c4f69
"""
from PySide6.QtGui import QPalette, QColor
from gui.theme import PRIMARY, PRIMARY_HOVER, PRIMARY_ACTIVE

NAME = "Soft Light"

# ── Catppuccin Latte palette ─────────────────────────────────────────────────
_BASE     = "#eff1f5"   # main window / app background
_MANTLE   = "#e6e9ef"   # sidebar / alternate background (slightly darker)
_CRUST    = "#dce0e8"   # pressed surface / darkest bg layer
_SURFACE0 = "#ccd0da"   # standard border
_SURFACE1 = "#bcc0cc"   # subtle border (inputs on hover)
_OVERLAY0 = "#9ca0b0"   # disabled / placeholder
_SUBTEXT0 = "#6c6f85"   # secondary / muted text
_TEXT     = "#4c4f69"   # primary text  (~8:1 on white — soft, still WCAG AA)
_WHITE    = "#ffffff"   # inputs, cards, tables  (elevated above _BASE)

# ── Palette ─────────────────────────────────────────────────────────────────
palette = QPalette()

palette.setColor(QPalette.Accent,          QColor(PRIMARY))
palette.setColor(QPalette.Window,          QColor(_BASE))
palette.setColor(QPalette.AlternateBase,   QColor(_MANTLE))
palette.setColor(QPalette.Base,            QColor(_WHITE))
palette.setColor(QPalette.Button,          QColor(_WHITE))
palette.setColor(QPalette.Mid,             QColor(_SURFACE0))
palette.setColor(QPalette.Midlight,        QColor(_SURFACE1))
palette.setColor(QPalette.Light,           QColor(_CRUST))
palette.setColor(QPalette.Highlight,       QColor(PRIMARY))
palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
palette.setColor(QPalette.Text,            QColor(_TEXT))
palette.setColor(QPalette.WindowText,      QColor(_TEXT))
palette.setColor(QPalette.ButtonText,      QColor(_TEXT))
palette.setColor(QPalette.PlaceholderText, QColor(_OVERLAY0))

# ── QSS tokens ──────────────────────────────────────────────────────────────
QSS_TOKENS: dict[str, str] = {
    "$primary-hover":  PRIMARY_HOVER,
    "$primary-active": PRIMARY_ACTIVE,
    "$border-subtle":  _SURFACE1,
    "$surface-active": _CRUST,
    "$body-color":     _TEXT,
    "$secondary":      _SUBTEXT0,
    "$primary":        PRIMARY,
    "$body-bg":        _BASE,
    "$border":         _SURFACE0,
    "$surface":        _CRUST,
    "$muted":          _OVERLAY0,
    "$white":          _WHITE,
}
