# Audit: unversioned config vs dotbot manifest

Generated: `audit_dotfiles.py` — manifest links: 26

Total rows: 66

## Decisions
| location | kind | size_kb | decision |
|---|---|---|---|
| ~/.config/Microsoft\VisualStudio Services | dir | 719 | ignore |
| ~/.config/OpenRGB | dir | 66 | ignore |
| ~/.config/atuin | dir | 14 | version |
| ~/.config/browser-harness | dir | 98 | ignore |
| ~/.config/btop | dir | 9 | version |
| ~/.config/cagent | dir | 0 | ignore |
| ~/.config/claude-usage-bar | dir | 0 | secrets |
| ~/.config/cmux | dir | 14 | ignore |
| ~/.config/codeburn | dir | 2 | ignore |
| ~/.config/codexbar | dir | 4 | ignore |
| ~/.config/configstore | dir | 0 | ignore |
| ~/.config/containers | dir | 0 | ignore |
| ~/.config/gh | dir | 0 | version-partial |
| ~/.config/git | dir | 0 | version |
| ~/.config/github-copilot | dir | 302003 | ignore |
| ~/.config/helm | dir | 0 | version |
| ~/.config/iterm2 | dir | 0 | version |
| ~/.config/jgit | dir | 2 | version |
| ~/.config/karabiner | dir | 11 | version |
| ~/.config/llmfit | dir | 76 | ignore |
| ~/.config/mole | dir | 1277 | ignore |
| ~/.config/opencode | dir | 53563 | ignore |
| ~/.config/raycast | dir | 340816 | ignore |
| ~/.config/rclone | dir | 0 | version |
| ~/.config/thefuck | dir | 0 | version |
| ~/.config/topgrade.d | dir | 0 | version |
| ~/.config/yarn | dir | 0 | version |
| ~/.atuin | dir |  | ignore |
| ~/.aws | dir |  | secrets |
| ~/.bun | dir |  | ignore |
| ~/.cargo | dir |  | ignore |
| ~/.claude | dir |  | secrets |
| ~/.codex | dir |  | ignore |
| ~/.copilot | dir |  | ignore |
| ~/.docker | dir |  | secrets |
| ~/.gemini | dir |  | ignore |
| ~/.git-credentials | file |  | secrets |
| ~/.gitconfig.devtools | file |  | ignore |
| ~/.gnupg | dir |  | secrets |
| ~/.gradle | dir |  | ignore |
| ~/.hushlogin | dir |  | ignore |
| ~/.ivy2 | dir |  | ignore |
| ~/.kube | dir |  | machine-specific |
| ~/.local | dir |  | ignore |
| ~/.m2 | dir |  | ignore |
| ~/.npm | dir |  | ignore |
| ~/.npmrc | file |  | ignore |
| ~/.nvm | dir |  | ignore |
| ~/.sbt | dir |  | ignore |
| ~/.spotify_token.json | file |  | secrets |
| ~/.ssh | dir |  | secrets |
| ~/.toolhive | dir |  | ignore |
| ~/.yarn | dir |  | ignore |
| ~/.yarnrc | file |  | ignore |
| ~/.z | file |  | ignore |
| ~/.zcompdump | file |  | ignore |
| ~/.zcompdump.zwc | file |  | ignore |
| ~/.zsh_sessions | dir |  | ignore |

## Summary
- version: 11
- version-partial: 1
- secrets: 8
- machine-specific: 1
- ignore: 37
- keep-managed: 8

## Next
Move version/version-partial configs into ~/.dotfiles/<topic>/ and add dotbot link: entries. Templates for machine-specific and secrets documented in SECRETS-MAPPING.md.