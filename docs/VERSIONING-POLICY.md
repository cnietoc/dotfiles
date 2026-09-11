# Versioning policy

- Never commit: private keys, tokens, cookies, `hosts.yml` with tokens, `~/.aws/credentials`, `~/.docker/config.json` auths, `~/.gnupg`, `~/.ssh/id_*`.
- Secrets go via Bitwarden: document mapping in `docs/SECRETS-MAPPING.md` (item name + env vars).
- Caches/logs/sockets ignored: `**/__pycache__/`, `**/node_modules/`, `**/.venv/`, `**/*.log`, `**/*.sock`, `~/.cache`, `~/.local/share`, `~/.zcompdump*`, `~/.Trash`.
- Machine-specific: version `*.template` + `*.example`, gitignore live file, restore via `dot` + manual copy.
- Each `version` move must add a dotbot `link:` entry and be verified with `dot bot --dry-run` before push.
