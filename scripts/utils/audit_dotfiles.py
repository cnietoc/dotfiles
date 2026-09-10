#!/usr/bin/env python3
"""Audit unversioned config vs dotbot manifest. Read-only; writes CSV + markdown."""
import csv, json, os, pathlib, re, sys

HOME = pathlib.Path.home()
DOTFILES = HOME / ".dotfiles"
MANIFESTS = [DOTFILES / "symlinks/conf.yaml", DOTFILES / "symlinks/conf.macos.yaml", DOTFILES / "symlinks/conf.linux.yaml"]
CONFIG_DIR = HOME / ".config"

# Parse dotbot manifests naively: collect every "  ~/.xxx: ..." and "~/.config/yyy" target
LINK_RE = re.compile(r"^\s*~/(.+?):\s*(.+)$")

def load_manifest_links():
    links = set()
    for mf in MANIFESTS:
        if not mf.exists():
            continue
        for line in mf.read_text().splitlines():
            m = LINK_RE.match(line)
            if m:
                # normalize ~/path
                links.add(f"~/{m.group(1).strip()}")
    return links

def is_symlink_to_dotfiles(p: pathlib.Path) -> bool:
    try:
        return p.is_symlink() and ".dotfiles" in os.readlink(p)
    except OSError:
        return False

def inventory():
    manifest_links = load_manifest_links()
    rows = []
    # 1) ~/.config entries
    if CONFIG_DIR.exists():
        for name in sorted(os.listdir(CONFIG_DIR)):
            p = CONFIG_DIR / name
            is_link = p.is_symlink()
            target = os.readlink(p) if is_link else ""
            managed = f"~/.config/{name}" in manifest_links or is_symlink_to_dotfiles(p)
            size_kb = 0
            if not is_link and p.is_dir():
                try:
                    size_kb = sum(f.stat().st_size for f in p.rglob("*") if f.is_file()) // 1024
                except OSError:
                    size_kb = -1
            rows.append({
                "location": f"~/.config/{name}",
                "kind": "symlink->dotfiles" if is_symlink_to_dotfiles(p) else ("symlink" if is_link else ("dir" if p.is_dir() else "file")),
                "managed": managed,
                "target": target,
                "size_kb": size_kb,
                "suggested_action": "keep-managed" if managed else "triage",
            })
    # 2) ~/ dotfiles/dirs (curated list, extend as needed)
    home_candidates = [
        ".ssh", ".aws", ".kube", ".gnupg", ".docker", ".claude", ".codex", ".copilot",
        ".gemini", ".local", ".toolhive", ".npm", ".npmrc", ".yarn", ".yarnrc",
        ".cargo", ".nvm", ".bun", ".gradle", ".m2", ".ivy2", ".sbt", ".atuin",
        ".z", ".git-credentials", ".gitconfig.devtools", ".spotify_token.json",
        ".zcompdump", ".zcompdump.zwc", ".zsh_sessions", ".hushlogin",
        ".config/btop", ".config/karabiner", ".config/gh", ".config/atuin",
        ".config/raycast", ".config/opencode", ".config/mole", ".config/btop",
    ]
    for rel in sorted(set(home_candidates)):
        p = HOME / rel
        if not p.exists() and not p.is_symlink():
            continue
        key = f"~/{rel}"
        is_link = p.is_symlink()
        managed = key in manifest_links or is_symlink_to_dotfiles(p)
        rows.append({
            "location": key,
            "kind": "symlink->dotfiles" if is_symlink_to_dotfiles(p) else ("symlink" if is_link else ("dir" if p.is_dir() else "file")),
            "managed": managed,
            "target": os.readlink(p) if is_link else "",
            "size_kb": "",
            "suggested_action": "keep-managed" if managed else "triage",
        })
    return rows, manifest_links

def main():
    rows, manifest_links = inventory()
    out_csv = DOTFILES / "docs" / "audit-unversioned-config.csv"
    out_md = DOTFILES / "docs" / "AUDIT-UNVERSIONED-CONFIG.md"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["location","kind","managed","target","size_kb","suggested_action"])
        w.writeheader()
        w.writerows(rows)
    unmanaged = [r for r in rows if not r["managed"] and r["suggested_action"]=="triage"]
    md = ["# Audit: unversioned config vs dotbot manifest", "",
          f"Generated: `audit_dotfiles.py` — manifest links: {len(manifest_links)}", "",
          f"Unmanaged candidates: {len(unmanaged)}", "",
          "| location | kind | size_kb | target |",
          "|---|---|---|---|"]
    for r in unmanaged:
        md.append(f"| {r['location']} | {r['kind']} | {r['size_kb']} | {r['target']} |")
    md += ["", "## Next", "Fill `suggested_action` per triage matrix (Phase 1) and move in batches (Phase 2)."]
    out_md.write_text("\n".join(md))
    print(f"Wrote {out_csv} ({len(rows)} rows)")
    print(f"Wrote {out_md}")
    print(f"Managed: {sum(1 for r in rows if r['managed'])} / {len(rows)}")

if __name__ == "__main__":
    main()
