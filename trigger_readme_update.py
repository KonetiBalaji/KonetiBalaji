#!/usr/bin/env python3
"""
Trigger README Update Script
This script can be used to trigger README updates from other repositories
"""

import requests
import os
import sys

def trigger_readme_update():
    """Trigger README update via GitHub API"""
    
    # Get GitHub token from environment or input
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("Please set GITHUB_TOKEN environment variable")
        print("You can get a token from: https://github.com/settings/tokens")
        return False
    
    # Repository details
    owner = "KonetiBalaji"  # Your GitHub username
    repo = "KonetiBalaji"   # Your profile repository name
    
    # GitHub API endpoint for repository dispatch
    url = f"https://api.github.com/repos/{owner}/{repo}/dispatches"
    
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "README-Update-Trigger"
    }
    
    payload = {
        "event_type": "update-readme",
        "client_payload": {
            "message": "Repository activity detected - updating README",
            "triggered_by": "repository_activity"
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 204:
            print("README update triggered successfully!")
            print("Your README will be updated within a few minutes.")
            return True
        else:
            print(f"Failed to trigger update: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Error triggering update: {e}")
        return False

def main():
    """Main function"""
    print("Triggering README update...")
    
    success = trigger_readme_update()
    
    if success:
        print("\nREADME update process started!")
        print("Check your repository's Actions tab to see the progress.")
    else:
        print("\nFailed to trigger README update!")
        print("Make sure you have a valid GITHUB_TOKEN set.")

if __name__ == "__main__":
    main()
