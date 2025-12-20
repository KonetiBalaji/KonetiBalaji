#!/usr/bin/env python3
"""
Dynamic README Updater for KonetiBalaji
Fetches latest 3 public repositories and updates the Goals & Focus section
"""

import requests
import json
from datetime import datetime
import os
import re
import sys

# Fix Windows encoding for emojis
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class GitHubRepoUpdater:
    def __init__(self, username="KonetiBalaji", token=None):
        self.username = username
        self.api_base = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "README-Updater"
        }
        # Use token if provided (from GITHUB_TOKEN or PAT_TOKEN)
        if token:
            self.headers["Authorization"] = f"token {token}"
        
    def get_latest_repos(self, count=3):
        """Fetch the latest public repositories sorted by last push date"""
        try:
            # Get user's public repositories
            url = f"{self.api_base}/users/{self.username}/repos"
            params = {
                "type": "public",
                "sort": "pushed",
                "direction": "desc",
                "per_page": count
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 403:
                error_data = response.json() if response.content else {}
                if "rate limit" in error_data.get("message", "").lower():
                    print(f"❌ Rate limit exceeded. Please wait or use a GitHub token.")
                    print(f"   Remaining requests: {response.headers.get('X-RateLimit-Remaining', 'unknown')}")
                else:
                    print(f"❌ API Error (403 Forbidden): {error_data.get('message', response.text)}")
                return []
            
            if response.status_code != 200:
                error_msg = response.text
                try:
                    error_data = response.json()
                    error_msg = error_data.get("message", error_msg)
                except:
                    pass
                print(f"❌ API Error ({response.status_code}): {error_msg}")
                return []
            
            repos = response.json()
            if not repos:
                print(f"⚠️  No public repositories found for user: {self.username}")
                return []
            
            return repos[:count]  # Ensure we only get the requested number
            
        except requests.exceptions.Timeout:
            print(f"❌ Request timeout: GitHub API took too long to respond")
            return []
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching repositories: {e}")
            return []
    
    def format_repo_info(self, repo):
        """Format repository information for display"""
        # Calculate days since last push
        last_push = datetime.fromisoformat(repo['pushed_at'].replace('Z', '+00:00'))
        days_ago = (datetime.now(last_push.tzinfo) - last_push).days
        
        # Get repository language or default
        language = repo.get('language', 'Code')
        
        # Truncate description if too long
        description = repo.get('description') or 'No description available'
        if description and len(description) > 100:
            description = description[:97] + "..."
        
        return {
            'name': repo['name'],
            'url': repo['html_url'],
            'description': description,
            'language': language,
            'stars': repo['stargazers_count'],
            'forks': repo['forks_count'],
            'days_ago': days_ago,
            'last_push': last_push.strftime('%Y-%m-%d')
        }
    
    def format_time_ago(self, days_ago):
        """Format the time ago string properly"""
        if days_ago == 0:
            return "today"
        elif days_ago == 1:
            return "a day ago"
        else:
            return f"{days_ago} days ago"
    
    def generate_goals_focus_section(self, repos):
        """Generate the Goals & Focus section with latest repositories"""
        if not repos or len(repos) == 0:
            return """## 🎯 Goals & Focus
- Building scalable AI/ML solutions for social and enterprise impact  
- Contributing to open-source data visualization projects  
- Advancing cloud and ML ops deployment workflows"""
        
        section = "## 🎯 Goals & Focus\n"
        section += "Currently working on my latest projects:\n\n"
        
        for i, repo in enumerate(repos, 1):
            section += f"### [{repo['name']}]({repo['url']})\n"
            
            # Only show description if it's available and not the default message
            if repo['description'] and repo['description'] != 'No description available':
                section += f"**{repo['description']}**  \n"
            
            # Format the time string properly
            time_str = self.format_time_ago(repo['days_ago'])
            section += f"*Updated {time_str}*\n\n"
        
        section += "\n---"
        return section
    
    def update_readme(self, readme_path="README.md"):
        """Update the README.md file with latest repository information"""
        try:
            # Read current README
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Get latest repositories
            repos_data = self.get_latest_repos(3)
            if not repos_data:
                print("❌ No repositories found or error occurred")
                print("   This could be due to:")
                print("   - Rate limiting (use GITHUB_TOKEN or PAT_TOKEN)")
                print("   - No public repositories")
                print("   - Network/API issues")
                return False
            
            # Format repository information
            formatted_repos = [self.format_repo_info(repo) for repo in repos_data]
            
            # Generate new Goals & Focus section
            new_section = self.generate_goals_focus_section(formatted_repos)
            
            # Replace the Goals & Focus section in README
            # Pattern to match the Goals & Focus section until the next section (--- or more dashes)
            # Match from "## 🎯 Goals & Focus" until the next section header (##)
            pattern = r'## 🎯 Goals & Focus.*?(?=\n## |\n---)'
            
            if re.search(pattern, content, re.DOTALL):
                updated_content = re.sub(pattern, new_section, content, flags=re.DOTALL)
            else:
                print("❌ Goals & Focus section not found in README")
                print("   Looking for pattern: '## 🎯 Goals & Focus'")
                return False
            
            # Write updated content
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print("README.md updated successfully!")
            print(f"Updated with {len(formatted_repos)} latest repositories:")
            for repo in formatted_repos:
                time_str = self.format_time_ago(repo['days_ago'])
                print(f"   - {repo['name']} (last updated {time_str})")
            
            return True
            
        except FileNotFoundError:
            print(f"README.md not found at {readme_path}")
            return False
        except Exception as e:
            print(f"Error updating README: {e}")
            return False

def main():
    """Main function to run the updater"""
    print("🔄 Updating README.md with latest repositories...")
    print(f"   Username: KonetiBalaji")
    
    # Try to get token from environment (GitHub Actions provides GITHUB_TOKEN)
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("PAT_TOKEN")
    if token:
        print("   ✅ Using GitHub token for API authentication")
    else:
        print("   ⚠️  No token found - using unauthenticated requests (rate limited)")
    
    updater = GitHubRepoUpdater(token=token)
    success = updater.update_readme()
    
    if success:
        print("\n✅ README update completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ README update failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
