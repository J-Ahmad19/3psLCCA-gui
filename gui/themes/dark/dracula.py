"""
gui/themes/dark/dracula.py — Dracula dark theme.

Dracula palette reference: https://draculatheme.com/contribute
    Background  #282a36   Current Line  #44475a   Foreground  #f8f8f2
    Comment     #6272a4   Cyan          #8be9fd   Green       #50fa7b
    Orange      #ffb86c   Pink          #ff79c6   Purple      #bd93f9
    Red         #ff5555   Yellow        #f1fa8c

Brand tokens (PRIMARY / PRIMARY_HOVER / PRIMARY_ACTIVE) are preserved so
buttons and accents stay on-brand while the chrome uses Dracula's palette.
"""
from PySide6.QtGui import QPalette, QColor
from gui.theme import PRIMARY, PRIMARY_HOVER, PRIMARY_ACTIVE

NAME = "Dracula"

# ── Dracula base palette ────────────────────────────────────────────────────
_BG       = "#282a36"   # main window background
_SURFACE  = "#383a4a"   # hover surface (between bg and current-line)
_CURRENT  = "#44475a"   # current-line / button / border
_ELEVATED = "#21222c"   # inputs, cards  (darker than bg — creates depth)
_FG       = "#f8f8f2"   # primary text
_COMMENT  = "#6272a4"   # muted / secondary / placeholder
_PURPLE   = "#bd93f9"   # selection highlight
_ACCENT   = "#6B7D20"   # brand olive-green accent (kept for consistency)

# ── Palette ─────────────────────────────────────────────────────────────────
palette = QPalette()

palette.setColor(QPalette.Accent,          QColor(_ACCENT))
palette.setColor(QPalette.Window,          QColor(_BG))
palette.setColor(QPalette.AlternateBase,   QColor(_ELEVATED))
palette.setColor(QPalette.Base,            QColor(_ELEVATED))
palette.setColor(QPalette.Button,          QColor(_CURRENT))
palette.setColor(QPalette.Mid,             QColor(_CURRENT))
palette.setColor(QPalette.Midlight,        QColor("#565869"))
palette.setColor(QPalette.Light,           QColor("#565869"))
palette.setColor(QPalette.Highlight,       QColor(_PURPLE))
palette.setColor(QPalette.HighlightedText, QColor(_BG))
palette.setColor(QPalette.Text,            QColor(_FG))
palette.setColor(QPalette.WindowText,      QColor(_FG))
palette.setColor(QPalette.ButtonText,      QColor(_FG))
palette.setColor(QPalette.PlaceholderText, QColor(_COMMENT))

# ── QSS tokens ──────────────────────────────────────────────────────────────
QSS_TOKENS: dict[str, str] = {
    "$primary-hover":  PRIMARY_HOVER,
    "$primary-active": PRIMARY_ACTIVE,
    "$border-subtle":  "#565869",
    "$surface-active": _CURRENT,
    "$body-color":     _FG,
    "$secondary":      _COMMENT,
    "$primary":        PRIMARY,
    "$body-bg":        _BG,
    "$border":         _CURRENT,
    "$surface":        _SURFACE,
    "$muted":          "#4d5068",
    "$white":          _ELEVATED,   # elevated surface (inputs, cards, tables)
}
