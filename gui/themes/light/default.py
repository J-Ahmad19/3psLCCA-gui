"""
gui/themes/light/default.py — Default light theme (Bootstrap 5 tokens).

This is the original built-in light theme.
"""
from PySide6.QtGui import QPalette, QColor
from gui.theme import (
    PRIMARY, PRIMARY_HOVER, PRIMARY_ACTIVE,
    WHITE, BODY_BG, BODY_COLOR, SECONDARY,
    BORDER, BORDER_SUBTLE, MUTED, SURFACE, SURFACE_ACTIVE,
)

NAME = "Default Light"

# ── Palette ─────────────────────────────────────────────────────────────────
palette = QPalette()

palette.setColor(QPalette.Accent,          QColor(PRIMARY))
palette.setColor(QPalette.Window,          QColor(BODY_BG))
palette.setColor(QPalette.AlternateBase,   QColor(WHITE))
palette.setColor(QPalette.Base,            QColor(WHITE))
palette.setColor(QPalette.Button,          QColor(WHITE))
palette.setColor(QPalette.Mid,             QColor(BORDER_SUBTLE))
palette.setColor(QPalette.Light,           QColor(BORDER))
palette.setColor(QPalette.Highlight,       QColor(PRIMARY))
palette.setColor(QPalette.HighlightedText, QColor("#000000"))
palette.setColor(QPalette.Text,            QColor(BODY_COLOR))
palette.setColor(QPalette.WindowText,      QColor(BODY_COLOR))
palette.setColor(QPalette.ButtonText,      QColor(BODY_COLOR))
palette.setColor(QPalette.PlaceholderText, QColor(SECONDARY))

# ── QSS tokens ──────────────────────────────────────────────────────────────
QSS_TOKENS: dict[str, str] = {
    "$primary-hover":  PRIMARY_HOVER,
    "$primary-active": PRIMARY_ACTIVE,
    "$border-subtle":  BORDER_SUBTLE,
    "$surface-active": SURFACE_ACTIVE,
    "$body-color":     BODY_COLOR,
    "$secondary":      SECONDARY,
    "$primary":        PRIMARY,
    "$body-bg":        BODY_BG,
    "$border":         BORDER,
    "$surface":        SURFACE,
    "$muted":          MUTED,
    "$white":          WHITE,
}
