#!/usr/bin/env zsh

# Only run in real terminal sessions.
[[ -t 0 && -t 1 ]] || exit 0

# Skip inside JetBrains terminals.
[[ "${TERMINAL_EMULATOR:-}" == "JetBrains-JediTerm" || "${TERM_PROGRAM:-}" == "JetBrains-JediTerm" ]] && exit 0
[[ -n "${IDEA_INITIAL_DIRECTORY:-}" || -n "${JETBRAINS_IDE:-}" ]] && exit 0

# Skip in CI environments or if already shown.
[[ -z "${CI:-}" && -z "${FASTFETCH_SHOWN:-}" ]] || exit 0
export FASTFETCH_SHOWN=1

# Skip if fastfetch is not installed.
command -v fastfetch >/dev/null 2>&1 || exit 0

# Only show the logo if the terminal is wide enough to accommodate it without wrapping.
LOGO_MIN_COLS=80

# Minimum dimensions to show. If the terminal is too small, it may be better to show nothing than a broken logo or truncated information.
MIN_COLS=30
MIN_LINES=4

# Get terminal dimensions: zsh vars → stty fallback → hardcoded defaults.
term_cols=${COLUMNS:-0}
term_lines=${LINES:-0}
if ((term_cols <= 0 || term_lines <= 0)); then
  read term_lines term_cols < <(stty size </dev/tty 2>/dev/null)
  ((term_cols > 0)) || term_cols=80
  ((term_lines > 0)) || term_lines=24
fi

# Exit if terminal is too small.
((term_lines > MIN_LINES && term_cols > MIN_COLS)) || exit 0

# Center the output (logo is ~110 cols wide).
left_padding=$((($(tput cols) - 110) / 2))
((left_padding < 0)) && left_padding=0

if ((term_cols >= LOGO_MIN_COLS)); then
  fastfetch --logo-padding-left ${left_padding}
else
  fastfetch --logo-padding-left ${left_padding} --logo None
fi
