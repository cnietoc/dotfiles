#!/usr/bin/env bash
set -euo pipefail

sudo apt-get update
sudo apt-get install -y \
  zsh git git-lfs curl wget unzip build-essential \
  bat eza fd-find ripgrep fzf jq \
  tmux neovim \
  shellcheck shfmt \
  python3 python3-pip python3-venv \
  pre-commit

# Tools not available via apt or with outdated versions
curl -sSf https://starship.rs/install.sh | sh -s -- -y
curl https://mise.run | sh

# Bitwarden CLI
npm install -g @bitwarden/cli 2>/dev/null || snap install bw

# atuin (shell history)
curl --proto '=https' --tlsv1.2 -sSf https://setup.atuin.sh | sh

# zoxide (smart cd)
curl -sSfL https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | sh

# lazygit
LAZYGIT_VERSION=$(curl -s "https://api.github.com/repos/jesseduffield/lazygit/releases/latest" | grep -Po '"tag_name": "v\K[^"]*')
curl -Lo lazygit.tar.gz "https://github.com/jesseduffield/lazygit/releases/download/v${LAZYGIT_VERSION}/lazygit_${LAZYGIT_VERSION}_Linux_x86_64.tar.gz"
tar xf lazygit.tar.gz lazygit
sudo install lazygit /usr/local/bin
rm lazygit lazygit.tar.gz

# git-delta
DELTA_VERSION=$(curl -s "https://api.github.com/repos/dandavison/delta/releases/latest" | grep -Po '"tag_name": "\K[^"]*')
curl -Lo delta.deb "https://github.com/dandavison/delta/releases/download/${DELTA_VERSION}/git-delta_${DELTA_VERSION}_amd64.deb"
sudo dpkg -i delta.deb && rm delta.deb
