# Fix GitHub Actions Permissions

The error you're seeing is due to insufficient permissions for the GitHub Actions bot to push changes to your repository.

## 🔧 **Quick Fix Steps**

### **1. Enable Workflow Permissions**

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Scroll down to **Actions** → **General**
4. Under **Workflow permissions**, select:
   - ✅ **Read and write permissions**
   - ✅ **Allow GitHub Actions to create and approve pull requests**

### **2. Alternative: Use Personal Access Token**

If the above doesn't work, create a Personal Access Token:

1. Go to GitHub Settings → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Click **Generate new token (classic)**
3. Give it a name like "README Auto-Update"
4. Select scopes:
   - ✅ **repo** (Full control of private repositories)
   - ✅ **workflow** (Update GitHub Action workflows)
5. Click **Generate token**
6. Copy the token (you won't see it again!)

### **3. Add Token to Repository Secrets**

1. Go to your repository → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `PERSONAL_ACCESS_TOKEN`
4. Value: Paste your token
5. Click **Add secret**

### **4. Update Workflow to Use Personal Token**

Replace the checkout step in `.github/workflows/update-readme.yml`:

```yaml
- name: Checkout repository
  uses: actions/checkout@v4
  with:
    token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
    fetch-depth: 0
```

## 🚀 **Test the Fix**

1. **Commit and push** the updated workflow
2. Go to **Actions** tab
3. Click **"Run workflow"** to test manually
4. Check if the README gets updated successfully

## 🔍 **Troubleshooting**

### **If still getting permission errors:**

1. **Check token permissions** - Make sure the token has `repo` scope
2. **Verify secret name** - Must be exactly `PERSONAL_ACCESS_TOKEN`
3. **Check repository settings** - Ensure Actions are enabled
4. **Try different token** - Generate a new token if needed

### **Alternative Solution:**

If you prefer not to use personal tokens, you can:

1. **Disable auto-commit** in the workflow
2. **Manual review process** - Actions will create a PR instead of direct push
3. **Use different approach** - Run the script locally and commit manually

## ✅ **Expected Result**

After fixing permissions, you should see:
- ✅ Actions run successfully
- ✅ README gets updated automatically
- ✅ Changes are committed and pushed
- ✅ No more permission errors

The workflow will now work with instant updates as designed!
