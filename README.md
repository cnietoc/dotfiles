# Carlos Nieto's dotfiles

Personal macOS (Apple Silicon) setup based on **dotly** + Zim + starship + dotbot.

## What's inside

- Brewfile with ~200 packages (CLI tools, casks, Mac App Store apps).
- Shell config: zsh + Zim + starship + Ghostty.
- AI tooling: Claude Code, Codex, Copilot CLI.
- Secrets via Bitwarden CLI lazy-load (`load_secrets <scope>`).
- K8s/Helm/Docker aliases, Azure/AKS tooling.

## First-time install on a new Mac

1. `xcode-select --install`
2. Install Homebrew: `https://brew.sh`
3. `git clone <repo> ~/.dotfiles && cd ~/.dotfiles`
4. `brew bundle --file=os/mac/brew/Brewfile`
5. `./bin/dotly install`
6. `bw login && bwu` (configure Bitwarden CLI)
7. `dot mac defaults import` (restore macOS preferences — if snapshot exists)
8. `dot atuin setup` (login to atuin history sync via Bitwarden)
9. `atuin import zsh` (import existing zsh history — skip if not the first machine)

## Platform support

- **macOS 14+ Apple Silicon** — primary, fully supported.
- **Ubuntu/Debian (headless server + WSL2)** — supported for shell + git + tmux + nvim + secrets. See `os/linux/README.md`.

macOS Intel is **not supported**.

## Layout

| Path | Purpose |
|---|---|
| `shell/` | zsh config, functions, aliases, exports |
| `git/` | `.gitconfig`, `.gitignore_global` |
| `os/mac/` | Brewfile, Ghostty, topgrade, macOS defaults snapshot |
| `os/linux/` | apt packages script, Linux-specific setup |
| `scripts/` | personal utility scripts |
| `editors/nvim/` | LazyVim starter config |
| `langs/mise/` | mise tool version config |
| `symlinks/` | dotbot YAML configs |
| `modules/` | dotly and Zim submodules |

## Secrets (Bitwarden)

Secrets are never stored in plaintext. They are loaded on demand from Bitwarden CLI.

```bash
bwu                        # unlock vault (required first)
load_secrets spotify        # loads SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET
load_secrets telegram       # loads TL_TELEGRAM_TOKEN / TL_TELEGRAM_CHAT_ID
load_secrets steam          # loads STEAM_API_KEY / STEAM_VANITY_URL
load_secrets notion         # loads NOTION_TOKEN / NOTION_DHCP_DATASOURCE
load_secrets router         # loads ROUTER_IP / ROUTER_USER / ROUTER_PASS
```

## Shell history sync (atuin)

History is synced across machines via [atuin](https://atuin.sh) with E2E encryption.
Credentials are stored in Bitwarden under the item `hub.atuin.sh`.
After setup, `Ctrl+R` opens atuin's history search instead of the default zsh reverse search.

## Updating

```bash
# Dump installed Homebrew packages
brew bundle dump --force --file=os/mac/brew/Brewfile

# Export macOS defaults snapshot
dot mac defaults export

# Update Zim modules
zimfw update
```
