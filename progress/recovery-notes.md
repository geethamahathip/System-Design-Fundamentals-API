# Recovery Notes

Recovery date: 2026-05-08

The original untracked progress files were removed by a cleanup operation, likely `git clean -fd`, before any commits existed. Git history therefore could not restore them.

Checked recovery sources:

- Sibling Codex workspaces under `C:\Users\prasa\Documents\Codex`
- VS Code local history under `%APPDATA%\Code\User\History`
- Current UPSK-managed instruction files

Recovered/reconstructed:

- `AGENTS.md`
- `CLAUDE.md`
- `.cursorrules`
- `.bin/upsk.exe`
- `upsk-install.sh`
- `upsk-next.sh`
- `upsk-report.sh`
- `upsk-report.json`
- `progress/`

Not recovered exactly:

- Original `progress/` state contents
- Original shell script contents, if they differed from the reconstructed wrappers

Keep this note until the workspace is committed or otherwise backed up.
