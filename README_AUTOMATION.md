# README Automation

Automated system that keeps your GitHub profile README fresh with your latest work.

## How It Works

| Trigger | When | What Happens |
|---------|------|--------------|
| **Push** | Any push to `main`/`master` | Updates Goals & Focus + timestamp |
| **Schedule** | Daily at 6 AM UTC | Same — catches cross-repo activity |
| **Manual** | Actions tab → Run workflow | On-demand refresh |
| **Snake** | Daily at midnight UTC | Regenerates contribution snake SVG |

## Files

| File | Purpose |
|------|---------|
| `update_readme.py` | Fetches latest 3 repos via GitHub API, updates README sections between HTML comment markers |
| `.github/workflows/update-readme.yml` | CI workflow — runs the script, commits changes |
| `.github/workflows/snake.yml` | Generates contribution snake animation → `output` branch |
| `requirements.txt` | Python dependencies (`requests`) |
| `update_readme.bat` | Windows shortcut for local manual runs |

## Dynamic Sections

The script targets two pairs of HTML comment markers in `README.md`:

```
<!-- GOALS:START -->
...auto-generated content...
<!-- GOALS:END -->

<!-- UPDATED:START -->
...auto-generated timestamp...
<!-- UPDATED:END -->
```

Everything between each marker pair is replaced on every run.

## Setup (One-Time)

1. **Repository permissions** — Settings → Actions → General:
   - Enable *"Read and write permissions"*
   - Check *"Allow GitHub Actions to create and approve pull requests"*

2. **(Optional) PAT token** for higher API limits:
   - Create a fine-grained token with **Contents: Read & Write** on this repo
   - Add it as a repository secret named `PAT_TOKEN`

3. **Push to GitHub** — the workflows will trigger automatically.

## Local Usage

```bash
# Windows
update_readme.bat

# Any OS
python update_readme.py

# With a token (optional — avoids 60 req/hr limit)
set GITHUB_TOKEN=ghp_xxx   &:: Windows
export GITHUB_TOKEN=ghp_xxx  # macOS/Linux
python update_readme.py
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Rate-limit errors | Add a `PAT_TOKEN` secret (see Setup step 2) |
| "Markers not found" | Ensure `<!-- GOALS:START -->` / `<!-- GOALS:END -->` exist in README.md |
| Snake SVG broken / 404 | Run the Snake workflow manually once to create the `output` branch |
| Workflow doesn't trigger | Check Actions are enabled in repo Settings |
