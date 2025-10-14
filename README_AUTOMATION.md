# README Automation Setup

This repository automatically updates your README with your latest 3 public repositories.

## 📁 **Essential Files**

- `update_readme.py` - Main script that fetches and updates repositories
- `requirements.txt` - Python dependencies
- `.github/workflows/update-readme.yml` - GitHub Actions workflow
- `update_readme.bat` - Windows batch script for manual execution
- `PAT_SETUP_GUIDE.md` - Complete setup instructions

## 🚀 **How It Works**

- **Instant updates** when you create or modify repositories
- **Daily backup** at 6 AM UTC
- **Manual triggers** from GitHub Actions tab
- **Clean format** without icons, proper time formatting

## ⚙️ **Setup Required**

1. **Add PAT Token to Repository Secrets:**
   - Go to repository Settings → Secrets and variables → Actions
   - Add secret: `PAT_TOKEN` with your GitHub token

2. **Enable Repository Permissions:**
   - Go to repository Settings → Actions → General
   - Enable "Read and write permissions"
   - Check "Allow GitHub Actions to create and approve pull requests"

3. **Commit and push** all files to GitHub

## 🎯 **Expected Results**

Your README will automatically update with:
- Latest 3 repositories sorted by last push date
- Clean format without icons
- Proper time formatting ("Updated today", "a day ago", etc.)
- Only shows descriptions when available

## 📋 **Manual Usage**

```bash
# Windows
update_readme.bat

# Or run Python directly
python update_readme.py
```

Your README will stay perfectly up-to-date with your latest work! 🎉
