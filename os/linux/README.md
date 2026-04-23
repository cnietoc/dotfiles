# Linux setup (Ubuntu/Debian + WSL2)

## Install

1. `sudo apt-get install -y git zsh`
2. `chsh -s $(which zsh)`
3. `git clone <repo> ~/.dotfiles`
4. `bash ~/.dotfiles/os/linux/apt/packages.sh`
5. `~/.dotfiles/bin/dotly install` (uses `symlinks/conf.linux.yaml`)
6. `bw login && bwu`
7. Restart shell.

## WSL2 tips

- Clipboard: `pbcopy` is aliased to `clip.exe` automatically.
- Docker Desktop on Windows exposes the Docker CLI inside WSL2.
- Windows paths are accessible at `/mnt/c/`.
