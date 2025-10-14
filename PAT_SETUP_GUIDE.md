# Personal Access Token (PAT) Setup Guide

This guide will help you set up a Personal Access Token for your README update workflow.

## 🔐 **Step 1: Create Personal Access Token**

### **Option A: Fine-grained Token (Recommended)**
1. Go to **GitHub** → **Settings** → **Developer settings** → **Personal Access Tokens** → **Fine-grained tokens**
2. Click **"Generate new token"**
3. Fill in the details:
   - **Token name**: `README Update Token`
   - **Expiration**: Choose your preferred expiration (e.g., 1 year)
   - **Repository access**: Select **"Selected repositories"**
   - **Repositories**: Select your profile repository (`KonetiBalaji/KonetiBalaji`)

4. **Permissions**:
   - ✅ **Contents**: Read and write
   - ✅ **Metadata**: Read
   - ✅ **Pull requests**: Write (if using PR workflow)

5. Click **"Generate token"**
6. **Copy the token** (you won't see it again!)

### **Option B: Classic Token (Alternative)**
1. Go to **GitHub** → **Settings** → **Developer settings** → **Personal Access Tokens** → **Tokens (classic)**
2. Click **"Generate new token (classic)"**
3. Fill in the details:
   - **Note**: `README Update Token`
   - **Expiration**: Choose your preferred expiration
   - **Scopes**: Select **`repo`** (Full control of private repositories)

4. Click **"Generate token"**
5. **Copy the token** (you won't see it again!)

## 🔧 **Step 2: Add Token to Repository Secrets**

1. Go to your repository: `https://github.com/KonetiBalaji/KonetiBalaji`
2. Click **"Settings"** tab
3. Navigate to **"Secrets and variables"** → **"Actions"**
4. Click **"New repository secret"**
5. Fill in:
   - **Name**: `PAT_TOKEN`
   - **Secret**: Paste your token here
6. Click **"Add secret"**

## ⚙️ **Step 3: Choose Your Workflow**

### **Option A: Direct Commit (Recommended)**
```bash
# Run the setup script
python setup-workflow.py
# Choose option 1 (Direct Commit)
```

### **Option B: Pull Request**
```bash
# Run the setup script  
python setup-workflow.py
# Choose option 2 (Pull Request)
```

## 🧪 **Step 4: Test the Setup**

### **Test 1: Manual Trigger**
1. Go to your repository → **Actions** tab
2. Click **"Update README with Latest Repos"**
3. Click **"Run workflow"**
4. Check if it runs successfully

### **Test 2: Push Trigger**
1. Make a small change to any file
2. Commit and push to main branch
3. Check if the workflow triggers automatically

### **Test 3: Repository Dispatch**
```bash
# Set your token as environment variable
export GITHUB_TOKEN=your_token_here

# Run the trigger script
python trigger_readme_update.py
```

## 🔍 **Troubleshooting**

### **If you get permission errors:**
1. ✅ Verify the token has correct permissions
2. ✅ Check that the secret name is exactly `PAT_TOKEN`
3. ✅ Ensure the token hasn't expired
4. ✅ Verify the repository access in token settings

### **If the workflow doesn't trigger:**
1. ✅ Check that the workflow file is in `.github/workflows/`
2. ✅ Verify the workflow syntax is correct
3. ✅ Ensure Actions are enabled in repository settings

### **If PRs are created but not merged:**
1. ✅ Enable auto-merge in repository settings
2. ✅ Or manually merge the PRs when created
3. ✅ The workflow will clean up branches automatically

## 📊 **Token Security Best Practices**

### **Fine-grained Token (Recommended)**
- ✅ **Scoped to specific repository**
- ✅ **Limited permissions**
- ✅ **Better security**
- ✅ **Easier to manage**

### **Classic Token (Alternative)**
- ⚠️ **Full repository access**
- ⚠️ **Broader permissions**
- ⚠️ **Less secure**
- ✅ **Easier to set up**

## 🎯 **Expected Results**

After setup, your workflow will:
- ✅ **Trigger on push** to main/master branch
- ✅ **Update README** with latest 3 repositories
- ✅ **Create PRs** (if using PR workflow) or **direct commits**
- ✅ **Run daily** at 6 AM UTC as backup
- ✅ **Work with manual triggers**

## 🚀 **Next Steps**

1. **Create the PAT token** using the steps above
2. **Add it to repository secrets** as `PAT_TOKEN`
3. **Choose your workflow** (direct commit or PR)
4. **Test the setup** with manual triggers
5. **Commit and push** your changes

Your README will now update automatically with your latest repositories! 🎉
