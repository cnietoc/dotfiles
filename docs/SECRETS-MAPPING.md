# Secrets mapping (Bitwarden)

Secrets are never stored in plaintext. They are loaded on demand from Bitwarden CLI (`load_secrets <scope>` / `bw get ...`).

| Location | Bitwarden item | Env vars / notes |
|---|---|---|
| `~/.config/gh/hosts.yml` (GitHub token) | `github-cli` (placeholder) | `gh auth login` or `gh auth token`; token stored in Bitwarden, not in repo. |
| `~/.aws/*` (AWS credentials/SSO) | `aws` (placeholder) | `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` via `aws sso login` |
| `~/.ssh/id_*` (SSH private keys) | `ssh-keys` (placeholder) | Never commit; permissions 600. Restore manually or via Bitwarden Secure Note |
| `~/.gnupg/*` | `gnupg` (placeholder) | Never commit |
| `~/.docker/config.json` (registry auths) | `docker-config` (placeholder) | `auths` section stripped; use `docker login` |
| `~/.git-credentials` | `git-credentials` (placeholder) | `credential.helper` cache; prefer `gh auth` |
| `~/.spotify_token.json` | `spotify` (via `load_secrets spotify`) | `SPOTIFY_CLIENT_ID` / `SPOTIFY_CLIENT_SECRET` |
| `~/.claude/.credentials.json` + `~/.config/claude-usage-bar/credentials.json` | `claude-code` (placeholder) | OAuth tokens; use `claude login` |
| `~/.config/atuin/key` + `session` | `hub.atuin.sh` (existing) | `ATUIN_USERNAME` / `ATUIN_PASSWORD` via `load_secrets atuin` |
| `~/.kube/config` (certs/tokens) | `kube-contexts` (placeholder) | Per-cluster; version only `kube/config.template` stripped |

Add real Bitwarden item names by replacing `(placeholder)` entries.
