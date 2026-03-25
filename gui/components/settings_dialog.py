"""
gui/components/settings_dialog.py

SettingsPanel  — reusable form widget (name + theme pickers).
                 Embedded by both SettingsDialog and FirstLaunchDialog.

SettingsDialog — sidebar gear-button dialog (Save / Cancel).
"""

import core.start_manager as sm
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)
from gui.themes import (
    list_themes,
    get_theme_name,
    set_active_theme,
    set_appearance_mode,
    reapply,
)
import gui.themes as _themes


# ── Shared form panel ─────────────────────────────────────────────────────────


class SettingsPanel(QWidget):
    """
    The shared settings form — display name + light/dark theme pickers.
    Contains no buttons or title; embed this inside any dialog.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # ── Display Name ──────────────────────────────────────────────────
        layout.addWidget(QLabel("<b>Display Name</b>"))

        self._name_edit = QLineEdit()
        self._name_edit.setPlaceholderText("Enter your name…")
        self._name_edit.setFixedHeight(34)
        self._name_edit.setText(sm.get_profile().get("display_name", ""))
        self._name_edit.textChanged.connect(
            lambda: (
                self._name_edit.setStyleSheet("")
                if self._name_edit.text().strip()
                else None
            )
        )
        layout.addWidget(self._name_edit)

        layout.addSpacing(4)

        # ── Appearance Mode ───────────────────────────────────────────────
        layout.addWidget(QLabel("<b>Appearance Mode</b>"))

        self._mode_combo = QComboBox()
        self._mode_combo.setFixedHeight(34)
        for value, label in [
            ("auto", "Auto (follow OS)"),
            ("light", "Light"),
            ("dark", "Dark"),
        ]:
            self._mode_combo.addItem(label, userData=value)
            if value == _themes.APPEARANCE_MODE:
                self._mode_combo.setCurrentIndex(self._mode_combo.count() - 1)
        layout.addWidget(self._mode_combo)

        layout.addSpacing(4)

        # ── Light Theme ───────────────────────────────────────────────────
        layout.addWidget(QLabel("<b>Light Theme</b>"))

        self._light_combo = self._theme_combo("light", _themes.ACTIVE_LIGHT)
        layout.addWidget(self._light_combo)

        layout.addSpacing(4)

        # ── Dark Theme ────────────────────────────────────────────────────
        layout.addWidget(QLabel("<b>Dark Theme</b>"))

        self._dark_combo = self._theme_combo("dark", _themes.ACTIVE_DARK)
        layout.addWidget(self._dark_combo)

        theme_hint = QLabel("Theme changes apply immediately on save.")
        theme_hint.setEnabled(False)
        layout.addWidget(theme_hint)

    # ── Public API ────────────────────────────────────────────────────────────

    def get_name(self) -> str:
        return self._name_edit.text().strip()

    def save(self) -> None:
        """Persist name + theme choices; re-applies theme live if anything changed."""
        sm.set_name(self.get_name())

        mode = self._mode_combo.currentData()
        light_mod = self._light_combo.currentData()
        dark_mod = self._dark_combo.currentData()

        changed = (
            mode != _themes.APPEARANCE_MODE
            or light_mod != _themes.ACTIVE_LIGHT
            or dark_mod != _themes.ACTIVE_DARK
        )

        set_appearance_mode(mode)
        set_active_theme("light", light_mod)
        set_active_theme("dark", dark_mod)

        if changed:
            reapply()

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _theme_combo(self, variant: str, current: str) -> QComboBox:
        combo = QComboBox()
        combo.setFixedHeight(34)
        for module_name in list_themes(variant):
            combo.addItem(get_theme_name(variant, module_name), userData=module_name)
            if module_name == current:
                combo.setCurrentIndex(combo.count() - 1)
        return combo


# ── Settings dialog (sidebar gear button) ─────────────────────────────────────


class SettingsDialog(QDialog):
    """
    Settings dialog opened from the sidebar gear button.
    Framing: plain title bar + Save / Cancel.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedWidth(420)
        self.setModal(True)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(24, 24, 24, 24)

        self._panel = SettingsPanel(self)
        layout.addWidget(self._panel)

        layout.addSpacing(8)

        # ── Buttons ───────────────────────────────────────────────────────
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self._on_accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def _on_accept(self):
        self._panel.save()
        self.accept()
