#!/usr/bin/env python3
"""
Workflow Setup Script
Helps you choose between direct commit and pull request workflows
"""

import os
import shutil

def setup_direct_commit():
    """Setup direct commit workflow"""
    print("Setting up direct commit workflow...")
    
    # Disable PR workflow
    if os.path.exists('.github/workflows/update-readme.yml'):
        shutil.move('.github/workflows/update-readme.yml', '.github/workflows/update-readme-pr.yml.disabled')
        print("✅ Disabled PR workflow")
    
    # Enable direct commit workflow
    if os.path.exists('.github/workflows/update-readme-direct.yml'):
        shutil.move('.github/workflows/update-readme-direct.yml', '.github/workflows/update-readme.yml')
        print("✅ Enabled direct commit workflow")
    
    print("\n🎉 Direct commit workflow is now active!")
    print("Your README will be updated directly to the main branch.")
    print("\n📋 Next steps:")
    print("1. Go to repository Settings → Actions → General")
    print("2. Enable 'Read and write permissions'")
    print("3. Check 'Allow GitHub Actions to create and approve pull requests'")
    print("4. Save the settings")

def setup_pull_request():
    """Setup pull request workflow"""
    print("Setting up pull request workflow...")
    
    # Disable direct commit workflow
    if os.path.exists('.github/workflows/update-readme-direct.yml'):
        shutil.move('.github/workflows/update-readme-direct.yml', '.github/workflows/update-readme-direct.yml.disabled')
        print("✅ Disabled direct commit workflow")
    
    # Enable PR workflow
    if os.path.exists('.github/workflows/update-readme-pr.yml.disabled'):
        shutil.move('.github/workflows/update-readme-pr.yml.disabled', '.github/workflows/update-readme.yml')
        print("✅ Enabled PR workflow")
    
    print("\n🎉 Pull request workflow is now active!")
    print("Your README updates will be created as pull requests.")
    print("\n📋 Next steps:")
    print("1. Go to repository Settings → Actions → General")
    print("2. Enable 'Read and write permissions'")
    print("3. Check 'Allow GitHub Actions to create and approve pull requests'")
    print("4. Save the settings")
    print("5. Manually merge PRs when they're created (or enable auto-merge)")

def main():
    """Main function"""
    print("🚀 README Update Workflow Setup")
    print("=" * 40)
    print()
    print("Choose your preferred workflow:")
    print()
    print("1. Direct Commit (Recommended)")
    print("   ✅ Simple setup")
    print("   ✅ No PRs to manage")
    print("   ✅ Direct updates to main branch")
    print()
    print("2. Pull Request")
    print("   ✅ Review changes before merging")
    print("   ✅ Better for team collaboration")
    print("   ❌ Requires manual PR merging")
    print()
    
    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == '1':
            setup_direct_commit()
            break
        elif choice == '2':
            setup_pull_request()
            break
        else:
            print("Please enter 1 or 2")
    
    print("\n🎯 Workflow setup complete!")
    print("Commit and push these changes to activate the workflow.")

if __name__ == "__main__":
    main()
