"""Design tokens dos três temas visuais do Corvus PDF.

Cada tema é um dicionário de tokens semânticos. Os componentes de UI usam
apenas os nomes dos tokens — nunca valores HEX diretamente. O ThemeManager
consome esses dicionários e gera o QSS correspondente.

Paleta oficial definida pelo CTO (Corvus One / gptão) — não alterar valores
sem revisão arquitetural. Ajustes de contraste/acessibilidade devem preservar
a família de matiz e o papel semântico do token.
"""
from __future__ import annotations

# ─── CLEAN DARK (padrão) ──────────────────────────────────────────────────────
CLEAN_DARK: dict[str, str] = {
    # Surface
    "--bg-app":              "#121417",
    "--bg-sidebar":          "#181B20",
    "--bg-surface":          "#20242B",
    "--bg-surface-elevated": "#282D35",
    "--bg-input":            "#171A1F",
    # Text
    "--text-primary":        "#F1F3F5",
    "--text-secondary":      "#AAB2BD",
    "--text-muted":          "#727B87",
    "--text-on-accent":      "#FFFFFF",
    # Border
    "--border-subtle":       "#2B313A",
    "--border-default":      "#3A424E",
    "--border-focus":        "#4C8DFF",
    # Accent
    "--accent-primary":      "#3B82F6",
    "--accent-primary-hover":"#5A9BFF",
    "--accent-primary-active":"#2563EB",
    # Status
    "--color-success":       "#32B67A",
    "--color-warning":       "#E6A23C",
    "--color-error":         "#E05252",
    "--color-info":          "#4C8DFF",
    # Sidebar nav item
    "--nav-item-hover":      "#20242B",
    "--nav-item-active-bg":  "#1D2A3F",
    "--nav-item-active-fg":  "#3B82F6",
    "--nav-item-indicator":  "#3B82F6",
}

# ─── CLEAN LIGHT ─────────────────────────────────────────────────────────────
CLEAN_LIGHT: dict[str, str] = {
    "--bg-app":              "#F4F6F8",
    "--bg-sidebar":          "#FFFFFF",
    "--bg-surface":          "#FFFFFF",
    "--bg-surface-elevated": "#FFFFFF",
    "--bg-input":            "#F8FAFC",
    "--text-primary":        "#18212B",
    "--text-secondary":      "#52606D",
    "--text-muted":          "#7B8794",
    "--text-on-accent":      "#FFFFFF",
    "--border-subtle":       "#E3E8EE",
    "--border-default":      "#CBD5E1",
    "--border-focus":        "#3B82F6",
    "--accent-primary":      "#2563EB",
    "--accent-primary-hover":"#1D4ED8",
    "--accent-primary-active":"#1E40AF",
    "--color-success":       "#15803D",
    "--color-warning":       "#B45309",
    "--color-error":         "#DC2626",
    "--color-info":          "#2563EB",
    "--nav-item-hover":      "#F4F6F8",
    "--nav-item-active-bg":  "#EFF6FF",
    "--nav-item-active-fg":  "#2563EB",
    "--nav-item-indicator":  "#2563EB",
}

# ─── CORVUS NOIR (tema de personalidade GeralZona) ───────────────────────────
CORVUS_NOIR: dict[str, str] = {
    "--bg-app":              "#090B10",
    "--bg-sidebar":          "#0E1118",
    "--bg-surface":          "#141923",
    "--bg-surface-elevated": "#1B2230",
    "--bg-input":            "#0C1017",
    "--text-primary":        "#E8EDF5",
    "--text-secondary":      "#A9B4C4",
    "--text-muted":          "#667085",
    "--text-on-accent":      "#FFFFFF",
    "--border-subtle":       "#202938",
    "--border-default":      "#303C4F",
    "--border-focus":        "#00B8D9",
    "--accent-primary":      "#007CFF",
    "--accent-primary-hover":"#2997FF",
    "--accent-primary-active":"#0064D1",
    # Dourado — apenas para identidade/ações especiais
    "--accent-gold":         "#D6A84A",
    "--accent-gold-hover":   "#E5BC68",
    # Status
    "--color-success":       "#22C55E",
    "--color-warning":       "#F59E0B",
    "--color-error":         "#EF4444",
    "--color-info":          "#00B8D9",
    "--nav-item-hover":      "#141923",
    "--nav-item-active-bg":  "#0D1A2E",
    "--nav-item-active-fg":  "#2997FF",
    "--nav-item-indicator":  "#007CFF",
}

THEMES: dict[str, dict[str, str]] = {
    "Clean Dark":  CLEAN_DARK,
    "Light":       CLEAN_LIGHT,
    "Corvus Noir": CORVUS_NOIR,
}

THEME_ICONS: dict[str, str] = {
    "Clean Dark":  "◐",
    "Light":       "☀",
    "Corvus Noir": "☾",
}
