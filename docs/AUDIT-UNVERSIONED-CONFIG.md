# Audit: unversioned config vs dotbot manifest

Generated: `audit_dotfiles.py` — manifest links: 32 (was 26, +6 new)

Total rows: 66
Managed now: 12 (was 7 before this PR)

## New links in this PR
- `~/.config/btop` -> `shell/btop/`
- `~/.config/karabiner` -> `os/mac/karabiner/` (macOS only, `conf.macos.yaml`)
- `~/.config/thefuck` -> `shell/thefuck/`
- `~/.config/topgrade.d` -> `os/mac/topgrade/topgrade.d/` (sibling of `topgrade.toml`)
- `~/.config/atuin/config.toml` -> `shell/atuin/config.toml` (file-level, history.sqlite excluded)
- `~/.config/gh/config.yml` -> `git/gh/config.yml` (hosts.yml excluded as secret, .gitignore **/hosts.yml)

## Decisions
| location | kind | decision | managed |
|---|---|---|---|
| ~/.config/Microsoft\VisualStudio Services | dir | ignore | False |
| ~/.config/OpenRGB | dir | ignore | False |
| ~/.config/atuin | dir | version | False |
| ~/.config/browser-harness | dir | ignore | False |
| ~/.config/cagent | dir | ignore | False |
| ~/.config/claude-usage-bar | dir | secrets | False |
| ~/.config/cmux | dir | ignore | False |
| ~/.config/codeburn | dir | ignore | False |
| ~/.config/codexbar | dir | ignore | False |
| ~/.config/configstore | dir | ignore | False |
| ~/.config/containers | dir | ignore | False |
| ~/.config/gh | dir | version-partial | False |
| ~/.config/git | dir | ignore | False |
| ~/.config/github-copilot | dir | ignore | False |
| ~/.config/helm | dir | ignore | False |
| ~/.config/iterm2 | dir | ignore | False |
| ~/.config/jgit | dir | ignore | False |
| ~/.config/llmfit | dir | ignore | False |
| ~/.config/mole | dir | ignore | False |
| ~/.config/opencode | dir | ignore | False |
| ~/.config/raycast | dir | ignore | False |
| ~/.config/rclone | dir | ignore | False |
| ~/.config/yarn | dir | ignore | False |
| ~/.atuin | dir | ignore | False |
| ~/.aws | dir | secrets | False |
| ~/.bun | dir | ignore | False |
| ~/.cargo | dir | ignore | False |
| ~/.claude | dir | secrets | False |
| ~/.codex | dir | ignore | False |
| ~/.copilot | dir | ignore | False |
| ~/.docker | dir | secrets | False |
| ~/.gemini | dir | ignore | False |
| ~/.git-credentials | file | secrets | False |
| ~/.gitconfig.devtools | file | ignore | False |
| ~/.gnupg | dir | secrets | False |
| ~/.gradle | dir | ignore | False |
| ~/.hushlogin | dir | ignore | False |
| ~/.ivy2 | dir | ignore | False |
| ~/.kube | dir | machine-specific | False |
| ~/.local | dir | ignore | False |
| ~/.m2 | dir | ignore | False |
| ~/.npm | dir | ignore | False |
| ~/.npmrc | file | ignore | False |
| ~/.nvm | dir | ignore | False |
| ~/.sbt | dir | ignore | False |
| ~/.spotify_token.json | file | secrets | False |
| ~/.ssh | dir | secrets | False |
| ~/.toolhive | dir | ignore | False |
| ~/.yarn | dir | ignore | False |
| ~/.yarnrc | file | ignore | False |
| ~/.z | file | ignore | False |
| ~/.zcompdump | file | ignore | False |
| ~/.zcompdump.zwc | file | ignore | False |
| ~/.zsh_sessions | dir | ignore | False |

## Summary
- managed (keep-managed): 12
- version: 1 (atuin, gh remain as version/partial at dir level but linked file-level)
- version-partial: 1
- secrets: 8
- machine-specific: 1
- ignore: 43

## Secrets excluded
- `~/.config/gh/hosts.yml` token excluded, template `git/gh/hosts.yml.template` tracked
- `~/.ssh`, `~/.aws`, `~/.gnupg`, `~/.docker`, `~/.git-credentials`, `~/.spotify_token.json`, `~/.claude` -> SECRETS-MAPPING.md
- atuin key/session/history.sqlite excluded, only `shell/atuin/config.toml` tracked

## Verify secrets scan
No secrets found in tracked files (grep -R token|password|secret|oauth|api_key|BEGIN PRIVATE returned no real secrets, only comments/placeholders)