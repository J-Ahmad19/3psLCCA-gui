"""
gui/themes/dark/default.py — Default dark theme.

This is the original built-in dark theme.
"""
from PySide6.QtGui import QPalette, QColor
from gui.theme import PRIMARY, PRIMARY_HOVER, PRIMARY_ACTIVE

NAME = "Default Dark"

_ACCENT = "#6B7D20"   # desaturated brand green for dark-mode accent

# ── Palette ─────────────────────────────────────────────────────────────────
palette = QPalette()

palette.setColor(QPalette.Accent,          QColor(_ACCENT))
palette.setColor(QPalette.Window,          QColor("#282828"))
palette.setColor(QPalette.AlternateBase,   QColor("#333333"))
palette.setColor(QPalette.Base,            QColor("#3a3a3a"))
palette.setColor(QPalette.Button,          QColor("#3a3a3a"))
palette.setColor(QPalette.Mid,             QColor("#505050"))
palette.setColor(QPalette.Midlight,        QColor("#484848"))
palette.setColor(QPalette.Light,           QColor("#555555"))
palette.setColor(QPalette.Highlight,       QColor(_ACCENT))
palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
palette.setColor(QPalette.Text,            QColor("#e2e2e2"))
palette.setColor(QPalette.WindowText,      QColor("#e2e2e2"))
palette.setColor(QPalette.ButtonText,      QColor("#e2e2e2"))
palette.setColor(QPalette.PlaceholderText, QColor("#888888"))

# ── QSS tokens ──────────────────────────────────────────────────────────────
QSS_TOKENS: dict[str, str] = {
    "$primary-hover":  PRIMARY_HOVER,
    "$primary-active": PRIMARY_ACTIVE,
    "$border-subtle":  "#5a5a5a",
    "$surface-active": "#525252",
    "$body-color":     "#e2e2e2",
    "$secondary":      "#a0a0a0",
    "$primary":        PRIMARY,
    "$body-bg":        "#282828",
    "$border":         "#505050",
    "$surface":        "#4a4a4a",
    "$muted":          "#686868",
    "$white":          "#3a3a3a",   # elevated surface (inputs, cards, tables)
}
