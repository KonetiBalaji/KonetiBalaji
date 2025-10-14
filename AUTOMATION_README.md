# Dynamic README Automation

This setup automatically updates your README.md with your latest 3 public repositories based on their last push date.

## Files Created

- `update_readme.py` - Main Python script that fetches and updates repositories
- `requirements.txt` - Python dependencies
- `.github/workflows/update-readme.yml` - GitHub Actions workflow for automation
- `update_readme.bat` - Windows batch script for manual execution

## How It Works

1. **Fetches Latest Repos**: Uses GitHub API to get your 3 most recently updated public repositories
2. **Updates Goals & Focus**: Replaces the hardcoded Goals & Focus section with dynamic content
3. **Shows Repository Info**: Displays repository name, description, language, stars, forks, and last update date

## Manual Usage

### Windows
```bash
# Run the batch file
update_readme.bat

# Or run Python directly
python update_readme.py
```

### Linux/Mac
```bash
python3 update_readme.py
```

## Automated Usage (GitHub Actions)

The GitHub Actions workflow will:
- Run daily at 6 AM UTC
- Automatically commit changes to your README
- Can be triggered manually from GitHub Actions tab

## Customization

You can modify the script to:
- Change the number of repositories shown (default: 3)
- Modify the section format
- Add more repository information
- Change the update frequency

## Requirements

- Python 3.7+
- `requests` library
- GitHub account with public repositories

## Troubleshooting

- Ensure your repositories have descriptions for better display
- Check GitHub API rate limits if you have many repositories
- Verify the regex pattern matches your README structure
