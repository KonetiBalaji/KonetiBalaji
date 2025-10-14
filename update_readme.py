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

class GitHubRepoUpdater:
    def __init__(self, username="KonetiBalaji"):
        self.username = username
        self.api_base = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "README-Updater"
        }
        
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
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code != 200:
                print(f"API Error: {response.text}")
                return []
            
            repos = response.json()
            return repos[:count]  # Ensure we only get the requested number
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repositories: {e}")
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
        
        section += "---"
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
                print("No repositories found or error occurred")
                return False
            
            # Format repository information
            formatted_repos = [self.format_repo_info(repo) for repo in repos_data]
            
            # Generate new Goals & Focus section
            new_section = self.generate_goals_focus_section(formatted_repos)
            
            # Replace the Goals & Focus section in README
            # Pattern to match the Goals & Focus section
            pattern = r'## 🎯 Goals & Focus.*?(?=---)'
            
            if re.search(pattern, content, re.DOTALL):
                updated_content = re.sub(pattern, new_section, content, flags=re.DOTALL)
            else:
                print("Goals & Focus section not found in README")
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
    print("Updating README.md with latest repositories...")
    
    updater = GitHubRepoUpdater()
    success = updater.update_readme()
    
    if success:
        print("\nREADME update completed successfully!")
    else:
        print("\nREADME update failed!")

if __name__ == "__main__":
    main()
